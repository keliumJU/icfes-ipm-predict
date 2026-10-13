"""Runner serial terminable y ledger persistente con plazo único no renovable."""
from comun import *
import signal, numpy as np

class BudgetError(RuntimeError): pass
class InfrastructureFailure(RuntimeError): pass

class Ledger:
    def __init__(self,folder,context,limit=7200,synthetic=False):
        self.folder=folder; self.path=safe_path(HERE,folder+'/ledger.json')
        if self.path.exists():
            self.state=load(self.path)
            assert self.state['context']==context and self.state['limit']==limit and self.state['synthetic']==synthetic
            for r in self.state['attempts']:
                if r['state']=='pending':
                    r['state']='unknown_crash'; self.state.update(used=limit,exhausted=True,closed=True); self.save()
                    raise BudgetError('Caída sin tiempo medido; saldo agotado')
                if r['state']=='success': assert digest(safe_path(HERE,r['output']))==r['output_sha256']
            if self.state.get('closed'): raise BudgetError('Presupuesto cerrado: no reiniciar')
        else:
            self.state={'version':'1.0.0','context':context,'limit':limit,'synthetic':synthetic,'start_monotonic':time.monotonic(),
                'start_wall':time.time(),'used':0.0,'attempts':[],'retries':0,'closed':False,'exhausted':False,
                'medicion':'Tiempo monotónico continuo desde arranque del runner hasta cierre: incluye procesos, comunicación, fallos, retries, repeticiones y pausas. Sin saldo heredado.'}
            self.save()
    def save(self):
        folder=safe_path(HERE,self.folder+'/historia'); folder.mkdir(parents=True,exist_ok=True)
        seq=len(list(folder.glob('*.json')))
        fresh(self.folder+f'/historia/{seq:04d}.json',self.state); write(self.folder+'/ledger.json',self.state)
    def tick(self):
        elapsed=time.monotonic()-self.state['start_monotonic']
        if elapsed<self.state['used']: raise IntegrityError('Reloj/consumo retrocede')
        self.state['used']=min(elapsed,self.state['limit'])
        if elapsed>=self.state['limit']: self.state['exhausted']=True
        return self.state['limit']-self.state['used']
    def close(self):
        self.tick(); self.state['closed']=True; self.save()
    def run(self,levels,evaluated,role,candidate,job,mode=None,timeout=None):
        p=prepare(levels,evaluated,role); ctx=prepared_context(p,candidate)
        previous=[r for r in self.state['attempts'] if r['job']==job]
        if previous:
            if previous[-1]['context']!=ctx: raise IntegrityError('Contexto cambiado')
            if previous[-1]['state']=='success': return load(safe_path(HERE,previous[-1]['output']))
            if previous[-1]['state']=='numerical': return load(safe_path(HERE,previous[-1]['output']))
            raise InfrastructureFailure('Trabajo fallido previo: no repetición silenciosa')
        if mode and not self.state['synthetic']: raise IntegrityError('Inyección solo sintética')
        if candidate=='persistencia' or not p.supervised_years:
            start=time.monotonic(); result=fit_predict(p,candidate)
            evidence=serial_prepared(p,candidate)
            evidence.update(state='success',score=result['score'].tolist(),delta=result['delta'].tolist(),reason=result['reason'],fits=0,pipelines={},warnings=[],seconds_worker=time.monotonic()-start,synthetic=self.state['synthetic'])
            output=self.folder+'/jobs/'+job+'/respaldo.json'; fresh(output,evidence)
            self.state['attempts'].append({'job':job,'context':ctx,'state':'success','output':output,'output_sha256':digest(safe_path(HERE,output)),
                'attempt':1,'pipeline_fits_started':0,'seconds_measured':evidence['seconds_worker'],'no_fit':True})
            if self.tick()<=0: raise BudgetError('Límite en respaldo')
            self.save(); return evidence
        for attempt in (1,2):
            remaining=self.tick()
            if remaining<=0: raise BudgetError('Sin saldo')
            base=self.folder+'/jobs/'+job+f'/intento_{attempt}'
            output=base+'/resultado.json'; progress=base+'/progreso.json'; request=base+'/solicitud.json'
            # Solo niveles anteriores; objetivo se lee en padre después de predicción.
            req={'levels':{str(y):levels[y] for y in YEARS if y<evaluated},'evaluated':evaluated,'role':role,'candidate':candidate,
                'context':ctx,'output':output,'progress':progress,'synthetic':self.state['synthetic'],'mode':mode}
            fresh(request,req)
            record={'job':job,'attempt':attempt,'context':ctx,'state':'pending','request':request,'request_sha256':digest(safe_path(HERE,request)),
                'output':output,'start_monotonic':time.monotonic()}
            self.state['attempts'].append(record); self.save()
            proc=None; out=b''; err=b''; state='infrastructure'
            try:
                proc=subprocess.Popen([sys.executable,str(HERE/'worker.py'),request],stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),start_new_session=True)
                record['pid']=proc.pid
                out,err=proc.communicate(timeout=min(remaining,timeout) if timeout is not None else remaining)
                state={0:'success',2:'numerical',4:'integrity'}.get(proc.returncode,'infrastructure')
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGTERM)
                try: out,err=proc.communicate(timeout=0.2)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid,signal.SIGKILL); out,err=proc.communicate()
                state='timeout'
            except BaseException as exc:
                if proc and proc.poll() is None:
                    os.killpg(proc.pid,signal.SIGKILL); out,err=proc.communicate()
                record['exception']=repr(exc)
                if isinstance(exc,(KeyboardInterrupt,SystemExit)): state='interrupted'
            record.update(state=state,seconds_measured=time.monotonic()-record['start_monotonic'],
                returncode=proc.returncode if proc else None,process_terminated=proc is None or proc.poll() is not None)
            safe_path(HERE,base+'/stdout.txt').write_bytes(out); safe_path(HERE,base+'/stderr.txt').write_bytes(err)
            fitprogress=load(safe_path(HERE,progress)) if safe_path(HERE,progress).exists() else {'fits':[]}
            record['pipeline_fits_started']=len(fitprogress['fits'])
            if safe_path(HERE,output).exists(): record['output_sha256']=digest(safe_path(HERE,output))
            self.tick(); self.save()
            if self.state['exhausted'] or state in ('timeout','interrupted'): raise BudgetError(state)
            if state=='integrity': raise IntegrityError('Worker rechazó integridad')
            if state in ('success','numerical'):
                result=load(safe_path(HERE,output))
                assert result['context']==ctx and result['state']==state
                return result
            if attempt==2 or self.state['retries']>=1: raise InfrastructureFailure('Máximo un retry infraestructura en piloto')
            self.state['retries']+=1; self.save()

def prediction_rows(res,levels,external,validation=None,policy=None):
    evaluated=validation or external
    rows=[]
    for i,code in enumerate(CODES):
        row={'external':external,'validation':evaluated,'candidate':res['candidate'],'code':code,
             'observed':levels[evaluated][code],'predicted':res['score'][i],'delta':res['delta'][i],
             'previous_score':res['previous_score'][i],'previous_year':res['previous_year'],
             'interval':evaluated-res['previous_year'],'context':res['context'],'reason':res['reason']}
        if policy is not None: row['policy']=policy
        rows.append(row)
    return rows

def execute(levels,ledger):
    internal=[]; external_rows=[]; records=[]; selections=[]; checks=[]
    for w in [window(y) for y in YEARS[2:]]:
        ext=w['externo']; selected='persistencia'
        if ext!=2021:
            candidate_records=[]
            for candidate in CANDIDATES:
                pool=[]; failures=[]
                for v in w['internas']:
                    val=v['validacion']; job=f'int_e{ext}_v{val}_{candidate}'
                    res=ledger.run(levels,val,'interna',candidate,job)
                    if res['state']=='numerical': failures.append({'validation':val,'reason':res['reason']}); continue
                    rows=prediction_rows(res,levels,ext,val); pool.extend(rows); internal.extend(rows)
                if failures:
                    rec={'external':ext,'role':'interna','candidate':candidate,'eligible':False,'n':len(pool),'reason':json.dumps(failures)}
                else:
                    rec={'external':ext,'role':'interna','candidate':candidate,'eligible':True,'reason':'cobertura completa',
                         **metrics([r['observed'] for r in pool],[r['predicted'] for r in pool])}
                candidate_records.append(rec)
            choice=select_internal(ext,candidate_records); selected=choice['candidate']
            for rec in candidate_records: rec['selected']=rec['candidate']==selected
            records.extend(candidate_records); selections.append({'external':ext,**choice})
            # Persiste decisión ANTES de ajustes/predicciones externas de la ventana.
            fresh(ledger.folder+f'/selecciones/e{ext}.json',{'records':candidate_records,'choice':choice})
        outputs={}
        for candidate in CANDIDATES:
            res=ledger.run(levels,ext,'externa',candidate,f'ext_e{ext}_{candidate}')
            if res['state']=='numerical': raise NumericalFailure('Cobertura externa incompleta: '+candidate)
            outputs[candidate]=res
            external_rows.extend(prediction_rows(res,levels,ext,policy=candidate))
        source=outputs[selected]
        score=reuse_global({'candidate':selected,'score':source['score']},selected,ext,selected,ext)
        global_res=dict(source,score=score.tolist())
        external_rows.extend(prediction_rows(global_res,levels,ext,policy='global'))
        if selected=='persistencia':
            p=prepare(levels,ext,'externa'); assert np.array_equal(score,p.previous_score)
            checks.append({'external':ext,'candidate':selected,'mode':'previo exacto sin fit','max_difference':0.0,'approved':True,'context':source['context']})
        else:
            repeat=ledger.run(levels,ext,'externa',selected,f'rep_e{ext}_{selected}')
            if repeat['state']!='success': raise NumericalFailure('Repetición global fallida')
            assert repeat['context']==source['context']
            diff=float(np.max(np.abs(np.asarray(repeat['score'])-score)))
            np.testing.assert_allclose(repeat['score'],score,atol=1e-10,rtol=0)
            checks.append({'external':ext,'candidate':selected,'mode':'repetición mismo contexto','max_difference':diff,'approved':True,'context':source['context']})
        fresh(ledger.folder+f'/ventanas/e{ext}.json',{'internas':[r for r in internal if r['external']==ext],
            'externas':[r for r in external_rows if r['external']==ext],'global_check':checks[-1]})
        print(json.dumps({'external':ext,'selected_by_internal':selected,'internal_rows':len(internal),'external_rows':len(external_rows),'used_seconds':ledger.state['used']}),flush=True)
    exact_coverage([(r['external'],r['validation'],r['candidate'],r['code']) for r in internal],expected_internal_keys())
    exact_coverage([(r['external'],r['policy'],r['code']) for r in external_rows],expected_external_keys())
    unique,links=lineage(internal)
    assert len(internal)==1320 and len(unique)==528 and len(records)==16 and len(external_rows)==825 and len(checks)==5
    started=sum(r.get('pipeline_fits_started',0) for r in ledger.state['attempts'])
    if ledger.state['retries']==0: assert 40<=started<=46
    return {'internal':internal,'external':external_rows,'records':records,'selections':selections,'unique':unique,'lineage':links,'global_checks':checks,'pipeline_fits_started':started}
