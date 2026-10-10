# Hallazgos y controles de cierre — fase 5

Las decisiones previas están en decisiones_previas.md. No se produjeron problemas materiales que requirieran cambiar el protocolo o consultar al usuario.

| Evidencia | Impacto | Alternativa verificable | Decisión / comprobación |
|---|---|---|---|
| Tablas seleccionadas vs pregunta del plan sobre persistencia | Ausencia de una referencia impide afirmar superioridad sobre ella | Limitar comparación a media/OLS existentes | Informe§§1,6 declara no evaluada; sin nuevo ajuste |
| metricas_reevaluacion.csv: OLS IPM menor MAE que GBR IPM en ambos años | Complejidad no mejora siempre; RMSE conjunto difiere de patrón MAE | Mostrar MAE y RMSE con mismos datos | Informe§4 y verificacion_informe.py contrastan cifras; ganador global intacto |
| metricas_agrupadas.csv / bootstrap_resumen.csv: tasas favorable, rango tasas−ambas cruza0 | Ventaja territorial no universal | Presentar comparación pareada ya ejecutada | Informe§5 y control numérico; sin reselección |
| asociaciones_longitudinales.csv / colinealidad.csv | Explicación geográfica no identifica mecanismo dentro del territorio | Separar asociaciones y coeficientes OLS existentes | Tabla10/figura4; sin inferir causalidad o importancia GBR |
| Primera inspección gráfica: pie temporal solapa etiquetas; leyenda de asociaciones cubre última fila | Reduce legibilidad y oculta puntos | Mover pie/leyenda sin alterar coordenadas | Corregido en fuente Python y regenerado; reinspección aprobada |
| Título inicial observado/predicho llamaba congelado al GBR de los tres diseños | Solo artefacto temporal final está congelado; ventanas/territorial tienen ajustes previos separados | Rotular configuración ganadora por diseño | Título corregido antes de cierre; paneles y pies identifican cada evaluación |
| Importación inicial matplotlib no podía crear caché en config de usuario | Aviso de entorno, sin impacto analítico | Fijar caché escribible en /tmp | MPLCONFIGDIR definido en fuente antes de importar; no modificación de archivos previos |
| Manifiestos antiguos contienen continuidad histórica | Falso incumplimiento si se compara con vigente | Excepción documentada solo de esa ruta histórica, cotejo cierre4 y snapshot | Controles inicial/final aprobados; ninguna excepción para base/protocolo/modelos |

Control Git final: se retiraron cachés Python generadas de la entrega y se normalizaron espacios de fin de línea de SVG desde el generador, sin alterar coordenadas. La escritura inicial del índice fue bloqueada por `.git` de solo lectura; el permiso técnico solicitado permitió registrar el cierre local. Estas incidencias no cambiaron resultados ni alcance.

No hay fallos de modelos nuevos porque no se entrenó. No se atribuyen causas a2024. No nuevas lecturas PDF; registro de referencias distingue antecedentes revisados previamente. Remuestreo permanece previo y condicional a errores fijos. Los antecedentes históricos archivados se conservan sin reabrirlos.
