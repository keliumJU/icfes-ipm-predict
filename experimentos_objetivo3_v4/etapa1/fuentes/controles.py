"""Pruebas exclusivamente inventadas/dobles, nunca cargar ni ajustar el panel."""
from comun_v4 import *
import tempfile,time,multiprocessing
class Lento:
    def fit(self,X,y):time.sleep(10)
class Falla:
    def fit(self,X,y):raise ValueError('numérico sintético')
class NoConverge:
    def fit(self,X,y):
        import warnings
        from sklearn.exceptions import ConvergenceWarning
        warnings.warn('convergencia sintética',ConvergenceWarning)
        return self
def rechaza(call,kind=ValueError):
    try:call()
    except kind:return
    raise AssertionError('no rechazó')

def controles(out=OUT/'sinteticos'):
    out=destino(out);out.mkdir(exist_ok=True)
    run=Path(tempfile.mkdtemp(prefix='prueba_',dir=out));passed=[]
    rows=[]
    for code,base in [('05',100),('08',300)]:
        for y,delta in [(2018,0),(2019,7),(2021,20),(2022,25)]:
            rows.append(dict(codigo_departamento=code,anio=y,prom_punt_global=base+delta,**{s:50-delta+j for j,s in enumerate(COV)}))
    source=pd.DataFrame(rows);p=historial(source.sample(frac=1,random_state=SEMILLA))
    assert p[p.anio==2018].cambio_observado.isna().all()
    assert p[p.anio==2021].anio_previo.eq(2019).all()
    assert p[p.anio==2021].cambio_observado.eq(13).all()
    assert p[p.anio==2021].cambio_ipm.eq(-13).all()
    assert p[(p.codigo_departamento=='08')&(p.anio==2021)].puntaje_previo.item()==307
    q=source.copy();q.loc[q.anio==2022,COV+[anterior.RESULTADO]]=9999
    a=historial(q)
    pd.testing.assert_frame_equal(p[p.anio<=2021].reset_index(drop=True),a[a.anio<=2021].reset_index(drop=True))
    rechaza(lambda:historial(pd.concat([source,source.iloc[:1]])))
    rechaza(lambda:historial(source.assign(anio=2020)))
    passed.append('anterioridad/aislamiento territorial/futuro/salto/diferencias negativas y misma llave')
    cs=candidatos();assert len(cs)==29 and len({c['id'] for c in cs})==29
    assert [len(v) for v in GRUPOS.values()]==[1,2,2,16,17]
    assert [c['familia'] for c in cs]==['persistencia']+['correccion_comun']*3+['ridge']*15+['huber']*10
    old=read(ROOT/'experimentos_objetivo3_v3/etapa1/resultados/configuraciones_congeladas.json')['configuraciones']
    ridge=next(c for c in old if c['familia']=='ridge')['parametros_completos']
    for c in cs:
        if c['familia']=='ridge':
            for k,v in ridge.items():
                if k.startswith(('modelo__','escalado__')) and k!='modelo__alpha':assert c['parametros_completos'][k]==v
    assert [len(w['internas']) for w in ventanas()]==[0,1,2,3,4]
    assert 28*sum(len(w['internas']) for w in ventanas())+6*4+4==308
    rechaza(lambda:construir(cs[0]));rechaza(lambda:seleccionar([{}],[],2021))
    assert ids_externos(seleccionar([],[],2021))==['persistencia']
    for group in GRUPOS:
        c=next(c for c in cs if c['familia']=='ridge' and c['especificacion']==group)
        X,y=matrices_entrenamiento(p[p.anio==2021],c)
        assert X.shape==(2,len(GRUPOS[group])) and y.tolist()==[13,13]
        rechaza(lambda:matrices_entrenamiento(p[p.anio==2021],{**c,'entradas':c['entradas']+['anio']}))
    passed.append('grilla29/orden/defaults/matrices1-2-2-16-17/ventanas/cota308/persistencia sin fit')
    X=np.arange(4.).reshape(-1,1);y=np.array([-3.,1.,5.,9.])
    for c in cs[1:4]:
        m=construir(c).fit(X,y);assert m.mediana_==3 and m.n_train_==4
        np.testing.assert_array_equal(m.predict([[1e9],[-1e9]]),[3*c['parametros']['lam']]*2)
        assert m.mediana_==3
    assert CorreccionComun().fit(X[:3],y[:3]).mediana_==1
    rechaza(lambda:CorreccionComun().fit(X,y*np.nan))
    passed.append('mediana todas las filas train/n par e impar/lambda fijo/validación extrema no interviene')
    X=np.array([[1.,2.],[3.,4.],[5.,6.],[7.,8.]]);y=np.array([1.,3.,5.,7.])
    for family in ('ridge','huber'):
        c=next(c for c in cs if c['familia']==family and c['especificacion']=='nivel_ipm')
        model=construir(c).fit(X,y);sc=model.named_steps['escalado']
        np.testing.assert_array_equal(sc.mean_,[4,5]);assert sc.n_samples_seen_==4
        model.predict([[1000,-1000]]);np.testing.assert_array_equal(sc.mean_,[4,5])
        assert serial(construir(c).get_params(deep=True))==c['parametros_completos']
    pred=reconstruir([100,300,200],[10,-20,-250]);assert pred.tolist()==[110,280,-50]
    obs=np.array([112,277,-48]);e=pred-obs;m=metricas(obs,pred)
    assert m['mae']==math.fsum(abs(float(v)) for v in e)/3
    assert abs(m['rmse']-math.sqrt(math.fsum(float(v)**2 for v in e)/3))<1e-12
    assert m['sesgo']==math.fsum(map(float,e))/3
    den=math.fsum((float(v)-math.fsum(map(float,obs))/3)**2 for v in obs)
    assert abs(m['r2']-(1-math.fsum(float(v)**2 for v in e)/den))<1e-12
    rechaza(lambda:reconstruir([1],[np.nan]))
    a,info=persistencia(p[p.anio==2021]);b,_=persistencia(p[p.anio==2021])
    np.testing.assert_allclose(a,b,atol=1e-10,rtol=0);assert info['ajustes']==0
    assert compartido.condicion_personal(100,95,True)['entregar']
    assert not compartido.condicion_personal(100,95.0000000001,True)['entregar']
    passed.append('scaler solo train ambos pipelines/reconstrucción sin clipping/métricas independientes/repetición/umbral sintético')
    def scores():return [dict(id=c['id'],estado='completo',ventanas=[2021],mae=9.,rmse=10.) for c in cs]
    rs=scores();rs[0].update(mae=1.09,rmse=1.09);rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']=='persistencia'
    rs[0]['mae']=1.10000001;d=seleccionar(rs,[2021],2022)
    assert d['global_id']==cs[1]['id'] and set(d['especificaciones'].values())=={cs[1]['id']}
    rs=scores();rs[0].update(mae=1.,rmse=1.10000001);rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rs=scores();rs[1].update(mae=0,rmse=0,ventanas=[])
    assert seleccionar(rs,[2021],2022)['global_id']=='persistencia'
    rs[1]['mae_externo']=0;rechaza(lambda:seleccionar(rs,[2021],2022))
    rs=scores();rs[1].update(mae=float('nan'),rmse=0.)
    assert seleccionar(rs,[2021],2022)['global_id']=='persistencia'
    rs=scores();rs[1].update(mae=1.,rmse=1.);rs[2].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rechaza(lambda:seleccionar(scores(),[2019],2022))
    rs=scores();rs[0]['estado']='fallo';rechaza(lambda:seleccionar(rs,[2021],2022))
    # Global puede diferir de ganador de su grupo: mínimo global excluye candidato
    # menos complejo que sí cae en banda local. Preservar los seis IDs posibles.
    rs=scores();rs[4].update(mae=1.15,rmse=1.);rs[5].update(mae=1.06,rmse=1.)
    ident=next(c['id'] for c in cs if c['familia']=='ridge' and c['especificacion']=='nivel_ipm')
    next(r for r in rs if r['id']==ident).update(mae=1.,rmse=2.)
    decision=seleccionar(rs,[2021],2022)
    assert decision['global_id']==cs[5]['id'] and decision['especificaciones']['historico']==cs[4]['id']
    distinct=dict(global_id=cs[5]['id'],especificaciones={g:next(c['id'] for c in cs if c['familia']=='huber' and c['especificacion']==g) for g in GRUPOS})
    assert len(ids_externos(distinct))==6
    passed.append('bandas MAE/RMSE/entradas/familias/JSON/elegibilidad/campos externos/grupos comunes/global distinto/6 IDs')
    assert etiqueta_interna('e2022_i2021_ridge_cambio_ipm_00')
    assert not etiqueta_interna('e2022_externo_ridge_cambio_ipm_00')
    assert not etiqueta_interna('e2022_i2024_ridge_cambio_ipm_00')
    assert not etiqueta_interna('e2022_i2021_ridge_cambio_ipm_00_extra')
    rechaza(lambda:guardar(ROOT/'experimentos_objetivo3_v3/no_escribir.json',{}))
    rechaza(lambda:Presupuesto(ROOT/'experimentos_objetivo3_v2/no_escribir.json'))
    f=destino(run/'huella.txt');f.write_text('antes');h=sha(f);f.write_text('después');assert sha(f)!=h
    passed.append('regex completa temporal/huellas alteradas/rutas rechazadas')
    budget=Presupuesto(run/'ledger_doble.json',1)
    budget.ajustar('a',None,None,None,executor=lambda *args:('ok',.2))
    budget=Presupuesto(run/'ledger_doble.json',1);assert budget.data['consumido']==.2
    rechaza(lambda:Presupuesto(run/'ledger_doble.json',2))
    rechaza(lambda:budget.ajustar('b',None,None,None,executor=lambda *args:('ok',.8)),TimeoutError)
    assert budget.data['consumido']==1
    guardar(run/'caida.json',dict(limite=1.,consumido=.1,pendiente=True,ajustes=[]))
    assert Presupuesto(run/'caida.json',1).data['consumido']==1
    b=Presupuesto(run/'intentos.json',10);calls=[]
    def retry(*args):
        calls.append(1)
        if len(calls)==1:raise OSError('infraestructura sintética')
        return 'ok',.2
    assert ajuste_con_fallos(b,'a',None,None,None,retry)=='ok' and len(b.data['ajustes'])==2
    assert b.data['consumido']>.2
    b=Presupuesto(run/'intentos.json',10);rechaza(lambda:ajuste_con_fallos(b,'a',None,None,None,retry))
    def failure(*args):raise OSError('infraestructura persistente')
    b=Presupuesto(run/'persistente.json',10)
    rechaza(lambda:ajuste_con_fallos(b,'a',None,None,None,failure),OSError)
    rechaza(lambda:ajuste_con_fallos(Presupuesto(run/'persistente.json',10),'a',None,None,None,failure),RuntimeError)
    assert len(b.data['ajustes'])==2
    def numerical(*args):raise FloatingPointError('numérico')
    b=Presupuesto(run/'numerico.json',10);rechaza(lambda:ajuste_con_fallos(b,'a',None,None,None,numerical),FloatingPointError)
    assert len(b.data['ajustes'])==1
    rechaza(lambda:ajuste_con_fallos(Presupuesto(run/'numerico.json',10),'a',None,None,None,numerical))
    before={p.pid for p in multiprocessing.active_children()};b=Presupuesto(run/'terminacion.json',.4);start=time.monotonic()
    rechaza(lambda:b.ajustar('lento',Lento(),X,y),TimeoutError)
    assert time.monotonic()-start<5 and b.data['consumido']==.4
    assert {p.pid for p in multiprocessing.active_children()}==before
    b=Presupuesto(run/'fallo_real.json',10);rechaza(lambda:ajuste_con_fallos(b,'numerico',Falla(),X,y))
    assert len(b.data['ajustes'])==1 and b.data['consumido']>0
    b=Presupuesto(run/'convergencia_real.json',10);rechaza(lambda:ajuste_con_fallos(b,'no_converge',NoConverge(),X,y))
    assert len(b.data['ajustes'])==1 and b.data['ajustes'][0]['clase_fallo']=='numerico_convergencia'
    b=Presupuesto(run/'interrupcion.json',10)
    def interrupt(*args):raise KeyboardInterrupt()
    rechaza(lambda:b.ajustar('interrumpido',None,None,None,executor=interrupt),KeyboardInterrupt)
    assert b.data['consumido']>0 and not b.data['pendiente']
    passed.append('presupuesto serial/reanudación/no ampliación/intentos/fallos/caída/interrupción/límite/terminación real spawn')
    result=dict(aprobado=True,origen='sintéticos/dobles exclusivamente',controles=passed,pruebas=str(run.relative_to(ROOT)),
                ajustes_panel=0,ledger_operativo_creado=False,semilla=SEMILLA,
                fuentes_sha256={str(f.relative_to(ROOT)):sha(f) for f in [Path(__file__),E1/'fuentes/comun_v4.py']})
    guardar(out/'controles.json',result);print(f'{len(passed)} grupos sintéticos aprobados.');return result
if __name__=='__main__':controles()
