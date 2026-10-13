"""Piloto único serial; subprocesos terminables, ledger durable sin reapertura."""
from motor import *
import time, signal, traceback
PILOT=HERE/'fase2/piloto'
def worker(request,result,events):
    req=load(request); seq=[]
    def progress(x):
        seq.append(dict(monotonic=time.monotonic(),**x));save(events,seq)
    try:
        if req.get('test_sleep'):
            time.sleep(req['test_sleep']);save(result,dict(ok=True));return
        if req.get('test_fail'): raise OSError('infraestructura inventada')
        cand=req['candidate'];out=estimate(cand,req['context'],progress)
        out['versions']=load(HERE/'ENTORNO_DOCUMENTAL.json')['lock'];save(result,out)
    except Exception as e:
        save(result,dict(error=type(e).__name__,message=str(e),kind='infraestructura' if isinstance(e,OSError) else 'numerico_integridad',traceback=traceback.format_exc()))
        sys.exit(2)
class Ledger:
    def __init__(self,folder,seconds=7200):
        self.folder=safe(folder);self.path=self.folder/'ledger.json'
        check(not self.path.exists(),'ledger existente; prohibido reabrir')
        self.start=time.monotonic();self.index=0
        self.state=dict(status='abierto',budget_seconds=seconds,start_monotonic=self.start,start_wall=time.time(),elapsed_seconds=0,fits_started=0,fits_completed=0,statistical_estimates=0,retries=0,failures=0,pending=None,events=[],serial=True)
        self.persist()
    def persist(self):
        self.state['elapsed_seconds']=time.monotonic()-self.start
        save(self.folder/'snapshots'/f'{self.index:04d}.json',self.state);self.index+=1;save(self.path,self.state)
    def remaining(self):return self.state['budget_seconds']-(time.monotonic()-self.start)
    def close(self,complete,error=None):
        check(self.state['status']=='abierto','no reapertura')
        self.state.update(status='cerrado_completo' if complete else 'cerrado_incompleto',error=error,end_wall=time.time(),pending=None)
        self.persist()
    def task(self,name,request):
        check(self.state['status']=='abierto' and self.state['pending'] is None,'serial abierto')
        base=self.folder/'jobs'/name;save(base/'request.json',request)
        attempt=0
        while True:
            check(self.remaining()>0,'timeout presupuesto')
            suffix=str(attempt);result=base/('result_'+suffix+'.json');events=base/('events_'+suffix+'.json')
            self.state['pending']=dict(name=name,attempt=attempt,request_sha=sha(base/'request.json'),start=time.monotonic());self.persist()
            process=subprocess.Popen([sys.executable,str(HERE/'runner.py'),'--worker',str(base/'request.json'),str(result),str(events)],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1'),start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.state['pending']['pid']=process.pid;self.persist();timeout=False
            try:stdout,stderr=process.communicate(timeout=max(0.001,self.remaining()))
            except subprocess.TimeoutExpired:
                timeout=True;os.killpg(process.pid,signal.SIGTERM)
                try:stdout,stderr=process.communicate(timeout=2)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);stdout,stderr=process.communicate()
            seq=load(events) if events.exists() else []
            for counter in ['fits_started','fits_completed','statistical_estimates']:self.state[counter]+=sum(x.get(counter,0) for x in seq)
            outcome=load(result) if result.exists() else dict(error='sin resultado',kind='infraestructura')
            ev=dict(name=name,attempt=attempt,pid=process.pid,returncode=process.returncode,terminated=process.poll() is not None,timeout=timeout,events_sha=sha(events) if events.exists() else None,result_sha=sha(result) if result.exists() else None,stderr=stderr.decode(),duration=time.monotonic()-self.state['pending']['start'],ok=process.returncode==0 and not timeout and 'error' not in outcome)
            self.state['events'].append(ev);self.state['pending']=None;self.persist()
            if ev['ok']:return outcome
            self.state['failures']+=1;self.persist()
            if not timeout and outcome.get('kind')=='infraestructura' and self.state['retries']==0:
                self.state['retries']+=1;attempt+=1;self.persist();continue
            raise RuntimeError('Trabajo incompleto '+name+': '+str(outcome.get('message',outcome.get('error'))))
def reject_crashed(path):
    """Una caída sin cierre medido agota conservadoramente; nunca reanuda."""
    x=load(path);check(x['status']=='abierto','solo caída abierta')
    x.update(status='cerrado_incompleto',elapsed_seconds=x['budget_seconds'],pending_unmeasured=True,error='caída sin medición; saldo agotado conservadoramente')
    save(path,x);return x
def rows(out,p,kind,external=None):
    y=out['context']['year'];return [dict(id=out['context']['id'],year=y,code=j,observed=float(p['levels'][y][i]),previous=float(out['context']['previous_score'][i]),predicted=out['prediction'][i],predicted_delta=out['predicted_delta'][i],kind=kind,external=external,context_sha=hashlib.sha256(json.dumps(out['context'],sort_keys=True).encode()).hexdigest()) for i,j in enumerate(p['codes'])]
def writecsv(path,records):
    path=safe(path);path.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(records).to_csv(path,index=False,float_format='%.17g')
def run():
    # Validación de freeze antes de crear un presupuesto nuevo.
    f=load(HERE/'fase1/CONGELACION.json')
    for s,h in f['sha256'].items():check(sha(HERE/s)==h,'freeze '+s)
    check(load(HERE/'fase1/ACEPTACION.json')['completa'],'fase1 aceptada')
    environment();conservation();defaults()
    ledger=Ledger(PILOT);complete=False;error=None
    try:
        p=panel();spec=load(HERE/'ESPECIFICACION_V6.json');cands=spec['candidates'];unique={};original=[];external=[];selections=[];lineage=[];checks=[]
        # Seis contextos internos ajustables (2022,23,24) × candidatos; 2021 respaldo.
        for y in [2021,2022,2023,2024]:
            for cand in cands:
                out=ledger.task(f'interno_{y}_{cand["id"]}',dict(candidate=cand,context=context(p,cand,y)))
                unique[(y,cand['id'])]=out
        for window in spec['windows']:
            y=window['externo'];decision=None
            if y>2021:
                records=[]
                for cand in cands:
                    rr=[]
                    for internal in window['internas']:
                        iy=internal['validacion'];r=rows(unique[(iy,cand['id'])],p,'interna',y);original+=r;rr+=r
                        for row in r:lineage.append(dict(external=y,id=cand['id'],year=iy,code=row['code'],representative_external=iy+1,context_sha=row['context_sha']))
                    records.append(dict(id=cand['id'],inputs=cand['inputs'],order=cand['order'],**metrics([r['predicted'] for r in rr],[r['observed'] for r in rr])))
                decision=select(records);decision['external']=y;decision['created_monotonic']=time.monotonic()
                save(PILOT/'selections'/f'{y}.json',decision);selections+= [dict(external=y,selected=decision['winner'],pool_mae=r['id'] in decision['pool_mae'],pool_rmse=r['id'] in decision['pool_rmse'],**r) for r in records]
            outs={}
            for cand in cands:
                out=ledger.task(f'externo_{y}_{cand["id"]}',dict(candidate=cand,context=context(p,cand,y))) if y>2021 else dict(context=context(p,cand,y),prediction=p['levels'][p['previous'][y]].tolist(),predicted_delta=[0.0]*33,state='externa_fija',fits=0,statistical_estimates=0,metadata={})
                outs[cand['id']]=out;external+=rows(out,p,'externa',y)
                save(PILOT/'externals'/f'{y}_{cand["id"]}.json',out)
            chosen=decision['winner'] if decision else 'persistencia';out=outs[chosen]
            cand=next(c for c in cands if c['id']==chosen)
            if y==2021 or cand['family']=='persistencia':
                repeated=dict(prediction=p['levels'][p['previous'][y]].tolist(),fits=0,statistical_estimates=0);method='previo_exacto'
            else:repeated=ledger.task(f'check_global_{y}_{chosen}',dict(candidate=cand,context=context(p,cand,y)));method='constante_recalculada' if not cand['components'] else 'fit_repetido'
            check(np.allclose(out['prediction'],repeated['prediction'],atol=1e-10,rtol=0) if method=='fit_repetido' else np.array_equal(out['prediction'],repeated['prediction']),'global check')
            checks.append(dict(year=y,selected=chosen,method=method,prediction=out['prediction'],repeated=repeated['prediction'],fits=repeated['fits'],statistical_estimates=repeated['statistical_estimates']))
            gr=rows(out,p,'global',y)
            for r in gr:r['source_id']=chosen;r['id']='global_v6'
            external+=gr
        uniques=[r for (y,c),out in unique.items() for r in rows(out,p,'interna',y+1)]
        check(len(original)==12870 and len(uniques)==5148 and len(external)==6600 and len(selections)==156 and len(lineage)==12870 and len(checks)==5,'cobertura indispensable')
        check(ledger.state['fits_started']<=328 and ledger.state['statistical_estimates']<=104,'cotas')
        for n,rs in [('internas_originales',original),('internas_unicas',uniques),('externas',external),('selecciones',selections),('linaje',lineage)]:writecsv(PILOT/(n+'.csv'),rs)
        save(PILOT/'global_checks.json',checks);save(PILOT/'COBERTURA.json',dict(aprobado=True,internal_original=len(original),internal_unique=len(uniques),external=len(external),selection_records=len(selections),lineage=len(lineage),global_checks=len(checks)))
        complete=True
    except Exception as e:error=traceback.format_exc();save(PILOT/'INCIDENCIA.json',dict(error=str(e),traceback=error));raise
    finally:ledger.close(complete,error)
    print(json.dumps(dict(completo=complete,fits=ledger.state['fits_started'],constantes=ledger.state['statistical_estimates'],seconds=ledger.state['elapsed_seconds'])))
if __name__=='__main__':
    if sys.argv[1:2]==['--worker']:worker(*sys.argv[2:])
    elif sys.argv[1:]==['--run']:run()
    else:raise ValueError('usar --run o --worker')
