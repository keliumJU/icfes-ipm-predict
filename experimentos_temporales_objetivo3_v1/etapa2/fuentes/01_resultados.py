# %%
"""Resultados auditados del piloto recencia_h2; no ejecuta ajustes."""
from pathlib import Path
import json
import pandas as pd
ROOT = Path('/home/kelium/Documents/espcarlos/icfes-predict-improved')
OUT = ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados'
meta=json.loads((OUT/'meta.json').read_text())
assert json.loads((OUT/'auditoria_independiente.json').read_text())['aprobado']
print('Exploratorio: todos2021–2025 vistos; sin causalidad/confirmación independiente')
print(json.dumps(meta,ensure_ascii=False,indent=2))
# %%
metricas=pd.read_csv(OUT/'tablas/metricas_externas.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
print(metricas[metricas.corte=='global'][['procedimiento','n','mae','rmse','sesgo','delta_mae']].to_string(index=False))
# %%
selecciones=pd.read_csv(OUT/'tablas/selecciones.csv')
print(selecciones.to_string(index=False))
# %%
registros=pd.read_csv(OUT/'tablas/registros_144.csv',float_precision='round_trip')
assert len(registros)==144 and registros.id.nunique()==36
print(registros.groupby(['externo','estado']).size().to_string())
print('11880 originales;4752 únicas condicionadas a copias/contexto exactos;1155 externas')
# %%
print(metricas[(metricas.procedimiento=='global')&metricas.corte.isin(['anio','2021–2024','2025'])][['corte','anio','n','mae','rmse','sesgo','delta_mae']].to_string(index=False))
# %%
from IPython.display import display,Image
for name in ('mae_por_anio.png','delta_mae_territorio.png','cambios_global.png'):
    display(Image(filename=str(OUT/'graficos'/name)))
