# %%
from pathlib import Path
import sys
root = Path.cwd()
if not (root / 'AGENTS.md').exists():
    root = next(p for p in root.parents if (p / 'AGENTS.md').exists())
sys.path.insert(0, str(root / 'experimentos_objetivo3_v5/etapa1/fuentes'))
from comun_v5 import candidatos, GRUPOS, ventanas, SEMILLA, OUT, historial
from controles import datos, ejecutar
print('Diseño 5.0.0; semilla', SEMILLA, ';36 candidatos; cero fits del panel real')
for grupo, entradas in GRUPOS.items():
    print(grupo, len(entradas), entradas)
print('Ventanas:', ventanas())
# %%
panel_inventado = historial(datos())
print(panel_inventado[['codigo_departamento','anio','anio_previo','puntaje_previo','cambio_observado','cambio_ipm']].to_string(index=False))
assert panel_inventado[panel_inventado.anio == 2021].anio_previo.eq(2019).all()
print('2018 solo historial; salto2019→2021 sin anualizar; cambios negativos válidos')
# %%
resultado = ejecutar(OUT / 'sinteticos/notebook')
for control in resultado['controles']:
    print('APROBADO:', control)
print('Pruebas:', resultado['pruebas'])
assert resultado['ajustes_panel'] == 0 and not resultado['ledger_operativo_creado']
print('Presupuesto real no iniciado; meta v5 no evaluada; etapa2 requiere otra autorización')
