# %% markdown
# Resultados de la evaluación exploratoria del puntaje global territorial.
# Fuentes agregadas locales; no datos personales. Ledger cerrado antes de este análisis.
# Las cifras, tablas y figuras se generan aquí mediante funciones compartidas.
# Orden: integridad, auditoría independiente, antecedentes, análisis, figuras, tablas complementarias.
# No ajustes nuevos, carga de modelos ni aprovechamiento del saldo del piloto.
# %%
from comun import *
from auditor import audit
from resultados import antecedents,analyse,figures,complementary_tables
print(preflight())
# %%
print(audit())
# %%
historical=antecedents()
# %%
primary=analyse()
# %%
figure_files=figures()
# %%
design=complementary_tables()
# %% markdown
# Redacción final, después de auditoría, tablas y revisión visual; cifras ligadas a salidas anteriores.
# %%
from redaccion import thesis
from informe import technical
text_control=thesis()
technical()
