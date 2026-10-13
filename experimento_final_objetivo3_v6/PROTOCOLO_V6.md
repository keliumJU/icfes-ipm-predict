# Protocolo6.0.0 — último experimento exploratorio y entrega del objetivo3

Fecha2026-10-11 America/Bogota. Autoridad actual: usuario pide cerrar protocolo/crear plan/archivos/prompt para ejecutar en NUEVA sesión. Esta sesión solo preparación documental. No ejecutar ajustes reales/inventados, crear matrices/notebooks de modelos, instalar, buscar fuentes, commit/push, modelo final, proyectar2026 u objetivo4. El envío humano posterior del prompt autoriza su flujo condicionado; la existencia/lectura del archivo no autoriza ejecución.

## 1. Pregunta, primario y límites

¿Puede un procedimiento predefinido que contraste nivel histórico, rezago, regularización y cantidad de historia reducir al menos5% el MAE frente a persistencia/v3 sobre las mismas165llaves/observados? Primario: global_v6, selección exclusivamente interna. Las39políticas individuales son contrastes exploratorios completos, no ganadores externos que sustituyan al primario. Referencia exacta3.429267191379531; umbral orientativo3.2578038318105547. Calcular100×(MAEref−MAEglobal)/MAEref con denominador positivo finito. No sumar porcentajes de mejoras con bases distintas. V3/meta registra29.721754266970148%frentev2 y ganador persistencia; no18% ni aprendizaje IPM demostrado. Memoria reciente12.392390281511053%solo descriptivo;global1.7979745286559843%. Son antecedentes, deben recalcularse en notebook antes de usarse numéricamente en texto final.

Todos2021–2025vistos y grilla inspirada en hallazgos previos: exploratorio, sin prueba independiente, causalidad ni promesa5%. El plazo no justifica redefinir población, selección, métricas, meta o declarar resultados incompletos como completos. No nuevas versiones ni experimentos automáticos después de v6; entregar informe incluso sin mejora.

## 2. Población, objetivo y tiempo

Conservar ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario/media global recibida/geografía colegio;33territorios/peso igual territorio-año.2018nivel histórico,2020excluido,2019historial sin respuesta supervisada por lag inexistente. d[j,t]=puntaje[j,t]−puntaje[j,previo(t)], máximo previo estrictamente anterior, sin anualizar el salto2019–2021. c[t]=mediana de33d, auxiliar no media nacional; r[j,t]=d[j,t]−c[t]. Puntaje previsto=previo+cambio previsto, sin clipping, mezcla o calibración. No introducir año/código/intervalo/conteos/IPM/tasas como entradas. No es un modelo de efectos de intervenciones.

Ventanas exactas en ESPECIFICACION_V6.json/windows:externas2021–2025;2021externa fija persistencia para todas políticas/global, sin ajuste/puntuación/selección. Para externas2022–2025 internas2021..externo−1 (1+2+3+4=10). Internas2021 respaldadas y puntuadas. Predicción siempre solo historia anterior, nunca2025para2024. Rangos con años posteriores serían reconstrucción y quedan fuera.

## 3. Grilla fija39 candidatos y orden de desempate

Autoridad: detalles técnicos nuevos decididos en preparación tras usuario aprobar último experimento acotado, proyección un año,7200s/meta5%/entrega notebook+texto. No se observaron resultados v6 al elegirlos. CANDIDATOS.csv/ESPECIFICACION_V6.json son el contrato de IDs/orden/params completos, no una búsqueda abierta.

1. Persistencia(1):cambio0,0entradas.
2. Niveles territoriales(8):mediana o media de respuestas d históricas apiladas33filas/año;historia all/last1/last2/last3;0entradas predictoras. Aprenden una estadística histórica aunque no llamen sklearn.fit. Mediana par=promedio de centrales;media=fsum/n. No se reproduce retrospectivamente un extremo de mediana para conseguir mejor métrica.
3. MemoriaQR(12):dprevio→d,alpha0/0.01/0.1/1,history all/last2/last3,quantile0.5/highs/interceptTrue;1entrada. Rango fijo incluye regularización nula y tres órdenes de magnitud, para separar hipótesis de rezago y regularización, sin refinamiento posterior. No atribuir diferencias causalmente solo a alpha.
4. MemoriaRidge(6):mismoX/y,alpha1/10 y all/last2/last3;1entrada. Contraste pequeño de pérdida cuadrática y estabilización, no búsqueda de óptimo.
5. Memoriaárbol(2):mismoX/y,historyall,criterionabsolute_error,depth1/2,min_samples_leaf11;1entrada. Contraste no lineal limitado por pocos años;11filas equivalen a un tercio del primer año territorial, sin inferir independencia de33territorios. No boosting/grillas arbitrarias ni nuevas variables.
6. Niveles comunes(2):media/mediana de c por año con historyall,1fila/año,0entradas predictoras; igual peso años.
7. ComúnQR y común+correcciónQR(8):historyall,alpha0/0.01/0.1/1;común cprevio→c con1fila/año;corrección rprevio→r con33filas/año;1/2entradas. Cada candidato tiene común propio; ambos componentes de corregido usan su alpha pero Pipelines independientes. Permite estudiar corrección bajo regularizaciones distintas del antecedentealpha1; no asumir utilidad/inutilidad universal.

Todos componentes ajustados:Pipeline nuevo StandardScaler(copyTrue,with_meanTrue,with_stdTrue)→regresor indicado. Árbol usa mismo scaler por contrato uniforme; no se exige que escalar aporte al árbol. Defaults completos obtenidos sinfit del entorno en ESPECIFICACION/ENTORNO_DOCUMENTAL;random_state20261010 para Ridge/árbol. QR no recibe random_state inexistente. Sin sample_weight/recencia, selección automática adicional, ajustes compartidos entre candidatos/ventanas o cachéfit. Fijar todos los defaults antes del primerfit. No cargar/deserializar modelos históricos.

## 4. Cantidad de historia y respaldos

Primero determinar respuestas completas con lag disponible y33territorios desde2021 anteriores al evaluado. Después all conserva todas y lastk toma últimosk años de esas RESPUESTAS;mantener los niveles y rezagos anteriores requeridos para formar esas filas. No cortar niveles antes de verificar lag, ni incluir2019como respuesta. Con menos dek años usar todos los disponibles; cero años obliga persistencia declarada sinfit/estimación;uno permite ajuste (común1fila,territorial33). Duplicados, falta inesperada de territorios o nofinito son integridad fallida, no respaldo silencioso.

Niveles territoriales/comunes usan ese mismo conjunto de respuestas elegibles; no introducir d2019en su estimación para favorecerlos. Comparación sinrezago/rezago queda sobre historia comparable. No mezclar territorio con año como predictor. Las grillas lastk pueden coincidir en historia pequeña: registrar equivalencia, no contarlas como evidencia independiente ni compartir ajustes. La deduplicación de internas solo procede dentro del MISMO ID y año con contexto/copia exactos.

## 5. Selección y salidas fijas

Por ventana, concatenar internas de cada ID con mismo peso. MAE=fsum(abs(error))/n;RMSE=sqrt(fsum(error²)/n). Elegibilidad exige cobertura completa/finita. PoolMAE≤mínimo+0.1 inclusivo; dentro poolRMSE≤mínimoRMSE+0.1 inclusivo; desempatar por entradas predictoras0/1/2 y orden fijo. Niveles constantes cuentan0entradas X, aunque aprendan respuestas históricas; persistencia va primero en el orden. Es nueva convención explícita antes de v6, no criterio histórico inventado. No cambiar bandas, preferir recencia o política externa por resultados. No external2021en selección. Guardar decisiones antes de externas de cada ventana.

Cobertura:12870internas originales=39×10×33;156registros=39×4;6600externas=(39+global)×165;5148únicas=39×4×33 solo copias/contextos exactos,linaje12870y representante menor externo. Conservar originales y contextos de entrenamiento que excluyan externo para comparar copias. Global reutiliza salida del mismo ID/ventana;cinco checks con previo exacto, recomputación constante mismo contexto o repetición ajustada conatol1e-10/rtol0. No cambiar métricas para rescatar éxito. Auditar CSVexactos/intfloat0/rechazo1e-11.

Además del primario:comparaciones pareadas constantes/rezagos/alphas/history/pérdidas/común/corrección,MAE/RMSE/sesgo/signos por año/territorio,coef/scaler/predicción. Todos descriptivos; controlar que cambie solo el factor del contraste cuando sea posible. No atribuir diferencias en combinaciones a un único factor. No tratar165pares o copias internas como observaciones independientes. Sin p-valores confirmatorios, exactitud por tolerancia inventada ni umbral de categoría nuevo.

## 6. Presupuesto y fallos

Nuevo ledger7200s, sin heredar saldos;NO iniciado en preparación. ComponentePipeline completo cuenta1fit.39candidatos suman32componentes por contexto ajustable;192internos=32×6,128externos=32×4,hasta8repeticiones=2×4;cota328sin fallos. Aparte constantes:60estimaciones internas+40externas+hasta4recomputacionesglobales=104máximo, presupuestadas en tiempo aunque no son fits sklearn. No ocultar aprendizaje de constantes bajo etiqueta sinmodelo. Preparación y tests inventados tiempos separados y claramente rotulados.

Runner serial durable y terminable, medición monotónica continua desde creación ledger antes de primertrabajo hasta cierre, incluidos arranque/comunicación/constantes/repeticiones/fallos/retries/pausas. Un retry máximo de infraestructura en el piloto;numérico/convergencia inelegible, sin retry. Si impide coberturas indispensables, detener y cerrar incompleto sin síntesis dependiente. Pendiente tras caída sin tiempo medido agota conservadoramente;no reiniciar/ampliar7200ni reabrir cierre. No eliminar un candidato fallido para inventar cobertura39. Registrar procesos terminados. Cerrar ledger al terminar piloto/checks antes de auditoría y redacción, que son0fits y no reutilizan saldo.

## 7. Entorno, fuentes y comprobaciones

Exigir antes de cálculos:Python3.12.14/sklearn1.9.1/54lock exactos/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010. Entorno/tmp/icfes-v2-fase2-venv. Ausencia/diferencia:documentar/consultar, sin instalación/sustitución. Fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc. Solo fuentes actuales;sinraw/nuevasfuentes/red.

GitHEAD/asunto/rama/ascendencia/posteriores/conservación;no reset/sobrescribir ajenos. Continuidades históricas en commits reales;temporal solo preservada/huella partidaetapa2;fase2memoria continuidad íntegra preservada. Cierres previos no se modifican para tolerar carpeta nueva;verificar sus mappings/continuidades históricas. Fase4memoria íntegra ya revalidada antes crear este paquete,registro propio. Manifestación original y aceptación de v6documental obligatorias antes implementar.

Pruebas inventadas útiles:fuentes/llaves/fechas/cobertura/lag/lastk/2019/noanualización,anti-fuga mutando futuros,mediana par/mean/cero-un año/unidades,defaults/scalertrain/Pipelines propios,constantes/aporte común/reconstrucción,selección/pools inclusivos/entradas/orden,linaje/copias/contextos/reuso/globalfitynofit,CSV/routes/symlinks/terminación/caída/retry/presupuesto/no reabrir. Congelar fuentes/candidatos/rules/defaults/tests/notebookcontroles/entorno ANTES ajustes reales. Auditor independiente posterior no importa selector/constructores/runners ni deserializa;reconstruye desde fuentes y guardados. Coef0no atribuir soloalpha sin contraste;inspeccionar estabilidad/coef/no finitos.

## 8. Notebook y texto listo para tesis

Entregables principales futuros:02_resultados_objetivo3.ipynb desde fuenteeditablePython+generadorPython validado/releído nbformat, celdas realmente ejecutadas (kernel oexecsecuencial explícito),y TEXTO_OBJETIVO3_TESIS.md listo para incorporar. Notebook controla el análisis:funciones compartidas Python para cálculos/plots, llamadas desde sus celdas que generan CSV/JSON/PNG finales;no cifras o gráficos nuevos calculados únicamente fuera de notebook y copiados. Guardados piloto son entradas,no salidas de ejecución ficticia. Separar notebook01controles y02resultados;no notebookpersonal ni objetivo4. No datos personales, solo agregados.

Todas cifras nuevas del texto salen de salidas notebook. Generar EVIDENCIAS_TEXTO.csv con identificador de afirmación,celda/función,archivo/tabla/llave/unidad/n/sha;verificar valores contra salidas, incluidas cifras históricas utilizadas (v3/meta,etc) recalculadas/cotejadas allí. No inventar resultados o citas;afirmaciones bibliográficas solo documentos locales verificados y ubicación, sin nuevas fuentes. Figuras con unidades/n/peso/códigos, revisión visual, versionadas porSHA;cada figura originada desde notebook. Entregar tablas completas, no solo mejores cortes.

Texto:objetivo/población/cronología/referencia/metodología/historialexperimental/resultadosprimarios/contrastes/limitaciones/conclusión honesta/puente a objetivo4. Escribir incluso si no mejora;si incompleto, describir controles fallidos y no sintetizar métricas dependientes. No convertir grilla amplia y años vistos en confirmación. Plazo usuario:entrega hoy para presentación martes;no prometer duración o suficiencia científica por presión.

## 9. Puente al objetivo4 y cierre

Objetivo4 humano aclarado:proyectar solo el siguiente año,puntaje global promedio territorial. Verificar último año del panel esperado2025 y evidencias locales de disponibilidad;sin autenticar publicación por hashes. Documentar horizonte2026CONDICIONAL si el último año utilizable fuera2025, no emitir predicciones2026 ahora. Ningún nuevo dato o simulación. BuenMAE no obliga a usarIPM;la proyección de puntajes no es efecto de modificar pobreza.

MetaNO no impide concluir científicamente objetivo3;no autoriza rescatar otra política, modelo final ni avanzar automáticamente al4. Informe puede declarar referencia o método exploratorio útil con límites, y ausencia de mejora adicional. Decisión de aplicación/objetivo4 requiere autorización separada;incertidumbre no se inventa con pocos años, se documenta necesidad de diseño/evaluación de cobertura.

Preservar procedencia local no autenticada,Guainía238vs404/21.012105832431985puntos histórico v2 diagnóstico_medias_disponibles filas57y90,IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años. Aceptación técnica no acredita autenticidad/disponibilidad/causalidad/confirmación. Archivar antecedentes sin impacto actual con evidencia;no reabrir sin nueva información. Cerrar cada fase con lecturas,hallazgos/impacto/alternativa/resolución,aceptación/conservación/manifiesto/pendientes/continuidad propia preservando anterior. Sin commit/push/instalaciones/fuentesextra/otra versión/otro experimento automático.
