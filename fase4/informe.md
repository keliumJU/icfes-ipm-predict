# Fase 4 — contraste territorial, robustez y explicaciones

2026-10-09, America/Bogota. Resultados actuales; no reproducción de rankings históricos. Partida `9a22b8adc406423fa6829b75e77d7473deffe710`, Git limpio. Alcance exclusivo fase4. Diferencias frente a plan fase4 líneas87–104 documentadas antes de cálculos en decisiones_previas.md; prevalece protocolo v1.0. Se mantienen población198, promedio global recibido, filtros, Bogotá/2021, peso igual y predictores1/15/16. Selección59 archivada. No simulaciones ni push.

## Integridad y ejecución

resultados/preparacion.json verificó antes de ajustar todas las huellas del cierre3 y sus entradas, base SHA256 `609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866`, protocolo y artefactos. Python3.12.14 y todas las dependencias coinciden exactamente con fase3/resultados/preparacion.json y requirements.lock.txt; pip check aprobado. Entorno `/tmp/icfes-fase3-venv`, sklearn1.9.1, semilla20261008, un hilo. Se reutilizan funciones de fase3 sin escribir allí. Los dos notebooks se ejecutaron realmente en kernel aislado; ver verificacion_notebooks.json. El bloqueo inicial del kernel dentro del sandbox y advertencia de caché pip se conservan en incidencias_ejecucion.md; no son fallos de modelos.

## Transporte territorial

Protocolo §7: 33 grupos por cada ganador seleccionado, 128 filas de32 territorios de desarrollo para entrenar y4 filas del excluido para evaluar. Los99 ajustes mantuvieron hiperparámetros, no reseleccionaron y no usaron2023–2024. Los ganadores GBR actuales no llevan transformaciones; el constructor compartido conserva pipelines internos de entrenamiento si corresponde. Particiones.json guarda membresía, años y parámetros. Predicciones_territoriales.csv conserva396 predicciones/error firmado/absoluto/cuadrado; métricas por99 territorio-modelo y12 año-modelo, advertencias/fallos vacíos. No hubo clipping.

| id | especificacion | n | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- | --- |
| gradient_boosting_ambas_07 | ambas | 132 | 8.067691 | 10.276440 | -1.301338 | 0.620259 |
| gradient_boosting_ipm_02 | ipm | 132 | 9.316132 | 12.126201 | -0.498728 | 0.471248 |
| gradient_boosting_tasas_07 | tasas | 132 | 7.825903 | 10.015879 | -0.936268 | 0.639272 |


Tasas tiene MAE0.241788 menor que ambas en este diagnóstico; **no cambia el ganador global** `gradient_boosting_ambas_07` ni la reevaluación cerrada. Los hiperparámetros fueron seleccionados utilizando esos territorios en desarrollo: existe sesgo de selección y el contraste no es validación independiente. Transporta a un territorio excluido con años coetáneos disponibles; no mide transporte temporal ni anticipación. Comparar sus8.067691 puntos con6.345582 temporales no prueba deterioro por un mecanismo: cambian diseño y años.

Mayores errores territoriales (tabla completa permanece en metricas_territorio.csv):

| id | departamento | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- |
| gradient_boosting_ambas_07 | Choco | 26.213950 | 26.482544 | 26.213950 | -62.339731 |
| gradient_boosting_tasas_07 | Choco | 25.897702 | 26.200448 | 25.897702 | -60.997511 |
| gradient_boosting_ipm_02 | San Andres | 25.481143 | 26.309243 | 25.481143 | -45.677439 |
| gradient_boosting_ipm_02 | Bogota D.C. | 24.460876 | 24.586251 | -24.460876 | -97.301361 |
| gradient_boosting_ipm_02 | Choco | 24.314915 | 24.541547 | 24.314915 | -53.395215 |
| gradient_boosting_ambas_07 | San Andres | 22.595519 | 22.703115 | -22.595519 | -33.758517 |
| gradient_boosting_tasas_07 | San Andres | 22.414121 | 22.477295 | -22.414121 | -33.070491 |
| gradient_boosting_tasas_07 | Cauca | 14.119169 | 14.381300 | 14.119169 | -28.471226 |
| gradient_boosting_ambas_07 | Cauca | 13.670752 | 13.915772 | 13.670752 | -26.594117 |


Los R² territoriales se apoyan en solo cuatro años y pueden ser muy negativos con poca variación del resultado. No se omiten. La sensibilidad de la agregación al retirar de evaluación un grupo de errores es:

| id | min | max |
| --- | --- | --- |
| gradient_boosting_ambas_07 | 7.500620 | 8.251786 |
| gradient_boosting_ipm_02 | 8.810975 | 9.549194 |
| gradient_boosting_tasas_07 | 7.261159 | 8.024042 |


Estos rangos mantienen predicciones fijas; no son otros entrenamientos ni nuevas métricas para seleccionar. El retiro del entrenamiento se implementó en los33 grupos originales.

## Robustez de diferencias

2.000 remuestreos pareados por comparación, grupos completos de33 territorios, semilla20261008. Resultados exactos en bootstrap_resumen.csv y14.000 réplicas en bootstrap_replicas.csv. Cada territorio conserva cuatro años de desarrollo o dos años de reserva. Errores fijos, sin ajuste adicional. Diferencia a−b negativa favorece a bajo este procedimiento.

| contexto | a | b | delta_mae | percentil_2_5 | percentil_97_5 | replicas |
| --- | --- | --- | --- | --- | --- | --- |
| territorial_desarrollo | gradient_boosting_ipm_02 | gradient_boosting_tasas_07 | 1.490229 | 0.026352 | 3.191831 | 2000 |
| territorial_desarrollo | gradient_boosting_ipm_02 | gradient_boosting_ambas_07 | 1.248441 | -0.101604 | 2.819498 | 2000 |
| territorial_desarrollo | gradient_boosting_tasas_07 | gradient_boosting_ambas_07 | -0.241788 | -0.569529 | 0.045591 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | media | -8.558305 | -11.930379 | -5.464742 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | ols_ipm | -3.206676 | -5.669490 | -0.962579 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | ols_tasas | -1.810303 | -3.022922 | -0.568942 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | ols_ambas | -1.906531 | -3.166595 | -0.616960 | 2000 |


El rango condicional tasas−ambas [−0.569529,0.045591] cruza cero, al igual que IPM−ambas. La ventaja de tasas no es uniforme frente a la composición territorial remuestreada. Los rangos temporales del ganador frente a media/OLS son negativos, pero proceden de resultados cerrados, reserva previamente expuesta y años fijos; no establecen superioridad independiente. Los percentiles no incorporan incertidumbre de selección, ajuste, dependencia entre particiones, precisión IPM o transporte a años futuros. No hay p-valores ni intervalos i.i.d.

## Explicaciones y medición

Asociaciones exclusivamente de desarrollo, sin ponderación, sin ajuste causal ni selección de tasas. Entre territorios usa33 medias; dentro usa132 desviaciones de media territorial; doble centrado resta también la media de año y añade la media global. Base equilibrada33×4. Todas las asociaciones están conservadas:

| variable | r_entre_territorios | r_dentro_territorio | r_doble_centrado |
| --- | --- | --- | --- |
| ipm | -0.764626 | 0.116285 | -0.136136 |
| Analfabetismo | -0.693218 | 0.264018 | 0.039625 |
| Bajo logro educativo | -0.542565 | 0.306436 | -0.017072 |
| Barreras a servicios para cuidado de la primera infancia | -0.654116 | 0.059034 | -0.027972 |
| Inasistencia escolar | -0.526685 | -0.300279 | -0.017109 |
| Rezago escolar | -0.773640 | 0.339428 | -0.001334 |
| Trabajo infantil | 0.052394 | 0.288545 | 0.036772 |
| Desempleo de larga duracion | -0.367299 | -0.057091 | -0.080515 |
| Trabajo informal | -0.576601 | -0.085971 | -0.092883 |
| Barreras de acceso a servicios de salud | 0.154560 | 0.361362 | 0.067823 |
| Sin aseguramiento en salud | 0.146983 | -0.028985 | -0.203463 |
| Hacinamiento critico | -0.685957 | 0.138346 | 0.111031 |
| Inadecuada eliminacion de excretas | -0.818614 | -0.098374 | -0.011939 |
| Material inadecuado de paredes exteriores | -0.681153 | 0.021966 | 0.167310 |
| Material inadecuado de pisos | -0.545915 | -0.093014 | -0.008550 |
| Sin acceso a fuente de agua mejorada | -0.801567 | -0.150764 | -0.106031 |


IPM–puntaje: entre−0.764626, dentro+0.116285, doble centrado−0.136136. La fuerte asociación geográfica no se traslada al cambio dentro del territorio. Es evidencia descriptiva comprobada, no un efecto de pobreza ni una contradicción causal. Rezago escolar también difiere: entre−0.773640, dentro+0.339428, doble−0.001334. Los cambios comunes por año pueden alterar asociaciones, pero el doble centrado no identifica su origen ni controla toda confusión.

Coeficientes OLS congelados, por una desviación estándar del entrenamiento, en coeficientes_ols_congelados.csv. IPM solo−12.028504 y ambas−10.314072. El coeficiente no es aporte causal ni importancia del GBR. Correlaciones/pares y colinealidad.csv muestran número de condición1.000000/IPM,12.644109/tasas y30.647008/ambas, rango completo1/15/16. Mayor condición con ambas es límite de separación de contribuciones, no permiso para eliminar variables. Pares más correlacionados:

| a | b | r |
| --- | --- | --- |
| Inadecuada eliminacion de excretas | Sin acceso a fuente de agua mejorada | 0.864463 |
| ipm | Material inadecuado de pisos | 0.862642 |
| Bajo logro educativo | Trabajo informal | 0.843928 |
| Rezago escolar | Hacinamiento critico | 0.832479 |
| Barreras a servicios para cuidado de la primera infancia | Hacinamiento critico | 0.828379 |


Diagnostico_tamanos.csv: tamaños Saber190–79.542 registros por celda de desarrollo; correlación error absoluto/log tamaño−0.213624/ambas,−0.037864/IPM,−0.244992/tasas. Es asociación diagnóstica, no prueba de precisión de encuesta o representatividad. Se conserva peso igual; no se cambia estimando con ponderación.

Soporte_territorial.csv registra **126 valores fuera de rango marginal** de entrenamiento entre 4224 entradas evaluadas (sumadas sobre especificaciones). Las tasas repetidas entre ambas/tasas no son casos independientes. Resumen_soporte.csv identifica indicador/modelo; rangos marginales no garantizan soporte conjunto, ausencia de extrapolación del resultado ni intervalos de predicción. Se conservan casos y errores.

Las notas de medición de IPM (auditoria/evidencia/notas_ipm.csv, IPM_Departamentos A50–A53 e IPM_Variables_Departamento A864–A868; protocolo §8) advierten comparabilidad. Saber geografía del colegio e IPM hogares residentes son poblaciones distintas. Composición de examinados, precisión de encuesta y cambios de medición son hipótesis posibles, sin insumos aquí para cuantificar su influencia ni explicar causalmente2024. La procedencia local, regla aritmética global desconocida, pocos años y dependencia permanecen. No se releen PDFs ni se alteran evidencias históricas.

## Hallazgos: impacto, alternativa, decisión y comprobación

| Evidencia / problema material | Impacto | Alternativa verificable | Decisión y comprobación |
|---|---|---|---|
| metricas_agrupadas.csv: tasas mejora0.241788 frente a ambas | Desaconseja afirmar ventaja territorial universal del ganador | Comparación pareada con errores completos y bootstrap predefinido | Se ejecutó; rango cruza0; informar sin reselección |
| asociaciones_longitudinales.csv: IPM entre/dentro difieren | Explicación geográfica no justifica mecanismo longitudinal | Centrar por territorio y luego por año | Se ejecutó y verificó; reportar patrones diferenciados sin causalidad |
| pares_correlacion.csv y colinealidad.csv | Aportes aislados no separables de covariación | Correlaciones completas, SVD y OLS congelados | Se ejecutó; conservar especificaciones, no ablar ni atribuir importancia GBR |
| mayores_errores_territoriales.csv y soporte_territorial.csv | Heterogeneidad y límites de transporte | Conservar extremos; inspección por grupos/rangos | Se ejecutó; ninguna exclusión ni clipping; no causas territoriales inventadas |
| Sin precisiones IPM/composición individual validada; protocolo §8 | No se puede cuantificar incertidumbre de medición ni causa2024 | Diagnóstico de tamaños y notas locales, distinguir hipótesis | Comprobado alcance; límite visible, no control de fuga pendiente ni imputación |
| Selección previa y entrenamientos solapados | Remuestreo no es confirmación independiente | Dispersión condicional de errores fijos, sin p-valores | 14.000 réplicas verificadas; limita interpretación y no cambia ganador |

## Verificaciones y condición de avance

Verificacion.json: cobertura396 sin duplicados,33×4 por especificación,99 particiones completas, errores y métricas recalculados independientemente,14.000 réplicas reproducidas, asociaciones cotejadas, seis ajustes focales adicionales en dos controles (primer código fijo) reprodujeron12 predicciones por control con tolerancia1e−12, sin búsqueda. Notebooks validados nbformat y sin errores de celdas.192 archivos previos se conservan contra snapshot inicial, salvo continuidad intencional. Manifiesto_cierre.json fija huellas de entrega. No se ejecutó una segunda reproducción completa en copia; hay reproducción parcial y verificación concretas descritas.

No quedan controles indispensables activos de fase4. Sensibilidades de año, exclusión2021, ponderación/ablaciones del plan no se ejecutan porque cambian decisiones congeladas; no son resultados ausentes ocultados ni fallos. Límites históricos archivados siguen intactos. Avance solo con autorización nueva y definición prospectiva de escenarios, conservando objetivo/modelos/población y sin interpretación causal. Adopción editorial de tesis permanece externa.
