# %%
from pathlib import Path
import json
import pandas as pd
ROOT=Path.cwd()
assert (ROOT/'experimentos_objetivo3_v3/etapa2/resultados/verificacion.json').exists(), 'Ejecutar desde la raíz del proyecto después de verificar el piloto.'
RESULTADOS=ROOT/'experimentos_objetivo3_v3/etapa2/resultados'
check=json.loads((RESULTADOS/'verificacion.json').read_text())
assert check['aprobado'] and check['completo']
print('Piloto exploratorio completo verificado. Este notebook solo lee artefactos; no ajusta modelos.')
print('Ajustes documentados:',check['ajustes_documentados'],'; segundos presupuestados:',check['segundos_ajustes'])
# %%
metricas=pd.read_csv(RESULTADOS/'metricas.csv',float_precision='round_trip')
print(metricas[metricas.periodo=='2021–2025'].to_string(index=False))
print(json.loads((RESULTADOS/'meta.json').read_text()))
# %%
ganadores=pd.read_csv(RESULTADOS/'ganadores.csv')
print(ganadores.to_string(index=False))
print('2021 persistencia fija; desde2022 selección interna sobre puntaje reconstruido. Internas v3 distintas de v2,165 externas idénticas.')
print('2021–2025 ya examinados: sin confirmación independiente, causalidad ni pronóstico anterior a publicación del IPM. Revisión/notebook personal requieren etapa3 separada.')
