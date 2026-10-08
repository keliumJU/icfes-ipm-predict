# Diagnóstico de calidad y trazabilidad — fase 1

Fecha: 2026-10-07, America/Bogota. Commit de partida: `c288074795f2c8b1b4865b73f8e08561cecd4448`. Git estaba limpio; no existía continuidad. Se conserva cada original y `.gitignore`. No se entrenaron modelos, seleccionaron predictores ni ejecutaron escenarios. Solo se audita la fase 1 de `PLAN_OBJETIVO_3.md`.

## Dictamen y límite de validación

**La auditoría tiene un avance verificable, pero no está terminada: falta cerrar la procedencia y los filtros previos.** La anomalía grave de 2021 pertenece al panel de la raíz. El consolidado individual actual contiene la cohorte 20212 y permite reproducir internamente la población de grado 11 y los principales descriptivos de ACA2. No hay fundamento para excluir 2021 automáticamente. No se imputó ningún puntaje.

Se separan tres objetos que antes se confundían:

| Objeto | Población efectivamente observada | Cobertura | Estado |
|---|---|---|---|
| `panel_departamento_anio_unido.csv` de la raíz | Todos los grados del consolidado depurado, pero 2021 conserva solamente 20211 | 198 llaves IPM, 193 resultados Saber, 2.866.394 filas individuales agregadas | Versión histórica recibida, incompleta en 2021 |
| `Saber_11_Listo_2018_2024.csv` local | 3.401.100 registros; `ESTU_ESTUDIANTE=ESTUDIANTE`; 414.635 grado 26 y 2.266 otros grados además de grado 11 | Doce periodos en seis años, incluido 20212 | Insumo derivado actual, no fuente original verificada |
| Reconstrucción de control `grado11_control` | 2.984.199 registros con grado numérico 11 | 198 celdas, 33 territorios por año; mínimo 190 en Guainía 2021 | Validada internamente contra conteos y descriptivos; cadena de origen pendiente |

Fuentes: `evidencia/reconciliacion_anual.csv`, `categorias_Saber_11_Listo_2018_2024.csv`, `agregados_Saber_11_Listo_2018_2024.csv`, `resumen_tesis.json` y `resumen_recomprobacion.json`; procedimientos `comprobar_datos.py`, `contrastar_tesis.py` y `resumir_evidencia.py`. Las cantidades representan filas administrativas, no personas únicas demostradas.

**No se entrega base analítica ni diccionario de una base validada.** Los agregados en `evidencia/` son tablas de comprobación separadas de los originales, no autorización para modelar. Para validar de extremo a extremo faltan los originales, el insumo de 20181, identificadores y registros de las transformaciones. También hay una discrepancia de fórmula global en 20222 pendiente de explicación. Esto impide presentar la cadena completa como reproducida.

## Objetivo vigente y contradicciones de la tesis

El objetivo 3 aprobado en el documento vigente es diseñar un modelo departamental que estime el desempeño a partir del IPM y sus componentes (ACA2, p. 25). La metodología define como resultado el puntaje global promedio, no una categoría ≥250 (p. 58). La población es grado 11 regular, ambos periodos de cada año, asignada al departamento del colegio; seis años sin 2020 (pp. 52–55). Los tres scripts previos son clasificadores del promedio ≥250; constituyen antecedentes y no una ejecución del resultado continuo planteado.

ACA2 contiene una contradicción interna indispensable. Las pp. 53–69 describen 198 celdas, colegio, 2021 completo y 33 territorios. La sección de pp. 115–117 describe 160 celdas, departamento de presentación, sin 2021 ni Bogotá y otra selección por correlación. Los scripts `unir_datos.py`, `correlaciones_predictoras.py` y los archivos `Resultado_de_la_asociacion.xlsx` y `Correlaciones_variables_predictoras.xlsx` citados allí no están en el inventario. Su ejecución histórica no puede verificarse. El IPM local sí tiene Bogotá completo en seis años.

Como hipótesis de reconstrucción documental, se aplicó exclusivamente para el cotejo la población grado 11 y geografía de presentación de p. 115, en 2018, 2019, 2022, 2023 y 2024. La unión actual tiene 165 celdas con IPM; retirando Bogotá para contrastar el texto quedan 160. Se reproducen las 16 correlaciones entre medias territoriales y las 16 correlaciones sobre celdas de la tabla 12 a tres decimales. Esto respalda sus cifras bajo esa construcción, pero no autentica archivos históricos ni justifica las exclusiones. No se adoptó ese subconjunto como base principal ni se excluyó 2021 del control completo. Evidencia: `cotejo_tabla12_hipotesis.csv`, `resumen_seccion115.json`; procedimiento `contrastar_seccion115.py`.

La tabla 4 (p. 66 y nota p. 67) declara 4.039.755 originales y una secuencia de filtros. Sus conteos finales sí coinciden con el consolidado actual; sus mermas iniciales no se pueden verificar con fuentes de 59 columnas sin las variables de estudiante y libertad. La afirmación de censo completo (p. 53) requiere contrastar cobertura con los originales publicados; la ausencia de duplicados exactos no demuestra unicidad de personas. `mapa_tesis.md` distingue lectura completa de páginas, extracción y revisión visual.

## Inventario, procedencia y transformaciones

`inventario_trazabilidad.csv` registra tamaño y SHA-256 de todos los insumos relevantes, incluyendo **los doce CSV ignorados por Git**: once `_limpio` periódicos y el consolidado individual. No se limitó el inventario a `git ls-files`. `Resultados Guardados/` y `Entorno de ejecución/` están vacíos. El repositorio de partida solo tiene un commit; no aporta versiones anteriores de datasets ni modelos. Las filas de directorios vacíos carecen de huella porque no son archivos.

Los once CSV periódicos suman 3.973.901 filas. Falta `Examen_Saber_11_20181_limpio.csv`; 20181 sí aparece con 19.714 filas ya filtradas en el consolidado. La diferencia entre las 4.039.755 filas declaradas en la tesis y las once fuentes locales es 65.854; **no se trata como un conteo verificado de un original ausente**. No hay TXT originales ni carpeta `recuperacion_20212/` suministrada. Fuentes: inventario y `controles_todos.csv`, control `filas`.

Los `_limpio` no son originales. Tienen 59 columnas, mientras el normalizador documenta una selección canónica de 77, y el consolidado tiene esas 77 más `DEPTO_ANALISIS` y `ANIO`. Los 59 campos omiten 18 campos de fuente presentes en el consolidado, entre ellos `ESTU_ESTUDIANTE`, `ESTU_PRIVADO_LIBERTAD`, niveles, percentiles y atributos institucionales (`evidencia/columnas_omitidas_59.csv`). La selección a 59 no está documentada por un procedimiento suministrado. Además, el propio `normalizar_txt_icfes.py` elimina identificador `estu_consecutivo`, calendario y códigos de establecimiento/sede, entre otros; por tanto tampoco su producto puede llamarse original (líneas 15–21 y 39–57).

| Script inspeccionado, no ejecutado | Transformación documentada | Límite de reproducción |
|---|---|---|
| `normalizar_txt_icfes.py` | Detecta `;`, tab o coma y UTF-8/Latin-1; normaliza encabezados; proyecta al esquema tomado de primer archivo con `;`; omite columnas y 20201/20202; exporta `;` | Faltan TXT; no explica 59 columnas. Canon no garantiza por sí mismo exactamente 77 |
| `limpiar_columnas_icfes.py` | Lee consolidado con coma; convierte global; departamento por cascada colegio/residencia/presentación; normaliza nombres; conserva global >0, departamento y no libertad S; exporta `;` | No filtra `ESTU_ESTUDIANTE`; no limita grado ni exige cinco pruebas completas |
| `limpiar_consolidado_fix.py` | Lee consolidado FIX con `;`; rechaza tab en encabezado; global válido; cascada departamental; filtra estudiante y libertad si existen; reporta mermas por periodo e intersecciones | Sin campos ausentes acepta todos; no equivale a filtrar estudiantes verificados. Faltan entradas FIX y sus reportes |
| `limpiar_tildes_nombres.py` | Quita tildes/puntuación, homologa Bogotá/San Andrés/Valle y otras variantes; regla amplia para Nariño; cambia tres nombres geográficos | No cambia códigos ni valida cada correspondencia; intermedio ausente |
| `limpiar_datos_final.py` | Exige código del colegio no nulo; zfill de dos dígitos; año de periodo; global y cinco pruebas >0; bilingüismo faltante a N; CSV con coma | No filtra grado 11 ni valida lista oficial de códigos. El comentario «población regular» no demuestra condición escolar |
| `unir_divipola.py` | Código numérico del colegio y año derivado de periodo; sumas/count propios por variable; medias a dos decimales; unión exterior con IPM | No filtra grado; cambia código a entero; no valida cardinalidad en merge original. Exporta coma, distinto del panel raíz |

Ubicaciones: scripts originales incluidos en el inventario; líneas/funciones indicadas en `auditoria_afirmaciones.csv` y `dependencias_scripts.csv`. Las tablas de control son procedimientos nuevos, guardados en `auditoria/procedimientos/`; no se adaptó ni sobreescribió un original.

La comparación de multiconjuntos sobre 16 campos compartidos encontró **cero filas consolidadas sin correspondencia en cada uno de los once periodos con fuente local**. Antes de comparar se normalizaron representaciones numéricas (`05`, `5.0`, `5`) y el relleno de día/mes de nacimiento; no se cambiaron valores de fuentes. Esta proyección respalda la conservación de periodo, grado, geografía codificada y seis puntajes. No demuestra identidad individual, todos los demás atributos ni motivo de exclusión. 20181 sigue sin fuente. Fuente: `conservacion_registros.csv` y función `normal`/`scan` de `comprobar_registros.py`.

## Periodos, población, códigos y denominadores

Se recorrieron íntegramente los once periódicos y el consolidado. Los controles de calidad y agregación usaron columnas necesarias en bloques de 100.000; la verificación de estructura y repetición exacta leyó todas las columnas lógicas de cada fila CSV. En total esa comprobación estructural cubrió 7.375.001 registros locales (incluye los mismos registros en etapas diferentes, no se suma como población).

Todos tienen el número de campos esperado (59 o 79); no se encontraron tabs en campos ni filas completas repetidas por SHA-256 (`estructura_duplicados.csv`). El identificador individual falta: no se verifican repeticiones de persona entre aplicaciones ni se deduplica por firmas incompletas.

El consolidado contiene `20181, 20182, 20191, 20192, 20211, 20212, 20221, 20222, 20231, 20232, 20241, 20242`. No hay 2020 ni año discordante entre `ANIO` y los primeros cuatro dígitos de `PERIODO`. La ausencia de `COLE_CALENDARIO` impide auditar calendario A/B por registro: el sufijo del periodo no se presenta como sustituto documental de ese campo. Los controles cubren los 3.401.100 registros del consolidado.

Los seis puntajes están presentes, son numéricos, positivos y están en rango global ≤500/pruebas ≤100 en el consolidado. Todos los códigos de colegio corresponden al conjunto de 33 códigos departamentales del anexo local. El consolidado usa códigos con cero inicial; el agregador los convierte a enteros. La asignación por colegio no equivale a residencia ni presentación: hay 39.641 registros con colegio/residencia codificados distintos y 75.857 con colegio/presentación distintos, contando solo pares no nulos (`discrepancias_geograficas.csv`). No se mezcla la cascada de nombres con la llave de colegio empleada para agregar.

Las medias se reconstruyen como suma de puntajes / número no nulo del puntaje dentro de cada territorio-año. `n_estudiantes_saber` cuenta filas; `n_punt_*`, `n_percentil_global` y `n_estu_inse_individual` cuentan valores disponibles propios. No son unidades de puntaje. En los seis puntajes coinciden los denominadores del consolidado; en INSE no: hay 683.744 nulos. El promedio de los 33 territorios da igual peso territorial; el promedio de estudiantes usa sumas y conteos individuales y no promedios ya redondeados (`contrastar_tesis.py`).

## Reconciliación exacta de 2021 y de los conteos

| Año | Consolidado actual, todos grados | Grado 11 actual | Panel raíz | Diferencia consolidado − panel |
|---|---:|---:|---:|---:|
| 2018 | 573.270 | 478.689 | 573.270 | 0 |
| 2019 | 572.788 | 495.224 | 572.788 | 0 |
| 2021 | 550.220 | 494.331 | 15.514 | 534.706 |
| 2022 | 557.656 | 497.562 | 557.656 | 0 |
| 2023 | 577.021 | 516.936 | 577.021 | 0 |
| 2024 | 570.145 | 501.457 | 570.145 | 0 |
| Total | 3.401.100 | 2.984.199 | 2.866.394 | 534.706 |

Fuente: `reconciliacion_anual.csv` y controles completos. La diferencia 2.984.199 − 2.866.394 = **117.805** se descompone como **534.706** filas de 20212 omitidas en panel, menos **416.901** filas fuera de grado 11 retenidas en su población de partida. No es una pérdida aislada de 117.805 estudiantes.

En 2021, los conteos y seis promedios del panel de raíz coinciden exactamente con los del periodo **20211** del consolidado actual, en las 168 comparaciones (28 departamentos × seis pruebas). Fuente: `panel2021_vs_periodo20211.csv`, deltas de conteo y promedio todos cero. El panel no incorpora 20212: el consolidado sí tiene 534.706 filas de ese periodo. Los otros cinco años tienen 165 celdas con conteos y medias coincidentes entre panel raíz y agregado actual de todos los grados (`comparacion_panel_recibido.csv`).

Las cinco celdas sin Saber son Chocó (27), San Andrés (88), Amazonas (91), Vaupés (97) y Vichada (99) en 2021. Entre las celdas observadas hay Sucre n=1, Arauca n=2, Guaviare n=2 y Casanare n=9. El promedio simple 2021 del panel es 272,105714, sobre **28** territorios; su promedio de estudiantes usando promedios redondeados es 302,281774. No puede compararse como si representara el promedio de los 33 territorios de grado 11.

`limpiar_consolidado_fix.py` menciona un encabezado tabulado y una recuperación; `normalizar_txt_icfes.py` implementa detección de delimitador. Son pistas de una causa histórica posible. **La omisión de 20212 está demostrada en la composición del panel; la causa técnica exacta no.** Los archivos locales actuales están estructuralmente bien separados. Sin TXT defectuoso, consolidado previo, fecha de ejecución y mermas no se prueba que un tab haya causado el fallo; tampoco que la pandemia haya producido la pérdida administrativa.

## Comprobación de tesis y muestras de modelos previos

La restricción a grado 11 reproduce exactamente los seis conteos de las tablas 4 y 7. Los promedios departamentales actuales son 249,9824; 244,1667; 242,7596; 247,2658; 249,5167; 253,1518. La correlación IPM/global en 198 celdas es −0,7215676 y la correlación entre cambios 2018–2024 por 33 territorios es −0,0769716. Los 33 territorios bajan 2018–2019 y suben 2021–2024. Fuentes: `contraste_tabla7.csv`, `resumen_tesis.json`. Son descriptivos reproducidos desde un derivado local, no causalidad ni validación del origen completo.

También se conservaron discrepancias finas, sin ajustar criterios para igualar cifras: de 24 cifras de la tabla 7 cotejadas, tres difieren a un decimal con redondeo directo: IPM medio 2022 =20,748485 →20,7, frente20,8; DE global2022=16,848792 →16,8, frente16,9; promedio estudiantes2023=258,153152 →258,2, frente258,1. De 42 correlaciones de puntajes de la tabla10 cotejadas, dos difieren a dos decimales: global2018=−0,784925 →−0,78 frente−0,79; lectura del periodo=−0,764984 →−0,76 frente−0,77. No se supone cuál fue el redondeo o la versión histórica. Evidencia: `cotejo_tabla7_declarado.csv`, `cotejo_tabla10_puntajes.csv`. La fila de proporción nivel3–4 de tabla10 no está incluida en ese cotejo de seis puntajes.

| Versión de comprobación | Celdas hasta2022 | Promedios ≥250 hasta2022 | Celdas2023–24 | Promedios ≥250 en2023–24 |
|---|---:|---:|---:|---:|
| Panel raíz, solo `_merge=both` | 127 | 50 | 66 | 29 |
| Consolidado completo, todos grados | 132 | 41 | 66 | 29 |
| Consolidado, solo grado11 | 132 | 61 | 66 | 39 |

Fuente: `reconciliacion_muestras.csv`. **132/41 y66/29 de `prom.pdf` sí coinciden con el consolidado completo sin restricción de grado**; 127/50 de la revisión preliminar describe el panel raíz defectuoso. No se demostró que las métricas provengan de un archivo con la misma huella que el consolidado actual. El hallazgo permite plantear la reconstrucción de la muestra histórica, no certificar AUC, Brier, coeficientes ni hiperparámetros.

Los scripts originales leen coma pero el panel raíz usa `;`; no ejecutarían directamente sus selecciones de columna sobre esa serialización. `unir_divipola.py` exporta coma: el historial entre formatos no fue suministrado. Además, los comentarios que dicen excluir2021 contradicen el filtro ejecutable, que incluye2021. SGKF agrupa departamentos, no bloquea el tiempo dentro de desarrollo. Se suprimen todas las advertencias en los scripts originales, por lo que no hay evidencia de convergencia histórica. Ningún modelo ni probabilidad guardada está disponible.

## IPM: procedencia, unidades, llaves y comparabilidad

El CSV de IPM tiene 198 llaves únicas, 33 territorios en seis años, 16 variables numéricas por llave, cero nulos. **Las 3.168 cifras coinciden exactamente con el XLSX local**, incluyendo Bogotá; el panel raíz también reproduce esos valores. `cotejo_ipm_celdas.csv` conserva hoja/celda, filaCSV y diferencia para cada comparación. La incidencia usa totales departamentales de `IPM_Departamentos` B/E/K/N/Q/T (años no2020); las tasas usan totales de `IPM_Variables_Departamento ` C/F/L/O/R/U, no columnas de cabeceras o rural. Se homologa el nombre al código de la tabla local sin mezclar regiones ni total nacional.

El anexo declara ECV y expansión basada en CNPV2018, actualizado el22 de abril de2025 (`notas_ipm.csv`: `IPM_Departamentos` A49–A54; variables A863–A869). Son estimaciones de la encuesta para departamentos; no se identificó una sustitución por estimaciones municipales SAE ni por privaciones censales en estos insumos. La incidencia es porcentaje de personas pobres; las tasas marginales de privación se rotulan por hogar. No son denominadores intercambiables ni una suma lineal que produzca la incidencia. ACA2 explica identificación conjunta y umbral en pp.69–70.

Las notas distinguen en2020 el uso de SIMAT–C600–ECV para inasistencia, en2021 la fotografía para servicios rurales, y en2019–2020 un cambio de nivel de agua rural por marco CNPV2018. Se guardan sin convertirlas en causa de cobertura de Saber. 2020 permanece en el XLSX original y no se introdujo al CSV o a la reconstrucción. En 2024 los IC tienen amplitud media4,8212pp y13 departamentosCV>10%, que reproducen ACA2 pp.86–88. El anexo también publica intervalos desagregados por sexo en otras hojas; no se afirma que cualquier forma de intervalo solo exista en2023–24.

La incidencia ajustada está almacenada como fracción (por ejemplo0,063; formato `0.000`), pese al encabezado de porcentaje; H y A están en porcentajes. Para comparar en puntos porcentuales se multiplica aquella fracción por100 y se usa H×A/100. El error máximo es0,0802pp, compatible con0,08 redondeado. Las cinco contribuciones suman99,9–100,1;84 de198 difieren de100 exactamente por0,1pp, por lo que la afirmación «todas suman100» requiere la salvedad de redondeo (`identidades_ipm.csv`).

La captura `archivo-IPM-descargado.png` muestra14/04/2026 y470KB; no muestraURL nihuella. El XLSX local declara actualización2025 y tiene396.132bytes. La captura no acredita qué archivo se descargó. El sitio oficial DANE para la edición2024 lista el anexo con fecha22/04/2025; no se descargó otra versión ni se sustituyó el insumo. Véase `fuentes_verificadas.md`; la coincidencia de cifras es con el **archivo local**, no una certificación de la descarga histórica.

## Hallazgos adicionales y límites de interpretación

La reconstrucción de cuatro niveles completos por prueba, con los límites oficiales documentados, coincide en **13.604.400 comparaciones** del consolidado, con cero discrepancias. Incluye todos los grados depurados, no solamente grado11 (`niveles_desempeno.csv`). No justifica llamar «satisfactorio» a un promedio global≥250: los niveles son por prueba. La regla≥250 de los modelos es un umbral analítico escogido.

La fórmula estándar `redondear(5×[3×(Mat+Lect+Nat+Soc)+Ing]/13)` difiere del global recibido en **525 registros de20222**, todos con discapacidad reportadaN:414 grado11 y111 grado26, diferencias positivas de1–12puntos. La misma distribución aparece en el `_limpio` periódico de20222. Se requiere original/versión y regla aplicable; no se afirma que sean errores del ICFES ni se corrige el global. Fuentes: `formula_global.csv`, `formula_global20222_detalle_agregado.csv`, `diagnosticos_adicionales.py`. Se conserva la fórmula como diagnóstico y no se convierte en un nuevo filtro.

INSE tiene683.744 nulos,4.621 valores>100 y máximo806,353. El umbral100 es un control exploratorio, **no un rango oficial de INSE verificado**. Las seis variables de puntaje están dentro de rango. El grado también contiene categorías distintas de11/26 (100grado10,696grado12,1.392grado25 y3 con valor20234); se registran sin reinterpretar sus significados ni incluirlos en grado11. Fuentes: `inse_exploratorio.json`, `categorias_Saber_11_Listo_2018_2024.csv`.

La matriz `auditoria_afirmaciones.csv` contiene59 afirmaciones, clasificadas como respaldadas, parcialmente respaldadas, incorrectas o no verificables. Cada fila diferencia evidencia documental histórica, reproducción actual e hipótesis, con ubicación y corrección. Las correcciones principales son:

- Un coeficiente logístico tras estandarización modifica log-odds por desviación estándar. No da directamente puntos porcentuales de probabilidad ni puntos Saber.
- Cero por penalización no prueba irrelevancia sustantiva. Los diez predictores no nulos reportados incluyen IPM; no son diez privaciones.
- Gini, gain y coeficientes usan escalas distintas; tampoco identifican efectos. Los rankings históricos ni siquiera coinciden exactamente en top4.
- Menor Brier no demuestra mejor calibración por sí solo. Véase [documentación primaria de calibración](https://scikit-learn.org/stable/modules/calibration.html).
- INSE no genera fuga automáticamente: depende de finalidad y disponibilidad. Se conserva su exclusión del modelo principal por el alcance acordado, sin entrenar para comprobarla.
- La incidencia IPM no es combinación lineal de15tasas marginales. Se conserva identificación conjunta y unidades de la fuente.
- Reducir entradas de un clasificador no evalúa políticas. Las afirmaciones de ineficacia educativa, retornos o «trampa» causal de Gemini exceden el diseño. ACA2 pp.32 y60 reconoce ese límite.
- `nueva_simulacion_educacion_vs_choque.py` multiplica por0,40, o sea reduce60%, mientras rótulos dicen−40% y−30% (líneas91–106 y150). Solo se inspeccionó.
- SHAP tiene unidades de la salida explicada, que pueden ser log-odds o probabilidad. No siempre puntos porcentuales; véase [TreeExplainer, parámetro model_output](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).
- 2023–24 ya se usaron para comparar modelos y elegir uno (`prom.pdf` pp.14,18,22; nuevo informe pp.5–7). Una evaluación posterior no será inédita.

## Dependencias, versiones y reproducción

Se usó el Python3.12.14 incluido en el runtime actual, pandas2.2.3, numpy2.3.5, openpyxl3.1.5 y pdftotext del sistema. `entorno_actual.json` registra ejecutable, plataforma y distribuciones; `dependencias_scripts.csv` registra imports y líneas de cada script original sin importarlos ni ejecutarlos. El Python por defecto del sistema es3.14.7 y no tiene las bibliotecas usadas; no se usó para procesar los datos. scikit-learn, xgboost, matplotlib y seaborn no están instalados en el intérprete de auditoría. No eran necesarios ni se instalaron para entrenar.

Estas son **versiones actuales**, no el entorno histórico de los informes. Falta lockfile, registro de ejecución y artefactos de modelos. Los comandos y el orden de reconstrucción de evidencias están en `procedimientos/README.md`. No se versionan datos grandes, registros individuales, hashes de personas, imágenes de páginas ni textos completos extraídos; los resultados son agregados compactos.

## Pendientes indispensables y condición de avance

1. Recuperar los TXT originales de los doce periodos, en particular20181, y metadatos de descarga. Mantenerlos fuera de Git grande, con tamaño/huella y ubicación verificables.
2. Obtener el procedimiento real de selección59columnas, los consolidado pre-FIX/FIX, los intermediarios antes/después de filtros y los reportes de recuperación20212. Verificar cada merma con campos originales de estudiante/libertad; documentar cuáles versiones produjeron el panel raíz y el consolidado actual.
3. Recuperar el identificador original y calendario para comprobar unicidad/duplicados y cobertura por calendario; no sustituir esos controles por una firma de16campos.
4. Reconciliar las525 diferencias de fórmula global20222 con la versión/regla de la fuente. Conservar puntajes recibidos hasta disponer de evidencia.
5. Resolver la contradicción de población, geografía, años y territorios entre pp.53–69 y115–117; obtener los cuatro artefactos citados en la sección añadida o documentar formalmente su sustitución. No editar la tesis original en esta fase.
6. Para autenticar métricas históricas, faltan base con huella, probabilidades, modelos y entorno. En esta fase se dejan como históricas no verificables; no se autoriza entrenar para «recrearlas».

**Condición para fase2:** población/grado, cobertura temporal y geográfica, denominadores, puntajes y cadena de origen verificables; elección de una construcción coherente con el objetivo vigente, explícita y documentada. 2021 no está excluido. La regla condicional de exclusión del plan no se activa por el panel viejo: hay datos actuales de2021, pero aún debe cerrarse su trazabilidad. El cierre de esta sesión usa el commit de avance y pendientes; `CONTINUIDAD_OBJETIVO_3.md` da una continuación concreta, sin pasar a fase2.
