"""Verificaciones independientes de resultados y conservación; sin búsqueda nueva."""
import analisis as a
import numpy as np
import pandas as pd
import nbformat
import itertools
from pathlib import Path
checks={}
prep=a.load('preparacion.json')
for p,h in prep['snapshot_previo'].items():
    if p=='CONTINUIDAD_OBJETIVO_3.md': continue
    assert a.m.huella(a.ROOT/p)==h,p
checks['archivos_previos_intactos_excepto_continuidad']=len(prep['snapshot_previo'])-1
r=a.readcsv(a.OUT/'predicciones_territoriales.csv')
assert len(r)==396 and not r.duplicated(['id','codigo_departamento','anio']).any()
assert set(r.anio)==set(a.m.cfg.DESARROLLO) and r.groupby('id').size().eq(132).all()
assert r.groupby(['id','codigo_departamento']).size().eq(4).all()
np.testing.assert_allclose(r.prediccion-r.observado,r.error,atol=1e-12,rtol=0)
np.testing.assert_allclose(abs(r.error),r.error_absoluto,atol=1e-12,rtol=0)
np.testing.assert_allclose(r.error**2,r.error_cuadrado,atol=1e-12,rtol=0)
checks['cobertura_y_errores']=True
# Recalcular sin llamar métricas compartidas; RMSE sobre cuadrados concatenados.
for name,cols in [('metricas_agrupadas.csv',['id']),('metricas_territorio.csv',['id','codigo_departamento']),('metricas_anio.csv',['id','anio'])]:
    scores=a.readcsv(a.OUT/name)
    for _,row in scores.iterrows():
        g=r
        for col in cols:g=g[g[col]==row[col]]
        e=g.prediccion.to_numpy()-g.observado.to_numpy(); y=g.observado.to_numpy();d=((y-y.mean())**2).sum()
        calc=[abs(e).sum()/len(e),np.sqrt((e*e).sum()/len(e)),e.sum()/len(e),1-(e*e).sum()/d if d else np.nan]
        np.testing.assert_allclose(calc,row[['mae','rmse','sesgo','r2']].to_numpy(dtype=float),atol=1e-12,rtol=1e-12,equal_nan=True)
checks['metricas_independientes']=True
splits=a.load('particiones.json'); assert len(splits)==99
for s in splits:
    assert len(s['territorios_entrenamiento'])==32 and s['excluido'] not in s['territorios_entrenamiento']
    assert s['n_entrenamiento']==128 and s['n_evaluacion']==4
checks['particiones_completas']=True
# Comprobación focal de tres ajustes, primer código fijo; no entrenamiento reservado.
dev=a.m.panel().query('anio<=2022');code=sorted(dev.codigo_departamento.unique())[0]
for c in a.m.cfg.candidatos():
    if c['id'] not in a.m.read('congelacion.json')['ganadores_especificacion'].values():continue
    _,pred,w=a.m.fit_predict(c,dev[dev.codigo_departamento!=code],dev[dev.codigo_departamento==code],'verificacion_fase4')
    expected=r[(r.id==c['id'])&(r.codigo_departamento==code)].sort_values('anio')
    np.testing.assert_allclose(pred.sort_values('anio').prediccion,expected.prediccion,atol=1e-12,rtol=0)
checks['tres_ajustes_focales_reproducidos']=True
reps=a.readcsv(a.OUT/'bootstrap_replicas.csv'); summary=a.readcsv(a.OUT/'bootstrap_resumen.csv')
assert len(reps)==14000 and len(summary)==7
for _,row in summary.iterrows():
    source=r if row.contexto=='territorial_desarrollo' else a.readcsv(a.ROOT/'fase3/resultados/predicciones_reevaluacion.csv')
    groups={}
    for ident in (row.a,row.b):
        sub=source[source.id==ident];groups[ident]=sub.assign(e=abs(sub.prediccion-sub.observado)).groupby('codigo_departamento').e.mean().sort_index().to_numpy()
    dif=groups[row.a]-groups[row.b];rng=np.random.default_rng(a.m.cfg.SEMILLA)
    expected=np.array([dif[rng.integers(0,33,33)].mean() for _ in range(2000)])
    actual=reps[(reps.contexto==row.contexto)&(reps.a==row.a)&(reps.b==row.b)].sort_values('replica').delta_mae
    np.testing.assert_allclose(actual,expected,atol=1e-12,rtol=0)
    np.testing.assert_allclose([row.delta_mae,row.percentil_2_5,row.percentil_97_5],[dif.mean(),*np.quantile(expected,[.025,.975])],atol=1e-12,rtol=0)
checks['bootstrap_14000_replicas_verificadas']=True
assoc=a.readcsv(a.OUT/'asociaciones_longitudinales.csv')
for _,row in assoc.iterrows():
    columns=[row.variable,a.m.cfg.RESULTADO];matrix=dev[columns].to_numpy()
    means=dev.groupby('codigo_departamento')[columns].mean().to_numpy()
    within=matrix-dev.groupby('codigo_departamento')[columns].transform('mean').to_numpy()
    double=within-dev.groupby('anio')[columns].transform('mean').to_numpy()+matrix.mean(axis=0)
    np.testing.assert_allclose([np.corrcoef(z.T)[0,1] for z in (means,within,double)],row[['r_entre_territorios','r_dentro_territorio','r_doble_centrado']].to_numpy(dtype=float),atol=1e-12)
checks['asociaciones_verificadas']=True
for stage in ('05_contraste_territorial','06_robustez_explicaciones'):
    nb=nbformat.read(a.ROOT/'notebooks'/f'{stage}.ipynb',as_version=4);nbformat.validate(nb)
    for cell in nb.cells:
        if cell.cell_type=='code':
            assert cell.execution_count is not None
            assert not any(o.output_type=='error' for o in cell.outputs)
checks['notebooks_ejecutados_validados']=True
assert a.load('fallos.json')==[]
checks['ganador_global_inalterado']=a.m.read('congelacion.json')['ganador_global']
a.save('verificacion.json',checks)
print(checks)
