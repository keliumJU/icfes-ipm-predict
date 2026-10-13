# Integración académica para la última revisión

12/10/2026. Documento original preservado. La entrega prepara contenido insertable; no acredita aceptación del asesor, cierre de tesis o modificación de objetivos.

## Dónde incorporar el contenido

Tesis Vigente/ACA2.pdf p. 114 concluye el descriptivo. El texto nuevo objetivo3/TEXTO_PARA_TESIS.md y su Word comienzan con «Diseño y evaluación del modelo predictivo departamental» y mantienen subtítulos claros e impersonal académico. Incorporar allí el desarrollo predictivo, después de conciliar la sección existente pp. 115–117. No pegar sobre sus afirmaciones incompatibles.

La sección pp. 115–117 usa departamento de presentación, 160 celdas y una regla de correlación para sugerir predictores. El análisis actual conserva colegio, grado 11, Bogotá, 2021 y filtros auditados; 198 celdas anteriores y 231 en ampliación. Ese contraste es indispensable para no atribuir los modelos a otra población. Reutilizar auditoria/propuesta_correccion_tesis.md para sustituir la explicación antigua o rotularla como antecedente. No emplear sus correlaciones calculadas sobre toda la serie para justificar la selección temporal actual. No se repite auditoría descriptiva ni efectos fijos.

Las tablas y figuras nuevas tienen rótulos provisionales: numerarlas correlativamente según la edición final del grupo. Sus fuentes ya están en los pies y en objetivo3/EVIDENCIAS*.json. Las cifras se muestran con tres decimales en el cuerpo; CSV completos conservan precisión de cálculo, sin afirmar precisión sustantiva equivalente.

## Decisiones de periodo y alcance que deben reflejarse

El usuario decidió 2018–2025 principal en esta sesión. Esto amplía el análisis predictivo a 231 celdas y no actualiza por sí solo descriptivos o efectos fijos. Las 198 medias y denominadores anteriores se comprobaron exactamente dentro de analisis.data, sin revisar microdatos.

Ubicaciones a conciliar: pregunta p. 23, preguntas específicas p. 24, objetivo general/específicos p. 25, periodo y particiones pp. 58–59, resultados y conclusión. No reemplazar globalmente 2024 por 2025: el capítulo descriptivo anterior sigue documentando 2018–2024 y el trabajo del objetivo 2 queda fuera de esta sesión. Una formulación transparente para revisión es «El estudio descriptivo original cubre 2018–2024; el análisis predictivo se amplía a 2025». Si el asesor exige un único periodo para todos los objetivos, la actualización de los otros objetivos sería un pendiente académico separado, no una tarea aquí realizada.

## Metodología que no puede mantenerse como si se hubiera ejecutado

P. 58: línea base de año/composición, cinco contribuciones dimensionales oficiales, Lasso y proporción niveles 3–4 de Matemáticas. La ampliación V2 sí incluyó ElasticNet, a diferencia de fase6, pero no certifica el cumplimiento de toda esa página. V6 trabaja solo con historia y no reemplaza el modelo de pobreza. Conservar la respuesta global original; Matemáticas no se convierte en respuesta principal.

P. 59: reserva inédita/una sola evaluación, promedio territorial de entrenamiento, especificación sin IPM/composición, exclusión 2021 y escenarios. Describir separaciones realmente realizadas y exposición de años. El diagnóstico territorial de fase4 utilizó hiperparámetros seleccionados con esos territorios: diagnóstico, no validación independiente. No atribuir esos diagnósticos a V6 si no fueron ejecutados para ella.

H3 p. 26 requiere ventaja significativa frente a composición/año. Las comparaciones disponibles no ejecutan ese contraste completo. No declarar H3 confirmada ni sustituir «significativa» por el umbral histórico del 5 %. Informar resultado desfavorable y ausencia de confirmación; cualquier modificación de hipótesis/objetivo debe ser explícita ante el asesor.

## Evolución desde la base

La narrativa cubre etapas útiles para el objetivo: base con pobreza (fase6, 198 celdas); ampliación V2 con pobreza (231 celdas); incorporación de persistencia y exploración final de historia (V6). No presenta todas las carpetas como validaciones independientes ni reconstruye la rama histórica de procedencia. Parámetros/semillas/grillas completas permanecen en los notebooks y contratos originales enlazados. V5 y recencia coincidieron con persistencia según antecedentes_recalculados.csv; no se cuentan como mejoras separadas. Los candidatos individuales de mejor MAE externo no reemplazan la elección primaria.

## Reproducción y evidencia

1. 01_diseno_y_reproduccion.ipynb: explicación, contratos de parámetros y rutas manuales base/V2/V6 desactivadas por defecto. Generado y validado; no entrenado en esta entrega. Rutas globales, no duplicación de todos los pilotos/auditorías anteriores.
2. 02_resultados_y_graficas.ipynb: realmente ejecutado; cinco pruebas de llaves, observados, métricas y etiquetas; genera tablas/gráficas y evidencia. No entrena modelos.
3. Fuentes Python: analisis.py, test_graficas.py, reproduccion_manual.py, fuentes de cuadernos y generador. Orden/entornos en README. No editar JSON de notebooks.

La reproducción manual de ajustes no se presenta como verificada por nueva ejecución. Si se activa, registrar sus resultados separados, entorno y duración; no ejecutar runners que escriben en carpetas previas. Los verificadores previos de inventario cerrado no se adaptan a esta ampliación. Se comprobaron 3.483 huellas del manifiesto de V6 sin ejecutar su preflight externo, que contiene inventarios/Git cerrados. Esto conserva la evidencia local; no autentica publicación histórica.

Objetivo 4 permanece fase separada. La selección final de historia no sustenta sensibilidad a IPM. Decidir escenarios o brecha académica con el usuario antes de calcular. No declarar todo listo científicamente mientras esa decisión indispensable siga pendiente.
