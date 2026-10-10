# Hallazgos, impacto y resolución de fase1

Fecha2026-10-10. Evidencias en resultados/, procedimientos en fuentes/.

| Hallazgo y evidencia | Impacto | Alternativa lógica y decisión | Verificación/estado |
| --- | --- | --- | --- |
| Trabajo v2 encontrado sin continuidad/cierre; Git742c665, snapshot encontrado | No atribuir ejecuciones anteriores a esta sesión ni sobrescribir trabajo | Reutilizar rama, repetir en copia temporal y comparar, conservar entregables | reproduccion_actual.json;24 archivos idénticos, ocho pruebas aprobadas. Resuelto |
| Candidato sin IPM y3.003 discrepancias Saber; cotejo_candidato.csv por llave/variable/fila | No cumple estimando de grado11, perdería precisión histórica | Reconstrucción separada desde raw filtrado e IPM local, conservar candidato | diagnóstico sin grado11 reproduce3.003 celdas;198 líneas históricas exactas. Resuelto |
| Dos IDs raw repetidos; identificadores_repetidos_revision.json por periodo/línea | Deduplicar por ID alteraría población sin fundamento | Revisar filas completas, controlar unicidad elegible, mantener raw | Cada grupo tiene dos filas distintas y solo una elegible; dictamen inicial conservado en antecedentes. Resuelto con advertencia |
| Guainía238 completos/404 global disponible; diagnóstico anual código94 | Sensibilidad al filtro de otras pruebas, no causalidad identificada | Mostrar ambas medias y proporción excluida; conservar estimando y filtros | diferencia21,012106; concentracion_otras_pruebas.csv. Resuelto como límite, causa desconocida |
| 20251 aporta26 territorios elegibles; controles_complementarios.json | Cobertura por periodo distinta de anual, promedio de medias no ponderadas sería incorrecto | Sumar numeradores/denominadores de ambos periodos, no fabricar casos | 20252/anual33;429 cotejos exactos de segunda lectura y medias por periodo. Resuelto |
| Saber11 frente Pre Saber no autenticado externamente; categorías/esquemas locales | Limita certificación del origen, no permite afirmar identidad oficial | Comprobar coherencia local, filtrar grado11 y explicitar alcance | Sin categoría Pre Saber explícita; sin cambio poblacional ni descarga. Límite de procedencia |
| Anexo cambia nombre de hoja de indicadores y tiene fecha2026; cifras_xlsx.csv y notas | Lectura rígida o confusión de fecha alteraría unión/año | Mapear hoja real, años/Total y variables por encabezado, registrar celdas | 3.696 entradas cotejadas, cero revisiones históricas; no reemplazos. Resuelto |
| Exclusiones históricas raw por territorio no disponibles en evidencia agregada consultada | No se puede afirmar estabilidad territorial histórica de faltantes | Comparar filtros históricos por periodo y conteos2024/2025 por territorio, explicitar límite | comparacion_filtros_historicos.csv y comparacion_cobertura_territorial_2024_2025.csv. Sin recenso histórico innecesario |

2020 excluido definitivamente: ningún TXT2020 leído ni cifras2020 extraídas o
sensibilidades realizadas. Las notas generales del anexo que mencionan2020 se
conservaron como texto de fuente, sin auditar ese año. No se reabren los problemas
archivados de selección59 o causa antigua20212: no afectan estos controles.

Lecturas PDF efectivas de este turno: ninguna. No resultados predictivos nuevos.
