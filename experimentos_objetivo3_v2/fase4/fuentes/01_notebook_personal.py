# %% [markdown]
# Notebook personal — objetivo 3 v2, fase 4
# Modo predeterminado: verificar predicciones guardadas, sin entrenar.
# Protocolo 2.0.2 y 100 configuraciones congeladas, semilla 20261010.
# Requiere repositorio completo y entorno exacto fase2/requirements.lock.txt:
# Python 3.12.14, sklearn 1.9.1. No instala dependencias ni descarga datos.
# Abrir desde el repositorio o fase4/notebooks; ejecutar las celdas en orden.
# Entradas: panel fase1, configuración fase2 y artefactos guardados fase3.
# Salidas de esta verificación: fase4/resultados/notebook_verificacion/.
# Los resultados son ecológicos contemporáneos; no efectos causales ni pronósticos
# disponibles antes de publicar el IPM. 2025 es exploratorio, no reserva inédita.
# %%
import sys
sys.dont_write_bytecode = True
from pathlib import Path
inicio = Path.cwd().resolve()
ROOT = next((p for p in [inicio, *inicio.parents] if (p / 'experimentos_objetivo3_v2/fase4/fuentes/revision.py').is_file()), None)
assert ROOT is not None, 'Ejecutar desde el repositorio o sus subcarpetas'
sys.path.insert(0, str(ROOT / 'experimentos_objetivo3_v2/fase4/fuentes'))
from revision import integridad, revisar, F4, guardar
from presentar import presentar
MODO = 'verificar'  # Cambiar voluntariamente a 'reejecutar' para un piloto NUEVO completo.
assert MODO in ('verificar', 'reejecutar')
verificacion_entorno = integridad()
print('Entorno y huellas aprobados:', verificacion_entorno['python'])
print('Semilla: 20261010; configuración: 2.0.2; 100 candidatos')
# %%
SALIDA = F4 / 'resultados/notebook_verificacion'
metricas, comparaciones, pares, controles = revisar(out=SALIDA)
guardar(SALIDA / 'integridad_consulta.json', verificacion_entorno)
print('Revisión ejecutada sobre artefactos guardados; ajustes nuevos:', controles['ajustes_nuevos_revision'])
print('Condición exacta de entrega:', controles['condicion'])
print(metricas[(metricas.periodo == '2021-2025') & (metricas.ambito == 'conjunto')].to_string(index=False))
# %% [markdown]
# 2021–2024 separado y aporte de 2025
# La condición se calcula sobre las 165 filas de 2021–2025, sin sustituir el
# procedimiento por la especificación que parezca mejor en los errores externos.
# R² territorial usa cinco observados; puede ser negativo con baja variación.
# %%
print(metricas[(metricas.ambito == 'conjunto') & metricas.procedimiento.isin(['procedimiento_v2', 'referencia_v1'])].to_string(index=False))
deterioros = comparaciones[(comparaciones.periodo == '2021-2025') & (comparaciones.procedimiento == 'procedimiento_v2') & (comparaciones.ambito != 'conjunto')]
print(deterioros[['ambito', 'grupo', 'delta_mae', 'delta_rmse', 'deteriora_mae']].to_string(index=False))
print('Diferencias emparejadas, primeras filas:')
print(pares[['codigo_departamento', 'anio', 'delta_error_firmado', 'delta_error_absoluto', 'delta_error_cuadratico']].head().to_string(index=False))
# %% [markdown]
# Diferencias: e = predicción − observado. Error firmado v2−v1 indica dirección,
# no mejora: positivo puede reducir una subestimación. Error absoluto positivo
# indica deterioro de ese par; error cuadrático positivo también, en puntos².
# CSV completo: 165 pares. No se presupone independencia temporal o territorial
# ni se aplica una prueba de significancia para justificar el umbral práctico.
# %%
GRAPH_PATHS = presentar(metricas, comparaciones, pares, SALIDA)
print('Gráficos recalculados:', ', '.join(p.name for p in GRAPH_PATHS))
# %% [markdown]
# Reejecución voluntaria completa
# Cambiar MODO a 'reejecutar' y ejecutar la siguiente celda inicia un piloto nuevo,
# con presupuesto máximo de 7200 segundos para TODO el procedimiento, referencias
# y repeticiones incluidas. Tiempo histórico observado: 1540.91 segundos (~25.7 min),
# sin garantía de duración en otro equipo. Revisión/gráficos quedan fuera del tiempo
# de ajustes. Un subproceso ejecuta el motor compartido con un hilo y semilla fija.
# Guarda configuración referenciada, ledger propio y controles en una carpeta nueva
# fase4/reproducciones/piloto_FECHA/. Nunca reutiliza modelos ni saldo de fase3.
# No borrar ni reiniciar el ledger ante una interrupción. Estado incompleto se conserva;
# no afirmar reproducción exitosa si falla o agota presupuesto. Esta celda no fue
# ejecutada con entrenamiento en la entrega: solo se verificó su rama predeterminada.
# %%
if MODO == 'reejecutar':
    import subprocess
    subprocess.run([sys.executable, str(F4 / 'fuentes/reejecutar.py')], cwd=ROOT, check=True)
else:
    print('Modo verificar: no se inició reentrenamiento. La reproducción completa es voluntaria.')
# %% [markdown]
# Límites conservados
# Población de casos completos, geografía del colegio, peso igual territorio-año,
# IPM y Saber de poblaciones distintas, comparabilidad IPM, dependencia y pocos años.
# Guainía: 238 completos frente a 404 con global; diferencia descriptiva 21.012106
# puntos (fase1/resultados/diagnostico_medias_disponibles.csv). No identifica causa.
# Fuentes locales sin autenticación independiente. 2020 excluido definitivamente.
# E3-01 conserva regex temporal completa; E3-02 corrige máximo descriptivo a 1555
# sin cambiar 100 candidatos ni 7200 segundos. No hay ajuste final ni simulación.
