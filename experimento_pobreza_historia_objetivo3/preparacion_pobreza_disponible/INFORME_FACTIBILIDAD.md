# Factibilidad documental de pobreza disponible antes de predecir

Consulta y cierre: 12 de octubre de 2026, America/Bogota. Preparación documental v1. No se ejecutó experimento, modelos, ajustes, escenarios ni objetivo 4. No se heredan presupuesto, candidatos o meta del contraste cerrado.

**Resultado: cierre documental incompleto respecto de los controles indispensables de procedencia y disponibilidad.** Se reconstruyeron fechas de productos oficiales y dos intervalos de publicación de bases Saber 11. No se demostró que los valores de los archivos locales pertenecieran a las ediciones disponibles en cada corte. Por ello no se certifica retrospectivamente una predicción factible. El trabajo documental y su conservación sí son verificables con `verificar_documental.py`; su aprobación no autentica datos.

## Qué se comprobó

El calendario detallado `CALENDARIO.csv` contiene 134 filas: IPM y cada una de las quince tasas en los siete años locales, un antecedente original de IPM 2018, las dos aplicaciones locales Saber 11 por año y sus siete medias anuales. `REFERENCIAS.json` identifica cada prueba por URL, consulta, ubicación, extracto e interpretación. `REGISTRO_PROCEDENCIA_REVISIONES.md` distingue eventos y ediciones. Las ubicaciones locales proceden de encabezados/notas ya auditados, del protocolo cerrado y de metadatos inspeccionados ahora; no se regeneró una base analítica.

| Año observado | Fecha de producto DANE departamental documentada | Qué permite afirmar |
|---|---|---|
| 2018 | Comunicado original 12/07/2019; revisión CNPV 2018 divulgada 14/07/2020 | Existió una edición previa y una recalibración posterior. Primera fecha de todas las celdas departamentales revisadas no demostrada. |
| 2019 | Edición del anexo 21/12/2020; publicación nacional 14/07/2020 | La fecha nacional no se transfiere automáticamente a las quince tasas departamentales. “Actualizada” no identifica primera publicación. |
| 2021 | 28/04/2022 | Fecha de anexo departamental; identidad de edición local pendiente. |
| 2022 | 23/05/2023 | Fecha de anexo departamental; identidad de edición local pendiente. |
| 2023 | 19/04/2024 | Anexo fechado; boletín corrigió un año escrito en página 3 el 07/05/2024. |
| 2024 | 22/04/2025 | Fecha de anexo departamental; identidad de edición local pendiente. |
| 2025 | 14/04/2026 | Coincide nominalmente con la nota local; comunicado reemplazado 20/04/2026, sin prueba de cambio del anexo. |

Pruebas: D2018ORIGINAL, DRECALIBRACION, D2019 y D2021–D2025 en `REFERENCIAS.json`. Las fechas son evidencia del **producto** publicado; ninguna prueba aquí demuestra todas las cifras locales en esas fechas. Para las tasas se identifica su pertenencia declarada al anexo por rótulos locales y auditoría previa, sin cotejo de contenido remoto histórico.

El DANE usa ECV para IPM; el boletín 2025, páginas 2–3 y tabla 5, identifica organismo, metodología, porcentaje de personas y cobertura de 32 departamentos más Bogotá. Los libros locales rotulan las quince tasas como privaciones por hogar. Es un enlace ecológico entre residentes y puntajes agrupados por colegio; no iguala hogares, personas y estudiantes. Prueba DMETODO2025 y `METADATOS_LOCALES.json`, `rotulos_privaciones`; auditoría v2, sección IPM.

Para Saber 11, el producto local declarado deriva de TXT por aplicación, con una media anual propia. El informe de gestión 2021, página 146, registra carga anonimizada de calendario A durante el tercer cuatrimestre de 2021. El informe de rendición, páginas PDF 111–112, registra revisión y publicación de Saber 11 2023 A y B durante el primer trimestre de 2024. Son intervalos de eventos reportados por el organismo, sin día ni identificación de versión. La equivalencia concreta entre aplicaciones/calendarios del informe y TXT locales no se autentica. Pruebas I2021CARGA e I2023CARGA.

El inventario enlazado actual de DataIcfes declara Saber 11 1996–2024 a nivel estudiante. La imagen de nuevas bases anuncia cambios en desagregaciones; el calendario de Fase II encontrado no incluye Saber 11. Estos documentos no establecen primeras fechas históricas. Las fechas de agregados públicos de ICFES son de otro producto y sus filtros actuales difieren de los locales; no sustituyen la procedencia de los TXT. Pruebas IDATA, IINVENTARIO, INUEVAS, ICALENDARIO, IAGREGADOS e IESTADISTICAS. No se accedió al repositorio de bases con registro ni se solicitaron credenciales.

## Cortes y cobertura documental

`CORTES_PROPUESTOS.csv` contiene dos opciones por respuesta 2021–2025 y cinco fechas posteriores a la publicación de pobreza del mismo año. Son cálculos documentales por comparación de fechas, sin leer puntajes ni errores. El día siguiente a una publicación evita asumir una hora que no está documentada.

| Respuesta anual | Opción 1: 1 de enero, 00:00 Bogotá | Último año de pobreza con producto fechado anterior al corte* | Opción 2: 1 de julio | Último año con producto fechado anterior* |
|---|---|---|---|---|
| 2021 | 01/01/2021 | 2019 | 01/07/2021 | 2019 |
| 2022 | 01/01/2022 | 2019 | 01/07/2022 | 2021 |
| 2023 | 01/01/2023 | 2021 | 01/07/2023 | 2022 |
| 2024 | 01/01/2024 | 2022 | 01/07/2024 | 2023 |
| 2025 | 01/01/2025 | 2023 | 01/07/2025 | 2024 |

\* Universo documental restringido a años locales conservados y con fecha departamental documentada; 2020 sigue excluido. No se afirma que sean el último producto de todos los existentes. IPM/tasas y sus valores exactos solo serían elegibles tras autenticar edición y contenido en cada corte. La fecha de 2018 revisado sigue abierta. Procedimiento: `fuentes/generar_calendario.py`, `releases` y comparación estricta `date < cut`.

**Recomendación nueva, pendiente de decisión del usuario:** considerar 1 de enero para anticipar la media anual de ambas aplicaciones. Su justificación es el periodo objetivo anual y evitar que una parte de la respuesta ya haya sido observada; no errores favorables. La evidencia no impone una decisión de uso. La opción 1 de julio aprovecha productos de pobreza más recientes, pero requiere revisar si una aplicación académica ya ocurrió: no se presenta como anticipación de toda la respuesta anual. Convertirla en predicción de calendario A solamente cambiaría respuesta/población y sería otra pregunta, con autorización separada.

La pobreza contemporánea 2021–2025 aparece documentada en el año siguiente. Los cortes 29/04/2022, 24/05/2023, 20/04/2024, 23/04/2025 y 15/04/2026 para sus respectivos años observados describen una estimación contemporánea o reconstrucción posterior, no anticipación anual. Aunque el puntaje aún no fuera descargable, su periodo ya transcurrió. No se elige un corte posterior a conocer la respuesta para llamarlo pronóstico.

Se conserva como objetivo inicial el universo histórico de **165 pares, 33 territorios × respuestas 2021–2025**, y media recibida `prom_punt_global`. Es cobertura nominal del diseño previo, no cobertura disponible certificada. Actualmente hay **0 pares retrospectivamente certificados** bajo los controles indispensables: no significa datos faltantes o inexistentes, sino ausencia de autenticación de ediciones y calendario conjunto Saber. La cobertura condicionada máxima sería 165 si se resolvieran todos los controles y entradas; no se asegura que sea alcanzable. La tabla no construye ni exporta filas de un panel.

La historia requiere dos puntajes anuales anteriores efectivamente disponibles. El ejemplo de 2023 A+B publicados durante 2024 impide garantizar `y_2023` al 01/01/2024. Cambiar a historia más antigua, excluir filas o cambiar ventana puede reducir cobertura o alterar la pregunta: debe declararse antes de evaluar. Los controles deben afectar por igual la referencia histórica y la ampliada; no imputar disponibilidad por conveniencia. Mantener el salto 2019→2021 sin anualizar y excluir 2020 no permite inventar las fechas de los puntajes.

## Año no examinado

El último año local es 2025, según la continuidad superior, protocolo y `resultados/FECHA_LOCAL.json`. Se encontró en la página oficial ICFES un resumen preliminar de calendario B 2026 (I2026), sin acceder a sus resultados. **2026 es un candidato cronológico condicional, no un año anual comparable demostrado ni una prueba independiente reservada.** No hay aquí archivos de ambos periodos autenticados, filtros comparables, media anual, pobreza 2026 ni historial de quién examinó los resultados. No se incorporan datos. La existencia de una noticia, calendario o resumen preliminar no resuelve esos controles.

Los años 2018, 2019 y 2021–2025 constan vistos en las continuidades; nuevas evaluaciones de 2021–2025 serían exploratorias. 2020 permanece excluido, no se rescata como año independiente. Declarar confirmación requeriría documentar que un año comparable no intervino en decisiones, además de separar entrenamiento/evaluación y sellar protocolo antes de examinar su respuesta.

## Qué impide autorizar una ejecución concreta

Faltan autenticación de la cadena archivo local→edición oficial; calendario efectivo de ambas bases Saber y revisiones por año; disponibilidad de las quince tasas exactas, especialmente edición revisada 2018; elección humana de fecha/uso; definición prospectiva de ventanas, tratamiento de entradas no disponibles, candidatos, evaluación, criterio práctico y presupuesto nuevo. Alternativa verificable: obtener certificados/versiones documentales históricas o una colección oficial con fechas y huellas, sin usar versiones posteriores para certificar un pronóstico anterior. La preparación actual no autoriza esa adquisición de datos ni ejecución.

Si solo se obtienen valores revisados actuales, podría proponerse una reconstrucción exploratoria con fechas de productos y advertencia explícita de revisiones; no una validación de factibilidad histórica. Si se desea un experimento prospectivo, habría que reservar un futuro corte y congelar los archivos existentes en ese momento, con autorización nueva. Ambas alternativas mantienen la pregunta incremental, pero tienen distinto alcance de evidencia.

No hay causalidad: comparar precisión predictiva no permite atribuir cambios del puntaje a modificar pobreza. El contraste anterior permanece cerrado, sin repetirlo, cambiar sus criterios ni reabrir incidencias históricas resueltas. Ningún avance automático.
