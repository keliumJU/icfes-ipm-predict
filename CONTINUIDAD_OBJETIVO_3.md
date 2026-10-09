# Continuidad del objetivo 3

Actualización: 2026-10-09 (America/Bogota). Alcance vigente: **fase 4 cerrada**, contraste territorial, robustez y explicaciones ejecutados; sin simulaciones.
Estado: protocolo v1.0 conservado, ganador y artefactos congelados hasta 2022 intactos; salvedades históricas conservadas. Cualquier fase posterior requiere autorización nueva. Las secciones anteriores conservan su registro histórico; el cierre vigente está al final.

## Partida y conservación

- Primera auditoría: inicio `c288074795f2c8b1b4865b73f8e08561cecd4448`, cierre de avance `77c286f43a3c6d811fc68ba9399fd5ec99277528`.
- Esta sesión parte de `77c286f43a3c6d811fc68ba9399fd5ec99277528`. Git tenía un cambio del usuario en `.gitignore`: renombraba la carpeta ignorada y añadía `raw_data`. Se conserva y no se incluye en el commit de auditoría.
- El usuario aportó `raw_data/` y renombró la carpeta a `Datos anteriores a la unificacion/`. Los once CSV renombrados y el consolidado tienen las mismas huellas previas. Los 49 archivos relevantes y dos directorios vacíos están inventariados; 28 datasets ignorados siguen fuera de Git.
- No se alteró ningún original. `Resultados Guardados/` y `Entorno de ejecución/` siguen vacíos. No se entrenaron modelos, imputaron puntajes, editaron PDFs ni excluyó 2021.
- Commit de cierre solicitado: `fase 1: auditoría de datos y evidencia`. Consultar identificador en Git o respuesta de cierre. No hacer push.

## Resultado nuevo y evidencia

1. **Doce TXT completos:** se auditaron 4.039.755 registros de 2018, 2019, 2021, 2022, 2023, 2024 y sus dos periodos. Los cuatro TXT de 2020/2025 se inventarían e inspeccionan por encabezado, fuera del análisis. Cero filas de ancho incorrecto y cero periodos discordantes. Evidencia: `auditoria/evidencia/actualizacion_20261008/esquemas_raw.csv`, `filtros_raw.csv`.
2. **Filtros:** 3.433.542 estudiantes, 3.432.366 sin libertad S, 3.401.100 con seis puntajes positivos/disponibles y código de colegio, 2.984.199 grado 11. Reproducen tabla 4. Cadena FIX concurrente: 3.432.344; FIX+final: 3.401.100. No se mezclan mermas secuenciales y concurrentes. Se comprueban 608.458 bilingüismos faltantes antes del reemplazo escrito; la auditoría no imputa ni usa bilingüismo. Evidencia: `filtros_raw.csv`.
3. **IDs/calendarios:** IDs de registro no faltantes ni repetidos dentro/entre periodos; no son prueba de personas únicas. Grado 11 incluye calendario A 2.901.089, B 78.075, OTRO 5.034, faltante 1. No se añadió filtro A/B. Evidencia: `resumen_raw.json`, `calendarios_raw.csv`. IDs y firmas solo en memoria, no versionados.
4. **Conservación bidireccional:** todos los 3.401.100 finales coinciden con raw filtrado en 16 campos críticos; cero sobrantes o firmas ambiguas en doce periodos. Once periódicos 59 conservan las filas raw en la misma proyección. No se certifican todos los atributos socioeconómicos. Evidencia: `conservacion_raw_final.csv`, `conservacion_raw_periodicos.csv`.
5. **20212:** raw 606.030; elegibles 534.706; grado 11 480.252, todos conservados. El usuario recuerda error de lectura antiguo; no se exige recrearlo ni se declara demostrada su causa técnica. El panel raíz viejo omite 20212; se conserva como versión histórica distinta y no se usa como base actual.
6. **Fórmula global:** 525 diferencias retenidas ya existen en TXT 20222; 414 grado 11, 111 grado 26, delta+1..12, discapacidad N. Los TXT completos tienen 527 diferencias entre casos con cinco pruebas positivas; dos de 20181 no sobreviven filtros. Se conservan globales de fuente; no se conoce regla/versión aritmética, ni se atribuye recalificación/error manual. Evidencia: `formula20222_raw.csv`, `filtros_raw.csv`.
7. **Agregación independiente:** segunda lectura raw por bloques para grado 11 y seis pruebas. Sus conteos/sumas coinciden con los del consolidado en 2.574 cotejos (198 celdas×13 variables). Evidencia: `agregados_grado11_raw.csv`, `cotejo_agregacion_raw_final.csv`.
8. **Base validada:** `auditoria/base_analitica_departamento_anio.csv`, 198 llaves únicas, 33 territorios/año, 2.984.199 registros, sin nulos; medias sin redondeo intermedio y denominadores propios. Colegio/grado 11, incluye Bogotá/2021, sin 2020/2025. IPM+15 tasas se unen uno a uno por código/año; cifras cotejadas previamente contra XLSX local. `auditoria/diccionario_base_analitica.csv` documenta unidades, fuente y advertencias. Validación: `validacion_reconstruccion.json`, `verificacion_cierre.json` en carpeta fechada.
9. **Propuesta al grupo:** `auditoria/propuesta_correccion_tesis.md` ofrece sustitución de pp 115–117 para coherencia con pp 53–69; `tabla12_propuesta_198.csv` recalcula 16 asociaciones de base principal. No se modifica ACA2 ni se afirma aceptación del grupo. IPM/global: r 198 celdas−0,7215676; r 33 medias−0,7521243. No causalidad ni selección automática de variables.
10. **Matriz:** 59 afirmaciones, actualizadas con columnas de dictámenes/evidencias/pendientes 20261007. Métricas previas permanecen históricas reportadas, no reproducidas. Ausencia de probabilidades/modelos no impide auditar la base actual y no se llena entrenando.

## Evidencia anterior conservada

Diagnóstico 20261007 guardado en `auditoria/historico/diagnostico_calidad_20261007.md`; sus CSV/JSON permanecen como entrega fechada anterior. Mapa PDF igual: 58 páginas de ACA2 leídas completas, 68 fuera del foco pendientes, dos informes completos. La actualización no simula lecturas adicionales. IPM: 3.168 cifras locales cotejadas sin diferencias, notas de comparabilidad conservadas. Descriptivos: niveles 13.604.400 coincidencias, INSE 683.744 nulos/4.621>100 exploratorio, tres diferencias de precisión en tabla 7 y dos en tabla 10. Referencias y ubicaciones en diagnóstico actual/matriz.

## Salvedades y acciones posteriores

- No hay metadatos que autentiquen URL/fecha/versión de descarga. Se validan los TXT locales con huellas, no una descarga oficial.
- El criterio histórico de selección 59 columnas y esquema 82 no se recuperó. La construcción nueva explícita evita depender de ellos; la conservación comprobada se limita a campos críticos.
- La selección histórica de 59 columnas queda archivada como antecedente, no como pendiente activo ni condición de avance. El usuario aclara que, después de limpiar, utilizó el puntaje global individual para calcular el promedio departamental; no comparó previamente media y mediana. Los campos de periodo, geografía y población siguen siendo necesarios para definir y agrupar los registros. Esta declaración no elimina los filtros ya verificados ni cambia la base.
- Causa antigua del error 20212 y logs pre-FIX no autenticados. El usuario permite dejar ese problema histórico documentado y continuar con final conservado.
- Regla oficial que explica 525 diferencias aritméticas desconocida. Se cierran procedencia y conservación; la advertencia de fuente queda, sin nuevo filtro ni puntaje recalculado.
- Artefactos y entorno de modelos históricos ausentes. AUC/Brier/rankings no son resultados reproducidos ni se transfieren a regresión.
- El grupo debe decidir/editar la propuesta de tesis. La auditoría entrega la propuesta y su evidencia; no afirma que ya se adoptó.

Estas salvedades no se ocultan ni se tratan como causas demostradas. No quedan controles indispensables pendientes para la construcción local declarada; autenticaciones históricas distintas siguen con dictamen no verificable.

## Reproducción y próxima sesión

Secuencia vigente en `auditoria/procedimientos/README.md`: `auditar_raw_20261008.py`, `actualizar_entrega_20261008.py`, `verificar_cierre_20261008.py`. No ejecutar inventarios/procedimientos antiguos con rutas renombradas: sobrescribirían estados históricos. Los nuevos usan el commit `77c286f` como referencia fija. Python 3.12.14, pandas 2.2.3, numpy 2.3.5, openpyxl 3.1.5 son versiones actuales, no históricas.

## Criterios de partida conservados de la fase 2

Actualización documental solicitada por el usuario el 2026-10-08; partida de esta actualización: `54cd549700c9ce8ef83c707b825d215f1902fe53`. No se ejecuta fase 2 en esta sesión. El commit del usuario ya registra la nueva carpeta y `.gitignore`; no se modifica ese archivo. Se conservan las evidencias y cifras de la auditoría.

1. **Resultado principal:** `prom_punt_global`, media aritmética de los puntajes globales individuales elegibles dentro de departamento-año, sin redondeo intermedio. Es la construcción usada y comprobada, no una conclusión de que la media sea universalmente superior a la mediana. En fase 2 justificar qué resultado se quiere estimar. Si un contraste descriptivo con mediana aporta información material, limitar la decisión metodológica al desarrollo hasta 2022, guardar el contraste por separado y no sustituir el objetivo principal buscando mejores métricas.
2. **Población y unidad:** registros de grado 11, departamento del colegio, 33 territorios y los años 2018, 2019, 2021, 2022, 2023, 2024; base validada de 198 filas. Conservar los filtros auditados de estudiante, libertad S, seis puntajes positivos/disponibles y código de colegio. No retirar 2021/Bogotá ni añadir filtro de calendario. Cada territorio-año tiene el mismo peso en el análisis principal; los conteos son trazabilidad y diagnóstico.
3. **Puntajes y predictores:** conservar globales recibidos, incluidas las 414 diferencias aritméticas de grado 11; no imputar ni recalcular. IPM y 15 tasas como entradas principales, comparando IPM solo, tasas solas y combinación. Excluir del principal INSE, puntajes por asignatura, percentiles, variables derivadas del resultado y códigos como predictores. Las áreas se conservaron para controles/filtros, no para construir el promedio global ni predecirlo. No inventar índices oficiales de dimensión con promedios de tasas.
4. **Uso temporal:** el alcance actual estima el puntaje departamental dado el IPM del mismo año. No describirlo como anticipación de un año futuro cuando aún se desconocen sus entradas. Si aparece una exigencia explícita de anticipación, formular una alternativa con información disponible previamente y documentar el cambio antes de implementarlo.
5. **Evaluación:** desarrollo con 2018, 2019, 2021 y 2022; validación temporal expansiva, conservando juntos los territorios de cada año. Definir posteriormente evaluación separada y conjunta de 2023–2024 con modelos congelados hasta 2022. Es una reevaluación temporal sobre años excluidos del ajuste, **no una prueba completamente inédita**, porque sus resultados se compararon antes. Evidencia verificada: `prom.pdf`, páginas físicas 13–14 (logística), 18 (Random Forest), 22 (XGBoost); `nueva ivestigacion .pdf`, páginas 5 (tabla), 6–7 (selección del ganador). No ajustar el procedimiento repetidamente con esos resultados. Las métricas históricas siguen reportadas, no reproducidas.
6. **Auditoría dinámica:** ante un problema, registrar evidencia, impacto, alternativa, decisión y comprobación. Resolver lo verificable y las decisiones rutinarias dentro de la fase autorizada. Archivar antecedentes irrelevantes para el resultado actual, sin ocultarlos ni tratarlos como bloqueos. Un problema indispensable para validez, cobertura o ausencia de fuga sigue activo hasta resolverse. La reducción histórica a 59 columnas no se reabre sin nueva evidencia que afecte la población, puntajes o unión.
7. **Notebooks:** el usuario solicita los necesarios para reproducir preparación, predicción de modelos y posteriormente simulación. Mantener fuentes editables `.py` y un generador Python de `.ipynb` con validación del formato, celdas ordenadas y funciones compartidas. Definir el número por etapas útiles, sin un notebook obligatorio por algoritmo. Separar entradas, parámetros, controles, salidas y versiones; usar rutas relativas al proyecto y semillas explícitas cuando corresponda. No incrustar datos personales ni resultados ficticios. En fase 2 pueden prepararse notebooks de protocolo/controles; entrenamiento y simulación pertenecen a sus fases posteriores autorizadas.

**Mensaje histórico de entrada a fase 2, ya atendido:** utilizar `PROMPT_FASE_2.md` y solo la sección de fase 2 del plan para cerrar protocolo, sin entrenar ni simular. Se conserva como antecedente; no reiniciar la fase por este mensaje.

## Cierre histórico de fase 2 — 2026-10-08

Partida `a68f0bb58b7b5268e6025ef33afc64862f8e8cc8`, Git limpio. Se leyeron AGENTS,
PROMPT_FASE_2, continuidad y exclusivamente líneas 49–64 (fase 2) del plan. No se
leyeron fases posteriores. No se alteró .gitignore, originales, datasets ignorados,
evidencias de fase 1 ni scripts históricos. Commit de cierre local: consultar
`git log -1 --format='%H %s'`; asunto `fase 2: cerrar protocolo reproducible antes de entrenar`.
No se hizo push. No se entrenaron modelos, calcularon errores predictivos ni simularon escenarios.

### Decisiones congeladas y comprobaciones

- **Usuario:** mantener población/filtros, Bogotá/2021, promedio principal, peso territorial
  igual, IPM/15 tasas/ambas, exclusiones y años acordados. Selección59 archivada.
- **Comprobación actual:** 198 filas, 33 territorios por año, 2.984.199 registros, sin
  nulos/llaves repetidas; diccionario, rangos y denominadores coherentes; se cotejan 2.574
  deltas raw/final existentes iguales a cero. No se repite censo raw. Huella base
  `609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866`, fijada en configuración.
- **Decisión nueva de agregación:** media para estimar nivel promedio de registros
  elegibles, no mediana del estudiante típico. No superioridad demostrada ni comparación
  histórica inventada; contraste con mediana innecesario para el estimando fijado.
- **Decisión nueva de entradas:** cinco dimensiones oficiales documentadas, sin tasas
  agregadas inventadas; 1/15/16 entradas. No INSE, áreas, percentiles, derivados de y,
  códigos, año ni conteos como X. IPM del mismo año: estimación contemporánea, no anticipación.
- **Decisión nueva de desarrollo:** 132 filas hasta 2022; ventanas 2018→2019,
  2018+2019→2021, 2018+2019+2021→2022, años completos 33/66/99 de entrenamiento y
  33 de validación. Transformaciones solo dentro de entrenamiento; escalado para OLS/Ridge.
- **Decisión nueva de modelos:** media constante y OLS como referencias; Ridge, RF regresor
  y Gradient Boosting regresor, tres especificaciones, grillas finitas: 67 candidatos
  definidos, ninguno entrenado. Semilla futura20261008. Parámetros en configuración y JSON.
- **Decisión nueva de selección:** MAE principal en puntos, RMSE/sesgo en puntos y R²
  secundario; candidatos completos en tres ventanas, tolerancia de 0.1 en MAE y luego
  RMSE, menos entradas y orden fijo de familia/ID. No clipping, búsqueda adaptativa ni
  ranking con ventanas fallidas. CV usada para selección tiene posible optimismo.
- **Decisión nueva de reevaluación:** 66 filas de 2023/2024, cada año y concatenadas;
  modelos ajustados hasta 2022 congelados antes de errores, sin actualizar con 2023.
  No es prueba inédita (PDFs y páginas ya verificadas en fase1); no reescoger ganador.
- **Decisión nueva de contraste territorial:** 33 grupos completos dentro de desarrollo,
  hiperparámetros fijos, diagnóstico distinto al transporte temporal, con advertencia
  de selección previa. Definido, no ejecutado.

### Entregables y reproducción

`protocolo/PROTOCOLO_OBJETIVO_3.md` (v1.0 completo), `protocolo/decisiones_fase2.md`
(D01–D14: evidencia, impacto, alternativa, decisión y control), `protocolo/README.md`
(organización de cinco etapas lógicas), fuentes Python compartidas y solo
`notebooks/01_protocolo_controles.ipynb` creado. No se crean fuentes/notebooks de modelos
ni simulaciones en esta fase.

Ejecutados, en orden: `protocolo/fuentes/controles.py`, `generar_notebooks.py`,
`verificar_cierre.py`. Evidencia nueva en `protocolo/evidencia/`: validación panel/ventanas,
67 candidatos definidos, validación del notebook/ejecución de tres celdas y manifiesto
de huellas. Notebook sin salidas incrustadas ni datos personales. Formato4.5, validación
estricta del subconjunto generado y ejecución compile/exec, sin kernel Jupyter.

Runtime usado: Python 3.12.14; pandas 2.2.3/numpy 2.3.5 presentes, no necesarios para estos
controles de biblioteca estándar. sklearn/nbformat/ipykernel ausentes. Python del sistema
es3.14.7. No se confunden entornos ni versiones actuales con históricas.

### Pendientes, límites y condición de avance

No quedan decisiones indispensables pendientes de fase2. Permanecen advertencias de
procedencia local, regla de fórmula global desconocida, notas de comparabilidad IPM,
poblaciones Saber/IPM distintas, dependencia y escasos años, selección optimista y
exposición previa de reserva. Selección59, causa antigua20212, descargas y entorno
histórico no autenticados quedan archivados con motivo; no se reabren sin evidencia
relevante. Aceptación editorial de corrección de tesis por el grupo sigue externa.

Pendientes de implementación posterior: entorno aislado y versiones exactas/API compatible
antes de cualquier ajuste; fuentes/notebooks de preparación/modelos/evaluación;
entrenamientos, métricas y contraste territorial. Escenarios solo cuando se autoricen,
sin interpretación causal. Estos pendientes no simulan trabajo realizado ni autorizan
continuar. Cualquier cambio material al protocolo exige motivo previo a nuevos resultados.

**Prompt siguiente, solo si el usuario autoriza fase 3:**
Continuar en icfes-predict-improved y ejecutar únicamente la fase 3 autorizada. Leer
AGENTS.md, esta continuidad, protocolo/PROTOCOLO_OBJETIVO_3.md, decisiones y README;
consultar solo fase 3 del plan. Preservar protocolo v1.0, panel198 y huellas, promedio,
población, especificaciones, ventanas y reglas. Preparar/verificar entorno antes de
ajustar, implementar lógica compartida y notebooks desde Python, registrar ejecuciones
reales y fallos. Seleccionar solo hasta 2022, congelar antes de reevaluar2023–2024 conforme
al alcance de esa fase; no reutilizar reserva para ajustar, no reabrir59 sin evidencia,
no simular ni avanzar sin autorización. Cerrar con evidencia, continuidad y commit local;
no push. Este prompt queda preparado, no ejecutado.


## Cierre vigente de fase 3 — 2026-10-09

**Autorización del usuario:** exclusivamente fase 3, incluida reevaluación separada y conjunta de 2023–2024. Sin simulación, fases posteriores ni push. Partida `7e95ffe823c3d08f345620c0f9bc65dc72fae7d5`, árbol limpio. Se leyeron AGENTS, continuidad, protocolo, decisiones/README y solo líneas 65–85 (fase 3) del plan. No se leyeron otras fases del plan. El protocolo v1.0 y la evidencia anterior permanecen intactos. El commit de cierre se identifica con `git log -1 --format='%H %s'`, asunto `fase 3: comparar modelos y congelar reevaluacion temporal reproducible`.

### Decisiones previas y controles

- **Usuario/conservado:** media global recibida, grado 11/filtros auditados, Bogotá/2021, peso igual por territorio-año, IPM/15 tasas/ambas, exclusiones de predictores, desarrollo hasta 2022 y reserva previamente expuesta. Selección59 archivada, sin nueva investigación ni criterios históricos inventados.
- **Comprobación actual:** base198 con SHA256 `609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866`; diccionario y demás huellas cotejadas. 33 territorios/año, 132 desarrollo, 66 reserva; 2.574 cotejos previos comprobados. No se repite censo de microdatos ni modifica población/agregación.
- **Decisión operativa antes de entrenar:** las diferencias del plan (persistencia/ElasticNet/XGBoost, grillas mayores, semilla 42 y desempate general) se documentan en `fase3/decisiones.md`. Prevalece protocolo v1.0: media/OLS/Ridge/RF/GBR, 67 candidatos, ventanas expansivas, semilla 20261008 y tolerancia 0.1/orden fijo. No se amplía búsqueda por desempeño.
- **Entorno verificado antes de ajustar:** venv aislado `/tmp/icfes-fase3-venv`, Python 3.12.14, sklearn 1.9.1, pandas 2.2.3, numpy 2.5.3, scipy 1.18.1, joblib 1.6.0, threadpoolctl 3.7.0, nbformat 5.10.4, ipykernel 6.30.1, nbclient 0.10.2. `fase3/requirements.lock.txt` fija todas las dependencias; `resultados/preparacion.json` registra versiones, defaults completos de 67 estimadores construidos sin ajustar, entradas/huellas, semilla y controles. Un hilo BLAS/OpenMP/RF.
- **Alcance resuelto:** reevaluación ejecutada ahora por autorización explícita. Contraste territorial predefinido queda para fase4; no se ejecutó ni se usa para seleccionar. No notebooks ni escenarios de simulación.

### Resultados actuales verificables

Fuente: `fase3/resultados/comparacion_desarrollo.csv`, `metricas_ventanas.csv`, `congelacion.json` y `metricas_reevaluacion.csv`. Son resultados nuevos, no reproducciones de rankings históricos de clasificación.

Se completaron 201 ajustes de ventanas (67×3), sin fallos ni advertencias de entrenamiento; 6.633 predicciones por territorio-año. Pipeline OLS/Ridge ajusta escalado solo dentro de entrenamiento; árboles mantienen porcentajes originales. Sin clipping, selección adicional de variables ni uso de reserva para parámetros.

**Ganador global:** `gradient_boosting_ambas_07`, 16 entradas, 100 etapas, aprendizaje 0.1, profundidad 2, hoja mínima3, subsample 1, semilla 20261008. MAE desarrollo 6.332499, RMSE 7.764136, sesgo+3.297261, R² 0.779915. La mejor configuración tasas da MAE 6.440524, diferencia0.108025 fuera de banda0.1: no desplaza al ganador por parsimonia. Mejores MAE brutos por familia: RF6.504996, Ridge7.074271, OLS7.693311, media13.842431. Tabla completa conserva configuraciones menos favorables.

Ganadores por especificación: IPM `gradient_boosting_ipm_02` (50 etapas/profundidad 1/aprendizaje 0.1); tasas `gradient_boosting_tasas_07`; ambas `gradient_boosting_ambas_07`. Los siete artefactos (media, tres OLS, tres ganadores) se ajustaron en 132 filas y congelaron antes de errores reservados, a2026-10-09T15:20:08.821292+00:00. Huellas, parámetros completos y transformaciones lineales en congelacion.json.

**Reevaluación temporal, no prueba inédita:** mismo ajuste hasta 2022 aplicado a2023/2024, sin actualizar con 2023 ni reseleccionar. Ganador: MAE 5.020614 en 2023,7.670549 en 2024,6.345582 conjunto; RMSE conjunto 7.802886, sesgo−2.779014, R² 0.788903. Subestimación mayor en 2024; no se atribuye causa. En conjunto, media14.903887, OLS IPM9.552257, OLS tasas8.155885, OLS ambas8.252112, GBR IPM9.768153, GBR tasas6.436305. Ninguna referencia supera al ganador global en reserva, pero **OLS IPM supera a GBR IPM** en ambos años y conjuntamente (diferencias MAE 0.128946/0.302844/0.215895 a favor de OLS). Impacto: complejidad no ayuda siempre; alternativa/control: comparación explícita con misma reserva y métricas; decisión: informar sin cambiar ganador. No se evalúan67 candidatos para buscar otro ganador reservado.

Se guardan462 predicciones de reserva (7×66), métricas21 filas (7×3 conjuntos), deltas frente a media/OLS y figura anual. Predicciones reservadas finitas y dentro0–500, sin recorte. Límites históricos de exposición permanecen con ubicaciones PDF ya verificadas, sin nuevas lecturas.

### Problemas encontrados, resolución y verificación

`fase3/incidencias_ejecucion.md`: DNS de instalación en sandbox resuelto mediante descarga autorizada del mismo paquete; kernel bloqueado antes del primer ajuste resuelto con ejecución autorizada fuera del sandbox (causa exacta no certificada). Verificación CSV encontró diferencias de hasta 5.7e-14 por parser ordinario: lectura round_trip recuperó igualdad estricta, sin alterar datos o errores. Un fallo del inventario de verificación por nombres Unicode escapados se corrigió usando salida Git delimitada por NUL, sin cambio de archivos históricos. No se oculta ningún candidato fallido: fallos.json está vacío porque ninguno falló.

`verificacion.json`: controles aprobados,67 candidatos completos, cobertura/llaves, métricas independientes, selección determinista, artefactos conservados y 152 archivos previos intactos (excepto actualización intencional de continuidad). Seis ajustes adicionales de comprobación (tres en el control interrumpido por Unicode y tres en el control aprobado) reproducen las 99 predicciones de ventanas del ganador; cargar siete artefactos reproduce las462 de reserva con tolerancia numérica1e-12. No se volvió a buscar por resultados.

### Entregables, reproducción y pendientes

- `fase3/README.md`: orden, entorno, entradas/salidas y procedimiento de reproducción en copia nueva.
- `fase3/informe.md`: comparación de todas las familias y referencias, hallazgo OLS IPM, límites y ubicaciones verificables.
- `fase3/fuentes/`: lógica común, fuentes narrativas02/03/04, generador/validador nbformat, informe y verificador; `reproducir.py` prepara copia Git/venv nuevos conservando cierre. Esa segunda búsqueda completa en copia **no se ejecutó** aquí; las verificaciones concretas anteriores sí.
- `notebooks/02_preparacion_desarrollo.ipynb`, `03_modelos_validacion.ipynb`, `04_reevaluacion_temporal.ipynb`: ejecutados realmente en kernel aislado, narrativa antes y discusión de resultados reales después. Se enriqueció Markdown y regeneró desde fuentes preservando outputs solo con código idéntico, sin editar JSON manualmente ni repetir ajustes. Notebook01/evidencias de fase2 intactos.
- `fase3/resultados/`: tablas/predicciones, siete modelos, preparación/congelación/reevaluación, fallos/advertencias, figura, verificación y manifiesto SHA256. Sin datos personales ni resultados ficticios.

Persisten limitaciones de procedencia local, fórmula global no autenticada, comparabilidad IPM, enlace ecológico, pocos años/dependencia, optimismo de selección y exposición previa de reserva. No hay afirmaciones causales. Antecedentes59/20212/descargas/entorno histórico siguen archivados; aprobación editorial de propuesta de tesis continúa externa. No quedan decisiones indispensables activas para fase3. Condición de avance: autorización nueva de fase4 sobre estos artefactos, sin ampliar búsqueda por reserva ni ejecutar escenarios no acordados.

**Prompt siguiente preparado, no ejecutado:** Continuar exclusivamente fase4 si se autoriza. Leer AGENTS, esta continuidad y protocolo/decisiones/README; consultar solo fase4 del plan y documentar discrepancias frente a protocolo antes de cualquier cálculo nuevo. Verificar huellas y artefactos congelados de fase3. Mantener población198, media, filtros, Bogotá/2021, peso igual, especificaciones/exclusiones y ganador hasta 2022. Implementar el contraste territorial ya predefinido únicamente en desarrollo con parámetros fijos, advertir selección previa y diferenciar transporte territorial de temporal. No reseleccionar con 2023–2024, cambiar grillas, afirmar causalidad ni ejecutar simulaciones sin autorización expresa. Registrar problemas/evidencia/impacto/alternativa/decisión/control, cerrar con continuidad y commit local; sin push.


## Cierre vigente de fase 4 — 2026-10-09

**Usuario:** autorizó únicamente fase4, conservar decisiones/artefactos congelados, no push ni simulaciones. Partida comprobada `9a22b8adc406423fa6829b75e77d7473deffe710`, coincidente con cierre anterior declarado; Git limpio, ningún cambio existente que apartar. Se leyeron AGENTS, continuidad, protocolo/decisiones/README y fase3 README/decisiones/informe; del plan solamente fase4 líneas87–104. No se leyó fase posterior. Commit de cierre local: consultar Git, asunto `fase 4: contrastar transporte territorial y robustez sin reseleccion`.

### Decisiones previas, conservación y comprobaciones

- Usuario/conservado: base198, promedio global recibido, filtros auditados, Bogotá/2021, peso igual, tres especificaciones exactas y exclusiones; selección59 archivada. Ganador global/reevaluación cerrados. No se modifica protocolo v1.0, fase3, originales, evidencias históricas o .gitignore.
- Comprobación actual antes de ajustes: huella base609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866; todas las huellas de cierre3 y entradas/protocolo/modelos coinciden. Python3.12.14, sklearn1.9.1 y todas las versiones exactas de fase3 coinciden; pip check aprobado. Se reutilizan entorno `/tmp/icfes-fase3-venv` y funciones compartidas, semilla20261008 y un hilo.
- Decisión operativa prospectiva: `fase4/decisiones_previas.md` documentó diferencias antes de nuevos resultados. No excluir2021, añadir año como predictor, ponderar por estudiantes ni excluir dimensiones: cambiarían decisiones congeladas. Alternativas ejecutadas: métricas anuales, asociaciones longitudinales/doble centrado, tamaño frente a error, coeficientes OLS congelados y colinealidad. No enmienda material del protocolo ni búsqueda adicional.
- Remuestreo prospectivo:2.000 réplicas pareadas por33 territorios completos, errores fijos; tres comparaciones territoriales entre especificaciones y cuatro temporales del ganador frente a referencias cerradas. Percentiles condicionales, no p-valores, inferencia i.i.d., incertidumbre de selección/ajuste o de años futuros.

### Resultados actuales (no históricos ni causales)

Fuentes: `fase4/resultados/metricas_agrupadas.csv`, `predicciones_territoriales.csv`, `bootstrap_resumen.csv`, `asociaciones_longitudinales.csv`; explicación/impacto/alternativas en `fase4/informe.md`.

- Contraste §7 realizado:99 ajustes, cada uno128 filas/32 territorios de2018/2019/2021/2022 para entrenamiento y4 filas del territorio excluido. Tres ganadores ya seleccionados, hiperparámetros fijos, sin2023–2024.396 predicciones, métricas agrupadas/territoriales/anuales, ningún fallo o advertencia de modelos. Los ganadores son GBR sin escalado; la lógica compartida ajusta transformaciones dentro de entrenamiento cuando corresponde. No clipping.
- MAE territorial IPM9.316132, tasas7.825903, ambas8.067691; RMSE12.126201/10.015879/10.276440, sesgo−0.498728/−0.936268/−1.301338. Tasas mejora0.241788 frente a ambas. Impacto: no afirmar ventaja territorial universal del ganador; alternativa/comprobación: comparación pareada predefinida, percentiles tasas−ambas[−0.569529,0.045591], cruza0. Decisión: informar sin cambiar ganador global `gradient_boosting_ambas_07` o evaluación temporal cerrada.
- Parámetros seleccionados previamente con estos territorios: sesgo de selección explícito, no validación independiente. Transporte territorial con años coetáneos distinto del temporal, no anticipación ni prueba de que un diseño supera al otro.
- IPM/global en desarrollo: r entre33 medias−0.764626, dentro132 desviaciones+0.116285, doble centrado−0.136136. Impacto: patrón geográfico no identifica mecanismo longitudinal. Alternativa ejecutada: separar y centrar por año; decisión: asociaciones descriptivas, sin causalidad. Se conservan16 indicadores completos.
- SVD entradas estandarizadas: condición1/IPM,12.644109/tasas,30.647008/ambas; rangos completos1/15/16. Coeficientes OLS congelados no son importancia GBR ni efecto causal; tablas de correlación y coeficientes completas. Tamaños Saber190–79.542 en desarrollo, diagnóstico sin ponderar ni inferir precisión IPM. Soporte marginal/influencia de grupos/extremos preservados sin excluir filas.
-14.000 réplicas guardadas. Los percentiles temporales del ganador frente a media/OLS son negativos, pero reserva previamente expuesta/selección/dependencia y años fijos limitan confirmación. No nuevos ajustes temporales ni uso de2024 para modificar criterios. El deterioro2024 permanece sin causa identificada.

### Incidencias y verificación

Primer kernel sandbox sin progreso se interrumpió (salida130) antes de resultados; misma ejecución aprobada fuera del sandbox terminó. Causa exacta no certificada. Aviso de caché pip sin impacto, dependencias aprobadas. El control documental final rechazó inicialmente prosa Markdown al aplicar ast.parse a la fuente completa; se corrigió compilando solo celdas de código, sin alterar cálculos ni repetir ajustes. Evidencia/impacto/alternativa/decisión en incidencias_ejecucion.md. No se ocultan fallos de modelos: registros vacíos por completitud real.

`fase4/resultados/verificacion.json`: cobertura396,99 particiones, métricas/errores independientes,14.000 réplicas verificadas, asociaciones verificadas; seis ajustes focales adicionales en dos controles reprodujeron12 predicciones por control con tolerancia1e−12.192 archivos previos intactos salvo continuidad intencional. Los notebooks05/06 se ejecutaron en kernel aislado y validaron con nbformat; discusión concreta añadida desde resultados reales regenerando con código idéntico/salidas preservadas. No JSON manual. Manifiesto final fija entregables; segunda reproducción completa en copia implementada pero no ejecutada, sin simular evidencia.

### Entregables, límites, pendientes y condición de avance

`fase4/README.md` documenta orden/entradas/salidas/entorno y reproducción en copia nueva; `decisiones_previas.md`, `informe.md`, `incidencias_ejecucion.md`, fuentes Python y resultados completos. `notebooks/05_contraste_territorial.ipynb` y `06_robustez_explicaciones.ipynb` ejecutados realmente. Sin artefactos de simulación. No repetir preparación en árbol cerrado: reproducción crea copia nueva del commit de partida y conserva fuente.

No quedan controles indispensables activos de fase4. Permanecen selección previa, dependencia/pocos años, exposición temporal previa, medición IPM y enlace ecológico, procedencia local y fórmula desconocida. No existen insumos aquí para cuantificar precisión de encuesta/composición individual ni atribuir causas a2024: hipótesis, no evidencia causal. Antecedentes59/20212/descargas/entorno histórico archivados; aceptación editorial de tesis externa. Sensibilidades del plan que cambian protocolo no ejecutadas y explícitas, no fallos ocultados.

Condición de avance: nueva autorización de fase posterior y definición prospectiva de escenarios/pregunta/soporte sin alterar ganador o estimando por métricas. No se avanzó ni simuló. No push.

**Prompt siguiente preparado, no ejecutado:** Continúa en el proyecto y ejecuta únicamente la fase posterior que autorice expresamente el usuario. Lee AGENTS, continuidad vigente, protocolo/decisiones y README/informe de fase4; consulta solamente la sección correspondiente del plan. Verifica huellas de base/protocolo/fases3–4 y Git, conserva originales y cambios existentes. Documenta cualquier diferencia antes de cálculos. Si se autorizan escenarios, define previamente entradas plausibles y controles de soporte con modelos congelados, sin reselección ni afirmaciones causales; consulta solo decisiones materiales no resolubles con evidencia. Genera notebooks desde Python editable, verifica ejecuciones reales y registra resultados desfavorables. Cierra con entregables/continuidad/commit local; no push.
