# %% markdown
# Controles previos a la ejecución autorizada del mismo diseño.
# Entorno exacto, originales, semilla y contrato; datos inventados para todos los fits de prueba.
# Presupuesto del piloto aún no iniciado. Esta ejecución no produce resultados de tesis.
# %%
from comun import *
from motor import panel,defaults
from pruebas import tests
from pruebas_ejecucion import execute_tests
print(preflight())
# %%
print(tests())
# %%
print(execute_tests())
# %%
p=panel()
print({'niveles':sum(len(v) for v in p['levels'].values()),'cambios':sum(len(v) for v in p['d'].values()),'anios':p['years'],'defaults_completos':defaults(),'fits_reales':0})
