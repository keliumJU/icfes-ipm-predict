"""Datos exclusivamente inventados y dobles. No lee el panel para ajustar."""
from comun_v5 import *
import tempfile,time,multiprocessing,warnings
from unittest.mock import patch
from types import SimpleNamespace
class Lento:
    def fit(self,X,y):time.sleep(20)
class HiGHSFalla:
    """Proceso real; doble de linprog falla, Pipeline completo propio."""
    def __init__(self,c,convergencia=False):self.c=c;self.convergencia=convergencia
    def fit(self,X,y):
        import sklearn.linear_model._quantile as q
        from unittest.mock import patch
        model=construir(self.c)
        if self.convergencia:
            with patch.object(q,'linprog',return_value=SimpleNamespace(x=np.zeros(2*(X.shape[1]+1)+2*len(y)),success=False,status=1,message='doble HiGHS límite',nit=1)):model.fit(X,y)
        else:
            with patch.object(q,'linprog',side_effect=ValueError('HiGHS numérico sintético')):model.fit(X,y)
        return self

def rechaza(call,kind=Exception):
    try:call()
    except kind:return
    raise AssertionError('no rechazó')

def datos():
    rows=[]
    for code,base in [('05',100),('08',300)]:
        for y,delta in [(2018,0),(2019,7),(2021,20),(2022,25)]:
            rows.append(dict(codigo_departamento=code,anio=y,prom_punt_global=base+delta,**{s:50-delta+j for j,s in enumerate(COV)}))
    return pd.DataFrame(rows)

def ejecutar(out=OUT/'sinteticos'):
    out=destino(out);out.mkdir(exist_ok=True)
    run=Path(tempfile.mkdtemp(prefix='controles_',dir=out));passed=[]
    source=datos();p=historial(source.sample(frac=1,random_state=SEMILLA))
    assert p[p.anio==2018].cambio_observado.isna().all()
    assert p[p.anio==2021].anio_previo.eq(2019).all() and p[p.anio==2021].cambio_observado.eq(13).all()
    assert p[p.anio==2021].cambio_ipm.eq(-13).all()
    assert p[(p.codigo_departamento=='08')&(p.anio==2021)].puntaje_previo.item()==307
    q=source.copy();q.loc[q.anio==2022,COV+['prom_punt_global']]=9999
    a=historial(q);igualdad_exacta(p[p.anio<=2021].reset_index(drop=True),a[a.anio<=2021].reset_index(drop=True))
    rechaza(lambda:historial(pd.concat([source,source.iloc[:1]])))
    rechaza(lambda:historial(source.assign(anio=2020)))
    np.testing.assert_array_equal(reconstruir([100,300,200],[10,-20,-250]),[110,280,-50])
    rechaza(lambda:reconstruir([1],[np.nan]))
    observed=np.array([112,277,-48]);pred=reconstruir([100,300,200],[10,-20,-250]);m=metricas(observed,pred)
    assert m['mae']==math.fsum(abs(float(v)) for v in pred-observed)/3
    pp,info=persistencia(p[p.anio==2021]);np.testing.assert_array_equal(pp,[107,307]);assert info['ajustes']==0
    passed.append('historial misma llave/futuro/anterioridad/2021 previo2019/salto/diferencias negativas/reconstrucción/metricas en puntos')
    cs=candidatos();assert len(cs)==36 and len({c['id'] for c in cs})==36
    assert [c['orden'] for c in cs]==list(range(36))
    assert [c['familia'] for c in cs]==['persistencia']+['mediana']*15+['boosting_absoluto']*20
    assert GRUPOS==previo.GRUPOS and [len(v) for v in GRUPOS.values()]==[1,2,2,16,17]
    assert [(c['especificacion'],c['parametros']['alpha']) for c in cs[1:16]]==[(g,a) for g in GRUPOS for a in (.01,.1,1.)]
    assert [(c['especificacion'],c['parametros']['learning_rate'],c['parametros']['max_depth']) for c in cs[16:]]==[(g,lr,d) for g in GRUPOS for lr in (.03,.1) for d in (1,2)]
    assert [len(w['internas']) for w in ventanas()]==[0,1,2,3,4] and ventanas()[0]['entrenamiento']==[]
    assert 35*sum(len(w['internas']) for w in ventanas())+6*4+4==378
    for w in ventanas()[1:]:
        assert w['entrenamiento']==[a for a in ANIOS if 2018<a<w['externo']]
        for i in w['internas']:assert i['entrenamiento']==[a for a in ANIOS if 2018<a<i['validacion']]
    for c in cs[1:]:
        X,y=matrices_entrenamiento(p[p.anio==2021],c)
        assert X.shape==(2,len(GRUPOS[c['especificacion']])) and y.tolist()==[13,13]
        rechaza(lambda:matrices_entrenamiento(p[p.anio==2021],{**c,'entradas':c['entradas']+['anio']}))
        assert serial(construir(c).get_params(deep=True))==c['parametros_completos']
    rechaza(lambda:construir(cs[0]));rechaza(lambda:matrices_entrenamiento(p,cs[1]))
    expansivo=pd.DataFrame([dict(codigo_departamento=f'{j:02d}',anio=a,prom_punt_global=200.+a-2018+j,**{s:float(k+10) for k,s in enumerate(COV)}) for j in range(33) for a in ANIOS])
    expansivo=historial(expansivo)
    for w in ventanas():
        train,test=dividir(expansivo,w['entrenamiento'],w['externo'])
        assert len(test)==33 and len(train)==33*len(w['entrenamiento'])
        for internal in w['internas']:
            train,test=dividir(expansivo,internal['entrenamiento'],internal['validacion'])
            assert len(train)==33*len(internal['entrenamiento']) and train.anio.max()<test.anio.min()
    rechaza(lambda:dividir(expansivo,[2019,2022],2022),ValueError)
    passed.append('grilla36 IDs/orden/grupos íntegros/defaults completos/matrices1-2-2-16-17/ventanas/cota378')
    # Mediana condicional: media=33.67 frente mediana=1, y grupo alto mediana=11.
    X=np.array([[0.]]*3+[[1.]]*3);y=np.array([0.,1.,100.,10.,11.,110.])
    c=cs[1];model=construir(c).fit(X,y)
    np.testing.assert_allclose(model.predict([[0],[1]]),[1,11],atol=1e-10,rtol=0)
    assert not np.isclose(model.predict([[0]])[0],np.mean(y[:3]))
    strong=construir(cs[3]).fit(X,y);assert abs(strong.named_steps['modelo'].coef_[0])<abs(model.named_steps['modelo'].coef_[0])
    sc=model.named_steps['escalado'];np.testing.assert_array_equal(sc.mean_,[.5]);assert sc.n_samples_seen_==6
    old_mean=sc.mean_.copy();model.predict([[1e12]]);np.testing.assert_array_equal(sc.mean_,old_mean)
    assert model.named_steps['modelo'].quantile==.5 and model.named_steps['modelo'].solver=='highs'
    passed.append('mediana condicional no media/regularización L1/scaler solo train/Pipeline objetivo no escalado')
    cb=cs[16];xb=np.arange(30.).reshape(-1,1);yb=np.sin(xb[:,0])+xb[:,0]/4
    a=construir(cb).fit(xb,yb);b=construir(cb).fit(xb,yb)
    np.testing.assert_array_equal(a.predict(xb),b.predict(xb))
    assert a.loss=='absolute_error' and a.random_state==SEMILLA and a.n_estimators_==100 and a.min_samples_leaf==3 and a.n_iter_no_change is None
    assert not isinstance(a,Pipeline)
    passed.append('boosting absoluto/defaults íntegros/semilla fija/sin escalado ni parada temprana')
    def scores():return [dict(id=c['id'],estado='completo',ventanas=[2021],mae=9.,rmse=10.,razon=None) for c in cs]
    rs=scores();rs[0].update(mae=1.09,rmse=1.09);rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']=='persistencia'
    rs[0]['mae']=1.10000001;assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rs=scores();rs[0].update(mae=1.,rmse=1.10000001);rs[1].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rs=scores();rs[1].update(estado='inelegible',mae=None,rmse=None,razon='numérico');d=seleccionar(rs,[2021],2022)
    assert len(d['candidatos'])==36 and not d['candidatos'][1]['elegible'] and d['global_id']=='persistencia'
    rs[1]['razon']=None;rechaza(lambda:seleccionar(rs,[2021],2022))
    rs=scores();rs[1].update(ventanas=[],mae=0.,rmse=0.,razon='incompleto');assert seleccionar(rs,[2021],2022)['global_id']=='persistencia'
    rs=scores();rs[1].update(mae=float('nan'),razon='no finito');assert seleccionar(rs,[2021],2022)['global_id']=='persistencia'
    rs=scores();rs[1].update(mae=1.,rmse=1.);rs[2].update(mae=1.,rmse=1.);rs[16].update(mae=1.,rmse=1.)
    assert seleccionar(rs,[2021],2022)['global_id']==cs[1]['id']
    rs[1]['mae_externo']=0;rechaza(lambda:seleccionar(rs,[2021],2022))
    rs=scores();rs[0]['estado']='fallo';rs[0]['razon']='falta';rechaza(lambda:seleccionar(rs,[2021],2022))
    rechaza(lambda:seleccionar(scores()[::-1],[2021],2022));rechaza(lambda:seleccionar(scores()[:-1],[2021],2022));rechaza(lambda:seleccionar(scores(),[2019],2022))
    assert ids_externos(seleccionar([],[],2021))==['persistencia'];rechaza(lambda:seleccionar(scores(),[],2021))
    rs=scores();rs[1].update(mae=1.15,rmse=1.);rs[2].update(mae=1.06,rmse=1.);rs[4].update(mae=1.,rmse=2.)
    decision=seleccionar(rs,[2021],2022)
    assert decision['global_id']==cs[2]['id'] and decision['especificaciones']['historico']==cs[1]['id']
    distinct=dict(global_id=cs[2]['id'],especificaciones={g:next(c['id'] for c in cs if c['familia']=='boosting_absoluto' and c['especificacion']==g) for g in GRUPOS})
    assert len(ids_externos(distinct))==6
    distinct['especificaciones']['historico']=distinct['global_id'];assert len(ids_externos(distinct))==5
    # Concatenación igual peso filas, no promedios de tamaños desiguales.
    assert metricas([0,0,0],[0,3,6])['mae']==3
    passed.append('bandas MAE/RMSE/entradas/familia/JSON/36 registros y razones/2021 fijo/global distinto del grupo/ID deduplicado solo en ventana')
    codes=[f'{i:02d}' for i in range(33)]
    cover=pd.DataFrame([dict(procedimiento=r,codigo_departamento=c,anio=y,observado=200.,prediccion=201.) for r in PROCEDIMIENTOS for c in codes for y in range(2021,2026)])
    assert cobertura(cover,codes)
    rechaza(lambda:cobertura(cover.iloc[:-1],codes))
    corrupt=cover.copy();corrupt.loc[1,LLAVES]=corrupt.loc[0,LLAVES];rechaza(lambda:cobertura(corrupt,codes))
    corrupt=cover.copy();corrupt.loc[0,'prediccion']=np.nan;rechaza(lambda:cobertura(corrupt,codes))
    corrupt=cover.copy();corrupt.loc[165,'observado']=200.00000000001;rechaza(lambda:cobertura(corrupt,codes))
    # CSV realmente escritos/leídos con inferencia int/float distinta.
    a=pd.DataFrame(dict(codigo_departamento=['05','08'],anio=[2022,2022],cambio_predicho=[0,0]))
    b=a.copy();b.cambio_predicho=b.cambio_predicho.astype(float)
    a.to_csv(destino(run/'cero_int.csv'),index=False);b.to_csv(destino(run/'cero_float.csv'),index=False)
    aa=pd.read_csv(run/'cero_int.csv',dtype={'codigo_departamento':str});bb=pd.read_csv(run/'cero_float.csv',dtype={'codigo_departamento':str})
    assert aa.cambio_predicho.dtype!=bb.cambio_predicho.dtype;igualdad_exacta(aa,bb)
    for field,value in [('cambio_predicho',1e-11),('codigo_departamento','11'),('anio',2021)]:
        q=bb.copy();q.loc[0,field]=value;rechaza(lambda:igualdad_exacta(aa,q),AssertionError)
    rechaza(lambda:igualdad_exacta(aa,bb.iloc[::-1].reset_index(drop=True)),AssertionError)
    rechaza(lambda:igualdad_exacta(aa,bb[list(reversed(bb.columns))]),AssertionError)
    rechaza(lambda:igualdad_exacta(aa,bb.rename(columns={'anio':'year'})),AssertionError)
    passed.append('cobertura1155/7×165/llaves y observados/CSV igualdad exacta cero int-float/rechazo1e-11 llaves campos orden')
    rechaza(lambda:guardar(ROOT/'experimentos_objetivo3_v4/prohibido.json',{}),ValueError)
    rechaza(lambda:PresupuestoSintetico(OUT/'ledger.json'),ValueError)
    # Symlink escapa también se rechaza sin escribir en antecedente.
    link=run/'escape';link.symlink_to(ROOT/'experimentos_objetivo3_v4',target_is_directory=True)
    rechaza(lambda:destino(link/'prohibido.json'),ValueError);link.unlink()
    f=destino(run/'artefacto.txt');f.write_text('completo');hashes={str(f.relative_to(ROOT)):sha(f)}
    b=PresupuestoSintetico(run/'reanudacion.json',10);b.ajustar('a#1',None,None,None,executor=lambda *args:('ok',.2))
    b=PresupuestoSintetico(run/'reanudacion.json',10);assert b.data['consumido']==.2
    assert verificar_reanudacion({'x':'sha'},{'x':'sha'},hashes,b,'a')==1
    rechaza(lambda:verificar_reanudacion({},dict(x=1),hashes,b,'a'),ValueError)
    rechaza(lambda:verificar_reanudacion({}, {},{},b,'a'),ValueError)
    f.write_text('alterado');rechaza(lambda:verificar_reanudacion({}, {},hashes,b,'a'),ValueError)
    rechaza(lambda:ajuste_con_fallos(b,'a',None,None,None,lambda *args:('ok',.1)),ValueError)
    rechaza(lambda:PresupuestoSintetico(run/'reanudacion.json',11),ValueError)
    b=PresupuestoSintetico(run/'limite_doble.json',1)
    b.ajustar('a',None,None,None,executor=lambda *args:('ok',.2))
    rechaza(lambda:b.ajustar('b',None,None,None,executor=lambda *args:('ok',.8)),TimeoutError)
    before=len(b.data['ajustes']);rechaza(lambda:ajuste_con_fallos(b,'c',None,None,None),TimeoutError)
    assert b.data['consumido']==1 and len(b.data['ajustes'])==before
    guardar(run/'caida.json',dict(limite=1.,consumido=.1,pendiente=True,ajustes=[]))
    b=PresupuestoSintetico(run/'caida.json',1);assert b.data['consumido']==1 and b.data['ajustes'][-1]['estado']=='interrupcion_no_medida'
    calls=[]
    def retry(*args):
        calls.append(1)
        if len(calls)==1:raise OSError('infraestructura sintética')
        return 'ok',.2
    b=PresupuestoSintetico(run/'retry.json',10);assert ajuste_con_fallos(b,'a',None,None,None,retry)=='ok'
    assert len(b.data['ajustes'])==2 and b.data['consumido']>.2
    def infra(*args):raise OSError('infraestructura')
    b=PresupuestoSintetico(run/'persistente.json',10);rechaza(lambda:ajuste_con_fallos(b,'a',None,None,None,infra),OSError)
    rechaza(lambda:ajuste_con_fallos(PresupuestoSintetico(run/'persistente.json',10),'a',None,None,None,infra),RuntimeError)
    assert len(b.data['ajustes'])==2
    def numeric(*args):raise FloatingPointError('numérico')
    b=PresupuestoSintetico(run/'numerico.json',10);rechaza(lambda:ajuste_con_fallos(b,'a',None,None,None,numeric),FloatingPointError)
    rechaza(lambda:ajuste_con_fallos(PresupuestoSintetico(run/'numerico.json',10),'a',None,None,None,numeric),ValueError)
    assert len(b.data['ajustes'])==1
    passed.append('rutas propias y symlink/artefactos huellas/contexto/reanudación/intentos consumidos/un retry/numérico persistente/caída sin tiempo agota/sin saldo no intento')
    # Proceso spawn real carga Pipeline/HiGHS/boosting con entradas inventadas.
    child_before={p.pid for p in multiprocessing.active_children()};worker=[]
    for label,c in [('mediana',cs[1]),('boosting',cs[16])]:
        b=PresupuestoSintetico(run/f'worker_{label}.json',20)
        fitted,captured=ajuste_con_fallos(b,label,construir(c),xb,yb)
        assert not captured and b.data['consumido']>0 and len(b.data['ajustes'])==1
        assert serial(fitted.get_params(deep=True))==c['parametros_completos']
        worker.append(dict(familia=label,segundos=b.data['consumido'],importacion_hijo=True,datos='inventados'))
    for flag in (False,True):
        label='highs_convergencia' if flag else 'highs_fallo'
        b=PresupuestoSintetico(run/f'{label}.json',20)
        rechaza(lambda:ajuste_con_fallos(b,label,HiGHSFalla(cs[1],flag),X,y),ValueError)
        assert len(b.data['ajustes'])==1 and b.data['ajustes'][0]['clase_fallo']=='numerico_convergencia'
        rechaza(lambda:ajuste_con_fallos(PresupuestoSintetico(run/f'{label}.json',20),label,HiGHSFalla(cs[1],flag),X,y),ValueError)
    b=PresupuestoSintetico(run/'terminacion.json',.4);started=time.monotonic()
    rechaza(lambda:b.ajustar('lento',Lento(),X,y),TimeoutError)
    assert time.monotonic()-started<5 and b.data['consumido']==.4
    assert {p.pid for p in multiprocessing.active_children()}==child_before
    b=PresupuestoSintetico(run/'interrupcion.json',10)
    def interrupt(*args):raise KeyboardInterrupt()
    rechaza(lambda:b.ajustar('interrumpido',None,None,None,executor=interrupt),KeyboardInterrupt)
    assert b.data['consumido']>0 and not b.data['pendiente']
    guardar(run/'procesos.json',dict(aprobado=True,workers=worker,terminacion_real=True,hijos_restantes=[],highs_fallo_convergencia_rechazados=True))
    passed.append('imports procesos hijos reales/Pipeline entero/HiGHS fallo y convergencia/inelegibilidad reanudada/terminación real/límite/interrupción')
    files=[Path(__file__),E1/'fuentes/comun_v5.py']
    result=dict(aprobado=True,origen='exclusivamente datos inventados/dobles',controles=passed,pruebas=str(run.relative_to(ROOT)),ajustes_panel=0,ledger_operativo_creado=False,meta_v5_evaluada=False,semilla=SEMILLA,fuentes_sha256={str(f.relative_to(ROOT)):sha(f) for f in files})
    guardar(run/'resumen.json',result);print(json.dumps(dict(aprobado=True,grupos=len(passed),pruebas=result['pruebas'],ajustes_panel=0),ensure_ascii=False));return result
if __name__=='__main__':
    result=ejecutar();guardar(OUT/'controles.json',result)
