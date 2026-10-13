# %% markdown
# Objetivo 3 — último experimento exploratorio v6
# Ejecutar desde la raíz del proyecto con entorno exacto y PYTHONDONTWRITEBYTECODE=1.
# Entradas: contrato congelado, fuentes agregadas y piloto cerrado. No fits/cargas.
# Orden: revalidación → auditor independiente → antecedentes → análisis → figuras → texto.
# No ejecutar para volver a abrir el piloto. Los artefactos originales quedan intactos.
# %%
from comun import *
from auditor import audit
from resultados import antecedents,analyse,figures,thesis
print({'environment':environment(),'conservation':conservation()})
# %%
audit_report=audit()
print(audit_report)
# %%
historical_results=antecedents()
# %%
primary_results=analyse()
# %%
figure_files=figures()
# %%
evidence_count=thesis()
print({'fits_this_notebook':0,'deserializations':0,'evidence_count':evidence_count,'primary':primary_results,'figures':figure_files})
