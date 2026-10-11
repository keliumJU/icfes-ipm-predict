# %% [markdown]
# Controles prospectivos v3 — únicamente etapa 1
# Estructura real agregada y controles sintéticos se guardan por separado.
# Este notebook no ajusta candidatos ni calcula predicciones/errores reales.
# Ejecutar con Python 3.12.14 y requirements.lock.txt exacto. Semilla 20261010.
# Orden: preparación estructural → controles sintéticos → lectura de evidencia.
# %%
import sys
from pathlib import Path
# Resolver desde raíz del proyecto o desde la carpeta notebooks.
root = Path.cwd().resolve()
while not (root / 'AGENTS.md').is_file() and root != root.parent:
    root = root.parent
if not (root / 'experimentos_objetivo3_v3/etapa1/fuentes').is_dir():
    raise RuntimeError('Ejecutar desde el proyecto o una subcarpeta')
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'experimentos_objetivo3_v3/etapa1/fuentes'))
from preparar import preparar
from controles import controles
from comun_v3 import E1, read
preparar()
# %% [markdown]
# Pruebas sintéticas, sin presupuesto operativo
# Se usan modelos lineales sobre tres filas inventadas y procesos dobles terminables.
# El ledger de prueba conserva cada ejecución; no es el ledger del futuro piloto.
# %%
resultado = controles(E1 / 'resultados/notebook_sinteticos')
print('Aprobados:', len(resultado['controles']), 'grupos; ajustes reales:', resultado['ajustes_panel_real'])
# %%
estructura = read(E1 / 'resultados/estructura_real.json')
grilla = read(E1 / 'resultados/configuraciones_congeladas.json')
print('Filas fuente/cambios/externas:', estructura['registros_fuente'], estructura['cambios'], estructura['externas'])
print('Configuraciones:', len(grilla['configuraciones']), 'Cota sin fallos:', grilla['cota_sin_fallos']['total'])
print('Etapa 2 pendiente de autorización en sesión posterior. Piloto no iniciado.')
