# %% [markdown]
# Resultados guardados del piloto36 v5
# Exploratorio: 2021–2025 ya examinados. Sin ajustes, simulación ni interpretación causal.
# %%
from pathlib import Path
import sys,json
root=Path.cwd()
if not (root/'experimentos_objetivo3_v5').exists():
    root=next(p for p in root.parents if (p/'experimentos_objetivo3_v5').exists())
sys.path.insert(0,str(root/'experimentos_objetivo3_v5/etapa2/fuentes'))
from piloto import read,OUT,loadcsv,sha
from verificar import independent
v=read(OUT/'verificacion.json');assert v['aprobado'] and v['completo']
print(json.dumps({k:v[k] for k in ['internos_documentados','ajustes_documentados','intentos_ledger','segundos_ajustes','externas_por_procedimiento','cinco_repeticiones']},ensure_ascii=False,indent=2))
# %% [markdown]
# Comparación exacta global y métricas de los siete procedimientos
# %%
import pandas as pd
m=loadcsv(OUT/'metricas.csv')
print(m[m.periodo=='2021–2025'].to_string(index=False))
p=loadcsv(OUT/'predicciones_externas.csv');q=p[p.procedimiento=='global']
meta=read(OUT/'meta.json');assert independent(q.observado,q.prediccion)['mae']==meta['mae_v5']
print(json.dumps(meta,ensure_ascii=False,indent=2))
# %% [markdown]
# Selecciones, años y deterioros conservados
# %%
print(loadcsv(OUT/'ganadores.csv').to_string(index=False))
print(m[(m.procedimiento=='global') & m.periodo.isin([str(y) for y in range(2021,2026)])].to_string(index=False))
d=loadcsv(OUT/'deterioros.csv')
print('Pares con deterioro MAE frente persistencia:',len(d),'de 165')
print(d.to_string(index=False))
print('Casos completos; Guainía238 frente404/21.012106 puntos; IPM hogares vs alumnos; colegio vs residencia; enlace ecológico; pocos años y dependencia territorial/temporal. Procedencia local sin autenticación independiente. No confirmación independiente ni causalidad.')
