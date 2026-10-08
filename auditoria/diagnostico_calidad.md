# Diagnóstico de calidad y trazabilidad — fase 1

Actualización: 2026-10-08, America/Bogota. Commit de partida de esta sesión: `77c286f43a3c6d811fc68ba9399fd5ec99277528`. Git comenzó con una modificación del usuario en `.gitignore`, que no se modifica ni incluye en el commit. La auditoría previa permanece en `historico/diagnostico_calidad_20261007.md` y en el historial de Git. Esta actualización sustituye sus pendientes de procedencia local cuando los nuevos controles los resuelven.

## Dictamen actual

**Queda validada la reconstrucción analítica departamental desde los TXT locales para la población, los campos críticos, los puntajes y la unión con IPM.** Los originales aportados permiten reproducir los filtros y completar el periodo 20181. Se entrega una base agregada de 198 celdas, con 2.984.199 registros de grado 11, y su diccionario. No se entrenaron modelos, no se imputaron puntajes y no se avanzó a fase 2.

El cierre de la fase 1 conserva salvedades de autenticación histórica: no se conoce el criterio original de selección de 59 columnas, no hay metadatos de descarga ni logs del fallo antiguo, y no se dispone de artefactos para verificar las métricas de los clasificadores previos. Esas ausencias se registran con dictamen explícito; no se presentan como resultados reproducidos ni se exigen modelos nuevos para resolverlas. La reconstrucción actual no depende de aquella selección de columnas ni del panel incompleto de la raíz.

La validación abarca 16 campos críticos compartidos: periodo, seis geocódigos, grado, fecha de nacimiento, género y seis puntajes. No afirma igualdad de todos los atributos socioeconómicos, autenticación del archivo publicado en un servidor ni unicidad de personas entre aplicaciones. Fuente y condiciones: `evidencia/actualizacion_20261008/validacion_reconstruccion.json`, `resumen_raw.json`, `conservacion_raw_final.csv`; procedimientos `auditar_raw_20261008.py` y `actualizar_entrega_20261008.py`.

## Insumos actuales y conservación

`raw_data/` contiene los doce periodos del universo y cuatro adicionales de 2020 y 2025. Se inventarían los 16 TXT con tamaño y SHA-256; únicamente los doce de 2018–2024 sin 2020 se leen completos para los controles. Los adicionales se inspeccionan por encabezado y permanecen fuera del análisis. `Datos anteriores a la limpieza/` ahora se llama `Datos anteriores a la unificacion/`: los once CSV tienen exactamente las huellas previas. El consolidado individual también conserva su huella.

`inventario_trazabilidad.csv` conserva la ruta de la entrega previa, la ruta actual y la fecha de verificación. Incluye 49 archivos y dos directorios vacíos, con 28 datasets ignorados por Git. `Resultados Guardados/` y `Entorno de ejecución/` siguen vacíos. Los TXT se describen como originales locales aportados por el usuario; no se inventa una URL o fecha de descarga. Evidencia: `inventario_nuevos_y_renombrados.csv` bajo la carpeta fechada y control final de conservación.

## Filtros reproducidos sobre todos los registros

Cada TXT relevante se lee con `csv.reader`, validando el ancho de cada fila; los cálculos emplean bloques de 100.000 y columnas necesarias. Los filtros se inspeccionaron en los cinco scripts de preparación, sin ejecutarlos ni cambiar sus entradas. Los controles nuevos reproducen dos cadenas explícitas: la secuencia de tabla 4 y la conjunción FIX más limpieza final.

| Etapa secuencial de control | Conservados | Merma respecto de etapa anterior |
|---|---:|---:|
| Doce TXT recibidos | 4.039.755 | — |
| `ESTU_ESTUDIANTE = ESTUDIANTE` | 3.433.542 | 606.213 |
| Excluir libertad `S` confirmada | 3.432.366 | 1.176 |
| Global y cinco pruebas disponibles y >0 | 3.401.100 | 31.266 |
| Código departamental del colegio no nulo | 3.401.100 | 0 |
| Grado numérico 11 | 2.984.199 | 416.901 |

Se reproducen los conteos de ACA2 pp. 66–67. La cadena ejecutable de FIX aplica simultáneamente global válido, departamento por cascada, estudiante y libertad: conserva 3.432.344; agregando colegio y las seis pruebas conserva 3.401.100. No se confunden filtros concurrentes con mermas secuenciales disjuntas. Fuente: `filtros_raw.csv`, controles `01_recibido`–`06_grado11`, `script_FIX` y `script_FIX_mas_final`.

Los doce TXT tienen cero filas con ancho incorrecto y cero periodos distintos del nombre del archivo. En sus 4.039.755 filas no hay identificadores `ESTU_CONSECUTIVO` faltantes ni repetidos, tampoco repetición de ese identificador entre periodos. Es un identificador de registro de aplicación; no se convierte en una afirmación de personas únicas. Los IDs no se guardan en archivos de auditoría ni en Git. Fuentes: `filtros_raw.csv`, `resumen_raw.json`.

Los 3.401.100 registros del consolidado coinciden **bidireccionalmente** con el filtrado raw en los 16 campos críticos, sin casos sobrantes ni firmas ambiguas, en cada uno de los doce periodos. La comparación solo normaliza representación de enteros y relleno de día/mes; no cambia puntajes ni población. Los once CSV de 59 columnas conservan, en esa misma proyección, todas las filas de sus respectivos TXT, sin casos sobrantes en ninguna dirección. Fuentes: `conservacion_raw_final.csv`, `conservacion_raw_periodicos.csv`.

## Calendarios, grados y transformaciones

El grado 11 conservado incluye calendario A: 2.901.089, B: 78.075, OTRO: 5.034 y faltante: 1. **No se añadió un filtro A/B** ni se reinterpretó el sufijo del periodo como calendario del colegio. La población validada se describe por grado y los filtros explícitos; no como población exclusivamente de calendario A/B. Fuente: `calendarios_raw.csv`, población `06_grado11`.

Los `_limpio` tienen 59 columnas y son derivados, no originales. El normalizador suministrado excluye identificador, calendario y otros campos y proyecta al esquema canónico; no implementa la selección histórica a 59. La conservación observada no demuestra igualdad de cada atributo ni explica por qué se descartó una columna. La nueva reconstrucción usa la población identificable en TXT y los campos críticos verificados, evitando depender de ese recorte desconocido. Esquemas: `esquemas_raw.csv`, `columnas_omitidas_59.csv`; código: `normalizar_txt_icfes.py`, `DROP_COLS` y `normalizar_archivo`.

Se comprobaron 608.458 bilingüismos faltantes en registros elegibles antes de la sustitución documentada por N; en 20241 los 20.485 elegibles no tienen ese atributo en raw. Coinciden con ACA2 p. 55 y el comportamiento escrito de `limpiar_datos_final.py`. La auditoría no imputa ni utiliza bilingüismo en la base departamental. Fuente: `filtros_raw.csv`, `bilingue_faltante_final`; categorías del consolidado de la entrega previa.

## 2021 y diferencia de versiones

Se cierra la conservación actual de 20212: sus 606.030 filas raw producen 534.706 registros elegibles y 480.252 de grado 11, todos presentes en el consolidado. El TXT aportado tiene encabezado separado por `;`. El usuario recuerda un fallo de lectura antiguo; se registra como antecedente, sin afirmar que este TXT actual demuestre un defecto tabulado histórico. No se recrea el fallo ni se excluye 2021.

El panel raíz sigue siendo una versión anterior que conserva solo 20211 en 2021: 15.514 registros y cinco territorios sin resultado. El conjunto actual tiene 550.220 registros de ambos periodos y 494.331 grado 11. La diferencia neta preliminar de 117.805 se explica por 534.706 omitidas de 20212 menos 416.901 fuera de grado 11. Se conserva el panel original y se entrega otra base; no se corrige silenciosamente. Fuentes: nueva conservación raw; `panel2021_vs_periodo20211.csv`, `reconciliacion_anual.csv` y `respuestas_pendientes_20261008.md`.

## Puntaje global y otras advertencias

Las **525 diferencias de fórmula retenidas en 20222 ya están en el TXT**, con la misma distribución: 414 grado 11, 111 grado 26, discapacidad N, diferencias +1 a +12 puntos respecto de la fórmula diagnóstica. Por tanto, no se introdujeron al unificar. En los TXT completos con cinco pruebas positivas hay 527 diferencias, dos adicionales en 20181 que no sobreviven todos los filtros. No se conoce la regla/versión que explica esas diferencias; no se atribuyen a recalificación, discapacidad o edición manual. Se conservan los globales recibidos y ninguna diferencia se usa como nuevo filtro. Fuentes: `formula20222_raw.csv`, `filtros_raw.csv`; fórmula documentada en ambos procedimientos de contraste.

Permanecen los controles anteriores: seis puntajes en rango en el consolidado, 13.604.400 comparaciones de niveles sin discrepancia, 683.744 INSE faltantes y 4.621 valores >100 (umbral exploratorio, no rango oficial). INSE queda fuera de la base principal. Se mantienen tres diferencias de precisión en 24 cifras de tabla 7 y dos en 42 correlaciones de puntajes de tabla 10; no se ajustan criterios o redondeos para igualar la tesis. Fuentes: `niveles_desempeno.csv`, `inse_exploratorio.json`, `cotejo_tabla7_declarado.csv`, `cotejo_tabla10_puntajes.csv`.

## Base entregada, IPM y diccionario

`base_analitica_departamento_anio.csv` contiene 198 llaves únicas, 33 territorios por año, sin nulos y con suma de 2.984.199 registros. Años: 2018, 2019, 2021, 2022, 2023 y 2024; unidad: departamento del colegio-año. Se incluyen conteos y medias de seis puntajes, IPM y 15 tasas marginales. Cada media es suma / denominador propio, sin redondeo intermedio. Se cotejan los conteos anuales contra grado 11 raw. El código DIVIPOLA se conserva con dos dígitos. No contiene registros personales.

El diccionario distingue conteos, puntos, códigos, incidencia en porcentaje de personas y privaciones marginales rotuladas por hogar. No hay imputación de puntajes ni cambio de universo. IPM se une por código/año, con cardinalidad uno a uno y coincidencia de todas las llaves. Las 3.168 cifras ya fueron cotejadas contra celdas del XLSX local; las notas ECV/CNPV2018, captura rural 2021 y marco de agua rural 2019–2020 permanecen aplicables. Esas notas no explican pérdida administrativa de Saber. Fuentes: `diccionario_base_analitica.csv`, `cotejo_ipm_celdas.csv`, `notas_ipm.csv`, `identidades_ipm.csv`; detalle histórico de IPM conservado en el diagnóstico anterior y `fuentes_verificadas.md`.

## Tesis y afirmaciones históricas

La contradicción de pp. 53–69 frente a 115–117 se resuelve en la auditoría mediante una **propuesta formal de sustitución**, sin editar ACA2 ni afirmar aceptación del grupo. `propuesta_correccion_tesis.md` ofrece texto para conservar colegio, grado 11, 2021 y Bogotá. `tabla12_propuesta_198.csv` recalcula las 16 asociaciones de la construcción principal. IPM/global da −0,7215676 en 198 celdas y −0,7521243 entre medias de 33 territorios. Son descriptivos, no efectos causales ni selección automática de predictores.

La tabla antigua se reproduce bajo otra construcción de 160 celdas, presentación y exclusión de 2021/Bogotá; se conserva como evidencia histórica distinta. Los cuatro artefactos citados allí siguen ausentes: no se autentica su ejecución. La edición por el grupo queda como acción editorial, sin impedir documentar y verificar una construcción coherente.

La matriz mantiene 59 afirmaciones y columnas que conservan sus dictámenes/evidencia/pendientes al 2026-10-07. Actualiza lo resuelto por raw. Las métricas de los clasificadores previos se mantienen «históricas reportadas, no reproducidas». No se solicitan nuevos entrenamientos. Continúan las correcciones sobre umbral ≥250, log-odds, ceros penalizados, Gini/gain, Brier, INSE y simulaciones no causales. Fuentes: `auditoria_afirmaciones.csv`, informes previos y procedimientos inspeccionados; detalle en diagnóstico histórico.

## Cierre y límites

Los pendientes indispensables para verificar la construcción local del resultado quedaron resueltos con la reconstrucción explícita y sus controles. La fase 1 cierra **para esta base local y este alcance**, con desconocidos históricos debidamente rotulados. No se declara certificada la descarga oficial ni explicada la regla aritmética de las 525 diferencias. Si se aportan otras versiones o documentación ICFES, deben inventariarse y contrastarse sin sobrescribir originales ni cambiar filtros para mejorar métricas.

Quedan acciones posteriores: que el grupo decida incorporar la propuesta; obtener metadatos de descarga, criterio histórico de 59 columnas o artefactos antiguos solo si se pretende autenticar aquellos procesos; consultar la explicación oficial de diferencias globales si aparece evidencia. Ninguna se presenta como realizada. Esta sesión no ejecuta fase 2; una continuación necesita mantener explícita la población aquí validada y el alcance de sus salvedades.

Versiones actuales: Python 3.12.14, pandas 2.2.3 y numpy 2.3.5; no son versiones históricas verificadas. Orden, memoria, rutas, límites y control de conservación: `procedimientos/README.md`. El mapa de páginas de ACA2 permanece igual: no se simula una nueva lectura completa ni se revisan páginas fuera del foco para declarar avance.
