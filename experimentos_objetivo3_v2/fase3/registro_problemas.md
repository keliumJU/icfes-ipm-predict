# Registro de problemas y decisiones — fase 3

Fecha del cliente: 2026-10-10, America/Bogota. Solo fase 3 autorizada.

| ID/origen | Evidencia | Impacto sobre objetivo | Alternativa | Decisión/comprobación | Estado |
|---|---|---|---|---|---|
| F3-01/comprobación | resultados/integridad_inicial.json | Partida o fuentes distintas impedirían reproducción | Cotejo Git, manifiesto y panel sin reconstrucción | HEAD 0664ac21100982006d1a20670c7e987879444dc6; rama solicitada; panel y 198 históricas exactas; manifiesto fase2 verificado | Resuelto |
| F3-02/comprobación | resultados/entorno.json | Entorno supuesto podría cambiar defaults/resultados | Validar entorno existente contra todas las líneas del lock | Python3.12.14 y versiones exactas; pip check; sin instalación/red | Resuelto |
| F3-03/prueba sintética | resultados/incidencia_sintetica_inicial.json | Fixture entero impide ensayo de fuga extremo | Crear y sintético float64 | Prueba repetida con salida0 en pruebas_sinteticas.log; cero ajustes reales durante prueba | Resuelto antes del piloto |
| F3-04/prueba sintética | resultados/prueba_extremo_fallida.log | Extremo 1e100 excede float32 interno de árboles y detiene evaluación sintética | Usar extremo representable 1e20 manteniendo comparación idéntica de selección | Prueba aprobada; no cambia población, rango real ni política numérica | Resuelto antes del piloto |
| F3-05/revisión estática previa al primer recálculo | fuentes/verificar_resultados.py condición subcadena '_i'; fuentes/enmienda_reporte.py | '_ipm' también coincide: agregado etiquetado interno incluiría externos IPM; selección y métricas leen rutas temporales exactas, sin impacto predictivo | Reconocer regex completa eAAAA_iAAAA_ID | Extensión explícita reconstruye agregado interno de CSV con etiquetas temporales; exige 49.500 filas sin fallos. No modifica fuentes congeladas ni fases1–2; se verifica al cierre | Resuelto mediante enmienda de reporte, comprobado:49.500 internas y particiones/roles exactos |

| F3-06/comprobación de conteos sin métricas | resultados/conteo_enmienda.json: 2022, 9 externos y cero fallos; protocolo §7 | Cota8/1550 omite posibilidad de global distinto de ganador por especificación | Conservar roles requeridos y deduplicar solo IDs iguales | ENMIENDAS_TECNICAS.md E3-02 corrige cota descriptiva a9/1555; sin cambios de selección/código ni repetición; tope7200s prevalece | Resuelto por enmienda aritmética |

Los controles sintéticos y dobles no son métricas reales ni tiempo del presupuesto del panel.
El código operativo de ajustes, selección y ledger permanece congelado. Las extensiones
posteriores de entrega no cambian criterios ni modelos; su huella final queda en manifiesto.

Advertencias activas heredadas: casos completos y Guainía, procedencia local sin
autenticación independiente, comparabilidad IPM, colegio/residencia de hogares y enlace
ecológico, dependencia temporal/territorial y pocos años. Se conservan población/filtros,
media global recibida, peso igual y especificaciones. Exclusión definitiva 2020: sin auditoría
ni sensibilidad. No se interpretan predicciones como efectos causales; 2025 exploratorio,
no reserva inédita. Umbral 5% práctico, no significancia estadística.

Antecedentes 59/esquema82, causa histórica20212 y fórmula global desconocida continúan
archivados en protocolo v1 §8 y decisiones_fase2 D10/D12/D13; sin evidencia nueva que
los conecte con el piloto actual, no se reabren ni se inventa documentación histórica.
PDF efectivamente leídos en fase3: ninguno, cero páginas.

## Hallazgos del piloto realmente ejecutado y cierre

| ID/origen | Evidencia | Impacto | Alternativa | Decisión y comprobación | Estado |
|---|---|---|---|---|---|
| F3-07/reproducción actual | verificacion_resultados.json:1552 ajustes,1540.906905419055s, cero fallos; reproducibilidad.json:10 repeticiones, diferencia0 | Procedimiento completo y comparación calculable sobre165 llaves iguales | Recalcular desde CSV y comprobar cobertura/huellas/particiones | Aprobado;49.500 internas y51.216 predicciones por artefacto verificadas;9 procedimientos con165 externas | Resuelto |
| F3-08/reproducción actual | metricas.csv/verificacion_resultados.json: MAE v2 4.879557188161031, v1 5.979303244989078; mejora18.392545281085766% | Umbral futuro≥5% se satisface; no autoriza fase4 en este turno | Conservar regla prospectiva exacta y posponer entrega personal | Cálculo independiente sin redondeo de condición, denominador positivo; no notebook personal ni fase4 | Resuelto dentro de fase3; fase4 pendiente de autorización |
| F3-09/reproducción actual | deterioros.csv, procedimiento_v2:0/5 años y8/33 territorios deterioran MAE | Mejora conjunta no implica beneficio uniforme por territorio ni causalidad | Entregar métricas y deterioros íntegros, sin exclusiones ni clipping | Reporte conserva ambos niveles y todos los territorios; población/pesos intactos | Resuelto, advertencias activas |
| F3-10/reproducción actual | metricas.csv, ambas MAE4.821934448903931 frente global4.879557188161031 | Elegir especificación con externo sería selección retrospectiva | Mantener procedimiento principal congelado; comparar especificaciones descriptivamente | Se conserva mejora18.392545281085766% del procedimiento global, sin sustituirlo por ambas | Resuelto sin cambiar criterio |

Conteo efectivo:1500 internos+42 externos deduplicados+10 repeticiones=1552. La enmienda
aritmética E3-02 explica diferencia respecto de estimación1550 sin ampliar búsqueda ni
presupuesto. Todas las repeticiones y referencias consumen el mismo saldo. Advertencias
capturadas se detallan en fallos.json, sin ConvergenceWarning/fallos de ajustes.

Notebook de lectura de resultados generado desde fuente Python editable, validado con
nbformat y tres celdas realmente ejecutadas mediante Python exec (no kernel Jupyter),
sin ningún ajuste adicional. Originales y fases1–2 comprobados por huellas al cierre.
