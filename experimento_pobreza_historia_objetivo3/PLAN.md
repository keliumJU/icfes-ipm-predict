# Contraste exploratorio entre pobreza e historia del puntaje

## Estado y propósito

Plan aprobado por el usuario. En esta sesión se realizó exclusivamente preparación: restauración offline del entorno exacto y verificación de la entrega anterior. El usuario decidió guardar el plan y continuar en una nueva sesión. No hay ajustes, piloto ni resultados de este contraste. Consultar CONTINUIDAD.md antes de ejecutar.

Pregunta: ¿el IPM o sus quince indicadores añaden información a la historia del puntaje para estimaciones condicionales territoriales? No se persigue una demostración causal. El texto académico se redactará al final, siguiendo la tesis vigente y sin etiquetas de versiones.

## Contrato científico cerrado

- Fuente principal, población, media recibida y geografía del colegio conservadas; igual peso por territorio-año. Fuente derivada solo para cotejar historia/cambios. No raw, red ni nuevas fuentes.
- Respuesta: prom_punt_global. H contiene puntaje anterior disponible y cambio anterior, sin anualizar. I contiene IPM contemporáneo; D contiene quince indicadores contemporáneos en orden DIMENSIONES/TASAS. HI y HD combinan historia con cada alternativa. No combinar IPM e indicadores ni introducir otras entradas.
- 2018 nivel histórico; 2019 historia, nunca respuesta de ajuste; 2020 excluido. Anterior de 2021: 2019. Respuestas entrenables desde 2021.
- 21 candidatos: persistencia; Ridge para H/I/D/HI/HD por alpha 0.1, 1, 10; árbol pequeño por esos cinco grupos. Orden exactamente el indicado. Scaler entrenado dentro de cada Pipeline independiente. Parámetros completos y defaults congelados antes de ajustes reales.
- Ridge: solver svd, fit_intercept True, copy_X True, positive False, max_iter None, tol 0.0001, random_state 20261010. Árbol: criterion absolute_error, max_depth 2, min_samples_leaf 11, random_state 20261010. Otros defaults del entorno exacto. StandardScaler copy/with_mean/with_std True.
- Evaluación: mismos 165 pares de 2021–2025. Externo 2021 fijo persistencia sin ajuste/selección. Internas acumuladas 2021 hasta externo-1 para externos 2022–2025: diez ventanas, con respaldos puntuados de 2021. Solo respuestas anteriores entrenan cada ventana; historia completa elegible.
- Selección: MAE <= mínimo+0.1; RMSE <= mínimo del pool+0.1; menor número de entradas; orden declarado. Histórico: persistencia y Ridge H. Ampliado: persistencia y Ridge H/HI/HD. Con pobreza: Ridge HI/HD. Selecciones cerradas antes de externas. Árbol e I/D exclusivamente diagnósticos.
- Primario: 100*(MAE_historico-MAE_ampliado)/MAE_historico, denominador positivo finito; meta >=5%. El denominador es el histórico de este experimento, diferente al contraste anterior. No elegir ganador externo ni rescatar primario con diagnósticos.
- Descriptivos: MAE/RMSE/sesgo/dirección por año y territorio; comparaciones de H con HI/HD al mismo alpha; árboles equivalentes; coeficientes y rangos observados. No p-valores confirmatorios ni escenarios.

## Ejecución única y controles

El envío expreso del PROMPT_NUEVA_SESION.md autorizará la ejecución pendiente con límite total nuevo de 7200 segundos desde la primera acción de esa sesión. La preparación actual queda cerrada y documentada separadamente; no se ha abierto un piloto ni existe saldo de ajustes que reusar. La lectura de archivos por sí sola no autoriza ejecución.

Preflight, conservación, entorno exacto, fuentes, controles inventados y congelación deben aprobar antes de ajustar. Un Pipeline por candidato/contexto; 200 ajustes originales y hasta doce repeticiones deduplicadas: máximo 212 sin fallos. Serial, ledger durable, terminación, un único retry total por infraestructura y ninguno numérico/de convergencia. Detener nuevos ajustes a 5400 segundos absolutos; cierre global a 7200. No reabrir piloto después de cerrarlo.

Auditor independiente sin fits, imports operativos ni deserialización: matrices/temporalidad/defaults/scaler/selección/reconstrucción de predicciones/cobertura/linaje/CSV/presupuesto/terminación. CSV exacto después de round-trip, entero/flotante cero equivalentes, rechazo de diferencia 1e-11; repeticiones atol 1e-10, rtol 0.

Ante fallo indispensable o tiempo/cobertura insuficientes: cierre incompleto con evidencia verificable y pendientes, sin meta ni síntesis dependiente. No rediseñar para mejorar métricas.

## Entrega

Notebook con fuente Python y generador, validado y realmente ejecutado, sin fits de análisis. Todas las cifras, tablas y figuras académicas originadas en sus celdas mediante funciones compartidas; huellas, revisión visual y EVIDENCIAS_TEXTO.csv. Texto final, informe técnico, hallazgos con impacto/alternativa/resolución, lecturas por página, aceptación, conservación, pendientes, manifiesto y continuidad propia.

Todos los años ya vistos: exploratorio, dependiente, sin confirmación independiente. Fuente local sin autenticación ni disponibilidad anticipada demostradas; hogares frente a estudiantes, colegio frente a residencia y agregación ecológica. Una mejora predictiva no demuestra efectos de reducción de pobreza. Recomendar qué falta justificar para considerar objetivo 4; no ejecutarlo.

Solo escribir dentro de esta carpeta y /tmp. No modificar originales, tesis ni cierres anteriores; no .git/commit/push/modelo final/nuevas fuentes/proyecciones/simulación/avance automático. PROMPT_NUEVA_SESION.md contiene las rutas, huellas y procedimientos concretos para ejecutar este plan.
