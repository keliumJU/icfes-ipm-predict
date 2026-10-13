"""Controles inventados; ningún fit. Deben aprobar antes de congelación."""
from infra import *
import copy, tempfile, math, numpy as np, pandas as pd
from diseno import build,metrics,select,contexts
import auditor
def run():
    passed=[]
    def test(label,v):check(v,label);passed.append(label)
    def rejected(label,fn):
        try:fn()
        except (AssertionError,ValueError):passed.append(label);return
        raise AssertionError('no rechazado '+label)
    toy=pd.DataFrame([dict(codigo_departamento=f'{code:02d}',anio=year,prom_punt_global=100+code+idx*3,ipm=50-idx,departamento='inventado') for code in range(1,34) for idx,year in enumerate([2018,2019,2021,2022,2023,2024,2025])])
    p=build(toy,[]);p=p[p.anio>=2021].sort_values(['anio','codigo_departamento'])
    c=dict(id='Htoy',family='Ridge',inputs=['puntaje_previo','cambio_previo'],params={},scaler={})
    mat=contexts(p,c,2023)
    test('2019 solo historia y2020 excluido',set(mat['train']['years'])=={2021,2022} and 2019 not in mat['train']['years'] and 2020 not in mat['train']['years'])
    test('salto2019→2021 sin anualizar/H',mat['train']['history'][0]['anio_previo']==2019 and mat['train']['history'][0]['cambio_previo']==3)
    a=build(toy.assign(prom_punt_global=np.where(toy.anio>=2023,999.,toy.prom_punt_global)),[]);a=a[a.anio>=2021].sort_values(['anio','codigo_departamento']);mat2=contexts(a,c,2023)
    test('no y_t enX y futuras respuestas no afectan training',mat['train']==mat2['train'] and mat['test']['X']==mat2['test']['X'])
    test('pobreza contemporánea',contexts(p,{**c,'inputs':['ipm']},2023)['test']['X']==[[46]]*33)
    future=toy.copy();future.loc[future.anio>=2024,'ipm']=999;f=build(future,[]);f=f[f.anio>=2021].sort_values(['anio','codigo_departamento'])
    test('pobreza futura no altera presente',contexts(f,{**c,'inputs':['ipm']},2023)==contexts(p,{**c,'inputs':['ipm']},2023))
    cs=[dict(id='p',inputs=[],order=0),dict(id='I',inputs=['a'],order=1),dict(id='H',inputs=['a','b'],order=2)]
    scores={'p':{'MAE':1.1,'RMSE':2.1},'I':{'MAE':1.,'RMSE':2.},'H':{'MAE':1.10001,'RMSE':1.}}
    test('selector inclusivo tolerancias/menos entradas',select(scores,cs,['p','I','H'])=='p')
    test('selector independiente coincide',auditor.choice(scores,['p','I','H'],cs)==select(scores,cs,['p','I','H']))
    for field in ['X','y','history','years','keys','inputs']:
        bad=copy.deepcopy(mat)
        if field in ['X','y']:bad['train'][field][0]=[999,0] if field=='X' else 999
        elif field=='history':bad['train'][field][0]['anio_previo']=2020
        elif field=='years':bad['train'][field][0]=2019
        elif field=='keys':bad['train'][field][0]['anio']=2023
        else:bad['train'][field]=['prom_punt_global','ipm']
        rejected('auditor matriz corrupta '+field,lambda bad=bad:auditor.validate_matrix(bad,c,p.to_dict('records'),2023))
    auditor.validate_matrix(mat,c,p.to_dict('records'),2023);passed.append('auditor acepta inventado correcto')
    rejected('rutas fuera',lambda:safe(ROOT/'ajeno.csv'));rejected('traversal',lambda:safe(HERE/'../ajeno'))
    link=HERE/'preflight/prueba_symlink';link.parent.mkdir(parents=True,exist_ok=True);link.symlink_to('/tmp')
    try:rejected('symlink',lambda:safe(link/'archivo'))
    finally:link.unlink()
    # Control temporal y de exclusividad de presupuesto: misma desigualdad del ejecutor.
    import infra, piloto
    from unittest.mock import patch, Mock
    with patch.object(infra,'elapsed',return_value=5400):rejected('stop nuevosfits5400',lambda:infra.deadline(True))
    with patch.object(infra,'elapsed',return_value=7200):rejected('cierre7200',lambda:infra.deadline(False))
    with patch.object(infra,'elapsed',return_value=5399):infra.deadline(True);passed.append('fit5399 permitido')
    rejected('reuso IDcontexto rechazado',lambda:piloto.new_identity('x',['x']))
    piloto.retry_allowed('infrastructure',0);passed.append('un retry infraestructura')
    rejected('retry agotado',lambda:piloto.retry_allowed('infrastructure',1))
    rejected('numérico sin retry',lambda:piloto.retry_allowed('numerical',0))
    inst=piloto.Pilot.__new__(piloto.Pilot);inst.l={'pending':None};inst.flush=Mock();inst.process=Mock();inst.process.poll.return_value=None
    inst.close('cerrado_incompleto','inventado')
    test('terminación durable inventada sin proceso real',inst.process.terminate.called and inst.process.wait.called and inst.flush.called and not inst.l['saldo_reutilizable'])
    # Ridge guardado inventado: aceptar escala de train y rechazar corrupción.
    fx=HERE/'preflight/fixture_matrix.json';fm=copy.deepcopy(mat);save(fx,fm)
    cr=dict(id='mock',family='Ridge',params={},inputs=c['inputs'],scaler={})
    X=np.asarray(fm['train']['X']);scale=np.std(X,axis=0);scale[scale==0]=1
    rr=dict(id='mock',family='Ridge',params={},runtime_params={},pipeline_params={'memory':None,'verbose':False,'transform_input':None},inputs=c['inputs'],matrix_file='preflight/fixture_matrix.json',matrix_sha256=sha(fx),scaler={'mean':np.mean(X,axis=0).tolist(),'var':np.var(X,axis=0).tolist(),'scale':scale.tolist(),'n_samples_seen':len(X),'params':{}},coef=[0.,0.],intercept=1.,prediction=[1.]*33,warnings=[])
    auditor.validate_record(rr,fm,cr);passed.append('scalertrain/coef auditor acepta fixture')
    for field in ['mean','scale','var','n_samples_seen']:
        bad=copy.deepcopy(rr)
        if field=='n_samples_seen':bad['scaler'][field]+=1
        else:bad['scaler'][field][0]+=1
        rejected('auditor scaler corrupto '+field,lambda bad=bad:auditor.validate_record(bad,fm,cr))
    bad=copy.deepcopy(rr);bad['params']={'random_state':0};rejected('auditor defaults corruptos',lambda:auditor.validate_record(bad,fm,cr))
    bad=copy.deepcopy(rr);bad['prediction'][0]+=.001;rejected('auditor prediction corrupta',lambda:auditor.validate_record(bad,fm,cr))
    test('prediccion repetida atol1e-10rtol0',np.allclose([0],[1e-10],atol=1e-10,rtol=0) and not np.allclose([0],[1.0001e-10],atol=1e-10,rtol=0))
    spec=load(HERE/'ESPECIFICACION.json')
    from diseno import params
    test('defaults inspeccionados congelados completos',params()==spec['defaults'])
    from sklearn.pipeline import Pipeline
    test('pipeline defaults completos sin fit',{k:v for k,v in Pipeline([]).get_params(deep=False).items() if k!='steps'}=={'memory':None,'verbose':False,'transform_input':None})
    test('cobertura21/200',len(spec['candidates'])==21 and 20*(6+4)==200)
    tests=auditor.self_tests();save(HERE/'preflight/PRUEBAS_AUDITOR.json',tests)
    save(HERE/'preflight/PRUEBAS.json',dict(aprobado=True,tests=passed,fits=0,inventados=True))
    return passed
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False))
