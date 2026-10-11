# %%
"""Notebook de lectura histórica y controles; no modelos reales ni simulación."""
import sys
from pathlib import Path
root=Path.cwd()
if not (root/'AGENTS.md').exists():raise ValueError('Ejecutar desde raíz del proyecto')
sys.dont_write_bytecode=True
sys.path.insert(0,str(root/'experimentos_objetivo3_v4/etapa1/fuentes'))
from comun_v4 import *
from preparar import check_hashes
r=read(OUT/'referencias_guardadas.json')
check_hashes(r['archivos_sha256']);check_hashes(r['selecciones_sha256'])
print('Referencias históricas íntegras; no se cargan modelos. Semilla:',SEMILLA)
# %%
from preparar import independientes
m=pd.read_csv(OUT/'metricas_historicas.csv',dtype={'periodo':str})
print(m[(m.referencia.isin(['v3','v2']))&(m.ambito.isin(['conjunto','anio','corte']))].to_string(index=False))
print('Recálculo histórico; meta v4 aún no evaluada. Deterioros completos en CSV.')
# %%
from controles import controles
resultado=controles(OUT/'notebook_sinteticos')
print('Controles realmente ejecutados:',len(resultado['controles']))
