# Informe del objetivo 3: predicción del promedio departamental Saber 11 mediante indicadores de pobreza multidimensional

Versión revisada 1.1, 9 de octubre de 2026 (America/Bogota). Entrega local para revisión editorial del grupo. Resultados actuales de fases 3–4, con decisiones del protocolo v1.0 conservadas. Las cifras se muestran con seis decimales para cotejo y no implican precisión sustantiva equivalente. El anexo técnico independiente conserva IDs, ubicaciones exactas, versiones y controles de revisión.

## Resumen

Se estimó el promedio global Saber 11 de registros elegibles de grado 11 por departamento del colegio y año, usando indicadores de pobreza del mismo año. La base contiene 198 celdas de 33 territorios; el desarrollo se limitó a 2018, 2019, 2021 y 2022. La regla predefinida seleccionó Gradient Boosting con IPM y quince tasas, con MAE de selección de 6.332499 puntos. El modelo congelado alcanzó MAE de 6.345582 en la reevaluación conjunta de 2023–2024, años previamente expuestos: el error aumentó de 5.020614 en 2023 a 7.670549 en 2024, sin causa identificada. OLS con IPM obtuvo menor MAE que GBR con IPM; en diagnóstico territorial las tasas resultaron favorables frente a la combinación. La selección temporal, la reevaluación y el diagnóstico territorial son evidencias distintas. Las asociaciones entre territorios no identifican cambios dentro de ellos ni efectos causales. No se evaluó persistencia. Estas conclusiones están respaldadas por las Tablas 1 y 4–10 y las ubicaciones del anexo técnico.

## 1. Propósito y correspondencia con el objetivo 3

El alcance operativo del objetivo 3 consiste en estimar el promedio global Saber 11 de registros elegibles de grado 11 de cada departamento del colegio y año, a partir de la incidencia de pobreza multidimensional (IPM), sus quince tasas marginales o ambas entradas. La pregunta es predictiva y ecológica: determina el error con que esos indicadores departamentales permiten estimar el desempeño agregado. Las entradas corresponden al mismo año del resultado; por ello se trata de estimación contemporánea condicionada a su disponibilidad, no de anticipación de un año cuyos indicadores aún se desconocen. Esta formulación corresponde al protocolo v1.0, §§1–3; no se atribuye aquí una nueva redacción literal al objetivo de la tesis.

Se distinguen tres usos de la evidencia: las ventanas temporales de desarrollo sirven para seleccionar; la aplicación de artefactos congelados a 2023–2024 constituye reevaluación temporal de años previamente expuestos; el retiro de territorios completos de desarrollo es un diagnóstico de transporte territorial con selección previa de hiperparámetros. Ninguno identifica efectos de intervenciones. La pregunta del plan sobre superar la persistencia territorial **no fue evaluada**: las referencias ejecutadas fueron media constante y OLS. No se completa esa ausencia con una comparación inventada o un ajuste adicional (anexo técnico R1, F03-01; protocolo §§5–7; anexo técnico R1, F05-01).

## 2. Datos, población, cobertura y decisiones de calidad

La unidad analítica es territorio-año. La base validada contiene 198 celdas: 33 territorios en 2018, 2019, 2021, 2022, 2023 y 2024; incluye Bogotá y 2021, sin incorporar 2020 o 2025. Su denominador total es 2.984.199 registros, sin certificación de personas únicas. Se mantienen los filtros auditados: estudiante, exclusión de libertad S, seis puntajes disponibles y positivos, código de colegio y grado 11. No se agregó un filtro de calendario. Fuentes y ubicaciones exactas: anexo técnico R2; protocolo §1.

**Tabla 1. Muestra analítica por año.** Los mínimos y máximos corresponden a registros Saber elegibles por celda, no al tamaño de la encuesta IPM. Calculada por año a partir de los conteos de registros elegibles; anexo técnico R2. Desarrollo suma 132 celdas y reevaluación 66.

| anio | territorios | celdas | registros | min_registros | max_registros | uso |
| --- | --- | --- | --- | --- | --- | --- |
| 2018 | 33 | 33 | 478689 | 242 | 79542 | Desarrollo |
| 2019 | 33 | 33 | 495224 | 258 | 79304 | Desarrollo |
| 2021 | 33 | 33 | 494331 | 190 | 75610 | Desarrollo |
| 2022 | 33 | 33 | 497562 | 264 | 74538 | Desarrollo |
| 2023 | 33 | 33 | 516936 | 311 | 76048 | Reevaluación temporal expuesta |
| 2024 | 33 | 33 | 501457 | 224 | 73893 | Reevaluación temporal expuesta |

El resultado es la suma de puntajes globales individuales recibidos dividida por su denominador elegible dentro de cada celda, sin redondeo intermedio. La media responde al estimando de desempeño promedio; la mediana respondería a un centro por orden distinto. El usuario declaró que no comparó previamente media y mediana; no se afirma superioridad empírica de la media. Cada territorio-año pesa igual en ajuste y evaluación, aunque dentro de la celda cada registro contribuye por igual al promedio. El MAE resultante describe errores entre medias territoriales, no el error del estudiante nacional típico (protocolo §2; decisiones fase2 D01 y D08).

La auditoría anterior verificó 2.574 cotejos de agregación raw/final sin diferencias. Conservó 414 discrepancias aritméticas de grado 11 presentes en la fuente de 20222, sin reemplazar el global por una fórmula no autenticada. Estas son evidencias anteriores comprobadas en la auditoría, no nuevos censos ejecutados en la revisión. Ubicaciones: anexo técnico R2; protocolo §§1–2. La conservación de base, protocolo y entregables se verificó nuevamente en fase 6; controles y huellas constan en el anexo técnico.

El IPM y las tasas se enlazan por código departamental y año. La incidencia local se expresa como porcentaje de personas y las tasas como porcentajes de hogares. Las cinco dimensiones oficiales organizan documentalmente las quince tasas, sin construir índices de dimensión mediante promedios. La definición de privaciones y dimensiones se documenta en DANE, *Algoritmo para la construcción del IPM*, §§3–4.5, y en protocolo §3. El enlace es ecológico: la ubicación del colegio de quienes presentan Saber no coincide necesariamente con la población de hogares residentes sobre la que se mide pobreza (anexo técnico R2; protocolo §8).

Las notas locales IPM advierten expansión basada en CNPV2018, captura rural en 2021 y cambio de marco de agua rural 2019–2020. Se conservaron datos y años; no se corrigieron tasas para mejorar métricas. Esas advertencias limitan comparabilidad y no demuestran una causa de variaciones educativas (anexo técnico R2, hoja IPM_Departamentos A50–A53 e IPM_Variables_Departamento A864–A868; protocolo §8). La autenticación de descarga y la regla aritmética del global siguen sin establecerse: se valida la conservación de archivos locales, no una versión oficial de descarga no documentada.

## 3. Diseño predictivo y procedimiento de selección

**Tabla 2. Especificaciones congeladas.** Nombres exactos, orden y unidades: anexo técnico R3 y diccionario de base. La media es una referencia común con cero predictores, no tres medias distintas.

| Especificación | Entradas | Unidad local | Familias comparadas |
| --- | --- | --- | --- |
| IPM | 1 | Incidencia (% personas) | Media común; OLS; Ridge; RF; GBR |
| Tasas | 15 | Tasas marginales (% hogares) | Media común; OLS; Ridge; RF; GBR |
| Ambas | 16 | Incidencia y tasas | Media común; OLS; Ridge; RF; GBR |

Se excluyeron INSE, puntajes por asignatura, percentiles, derivados del resultado, identificadores, año y conteos como predictores. OLS y Ridge estandarizaron X exclusivamente dentro de cada entrenamiento; los árboles usaron porcentajes originales. No se aplicaron imputación, selección adicional de variables, PCA, recorte de predicciones ni otras transformaciones (protocolo §3; anexo técnico R3). La documentación de scikit-learn, §3.1, sustenta separar entrenamiento y validación y ajustar transformaciones dentro del entrenamiento; la implementación local de años completos es la fijada por el protocolo.

OLS denota mínimos cuadrados ordinarios; Ridge, regresión lineal regularizada; RF, Random Forest; GBR, Gradient Boosting de regresión. Se utilizaron tres ventanas expansivas: 2018→2019 (33→33 filas), 2018+2019→2021 (66→33) y 2018+2019+2021→2022 (99→33). No se fabricó 2020 ni se dividió aleatoriamente un año. Las 99 predicciones concatenadas por candidato definen métricas de selección. Los territorios repetidos y los tres años de validación no equivalen a 99 réplicas temporalmente independientes (protocolo §4; anexo técnico R3).

[Figura 1. Partición temporal — archivo separado](figuras/01_particion_temporal.png)

**Figura 1.** Diseño de selección y ajuste final/reevaluación; no es una figura de desempeño. Fuente: protocolo §4 y cardinalidades de la base; generación en anexo técnico R3. El ajuste final usa 132 filas hasta 2022; ambos años posteriores reciben el mismo modelo, sin actualización con 2023.

La búsqueda finita incluyó 67 candidatos: media, tres OLS, quince Ridge, veinticuatro RF y veinticuatro GBR. Ridge exploró alpha 0.1, 1, 10, 100 y 1000; RF mantuvo 300 árboles y combinó profundidad 2/4, hoja mínima 3/8 y fracción de entradas 0.5/1.0; GBR combinó 50/100 etapas, aprendizaje 0.03/0.1 y profundidad 1/2, con hoja mínima 3. La semilla fue 20261008, sin búsqueda de semillas. Se completaron 201 ajustes de ventanas sin fallos de modelos registrados. Parámetros íntegros, versiones y advertencias: anexo técnico R3. Python 3.12.14 y scikit-learn 1.9.1 corresponden al entorno de los ajustes ejecutados en fase 3, no a un entorno histórico reconstruido (anexo técnico R3).

El criterio principal fue MAE en puntos. Con error e=predicho−observado, MAE es la media de |e|, RMSE la raíz de la media de e² y sesgo la media de e; R² compara suma cuadrática de error con variación del observado. Se conservaron candidatos a no más de 0.1 puntos del MAE mínimo y, entre ellos, a no más de 0.1 del RMSE mínimo; después se prefirieron menos entradas, orden fijo de familia y primer ID de grilla. La tolerancia es una decisión prospectiva de parsimonia, no un umbral de relevancia educativa demostrado. Se exigieron las tres ventanas completas (protocolo §§5–6).

Los ganadores por especificación y las referencias se ajustaron en las 132 filas y congelaron antes de calcular errores de reserva, el 9 de octubre de 2026 (marca temporal exacta en anexo técnico R3). Siete artefactos, parámetros y huellas constan en anexo técnico R3. No se evaluaron los 67 candidatos en reserva para un segundo ranking. Las diferencias generales entre plan y procedimiento ejecutado —ausencia de persistencia, ElasticNet y XGBoost, grillas y desempates del protocolo— se registraron antes de resultados en anexo técnico R3, F03-01; este informe preserva esa referencia operativa.

## 4. Resultados comparativos y justificación del modelo

**Tabla 3. Mínimos brutos por familia en desarrollo.** Resumen descriptivo de la búsqueda existente; no constituye una nueva regla de selección. Fuente: 67 candidatos completos; mínimos por familia documentados en anexo técnico R4.

| familia | id | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- |
| gradient_boosting | gradient_boosting_ambas_07 | 6.332499 | 7.764136 | 3.297261 | 0.779915 |
| random_forest | random_forest_ambas_05 | 6.504996 | 8.327778 | 3.996810 | 0.746801 |
| ridge | ridge_tasas_02 | 7.074271 | 8.779615 | 3.285771 | 0.718580 |
| ols | ols_tasas | 7.693311 | 9.492374 | 3.002022 | 0.671032 |
| media | media | 13.842431 | 16.991914 | 2.833713 | -0.054116 |

**Tabla 4. Referencias y ganadores por especificación, métricas de selección.** Cada fila representa 99 predicciones de validación expansiva, con posibilidad de optimismo por selección. La tabla íntegra de candidatos, incluidos desempeños menos favorables, permanece en comparacion_desarrollo.csv, identificado en el anexo técnico R4.

| id | n_entradas | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- |
| media | 0 | 13.842431 | 16.991914 | 2.833713 | -0.054116 |
| ols_ipm | 1 | 9.580612 | 12.574850 | 5.467537 | 0.422690 |
| gradient_boosting_ipm_02 | 1 | 8.879188 | 11.378401 | 5.731344 | 0.527321 |
| ols_tasas | 15 | 7.693311 | 9.492374 | 3.002022 | 0.671032 |
| gradient_boosting_tasas_07 | 15 | 6.440524 | 7.899214 | 3.475862 | 0.772191 |
| ols_ambas | 16 | 8.740390 | 10.987150 | 4.052061 | 0.559269 |
| gradient_boosting_ambas_07 | 16 | 6.332499 | 7.764136 | 3.297261 | 0.779915 |

El ganador global conservado es GBR ambas, con 16 entradas, 100 etapas, aprendizaje 0.1, profundidad 2, hoja mínima 3 y subsample 1. Su MAE de selección fue 6.332499; el GBR tasas quedó 0.108025 puntos por encima, fuera de la banda prospectiva de 0.1, y no desplazó a ambas por parsimonia. Esta diferencia no identifica una contribución causal del IPM adicional ni establece relevancia educativa por sí misma (anexo técnico R4; Tabla 4). La elección se justifica por la regla predefinida, no por resultados posteriores.

**Tabla 5. Reevaluación temporal conjunta de 2023–2024.** Mismos siete modelos congelados hasta 2022, 66 filas por modelo. Fuente: métricas conjuntas; anexo técnico R4. Reserva previamente expuesta, no prueba inédita.

| id | n | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- |
| media | 66 | 14.903887 | 17.788017 | -5.290637 | -0.097048 |
| ols_ipm | 66 | 9.552257 | 12.149070 | -0.868937 | 0.488251 |
| gradient_boosting_ipm_02 | 66 | 9.768153 | 12.055652 | 0.078490 | 0.496091 |
| ols_tasas | 66 | 8.155885 | 9.728699 | -5.194448 | 0.671844 |
| gradient_boosting_tasas_07 | 66 | 6.436305 | 8.003991 | -2.922603 | 0.777882 |
| ols_ambas | 66 | 8.252112 | 9.754632 | -5.486928 | 0.670092 |
| gradient_boosting_ambas_07 | 66 | 6.345582 | 7.802886 | -2.779014 | 0.788903 |

**Tabla 6. Reevaluación anual y conjunta del ganador global.** Fuente: métricas del ganador GBR ambas; anexo técnico R4. El R² conjunto se calcula sobre las 66 filas, sin promediar R² anuales; RMSE es raíz del MSE concatenado.

| periodo | n | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- |
| 2023 | 33 | 5.020614 | 5.985372 | -1.756802 | 0.872020 |
| 2024 | 33 | 7.670549 | 9.270673 | -3.801227 | 0.703958 |
| conjunto | 66 | 6.345582 | 7.802886 | -2.779014 | 0.788903 |

Ninguna referencia media/OLS superó al ganador global en MAE en estos años. Sin embargo, **OLS IPM obtuvo menor MAE que GBR IPM** en 2023, 2024 y conjuntamente: las diferencias a favor de OLS fueron 0.128946, 0.302844 y 0.215895 puntos, respectivamente (filas de OLS IPM y GBR IPM documentadas en anexo técnico R4; Tabla 5). El hallazgo impide afirmar que la complejidad siempre mejora la predicción y se conserva sin reselección. En esa comparación conjunta GBR IPM tiene un RMSE ligeramente menor: la conclusión de ventaja OLS se refiere al MAE principal, no a todas las métricas.

El MAE del ganador aumentó de 5.020614 a 7.670549 y su sesgo pasó de −1.756802 a −3.801227, indicando mayor subestimación en 2024 (Tabla 6). El resultado se reporta como deterioro de error entre esos años; no se atribuye a composición, políticas, pandemia o medición sin evidencia que identifique tales causas. La inclusión de tasas proporciona mejores resultados observados que IPM solo entre estos ganadores, pero no garantiza ventaja en cualquier familia, año o territorio (Tablas 4–5).

[Figura 2. Observado frente a predicho por diseño — archivo separado](figuras/02_observado_predicho.png)

**Figura 2.** GBR ambas: izquierda, 99 predicciones de ventanas usadas para selección; centro, 66 predicciones de reevaluación 2023–2024 previamente expuesta; derecha, 132 predicciones del diagnóstico territorial con parámetros seleccionados previamente. La diagonal es igualdad observado=predicho. Fuentes: anexo técnico R4, mismo ID. Los paneles no representan una sola evaluación combinable.

La exposición previa de 2023–2024 está documentada por la auditoría anterior en `prom.pdf`, páginas físicas 13–14, 18 y 22, y `nueva ivestigacion .pdf`, páginas 5–7 (protocolo §7; continuidad, criterios de fase2). En esta revisión no se releen esos PDF ni se reproducen métricas históricas. Los resultados históricos de clasificación son reportados y no reproducidos; no se trasladan AUC, Brier o rankings históricos a esta regresión.

## 5. Diagnóstico de errores y robustez

El contraste territorial dejó fuera un territorio completo de desarrollo y ajustó cada ganador por especificación en los otros 32 territorios: 128 filas de entrenamiento y cuatro de evaluación. Hubo 99 ajustes y 396 predicciones existentes. Los parámetros ya habían sido seleccionados utilizando esos territorios en desarrollo: existe sesgo de selección, por lo que el diagnóstico no es una validación independiente. Usa años coetáneos en entrenamiento y responde al transporte a un territorio ausente, distinto de aplicar un modelo congelado a años posteriores de territorios conocidos (protocolo §7; anexo técnico R5).

**Tabla 7. Diagnóstico territorial agrupado.** 132 errores por especificación en 2018, 2019, 2021 y 2022. Fuente: anexo técnico R5.

| id | n | mae | rmse | sesgo | r2 |
| --- | --- | --- | --- | --- | --- |
| gradient_boosting_ambas_07 | 132 | 8.067691 | 10.276440 | -1.301338 | 0.620259 |
| gradient_boosting_ipm_02 | 132 | 9.316132 | 12.126201 | -0.498728 | 0.471248 |
| gradient_boosting_tasas_07 | 132 | 7.825903 | 10.015879 | -0.936268 | 0.639272 |

Tasas obtuvo MAE 7.825903 frente a 8.067691 de ambas, una ventaja puntual de 0.241788. Este resultado desfavorable a la ventaja territorial universal del ganador no cambia la selección global ni la reevaluación cerrada. El remuestreo pareado tasas−ambas dio percentiles [−0.569529; 0.045591], que cruzan cero: la dispersión condicional de la diferencia agregada incluye valores de ambos signos (Tabla 8). Tampoco comparar 8.067691 territorial con 6.345582 temporal identifica una causa del cambio: difieren diseños y años.

[Figura 3. Errores territoriales por evaluación — archivo separado](figuras/03_errores_territoriales.png)

**Figura 3.** MAE territorial del GBR ambas: izquierda, dos errores de reevaluación por territorio (2023–2024); derecha, cuatro errores del diagnóstico territorial por territorio (desarrollo). El orden usa MAE del panel derecho para facilitar lectura, sin exclusiones. Fuentes: anexo técnico R5, agrupación de |error|; anexo técnico R5. Ambas evaluaciones se mantienen separadas.

La heterogeneidad es sustantiva: en el diagnóstico territorial de ambas, Chocó presentó MAE 26.213950 con sesgo positivo y San Andrés 22.595519 con sesgo negativo. No se eliminaron esos territorios ni se recortaron predicciones. Los R² por territorio, calculados con cuatro filas, pueden ser muy negativos con poca variación del observado; no equivalen a estabilidad inferencial (anexo técnico R5, filas del ganador; anexo técnico R5). No se atribuyen causas territoriales a estos errores.

**Tabla 8. Remuestreo pareado existente.** Primeras tres filas: diagnóstico territorial de desarrollo; últimas cuatro: reevaluación temporal conjunta previamente expuesta. Diferencia MAE a−b; valores negativos favorecen a. Fuente: anexo técnico R5; 2.000 réplicas por comparación, 14.000 guardadas en anexo técnico R5, semilla 20261008. No se ejecuta remuestreo nuevo en esta revisión.

| contexto | a | b | delta_mae | percentil_2_5 | percentil_97_5 | replicas |
| --- | --- | --- | --- | --- | --- | --- |
| territorial_desarrollo | gradient_boosting_ipm_02 | gradient_boosting_tasas_07 | 1.490229 | 0.026352 | 3.191831 | 2000 |
| territorial_desarrollo | gradient_boosting_ipm_02 | gradient_boosting_ambas_07 | 1.248441 | -0.101604 | 2.819498 | 2000 |
| territorial_desarrollo | gradient_boosting_tasas_07 | gradient_boosting_ambas_07 | -0.241788 | -0.569529 | 0.045591 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | media | -8.558305 | -11.930379 | -5.464742 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | ols_ipm | -3.206676 | -5.669490 | -0.962579 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | ols_tasas | -1.810303 | -3.022922 | -0.568942 | 2000 |
| temporal_cerrado_2023_2024 | gradient_boosting_ambas_07 | ols_ambas | -1.906531 | -3.166595 | -0.616960 | 2000 |

Se remuestrearon 33 grupos territoriales completos, conservando los cuatro años de desarrollo o los dos de reserva y las predicciones fijas. Los percentiles describen dispersión condicional a esos errores, años y modelos. No incorporan selección de hiperparámetros, incertidumbre del ajuste, precisión de IPM, dependencia entre entrenamientos solapados o variación de años futuros. Los grupos tampoco prueban independencia espacial entre territorios. Los rangos temporales negativos frente a media/OLS son favorables bajo ese procedimiento, pero no convierten la reserva expuesta en confirmación independiente. No se reportan p-valores ni intervalos basados en observaciones independientes e idénticamente distribuidas (i.i.d.; anexo técnico R5, remuestreo y robustez).

**Tabla 9. Síntesis de robustez y alcance.** Ubicaciones completas en el anexo técnico, R5 y matriz de trazabilidad. Los rangos de omisión mantienen errores fijos y no son nuevos ajustes al excluir territorios.

| Diagnóstico | Resultado existente | Alcance | Fuente en fase4/resultados |
| --- | --- | --- | --- |
| Diferencia tasas−ambas territorial | −0.241788; percentiles [−0.569529; 0.045591] | Ventaja puntual de tasas; rango cruza cero | bootstrap_resumen.csv; territorial_desarrollo |
| Ganador−OLS IPM temporal | −3.206676; [−5.669490; −0.962579] | Dispersión condicional favorable; reserva expuesta | bootstrap_resumen.csv; temporal_cerrado_2023_2024 |
| Omitir errores de un territorio; ambas | MAE entre 7.500620 y 8.251786 | Influencia de composición con errores fijos | influencia_grupos_errores.csv; ambas |
| Soporte marginal territorial | 126 valores fuera de rango / 4224 entradas | No acredita soporte conjunto; tasas repetidas | soporte_territorial.csv; fase4/informe.md |
| Colinealidad | Condición 1 / 12.644109 / 30.647008 | Rango completo; separación de aportes limitada | colinealidad.csv; IPM/tasas/ambas |
| Tamaño de celda Saber desarrollo | 190–79542 registros | No mide precisión de la encuesta IPM | diagnostico_tamanos.csv |

**Tabla 10. Asociaciones descriptivas en desarrollo.** Entre territorios: correlación de 33 medias por territorio; dentro: correlación de 132 desviaciones de la media de cada territorio; doble centrado: resta adicional de medias anuales y restitución de media global en el panel equilibrado. Fuentes y procedimiento: anexo técnico R5. No se utilizan como nueva selección de predictores.

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

Para IPM, r entre territorios fue −0.764626, dentro +0.116285 y con doble centrado −0.136136. La asociación geográfica fuerte no se traslada al cambio dentro de cada territorio. El doble centrado elimina medias comunes de año, pero no determina su origen ni identifica un mecanismo. Rezago escolar también cambia de patrón (−0.773640, +0.339428, −0.001334; Tabla 10). La evidencia es compatible con diferencias importantes entre patrones geográficos y longitudinales; no permite cuantificar qué proporción de la capacidad predictiva procede de cada uno ni equiparar correlaciones a efectos.

[Figura 4. Estabilidad interpretativa descriptiva — archivo separado](figuras/04_estabilidad_interpretativa.png)

**Figura 4.** Solo desarrollo hasta 2022. Izquierda, asociaciones entre/dentro/doble centrado de Tabla 10. Derecha, coeficientes de OLS congelados por una desviación estándar del entrenamiento, comparados entre IPM, tasas y ambas; ausencia de punto indica que la variable no pertenece a esa especificación. Fuentes: anexo técnico R5. No son importancias del GBR, efectos causales ni una distribución remuestreada de coeficientes. La figura examina sensibilidad interpretativa al centrado y la especificación, sin nuevos ajustes.

La descomposición en valores singulares de las entradas centradas y escaladas, sin añadir una columna de intercepto, muestra rango completo 1/15/16, pero números de condición 1, 12.644109 y 30.647008 para IPM/tasas/ambas. La condición mayor en ambas indica menor separación numérica de direcciones de las entradas y es coherente con su covariación; no es por sí sola un umbral de invalidez ni una prueba de inestabilidad de cada coeficiente. La colinealidad limita interpretar contribuciones aisladas; no justifica eliminar entradas después de evaluar (anexo técnico R5). Los coeficientes OLS IPM por una DE fueron −12.028504 en IPM solo y −10.314072 en ambas: son asociaciones condicionales de modelos lineales, no importancia del modelo ganador (anexo técnico R5). La relación entre eliminación inadecuada de excretas y falta de agua mejorada fue r=0.864463 en desarrollo (anexo técnico R5, par correspondiente), otra evidencia de covariación, sin implicación causal.

## 6. Discusión, limitaciones y conclusión

El procedimiento seleccionado proporcionó menores errores que media/OLS globales en los resultados temporales cerrados, pero su ventaja no es universal: tasas fue favorable en transporte territorial y OLS superó a GBR con IPM solo en MAE reservado (Tablas 5–8). La elección global permanece sustentada por la selección prospectiva y no por corregir el ranking después. El MAE de selección de 6.332499 y el temporal conjunto de 6.345582 resumen conjuntos distintos; su proximidad no demuestra estabilidad anual ni ausencia de sesgo, pues 2024 presentó mayor error y subestimación (Tablas 4 y 6).

La base incluye registros elegibles, no a toda la juventud; colegio y residencia no son intercambiables. No se dispone aquí de composición individual validada ni precisión de encuesta IPM para cuantificar su influencia. Dependencia territorial, pocos años y entrenamientos solapados limitan inferencia y transporte. El soporte marginal contabilizó 126 entradas fuera del rango de entrenamiento entre 4.224 evaluadas, sumadas sobre especificaciones; tasas duplicadas entre tasas/ambas no son observaciones independientes. Estar dentro de rangos marginales tampoco garantiza soporte conjunto (anexo técnico R6, Medición).

Composición de examinados, cambios de medición y condiciones no incluidas son hipótesis posibles para estudiar posteriormente; no son causas comprobadas del deterioro de 2024. Las notas de comparabilidad, el enlace ecológico y la regla global desconocida deben acompañar la interpretación. La selección histórica de 59 columnas y la causa antigua del problema20212 permanecen archivadas porque la reconstrucción actual y su conservación no dependen de resolverlas; no se inventan criterios históricos ni se reabren sin evidencia relevante (continuidad, Salvedades; decisiones fase2 D10 y D13).

El resultado del objetivo 3 es un modelo global congelado para estimación agregada contemporánea, con desempeño, heterogeneidad y límites documentados. Se conserva evidencia desfavorable y no se afirma que reducir una privación cause una mejora educativa, que una intervención sea ineficaz o que el buen ajuste agregado describa mecanismos individuales. La comparación con persistencia sigue no evaluada, no pendiente de completar mediante ajuste en esta fase. La integración editorial en la tesis requiere revisión del grupo; este informe no acredita su adopción.

## 7. Puente metodológico al objetivo 4

El objetivo 3 aporta un esquema de entradas, transformaciones y modelo congelados, además de controles de integridad y límites de transporte. Un trabajo posterior sobre escenarios deberá contar con autorización expresa y definir de forma prospectiva la pregunta, la población, la disponibilidad contemporánea de indicadores, las entradas plausibles y la regla de soporte antes de calcular nuevas predicciones. Deberá conservar parámetros, escalas y huellas, comprobar unidades 0–100 y consistencia entre incidencia y privaciones; no podrá reconstruir IPM mediante promedios de tasas marginales ni suponer que una modificación aislada representa una población factible (protocolo §§1–3; DANE, algoritmo §3; anexo técnico R7, soporte).

La colinealidad y las diferencias entre asociaciones geográficas y longitudinales exigen evitar cambios arbitrarios de una variable mientras se supone que las demás son invariantes. Haría falta documentar coherencia conjunta y límites de extrapolación; el soporte marginal por sí solo no basta. Los percentiles del remuestreo de errores existente tampoco son intervalos de efectos o de escenarios. Cualquier diferencia entre predicciones bajo entradas hipotéticas se interpretaría, si se autorizara su cálculo, como contraste condicionado al modelo, sin identificar un efecto de intervención. La inferencia causal exigiría otra pregunta y evidencia que aquí no se ha producido. En esta entrega no se simulan escenarios, no se anticipan efectos ni se avanza a otro objetivo.

## 8. Referencias verificadas

Las fuentes siguientes son las efectivamente utilizadas. El registro de consulta y alcance está en el anexo técnico y en fase6/referencias_verificadas.md. Las referencias web se reconsultaron el 9 de octubre de 2026; no autentican la fecha o versión de descarga de datos locales.

1. DANE. *Índice de Pobreza Multidimensional, IPM 2023: materiales relacionados; Algoritmo para la construcción del IPM*. [Catálogo oficial y descripción del algoritmo](https://microdatos.dane.gov.co/index.php/catalog/824/related-materials), §§3 y 4.1–4.5 de la descripción. Sustenta organización y construcción de privaciones; no se extrapola su descripción histórica de representatividad a todos los años del panel. El catálogo no muestra fecha del algoritmo: no se inventa una.
2. scikit-learn. *Cross-validation: evaluating estimator performance*, documentación identificada como 1.9.1. [Sección 3.1](https://scikit-learn.org/stable/modules/cross_validation.html). Sustenta separación de entrenamiento/validación y control de transformaciones; el protocolo local define las ventanas por año completo.
3. scikit-learn. *GradientBoostingRegressor*, documentación identificada como 1.9.1. [Referencia de API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html). Sustenta significado de parámetros; su disponibilidad web no sustituye el registro local de versiones y parámetros.
4. Proyecto local. `protocolo/PROTOCOLO_OBJETIVO_3.md`, v1.0, 2026-10-08, §§1–8; `protocolo/decisiones_fase2.md`, D01–D14; `protocolo/fuentes/configuracion.py`. Son decisiones prospectivas y definición operativa, no criterios históricos recuperados.
5. Proyecto local. `auditoria/base_analitica_departamento_anio.csv`; `auditoria/diccionario_base_analitica.csv`; `auditoria/evidencia/actualizacion_20261008/` y `auditoria/evidencia/notas_ipm.csv`. Evidencia de construcción local y calidad, ubicaciones especificadas en §2.
6. Proyecto local. `fase3/informe.md`, `decisiones.md`, `README.md` y `resultados/` (2026-10-09). Tablas de selección/reevaluación y manifiesto congelado citados en §§3–4; versiones exactas en `fase3/requirements.lock.txt`.
7. Proyecto local. `fase4/informe.md`, `decisiones_previas.md`, `README.md` y `resultados/` (2026-10-09). Contraste territorial, asociaciones, coeficientes y remuestreo citados en §5.
8. Proyecto local. `CONTINUIDAD_OBJETIVO_3.md`, criterios de partida fase2 y cierres fases3–4; protocolo §7. Registro de exposición histórica en `prom.pdf` pp. físicas13–14,18,22 y `nueva ivestigacion .pdf` pp.5–7. Ubicaciones heredadas de la auditoría; no se afirma lectura nueva en fase6 ni autenticación bibliográfica de autores ausentes.
