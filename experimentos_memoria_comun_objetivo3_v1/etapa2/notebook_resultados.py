"""Fuente editable: lector de resultados ya ejecutados, sin ajustar modelos."""
CELLS=[
'''from pathlib import Path
import json
base=Path(__file__).resolve().parent
read=lambda p:json.loads((base/p).read_text())
validation=read('resultados/VALIDACION_PILOTO.json')
assert validation['aprobado']
print(json.dumps(validation,ensure_ascii=False,indent=2))''',
'''meta=read('resultados/meta.json')
assert meta['n']==165
print(json.dumps(meta,ensure_ascii=False,indent=2))
print('Todos2021–2025vistos: exploratorio, sin confirmación independiente ni causalidad.')''']
