# Registro de revisión — fase 4

Fecha cliente: 2026-10-10, America/Bogota. Únicamente fase4 autorizada.

| ID y origen | Evidencia | Impacto | Alternativa lógica | Resolución y estado |
|---|---|---|---|---|
| F4-01, comprobación | partida.json, Git b37a2f338f0708958a412f5a0efa09f33861322b | Una partida diferente invalidaría continuidad | Cotejar commit/rama/cambios antes de crear entregables | Partida exacta y limpia; rama reutilizada. Resuelto |
| F4-02, primer control actual detenido | integridad de manifiesto fase2, continuidad v2 | La continuidad autorizada cambia entre cierres; compararla solo con estado actual da falso fallo | Verificar versión histórica en commit de cada cierre, sin excepción a otros archivos | Primer assert falló en continuidad antes de auditoría; se verifican SHA históricos en 0664ac y b37a2f. No se regeneran manifiestos. Resuelto; antecedente técnico sin impacto predictivo |
| F4-03, recálculo actual | verificacion.json; 1552 ajustes, 49500 internas, 51216 predicciones artefactos | Hace calculable comparación completa | Reusar funciones independientes/selector sin funciones que sobrescriben fase3 | Huellas, particiones, referencias, orden ledger, selección y repeticiones aprobados. Resuelto |
| F4-04, recálculo actual | metricas.csv, condición 18.392545281085766% | Habilita notebook personal | Aplicar criterio global predefinido sin elección retrospectiva de especificación | Condición exacta ≥5%; notebook entregado. Resuelto |
| F4-05, heterogeneidad | deterioros_v2.csv y diferencias_emparejadas.csv | Mejora global no implica mejora en todas las unidades | Mostrar íntegramente errores y deterioros | Ocho territorios y 61 pares deterioran MAE/pérdida absoluta; cinco años mejoran MAE. Resuelto para entrega; limitación activa |
| F4-06, ejecución real de notebook | verificacion_notebook.json | Evita afirmar entrenamiento no realizado | Ejecución real por Python exec, modo verificar, salida aparte y tres gráficos incrustados | Cinco celdas verificadas con nbformat; cero nuevos ajustes. Reejecución completa voluntaria no realizada |
| F4-07, aviso de infraestructura gráfica | primer import matplotlib: carpeta ~/.config sin escritura | Caché temporal automática, sin impacto numérico; ruta original inaccesible | Establecer caché de gráficos explícita en /tmp | presentar.py usa MPLCONFIGDIR temporal; gráficos regenerados y revisados visualmente. Resuelto; antecedente sin impacto en piloto |

Enmiendas E3-01 (regex temporal completa) y E3-02 (máximo descriptivo1555) conservadas.
100 configuraciones y 7200 segundos siguen congelados. La adaptación comparte funciones,
no altera fases previas, no reinicia ledger original ni el saldo histórico.

Advertencias activas: casos completos/Guainía, procedencia local sin autenticación
independiente, comparabilidad IPM, poblaciones/geografías distintas/enlace ecológico,
dependencia y pocos años. Umbral práctico; 2025 exploratorio. No causalidad ni
pronóstico disponible antes de publicar IPM. Fuentes: protocolo fase2 §8, continuidad
heredada y fase1/resultados/diagnostico_medias_disponibles.csv.

Antecedentes 59/esquema82, causa antigua20212 y fórmula global desconocida siguen
archivados con evidencia/motivo heredados, sin nueva información que justifique reapertura.
No control indispensable de fase4 pendiente. Reejecución voluntaria no realizada no es
requisito de cierre. Fase posterior/objetivo4/simulación/ajuste final requieren autorización.
