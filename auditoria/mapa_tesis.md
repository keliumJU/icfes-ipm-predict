# Mapa de revisión de tesis e informes

Actualización 2026-10-08: el conjunto de páginas leídas no cambia. Los TXT nuevos permiten cerrar la reproducción local de filtros y conteos. La contradicción de pp. 115–117 tiene una propuesta separada en `propuesta_correccion_tesis.md` y un reemplazo descriptivo en `evidencia/actualizacion_20261008/tabla12_propuesta_198.csv`. No se editó ACA2 ni se afirmó aceptación del grupo.

Fecha: 2026-10-07. Referencias a páginas físicas del PDF, contadas desde1. En ACA2 coinciden con el número impreso. La extracción se realizó con `pdftotext -layout`; se localizaron primero objetivos, metodología, construcción, tablas de conteos, 2021 y la sección de asociación. **Extraer o localizar una página no equivale a revisarla.** El detalle página por página, incluidos los pendientes, está en `evidencia/mapa_paginas.csv` (hash del texto extraído, estado y revisión visual), regenerable con `procedimientos/mapear_documentos.py`.

## ACA2.pdf — 126 páginas

Se leyó el texto completo de58 páginas: **10–11,25,30–33,50–60,63–74,85–88,95–118**. Se conservaron tablas, notas, denominadores y continuidad entre páginas. Las pp.63–64 se leyeron pero su presupuesto no interviene en la auditoría. Se inspeccionaron visualmente pp.66,68,73,88,96–103,105,107,109,111,115–117. Las cifras críticas de tablas4/7 y la construcción alternativa se comprobaron tanto en texto completo como en la imagen de página.

| Páginas revisadas | Sección/evidencia | Resultado de auditoría |
|---|---|---|
| 10–11 | Resumen, 2.984.199, trayectoria y correlaciones | Distinguir población grado11 de panel histórico |
| 25 | Objetivos específicos3 y4 | Predicción departamental de desempeño; escenarios son objetivo4 |
| 30–33 | Alcances y limitaciones, 2020/2021, incertidumbre, no causalidad | Conservar límites; anticipación requiere IPM del año |
| 50–53 | Enfoque, diseño, población y ambos periodos, colegio | Población declarada grado11 y unidad departamento-año |
| 54–55 | ETL, esquema82, filtros, bilingüismo | Derivados locales79/59; mermas iniciales no verificables |
| 56–60 | Medidas, modelos planeados y validación | Leído para auditar correspondencia; no ejecutado. Clasificadores previos difieren del puntaje continuo |
| 65–67 | Calidad, tabla4 y nota de ambas aplicaciones | Conteos finales reproducidos; falta fuente20181 y flags previos |
| 68–70 | Figura1, controles, umbrales, IPM y tabla5 | Niveles reproducidos; identidad personal no verificada |
| 71–74 | Tablas6–7, notas, ponderación y figura2 | Reproducción de tabla7; se mantienen discrepancias de redondeo |
| 85–88 | Grupos, tabla9, precisión y figura8 | IC2024 verificados contra XLSX; sin inferir certeza de límites de grupos |
| 95–103 | Puntajes, mapas, niveles y trayectoria por pobreza | Lectura completa e imágenes; descenso2021 válido en población grado11 |
| 104–107 | Correlaciones, tabla10 y figura20 | r global reproducida; 42 cifras de seis pruebas cotejadas |
| 108–111 | Cambios extremos, figuras21–22 | r de diferencias2018–24 no es efecto fijo ni causalidad |
| 112–114 | Tabla11, discusión y conclusiones | Leídas; tabla11 complementaria no se reproduce íntegramente en esta fase |
| 115–117 | Otra unión,160 celdas, presentación, sinBogotá/2021, tabla12 | Contradicción documentada; 32 correlaciones reproducidas bajo hipótesis descrita; artefactos históricos ausentes |
| 118 | Inicio de referencias | Referencias pertinentes se verifican por fuente primaria cuando se usan; no revisión bibliográfica completa |

**Pendientes de lectura completa:**1–9,12–24,26–29,34–49,61–62,75–84,89–94,119–126 (68páginas). Predominan portada/índices, antecedentes, teoría, cronograma, descriptivosIPM y referencias fuera del foco de esta fase. No se afirma haber revisado la tesis completa. Las figuras de páginas no listadas como revisión visual no se presentan como cotejadas visualmente. No hay páginas indispensables de construcción de resultado/objetivo3 pendientes de lectura en los bloques localizados; lo pendiente indispensable es evidencia de origen y artefactos ausentes.

La lectura de pp.56–60 corresponde a auditar lo que propone ACA2 y su correspondencia con el objetivo3, **no a ejecutar las fases2–6 de PLAN_OBJETIVO_3.md**. No se tomó de esos capítulos permiso para modelar.

## Informes previos

- `prom.pdf`,24 páginas: leído texto completo1–23; página24, gráfica de escenarioE3, inspeccionada como imagen. Objetivos/metodología1–2; descripción de variables3–9; código y muestra10–13; resultadoslogística14; RF15–19; XGB19–23. La página24 no contiene tabla numérica de probabilidades: no se extrajeron valores exactos del gráfico.
- `nueva ivestigacion .pdf`,11 páginas: todas leídas completas. Recomendaciones1–4; respuesta sobre clasificadores y métricas5–7; escenarios y afirmaciones de políticas8–11. Se identifica el cambio de partición165/33 frente132/66 y se separa clasificación de regresión.

El mapa contiene161 páginas en total. No se guardan copias de los textos completos ni renders en Git; los originales y su SHA-256 se conservan en el inventario. Las citas detalladas de afirmaciones están en `auditoria_afirmaciones.csv`.
