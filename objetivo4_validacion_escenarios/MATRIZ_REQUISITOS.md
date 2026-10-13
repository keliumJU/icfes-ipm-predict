# Requisitos, evidencia y brechas de la fase

Estado: ejecución autorizada completada, no certificación de tesis completa. Las adaptaciones se predefinieron en PLAN_Y_PROTOCOLO.md. Original intacto: Tesis Vigente/ACA2.pdf.

| Requisito escrito | Estado de esta entrega | Evidencia verificable |
| --- | --- | --- |
| p.58, tres especificaciones base, IPM, dimensiones/tasas | Ejecutadas, con composición auditada nueva | preparacion/panel_enriquecido.csv; resultados/CONGELACION_PREVIA.json, specs; DECISIONES.json |
| p.58, Ridge/Lasso/ElasticNet | Ejecutadas, 15 candidaturas por especificación | fuentes/modelos.py, candidates/estimator/develop; seleccion_desarrollo.csv |
| p.58, efectos de año e indicador2021 | Adaptación explícita: tendencia para extrapolar, indicador2021 conservado | PLAN_Y_PROTOCOLO.md antes de evaluación; freeze protocol_sha |
| p.58, selección dejando un año fuera | Ejecutada como sensibilidad separada; primario temporal expansivo | metricas.csv method=loyo frente temporal; DECISIONES.json |
| p.59, entrenar hasta2022/evaluar2023–2024 | Ejecutado con132/66; años ya vistos | metricas.csv exercise=corte2022; predicciones.csv |
| Ampliación humana hasta2023/evaluar2024–2025 | Ejecutada con165/66; mismo modelo por dos años | metricas.csv exercise=corte2023; modelos/corte2023*.joblib |
| p.59, única prueba sobre reserva inédita | No recuperable retrospectivamente. No fingir ni bloquear el resto | EJECUCION.json prueba_inedita=False; CONTINUIDAD.md; texto para tesis |
| p.59, MAE/RMSE/R², promedio territorial, sinIPM | Ejecutado; también persistencia, distinta información para2025 | metricas.csv; fuentes/modelos.py, predictions/summarise |
| p.59, departamento omitido | Ejecutado, selección anidada y ajuste sin territorio excluido | DECISIONES_TERRITORIALES.json:99 decisiones,32 territorios train cada una; seleccion_territorial.csv; predicciones.csv ejercicio territorial |
| p.59, residuos por departamento | Calculados y conservados para todos | residuos_departamentales.csv; fuentes/resumen.py |
| p.59, Matemáticas3–4 y excluir2021 | Ejecutados como robustez separada | controles_raw.csv niveles_discrepantes=0; metricas.csv target=mat34 y exercise=sin2021 |
| p.59, reduccionesIPM1/3/5pp | Las99 propuestas se verificaron. Solo3 reducciones1pp admisibles;0 para3/5pp | escenarios.csv; SOPORTE.json; tests.py test_escenarios |
| p.59, convergencia mediana nacional | Adaptación explícita a mediana33territorios13.0;0 convergencias efectivas admitidas. No llamarla IPM nacionalDANE | SOPORTE.json; escenarios.csv reducción>0. Cuatro entradas admitidas tienen reducción0 |
| p.59, anclar en variaciones observadas | Contextualización de165cambios anuales;33intervalos2019–2021 separados | variaciones_ipm_observadas.csv; DIAGNOSTICOS.json |
| p.59, reducir proporcionalmente quince tasas de forma coherente | No ejecutado: marginales no identifican conjunta/IPM. Brecha indispensable para cumplimiento literal | Texto, sección Escenarios; alternativa limitar objetivo a escenariosIPMagregado con alcance explícito |
| p.60, mantener otras entradas/interpretación asociacional | Ejecutado; comparación entre predicciones, no efecto de políticas ni pronóstico2026 | fuentes/modelos.py scenarios; texto; escenarios.csv |
| H3, mejora confirmatoria atribuible a pobreza | No confirmada. Diferencia relativa exploratoria vsbase, peor quepersistencia. No significación causal ni reserva inédita | DISPERSION.json alcance; metricas.csv; texto |
| Reproducibilidad Python→ipynb | Dos notebooks generados y ejecutados de verdad por Python secuencial;6celdas código en segundo,2en primero | metadata ejecucion_real; fuentes/generar_notebooks.py y actualizar_notebook_publicacion.py; pruebas finales10 |
| Fuentes y originales conservados | Verificar control nuevo al cierre; no adaptar verificadores antiguos | PARTIDA.json; fuentes/control.py; registros cierre |

## Decisiones para la revisión del asesor

Esta fase tiene autorizadas las elecciones analíticas por el usuario; no se requiere otra autorización para completarla. La aceptación académica de la tesis sigue pendiente: periodo2018–2025 en objetivos predictivos y su articulación global, tendencia en lugar de efectos libres, evaluación retrospectiva, mediana departamental y restricción de escenarios/dimensiones. La alternativa propuesta es incorporar explícitamente esas delimitaciones, conservar los resultados negativos y presentar tres ejemplos condicionales de1pp, sin prometer cobertura general. No aprobar estos cambios en nombre del asesor ni afirmar cumplimiento literal de los requisitos pendientes.

No se reabren objetivos1/2: solo se verificó la población indispensable para3/4. No se estima efectos fijos para sustituir este análisis ni se vuelve a investigar la rama histórica. No se certifican otras cifras complementarias de la tesis.
