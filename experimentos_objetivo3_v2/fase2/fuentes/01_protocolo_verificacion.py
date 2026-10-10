# %% [markdown]
# Protocolo v2 y verificación — exclusivamente fase 2

Orden: leer `../PROTOCOLO_V2.md`, verificar congelación, ejecutar nueve controles.
Entradas: panel agregado validado de fase 1 y huellas previas. Salidas: controles,
predicciones **sintéticas** y presupuesto de **dobles** en `../resultados/`.
No ajusta candidatos ni predice sobre el panel real. No es el notebook personal.
Semilla prospectiva 20261010. Las versiones efectivamente usadas se registran en entorno.json.

# %%
from pathlib import Path
import sys
sys.dont_write_bytecode = True
here = Path.cwd()
fase2 = next(p.resolve() for p in (here.parent, here, here / 'experimentos_objetivo3_v2/fase2')
             if (p / 'fuentes/verificar.py').is_file())
sys.path.insert(0, str(fase2 / 'fuentes'))
from verificar import ejecutar_verificacion

# %% [markdown]
Los controles reales verifican integridad y particiones del panel completo. El escalado,
selección, métricas, predicciones guardadas y presupuesto se prueban con ejemplos
sintéticos y dobles; sus cifras no son resultados predictivos de los territorios.
El piloto de cien configuraciones y dos horas requiere autorización expresa de fase 3.

# %%
resultado = ejecutar_verificacion('controles_notebook.json')
assert resultado['controles_aprobados'] == 9
assert resultado['ajustes_candidatos_panel'] == resultado['predicciones_panel'] == 0
print({'controles_aprobados': 9, 'predicciones_panel_real': 0, 'modo': 'verificacion'})
