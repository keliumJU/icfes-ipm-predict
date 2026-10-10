# %% [markdown]
# Documentación del objetivo 3, fase 5
# Consume base agregada y CSV congelados. Produce informe, tablas y figuras.
# No carga artefactos joblib, ajusta modelos, reselecciona o simula.
# La ejecución registrada usa Python secuencial compile/exec, no un kernel Jupyter.
# Entradas, versiones y contextos: fase5/resultados/generacion.json.
# %%
from pathlib import Path
import sys
root = Path.cwd()
assert (root / 'fase5/fuentes/documentar.py').exists(), 'Ejecutar desde raíz del proyecto'
sys.path.insert(0, str(root / 'fase5/fuentes'))
from documentar import generar
# %% [markdown]
# Generación con resultados existentes
# Las tablas conservan métricas de selección, reevaluación expuesta y diagnóstico
# territorial como contextos separados. Las figuras son descriptivas y no causales.
# %%
registro = generar()
print('Tablas:', len(registro['tablas']), '; figuras:', len(registro['figuras']))
print('Métricas existentes cotejadas:', len(registro['comprobaciones_metricas']))
assert registro['modelos_ajustados'] == 0
# %% [markdown]
# Lectura y límites
# Ganador global y reevaluación permanecen cerrados. No se evaluó persistencia.
# El informe conserva OLS IPM mejor que GBR IPM en MAE reservado y tasas con menor
# MAE territorial que ambas. Los percentiles son condicionales a errores fijos.
# Ver informe_objetivo_3.md y fase5/decisiones_previas.md para discusión completa.
