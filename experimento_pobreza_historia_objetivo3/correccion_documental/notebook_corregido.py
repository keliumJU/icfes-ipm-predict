"""Reutiliza todas las celdas congeladas; solo agrega reloj/guardia de infraestructura.

Celdas2–5 idénticas a las fuentes científicas originales. Cálculos sin cambios.
"""
from infra_correccion import MAIN
from notebook_resultados import CELLS as ORIGINAL
CELLS=[ORIGINAL[0]+'''
from correccion_documental.infra_correccion import activate, guard_status
print(json.dumps(activate(analisis), ensure_ascii=False))''',*ORIGINAL[1:]]
CELLS[-1]+='''
print(json.dumps(guard_status(), ensure_ascii=False))'''
SYNTHETIC=[
'''import sys,json,platform
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from correccion_documental.infra_correccion import activate,guard_status
activate()
print(json.dumps({'python':platform.python_version(),'inventado':True,'new_fits':0}))''',
'''import math
y=[1.,2.,4.];p=[2.,2.,3.]
e=[b-a for a,b in zip(y,p)]
mae=math.fsum(abs(v) for v in e)/len(e)
assert mae==2/3
print(json.dumps({'inventado_mae':mae,'n':len(e),'unidad':'puntos inventados'}))''',
'''print(json.dumps(guard_status()))'''
]
