"""Implementación compartida; protocolo v1.0, sin criterios adaptativos."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'protocolo/fuentes'))
import configuracion as cfg
from controles import verificar, huella
import json, hashlib, platform, subprocess, importlib.metadata, warnings, traceback
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.exceptions import ConvergenceWarning
import joblib
OUT = ROOT / 'fase3/resultados'
KEY = ['codigo_departamento', 'departamento', 'anio']

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False, default=str)+'\n')

def read(name):
    return json.loads((OUT/name).read_text())

def panel():
    verificar()  # no guardar ni sobrescribir evidencia histórica
    return pd.read_csv(ROOT/'auditoria/base_analitica_departamento_anio.csv', dtype={'codigo_departamento':str}).sort_values(['anio','codigo_departamento']).reset_index(drop=True)

def estimator(c):
    cls = {'media':DummyRegressor, 'ols':LinearRegression, 'ridge':Ridge,
           'random_forest':RandomForestRegressor,'gradient_boosting':GradientBoostingRegressor}[c['familia']]
    model = cls(**c['parametros'])
    return make_pipeline(StandardScaler(), model) if c['familia'] in ('ols','ridge') else model

def x(frame,c):
    cols=cfg.ESPECIFICACIONES.get(c['especificacion'], [])
    return frame[cols].to_numpy(dtype=float) if cols else np.zeros((len(frame),1))

def metrics(y,p):
    e=np.asarray(p)-np.asarray(y); denom=np.sum((y-np.mean(y))**2)
    return dict(mae=float(np.mean(abs(e))),rmse=float(np.sqrt(np.mean(e**2))),sesgo=float(np.mean(e)),r2=float(1-np.sum(e**2)/denom) if denom else None)

def fit_predict(c, train, valid, stage):
    model=estimator(c)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        model.fit(x(train,c),train[cfg.RESULTADO].to_numpy())
        pred=model.predict(x(valid,c))
    logs=[{'id':c['id'],'etapa':stage,'tipo':w.category.__name__,'mensaje':str(w.message)} for w in caught]
    if any(issubclass(w.category,ConvergenceWarning) for w in caught):
        raise ValueError('Convergencia no satisfecha: '+str(logs))
    if not np.isfinite(pred).all(): raise ValueError('Predicciones no finitas')
    if ((pred<0)|(pred>500)).any(): logs.append({'id':c['id'],'etapa':stage,'tipo':'fuera_rango','conteo':int(((pred<0)|(pred>500)).sum())})
    rows=valid[KEY].copy();rows['id']=c['id'];rows['observado']=valid[cfg.RESULTADO].to_numpy();rows['prediccion']=pred;rows['error']=pred-rows.observado
    return model,rows,logs

def select(table):
    t=table[table.mae<=table.mae.min()+cfg.TOLERANCIA_PUNTOS]
    t=t[t.rmse<=t.rmse.min()+cfg.TOLERANCIA_PUNTOS]
    return t.sort_values(['n_entradas','orden_familia','orden_id']).iloc[0]['id']

def prepare():
    OUT.mkdir(exist_ok=True,parents=True)
    checked=verificar(); data=panel(); cand=list(cfg.candidatos())
    assert cand==json.loads((ROOT/'protocolo/evidencia/candidatos_congelados.json').read_text())
    assert sys.prefix!=sys.base_prefix, 'Se requiere entorno aislado'
    subprocess.run([sys.executable,'-m','pip','check'],check=True)
    packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
    params={c['id']:estimator(c).get_params(deep=True) for c in cand}
    inputs=dict(checked['insumos_sha256'])
    for p in [ROOT/'protocolo/PROTOCOLO_OBJETIVO_3.md', ROOT/'protocolo/fuentes/configuracion.py',ROOT/'protocolo/evidencia/candidatos_congelados.json',ROOT/'fase3/decisiones.md',Path(__file__)]: inputs[str(p.relative_to(ROOT))]=huella(p)
    info={'commit_partida':'7e95ffe823c3d08f345620c0f9bc65dc72fae7d5','python':platform.python_version(),'ejecutable':sys.executable,'paquetes':packages,'semilla':cfg.SEMILLA,'entradas_sha256':inputs,'controles':checked,'parametros_completos':params,'ajustes_realizados':0,'metodo':'132 desarrollo / 66 reserva; transformaciones dentro del entrenamiento'}
    save('preparacion.json',info)
    lock=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True)
    (ROOT/'fase3/requirements.lock.txt').write_text(lock)
    print('Controles aprobados: 198 filas, 132 desarrollo, 66 reserva, 67 estimadores construidos sin ajustar.')
    return info

def develop():
    prep=read('preparacion.json')
    for name,h in prep['entradas_sha256'].items(): assert huella(ROOT/name)==h
    dev=panel().query('anio <= 2022').copy();assert len(dev)==132
    candidates=list(cfg.candidatos()); allrows=[];summary=[];windows=[];warn=[];fail=[]
    for order,c in enumerate(candidates):
        rows=[]
        for number,(years,year) in enumerate(cfg.VENTANAS,1):
            tr=dev[dev.anio.isin(years)];va=dev[dev.anio==year]
            assert len(tr)==33*len(years) and len(va)==33 and tr.anio.max()<va.anio.min()
            try:
                model,r,w=fit_predict(c,tr,va,f'ventana_{number}');warn+=w;r['ventana']=number; rows.append(r);allrows.append(r)
                if isinstance(model, type(make_pipeline(StandardScaler(), LinearRegression()))):
                    np.testing.assert_allclose(model[0].mean_,x(tr,c).mean(axis=0),atol=1e-12)
                windows.append({'id':c['id'],'ventana':number,**metrics(r.observado,r.prediccion)})
            except Exception:
                fail.append({'id':c['id'],'ventana':number,'traceback':traceback.format_exc(),'parametros':prep['parametros_completos'][c['id']]})
        if len(rows)==3:
            r=pd.concat(rows);summary.append({'id':c['id'],'familia':c['familia'],'especificacion':c['especificacion'],'n_entradas':len(cfg.ESPECIFICACIONES.get(c['especificacion'],[])),'orden_familia':cfg.ORDEN_FAMILIAS.index(c['familia']),'orden_id':order,**metrics(r.observado,r.prediccion)})
    save('fallos.json',fail);save('advertencias_desarrollo.json',warn)
    assert any(s['familia']=='media' for s in summary) and any(s['familia']=='ols' for s in summary)
    table=pd.DataFrame(summary);table.to_csv(OUT/'comparacion_desarrollo.csv',index=False)
    pd.DataFrame(windows).to_csv(OUT/'metricas_ventanas.csv',index=False)
    pd.concat(allrows).to_csv(OUT/'predicciones_desarrollo.csv',index=False)
    winners={s:select(table[(table.especificacion==s)|(table.familia=='media')]) for s in cfg.ESPECIFICACIONES}
    global_id=select(table)
    selected=set(winners.values())|{c['id'] for c in candidates if c['familia'] in ('media','ols')}
    (OUT/'modelos').mkdir(exist_ok=True)
    artifacts={}; transforms={}
    for c in candidates:
        if c['id'] not in selected:continue
        model,r,w=fit_predict(c,dev,dev,'ajuste_final_132');warn+=w
        path=OUT/'modelos'/f"{c['id']}.joblib";joblib.dump(model,path)
        artifacts[str(path.relative_to(ROOT))]=huella(path)
        if c['familia'] in ('ols','ridge'):transforms[c['id']]={'mean':model[0].mean_.tolist(),'scale':model[0].scale_.tolist(),'coef':model[1].coef_.tolist(),'intercept':float(model[1].intercept_)}
    from datetime import datetime,timezone
    save('advertencias_desarrollo.json',warn)
    save('congelacion.json',{'momento_utc':datetime.now(timezone.utc).isoformat(),'ganador_global':global_id,'ganadores_especificacion':winners,'artefactos_sha256':artifacts,'transformaciones':transforms,'parametros_completos':{c['id']:prep['parametros_completos'][c['id']] for c in candidates if c['id'] in selected},'base_sha256':cfg.BASE_SHA256,'entrenamiento_anios':list(cfg.DESARROLLO),'filas':132,'seleccion_sha256':huella(OUT/'comparacion_desarrollo.csv'),'preparacion_sha256':huella(OUT/'preparacion.json'),'predicciones_sha256':huella(OUT/'predicciones_desarrollo.csv'),'reserva_evaluada':False})
    print('Selección exclusivamente desarrollo:',global_id,winners,'; candidatos completos:',len(table),'fallos:',len(fail))
    return table

def evaluate():
    frozen=read('congelacion.json');assert frozen['reserva_evaluada'] is False
    assert huella(OUT/'comparacion_desarrollo.csv')==frozen['seleccion_sha256']
    reserve=panel().query('anio >= 2023').copy();assert len(reserve)==66
    candidates={c['id']:c for c in cfg.candidatos()};rows=[];scores=[]
    for name,h in frozen['artefactos_sha256'].items():
        path=ROOT/name;assert huella(path)==h
        c=candidates[path.stem];model=joblib.load(path)
        p=model.predict(x(reserve,c));assert np.isfinite(p).all()
        r=reserve[KEY].copy();r['id']=c['id'];r['observado']=reserve[cfg.RESULTADO].to_numpy();r['prediccion']=p;r['error']=p-r.observado;rows.append(r)
        for year in (2023,2024,'conjunto'):
            part=r if year=='conjunto' else r[r.anio==year]
            scores.append({'id':c['id'],'periodo':str(year),'n':len(part),**metrics(part.observado,part.prediccion)})
    pd.concat(rows).to_csv(OUT/'predicciones_reevaluacion.csv',index=False)
    table=pd.DataFrame(scores)
    table['delta_mae_media']=table.apply(lambda r:r.mae-table[(table.id=='media')&(table.periodo==r.periodo)].mae.iloc[0],axis=1)
    for spec in cfg.ESPECIFICACIONES:
        table[f'delta_mae_ols_{spec}']=table.apply(lambda r:r.mae-table[(table.id==f'ols_{spec}')&(table.periodo==r.periodo)].mae.iloc[0],axis=1)
    table.to_csv(OUT/'metricas_reevaluacion.csv',index=False)
    save('reevaluacion.json',{'congelacion_sha256':huella(OUT/'congelacion.json'),'ganador_inalterado':frozen['ganador_global'],'entrenamiento_actualizado':False,'prueba_inedita':False,'fuera_rango':int(sum(((r.prediccion<0)|(r.prediccion>500)).sum() for r in rows))})
    print(table[['id','periodo','mae','rmse','sesgo','r2']].to_string(index=False))
    return table
