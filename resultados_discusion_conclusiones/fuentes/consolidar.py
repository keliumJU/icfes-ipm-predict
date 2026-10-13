"""Consolidación de salidas existentes; cero modelos o escenarios nuevos."""
from pathlib import Path
import json,hashlib,time
import pandas as pd,numpy as np
H=Path(__file__).resolve().parents[1];R=H.parent;O=R/'objetivo4_validacion_escenarios/resultados';E=H/'evidencia'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 t=time.monotonic();paths=[O/'escenarios.csv',O/'metricas.csv',O/'predicciones.csv',O/'DISPERSION.json',R/'auditoria/evidencia/resumen_tesis.json',R/'auditoria/evidencia/actualizacion_20261008/tabla12_propuesta_198.csv',R/'entrega_objetivos3_4_final/objetivo3/tablas/metricas_comparables.csv']
 s=pd.read_csv(paths[0],dtype={'codigo_departamento':str},float_precision='round_trip');m=pd.read_csv(paths[1],dtype={'anio':str},float_precision='round_trip');p=pd.read_csv(paths[2],dtype={'codigo_departamento':str},float_precision='round_trip')
 assert len(s)==165 and s.groupby('escenario').size().eq(33).all()
 a=s[s.admitido & s.reduccion_pp.gt(0)].copy();assert len(a)==3 and set(a.departamento)=={'Meta','Sucre','Tolima'}
 assert s[~s.admitido].prediccion_escenario.isna().all()
 q=s.groupby('escenario').agg(propuestos=('admitido','size'),admitidos=('admitido','sum'));q['rechazados']=q.propuestos-q.admitidos;q['cambios_efectivos_admitidos']=a.groupby('escenario').size().reindex(q.index,fill_value=0);q.to_csv(E/'resumen_escenarios.csv');a.to_csv(E/'escenarios_efectivos.csv',index=False)
 for r in m.itertuples():
  z=p[(p.exercise==r.exercise)&(p.method==r.method)&(p.target==r.target)&(p.spec==r.spec)]
  if r.anio!='conjunto':z=z[z.anio==int(r.anio)]
  assert len(z)==r.n
  np.testing.assert_allclose(abs(z.observed-z.predicted).mean(),r.MAE,atol=1e-10)
 main=m.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global" and anio=="conjunto"');main.to_csv(E/'metricas_principales.csv',index=False)
 historical=json.loads(paths[3+1].read_text());assoc=pd.read_csv(paths[5]);assert abs(assoc.loc[assoc.variable.eq('ipm'),'r_198_celdas'].iloc[0]-historical['r_ipm_global_198'])<1e-12
 final={'fuentes_sha256':{str(x.relative_to(R)):sha(x) for x in paths},'escenarios_13_admitidos':int(s.admitido.sum()),'efectivos':len(a),'escenarios_no_predichos':int((~s.admitido).sum()),'nuevos_ajustes':0,'nuevos_escenarios':0,'verificacion_metricas':True,'fuente_asociacion':'auditoria/evidencia/actualizacion_20261008/tabla12_propuesta_198.csv','periodo_asociacion':'2018–2024 sin2020','segundos':time.monotonic()-t}
 assert final['segundos']<120
 (E/'CONTROL_CONSOLIDACION.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n');print(q.to_string());print('Bases admitidas:',', '.join(s[s.admitido & s.escenario.eq('sin_cambio')].departamento));print(a[['departamento','ipm_base','ipm_escenario','prediccion_base','prediccion_escenario','diferencia']].to_string(index=False));print(final)
if __name__=='__main__':run()
