# %% markdown
# Resultados comparables y gráficas del objetivo 3
# Reproducción nueva de métricas de predicciones anteriores; cero entrenamiento.
# Objetivo: distinguir desempeño de modelos con pobreza de la referencia de historia.
# %%
from pathlib import Path
import sys
root=Path.cwd()
while not (root/'AGENTS.md').exists():
    if root==root.parent:raise RuntimeError('Abrir dentro del proyecto')
    root=root.parent
folder=root/'entrega_objetivos3_4_final'
sys.dont_write_bytecode=True
sys.path.insert(0,str(folder/'fuentes'))
from analisis import run,verify_inputs
verify_inputs()
# %%
import unittest
from test_graficas import TestEvidence
test_result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestEvidence))
assert test_result.wasSuccessful()
# %%
metricas,figuras=run()
metricas
# %%
from IPython.display import display,Image
for name in figuras:display(Image(filename=str(folder/name)))
# %% markdown
# Lectura del resultado
# Modelo con pobreza ampliado: MAE 4,880; persistencia: 3,429;
# selección final histórica: 3,365 puntos sobre los mismos 165 pares.
# El último procedimiento no usa IPM. La ausencia de mejora de pobreza es válida.
# Todos los años eran conocidos por la investigación: comparación exploratoria.
# No se infiere causalidad, significación ni respuesta a intervenciones.
