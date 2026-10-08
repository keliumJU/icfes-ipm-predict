# %% [markdown]
# # 01 — Protocolo y controles de la base agregada
# Fase 2: no entrena, no simula y no calcula métricas de evaluación.
# Ejecutar desde la raíz o desde notebooks/. Solo lee agregados y evidencias.
# Las salidas de controles se guardan por CLI; el notebook distribuido no contiene salidas.
# %%
from pathlib import Path
import sys
sys.dont_write_bytecode = True

root = Path.cwd().resolve()
if not (root / "protocolo/fuentes/controles.py").exists():
    root = root.parent
assert (root / "protocolo/fuentes/controles.py").exists(), "Abrir desde raíz o notebooks/"
sys.path.insert(0, str(root / "protocolo/fuentes"))
from controles import verificar
from configuracion import DIMENSIONES, ESPECIFICACIONES
# %% [markdown]
# ## Integridad y separación temporal
# No se muestran registros individuales ni valores del resultado de 2023–2024.
# Las comprobaciones de cobertura/rango no se usan para ajustar candidatos.
# %%
resumen = verificar()
print({k: resumen[k] for k in ["base_filas", "desarrollo_filas", "reevaluacion_filas", "controles_aprobados"]})
print(resumen["ventanas"])
# %% [markdown]
# ## Entradas congeladas
# Las dimensiones son agrupaciones documentales. No se crean promedios de dimensión.
# %%
print(DIMENSIONES)
print({nombre: len(columnas) for nombre, columnas in ESPECIFICACIONES.items()})
