"""Auditor aritmético independiente. No imports del motor/selector/runner ni fits/cargas."""
from comun import *
import math,statistics,csv
import numpy as np
import pandas as pd
PILOT=HERE/'fase2/piloto'
def equal(a,b,label):check(np.array_equal(np.asarray(a),np.asarray(b)),label)
def error_metrics(pred,obs):
    e=[float(p)-float(o) for p,o in zip(pred,obs)];check(e and all(math.isfinite(x) for x in e),'métricas finitas')
    return dict(MAE=math.fsum(abs(x) for x in e)/len(e),RMSE=math.sqrt(math.fsum(x*x for x in e)/len(e)),bias=math.fsum(e)/len(e),n=len(e))
def independent_selection(records):
    low=min(r['MAE'] for r in records);a=[r for r in records if r['MAE']<=low+.1]
    rm=min(r['RMSE'] for r in a);b=[r for r in a if r['RMSE']<=rm+.1]
    return dict(winner=sorted(b,key=lambda r:(r['inputs'],r['order']))[0]['id'],mae_min=low,rmse_pool_min=rm,pool_mae=[r['id'] for r in a],pool_rmse=[r['id'] for r in b],records=records)
def readpanel():
    spec=load(HERE/'ESPECIFICACION_V6.json');frames=[]
    for s in spec['fuentes']:
        frame=pd.read_csv(ROOT/s,dtype={'codigo_departamento':str},float_precision='round_trip');frame['codigo_departamento']=frame['codigo_departamento'].str.zfill(2)
        frames.append(frame.sort_values(['anio','codigo_departamento']).reset_index(drop=True))
    a,b=frames
    equal(a[['anio','codigo_departamento']],b[['anio','codigo_departamento']],'source keys');equal(a.prom_punt_global,b.prom_punt_global,'source levels')
    codes=sorted(a.codigo_departamento.unique());years=sorted(a.anio.unique().tolist())
    check(years==spec['years'] and len(codes)==33 and len(a)==231 and not a.duplicated(['anio','codigo_departamento']).any(),'panel integrity')
    levels={y:a[a.anio==y].prom_punt_global.to_numpy() for y in years};prior={y:years[i-1] for i,y in enumerate(years) if i};d={y:levels[y]-levels[q] for y,q in prior.items()}
    c={y:statistics.median(v) for y,v in d.items()};r={y:v-c[y] for y,v in d.items()}
    for y in years[1:]:
        rows=b[b.anio==y];equal(rows.cambio_observado,d[y],'derived d');equal(rows.puntaje_previo,levels[prior[y]],'derived prior');check((rows.anio_previo==prior[y]).all(),'prior date')
    return dict(levels=levels,prior=prior,d=d,c=c,r=r,codes=codes,years=years)
def audit_context(ctx,cand,p):
    year=ctx['year'];ys=[y for y in p['years'] if y>=2021 and y<year and y in p['d'] and p['prior'][y] in p['d']]
    if cand['history']!='all':ys=ys[-int(cand['history'].replace('last','')):]
    check(ctx['id']==cand['id'] and ctx['history']==cand['history'] and ctx['eligible_years']==ys and ctx['previous']==p['prior'][year] and ctx['inputs']==cand['inputs'] and ctx['seed']==SEED and ctx['params']==cand['params'] and ctx['units']=='puntos globales; cambio sin anualizar','context contract')
    check(ctx['prediction_keys']==[[j,year] for j in p['codes']],'predict keys')
    equal(ctx['previous_score'],p['levels'][p['prior'][year]],'prior score')
    for saved,field in [('prior_levels','levels'),('prior_d','d'),('prior_c','c'),('prior_r','r')]:
        expected={str(y):np.asarray(v).tolist() for y,v in p[field].items() if y<year}
        check(ctx[saved]==expected,'prior context '+saved)
    check(set(ctx['components'])==set(cand['components']),'component count')
    for comp,dat in ctx['components'].items():
        field={'memoria':'d','comun':'c','correccion':'r'}[comp]
        X=[float(v) for y in ys for v in np.atleast_1d(p[field][p['prior'][y]])];Y=[float(v) for y in ys for v in np.atleast_1d(p[field][y])]
        equal(dat['X'],[[x] for x in X],'X exact');equal(dat['y'],Y,'y exact')
        check(dat['keys']==[[j,y] for y in ys for j in (['comun'] if comp=='comun' else p['codes'])] and dat['previous_years']==[p['prior'][y] for y in ys],'train keys/date')
        equal(dat['predict_X'],[[float(x)] for x in np.atleast_1d(p[field][p['prior'][year]])],'predict X')
        check(len(dat['y'])==len(ys)*(1 if comp=='comun' else 33),'33 vs1')
    if cand['family'] in ['nivel_territorial','nivel_comun']:
        expected=[float(v) for y in ys for v in np.atleast_1d(p['d' if cand['family']=='nivel_territorial' else 'c'][y])]
        equal(ctx['statistic_values'],expected,'constant input');check(ctx['statistic']==cand['statistic'],'constant rule')
    return ys
def reconstruct(out,cand,p):
    ctx=out['context'];ys=audit_context(ctx,cand,p);pred={}
    if not ys or cand['family']=='persistencia':
        delta=np.zeros(33);check(out['fits']==0 and out['statistical_estimates']==0,'backup no fit')
    elif not cand['components']:
        vals=ctx['statistic_values'];v=statistics.median(vals) if cand['statistic']=='median' else math.fsum(vals)/len(vals)
        equal(out['metadata']['statistic_value'],v,'constant median/mean');delta=np.full(33,v)
        check(out['fits']==0 and out['statistical_estimates']==1,'constant counted')
    else:
        check(out['fits']==len(cand['components']) and out['statistical_estimates']==0,'fits counted')
        for comp,dat in ctx['components'].items():
            m=out['metadata'][comp];X=np.asarray(dat['X']);XP=np.asarray(dat['predict_X']);mu=X.mean(axis=0);var=X.var(axis=0);sc=np.sqrt(var);sc[sc==0]=1
            check(m['n_samples']==len(X) and np.allclose(mu,m['scaler_mean'],rtol=0,atol=1e-12) and np.allclose(var,m['scaler_var'],rtol=0,atol=1e-12) and np.allclose(sc,m['scaler_scale'],rtol=0,atol=1e-12),'scaler onlytrain')
            Z=(XP-np.asarray(m['scaler_mean']))/np.asarray(m['scaler_scale'])
            if 'coef' in m:z=Z@np.asarray(m['coef'])+m['intercept']
            else:
                t=m['tree'];z=[]
                for row in Z.astype(np.float32):
                    node=0
                    while t['children_left'][node]!=-1:
                        node=t['children_left'][node] if row[t['feature'][node]]<=t['threshold'][node] else t['children_right'][node]
                    z.append(t['value'][node][0][0])
                z=np.asarray(z)
            equal(z,m['predicted_component'],'coef/tree component exact')
            check(all(w['category']!='ConvergenceWarning' for w in m['warnings']),'no convergence warning')
            pred[comp]=z
        delta=pred['memoria'] if 'memoria' in pred else np.full(33,pred['comun'][0])
        if 'correccion' in pred:delta=delta+pred['correccion']
    equal(delta,out['predicted_delta'],'delta exact');equal(np.asarray(ctx['previous_score'])+delta,out['prediction'],'score exact')
    return True
def csv_exact(a,b,keys):
    a=a.sort_values(keys).reset_index(drop=True);b=b.sort_values(keys).reset_index(drop=True)
    check(a.shape==b.shape and list(a.columns)==list(b.columns),'CSV shape')
    for c in a:equal(a[c],b[c],'CSV '+c)
def auditor_tests():
    csv_exact(pd.DataFrame({'x':[0]}),pd.DataFrame({'x':[0.0]}),['x'])
    try:csv_exact(pd.DataFrame({'x':[0]}),pd.DataFrame({'x':[1e-11]}),['x'])
    except AssertionError:pass
    else:raise AssertionError('CSV 1e-11')
    rr=[dict(id='a',MAE=1.1,RMSE=2.1,inputs=0,order=0),dict(id='b',MAE=1,RMSE=2,inputs=1,order=1)]
    check(independent_selection(rr)['winner']=='a','inclusive independent selector')
    # Matrices ficticias y coeficientes guardados: no fit ni constructor operativo.
    codes=[str(i) for i in range(33)];levels={2018:np.full(33,200.),2019:np.full(33,202.),2021:np.full(33,206.),2022:np.full(33,210.)};prior={2019:2018,2021:2019,2022:2021};d={y:levels[y]-levels[q] for y,q in prior.items()};c={y:float(statistics.median(v)) for y,v in d.items()};r={y:v-c[y] for y,v in d.items()};p=dict(levels=levels,prior=prior,d=d,c=c,r=r,codes=codes,years=list(levels))
    cand=dict(id='ficticio',history='all',inputs=1,params={},components=['comun'],family='comun_qr')
    ctx=dict(id='ficticio',history='all',year=2022,eligible_years=[2021],previous=2021,inputs=1,seed=SEED,params={},units='puntos globales; cambio sin anualizar',prediction_keys=[[j,2022] for j in codes],previous_score=levels[2021].tolist(),components={'comun':dict(X=[[2.]],y=[4.],keys=[['comun',2021]],previous_years=[2019],predict_X=[[4.]])})
    for saved,f in [('prior_levels','levels'),('prior_d','d'),('prior_c','c'),('prior_r','r')]:ctx[saved]={str(y):np.asarray(v).tolist() for y,v in p[f].items() if y<2022}
    out=dict(context=ctx,metadata={'comun':dict(scaler_mean=[2.],scaler_var=[0.],scaler_scale=[1.],n_samples=1,coef=[0.],intercept=4.,predicted_component=[4.],warnings=[])},fits=1,statistical_estimates=0,predicted_delta=[4.]*33,prediction=[210.]*33)
    reconstruct(out,cand,p)
    out['context']['components']['comun']['X'][0][0]+=1e-11
    try:reconstruct(out,cand,p)
    except AssertionError:pass
    else:raise AssertionError('X altered')
    return dict(aprobado=True,synthetic_fits=0,tests=['CSV0/1e-11','selector inclusive','matrices/fecha/coefs/scaler/reconstruction','rechazo matriz alterada'])
def audit():
    preflight();spec=load(HERE/'ESPECIFICACION_V6.json');p=readpanel();cands={c['id']:c for c in spec['candidates']};jobs=0;models=[]
    f=load(HERE/'fase1/CONGELACION.json')
    for s,h in f['sha256'].items():check(sha(HERE/s)==h,'freeze intacto')
    ledger=load(PILOT/'ledger.json');check(ledger['status']=='cerrado_completo' and ledger['elapsed_seconds']<=7200 and ledger['budget_seconds']==7200 and ledger['pending'] is None,'ledger cerrado/presupuesto')
    check(ledger['fits_started']==ledger['fits_completed']<=328 and ledger['statistical_estimates']<=104 and ledger['retries']<=1 and all(e['terminated'] and e['ok'] and not e['timeout'] for e in ledger['events']),'fits/termination')
    started=completed=constants=0
    for e in ledger['events']:
        base=PILOT/'jobs'/e['name'];outpath=base/f'result_{e["attempt"]}.json';evpath=base/f'events_{e["attempt"]}.json';req=load(base/'request.json');out=load(outpath)
        check(sha(outpath)==e['result_sha'] and sha(evpath)==e['events_sha'],'durable job hashes')
        equal(req['context'],out['context'],'request context');check(req['candidate']==cands[req['candidate']['id']],'params/order full exact')
        seq=load(evpath)
        started+=sum(s.get('fits_started',0) for s in seq);completed+=sum(s.get('fits_completed',0) for s in seq);constants+=sum(s.get('statistical_estimates',0) for s in seq)
        reconstruct(out,req['candidate'],p);jobs+=1
        for comp,m in out['metadata'].items():
            if isinstance(m,dict):models.append(dict(job=e['name'],id=req['candidate']['id'],year=out['context']['year'],component=comp,**m))
    check((started,completed,constants)==(ledger['fits_started'],ledger['fits_completed'],ledger['statistical_estimates']),'event counts')
    ext=pd.read_csv(PILOT/'externas.csv',dtype={'code':str},float_precision='round_trip');ori=pd.read_csv(PILOT/'internas_originales.csv',dtype={'code':str},float_precision='round_trip');uniq=pd.read_csv(PILOT/'internas_unicas.csv',dtype={'code':str},float_precision='round_trip');lin=pd.read_csv(PILOT/'linaje.csv',dtype={'code':str},float_precision='round_trip');sel=pd.read_csv(PILOT/'selecciones.csv',float_precision='round_trip')
    check((len(ext),len(ori),len(uniq),len(lin),len(sel))==(6600,12870,5148,12870,156),'coverage all')
    check(not ext.duplicated(['id','year','code']).any() and not uniq.duplicated(['id','year','code']).any(),'unique keys')
    # CSV exactos con JSON originario; sin tolerancia para predicciones serializadas.
    for frame,kind in [(ext,'externo'),(uniq,'interno')]:
        for (id,y),g in frame.groupby(['id','year'],sort=False):
            if id=='global_v6':continue
            out=load(PILOT/'externals'/f'{y}_{id}.json') if kind=='externo' else load(PILOT/'jobs'/f'interno_{y}_{id}'/'result_0.json')
            g=g.sort_values('code');reconstruct(out,cands[id],p)
            equal(g.predicted,out['prediction'],'CSV exact predicted');equal(g.predicted_delta,out['predicted_delta'],'CSV exact delta');equal(g.observed,p['levels'][y],'observed source');equal(g.previous,out['context']['previous_score'],'previous source')
            h=hashlib.sha256(json.dumps(out['context'],sort_keys=True).encode()).hexdigest();check((g.context_sha==h).all(),'context hash')
    for (ex,id,y),g in ori.groupby(['external','id','year'],sort=False):
        u=uniq[(uniq.id==id)&(uniq.year==y)].copy();u['external']=ex;csv_exact(g,u,list(['id','year','code']))
    for (y,id,j),g in lin.groupby(['year','id','code'],sort=False):
        check((g.representative_external==g.external.min()).all() and g.context_sha.nunique()==1 and len(g)==2025-y,'lineage reps/copies')
    for y in range(2022,2026):
        d=load(PILOT/'selections'/f'{y}.json');records=[]
        for cand in spec['candidates']:
            g=ori[(ori.external==y)&(ori.id==cand['id'])]
            records.append(dict(id=cand['id'],inputs=cand['inputs'],order=cand['order'],**error_metrics(g.predicted,g.observed)))
        expected=independent_selection(records)
        for k,v in expected.items():check(d[k]==v,'selection independent '+k)
        first_external=next(e for e in ledger['events'] if e['name'].startswith(f'externo_{y}_'))
        snap_req=load(PILOT/'jobs'/first_external['name']/'events_0.json')
        if snap_req:check(d['created_monotonic']<snap_req[0]['monotonic'],'selection before external')
        for rec in records:
            g=sel[(sel.external==y)&(sel.id==rec['id'])].iloc[0]
            for k,v in rec.items():check(g[k]==v,'selection CSV exact '+k)
            check(g.selected==d['winner'] and bool(g.pool_mae)==(rec['id'] in d['pool_mae']) and bool(g.pool_rmse)==(rec['id'] in d['pool_rmse']),'selection pools CSV')
    checks=load(PILOT/'global_checks.json');check(len(checks)==5,'5checks')
    for cc in checks:
        y=cc['year'];chosen=load(PILOT/'selections'/f'{y}.json')['winner'] if y>2021 else 'persistencia';check(cc['selected']==chosen,'selected global')
        g=ext[(ext.id=='global_v6')&(ext.year==y)].sort_values('code');ref=ext[(ext.id==chosen)&(ext.year==y)].sort_values('code')
        equal(g.predicted,ref.predicted,'global reuse same id/window');equal(g.observed,ref.observed,'same observed');equal(cc['prediction'],g.predicted,'global check original')
        check(np.allclose(cc['prediction'],cc['repeated'],rtol=0,atol=1e-10) if cc['method']=='fit_repetido' else np.array_equal(cc['prediction'],cc['repeated']),'check repetition')
    snapshots=sorted((PILOT/'snapshots').glob('*.json'));states=[load(s) for s in snapshots]
    check(states[0]['elapsed_seconds']>=0 and states[-1]==ledger and all(b['elapsed_seconds']>=a['elapsed_seconds'] for a,b in zip(states,states[1:])),'durable monotonic snapshots')
    test=auditor_tests();save(HERE/'fase3/PRUEBAS_AUDITOR.json',test)
    result=dict(aprobado=True,jobs=jobs,fits=started,constant_estimates=constants,seconds=ledger['elapsed_seconds'],coverage=load(PILOT/'COBERTURA.json'),snapshots=len(states),fits_auditor=0,deserializations=0,independence='solo comun/bytes/metadatos; ningún import motor/selector/runner',scaler_tolerance=dict(atol=1e-12,rtol=0),CSV='exacto;0intfloat equivalente;1e-11 rechazado')
    save(HERE/'fase3/COEFICIENTES.json',models);save(HERE/'fase3/AUDITORIA.json',result);return result
def audit_incomplete():
    """Coteja solo lo disponible; jamás sintetiza desempeño de piloto inválido."""
    preflight();p=readpanel();spec=load(HERE/'ESPECIFICACION_V6.json');cands={c['id']:c for c in spec['candidates']}
    ledger=load(PILOT/'ledger.json');original=load(HERE/'fase2/antecedentes/ledger_interrumpido.json');f=load(HERE/'fase1/CONGELACION.json')
    for s,h in f['sha256'].items():check(sha(HERE/s)==h,'freeze intacto '+s)
    check(ledger['status']=='cerrado_incompleto' and ledger['pending_unmeasured'] and ledger['elapsed_seconds']==7200,'cierre conservador')
    test=auditor_tests();save(HERE/'fase3/PRUEBAS_AUDITOR.json',test)
    rows=[];contexts_verified=0;exceptions=[]
    for e in original['events']:
        base=PILOT/'jobs'/e['name'];request=base/'request.json';rp=base/f'result_{e["attempt"]}.json';ep=base/f'events_{e["attempt"]}.json';out=load(rp);req=load(request)
        passed=True;err=None
        try:
            check(sha(rp)==e['result_sha'] and (sha(ep) if ep.exists() else None)==e['events_sha'],'durable hashes')
            check(req['context']==out['context'] and req['candidate']==cands[req['candidate']['id']],'request/defaults')
            reconstruct(out,req['candidate'],p);contexts_verified+=1
        except Exception as exc:passed=False;err=str(exc);exceptions.append(dict(job=e['name'],error=err))
        seq=load(ep) if ep.exists() else [];count=sum(x.get('fits_completed',0) for x in seq)
        rows.append(dict(job=e['name'],role=e['name'].split('_')[0],id=req['candidate']['id'],year=out['context']['year'],component_fits_completed=count,statistical_estimates=out['statistical_estimates'],durable_terminated=e['terminated'],matrices_predictions_verified=passed,error=err,result_sha=sha(rp),context_sha=hashlib.sha256(json.dumps(out['context'],sort_keys=True).encode()).hexdigest()))
    table=pd.DataFrame(rows);check(int(table.component_fits_completed.sum())==original['fits_completed'],'fits consolidated count')
    check(int(table.statistical_estimates.sum())==original['statistical_estimates'],'constants consolidated count')
    # Cota interna deriva de las ventanas originales, no del selector operativo.
    active=[(w['externo'],i['validacion']) for w in spec['windows'] for i in w['internas'] if i['validacion']>=2022]
    expected_internal=sum(len(c['components']) for c in cands.values())*len(active)
    internal_actual=int(table[table.role=='interno'].component_fits_completed.sum())
    check(expected_internal==192 and internal_actual==96,'diagnóstico del fallo debe reproducirse')
    pending=original['pending'];pe=PILOT/'jobs'/pending['name']/f'events_{pending["attempt"]}.json';pr=PILOT/'jobs'/pending['name']/f'result_{pending["attempt"]}.json'
    pending_events=load(pe) if pe.exists() else []
    snapshot_states=[load(p) for p in sorted((PILOT/'snapshots').glob('*.json'))]
    check(snapshot_states[-1]==original and all(b['elapsed_seconds']>=a['elapsed_seconds'] for a,b in zip(snapshot_states,snapshot_states[1:])),'snapshots intactos monotónicos')
    (HERE/'fase3/tablas').mkdir(parents=True,exist_ok=True);table.to_csv(HERE/'fase3/tablas/trabajos_consolidados_verificados.csv',index=False,float_format='%.17g')
    report=dict(complete=False,verified_available_contexts=contexts_verified,available_consolidated_jobs=len(rows),available_check_errors=exceptions,phase1_acceptance_superseded_by_failure=True,internal_fits_contract=expected_internal,internal_fits_durable=internal_actual,consolidated_fits_durable=original['fits_completed'],constant_estimates_durable=original['statistical_estimates'],pending_job=pending['name'],pending_events=pending_events,pending_result_exists=pr.exists(),last_measured_snapshot_seconds=original['elapsed_seconds'],budget_consumed_conservative_seconds=7200,ledger_closed=True,reopened=False,new_fits=0,deserializations=0,primary_evaluation_valid=False,performance_synthesis=False,controls={'sources_environment_conservation':True,'freeze_bytes':True,'synthetic_auditor_tests':test['aprobado'],'available_matrices_metadata':not exceptions,'no_fit_sharing_between_internal_windows':False,'coverage_complete':False,'last_worker_independent_termination_record':False},impact='piloto no cumple ejecución por ventana; ninguna métrica v6 o meta es admisible',resolution='cerrar incompleto; conservar fuentes/freeze/guardados; sin reinicio, otro experimento ni síntesis dependiente',independence='solo comun/bytes/metadatos/coef/scalers/árboles; no imports motor/selector/runner ni modelos')
    save(HERE/'fase3/AUDITORIA_INCOMPLETA.json',report);return report
if __name__=='__main__':print(json.dumps(audit_incomplete() if sys.argv[1:]==['--incompleto'] else audit(),ensure_ascii=False))
