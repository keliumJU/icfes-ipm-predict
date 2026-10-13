"""Fuente editable; cinco celdas ejecutables, sin fits."""
CELLS=[
'''from pathlib import Path
import sys, json
sys.path.insert(0, str(Path.cwd()))
from infra import HERE, load
import analisis
print(json.dumps({'audit_aprobado': load(HERE/'AUDITORIA.json')['aprobado'], 'new_fits': 0, 'seed': 20261010}, ensure_ascii=False))''',
'''resumen = analisis.tables()
print(json.dumps(resumen, ensure_ascii=False, indent=2))''',
'''figuras = analisis.figures()
from IPython.display import display, Image
for name in figuras:
    display(Image(filename=str(HERE/'resultados/figuras'/name)))
print(json.dumps(figuras, ensure_ascii=False))''',
'''texto = analisis.academic_text()
print(json.dumps(texto, ensure_ascii=False))''',
'''control = analisis.text_control()
print(json.dumps(control, ensure_ascii=False))'''
]
