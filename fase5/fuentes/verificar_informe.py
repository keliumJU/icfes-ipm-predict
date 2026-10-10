"""Coherencia numérica/editorial de fase5; no ajustes ni remuestreos."""
import json,re,ast
from pathlib import Path
import pandas as pd
import numpy as np
import nbformat
from verificar_integridad import ROOT,sha,cierre,guardar
from documentar import WIN

def main():
    informe=(ROOT/'informe_objetivo_3.md').read_text()
    encabezados=re.findall(r'^## ([1-8])\. ',informe,re.M)
    assert encabezados==list('12345678')
    assert '{{' not in informe
    assert len(re.findall(r'^\*\*Tabla \d+\.',informe,re.M))==10
    assert len(re.findall(r'^!\[Figura \d+\.',informe,re.M))==4
    for ruta in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',informe):assert (ROOT/ruta).exists()
    def csv(r):return pd.read_csv(ROOT/r,float_precision='round_trip',dtype={'codigo_departamento':str})
    cong=json.loads((ROOT/'fase3/resultados/congelacion.json').read_text());assert cong['ganador_global']==WIN
    for ruta,h in cong['artefactos_sha256'].items():assert sha(ROOT/ruta)==h
    d=csv('fase3/resultados/comparacion_desarrollo.csv');m=csv('fase3/resultados/metricas_reevaluacion.csv');t=csv('fase4/resultados/metricas_agrupadas.csv')
    def cerca(v,ref):assert abs(float(v)-ref)<.0000006,(v,ref)
    # Las cifras narrativas se validan contra fuentes; no reglas de reselección.
    cerca(d.set_index('id').loc[WIN,'mae'],6.332499)
    cerca(d.set_index('id').loc['gradient_boosting_tasas_07','mae']-d.set_index('id').loc[WIN,'mae'],.108025)
    for year,mae,bias in [('2023',5.020614,-1.756802),('2024',7.670549,-3.801227),('conjunto',6.345582,-2.779014)]:
        row=m[(m.id==WIN)&(m.periodo.astype(str)==year)].iloc[0];cerca(row.mae,mae);cerca(row.sesgo,bias)
    for year,delta in [('2023',.128946),('2024',.302844),('conjunto',.215895)]:
        z=m[m.periodo.astype(str)==year].set_index('id')
        cerca(z.loc['gradient_boosting_ipm_02','mae']-z.loc['ols_ipm','mae'],delta)
        assert z.loc['ols_ipm','mae']<z.loc['gradient_boosting_ipm_02','mae']
    z=m[m.periodo.astype(str)=='conjunto'].set_index('id')
    assert z.loc['gradient_boosting_ipm_02','rmse']<z.loc['ols_ipm','rmse']
    cerca(t.set_index('id').loc[WIN,'mae']-t.set_index('id').loc['gradient_boosting_tasas_07','mae'],.241788)
    b=csv('fase4/resultados/bootstrap_resumen.csv');row=b[(b.a=='gradient_boosting_tasas_07')&(b.b==WIN)].iloc[0]
    cerca(row.percentil_2_5,-.569529);cerca(row.percentil_97_5,.045591);assert row.percentil_2_5<0<row.percentil_97_5
    assert b.replicas.sum()==14000
    inf=csv('fase4/resultados/influencia_grupos_errores.csv');inf=inf[inf.id==WIN]
    cerca(inf.mae.min(),7.500620);cerca(inf.mae.max(),8.251786)
    sup=csv('fase4/resultados/soporte_territorial.csv');assert len(sup)==4224 and sup.fuera_rango.sum()==126
    col=csv('fase4/resultados/colinealidad.csv').set_index('especificacion')
    for k,v in [('ipm',1),('tasas',12.644109),('ambas',30.647008)]:cerca(col.loc[k,'numero_condicion'],v)
    mt=csv('fase4/resultados/metricas_territorio.csv');mt=mt[mt.id==WIN].set_index('departamento')
    cerca(mt.loc['Choco','mae'],26.213950);cerca(mt.loc['San Andres','mae'],22.595519)
    assert mt.loc['Choco','sesgo']>0 and mt.loc['San Andres','sesgo']<0
    sizes=csv('fase4/resultados/diagnostico_tamanos.csv');assert (sizes.min_n==190).all() and (sizes.max_n==79542).all()
    assoc=csv('fase4/resultados/asociaciones_longitudinales.csv').set_index('variable')
    for k,refs in [('ipm',[-.764626,.116285,-.136136]),('Rezago escolar',[-.773640,.339428,-.001334])]:
        for name,v in zip(['r_entre_territorios','r_dentro_territorio','r_doble_centrado'],refs):cerca(assoc.loc[k,name],v)
    cf=csv('fase4/resultados/coeficientes_ols_congelados.csv'); cf=cf[cf.variable=='ipm'].set_index('id')
    cerca(cf.loc['ols_ipm','coef_por_sd_entrenamiento'],-12.028504);cerca(cf.loc['ols_ambas','coef_por_sd_entrenamiento'],-10.314072)
    pairs=csv('fase4/resultados/pares_correlacion.csv');r=pairs[(pairs.a=='Inadecuada eliminacion de excretas')&(pairs.b=='Sin acceso a fuente de agua mejorada')].iloc[0];cerca(r.r,.864463)
    gen=json.loads((ROOT/'fase5/resultados/generacion.json').read_text());assert len(gen['comprobaciones_metricas'])==91
    for p,h in gen['fuentes_sha256'].items():assert sha(ROOT/p)==h
    nb=nbformat.read(ROOT/'fase5/notebooks/07_informe_tesis.ipynb',as_version=4);nbformat.validate(nb)
    for c in nb.cells:
        if c.cell_type=='code':assert c.execution_count is not None and all(o.output_type!='error' for o in c.outputs)
    for p in (ROOT/'fase5/fuentes').glob('*.py'):
        if p.name!='07_informe_tesis.py':ast.parse(p.read_text())
    # Coordenadas completas de figuras: no truncar datos por límites de ejes.
    for ruta in ['fase3/resultados/predicciones_desarrollo.csv','fase3/resultados/predicciones_reevaluacion.csv','fase4/resultados/predicciones_territoriales.csv']:
        p=csv(ruta);p=p[p.id==WIN];assert p[['observado','prediccion']].min().min()>=180 and p[['observado','prediccion']].max().max()<=300
    assert mt.mae.max()<30
    cierre()
    guardar('verificacion_informe.json',{'aprobado':True,'secciones':8,'tablas':10,'figuras_png':4,'figuras_svg':4,'filas_metricas_contrastadas':91,'cifras_narrativas_contrastadas':True,'notebook_validado':True,'sin_ajustes_nuevos':True,'sin_simulacion':True,'huellas_artefactos_congelados_coinciden':True,'revision_visual':'Cuatro figuras inspeccionadas; solapamientos de leyenda/pie corregidos; sin truncar coordenadas','limites':'No segunda reproducción de entrenamiento ni nueva lectura PDF; verificaciones documentales y aritméticas'})
    print('Coherencia de informe y conservación aprobadas')
if __name__=='__main__':main()
