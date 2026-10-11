"""Suite propia etapa2: datos inventados, recorrido real del orquestador y dobles."""
from piloto import *
from verificar import auditar_artefactos,etiqueta_interna
import tempfile,multiprocessing
class FallaHighs:
    def __init__(self,c,convergencia=False):self.c=c;self.convergencia=convergencia
    def fit(self,X,y):
        import sklearn.linear_model._quantile as q
        from unittest.mock import patch
        from types import SimpleNamespace
        model=construir(self.c)
        if self.convergencia:
            with patch.object(q,'linprog',return_value=SimpleNamespace(x=np.zeros(2*(X.shape[1]+1)+2*len(y)),success=False,status=1,message='HiGHS sintético',nit=1)):model.fit(X,y)
        else:
            with patch.object(q,'linprog',side_effect=ValueError('HiGHS fallo sintético')):model.fit(X,y)
        return self
class Lento:
    def fit(self,X,y):time.sleep(20)

def rechaza(call,kind=Exception):
    try:call()
    except kind:return
    raise AssertionError('no rechazó')
def inventado():
    raw=pd.DataFrame([dict(codigo_departamento=f'{j:02d}',anio=a,prom_punt_global=200.+a-2018+j,**{s:float(k+10)+j*.01+a*.001 for k,s in enumerate(COV)}) for j in range(33) for a in ANIOS])
    return historial(raw)
def doble(est,X,y,remaining):return est.fit(X,y),.001

def ejecutar():
    out=destino(OUT/'sinteticos');out.mkdir(exist_ok=True)
    run=Path(tempfile.mkdtemp(prefix='orquestacion_',dir=out));passed=[]
    p=inventado();cs=candidatos();r=Runner(run/'completo',p,executor=doble);r.run()
    result=auditar_artefactos(r.out,p)
    assert len(result['actual_internals'])==350 and len(result['score_rows'])==144
    assert len(result['ledger']['ajustes'])<=378
    assert sum(len(q) for q in result['externals'])==1155
    before=read(r.out/'ledger.json');again=Runner(r.out,p,executor=doble);again.run();assert before==read(r.out/'ledger.json')
    passed.append('orquestación completa36/350 internos/7×165/selecciones antes externo/repeticiones/orden/artefactos/transforms; reanudar sin fits')
    rechaza(lambda:Runner(r.out,p.assign(prom_punt_global=p.prom_punt_global+1),executor=doble))
    meta=next((r.out/'ajustes').glob('*/ajuste.json'));saved=meta.read_bytes();meta.write_text('{}');rechaza(lambda:Runner(r.out,p,executor=doble));meta.write_bytes(saved)
    file=next((r.out/'ajustes').glob('*/modelo.joblib'));saved=file.read_bytes();file.write_bytes(b'alterado');rechaza(lambda:Runner(r.out,p,executor=doble));file.write_bytes(saved)
    rechaza(lambda:Presupuesto(r.out/'ledger.json',7201))
    passed.append('contexto/matrices/artefactos/modelos/huellas/ledger alterado; saldo no ampliable')
    train,test=dividir(p,[2019],2021)
    calls=[]
    def retry(est,X,y,remaining):
        calls.append(1)
        if len(calls)==1:raise OSError('infraestructura inventada')
        return doble(est,X,y,remaining)
    rr=Runner(run/'retry',p,executor=retry);rr.predict('e2022_i2021_'+cs[1]['id'],cs[1],train,test)
    assert len(rr.budget.data['ajustes'])==2
    def infra(*args):raise OSError('infraestructura persistente')
    rr=Runner(run/'infra',p,executor=infra);label='e2022_i2021_'+cs[1]['id']
    rechaza(lambda:rr.predict(label,cs[1],train,test),OSError);rechaza(lambda:Runner(rr.out,p,executor=infra).predict(label,cs[1],train,test),RuntimeError)
    assert len(rr.budget.data['ajustes'])==2
    def numeric(*args):raise ValueError('numérico inventado')
    rr=Runner(run/'numerico',p,executor=numeric);assert rr.predict(label,cs[1],train,test) is None
    assert Runner(rr.out,p,executor=numeric).predict(label,cs[1],train,test) is None and len(rr.budget.data['ajustes'])==1
    rr=Runner(run/'caida',p,executor=doble);rr.budget.data['pendiente']=dict(etiqueta='perdido');guardar(rr.budget.path,rr.budget.data);rr.checkpoint()
    rechaza(lambda:Runner(rr.out,p,executor=doble),TimeoutError);assert read(rr.budget.path)['consumido']==7200
    passed.append('un retryinfra/segundo detiene/numérico inelegible persistente/caída pendiente agota')
    # Selección global distinta de ganadorgrupo: caso exacto antes de externos.
    rows=[dict(id=c['id'],estado='completo',ventanas=[2021],mae=9.,rmse=10.,razon=None) for c in cs]
    rows[1].update(mae=1.15,rmse=1.);rows[2].update(mae=1.06,rmse=1.);rows[4].update(mae=1.,rmse=2.)
    d=seleccionar(rows,[2021],2022);assert d['global_id']==cs[2]['id'] and d['especificaciones']['historico']==cs[1]['id']
    d=dict(global_id=cs[2]['id'],especificaciones={g:next(c['id'] for c in cs if c['familia']=='boosting_absoluto' and c['especificacion']==g) for g in GRUPOS});assert len(ids_externos(d))==6
    d['especificaciones']['historico']=d['global_id'];assert len(ids_externos(d))==5
    rechaza(lambda:seleccionar(rows[::-1],[2021],2022));rechaza(lambda:seleccionar(rows[:-1],[2021],2022));rechaza(lambda:seleccionar(rows,[],2021))
    assert not etiqueta_interna('e2022_externo_mediana_nivel_ipm_00') and etiqueta_interna('e2022_i2021_mediana_nivel_ipm_00')
    passed.append('global distinto de grupo/6IDs/dedup solo identidad/registro36/regex temporal completa')
    frames=pd.concat(result['externals'],ignore_index=True);assert cobertura(frames,p.codigo_departamento.unique())
    rechaza(lambda:cobertura(frames.iloc[:-1],p.codigo_departamento.unique()))
    corrupt=frames.copy();corrupt.loc[0,'prediccion']=float('nan');rechaza(lambda:cobertura(corrupt,p.codigo_departamento.unique()))
    corrupt=frames.copy();corrupt.loc[33,'observado']+=1e-11;rechaza(lambda:cobertura(corrupt,p.codigo_departamento.unique()))
    a=pd.DataFrame(dict(codigo_departamento=['05','08'],anio=[2022,2022],cambio_predicho=[0,0]));b=a.astype({'cambio_predicho':float})
    csv(run/'int.csv',a);csv(run/'float.csv',b);igualdad_exacta(loadcsv(run/'int.csv'),loadcsv(run/'float.csv'))
    for field,v in [('cambio_predicho',1e-11),('codigo_departamento','99'),('anio',2021)]:
        c=b.copy();c.loc[0,field]=v;rechaza(lambda:igualdad_exacta(a,c))
    rechaza(lambda:igualdad_exacta(a,b.iloc[::-1].reset_index(drop=True)));rechaza(lambda:igualdad_exacta(a,b[list(reversed(b.columns))]));rechaza(lambda:igualdad_exacta(a,b.rename(columns={'anio':'year'})))
    rechaza(lambda:destino(E1/'prohibido'));rechaza(lambda:Presupuesto(E1/'ledger.json'))
    link=run/'escape';link.symlink_to(E1,target_is_directory=True);rechaza(lambda:destino(link/'prohibido'));link.unlink()
    passed.append('cobertura incompleta/no finitos/observados/CSV int-float exacto rechaza1e-11 llaves campos orden/rutas y symlink')
    children={c.pid for c in multiprocessing.active_children()}
    for c in [cs[1],cs[16]]:
        b=Presupuesto(run/('worker_'+c['familia']+'.json'),20);model,notes=b.ajustar(c['id'],construir(c),np.arange(30.).reshape(-1,1),np.arange(30.))
        assert serial(model.get_params(deep=True))==c['parametros_completos'] and not notes
    for flag in (False,True):
        b=Presupuesto(run/f'highs_{flag}.json',20)
        rechaza(lambda:b.ajustar('highs',FallaHighs(cs[1],flag),np.arange(30.).reshape(-1,1),np.arange(30.)),ValueError)
        assert len(b.data['ajustes'])==1
    b=Presupuesto(run/'limite.json',.3);rechaza(lambda:b.ajustar('lento',Lento(),[[0]],[0]),TimeoutError)
    assert b.data['consumido']==.3;before=len(b.data['ajustes']);rechaza(lambda:b.ajustar('sin saldo',None,None,None),TimeoutError);assert len(b.data['ajustes'])==before
    b=Presupuesto(run/'interrumpido.json',10)
    def interrupt(*args):raise KeyboardInterrupt()
    rechaza(lambda:b.ajustar('interrumpido',None,None,None,executor=interrupt),KeyboardInterrupt)
    assert b.data['consumido']>0 and not b.data['pendiente']
    assert {c.pid for c in multiprocessing.active_children()}==children
    passed.append('worker propios imports/Pipeline/boosting real inventado/HiGHS fallo y convergencia/terminación límite e interrupción/sin proceso restante/sin intento ficticio')
    data=dict(aprobado=True,ajustes_panel=0,origen='inventados/dobles exclusivamente',grupos=passed,pruebas=str(run.relative_to(ROOT)),fuentes_sha256={str(q.relative_to(ROOT)):sha(q) for q in sorted((E2/'fuentes').glob('*.py'))},defaults_sha256=sha(CONFIG),panel_entrada_sha256=sha(PANEL),entorno_sha256=sha(OUT/'entorno.json'))
    guardar(run/'resumen.json',data);guardar(OUT/'pruebas_sinteticas.json',data)
    print('Pruebas propias etapa2 aprobadas',len(passed),flush=True)
if __name__=='__main__':ejecutar()
