"""Cotejo íntegro de fuente/derivado/referencias por bloques; no runners históricos."""
from comun import *
import pandas as pd
import numpy as np

def read(path):
    a=pd.concat(list(pd.read_csv(ROOT/path,dtype={'codigo_departamento':'string'},float_precision='round_trip',chunksize=1024)),ignore_index=True)
    a.codigo_departamento=a.codigo_departamento.str.zfill(2)
    return a
def validated_panel():
    spec=load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')
    assert [window(y) for y in YEARS[2:]]==spec['ventanas']
    paths=list(spec['fuentes'])
    for path in paths: assert digest(ROOT/path)==spec['fuentes'][path]['esperado']
    s,p=(read(path).sort_values(['codigo_departamento','anio']).reset_index(drop=True) for path in paths)
    keys=['codigo_departamento','anio']
    pd.testing.assert_frame_equal(s,p[list(s.columns)],check_exact=True)
    assert not s.duplicated(keys).any() and not s[keys].isna().any().any()
    assert len(s)==231 and tuple(sorted(s.codigo_departamento.unique()))==CODES
    assert set(map(tuple,s[keys].to_numpy()))=={(c,y) for c in CODES for y in YEARS}
    g=s.groupby('codigo_departamento',sort=False)
    expected={'anio_previo':g.anio.shift(1),'puntaje_previo':g.prom_punt_global.shift(1),
              'cambio_observado':s.prom_punt_global-g.prom_punt_global.shift(1),'intervalo':s.anio-g.anio.shift(1),
              'fuente_sha256':pd.Series([spec['fuentes'][paths[0]]['esperado']]*len(s))}
    for col in p.columns:
        if col.startswith('previo_'): expected[col]=g[col.removeprefix('previo_')].shift(1)
        elif col.startswith('cambio_') and col!='cambio_observado':
            cov=col.removeprefix('cambio_'); expected[col]=s[cov]-g[cov].shift(1)
    assert set(p.columns)==set(s.columns)|set(expected)
    for col,v in expected.items(): pd.testing.assert_series_equal(p[col],v,check_exact=True,check_names=False,check_dtype=False)
    external=p[p.anio.between(2021,2025)].reset_index(drop=True)
    refs=[]
    for path,policy in [('experimentos_objetivo3_v5/etapa2/resultados/predicciones_externas.csv','global'),
            ('experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv','persistencia'),
            ('experimentos_temporales_objetivo3_v1/etapa2/resultados/predicciones_externas.csv','global')]:
        full=read(path); q=full[full.procedimiento==policy].sort_values(keys).reset_index(drop=True)
        assert len(q)==165 and not q.duplicated(keys).any()
        pd.testing.assert_frame_equal(q[keys],external[keys],check_exact=True)
        for col,other in [('observado','prom_punt_global'),('prediccion','puntaje_previo'),('puntaje_previo','puntaje_previo'),('anio_previo','anio_previo')]:
            pd.testing.assert_series_equal(q[col],external[other],check_exact=True,check_dtype=False,check_names=False)
        assert q.cambio_predicho.eq(0).all()
        refs.append({'archivo':path,'procedimiento':policy,'filas':len(full),'pares':165,'sha256':digest(ROOT/path),'exacto':True})
    levels=levels_from_rows(s[['codigo_departamento','anio','prom_punt_global']].to_dict('records'))
    assert set(levels)==set(YEARS)
    return levels,{'aprobado':True,'procedimiento':'Bloques1024/round_trip, todas columnas por shift reconstruidas exactas en memoria; referencias165llaves/observados/previos/predicciones exactos',
            'filas':231,'cambios':198,'territorios':33,'referencias':refs,'fuentes':{path:digest(ROOT/path) for path in paths},'fits':0}
if __name__=='__main__':
    assert load(HERE/'ENTORNO_FASE3.json')['aprobado']
    levels,proof=validated_panel(); fresh('SEMANTICA_FASE3.json',proof); print(json.dumps(proof))
