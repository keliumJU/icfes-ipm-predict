"""Tablas de diagnóstico y contexto calculadas desde resultados actuales."""
from pathlib import Path
import pandas as pd,numpy as np,json
from modelos import panel,OUT,HERE,metrics

def run():
    d=panel();p=pd.read_csv(OUT/'predicciones.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    q=p.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global"').copy();q['error']=q.predicted-q.observed
    rows=[]
    for (code,spec),a in q.groupby(['codigo_departamento','spec']):rows.append(dict(codigo_departamento=code,departamento=d[d.codigo_departamento==code].departamento.iloc[0],spec=spec,**metrics(a.observed,a.predicted)))
    pd.DataFrame(rows).to_csv(OUT/'residuos_departamentales.csv',index=False)
    changes=d.sort_values(['codigo_departamento','anio']).copy();changes['ipm_previo']=changes.groupby('codigo_departamento').ipm.shift();changes['anio_previo']=changes.groupby('codigo_departamento').anio.shift();changes['reduccion_observada_pp']=changes.ipm_previo-changes.ipm
    changes=changes[changes.anio_previo.notna()]
    changes[['codigo_departamento','departamento','anio_previo','anio','ipm_previo','ipm','reduccion_observada_pp']].to_csv(OUT/'variaciones_ipm_observadas.csv',index=False)
    # No todas son diferencias de un año: se señala intervalo 2019–2021.
    a=changes[changes.anio-changes.anio_previo==1]
    support=pd.read_csv(OUT/'escenarios.csv');reasons=support[~support.admitido].motivos.fillna('').str.split('|').explode().value_counts().to_dict()
    mathpred=p[p.target=='mat34'];extreme=mathpred[~mathpred.predicted.between(0,100)]
    r=dict(variacion_anual_reduccion_pp=a.reduccion_observada_pp.describe().to_dict(),fraccion_descensos_1_3_5={str(v):float(a.reduccion_observada_pp.ge(v).mean()) for v in [1,3,5]},motivos_rechazos=reasons,matematicas_predicciones_fuera_0_100=len(extreme),intervalo2019_2021_no_anual=True)
    (OUT/'DIAGNOSTICOS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2));return r
if __name__=='__main__':run()
