# Informe del objetivo 3: predicción del promedio departamental Saber 11 mediante indicadores de pobreza multidimensional

Versión de redacción 1.0, 9 de octubre de 2026 (America/Bogota). Fase 5 exclusivamente. Commit de partida: `da48e1a4f85d206e8753fbad85b78ba2e3858b1a`. Este informe integra resultados actuales ya ejecutados y congelados de fases 3–4; no constituye un nuevo entrenamiento o una nueva selección. Las cifras se presentan con seis decimales para trazabilidad; esa precisión de representación no implica precisión sustantiva equivalente. Las diferencias respecto del plan se documentaron antes de redactar en `fase5/decisiones_previas.md`.

## 1. Propósito y correspondencia con el objetivo 3

El alcance operativo del objetivo 3 consiste en estimar el promedio global Saber 11 de registros elegibles de grado 11 de cada departamento del colegio y año, a partir de la incidencia de pobreza multidimensional (IPM), sus quince tasas marginales o ambas entradas. La pregunta es predictiva y ecológica: determina el error con que esos indicadores departamentales permiten estimar el desempeño agregado. Las entradas corresponden al mismo año del resultado; por ello se trata de estimación contemporánea condicionada a su disponibilidad, no de anticipación de un año cuyos indicadores aún se desconocen. Esta formulación corresponde al protocolo v1.0, §§1–3; no se atribuye aquí una nueva redacción literal al objetivo de la tesis.

Se distinguen tres usos de la evidencia: las ventanas temporales de desarrollo sirven para seleccionar; la aplicación de artefactos congelados a 2023–2024 constituye reevaluación temporal de años previamente expuestos; el retiro de territorios completos de desarrollo es un diagnóstico de transporte territorial con selección previa de hiperparámetros. Ninguno identifica efectos de intervenciones. La pregunta del plan sobre superar la persistencia territorial **no fue evaluada**: las referencias ejecutadas fueron media constante y OLS. No se completa esa ausencia con una comparación inventada o un ajuste adicional (`fase3/decisiones.md`, F03-01; protocolo §§5–7; `fase5/decisiones_previas.md`, F05-01).

## 2. Datos, población, cobertura y decisiones de calidad

La unidad analítica es territorio-año. La base validada contiene 198 celdas: 33 territorios en 2018, 2019, 2021, 2022, 2023 y 2024; incluye Bogotá y 2021, sin incorporar 2020 o 2025. Su denominador total es 2.984.199 registros, sin certificación de personas únicas. Se mantienen los filtros auditados: estudiante, exclusión de libertad S, seis puntajes disponibles y positivos, código de colegio y grado 11. No se agregó un filtro de calendario. Fuente: `auditoria/base_analitica_departamento_anio.csv`; protocolo §1; `auditoria/evidencia/actualizacion_20261008/filtros_raw.csv` y `calendarios_raw.csv`.

**Tabla 1. Muestra analítica por año.** Los mínimos y máximos corresponden a registros Saber elegibles por celda, no al tamaño de la encuesta IPM. Procedimiento de cálculo: `fase5/fuentes/documentar.py`, agrupación por `anio` y suma de `n_estudiantes_saber`; salida `fase5/resultados/tabla_muestra.csv`. Desarrollo suma 132 celdas y reevaluación 66.

{{MUESTRA}}

El resultado es la suma de puntajes globales individuales recibidos dividida por su denominador elegible dentro de cada celda, sin redondeo intermedio. La media responde al estimando de desempeño promedio; la mediana respondería a un centro por orden distinto. El usuario declaró que no comparó previamente media y mediana; no se afirma superioridad empírica de la media. Cada territorio-año pesa igual en ajuste y evaluación, aunque dentro de la celda cada registro contribuye por igual al promedio. El MAE resultante describe errores entre medias territoriales, no el error del estudiante nacional típico (protocolo §2; decisiones fase2 D01 y D08).

La auditoría anterior verificó 2.574 cotejos de agregación raw/final sin diferencias. Conservó 414 discrepancias aritméticas de grado 11 presentes en la fuente de 20222, sin reemplazar el global por una fórmula no autenticada. Estas son evidencias anteriores comprobadas en la auditoría, no nuevos censos ejecutados en fase 5. Ubicaciones: `auditoria/evidencia/actualizacion_20261008/cotejo_agregacion_raw_final.csv`, `formula20222_raw.csv`; protocolo §§1–2. En esta fase se cotejó la huella SHA256 de la base, `609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866`, y los manifiestos de entregables, sin alterar originales (`fase5/resultados/integridad_inicial.json`).

El IPM y las tasas se enlazan por código departamental y año. La incidencia local se expresa como porcentaje de personas y las tasas como porcentajes de hogares. Las cinco dimensiones oficiales organizan documentalmente las quince tasas, sin construir índices de dimensión mediante promedios. La definición de privaciones y dimensiones se documenta en DANE, *Algoritmo para la construcción del IPM*, §§3–4.5, y en protocolo §3. El enlace es ecológico: la ubicación del colegio de quienes presentan Saber no coincide necesariamente con la población de hogares residentes sobre la que se mide pobreza (`auditoria/diccionario_base_analitica.csv`; protocolo §8).

Las notas locales IPM advierten expansión basada en CNPV2018, captura rural en 2021 y cambio de marco de agua rural 2019–2020. Se conservaron datos y años; no se corrigieron tasas para mejorar métricas. Esas advertencias limitan comparabilidad y no demuestran una causa de variaciones educativas (`auditoria/evidencia/notas_ipm.csv`, hoja IPM_Departamentos A50–A53 e IPM_Variables_Departamento A864–A868; protocolo §8). La autenticación de descarga y la regla aritmética del global siguen sin establecerse: se valida la conservación de archivos locales, no una versión oficial de descarga no documentada.

## 3. Diseño predictivo y procedimiento de selección

**Tabla 2. Especificaciones congeladas.** Nombres exactos y orden de entradas: `protocolo/fuentes/configuracion.py`, `ESPECIFICACIONES`; diccionario de base. La media es una referencia común con cero predictores, no tres medias distintas.

{{ESPEC}}

Se excluyeron INSE, puntajes por asignatura, percentiles, derivados del resultado, identificadores, año y conteos como predictores. OLS y Ridge estandarizaron X exclusivamente dentro de cada entrenamiento; los árboles usaron porcentajes originales. No se aplicaron imputación, selección adicional de variables, PCA, recorte de predicciones ni otras transformaciones (protocolo §3; `fase3/resultados/preparacion.json`). La documentación de scikit-learn, §3.1, sustenta separar entrenamiento y validación y ajustar transformaciones dentro del entrenamiento; la implementación local de años completos es la fijada por el protocolo.

Se utilizaron tres ventanas expansivas: 2018→2019 (33→33 filas), 2018+2019→2021 (66→33) y 2018+2019+2021→2022 (99→33). No se fabricó 2020 ni se dividió aleatoriamente un año. Las 99 predicciones concatenadas por candidato definen métricas de selección. Los territorios repetidos y los tres años de validación no equivalen a 99 réplicas temporalmente independientes (protocolo §4; `fase3/resultados/metricas_ventanas.csv`).

![Figura 1. Partición temporal](fase5/figuras/01_particion_temporal.png)

**Figura 1.** Diseño de selección y ajuste final/reevaluación; no es una figura de desempeño. Fuente: protocolo §4 y cardinalidades de la base; generación en `fase5/fuentes/documentar.py`. El ajuste final usa 132 filas hasta 2022; ambos años posteriores reciben el mismo modelo, sin actualización con 2023.

La búsqueda finita incluyó 67 candidatos: media, tres OLS, quince Ridge, veinticuatro RF y veinticuatro GBR. Ridge exploró alpha 0.1, 1, 10, 100 y 1000; RF mantuvo 300 árboles y combinó profundidad 2/4, hoja mínima 3/8 y fracción de entradas 0.5/1.0; GBR combinó 50/100 etapas, aprendizaje 0.03/0.1 y profundidad 1/2, con hoja mínima 3. La semilla fue 20261008, sin búsqueda de semillas. Se completaron 201 ajustes de ventanas sin fallos de modelos registrados. Parámetros íntegros, versiones y advertencias: `protocolo/evidencia/candidatos_congelados.json`, `fase3/resultados/preparacion.json`, `fallos.json` y `advertencias_desarrollo.json`. Python 3.12.14 y scikit-learn 1.9.1 corresponden al entorno actual de ejecución, no a un entorno histórico reconstruido (`fase3/requirements.lock.txt`).

El criterio principal fue MAE en puntos. Con error e=predicho−observado, MAE es la media de |e|, RMSE la raíz de la media de e² y sesgo la media de e; R² compara suma cuadrática de error con variación del observado. Se conservaron candidatos a no más de 0.1 puntos del MAE mínimo y, entre ellos, a no más de 0.1 del RMSE mínimo; después se prefirieron menos entradas, orden fijo de familia y primer ID de grilla. La tolerancia es una decisión prospectiva de parsimonia, no un umbral de relevancia educativa demostrado. Se exigieron las tres ventanas completas (protocolo §§5–6).

Los ganadores por especificación y las referencias se ajustaron en las 132 filas y congelaron antes de calcular errores de reserva, a `2026-10-09T15:20:08.821292+00:00`. Siete artefactos, parámetros y huellas constan en `fase3/resultados/congelacion.json`. No se evaluaron los 67 candidatos en reserva para un segundo ranking. Las diferencias generales entre plan y procedimiento ejecutado —ausencia de persistencia, ElasticNet y XGBoost, grillas y desempates del protocolo— se registraron antes de resultados en `fase3/decisiones.md`, F03-01; este informe preserva esa referencia operativa.

## 4. Resultados comparativos y justificación del modelo

**Tabla 3. Mínimos brutos por familia en desarrollo.** Resumen descriptivo de la búsqueda existente; no constituye una nueva regla de selección. Fuente: `fase3/resultados/comparacion_desarrollo.csv`, 67 candidatos completos; cálculo de mínimos por familia en `fase5/fuentes/documentar.py`.

{{FAMILIAS}}

**Tabla 4. Referencias y ganadores por especificación, métricas de selección.** Cada fila representa 99 predicciones de validación expansiva, con posibilidad de optimismo por selección. La tabla íntegra de candidatos, incluidos desempeños menos favorables, permanece en el archivo anterior.

{{SELECCION}}

El ganador global conservado es `gradient_boosting_ambas_07`, con 16 entradas, 100 etapas, aprendizaje 0.1, profundidad 2, hoja mínima 3 y subsample 1. Su MAE de selección fue 6.332499; el GBR tasas quedó 0.108025 puntos por encima, fuera de la banda prospectiva de 0.1, y no desplazó a ambas por parsimonia. Esta diferencia no identifica una contribución causal del IPM adicional ni establece relevancia educativa por sí misma (`fase3/resultados/congelacion.json`; Tabla 4). La elección se justifica por la regla predefinida, no por resultados posteriores.

**Tabla 5. Reevaluación temporal conjunta de 2023–2024.** Mismos siete modelos congelados hasta 2022, 66 filas por modelo. Fuente: `fase3/resultados/metricas_reevaluacion.csv`, `periodo=conjunto`. Reserva previamente expuesta, no prueba inédita.

{{RESERVA}}

**Tabla 6. Reevaluación anual y conjunta del ganador global.** Fuente: mismo archivo, `id=gradient_boosting_ambas_07`. El R² conjunto se calcula sobre las 66 filas, sin promediar R² anuales; RMSE es raíz del MSE concatenado.

{{ANUAL}}

Ninguna referencia media/OLS superó al ganador global en MAE en estos años. Sin embargo, **OLS IPM obtuvo menor MAE que GBR IPM** en 2023, 2024 y conjuntamente: las diferencias a favor de OLS fueron 0.128946, 0.302844 y 0.215895 puntos, respectivamente (filas `ols_ipm` y `gradient_boosting_ipm_02` de `metricas_reevaluacion.csv`; Tabla 5). El hallazgo impide afirmar que la complejidad siempre mejora la predicción y se conserva sin reselección. En esa comparación conjunta GBR IPM tiene un RMSE ligeramente menor: la conclusión de ventaja OLS se refiere al MAE principal, no a todas las métricas.

El MAE del ganador aumentó de 5.020614 a 7.670549 y su sesgo pasó de −1.756802 a −3.801227, indicando mayor subestimación en 2024 (Tabla 6). El resultado se reporta como deterioro de error entre esos años; no se atribuye a composición, políticas, pandemia o medición sin evidencia que identifique tales causas. La inclusión de tasas proporciona mejores resultados observados que IPM solo entre estos ganadores, pero no garantiza ventaja en cualquier familia, año o territorio (Tablas 4–5).

![Figura 2. Observado frente a predicho por diseño](fase5/figuras/02_observado_predicho.png)

**Figura 2.** GBR ambas: izquierda, 99 predicciones de ventanas usadas para selección; centro, 66 predicciones de reevaluación 2023–2024 previamente expuesta; derecha, 132 predicciones del diagnóstico territorial con parámetros seleccionados previamente. La diagonal es igualdad observado=predicho. Fuentes: `fase3/resultados/predicciones_desarrollo.csv`, `predicciones_reevaluacion.csv` y `fase4/resultados/predicciones_territoriales.csv`, mismo ID. Los paneles no representan una sola evaluación combinable.

La exposición previa de 2023–2024 está documentada por la auditoría anterior en `prom.pdf`, páginas físicas 13–14, 18 y 22, y `nueva ivestigacion .pdf`, páginas 5–7 (protocolo §7; continuidad, criterios de fase2). En fase 5 no se releen esos PDF ni se reproducen métricas históricas. Los resultados históricos de clasificación son reportados y no reproducidos; no se trasladan AUC, Brier o rankings históricos a esta regresión.

## 5. Diagnóstico de errores y robustez

El contraste territorial dejó fuera un territorio completo de desarrollo y ajustó cada ganador por especificación en los otros 32 territorios: 128 filas de entrenamiento y cuatro de evaluación. Hubo 99 ajustes y 396 predicciones existentes. Los parámetros ya habían sido seleccionados utilizando esos territorios en desarrollo: existe sesgo de selección, por lo que el diagnóstico no es una validación independiente. Usa años coetáneos en entrenamiento y responde al transporte a un territorio ausente, distinto de aplicar un modelo congelado a años posteriores de territorios conocidos (protocolo §7; `fase4/resultados/particiones.json`; `fase4/informe.md`).

**Tabla 7. Diagnóstico territorial agrupado.** 132 errores por especificación en 2018, 2019, 2021 y 2022. Fuente: `fase4/resultados/metricas_agrupadas.csv`.

{{TERRITORIAL}}

Tasas obtuvo MAE 7.825903 frente a 8.067691 de ambas, una ventaja puntual de 0.241788. Este resultado desfavorable a la ventaja territorial universal del ganador no cambia la selección global ni la reevaluación cerrada. El remuestreo pareado tasas−ambas dio percentiles [−0.569529; 0.045591], que cruzan cero: la ventaja no es uniforme respecto de la composición territorial remuestreada (Tabla 8). Tampoco comparar 8.067691 territorial con 6.345582 temporal identifica una causa del cambio: difieren diseños y años.

![Figura 3. Errores territoriales por evaluación](fase5/figuras/03_errores_territoriales.png)

**Figura 3.** MAE territorial del GBR ambas: izquierda, dos errores de reevaluación por territorio (2023–2024); derecha, cuatro errores del diagnóstico territorial por territorio (desarrollo). El orden usa MAE del panel derecho para facilitar lectura, sin exclusiones. Fuentes: `fase3/resultados/predicciones_reevaluacion.csv`, agrupación de |error|; `fase4/resultados/metricas_territorio.csv`. Ambas evaluaciones se mantienen separadas.

La heterogeneidad es sustantiva: en el diagnóstico territorial de ambas, Chocó presentó MAE 26.213950 con sesgo positivo y San Andrés 22.595519 con sesgo negativo. No se eliminaron esos territorios ni se recortaron predicciones. Los R² por territorio, calculados con cuatro filas, pueden ser muy negativos con poca variación del observado; no equivalen a estabilidad inferencial (`fase4/resultados/metricas_territorio.csv`, filas del ganador; `mayores_errores_territoriales.csv`). No se atribuyen causas territoriales a estos errores.

**Tabla 8. Remuestreo pareado existente.** Diferencia MAE a−b; valores negativos favorecen a. Fuente: `fase4/resultados/bootstrap_resumen.csv`; 2.000 réplicas por comparación, 14.000 guardadas en `bootstrap_replicas.csv`, semilla 20261008. No se ejecuta remuestreo nuevo en fase 5.

{{BOOT}}

Se remuestrearon 33 grupos territoriales completos, conservando los cuatro años de desarrollo o los dos de reserva y las predicciones fijas. Los percentiles describen dispersión condicional a esos errores, años y modelos. No incorporan selección de hiperparámetros, incertidumbre del ajuste, precisión de IPM, dependencia entre entrenamientos solapados o variación de años futuros. Los grupos tampoco prueban independencia espacial entre territorios. Los rangos temporales negativos frente a media/OLS son favorables bajo ese procedimiento, pero no convierten la reserva expuesta en confirmación independiente. No se reportan p-valores ni intervalos i.i.d. (`fase4/decisiones_previas.md`, remuestreo; `fase4/informe.md`, Robustez).

**Tabla 9. Síntesis de robustez y alcance.** Ubicaciones completas en la última columna, relativas a `fase4/resultados/`. Los rangos de omisión mantienen errores fijos y no son nuevos ajustes al excluir territorios.

{{ROBUST}}

**Tabla 10. Asociaciones descriptivas en desarrollo.** Entre territorios: correlación de 33 medias por territorio; dentro: correlación de 132 desviaciones de la media de cada territorio; doble centrado: resta adicional de medias anuales y restitución de media global en el panel equilibrado. Fuente: `fase4/resultados/asociaciones_longitudinales.csv`; procedimiento `fase4/fuentes/analisis.py`. No se utilizan como nueva selección de predictores.

{{ASOC}}

Para IPM, r entre territorios fue −0.764626, dentro +0.116285 y con doble centrado −0.136136. La asociación geográfica fuerte no se traslada al cambio dentro de cada territorio. El doble centrado elimina medias comunes de año, pero no determina su origen ni identifica un mecanismo. Rezago escolar también cambia de patrón (−0.773640, +0.339428, −0.001334; Tabla 10). La evidencia es compatible con diferencias importantes entre patrones geográficos y longitudinales; no permite cuantificar qué proporción de la capacidad predictiva procede de cada uno ni equiparar correlaciones a efectos.

![Figura 4. Estabilidad interpretativa descriptiva](fase5/figuras/04_estabilidad_interpretativa.png)

**Figura 4.** Solo desarrollo hasta 2022. Izquierda, asociaciones entre/dentro/doble centrado de Tabla 10. Derecha, coeficientes de OLS congelados por una desviación estándar del entrenamiento, comparados entre IPM, tasas y ambas; ausencia de punto indica que la variable no pertenece a esa especificación. Fuentes: `fase4/resultados/asociaciones_longitudinales.csv` y `coeficientes_ols_congelados.csv`. No son importancias del GBR, efectos causales ni una distribución remuestreada de coeficientes. La figura examina sensibilidad interpretativa al centrado y la especificación, sin nuevos ajustes.

Las matrices estandarizadas tienen rango completo 1/15/16, pero números de condición 1, 12.644109 y 30.647008 para IPM/tasas/ambas. Esto muestra mayor colinealidad en ambas y limita separar contribuciones aisladas; no justifica eliminar entradas después de evaluar (`fase4/resultados/colinealidad.csv`). Los coeficientes OLS IPM por una DE fueron −12.028504 en IPM solo y −10.314072 en ambas: son asociaciones condicionales de modelos lineales, no importancia del modelo ganador (`coeficientes_ols_congelados.csv`). La relación entre eliminación inadecuada de excretas y falta de agua mejorada fue r=0.864463 en desarrollo (`pares_correlacion.csv`, par correspondiente), otra evidencia de covariación, sin implicación causal.

## 6. Discusión, limitaciones y conclusión

El procedimiento seleccionado proporcionó menores errores que media/OLS globales en los resultados temporales cerrados, pero su ventaja no es universal: tasas fue favorable en transporte territorial y OLS superó a GBR con IPM solo en MAE reservado (Tablas 5–8). La elección global permanece sustentada por la selección prospectiva y no por corregir el ranking después. El MAE de selección de 6.332499 y el temporal conjunto de 6.345582 resumen conjuntos distintos; su proximidad no demuestra estabilidad anual ni ausencia de sesgo, pues 2024 presentó mayor error y subestimación (Tablas 4 y 6).

La base incluye registros elegibles, no a toda la juventud; colegio y residencia no son intercambiables. No se dispone aquí de composición individual validada ni precisión de encuesta IPM para cuantificar su influencia. Dependencia territorial, pocos años y entrenamientos solapados limitan inferencia y transporte. El soporte marginal contabilizó 126 entradas fuera del rango de entrenamiento entre 4.224 evaluadas, sumadas sobre especificaciones; tasas duplicadas entre tasas/ambas no son observaciones independientes. Estar dentro de rangos marginales tampoco garantiza soporte conjunto (`fase4/resultados/soporte_territorial.csv`, `resumen_soporte.csv`; `fase4/informe.md`, Medición).

Composición de examinados, cambios de medición y condiciones no incluidas son hipótesis posibles para estudiar posteriormente; no son causas comprobadas del deterioro de 2024. Las notas de comparabilidad, el enlace ecológico y la regla global desconocida deben acompañar la interpretación. La selección histórica de 59 columnas y la causa antigua del problema20212 permanecen archivadas porque la reconstrucción actual y su conservación no dependen de resolverlas; no se inventan criterios históricos ni se reabren sin evidencia relevante (continuidad, Salvedades; decisiones fase2 D10 y D13).

El resultado del objetivo 3 es un modelo global congelado para estimación agregada contemporánea, con desempeño, heterogeneidad y límites documentados. Se conserva evidencia desfavorable y no se afirma que reducir una privación cause una mejora educativa, que una intervención sea ineficaz o que el buen ajuste agregado describa mecanismos individuales. La comparación con persistencia sigue no evaluada, no pendiente de completar mediante ajuste en esta fase. La integración editorial en la tesis requiere revisión del grupo; este informe no acredita su adopción.

## 7. Puente metodológico al objetivo 4

El objetivo 3 aporta un esquema de entradas, transformaciones y modelo congelados, además de controles de integridad y límites de transporte. Un trabajo posterior sobre escenarios deberá contar con autorización expresa y definir de forma prospectiva la pregunta, la población, la disponibilidad contemporánea de indicadores, las entradas plausibles y la regla de soporte antes de calcular nuevas predicciones. Deberá conservar parámetros, escalas y huellas, comprobar unidades 0–100 y consistencia entre incidencia y privaciones; no podrá reconstruir IPM mediante promedios de tasas marginales ni suponer que una modificación aislada representa una población factible (protocolo §§1–3; DANE, algoritmo §3; `fase4/informe.md`, soporte).

La colinealidad y las diferencias entre asociaciones geográficas y longitudinales exigen evitar cambios arbitrarios de una variable mientras se supone que las demás son invariantes. Haría falta documentar coherencia conjunta y límites de extrapolación; el soporte marginal por sí solo no basta. Los percentiles del remuestreo de errores existente tampoco son intervalos de efectos o de escenarios. Cualquier diferencia entre predicciones bajo entradas hipotéticas se interpretaría, si se autorizara su cálculo, como contraste condicionado al modelo, sin identificar un efecto de intervención. La inferencia causal exigiría otra pregunta y evidencia que aquí no se ha producido. En fase 5 no se simulan escenarios, no se anticipan efectos ni se avanza a otro objetivo.

## 8. Referencias verificadas

Las fuentes siguientes son las efectivamente utilizadas. El registro de consulta y alcance está en `fase5/referencias_verificadas.md`. Las referencias web se comprobaron el 9 de octubre de 2026; no autentican la fecha o versión de descarga de datos locales.

1. DANE. *Índice de Pobreza Multidimensional, IPM 2023: materiales relacionados; Algoritmo para la construcción del IPM*. [Catálogo oficial y descripción del algoritmo](https://microdatos.dane.gov.co/index.php/catalog/824/related-materials), §§3 y 4.1–4.5 de la descripción. Sustenta organización y construcción de privaciones; no se extrapola su descripción histórica de representatividad a todos los años del panel. El catálogo no muestra fecha del algoritmo: no se inventa una.
2. scikit-learn. *Cross-validation: evaluating estimator performance*, documentación identificada como 1.9.1. [Sección 3.1](https://scikit-learn.org/stable/modules/cross_validation.html). Sustenta separación de entrenamiento/validación y control de transformaciones; el protocolo local define las ventanas por año completo.
3. scikit-learn. *GradientBoostingRegressor*, documentación identificada como 1.9.1. [Referencia de API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html). Sustenta significado de parámetros; su disponibilidad web no sustituye el registro local de versiones y parámetros.
4. Proyecto local. `protocolo/PROTOCOLO_OBJETIVO_3.md`, v1.0, 2026-10-08, §§1–8; `protocolo/decisiones_fase2.md`, D01–D14; `protocolo/fuentes/configuracion.py`. Son decisiones prospectivas y definición operativa, no criterios históricos recuperados.
5. Proyecto local. `auditoria/base_analitica_departamento_anio.csv`; `auditoria/diccionario_base_analitica.csv`; `auditoria/evidencia/actualizacion_20261008/` y `auditoria/evidencia/notas_ipm.csv`. Evidencia de construcción local y calidad, ubicaciones especificadas en §2.
6. Proyecto local. `fase3/informe.md`, `decisiones.md`, `README.md` y `resultados/` (2026-10-09). Tablas de selección/reevaluación y manifiesto congelado citados en §§3–4; versiones exactas en `fase3/requirements.lock.txt`.
7. Proyecto local. `fase4/informe.md`, `decisiones_previas.md`, `README.md` y `resultados/` (2026-10-09). Contraste territorial, asociaciones, coeficientes y remuestreo citados en §5.
8. Proyecto local. `CONTINUIDAD_OBJETIVO_3.md`, criterios de partida fase2 y cierres fases3–4; protocolo §7. Registro de exposición histórica en `prom.pdf` pp. físicas13–14,18,22 y `nueva ivestigacion .pdf` pp.5–7. Ubicaciones heredadas de la auditoría; no se afirma lectura nueva en fase5 ni autenticación bibliográfica de autores ausentes.

La generación del informe, tablas y figuras usa `fase5/fuentes/documentar.py` y esta plantilla editable, con controles numéricos sobre todas las métricas existentes de selección, reevaluación y diagnóstico territorial. `fase5/resultados/generacion.json` registra versiones de documentación, huellas de entradas y contextos de figuras. Los controles y el manifiesto de fase5 permiten verificar conservación y coherencia sin reentrenar; su alcance es documental y aritmético, no una segunda reproducción de la búsqueda completa.
