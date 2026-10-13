# %% [markdown]
# Preparación focal del objetivo 4
# Fuentes locales completas; originales conservados. La lectura por bloques se realizó mediante preparar.py. Para repetir en una copia separada con las mismas fuentes, cambiar REPROCESAR_RAW a True y ejecutar con Python con pandas/openpyxl. No contiene datos individuales.
# %%
from pathlib import Path
import sys,json
BASE=Path.cwd()
if not (BASE/'PLAN_Y_PROTOCOLO.md').exists():
    BASE=BASE/'objetivo4_validacion_escenarios'
sys.path.insert(0,str(BASE/'fuentes'))
REPROCESAR_RAW=False
if REPROCESAR_RAW:
    from preparar import run
    run()
print(json.dumps(json.loads((BASE/'preparacion/CONTROL_PREPARACION.json').read_text()),ensure_ascii=False,indent=2))
# %%
from modelos import panel
from tests import run
print('Pruebas previas aprobadas:',run(False))
d=panel()
print(d.groupby('anio').agg(territorios=('codigo_departamento','size'),evaluados=('n_punt_global','sum')).to_string())
