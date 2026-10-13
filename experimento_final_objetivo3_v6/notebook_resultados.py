# %% markdown
# Objetivo 3 — cierre INCOMPLETO del último experimento exploratorio v6
# Ejecutar desde la raíz del proyecto con entorno exacto y PYTHONDONTWRITEBYTECODE=1.
# Entradas: contrato congelado, fuentes agregadas y piloto cerrado. No fits/cargas.
# Orden: revalidación → auditor independiente parcial → antecedentes → controles → figura diagnóstica → texto.
# No ejecutar para volver a abrir el piloto. Los artefactos originales quedan intactos.
# %%
from comun import *
from auditor import audit_incomplete
from resultados import antecedents
from entrega_incompleta import control_tables,diagnostic_figure,document
print({'environment':environment(),'conservation':conservation()})
# %%
audit_report=audit_incomplete()
print(audit_report)
# %%
historical_results=antecedents()
# %%
contract_controls=control_tables()
# %%
figure_file=diagnostic_figure()
# %%
evidence_count=document()
print({'fits_this_notebook':0,'deserializations':0,'evidence_count':evidence_count,'primary_v6_valid':False,'performance_v6_evaluated':False,'figure':str(figure_file)})
