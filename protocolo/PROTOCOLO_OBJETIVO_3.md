# Protocolo del objetivo 3 — versión 1.0 congelada antes de entrenar

Fecha: 2026-10-08, America/Bogota. Fase autorizada y ejecutada: **2 solamente**.
Partida: `a68f0bb58b7b5268e6025ef33afc64862f8e8cc8`; árbol limpio al inicio.
Las decisiones prospectivas de este documento son nuevas; no reconstruyen criterios históricos.
Estado de cierre y evidencia ejecutada: `evidencia/verificacion_fase2.json`,
`evidencia/verificacion_notebook.json` y `evidencia/manifiesto_cierre.json`.
No hay modelos entrenados, simulaciones ni métricas nuevas de evaluación.

## 1. Pregunta, población y alcance temporal

Estimar el **promedio global Saber 11 de los registros elegibles de grado 11 de un
departamento del colegio-año**, dadas la incidencia de pobreza multidimensional y/o
sus tasas marginales departamentales **del mismo año**. Es estimación contemporánea
condicionada a entradas disponibles, con evaluación de transporte temporal. No promete
anticipar un año cuyo IPM todavía no esté publicado. Tampoco estima efectos de políticas.

Base única: `auditoria/base_analitica_departamento_anio.csv`; diccionario:
`auditoria/diccionario_base_analitica.csv`. Son 198 filas: 33 territorios en 2018, 2019,
2021, 2022, 2023 y 2024, con 2.984.199 registros. Colegio y año definen la llave;
Bogotá y 2021 permanecen; 2020/2025 están fuera del universo acordado. Se conservan
los filtros auditados: estudiante, exclusión de libertad S, seis puntajes disponibles
y positivos, código de colegio y grado 11. No se añade filtro de calendario.
El denominador representa registros, sin certificación de personas únicas.

Evidencia de población/agregación: `auditoria/evidencia/actualizacion_20261008/`
`validacion_reconstruccion.json`, `filtros_raw.csv`, `calendarios_raw.csv` y
`cotejo_agregacion_raw_final.csv` (2.574 cotejos). Fase 2 verifica el panel y esta
evidencia; no repite el censo individual. Las huellas quedan en la verificación.

## 2. Resultado y justificación de la agregación

Para territorio d y año t: `y_dt = suma de PUNT_GLOBAL recibidos elegibles / n_punt_global`.
Se conserva la precisión de la base, sin redondear antes del ajuste o las métricas.
Los filtros hicieron disponibles los puntajes de los registros incluidos; no se
imputan ni recalculan. Se retienen las 414 diferencias aritméticas de grado 11
presentes en fuente (`formula20222_raw.csv` y `diccionario_base_analitica.csv`).

**Declaración del usuario:** utilizó promedio y no hizo comparación previa con mediana
(`CONTINUIDAD_OBJETIVO_3.md`, criterios de trabajo). **Comprobación:** la suma y el
denominador reconstruidos coinciden con el consolidado (cotejo citado). **Decisión nueva:**
la media corresponde al nivel promedio de desempeño de los registros elegibles de la
celda; cada registro contribuye por igual dentro de ella. La mediana describiría el
centro por orden de la distribución, un estimando diferente. La media conserva la
contribución de todos los puntajes y puede ser sensible a extremos válidos; no se afirma
superioridad empírica frente a la mediana, normalidad ni representatividad de toda la
juventud. No es necesario volver a leer microdatos para comparar medianas: el objetivo
ya está fijado. Un eventual contraste requeriría evidencia separada de desarrollo hasta
2022 y nunca elegir el resultado según mejores métricas.

Cada **territorio-año pesa igual** en ajuste y evaluación principal (`sample_weight=None`).
Así cada uno de los 33 territorios pesa igual por año; el promedio de errores no es el
error del estudiante nacional típico. Los conteos se conservan para diagnóstico, sin
ponderar. No se usan precisión muestral o intervalos IPM como pesos improvisados.

## 3. Entradas y transformaciones congeladas

Se comparan tres especificaciones exactas: `ipm` (1 entrada), `tasas` (15 entradas)
y `ambas` (16 entradas). Orden/nombres exactos en `fuentes/configuracion.py`,
`ESPECIFICACIONES`; corresponden al diccionario. IPM es porcentaje de personas;
las tasas marginales son porcentajes de hogares según los rótulos locales. No se
reconstruye incidencia IPM a partir de promedios de tasas: faltaría la distribución
conjunta de privaciones y son unidades diferentes.

| Dimensión oficial | Columnas exactas de la base |
|---|---|
| Condiciones educativas del hogar | Analfabetismo; Bajo logro educativo |
| Condiciones de la niñez y juventud | Barreras a servicios para cuidado de la primera infancia; Inasistencia escolar; Rezago escolar; Trabajo infantil |
| Trabajo | Desempleo de larga duracion; Trabajo informal |
| Salud | Barreras de acceso a servicios de salud; Sin aseguramiento en salud |
| Acceso a servicios públicos domiciliarios y condiciones de la vivienda | Hacinamiento critico; Inadecuada eliminacion de excretas; Material inadecuado de paredes exteriores; Material inadecuado de pisos; Sin acceso a fuente de agua mejorada |

Agrupación documental confirmada en [DANE, algoritmo IPM, secciones 4.1–4.5](https://microdatos.dane.gov.co/index.php/catalog/824/related-materials),
consultado 2026-10-08. Los encabezados oficiales y los nombres locales se corresponden;
no se generan tasas agregadas por dimensión.

Se excluyen INSE, áreas Saber, percentiles, variables derivadas del resultado,
identificadores, nombre/código departamental, año y conteos como predictores. Año y código
solo definen particiones, uniones y trazabilidad. Las áreas fueron filtros/controles de
calidad, no la entrada para predecir global. Ningún filtrado por correlación con y.

Se mantienen porcentajes 0–100 y resultado en puntos. OLS y Ridge usan
`Pipeline(StandardScaler(), regresor)`: centrar y escalar cada columna con media y
desviación del entrenamiento de la ventana; columna constante se transforma con escala
1, sin eliminarla por evaluación. Los árboles usan porcentajes originales. No se
normaliza y, no se aplican logaritmos, PCA, interacciones, discretización, selección de
variables, winsorización, imputación ni recorte de predicciones. Cualquier transformación
adicional cambiaría este protocolo y debe justificarse antes de resultados.
El ajuste dentro de cada ventana sigue la [documentación de validación y transformaciones
de scikit-learn, sección 3.1](https://scikit-learn.org/stable/modules/cross_validation.html).

## 4. Particiones temporales y selección

Desarrollo exclusivo: 132 filas de 2018, 2019, 2021 y 2022. Validación expansiva sobre
**años completos**, ordenados por llave, sin mezclar aleatoriamente filas:

| Ventana | Entrenamiento | n | Validación | n |
|---|---|---:|---|---:|
| 1 | 2018 | 33 | 2019 | 33 |
| 2 | 2018, 2019 | 66 | 2021 | 33 |
| 3 | 2018, 2019, 2021 | 99 | 2022 | 33 |

La ventana 2 cruza dos años calendario: 2020 no se fabrica. Solo hay tres años de
validación y territorios repetidos; 99 predicciones no son 99 observaciones temporalmente
independientes. No se aplica `TimeSeriesSplit` directamente por posición de fila: podría
partir un año. Se construyen máscaras de años explícitas (`VENTANAS`) y se validan
cardinalidad, disjunción y anterioridad antes de entrenar.

Cada configuración se evalúa en las tres ventanas con idénticos datos, sin búsqueda
adaptativa. Los errores de las 99 predicciones fuera del ajuste de cada ventana se
concatenan; equivalen a promediar MAE de tres años de 33 filas. Son **métricas de
selección**, potencialmente optimistas para el ganador. No se presenta la misma búsqueda
como validación independiente ni se inventa CV anidada en la primera ventana, cuyo
entrenamiento solo tiene un año. Alternativa resuelta: búsqueda pequeña predefinida,
tabla completa y posterior reevaluación temporal con parámetros congelados.

2023 y 2024 (33 + 33 filas) están excluidos de ajuste, escalado, selección de columnas,
hiperparámetros y desempates. Los controles estructurales de fase 2 leen las 198 filas
para integridad/rangos, sin calcular asociaciones, errores ni descriptivos del resultado
por año reservado; esa lectura no es selección. El script futuro de desarrollo deberá
separar inmediatamente desarrollo/reserva y no entregar y reservado al buscador.

## 5. Modelos y búsquedas prospectivas

El resultado es continuo. No se transfieren logística, cortes alto/bajo, AUC/Brier ni
rankings históricos a esta regresión. Las referencias nuevas son: media constante del
y de entrenamiento (un solo candidato) y OLS con intercepto en cada una de las tres
especificaciones (tres candidatos). Ambas participan en la selección y pueden ganar.

| Familia | Parámetros buscados, producto cartesiano | Parámetros fijados |
|---|---|---|
| Ridge | alpha: 0.1, 1, 10, 100, 1000 | Intercepto; solver=svd; escalado de X |
| RandomForestRegressor | max_depth: 2, 4; min_samples_leaf: 3, 8; max_features: 0.5, 1.0 | 300 árboles; squared_error; bootstrap=True; min_samples_split=2; n_jobs=1; oob_score=False |
| GradientBoostingRegressor | n_estimators: 50, 100; learning_rate: 0.03, 0.1; max_depth: 1, 2 | squared_error; min_samples_leaf=3; min_samples_split=2; subsample=1; max_features=None; n_iter_no_change=None |

Semilla única prospectiva `20261008` para componentes aleatorios; no se buscan semillas.
Parámetros no listados: defaults de la versión de biblioteca fijada antes del primer
ajuste, exportados íntegros mediante `get_params(deep=True)` al manifiesto de ejecución;
no se prueban otros defaults ni se decide entre versiones según métricas.
Grilla y orden determinista completos en `evidencia/candidatos_congelados.json`, generados
desde `fuentes/configuracion.py`: 63 configuraciones buscadas + 4 referencias = **67**.
Cada una tendrá tres ajustes de ventana (201 ajustes definidos, ninguno realizado).
Grilla pequeña por las 33 filas iniciales y colinealidad posible entre incidencia/tasas;
Ridge proporciona regularización. No se agregan XGBoost/redes/ensambles a partir del
desempeño observado. Estas elecciones no son afirmaciones de superioridad.

Referencias técnicas consultadas 2026-10-08, documentación mostrada como scikit-learn
1.9.1: [Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html),
[RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html),
[GradientBoostingRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html).
La API consultada no demuestra instalación o compatibilidad local; véase reproducción.

## 6. Métricas, desempates y fallos

Para m filas, error `e_i = pred_i - y_i`:

- **Principal MAE:** `sum(abs(e_i))/m`, puntos Saber, menor es mejor.
- RMSE: `sqrt(sum(e_i**2)/m)`, puntos Saber; penaliza errores grandes.
- Sesgo: `sum(e_i)/m`, puntos Saber; positivo implica sobreestimación.
- R²: `1 - sum(e_i**2)/sum((y_i-mean(y))**2)`, adimensional; puede ser negativo.
  Si el denominador es cero, se registra no definido, nunca se reemplaza por 0/1.

Se presentan por ventana y agrupadas, sin redondeo al seleccionar. Para RMSE agrupado
se usa raíz del MSE concatenado, no promedio de raíces. El MAE evalúa error absoluto
entre **medias departamentales**; no transforma y en mediana ni impone pérdida absoluta
para entrenar. No hay métricas de clasificación ni umbral de éxito inventado.

Regla determinista sobre los 67 candidatos completos: (1) conservar los que tengan
MAE hasta `mínimo MAE + 0.1 puntos`; (2) de ellos conservar los de RMSE hasta `mínimo
RMSE del conjunto + 0.1 puntos`; (3) preferir menos predictores (media=0); (4) familia
en orden media, OLS, Ridge, Random Forest, Gradient Boosting; (5) primer ID en el orden
de `candidatos_congelados.json`. La tolerancia de 0.1 es una preferencia prospectiva por
parsimonia ante diferencias pequeñas, no un umbral demostrado de relevancia educativa.
El orden de grilla rompe empates, sin llamarlo prueba universal de menor complejidad.
Aplicar también dentro de cada especificación para conservar sus ganadores comparables;
la media se reporta común a las tres, sin asignarle una entrada ficticia.

Fallos: detener ante cambio de huella/población, faltantes, rango no válido, fuga o
particiones incompletas; no imputar, eliminar filas o modificar filtros automáticamente.
Registrar traceback, ID, ventana, versión y parámetros en fallos de candidato; no calcular
promedio con menos ventanas. Un candidato con fallo numérico persistente es inelegible;
no se amplía la grilla para compensarlo. Una falla de infraestructura se corrige y se
repite el mismo ajuste, sin cambiar datos/criterios. Advertencias se registran; convergencia
no satisfecha o predicciones no finitas inhabilitan el candidato. Si todas las referencias
fallan, detener la comparación. Predicciones finitas fuera de 0–500 se conservan con
advertencia y conteo, sin clipping para mejorar errores.

## 7. Congelación y evaluación posterior, no ejecutadas

Después de selección por desarrollo, guardar tabla de las 67 configuraciones, predicciones
de validación con llaves, ganadores por especificación y ganador global, parámetros,
transformaciones, versiones, huellas, semillas y fallos. Ajustar cada ganador de
especificación y las referencias en las 132 filas hasta 2022; congelar artefactos y
manifiesto **antes** de leer errores reservados. El ganador global se marca de antemano.
No actualizar con 2023 para predecir 2024; aplicar el mismo ajuste congelado a ambos.

Reportar MAE, RMSE, sesgo y R² por 2023, por 2024 y sobre 66 filas concatenadas, con
peso igual. Comparar diferencias de MAE respecto de media/OLS y mostrar errores por
territorio-año; no escoger otro ganador por la reserva. Un resultado pobre es resultado,
no permiso para volver a buscar. No reportar intervalos i.i.d. o p-valores de superioridad
sobre estas filas dependientes como si fueran réplicas independientes.

**Es reevaluación temporal, no prueba inédita**: ya se compararon resultados de esos
años en `prom.pdf`, páginas físicas 13–14, 18 y 22, y `nueva ivestigacion .pdf`, páginas
5–7. Estas ubicaciones fueron verificadas en fase 1; no se releen ni se reproducen sus
métricas aquí. No usamos los valores históricos para definir candidatos/desempates.
La exposición previa limita la fuerza confirmatoria aun con esta congelación.

Contraste por territorios: secundario dentro de desarrollo, pregunta de transporte a un
territorio ausente del ajuste. Para cada ganador de especificación **ya seleccionado**,
dejar un código completo fuera (33 grupos, cuatro años por grupo), ajustar en los otros
32 territorios de desarrollo y evaluar las cuatro filas del excluido; escalado solo en
entrenamiento. Reportar 132 errores agrupados y por territorio. Incluye años coetáneos
en entrenamiento, por lo que no responde a anticipación ni sustituye las ventanas.
Los hiperparámetros ya seleccionados vieron esos territorios en el desarrollo: declarar
el sesgo de selección; no llamarlo contraste independiente ni reseleccionar con él.
No usa 2023–2024 ni cambia el ganador. Esta fase solo define el contraste.

## 8. Problemas resueltos y límites que permanecen

Registro completo, impacto, alternativas y comprobaciones en `decisiones_fase2.md`.
Las notas del XLSX local (`auditoria/evidencia/notas_ipm.csv`, IPM_Departamentos A50–A53;
IPM_Variables_Departamento A864–A868) advierten expansión CNPV2018, captura rural 2021
y cambio de marco de agua rural 2019–2020. Mantener valores originales y evaluación por
año, sin retirar 2021, corregir arbitrariamente tasas o atribuir toda variación a Saber.
No se cuantifica aquí incertidumbre de encuesta ni se supone exactitud poblacional IPM.

La geografía Saber es ubicación del colegio, IPM hogares residentes del territorio;
son poblaciones distintas enlazadas ecológicamente. No inferir efecto individual de
pobreza, composición de estudiantes ni causalidad desde asociaciones departamentales.
La inclusión condicionada por los filtros limita la población objetivo. Pocos años,
dependencia territorial y posibles cambios de medición limitan transportabilidad.

Antecedentes archivados: selección histórica 59/esquema 82, causa antigua 20212,
autenticación de descargas, entorno/métricas históricas ausentes. No se inventa su
explicación ni se reabren sin evidencia que afecte la construcción actual. Se conserva
advertencia de fórmula desconocida y procedencia local. La aceptación editorial de la
propuesta de tesis sigue en manos del grupo, sin bloquear este protocolo local.

## 9. Reproducción y condición de avance

Organización y comandos en `README.md`. Fuente común de parámetros y ventanas:
`fuentes/configuracion.py`. Fuente de controles: `fuentes/controles.py`. Fuente de
celdas: `fuentes/01_protocolo_controles.py`; generador/validador:
`fuentes/generar_notebooks.py`. Se entrega únicamente
`notebooks/01_protocolo_controles.ipynb`, sin salidas incrustadas.

Controles ejecutados con Python 3.12.14 del runtime disponible; dependen solo de la
biblioteca estándar. Las versiones de paquetes presentes/ausentes están en la evidencia;
son actuales, no históricas. No están instalados scikit-learn, nbformat ni ipykernel en
ese runtime. El generador valida exhaustivamente su subconjunto sin salidas de formato
4.5 y ejecuta secuencialmente sus celdas con compile/exec. No afirma validación JSON
Schema completa con nbformat ni ejecución en kernel Jupyter. La ausencia de kernel no
impide ejecutar los controles Python ni distribuir un notebook válido de este subconjunto.

En la siguiente fase autorizada de modelos: preparar entorno aislado antes de ajustar;
objetivo de API scikit-learn 1.9.1 consultada, exportar versiones exactas de Python,
numpy, scipy, pandas, joblib, threadpoolctl, scikit-learn y, para Jupyter, nbformat e
ipykernel. Validar compatibilidad y los defaults antes de observar métricas; si esa
versión no está disponible, documentar sustitución técnica compatible sin ampliar grilla
ni cambiar metodología. No atribuir a fase 2 instalación o pruebas de modelos no hechas.

Condición de avance: controles aprobados, parámetros y protocolo con huellas, decisiones
indispensables resueltas y autorización explícita de la fase posterior. Quedan tareas de
implementación/entorno, no decisiones de población, resultado, entradas o evaluación.
Cambios materiales requieren enmienda versionada con motivo y evidencia **antes** de
observar nuevos resultados; la reserva no se reutiliza para ajustes repetidos. Este
cierre no autoriza modelos ni simulaciones. Commit local; no push.
