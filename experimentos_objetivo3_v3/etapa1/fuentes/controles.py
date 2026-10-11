"""Controles sintéticos; cero ajustes/predicciones sobre el panel real."""
from comun_v3 import *
import math, multiprocessing, tempfile
class Lento:
    def fit(self,X,y):time.sleep(10)
class Falla:
    def fit(self,X,y):raise ValueError('fallo sintético')

def rechaza(call,kind=ValueError):
    try:call()
    except kind:return
    raise AssertionError('no rechazó entrada inválida')

def controles(out=E1/'resultados/sinteticos'):
    out=destino(out);out.mkdir(exist_ok=True)
    passed=[]
    def ok(name):passed.append(name)
    rows=[]
    for code,base in [('05',100),('08',300)]:
        for y,delta in [(2018,0),(2019,7),(2021,20),(2022,25)]:
            rows.append(dict(codigo_departamento=code,anio=y,prom_punt_global=base+delta))
    p=historial(pd.DataFrame(rows).sample(frac=1,random_state=SEMILLA))
    assert p[p.anio==2018].cambio_observado.isna().all()
    assert p[p.anio==2021].anio_previo.eq(2019).all()
    assert p[p.anio==2021].cambio_observado.eq(13).all() # no dividir por dos
    assert p.loc[(p.codigo_departamento=='08')&(p.anio==2021),'puntaje_previo'].item()==307
    rechaza(lambda:historial(pd.concat([p,p.iloc[:1]])))
    rechaza(lambda:historial(pd.DataFrame([dict(codigo_departamento='05',anio=2020,prom_punt_global=100)])))
    changed=pd.DataFrame(rows);changed.loc[changed.anio==2022,'prom_punt_global']=9999
    original=historial(pd.DataFrame(rows)); altered=historial(changed)
    pd.testing.assert_frame_equal(original[original.anio<=2021],altered[altered.anio<=2021])
    ok('historial aislado por territorio; anterioridad; 2018; salto sin anualizar; futuro no altera pasado')
    ws=ventanas();assert [len(w['internas']) for w in ws]==[0,1,2,3,4]
    for w in ws:
        assert 2018 not in w['entrenamiento'] and 2020 not in w['entrenamiento']
        for i in w['internas']:assert min(i['entrenamiento'])==2019 and max(i['entrenamiento'])<i['validacion']
    fixed=seleccionar([],[],2021);assert set(ids_externos(fixed))=={'persistencia'}
    rechaza(lambda:seleccionar([dict(id='persistencia')],[],2021))
    rechaza(lambda:construir(candidatos()[0]))
    ok('ventanas exactas; 2021 persistencia fija sin candidatos puntuados')
    prev=np.array([100.,300.,200.]);delta=np.array([10.,-20.,-250.])
    pred=reconstruir(prev,delta);assert pred.tolist()==[110.,280.,-50.] # sin clipping
    rechaza(lambda:reconstruir([1],[float('nan')]))
    target=np.array([112.,277.,-48.]); m=metricas(target,pred)
    errors=[a-b for a,b in zip(pred.tolist(),target.tolist())]
    den=math.fsum((v-math.fsum(target)/3)**2 for v in target)
    independent=dict(n=3,mae=math.fsum(abs(e) for e in errors)/3,rmse=math.sqrt(math.fsum(e*e for e in errors)/3),
                     sesgo=math.fsum(errors)/3,r2=1-math.fsum(e*e for e in errors)/den)
    for k in m:assert math.isclose(m[k],independent[k],abs_tol=1e-12,rel_tol=0)
    assert metricas([2,2],[1,3])['r2'] is None
    assert condicion_personal(100,95,True)['entregar'] and not condicion_personal(100,95.0000000001,True)['entregar']
    assert not condicion_personal(0,0,True)['entregar'] and not condicion_personal(100,90,False)['entregar']
    ok('reconstrucción original sin clipping; métricas independientes; umbral exacto/finito/completo')
    pp=p[p.anio==2021];v,info=persistencia(pp)
    np.testing.assert_array_equal(v,pp.puntaje_previo)
    repeat,_=persistencia(pp);np.testing.assert_allclose(v,repeat,atol=1e-10,rtol=0)
    assert info['ajustes']==0 and info['segundos_calculo']>=0
    pd.DataFrame(dict(previo=prev,cambio=delta,prediccion=pred,observado=target)).to_csv(destino(out/'reconstruccion_sintetica.csv'),index=False)
    ok('persistencia sin ajuste y repetición recalculada')
    cs=candidatos();assert len(cs)==100
    old=read(anterior.F2/'resultados/configuraciones_congeladas.json')['configuraciones'][1:]
    for c,o in zip(cs[1:],old):
        assert c['id']=='delta_'+o['id'] and c['parametros']==o['parametros'] and c['parametros_completos']==o['parametros_completos']
        assert c['entradas']==['puntaje_previo',*o['entradas']]
    X=np.array([[1.,2.],[3.,4.],[5.,6.]]);y=np.array([2.,3.,7.])
    for family in ('ols','ridge','elastic_net','svr'):
        c=next(c for c in cs if c['familia']==family)
        a=construir(c);a.fit(X,y);s=a.named_steps['escalado']
        np.testing.assert_array_equal(s.mean_,[3.,4.]);assert int(s.n_samples_seen_)==3
        a.predict(np.array([[1e50,-1e50]]));np.testing.assert_array_equal(s.mean_,[3.,4.])
    for family in ('gradient_boosting','extra_trees'):
        assert not hasattr(construir(next(c for c in cs if c['familia']==family)),'named_steps')
    # Construcción del objetivo y reconstrucción probadas con datos inventados.
    synthetic=p[p.anio==2021].copy()
    for col in anterior.ESPECIFICACIONES['ambas']:synthetic[col]=[10.,20.]
    for spec in ESPECIFICACIONES:
        c=next(c for c in cs if c['familia']=='ols' and c['especificacion']==spec)
        xx,yy=matrices_entrenamiento(synthetic,c)
        assert xx.shape==(2,len(ESPECIFICACIONES[spec])) and yy.tolist()==[13.,13.]
        np.testing.assert_array_equal(xx[:,0],synthetic.puntaje_previo)
        fitted=construir(c).fit(xx,yy)
        final=reconstruir(synthetic.puntaje_previo,fitted.predict(xx))
        np.testing.assert_allclose(final,synthetic.prom_punt_global,atol=1e-10,rtol=0)
        assert metricas(synthetic.prom_punt_global,final)['r2'] is not None
        assert metricas(yy,fitted.predict(xx))['r2'] is None
        rechaza(lambda:matrices_entrenamiento(synthetic,{**c,'entradas':[*c['entradas'],'anio']}))
    invalid=synthetic.copy();invalid['cambio_observado']=np.nan
    rechaza(lambda:matrices_entrenamiento(invalid,c))
    ok('100 entradas/parámetros/defaults exactos; cuatro escaladores solo entrenamiento; árboles sin escalado')
    def scores(mae=9.,rmse=10.):return [dict(id=c['id'],estado='completo',ventanas=[2021],mae=mae,rmse=rmse) for c in cs]
    rs=scores();rs[0].update(mae=1.09,rmse=1.09);rs[1].update(mae=1.,rmse=1.)
    d=seleccionar(rs,[2021],2022);assert d['global_id']=='persistencia' and set(d['especificaciones'].values())=={'persistencia'}
    rs=scores();rs[0].update(mae=1.1000001,rmse=1.);rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rs=scores();rs[0].update(mae=1.,rmse=1.1000001);rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rs=scores(1.,1.);rs[0]['estado']='fallo'
    assert seleccionar(rs,[2021],2022)['global_id']=='delta_ols_ipm_00'
    rs[1]['mae_externo']=0;rechaza(lambda:seleccionar(rs,[2021],2022))
    rs=scores();rs[0]['ventanas']=[];rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    # Orden JSON cuando empatan dos configuraciones Ridge de la misma especificación.
    tied=scores()
    for r in tied:r['estado']='fallo'
    ridges=[c for c in cs if c['familia']=='ridge' and c['especificacion']=='ipm'][:2]
    for c in ridges:next(r for r in tied if r['id']==c['id']).update(estado='completo',mae=1.,rmse=1.)
    # Persistencia sigue completa para las otras especificaciones, fuera de las bandas globales.
    tied[0].update(estado='completo',mae=9.,rmse=10.)
    assert seleccionar(tied,[2021],2022)['global_id']==ridges[0]['id']
    rechaza(lambda:seleccionar(scores(),[2019],2022))
    assert ids_externos({'global_id':cs[1]['id'],'especificaciones':{'ipm':cs[1]['id'],'tasas':'persistencia','ambas':cs[1]['id']}})==['persistencia',cs[1]['id']]
    ok('bandas MAE/RMSE; cero entradas ajustadas; familia/JSON; elegibilidad; fuga rechazada; deduplicación por ID')
    assert etiqueta_interna('e2022_i2021_delta_ols_ipm_00')
    assert not etiqueta_interna('e2022_externo_delta_ols_ipm_00')
    assert not etiqueta_interna('e2022_i2019_delta_ols_ipm_00')
    ok('E3-01 regex temporal completa; E3-02 antecedente separado; cota nueva 1010')
    rechaza(lambda:guardar(ROOT/'experimentos_objetivo3_v2/no_escribir.json',{}))
    rechaza(lambda:Presupuesto(ROOT/'experimentos_objetivo3_v2/no_ledger.json'))
    # Huella alterada y llaves inconsistentes detectables sin métricas reales.
    scratch=destino(out/'huella_sintetica.txt');scratch.write_text('antes')
    previous_hash=sha(scratch);scratch.write_text('después');assert sha(scratch)!=previous_hash
    left=pd.DataFrame(dict(codigo_departamento=['05','08'],anio=[2021,2021],a=[1.,2.]))
    right=pd.DataFrame(dict(codigo_departamento=['05','08'],anio=[2021,2021],b=[3.,4.]))
    assert len(compartido.unir(left,right,['b']))==2
    rechaza(lambda:compartido.unir(left,right.iloc[:1],['b']))
    rechaza(lambda:compartido.unir(left,pd.concat([right,right.iloc[:1]]),['b']))
    ok('rutas restringidas a v3; huellas y llaves incorrectas detectadas')
    # Cada ejecución usa una carpeta sintética distinta; nunca ledger operativo.
    run=Path(tempfile.mkdtemp(prefix='prueba_',dir=out))
    b=Presupuesto(run/'ledger_doble.json',1.)
    b.ajustar('doble',None,None,None,executor=lambda *a:('resultado',.2))
    b=Presupuesto(run/'ledger_doble.json',1.);assert b.data['consumido']==.2
    rechaza(lambda:Presupuesto(run/'ledger_doble.json',2.))
    rechaza(lambda:b.ajustar('limite',None,None,None,executor=lambda *a:('resultado',.8)),TimeoutError)
    assert b.data['consumido']==1 and not b.data['pendiente']
    rechaza(lambda:Presupuesto(run/'ledger_doble.json',1).ajustar('agotado',None,None,None),TimeoutError)
    guardar(run/'caida.json',dict(limite=1.,consumido=.1,pendiente=True,ajustes=[]))
    crash=Presupuesto(run/'caida.json',1.);assert crash.data['consumido']==1 and not crash.data['pendiente']
    interrupted=Presupuesto(run/'interrupcion_medida.json',2.)
    def stop(*a):raise KeyboardInterrupt('interrupción sintética')
    rechaza(lambda:interrupted.ajustar('interrumpido',None,None,None,executor=stop),KeyboardInterrupt)
    assert not interrupted.data['pendiente'] and interrupted.data['consumido']>0
    # Proceso spawn realmente terminado por el límite, arranque incluido.
    before={c.pid for c in multiprocessing.active_children()}
    real=Presupuesto(run/'terminacion_real_doble.json',.4)
    started=time.monotonic()
    rechaza(lambda:real.ajustar('lento_sintetico',Lento(),X,y),TimeoutError)
    assert time.monotonic()-started<5 and real.data['consumido']==.4
    assert {c.pid for c in multiprocessing.active_children()}==before
    failed=Presupuesto(run/'fallo_real_doble.json',10.)
    rechaza(lambda:failed.ajustar('falla_sintetica',Falla(),X,y),RuntimeError)
    assert failed.data['consumido']>0 and failed.data['ajustes'][0]['estado']=='error'
    ok('presupuesto persistente/reanudación; saldo no ampliable; caída/interrupción/fallo; límite spawn y terminación real')
    result=dict(aprobado=True,origen='exclusivamente sintético/dobles',controles=passed,
        ajustes_panel_real=0,predicciones_panel_real=0,consumo_piloto_real=0,ledger_operativo_creado=False,
        metricas_sinteticas=m,semilla=SEMILLA,pruebas_presupuesto=str(run.relative_to(ROOT)))
    guardar(out/'controles.json',result)
    print(f'{len(passed)} grupos de controles sintéticos aprobados; cero consumo del piloto.')
    return result
if __name__=='__main__':controles()
