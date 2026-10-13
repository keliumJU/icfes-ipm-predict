"""Cotejo completo por bloques de archivos guardados; no ajuste ni evaluación nueva.
Requiere preflight y entorno aprobados. No importa fuentes históricas.
"""
from pathlib import Path
import json
import os
import sys
import hashlib
import csv

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
def write(p,d):
    (OUT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def main():
    assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
    assert sys.version.split()[0]=='3.12.14'
    assert json.loads((OUT/'ENTORNO_FASE1.json').read_text())['aprobado']
    assert json.loads((OUT/'PREFLIGHT_FASE1.json').read_text())['aprobado']
    import pandas as pd
    import numpy as np
    seed=20261010  # Contrato; no operación aleatoria.
    def read(p):
        result=pd.concat(list(pd.read_csv(ROOT/p,dtype={'codigo_departamento':'string'},float_precision='round_trip',chunksize=1024)),ignore_index=True)
        result.codigo_departamento=result.codigo_departamento.str.zfill(2)
        return result
    source_path='experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
    panel_path='experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv'
    s,p=read(source_path),read(panel_path)
    keys=['codigo_departamento','anio']
    s=s.sort_values(keys).reset_index(drop=True); p=p.sort_values(keys).reset_index(drop=True)
    pd.testing.assert_frame_equal(s,p[list(s.columns)],check_exact=True)
    assert not s.duplicated(keys).any() and not s[keys].isna().any().any()
    years=[2018,2019,2021,2022,2023,2024,2025]
    codes=sorted(s.codigo_departamento.unique().tolist())
    assert len(codes)==33 and len(p)==231 and set(s.anio)==set(years)
    assert set(map(tuple,s[keys].to_numpy()))=={(c,y) for c in codes for y in years}
    g=s.groupby('codigo_departamento',sort=False)
    previous=g.anio.shift(1)
    prior_score=g.prom_punt_global.shift(1)
    expected={'anio_previo':previous,'puntaje_previo':prior_score,'cambio_observado':s.prom_punt_global-prior_score,'intervalo':s.anio-previous,'fuente_sha256':pd.Series(['6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3']*len(s))}
    for col in p.columns:
        if col.startswith('previo_'):
            cov=col.removeprefix('previo_'); expected[col]=g[cov].shift(1)
        elif col.startswith('cambio_') and col!='cambio_observado':
            cov=col.removeprefix('cambio_'); expected[col]=s[cov]-g[cov].shift(1)
    assert set(p.columns)==set(s.columns)|set(expected)
    for col,v in expected.items():
        pd.testing.assert_series_equal(p[col],v,check_exact=True,check_names=False,check_dtype=False)
    assert p[p.anio==2018].cambio_observado.isna().all()
    assert p[p.anio>2018].cambio_observado.notna().all()
    assert np.isfinite(p[p.anio>2018][['puntaje_previo','cambio_observado']].to_numpy(float)).all()
    assert p[p.anio==2021].anio_previo.eq(2019).all() and p[p.anio==2021].intervalo.eq(2).all()
    refs=[('experimentos_objetivo3_v5/etapa2/resultados/predicciones_externas.csv','global'),('experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv','persistencia'),('experimentos_temporales_objetivo3_v1/etapa2/resultados/predicciones_externas.csv','global')]
    reference_records=[]
    expected_external=p[p.anio.between(2021,2025)].sort_values(keys).reset_index(drop=True)
    refcols=keys+['observado','prediccion','cambio_predicho','puntaje_previo','anio_previo']
    first=None
    for path,role in refs:
        full=read(path); q=full[full.procedimiento==role].sort_values(keys).reset_index(drop=True)
        assert len(q)==165 and not q.duplicated(keys).any()
        pd.testing.assert_frame_equal(q[keys],expected_external[keys],check_exact=True)
        for col,pc in [('observado','prom_punt_global'),('prediccion','puntaje_previo'),('puntaje_previo','puntaje_previo'),('anio_previo','anio_previo')]:
            pd.testing.assert_series_equal(q[col],expected_external[pc],check_exact=True,check_dtype=False,check_names=False)
        assert q.cambio_predicho.eq(0).all()
        if first is None: first=q[refcols]
        else: pd.testing.assert_frame_equal(first,q[refcols],check_exact=True,check_dtype=False)
        reference_records.append({'archivo':path,'procedimiento':role,'filas_archivo_leidas':len(full),'pares':len(q),'llaves_observados_prediccion_exactos':True,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()})
    conf=json.loads((ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json').read_text())
    trace=[]
    def add(role,ext,target,train):
        supervised=[y for y in train if y!=2019]
        lags=[years[years.index(y)-1] for y in supervised]
        lag=years[years.index(target)-1]
        trace.append({'tipo':role,'externo':ext,'evaluado':target,'historia_cambios':';'.join(map(str,train)),'respuestas_supervisadas':';'.join(map(str,supervised)),'rezagos_respuestas':';'.join(map(str,lags)),'anios_pares_completos':len(supervised),'filas_memoria_correccion':33*len(supervised),'filas_comun':len(supervised),'rezago_entrada_evaluada':lag,'intervalo_objetivo':target-lag,'politica':'persistencia_fija' if role=='externa' and target==2021 else ('respaldo_cero_pares' if not supervised else 'ajuste_futuro_permitido'),'semantica':'documental_sin_fit'})
    for w in conf['ventanas']:
        add('externa',w['externo'],w['externo'],w['entrenamiento'])
        for i in w['internas']: add('interna',w['externo'],i['validacion'],i['entrenamiento'])
    with (OUT/'TRAZABILIDAD_TEMPORAL.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(trace[0])); writer.writeheader();writer.writerows(trace)
    write('SEMANTICA_FASE1.json',{'aprobado':True,'procedimiento':'Lectura completa por bloques1024, float_precision=round_trip; unión exacta33×7; reconstrucción en memoria de TODOS campos v5 por shift dentro territorio; igualdad exacta sin tolerancia; sin guardar reconstrucción ni estadísticos de resultados nuevos.','fuente':source_path,'derivado':panel_path,'filas':len(p),'territorios':codes,'anios':years,'cambios':198,'pares_supervisados_disponibles':[2021,2022,2023,2024,2025],'2019':'historial, no respuesta supervisada; falta cambio anterior en2018','externas':165,'referencias':reference_records,'trazabilidad_filas':len(trace),'particiones_fuente':'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json:ventanas','semilla':seed,'fits':0,'metricas_nuevas':0})
    print(json.dumps({'aprobado':True,'filas':231,'territorios':33,'cambios':198,'referencias_exactas':3,'trazabilidad_filas':len(trace),'fits':0}))

if __name__=='__main__': main()
