"""Cotejos de guardados históricos; no evidencia independiente ni fits."""
from auditor import readpanel,equal,error_metrics
from comun import *
import pandas as pd
def historical_frames():
    p=readpanel();frames={}
    for label,path,policy in [('v3','experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv','procedimiento_v3'),('v5','experimentos_objetivo3_v5/etapa2/resultados/predicciones_externas.csv','global'),('recencia','experimentos_temporales_objetivo3_v1/etapa2/resultados/predicciones_externas.csv','global')]:
        df=pd.read_csv(ROOT/path,dtype={'codigo_departamento':str},float_precision='round_trip');df=df[df.procedimiento==policy].copy();df.codigo_departamento=df.codigo_departamento.str.zfill(2)
        if label=='recencia':
            check(df.origen.nunique()==1,'recencia global única')
        df=df.sort_values(['anio','codigo_departamento']).reset_index(drop=True);check(len(df)==165 and not df.duplicated(['anio','codigo_departamento']).any(),'reference165 '+label)
        expected=[float(v) for y in range(2021,2026) for v in p['levels'][y]];prior=[float(v) for y in range(2021,2026) for v in p['levels'][p['prior'][y]]]
        equal(df.observado,expected,'observed ref '+label);equal(df.prediccion,prior,'prediction ref '+label)
        frames[label]=df;frames[label].attrs['path']=path
    for label in ['v5','recencia']:equal(frames[label][['anio','codigo_departamento']],frames['v3'][['anio','codigo_departamento']],'reference keys exact')
    return frames
if __name__=='__main__':
    environment();x=historical_frames();save(HERE/'fase1/REFERENCIAS.json',dict(aprobado=True,n=165,reference='persistencia',paths={k:v.attrs['path'] for k,v in x.items()},same_keys_observed_prediction=True,independent_evidence=False));print('Referencias v3/v5/recencia:165 llaves/observados/predicciones exactos')
