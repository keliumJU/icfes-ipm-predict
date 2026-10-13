"""Rutas manuales sin ejecutar runners cerrados ni escribir en entregas previas.

Entrenar solo cuando el lector invoque estas funciones. No se invocan en esta entrega.
Se reutilizan constructores y criterios originales en lugar de duplicar modelos.
"""
from contextlib import contextmanager
from pathlib import Path
import importlib.util, sys, time, json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
@contextmanager
def module_at(folder,name):
    old_path=list(sys.path);saved={k:sys.modules.get(k) for k in ['comun','configuracion','controles',name]}
    for k in saved:sys.modules.pop(k,None)
    sys.path.insert(0,str(folder));spec=importlib.util.spec_from_file_location(name,folder/(name+'.py'))
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    try:yield m
    finally:
        sys.path[:]=old_path
        for k,v in saved.items():
            if v is None:sys.modules.pop(k,None)
            else:sys.modules[k]=v
def base_manual(limit_seconds=600):
    """Reproduce 67 candidatos/selección base; devuelve resultados en memoria."""
    start=time.monotonic()
    with module_at(ROOT/'fase3/fuentes','comun') as m:
        d=pd.read_csv(ROOT/'auditoria/base_analitica_departamento_anio.csv',dtype={'codigo_departamento':str})
        rows=[];cands=list(m.cfg.candidatos())
        for order,c in enumerate(cands):
            parts=[]
            for i,(ys,y) in enumerate(m.cfg.VENTANAS):
                if time.monotonic()-start>limit_seconds:raise TimeoutError('Reproducción incompleta; no afirmar cierre')
                _,r,_=m.fit_predict(c,d[d.anio.isin(ys)],d[d.anio==y],str(i));parts.append(r)
            r=pd.concat(parts);rows.append(dict(id=c['id'],n_entradas=len(m.cfg.ESPECIFICACIONES.get(c['especificacion'],[])),orden_familia=m.cfg.ORDEN_FAMILIAS.index(c['familia']),orden_id=order,**m.metrics(r.observado,r.prediccion)))
        table=pd.DataFrame(rows);winner=m.select(table)
        c=next(c for c in cands if c['id']==winner)
        _,pred,_=m.fit_predict(c,d[d.anio<=2022],d[d.anio>=2023],'reserva_reproduccion')
        return table,winner,pred
def dinamica_manual(limit_seconds=900):
    """Reproduce selección V6; sin ledger anterior, sin archivos, sin reselección externa."""
    start=time.monotonic();folder=ROOT/'experimento_final_objetivo3_v6/ejecucion_autorizada'
    with module_at(folder,'motor') as m:
        p=m.panel();cands=m.load(folder/'ESPECIFICACION_V6.json')['candidates'];predictions=[];decisions=[]
        for y in range(2021,2026):
            if time.monotonic()-start>limit_seconds:raise TimeoutError('Reproducción incompleta; no afirmar cierre')
            records=[]
            if y>2021:
                for c in cands:
                    observed=[];pred=[]
                    for z in range(2021,y):
                        if time.monotonic()-start>limit_seconds:raise TimeoutError('Reproducción incompleta')
                        out=m.estimate(c,m.context(p,c,z));observed.extend(p['levels'][z]);pred.extend(out['prediction'])
                    records.append(dict(id=c['id'],inputs=c['inputs'],order=c['order'],**m.metrics(pred,observed)))
                winner=m.select(records)['winner']
            else:winner='persistencia'
            decisions.append(dict(year=y,selected=winner));c=next(c for c in cands if c['id']==winner)
            out=m.estimate(c,m.context(p,c,y))
            for code,obs,pr in zip(p['codes'],p['levels'][y],out['prediction']):predictions.append(dict(code=code,year=y,observed=obs,predicted=pr))
        return pd.DataFrame(decisions),pd.DataFrame(predictions)

def pobreza_ampliada_manual(limit_seconds=1800):
    """Ruta manual del selector de pobreza V2; mismos constructores/ventanas/criterios."""
    start=time.monotonic();folder=ROOT/'experimentos_objetivo3_v2/fase2/fuentes'
    with module_at(folder,'comun') as m:
        cfg=m.cfg;d=pd.read_csv(cfg.BASE,dtype={'codigo_departamento':str},float_precision='round_trip')
        candidates=cfg.candidatos();decisions=[];predictions=[]
        def predict(c,train,test):
            if time.monotonic()-start>limit_seconds:raise TimeoutError('Reproducción incompleta; no continuar ni sintetizar')
            cols=cfg.ESPECIFICACIONES.get(c['especificacion'],[])
            x=lambda t:t[cols].to_numpy(float) if cols else np.zeros((len(t),1))
            model=cfg.construir(c);model.fit(x(train),train[cfg.RESULTADO].to_numpy())
            return model.predict(x(test))
        for w in cfg.ventanas():
            scores=[];expected=[v['validacion'] for v in w['internas']]
            for order,c in enumerate(candidates):
                obs=[];pr=[]
                for v in w['internas']:
                    tr,te=m.dividir(d,v['entrenamiento'],v['validacion']);obs.extend(te[cfg.RESULTADO]);pr.extend(predict(c,tr,te))
                scores.append(dict(id=c['id'],familia=c['familia'],n_predictores=len(cfg.ESPECIFICACIONES.get(c['especificacion'],[])),orden=order,estado='completo',ventanas=expected,**m.metricas(obs,pr)))
            winner=m.seleccionar(scores,expected);year=w['externo'];decisions.append(dict(year=year,selected=winner))
            tr,te=m.dividir(d,w['entrenamiento'],year);c=next(c for c in candidates if c['id']==winner);pr=predict(c,tr,te)
            for code,obs,pred in zip(te.codigo_departamento,te[cfg.RESULTADO],pr):predictions.append(dict(code=code,year=year,observed=obs,predicted=pred))
        return pd.DataFrame(decisions),pd.DataFrame(predictions)
