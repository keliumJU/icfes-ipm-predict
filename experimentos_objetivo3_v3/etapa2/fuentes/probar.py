"""Orquestación completa con valores inventados y dobles; no usa panel real."""
from piloto import *
import tempfile, warnings, multiprocessing
class DeltaDoble:
    def predict(self,X):return np.full(len(X),5.)
class Lento:
    def fit(self,X,y):time.sleep(10)
def doble(remaining,model,X,y):
    assert np.isfinite(X).all() and np.isfinite(y).all()
    return (DeltaDoble(),[]),.001

def test():
    out=OUT/'sinteticos';destino(out).mkdir(exist_ok=True)
    run=Path(tempfile.mkdtemp(prefix='orquestacion_',dir=out))
    rows=[]
    for j,code in enumerate('05 08 11 13 15 17 18 19 20 23 25 27 41 44 47 50 52 54 63 66 68 70 73 76 81 85 86 88 91 94 95 97 99'.split()):
        for k,year in enumerate(ANIOS):
            row=dict(codigo_departamento=code,anio=year,prom_punt_global=200+j+5*k)
            for z,col in enumerate(anterior.ESPECIFICACIONES['ambas']):row[col]=10+j*.1+k*.2+z
            rows.append(row)
    p=historial(pd.DataFrame(rows)).reset_index(drop=True)
    r=Runner(run/'completo',p,executor=doble);r.run()
    assert len(r.budget.data['ajustes'])==1006 # 990+3 OLS externos x4+4 globales
    assert not list((r.out/'ajustes').glob('e2021*'))
    assert read(r.out/'seleccion_2021.json')['metricas_internas']==[]
    assert len(read(r.out/'reproducibilidad.json')['repeticiones'])==5
    assert read(r.out/'seleccion_2022.json')['global_id']=='delta_ols_ipm_00'
    for year in range(2021,2026):
        ext=loadcsv(r.out/f'externas_{year}.csv');assert len(ext)==165
        assert ext.seleccion_sha256.eq(sha(r.out/f'seleccion_{year}.json')).all()
    count=len(r.budget.data['ajustes']);spent=r.budget.data['consumido']
    resumed=Runner(r.out,p,executor=doble);resumed.run()
    assert len(resumed.budget.data['ajustes'])==count and resumed.budget.data['consumido']==spent
    changed=p.copy();changed.loc[changed.anio==2022,'prom_punt_global']=1e8
    rr=Runner(run/'externo_alterado',changed,executor=doble);rr.window(ventanas()[1])
    assert read(rr.out/'seleccion_2022.json')['metricas_internas']==read(r.out/'seleccion_2022.json')['metricas_internas']
    # Global puede diferir del ganador por su propia especificación: cuatro IDs externos.
    import piloto as motor
    saved_selector=motor.seleccionar
    def distinct(*args):
        return dict(global_id='delta_ols_ipm_00',especificaciones={'ipm':'delta_ridge_ipm_00','tasas':'delta_ols_tasas_00','ambas':'delta_ols_ambas_00'})
    motor.seleccionar=distinct
    try:
        separate=Runner(run/'cuatro_externos',p,executor=doble);separate.window(ventanas()[1])
        assert len(separate.budget.data['ajustes'])==103
        assert len(list((separate.out/'ajustes').glob('e2022_externo*')))==4
    finally:motor.seleccionar=saved_selector
    # Worker spawn con Pipeline real sobre datos inventados y objetivo de cambio.
    real=Runner(run/'worker_sintetico',p,limit=30);real.origin='sintetico_worker'
    tr,te=dividir(p,[2019],2021);c=candidatos()[1]
    q=real.predict('worker_sintetico',c,tr,te)
    assert len(q)==33;np.testing.assert_allclose(q.prediccion,te.prom_punt_global,atol=1e-10,rtol=0)
    assert read(real.out/'ajustes/worker_sintetico/ajuste.json')['transformacion_ajustada']['n_samples_seen']==33
    # Fallo de infraestructura se carga dos veces; numérico una; reanudar no amplía intentos.
    calls=[]
    def infra(*args):
        calls.append(1)
        if len(calls)==1:raise RuntimeError('infraestructura sintética')
        return doble(*args)
    retry=Runner(run/'reintento',p,executor=infra);retry.fit('doble',c,tr)
    assert len(retry.budget.data['ajustes'])==2
    def numeric(*args):raise ValueError('numérico sintético')
    fail=Runner(run/'numerico',p,executor=numeric);assert fail.fit('doble',c,tr)[0] is None
    assert len(fail.budget.data['ajustes'])==1;assert fail.fit('doble',c,tr)[0] is None
    def permanent(*args):raise RuntimeError('infraestructura persistente')
    per=Runner(run/'permanente',p,executor=permanent)
    for _ in range(2):
        try:per.fit('doble',c,tr);raise AssertionError('debe parar')
        except RuntimeError:pass
    assert len(per.budget.data['ajustes'])==2
    limit=Presupuesto(run/'limite.json',.001)
    try:limit.ajustar('doble',None,np.array([[1.]]),np.array([1.]),executor=doble);raise AssertionError('límite')
    except TimeoutError:pass
    assert Presupuesto(run/'limite.json',.001).data['consumido']==.001
    guardar(run/'caida.json',dict(limite=1.,consumido=.1,pendiente=True,ajustes=[]))
    assert Presupuesto(run/'caida.json',1).data['consumido']==1
    slow=Presupuesto(run/'terminacion.json',.5);before={x.pid for x in multiprocessing.active_children()}
    try:slow.ajustar('lento',Lento(),[[1]],[1]);raise AssertionError('terminación')
    except TimeoutError:pass
    assert before=={x.pid for x in multiprocessing.active_children()}
    guardar(OUT/'pruebas_sinteticas.json',dict(aprobado=True,origen='inventados/dobles/worker_sintetico',ruta=str(run.relative_to(ROOT)),ajustes_panel_real=0,consumo_piloto_real=0,ajustes_dobles_completo=count,grupos=['cinco ventanas/2021 sin fit ni métricas candidatos','990 internos independientes por ventana','selección guardada antes externo; global/especificación','deduplicación ID externo; cinco repeticiones','reanudación sin duplicar ajustes/saldo','externo alterado sin afectar selección','Pipeline spawn y escalador solo entrenamiento/cambio','fallos/reintentos persistentes y límite','caída conservadora/terminación real de doble'],fallos_sinteticos_esperados=True))
    print('Orquestación completa con dobles aprobada; cero ajustes de panel real.',flush=True)
if __name__=='__main__':test()
