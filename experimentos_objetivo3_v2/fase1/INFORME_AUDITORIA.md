# Auditoría v2 — fase 1: datos2025 y conservación

Fecha: 2026-10-10, America/Bogota. Partida efectiva `742c66577abaeade216d0498e4ecfd12d4c7abfb`, sucesor del cierre v1 `fc8dc23de8a85cffcc1c87d47ac740650b27ace5`. Solo fase1. No modelos, métricas predictivas, simulaciones o notebooks nuevos. Sin búsquedas externas ni PDF nuevos.

## Resultado y población

Se censaron **661,891 registros** de ambos TXT locales2025 con CSV por bloques100.000, y una segunda lectura completa con pandas. Se retienen **496,499** bajo los filtros del protocolo v1 (§1): estudiante, no libertadS, seis puntajes positivos/disponibles, código del departamento del colegio y grado11. Sin filtro de calendario. Son registros, no personas únicas. Evidencias: `resultados/filtros_raw_2025.csv`, `categorias_poblacion.csv`, `calendarios_2025.csv`, fuentes `auditar_2025.py:masks/audit_raw/independent_sum`.

Los nombres Saber11, campos y categorías (grado11/25/26 e individuales) son compatibles con los TXT históricos; no se observa una población Pre Saber identificada en estos campos. Esto valida coherencia local de las fuentes aportadas, **no autentica descarga o producto oficial independientemente**. No se infiere identidad personal por ID.

| etapa | periodo20251 | periodo20252 | total |
| --- | --- | --- | --- |
| 01_recibido | 85678 | 576213 | 661891 |
| 02_estudiante | 21793 | 547381 | 569174 |
| 03_sin_libertad | 21753 | 547190 | 568943 |
| 04_seis_puntajes | 21610 | 538923 | 560533 |
| 05_codigo_colegio | 21610 | 538923 | 560533 |
| 06_grado11 | 14143 | 482356 | 496499 |
| administrativo_grado11 | 14225 | 489717 | 503942 |
| diagnostico_global_disponible | 14225 | 489715 | 503940 |

Los registros físicos tienen ancho y periodo correctos. Cero puntajes fuera del rango documentado entre elegibles; códigos elegibles válidos y cobertura33. La segunda lectura reproduce exactamente **429 conteos/sumas**: 33territorios × 13variables de control. Evidencia: `cotejo_segunda_lectura.csv`, `verificacion_auditoria.json`.

## Consolidado candidato: no corresponde al filtro grado11

El candidato aportado se conserva intacto. Falta IPM y hay **3003 discrepancias** en las13 columnas Saber críticas: 429por año, incluidos2018–2024; no se corrigen originales. Sus15 tasas coinciden en todas las231 filas con el anexo. Evidencia: `cotejo_candidato.csv`, columna `coincide`, llave/celda y fila del candidato.

El diagnóstico de procedencia coteja sus conteos y medias con la agregación sin filtrogrado11: **3003/3003 coincidencias**, usando las medias redondeadas a dos decimales. Para2018–2024 se emplea evidencia anterior, no nuevos censos; para2025, agregación actual raw. Ubicaciones: `diagnostico_origen_candidato.csv`, fuente `documentar.py:main`, histórico `auditoria/evidencia/agregados_Saber_11_Listo_2018_2024.csv`, subconjunto `recibido`. Por tanto no se utiliza ese consolidado como base principal: incorpora registros excluidos por el estimando acordado y precisión redondeada. La reconstrucción conserva el filtro, no cambia la pregunta.

## Faltantes y diagnóstico de selección

No se convirtieron nulos en0 ni se imputaron puntajes. Los faltantes, ceros, negativos/no numéricos se distinguen, con estados que pueden coexistir entre variables; no sumar sus frecuencias como personas únicas. Evidencia: `faltantes_territorio_periodo.csv`; mermas secuenciales y combinaciones concurrentes separadas en `filtros_territorio_periodo.csv` y `combinaciones_exclusiones.csv` (bits1/2/4/8/16: estudiante/sinlibertad/seispuntajes/código/grado11).

Entre filtros administrativos de grado11, 503,940 tienen globalpositivo; exigir las otras pruebas retiene 496,499, una diferencia de 7,441 registros (1.476565%). En inglés se observan76+7.245 nulos y3+95 ceros en esos filtros administrativos; hay también ceros en otras áreas y dos globales0 en20252. Ubicación: `faltantes_territorio_periodo.csv`, población `administrativo_grado11`; `tabla_filtros_resumen.csv`.

**Mayores diferencias anuales entre media de casos completos y media con globaldisponible** (diagnóstico separado; no nueva respuesta principal):

| departamento | n_completos | n_global_disponible | media_completos | media_global_disponible | diferencia |
| --- | --- | --- | --- | --- | --- |
| Guainia | 238 | 404 | 241.848739 | 220.836634 | 21.012106 |
| La Guajira | 8562 | 9956 | 237.983532 | 231.359883 | 6.623648 |
| Vichada | 546 | 656 | 223.333333 | 217.099085 | 6.234248 |
| Choco | 4956 | 5346 | 214.018160 | 210.388328 | 3.629832 |
| Risaralda | 8739 | 8927 | 263.133768 | 261.684777 | 1.448992 |

Guainía presenta diferencia de aproximadamente21,01puntos, con238casos completos frente404 con global disponible. Esto demuestra sensibilidad descriptiva al filtro en ese territorio; no demuestra el mecanismo de los faltantes, sesgo frente a toda la población ni causa de errores predictivos. Ubicación: `diagnostico_medias_disponibles.csv`, alcance `anual`, código94. El objetivo principal sigue siendo la media de registros elegibles con las seis pruebas. No se selecciona población según futuros MAE.

Las mermas2025 se comparan con filtros históricos en `comparacion_filtros_historicos.csv`, conservando su etiqueta histórica. No se repiten censos2018–2024 ni se promete igualdad de composición entre años. Pocos años, dependencia territorial, selección por registros y enlace ecológico permanecen.

## Identificadores raw repetidos: resolución sin deduplicar

Se detectan dos grupos con el mismo ID en20252. La revisión de las filas completas encuentra dos filas distintas en cada grupo y solo una elegible. La otra no es grado11; por tanto no se duplica la población retenida. Se conserva todo raw y no se deduplica por ID. `identificadores_repetidos_revision.json` guarda únicamente ubicaciones y estados agregados, sin IDs/firmas personales.

La primera verificación rechazó la ampliación por unicidadraw y no exportó panel. Se conserva su dictamen en `antecedentes/primera_verificacion_ids_raw.json`. Enmienda documentada antes de exportar: verificar unicidad de **IDs elegibles**, mantener la repeticiónraw como advertencia y repetir censo. Todos los controles indispensables actuales pasan. No se oculta el rechazo inicial ni se afirma que los IDsraw sean únicos.

## IPM, cobertura y ampliación

El XLSXlocal2025 contiene incidencia departamental y15privaciones: hojas `IPM_Departamentos` e `IPM_Indicadores_Departamento `, encabezados de año en fila12 y dominioTotal en fila13. IPM2025 está en W y tasas2025 en X; se verifica por encabezados, no por nombre del archivo. Se cotejan528entradas nuevas y3.168históricas, sin extraer cifras2020. Las históricas no tienen diferencias frente a basev1 (0 revisiones encontradas). Fechas y advertencias en `notas_ipm_2025.csv`; celdas exactas en `cifras_xlsx.csv`, encabezados en `encabezados_ipm_2025.csv`.

La fecha14abril2026 es actualización/publicación, no año de observación. Se mantienen IPM%personas y tasas%hogares, dominioTotal. El enlace de colegio con hogares residentes sigue siendo ecológico; no implica efecto individual o causal.

**Ampliación validada: True**. `reconstrucciones/base_analitica_departamento_anio_v2.csv`:231filas,33territorios × siete años2018,2019,2021–2025, sin2020. Las198líneas históricas se conservan literalmente, sin reemplazar cifras; se añaden33líneas2025 desde raw y XLSX. Total3,480,698registros; SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`. Conteos por año: {2018: 478689, 2019: 495224, 2021: 494331, 2022: 497562, 2023: 516936, 2024: 501457, 2025: 496499}.

## Pruebas, conservación y condición de avance

Los tests de datos y pruebas negativas constan en `pruebas_auditoria.json`; no son tests de modelos ni notebook de experimentos. Los controles temporales, escalado, selección, métricas y presupuesto del piloto permanecen prospectivos en fase2. No nuevos notebooks en fase1.

Snapshot de311archivos previos y7fuentes;169huellas de manifiestos anteriores verificadas, con continuidades históricas cotejadas en sus commits y cambio de informe del usuario conservado. `integridad_inicial.json` fija partida; `conservacion_final.json` y manifiesto cierran sin excepciones a archivos existentes.

La base puede utilizarse en fase2 **cuando el usuario la autorice**. No entrenar ahora. El piloto futuro conserva100configuraciones/2horas y umbral práctico5%MAE frente a v1 reentrenada, sin exigencia3/5años. No hay resultado de mejora ni aceptación editorial del grupo. Procedencia de descarga y mecanismos de faltantes siguen como límites; no se sustituyen por una explicación inventada.
