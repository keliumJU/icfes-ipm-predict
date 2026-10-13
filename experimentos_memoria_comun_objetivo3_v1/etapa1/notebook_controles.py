# %%
"""Notebook de controles fase2. Solo datos inventados; sin modelos del panel.

Fuente editable. El generador ejecuta secuencialmente estas celdas con Python,
captura stdout real y valida nbformat; no requiere kernel Jupyter.
"""
from preflight import environment
env = environment()
print('Entorno exacto aprobado:', env['aprobado'], '| semilla:', env['semilla'])

# %%
from controles import run_suite
report, report_path = run_suite('notebook')
assert report['aprobado'] and report['fits_panel_real'] == 0
print('Todos los controles se ejecutaron con niveles inventados.')

# %%
from motor import FUTURE_CONTRACT
print('Contrato futuro:', FUTURE_CONTRACT)
print('Presupuesto real iniciado:', report['presupuesto_real_iniciado'])
print('Evidencia de esta ejecución:', report_path.name)
print('Fase3 requiere autorización expresa y validación de congelación/conservación.')
