# Procedencia y versiones históricas: cierre documental incompleto

Versión 1.0. Consulta documental: 12 de octubre de 2026, America/Bogota. La fase ejecutada comprende conservación, documentación oficial y cotejo de anexos agregados DANE. No habilita un experimento.

## Resultado verificable

Los dos libros locales de pobreza quedaron autenticados **frente a la descarga oficial actual**: los anexos departamentales 2024 y 2025 tienen exactamente las mismas huellas SHA256 que sus correspondientes archivos locales. La adquisición histórica local sigue sin constancia. Tampoco se probó que estos mismos bytes estuvieran publicados desde la fecha que hoy declara cada página.

El cotejo nuevo revisó todas las celdas pertinentes del dominio Total: 33 territorios × IPM y quince tasas × cada año local presente en cada edición. Son **31.152 comparaciones de celdas**, con repetición documental entre ediciones y libros, no 31.152 observaciones independientes. Las 30.168 comparaciones contra las siete ediciones recalibradas enlazadas hoy (2019, 2020 como soporte de 2018/2019, y 2021–2025) coinciden exactamente. La edición original de 2018 difiere en 492 de 528 celdas frente a cada libro local; suma 984 diferencias al cotejar los dos libros. En IPM difieren 32 de 33 territorios; en tasas difieren 460 de 495. Las 36 coincidencias de esa edición no identifican el vector recalibrado completo.

Evidencia: `RESUMEN_COTEJO.json`, `RESUMEN_COTEJO.csv`, `COTEJO_CELDAS.csv` y `DIFERENCIAS.csv`, producidos por `fuentes/cotejar.py:calculate`. Cada comparación lleva archivo, año, territorio, indicador, hoja y celda en ambos libros. Se exportan números únicamente para las diferencias; no se formó un panel ni se sustituyó valor local alguno. `ADQUISICIONES.jsonl` registra URL solicitada/final, instante actual, tamaño, huella y encabezados HTTP. `ESTRUCTURA_Y_NOTAS.json` conserva títulos, columnas y notas.

| Año observado local | Primera edición departamental cotejada con todo el vector local igual | Fecha declarada de ese producto | Alcance probado |
|---|---|---|---|
| 2018 | Anexo 2019, CNPV 2018 | 21/12/2020 | 528/528 celdas; no retrofechar al original de 12/07/2019 |
| 2019 | Anexo 2019 | 21/12/2020 | 528/528; página dice actualización, no historial completo |
| 2021 | Anexo 2021 | 28/04/2022 | 528/528 |
| 2022 | Anexo 2022 | 23/05/2023 | 528/528 |
| 2023 | Anexo 2023 | 19/04/2024 | 528/528 |
| 2024 | Anexo 2024 | 22/04/2025 | 528/528; identidad completa del libro local 2024 |
| 2025 | Anexo 2025 | 14/04/2026 | 528/528; identidad completa del libro local 2025 |

Ubicaciones: páginas oficiales conservadas `evidencia/dane_<edición>.html`, fila Anexo departamental; notas finales de las dos hojas en `ESTRUCTURA_Y_NOTAS.json`. **Primera edición cotejada** no significa primera publicación de cada valor. La nota metodológica del 14/07/2020 acredita el anuncio de actualización 2018/2019, pero no todas las 528 celdas departamentales locales en ese día (`../../evidencia_oficial/dane_nota2019.pdf`, páginas 1–3). El anexo 2019 aporta simultáneamente contenido y una fecha interna 21/12/2020, concordante con su página. Falta captura o constancia institucional histórica que enlace esos contenidos con el evento de publicación; el cotejo actual no elimina ese control.

## Saber 11: documentación encontrada y límite indispensable

Los catorce TXT locales permanecen identificados por sus huellas, tamaños y antecedentes de modificación (`PROCEDENCIA_TXT.json`, copia documental de metadatos previos; las huellas se revalidan en conservación). No se leyeron registros, recalcularon medias ni descargaron bases ICFES. La búsqueda local pertinente no encontró constancia de adquisición enlazada a esas huellas: las entregas previas ya declaraban su ausencia (`auditoria/diagnostico_calidad.md`, secciones conservación y cierre; `experimentos_objetivo3_v2/fase1/INFORME_AUDITORIA.md`, población y procedencia). No se afirma un inventario exhaustivo de todos los documentos del repositorio.

| Año y aplicaciones locales | Evidencia documental pertinente | Correspondencia con edición local |
|---|---|---|
| 2018, 1 y 2 | Informe gestión 2018 pp. PDF 146–147: FTP y publicaciones; no identifica ambos archivos 2018 | Nominal; sin fecha/edición/huella pública específica |
| 2019, 1 y 2 | Informe gestión 2019 p. PDF 70: revisiones Saber 2011–2014; no fechar 2019 con ellas | No demostrada |
| 2021, 1 y 2 | Gestión 2021 p. 146: carga anonimizada A en tercer cuatrimestre 2021; PAAC 2022 segundo cuatrimestre p. PDF 9, actividad 91: datos hasta 2021 completos | Evento A documentado; TXT 20212 no vinculado. La declaración general no identifica 20211 |
| 2022, 1 y 2 | PAAC 2022 tercer cuatrimestre p. PDF 9, actividad 91: última actualización Saber 11 junio 2022; no declara allí periodos 2022 | Sin fecha de ambas ediciones 2022; no asumir cobertura por año del informe |
| 2023, 1 y 2 | Rendición 2024 pp. PDF 111–112: revisión/publicación A+B en primer trimestre 2024 y actualización de diccionarios | Intervalo del evento; ninguna huella TXT vinculada |
| 2024, 1 y 2 | Gestión 2025 pp. PDF 46–47: nuevo repositorio, universo ampliado y Saber 11 hasta 2024 | Existencia general; no fecha inicial de ambas aplicaciones ni versiones locales |
| 2025, 1 y 2 | Página actual e inventario enlazado terminan en 2024; informes/medias agregadas 2025 son otros productos | No se encontró prueba indispensable de edición de los TXT 20251/20252; omisión del inventario no prueba inexistencia |

Referencias completas y huellas: `REFERENCIAS.json`; revisiones: `REGISTRO_PROCEDENCIA_REVISIONES.md`; calendario por aplicación: `CALENDARIO_EDICIONES.csv`. Los intervalos septiembre–diciembre 2021 y enero–marzo 2024 se conservan como eventos institucionales. **No** se usan sus extremos superiores como disponibilidad de los valores locales porque no se identificó su edición. La actualización de diccionarios y del universo de evaluados impide asumir que un mismo nombre de TXT represente una versión invariable. La página «Acceso a Bases de datos y diccionarios» consultada solo remite a pruebas 3°, 5°, 7°, 9°; no resuelve el diccionario histórico Saber 11 (`evidencia/icfes_acceso_diccionarios.html`, sección Datos abiertos).

## Factibilidad y cobertura

Quedan demostrados el origen oficial actual de los dos libros DANE, la igualdad de los valores pertinentes con las ediciones cotejadas y los eventos documentales especificados. La disponibilidad histórica de esos valores queda condicionada; la identidad y disponibilidad por aplicación ICFES no están demostradas. La cobertura inicial se conserva en **165 pares nominales**, con **0 certificados de manera conjunta** por los controles indispensables aún abiertos. Cero certificación no es ausencia de datos. El máximo condicionado de 165 tampoco es garantía de factibilidad.

`CORTES_REVISADOS.csv` revisa los quince cortes propuestos previamente: enero, julio y cortes posteriores al producto contemporáneo. Ninguno se adoptó. Para enero, los últimos años de pobreza nominalmente documentados dentro del universo inicial son 2019, 2019, 2021, 2022, 2023 para las respuestas 2021–2025; para julio: 2019, 2021, 2022, 2023, 2024. Las nuevas coincidencias refuerzan la correspondencia numérica, no sellan los bytes históricos. Persistencia, historia académica y respuestas de entrenamiento requieren sus propias ediciones disponibles al corte; un rezago de un año no basta. Los cortes posteriores a pobreza contemporánea no acreditan predicción anual anticipada.

No se redujo población, agregó 2020 o cambió ventana. Se mantienen `prom_punt_global`, ambos periodos y filtros del contraste, colegio, igual peso territorio-año, 2018 nivel, 2019 historia y salto 2019→2021 sin anualizar. El enlace de pobreza de residentes con estudiantes por colegio sigue siendo ecológico. Persistencia e historia sola permanecen referencias. Fuente: protocolo y continuidades previos; complemento propio `COMPLEMENTO_PROTOCOLO.md`.

## Año anual aún no examinado

La página oficial ICFES de análisis conserva un enlace preliminar B 2026 y productos anuales hasta 2025 (`evidencia/icfes_analisis.html`, sección Saber 11). Se revisó el listado, no los resultados enlazados. No demuestra respuesta anual A+B 2026 con los filtros iniciales ni edición de datos elegible. Tampoco documenta el historial externo de no examen de resultados por el investigador. Por tanto no se certifica un año anual comparable aún no visto. Todos los años locales 2021–2025 siguen siendo exploratorios; una reserva futura necesitaría protocolo y corte futuro explícitos.

## Pendientes y cierre

1. DANE: constancia/copia histórica del anexo departamental con contenido o huella vinculados al evento de publicación, principalmente 2018 recalibrado/2019; registro de revisiones suficiente para cada corte que se decida. La descarga actual igual a la local no reemplaza esa evidencia.
2. ICFES: constancia de adquisición local o manifiesto oficial por aplicación (URL/producto, periodo, edición, publicación/revisiones, huella y diccionario asociado). Sin bases nuevas se puede aportar documentación autenticada; obtener/recomparar bases necesitaría autorización separada. No se contactó a terceros.
3. Decisión humana de uso y fecha/hora de corte; enero 1 a las 00:00 Bogotá sigue pendiente. Después, cobertura común y cualquier cambio material de entradas/ventana/población; evaluación exploratoria o prospectiva, candidatos, criterio práctico y presupuesto nuevos, fijados antes de observar evaluación.

La investigación termina con **cierre documental incompleto verificable**. Conservación e integridad se verifican aparte de autenticación histórica y factibilidad científica. Cero ajustes, repeticiones, modelos, escenarios, nuevos datasets analíticos u objetivo 4. No se heredó meta del 5 %, candidatos ni presupuesto. No hay avance automático.
