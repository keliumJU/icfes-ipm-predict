"""Orquestación v4: datos inventados/dobles; jamás ajusta ni lee el panel real."""
from piloto import *
import tempfile,multiprocessing
from controles import controles,Lento,Falla,NoConverge,rechaza
class DeltaDoble:
    def predict(self,X):return np.full(len(X),5.)
def doble(remaining,model,X,y):
    assert np.isfinite(X).all() and np.isfinite(y).all()
    return (DeltaDoble(),[]),.001

def test():
    sources={str(f.relative_to(ROOT)):sha(f) for f in (E2/'fuentes').glob('*.py')}
    out=destino(OUT/'sinteticos');out.mkdir(exist_ok=True)
    run=Path(tempfile.mkdtemp(prefix='orquestacion_',dir=out))
    controles(run/'interfaces_etapa1') # destinos explícitos v4/etapa2
    rows=[]
    for j,code in enumerate('05 08 11 13 15 17 18 19 20 23 25 27 41 44 47 50 52 54 63 66 68 70 73 76 81 85 86 88 91 94 95 97 99'.split()):
        for k,year in enumerate(ANIOS):
            rows.append(dict(codigo_departamento=code,anio=year,prom_punt_global=200+j+5*k,**{col:10+j*.1+k*.2+z for z,col in enumerate(COV)}))
    p=historial(pd.DataFrame(rows)).reset_index(drop=True)
    r=Runner(run/'completo',p,executor=doble);r.run()
    assert auditar_orden(r.out,candidatos())['intentos']==288
    assert len(r.budget.data['ajustes'])==288 # 280 + 4 externos comunes + 4 repeticiones
    assert not list((r.out/'ajustes').glob('e2021*'))
    assert read(r.out/'seleccion_2021.json')['metricas_internas']==[]
    assert len(read(r.out/'reproducibilidad.json')['repeticiones'])==5
    assert read(r.out/'seleccion_2022.json')['global_id']=='correccion_comun_00'
    for year in range(2021,2026):
        ext=loadcsv(r.out/f'externas_{year}.csv');assert len(ext)==231
        assert ext.seleccion_sha256.eq(sha(r.out/f'seleccion_{year}.json')).all()
        assert all(len(g)==33 for _,g in ext.groupby('procedimiento'))
        if year>2021:assert len(read(r.out/f'seleccion_{year}.json')['metricas_internas'])==29
    count=len(r.budget.data['ajustes']);spent=r.budget.data['consumido']
    resumed=Runner(r.out,p,executor=doble);resumed.run()
    assert len(resumed.budget.data['ajustes'])==count and resumed.budget.data['consumido']==spent
    changed=p.copy();changed.loc[changed.anio==2022,'prom_punt_global']=1e8
    rechaza(lambda:Runner(r.out,changed,executor=doble),AssertionError)
    rr=Runner(run/'externo_alterado',changed,executor=doble);rr.window(ventanas()[1])
    assert read(rr.out/'seleccion_2022.json')['metricas_internas']==read(r.out/'seleccion_2022.json')['metricas_internas']
    import piloto as motor
    selector=motor.seleccionar
    distinct=dict(global_id='ridge_historico_01',especificaciones={g:next(c['id'] for c in candidatos() if c['familia']=='huber' and c['especificacion']==g) for g in GRUPOS})
    motor.seleccionar=lambda *args:distinct
    try:
        separate=Runner(run/'seis_externos',p,executor=doble);separate.window(ventanas()[1])
        assert len(separate.budget.data['ajustes'])==34
        assert len(list((separate.out/'ajustes').glob('e2022_externo*')))==6
        assert read(separate.out/'seleccion_2022.json')['global_id']!=distinct['especificaciones']['historico']
    finally:motor.seleccionar=selector
    tr,te=dividir(p,[2019],2021)
    # Procesos spawn realmente importan clase corrección propia y Pipelines Ridge/Huber.
    worker=Runner(run/'worker_sintetico',p,limit=30)
    for family in ('correccion_comun','ridge','huber'):
        c=next(c for c in candidatos() if c['familia']==family)
        q=worker.predict('worker_'+family,c,tr,te)
        assert len(q)==33 and np.isfinite(q.prediccion).all()
        info=read(worker.out/f'ajustes/worker_{family}/ajuste.json')
        if family=='correccion_comun':assert info['mediana_train']==5
        else:assert info['transformacion_ajustada']['n_samples_seen']==33
    c=candidatos()[4];calls=[]
    def infra(*args):
        calls.append(1)
        if len(calls)==1:raise OSError('infraestructura sintética')
        return doble(*args)
    retry=Runner(run/'reintento',p,executor=infra);retry.fit('doble',c,tr)
    assert len(retry.budget.data['ajustes'])==2
    retry2=Runner(retry.out,p,executor=infra);retry2.fit('doble',c,tr)
    assert len(retry2.budget.data['ajustes'])==2
    def numeric(*args):raise ValueError('numérico sintético')
    fail=Runner(run/'numerico',p,executor=numeric);assert fail.fit('doble',c,tr)[0] is None
    assert Runner(fail.out,p,executor=numeric).fit('doble',c,tr)[0] is None
    assert len(fail.budget.data['ajustes'])==1
    def permanent(*args):raise OSError('infraestructura persistente')
    per=Runner(run/'permanente',p,executor=permanent)
    rechaza(lambda:per.fit('doble',c,tr),OSError)
    rechaza(lambda:Runner(per.out,p,executor=permanent).fit('doble',c,tr),RuntimeError)
    assert len(per.budget.data['ajustes'])==2
    # Rescatar éxito con artefacto faltante, reintentar numérico o cambiar presupuesto es error.
    rechaza(lambda:Runner(r.out,p,executor=doble,limit=7201))
    target=r.out/'ajustes/e2022_i2021_ridge_historico_00/modelo.joblib'
    original=target.read_bytes();target.write_bytes(original+b'alterado')
    rechaza(lambda:Runner(r.out,p,executor=doble),AssertionError)
    target.write_bytes(original)
    target=r.out/'persistencia/e2021_externo_persistencia/predicciones.csv'
    original=target.read_bytes();target.rename(target.with_name('predicciones_ausentes.csv'))
    rechaza(lambda:Runner(r.out,p,executor=doble),AssertionError)
    target.with_name('predicciones_ausentes.csv').rename(target)
    bad=loadcsv(target).iloc[:-1];rechaza(lambda:r.validate_predictions(bad,dividir(p,[2019],2021)[1],candidatos()[0],target.parent.name),AssertionError)
    rechaza(lambda:Runner(ROOT/'experimentos_objetivo3_v3/no_escribir',p,executor=doble))
    rechaza(lambda:guardar(ROOT/'fuera_v4.json',{}))
    depleted=Runner(run/'agotado_sin_intento',p,executor=doble,limit=1)
    depleted.budget.data['consumido']=1;guardar(depleted.budget.path,depleted.budget.data);depleted.checkpoint()
    rechaza(lambda:depleted.fit('sin_saldo',c,tr),TimeoutError)
    assert depleted.budget.data['ajustes']==[]
    # Fallo de convergencia en proceso real: warnings en traceback y estado persistente.
    b=Presupuesto(run/'convergencia_hijo.json',10)
    rechaza(lambda:b.ajustar('hijo',NoConverge(),[[1],[2]],[1,2]),RuntimeError)
    assert len(b.data['ajustes'])==1 and b.data['consumido']>0
    result=dict(aprobado=True,origen='inventados/dobles/worker_sintetico',ruta=str(run.relative_to(ROOT)),ajustes_panel_real=0,consumo_piloto_real=0,ajustes_dobles_completo=count,grupos=['29 candidatos/familias/defaults/cinco matrices/mediana par impar','cinco ventanas/2021 sin fit ni métricas candidatos/280 internos no reutilizados','selecciones anteriores a externos/global distinto de grupo/seis IDs externos','165 externas por cada uno de siete procedimientos/cinco comprobaciones','reanudación verifica contexto/huellas/cobertura/artefactos/intentos/saldo','externo alterado sin afectar selección','spawn importa corrección propia/Pipeline Ridge/Huber/escalador train','inelegible persistente/infraestructura máximo un reintento/advertencia convergencia hijo','caída conservadora/interrupción/límite/terminación real/interfaces congeladas','rutas exteriores/persistencia ausente/modelo alterado/presupuesto ampliado rechazados'],fallos_sinteticos_esperados=True,fuentes_sha256=sources)
    check_hashes(sources)
    guardar(run/'resumen_pruebas.json',result)
    guardar(OUT/'pruebas_sinteticas.json',result)
    print('Orquestación v4 completa aprobada con sintéticos/dobles; cero ajustes del panel real.',flush=True)
if __name__=='__main__':test()
