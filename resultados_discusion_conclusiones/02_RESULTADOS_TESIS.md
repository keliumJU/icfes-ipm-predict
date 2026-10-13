# Síntesis de los resultados de la investigación

La investigación aporta evidencia descriptiva de una asociación negativa entre pobreza multidimensional y desempeño académico departamental, modelos que permiten estimar el puntaje con errores cuantificados y escenarios condicionales de alcance limitado. La asociación ajustada mediante efectos fijos permanece sin una entrega localizada; por tanto, la síntesis no presenta los cuatro objetivos como completamente resueltos.

## Población y periodos de los resultados

El núcleo descriptivo auditado contiene 198 observaciones de 33 territorios en 2018, 2019 y 2021–2024, y 2.984.199 registros elegibles de grado 11. La ampliación predictiva incluye 2025 y reúne 231 observaciones en siete años, sin incorporar 2020. No se atribuyen los descriptivos anteriores a una serie que ya incluya 2025. Los resultados corresponden al departamento del colegio y a medias globales recibidas; no constituyen seguimiento de personas únicas (E1 y E3).

## Objetivo 1 y evidencia descriptiva

Sobre las 198 celdas auditadas, la correlación entre IPM y puntaje global fue −0,722. Entre las medias de los 33 territorios fue −0,752. Ambos resultados muestran que los territorios con mayor pobreza tienden a registrar menor desempeño promedio, aunque responden a agregaciones distintas y no identifican causalidad (E1).

Las correlaciones con inadecuada eliminación de excretas, falta de acceso a agua mejorada y rezago escolar fueron −0,792, −0,786 y −0,687, respectivamente, sobre las 198 celdas. Son asociaciones de contexto; no permiten establecer que esas privaciones sean las causas principales del puntaje ni seleccionar automáticamente predictores para una prueba temporal. Las tasas están relacionadas entre sí y describen poblaciones agregadas (E1).

La correlación entre cambios de IPM y puntaje global de 2018 a 2024 fue −0,077 para los 33 territorios. Esta comparación de extremos no reproduce un modelo longitudinal completo. No permite concluir que la asociación interna sea inexistente ni que las políticas de reducción de pobreza carezcan de efectos educativos (E1).

El capítulo descriptivo existente cubre IPM, dimensiones, indicadores y desempeño, pero conserva correcciones editoriales y cifras complementarias pendientes de consolidación. La tabla histórica de 160 celdas y geografía de presentación no debe atribuirse a la construcción auditada de 198 celdas con geografía del colegio. La propuesta de corrección mantiene Bogotá y 2021 y distingue ambas construcciones (E2).

## Objetivo 2 y asociación ajustada

El método escrito propone efectos fijos de departamento y año, asociación contemporánea y rezagada e incertidumbre apropiada. No se localizó una entrega verificable de esa estimación dentro del alcance revisado. Esto es una ausencia de evidencia localizada, no un resultado nulo ni una prueba de inexistencia absoluta.

No se dispone, por tanto, de un coeficiente ajustado y su intervalo de incertidumbre para responder completamente la segunda pregunta. H1 y H2 no se consideran contrastadas con las correlaciones ni con el desempeño de los modelos predictivos. La entrega pendiente debe localizarse o el alcance debe conciliarse explícitamente antes de declarar completo ese objetivo (E2; ACA2, pp.25–26 y 56–57).

## Objetivo 3 y evolución de los modelos

### Modelo de pobreza de 2018 a 2024

El informe fase 6 documentó un modelo Gradient Boosting con IPM y quince tasas seleccionado con desarrollo hasta 2022. En las 66 observaciones de 2023–2024 obtuvo MAE de 6,346 y RMSE de 7,803 puntos. El MAE fue 5,021 en 2023 y 7,671 en 2024: el error aumentó, sin causa identificada. La persistencia no se evaluó en ese ejercicio, por lo que no se inventa una comparación posterior dentro de su informe (E6, tablas 5–6).

### Contraste posterior frente a historia

La consolidación posterior comparó 165 pares evaluados de 2021–2025 bajo procedimientos distintos del modelo fase 6. En esa muestra, el modelo ampliado con pobreza obtuvo MAE de 4,880, la persistencia 3,429 y la selección basada en historia 3,365. La diferencia entre historia y persistencia fue pequeña y no se estableció su relevancia educativa. Las cifras describen esa evaluación; no constituyen una progresión homogénea desde el MAE de fase 6 porque cambian procedimientos y años (E7).

### Diseño focal conectado con la metodología

Para completar la comparación prevista en la página 58 y disponer de un modelo apto para escenarios de IPM, se ejecutó un diseño con composición y tiempo, una extensión con IPM y otra con cinco contribuciones dimensionales y quince tasas. Se emplearon Ridge, Lasso y ElasticNet, con selección exclusivamente dentro del desarrollo. Los datos conservaron conteos y medias auditadas; las proporciones de composición y los niveles de Matemáticas se verificaron contra las fuentes locales (E3).

El diseño adoptó una tendencia temporal y un indicador de 2021, adaptación documentada de los efectos de año para estimar años posteriores. En entrenamiento hasta 2023 y evaluación 2024–2025, el MAE fue 12,538 para base, 9,704 para IPM y 8,479 para componentes. La incorporación de pobreza mejoró respecto a esa base, pero no superó el promedio territorial de 7,405 ni la persistencia de 3,103 (E3).

Estos resultados distinguen dos funciones: estimar con el menor error posible y construir una comparación condicional que responda al IPM. La referencia exclusivamente histórica puede ser útil para la primera, pero no para la segunda. El modelo auxiliar de IPM no se presenta como el mejor predictor.

## Objetivo 4 y escenarios

La validación mantiene separados los cortes hasta 2022/evaluación 2023–2024 y hasta 2023/evaluación 2024–2025. Se añadieron selección territorial anidada, respuesta alternativa de Matemáticas y exclusión de 2021 del desarrollo. Los resultados son retrospectivos y exploratorios porque los años ya habían sido vistos en investigaciones anteriores y las entradas del año evaluado son contemporáneas (E3 y E4).

Se revisaron 165 propuestas: referencia, reducciones de 1, 3 y 5 puntos porcentuales de IPM y convergencia a la mediana departamental de 13,0. Solo tres reducciones efectivas de 1 punto superaron soporte: Meta, Sucre y Tolima. Cada una produjo una diferencia de +0,574 puntos entre predicciones del modelo auxiliar. Las 13 admisiones totales incluyen además seis referencias y cuatro entradas de convergencia sin modificación; las 152 restantes fueron rechazadas. No hubo convergencia efectiva ni reducciones 3/5 puntos admitidas (E5).

## Respuesta que permiten los resultados

La evidencia muestra una asociación descriptiva negativa y un aporte predictivo relativo de pobreza frente a la base del diseño focal. También muestra que la historia reciente del puntaje ofrece menor error en las comparaciones ampliadas. Esta combinación no prueba causalidad ni ausencia de relación social: indica que asociación y utilidad predictiva incremental son preguntas diferentes.

La respuesta a la pregunta general es todavía parcial respecto a la asociación ajustada. H1/H2 siguen sin contraste localizado; H3 conserva un resultado exploratorio de reducción del error frente a una base temporal adaptada, sin confirmación de significación bajo la especificación original. El cierre académico requiere conciliar estos límites y los periodos de los capítulos, además de las correcciones descriptivas pendientes (E2 y E3).

## Fuentes de resultados

Fuente: E1, auditoria/evidencia/resumen_tesis.json y actualizacion_20261008/tabla12_propuesta_198.csv; E2, revision_cumplimiento_objetivos_20261012/REVISION_CUATRO_OBJETIVOS.md y auditoria/propuesta_correccion_tesis.md; E3–E5, objetivo4_validacion_escenarios/resultados; E6, fase6/entrega/informe_objetivo_3_revisado.md, tablas 5–6; E7, entrega_objetivos3_4_final/objetivo3/tablas/metricas_comparables.csv. Registro detallado: EVIDENCIAS_Y_REFERENCIAS.md.
