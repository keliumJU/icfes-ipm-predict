# %% markdown
# Diseño del modelo departamental y evolución de las decisiones
# Este cuaderno explica el diseño desde la base con pobreza hasta la evaluación 2018–2025.
# La pregunta de tesis es pobreza y desempeño; la historia del puntaje es una referencia,
# no evidencia de efectos de pobreza. Las cinco dimensiones organizan quince tasas,
# pero sus contribuciones oficiales no se reconstruyen promediándolas.
# El periodo principal fue ampliado por decisión del usuario el 12/10/2026.
# Población: grado 11, filtros auditados, global recibido, departamento del colegio.
# No personas únicas certificadas. Cada territorio-año pesa igual. 2020 excluido.
# %%
from pathlib import Path
import sys,json,importlib.util
root=Path.cwd()
while not (root/'AGENTS.md').exists():
    if root==root.parent:raise RuntimeError('Abrir dentro del proyecto')
    root=root.parent
folder=root/'entrega_objetivos3_4_final'
sys.dont_write_bytecode=True
sys.path.insert(0,str(folder/'fuentes'))
from analisis import verify_inputs
verify_inputs()
# %% markdown
# Primer diseño con pobreza
# Se comparan IPM, quince tasas y ambas entradas. Media/OLS sirven de referencia;
# Ridge estabiliza coeficientes y RF/GBR permiten relaciones no lineales.
# La selección usa ventanas 2018→2019, 2018–2019→2021 y hasta 2021→2022.
# Primero se minimiza MAE, después RMSE dentro de banda de 0,1 puntos, y finalmente
# se prefiere sencillez y el orden fijado. 2023–2024 no se usan en ese ajuste.
# Fueron años antes examinados: reevaluación expuesta, no prueba inédita.
# Parámetros completos se leen del congelamiento, nunca se inventan aquí.
# %%
base=json.loads((root/'fase3/resultados/congelacion.json').read_text())
print('Ganador base:',base['ganador_global'])
print(json.dumps(base['parametros_completos'][base['ganador_global']],indent=2,ensure_ascii=False))
# %% markdown
# Ampliación con pobreza y 2025
# V2 conserva la misma respuesta y añade 2025; compara 100 configuraciones y
# selecciona con validaciones internas anteriores a cada año externo 2021–2025.
# Más familias o candidatos no garantizan mejorar. La comparación relevante usa
# las mismas 165 llaves y observados, no el MAE de una muestra distinta.
# %%
v2=json.loads((root/'experimentos_objetivo3_v2/fase2/resultados/configuraciones_congeladas.json').read_text())
print('Configuraciones V2:',len(v2['configuraciones']))
print('Ventanas:',v2['ventanas'])
v2['configuraciones'] # contratos completos, incluidos parámetros
# %% markdown
# Historia y cambio como referencia
# Persistencia: usar el último puntaje conocido del territorio. Para 2021 es 2019;
# no se inventa 2020 ni se anualiza el salto. V6 compara persistencia, medias/medianas
# de cambios, regresión de mediana regularizada, Ridge y árboles pequeños.
# También examina cambio común y corrección territorial. El resultado principal
# es el procedimiento de selección; no el candidato de mejor error externo.
# Su mejora de 1,864 % se concentra en 2025 y no demuestra aporte del IPM.
# El 5 % fue una meta histórica cerrada, no requisito nuevo de esta entrega.
# %%
v6=json.loads((root/'experimento_final_objetivo3_v6/ejecucion_autorizada/ESPECIFICACION_V6.json').read_text())
print('Semilla V6:',v6['semilla'],'Candidatos:',len(v6['candidates']))
print(json.dumps(v6['selection'],indent=2,ensure_ascii=False))
v6['candidates'] # parámetros, historia, componentes y orden completos
# %% markdown
# Reproducción manual del entrenamiento
# Las siguientes rutas reutilizan constructores y selectores originales, pero no llaman
# runners ni escriben en entregas cerradas. Devuelven resultados en memoria.
# Use el entorno registrado /tmp/icfes-v2-fase2-venv, sus locks originales y fuentes intactas.
# No se entrenó de nuevo para esta entrega. Activar cada ruta es una ejecución manual nueva,
# cuya duración y resultados deben registrarse. Los límites son exclusivos de reproducción;
# no heredan presupuesto anterior. Si se agotan o falla un ajuste, el resultado es incompleto.
# Base reproduce selector global y reserva; V2 reproduce selector global por ventanas;
# V6 reproduce selección final. Para auditorías completas por candidato se conservan
# los notebooks y pruebas originales, que no deben ejecutar sobre sus carpetas selladas.
# %%
from reproduccion_manual import base_manual,pobreza_ampliada_manual,dinamica_manual
ENTRENAR_BASE=False
ENTRENAR_POBREZA_AMPLIADA=False
ENTRENAR_DINAMICA=False
if ENTRENAR_BASE:
    tabla_base,ganador_base,pred_base=base_manual(limit_seconds=600)
if ENTRENAR_POBREZA_AMPLIADA:
    decisiones_pobreza,pred_pobreza=pobreza_ampliada_manual(limit_seconds=1800)
if ENTRENAR_DINAMICA:
    decisiones_dinamica,pred_dinamica=dinamica_manual(limit_seconds=900)
print('Rutas manuales disponibles; entrenamiento desactivado por defecto.')
# %% markdown
# Comprobar resultados sin entrenar
# Continúe en 02_resultados_y_graficas.ipynb. Lee predicciones guardadas, comprueba
# llaves y observados idénticos, recalcula métricas y genera figuras con pruebas.
# Las versiones explican decisiones, no validaciones independientes acumulables.
# H3 original no queda contrastada: falta su línea base de año/composición y otros
# requisitos escritos. El buen error histórico tampoco hace apto un modelo para
# escenarios de IPM si ese modelo no lo utiliza. Objetivo 4 requiere decisión aparte.
