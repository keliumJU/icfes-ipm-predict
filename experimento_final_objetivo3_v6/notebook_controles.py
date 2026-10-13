# %% markdown
# Controles v6: entorno exacto, originales y pruebas inventadas. Sin fits reales.
# Orden: preflight → tests → integridad del panel. Entradas: contrato y dos fuentes.
# %%
from comun import *
from motor import panel,defaults
from pruebas import tests
print({'preflight':preflight()['aprobado'],'seed':SEED})
# %%
resultado_pruebas=tests()
print(resultado_pruebas)
# %%
p=panel()
print({'levels':sum(len(v) for v in p['levels'].values()),'changes':sum(len(v) for v in p['d'].values()),'years':p['years'],'defaults':defaults(),'real_fits':0})
