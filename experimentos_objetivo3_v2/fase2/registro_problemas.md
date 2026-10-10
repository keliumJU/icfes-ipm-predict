# Registro de problemas y decisiones — fase 2 v2

2026-10-10, America/Bogota. Solo fase 2; decisiones anteriores a predicciones reales.
Documentos de lectura: AGENTS.md, continuidad v2, PLAN_INVESTIGACION_V2.md líneas 63–103
(exclusivamente fase 2), protocolo v1, decisiones previas v1/fase3, configuración y
congelación v1, decisiones y manifiestos fase1 v2. PDF: ninguno, cero páginas.
No se usan métricas históricas para configurar búsquedas; identidad/defaults ganadores v1
se leen para fijar el comparador solicitado. No hay asociaciones ni errores nuevos reales.

| ID/origen | Evidencia verificable | Impacto | Alternativa lógica | Decisión y comprobación | Estado |
|---|---|---|---|---|---|
| F2-01/comprobación | resultados/integridad_inicial.json: HEAD 7c71c13e68420a2a4dd8f894efd7a540da8af7b5, rama solicitada, Git limpio | No inventar una partida ni pisar trabajo | Cotejar cierre conocido y conservar snapshot | Coinciden; 360 versionados y siete fuentes fotografiados por huella, cierre conserva todo salvo continuidad v2 autorizada | Resuelto |
| F2-02/comprobación | resultados/huellas_anteriores.json: 217 entradas de manifiestos; cambios históricos continuidad/informe cotejados en commits | Huellas antiguas pueden corresponder a otra versión legítima | Verificar versión histórica y conservar vigente, sin regenerar | Solo excepciones ya documentadas, más continuidad v2 al actualizarla autorizadamente; siete fuentes intactas por hash, sin censo raw | Resuelto |
| F2-03/comprobación nueva | resultados/antecedentes/control_inicial_formato_codigos.json; CSV fase1 filas históricas 05/08 frente a filas2025 5/8 | Lectura textual produce 35 etiquetas y rompe comprobación/seguimiento territorial | Validar código numérico y normalizar representación solo en memoria | comun.normalizar_codigos: uno/dos dígitos, zfill2, conjunto de33 códigos conocido; control1 y union prueban preservación/negativos. CSV/históricos byte a byte intactos | Resuelto por enmienda técnica previa al piloto |
| F2-04/usuario + decisión nueva | Protocolo §§3,5 y configuraciones_congeladas.json, ventanas | Usar MAE de búsqueda para umbral sería optimista | Cinco ventanas externas 2021–2025 con internas expansivas anteriores | Primera externa con dos años previos; 15 ventanas internas totales; controles4–5 con panel estructural y pipelines dobles demuestran anterioridad/escalado | Diseño resuelto; ejecución futura pendiente |
| F2-05/usuario + decisión nueva | Cien configuraciones JSON; protocolo §§4–5 | Referencias fuera de búsqueda pueden confundirse con ampliar grilla | Media y OLS dentro100; v1 comparador fijo separado, sin elegibilidad/búsqueda |33 por especificación +media; parámetros completos/defaults construidos sin fit; referencia v1 de congelacion.json, no joblib ni MAE histórico | Resuelto |
| F2-06/corrección de interpretación | antecedentes/v201_configuraciones_congeladas.json y versión vigente, referencia_historica | Mantener semilla histórica ignoraba orden explícita de usar20261010 | Mantener estructura v1 y aplicar semilla prospectiva ordenada | Semilla original20261008 guardada como antecedente; v1 futuro random_state20261010. Congelación v2.0.2 y controles repetidos, antes de cualquier ajuste real | Resuelto; no cambio de criterios por métricas |
| F2-07/comprobación del entorno | resultados/entorno.json, requirements.lock.txt; instalación offline desde caché pip | Entorno transitorio v1 ya ausente; suponer instalación sería falso | Recuperar paquetes exactos disponibles localmente | Python3.12.14/sklearn1.9.1, pip check aprobado. Primer fallo por etiquetas wheel múltiples abreviadas se corrige leyendo todos los Tag de WHEEL; bytes paquetes no cambiados; sin red | Resuelto |
| F2-08/infraestructura | antecedentes/incidencia_kernel.json y verificacion_notebook.json | Aislamiento bloquea sockets locales, impide kernel Jupyter | Ejecutar notebook de verificación fuera de aislamiento | Primer intento interrumpido salida130; ejecución autorizada fuera del aislamiento salida0; dos celdas código realmente ejecutadas, nbformat válido | Resuelto |
| F2-09/usuario + decisión nueva | Protocolo §7; comun.Presupuesto; controles8/presupuesto_sintetico.json | Dos horas por candidato o contador reiniciado evaden límite | Ledger persistente serial, proceso interrumpible y saldo acumulado | Dobles prueban referencias/repeticiones, reanudación, límite, caída pendiente y prohibición ampliar; proceso real lento terminado; registrar latencia. Cero segundos reales del panel | Resuelto, tolerancia física del sistema documentada |
| F2-10/usuario | Protocolo §6 y condicion_personal; controles6 | Umbral confundido con significancia o regla tres años | MAE concatenado165 filas sobre ventanas iguales frente v1 reentrenada |5% sin redondeo adicional, solo procedimiento completo/denominador positivo; tests sintéticos 5%, inferior, incompleto y cero. Informe incluso sin mejora, mostrar deterioros | Regla resuelta, mejora real desconocida |
| F2-11/decisión heredada + nueva | Protocolo §§2,5,7; controles5–7 | Fuga, rankings incompletos o clipping favorecerían métricas artificiales | Pipeline por entrenamiento, bandas0.1 MAE/RMSE, parsimonia/orden, fallo inelegible | Pruebas negativas y fronteras sintéticas; seleccionar rechaza argumentos de evaluación externa, ventanas faltantes y sin candidatos completos | Resuelto; política futura congelada |

## Limitaciones activas conservadas

Casos completos, Guainía (diagnostico_medias_disponibles.csv de fase1), procedencia local
sin autenticación independiente, notas/comparabilidad IPM, geografía colegio versus
residencia de hogares y enlace ecológico, dependencia temporal/territorial y pocos años.
No se cuantifican como causas ni se declaran resueltas por tests. Se mantiene 2021,
no se modifica población/filtros/media recibida ni peso igual. Excluir2020 es decisión
explícita del usuario; no se audita ni se abre sensibilidad de ese año.

## Antecedentes archivados, sin impacto nuevo

59/esquema82, causa antigua20212, regla aritmética global desconocida, métricas/entorno
históricos no documentados y aceptación editorial externa: protocolo v1 §8 y
protocolo/decisiones_fase2.md D10/D12/D13, fase1 v2/CONTINUIDAD_V2.md histórica.
Motivo de archivo: la ruta validada actual no depende de inventar criterios ausentes;
ninguna discrepancia nueva los conecta con el análisis de fase2. Procedencia/fórmula
siguen advertencias explícitas. No se reabren ni se sustituyen por explicaciones hipotéticas.
Las correcciones técnicas de formato, entorno y semilla no eliminan esas advertencias.

No hay control indispensable de fase2 pendiente. Fase3, sus ajustes, orquestación del
piloto y resultados son trabajo posterior que requiere autorización expresa. Notebook
personal condicionado se pospone; no simulaciones/objetivo4 ni push.
