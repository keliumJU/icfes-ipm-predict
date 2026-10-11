# Informe del piloto exploratorio v3 — etapa2 completa

Fecha cliente2026-10-10, America/Bogota. Protocolo3.0.0 conservado íntegro.
Solo etapa2 autorizada/ejecutada: implementación, controles, congelación, piloto,
auditoría, notebook de resumen de resultados guardados y cierre local. Etapa3,
notebook personal, simulación, objetivo4, entrenamiento final y push no ejecutados.

## Resultado principal verificable

Sobre las mismas165 externas completas,33 territorios×2021–2025:

|Procedimiento|MAE puntos|RMSE puntos|Sesgo pred−observado puntos|R² conjunto|
|---|---|---|---|---|
|v3 global|3.4292671913795312|4.3149206473689041|-2.0960105973100562|0.93835113391179781|
|v2 global guardado|4.8795571881610309|6.194961008561882|-0.97586426860308273|0.87292602337761915|

Mejora exacta =100×(MAE_v2−MAE_v3)/MAE_v2 = **29.721754266970148%**.
Denominador finito/positivo; meta≥5% satisfecha sin redondeo adicional ni regla
por número de años. El cálculo y decisión usan floats originales (repr en meta.json);
las tablas CSV usan17 dígitos para preservar ida/vuelta, no cambiar el umbral.
Fuentes: resultados/meta.json, metricas.csv; verificar.py/independent y verificar,
recálculo con math.fsum desde CSV round_trip. No significancia estadística.

**El ganador global y cada especificación es persistencia en todos los años.**
2021 estaba fijado prospectivamente, sin modelos entrenados/puntuados/seleccionados.
Desde2022 se evaluaron100 candidatos sobre internas completas; persistencia fue
el mínimo MAE interno global y ganó según bandas y desempates congelados.
No se seleccionó mirando externos. Las tres especificaciones conservan resultados
propios aunque coinciden realmente con global; la implementación no presupone esa
coincidencia. Persistencia depende de un histórico, tiene cero entradas ajustadas,
ningún estimador ni fit. No demuestra beneficio incremental del IPM o de modelos
ajustados frente al previo en este procedimiento. Evidencia: ganadores.csv,
piloto/seleccion_2022.json…seleccion_2025.json y metricas_internas.csv.

|Externo|MAE v3|MAE v2 guardado|
|---|---|---|
|2021|2.6402236932057406|5.859134383253795|
|2022|5.0919663135676627|3.8718846703591603|
|2023|3.2072717302598033|3.7435935263623121|
|2024|3.9602791908251427|5.9068794187603553|
|2025|2.2465950290393066|5.0162939420695309|

**2022 deteriora MAE** frente v2 pese a la mejora conjunta. El sesgo conjunto pasa
aproximadamente de−0.976 a−2.096 puntos; su magnitud aumenta. La mejora conjunta
no equivale a beneficio uniforme ni menor sesgo. Alternativa resuelta en esta etapa:
conservar y comunicar métricas anuales completas, sin cambiar selección ni filtros.
Fuente: metricas.csv, filas periodo2022 y2021–2025. La revisión territorial, cortes
2021–2024/2025, diferencias firmadas/absolutas/cuadráticas y todos deterioros queda
para etapa3 separada; no se reemplaza global por especificaciones externamente mejores.

## Ejecución y cobertura

990 ajustes reales internos documentados;990 intentos en ledger; cero fallos,
cero advertencias de ajuste, cero predicciones fuera0–500. Ningún ajuste externo ni
repetición ajustada porque ganó persistencia. La cota prospectiva sin fallos1010
(990+≤16+≤4) permanece íntegra; E3-02=1555 es antecedente v2, no cota v3.
33.000 predicciones internas (100×10×33, incluye persistencia sin fit).
Cinco procedimientos externos guardados con165 filas cada uno (825 filas por roles):
global, tres especificaciones y persistencia. Roles explícitos aun con ID igual.
Cinco comprobaciones globales una por año, persistencia recalculada sin fit:
diferencia máxima0, atol1e-10/rtol0. Fuentes: verificacion.json; ledger.json,
reproducibilidad.json, estado.json y externas_AAAA.csv en resultados/piloto/.

Consumo único **971.5884660900265s/7200s**, saldo
6228.4115339099735s. Incluye Pipeline completo, spawn, comunicación,
transformaciones de entrenamiento y terminación; ajustes seriales terminables.
Persistencia: 0.0003722910114447586s de cálculo aparte en esta ejecución;
las duraciones por artefacto se conservan en persistencia/*/calculo.json.
Duración total de la invocación real del piloto: 998.9289273680042s,
no confundir con presupuesto ni tiempo de preparar/revisar la sesión.
Sin reinicio/ampliación del ledger; nunca se tocó el saldo/modelosv2.

Orden de pruebas real: entorno/etapa1 en lectura; orquestación con dobles; congelación
operativa antes del primer fit; cinco ventanas; cinco repeticiones; auditoría desde
artefactos. En pruebas hubo una incidencia del contrato del doble y un preflight
inicial que no había reconstruido la columna fuente_sha256; resueltos antes de fit
real sin modificar etapa1. Evidencias fallidas y aprobadas conservadas separadas;
registro_problemas.md detalla impacto/alternativa/resolución.

## Fuente, decisiones y comparabilidad

Único panel fuente autorizado SHA2566cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;
derivado/grilla100/huellas etapa1 intactos. Población ESTUDIANTE/no libertad S/grado11,
seis puntajes positivos/presentes, sin calendario; media global recibida, geografía
colegio y peso igual territorio-año.2020 definitivamente excluido, sin extracción ni
sensibilidad.2018 solo historial; previo mismo territorio estrictamente anterior,
2021 previo2019, sin fabricar2020 ni anualizar. Modelos aprenden cambio y reconstruyen
puntaje global; selección/métricas en puntos originales. Entradas previo+IPM/tasas/
ambas2/16/17 en orden congelado; no otras pruebas/año/código/conteos; sin clipping
ni imputación. Pipeline escalado solo entrenamiento OLS/Ridge/ElasticNet/SVR;
árboles sin escalado. Fuentes: PROTOCOLO_V3.md §§1–4, comun_v3.py, fuentes/piloto.py,
ajustes/*/ajuste.json, datos de matrices por huellas y verificación independiente.

Internas v3:2021;2021/2022;2021/2022/2023;2021/2022/2023/2024, cada una entrenando
cambios anteriores desde2019. V2 entrenaba niveles con2018 disponible y validaciones
desde2019. **Entrenamiento interno distinto; externos idénticos165.** Comparación de
procedimientos completos, no atribución causal al historial. La familia ganadora
persistencia simplifica la predicción observada, pero se respetaron todas las internas.

Referenciasv2global/v1/media/tresOLS exclusivamente predicciones guardadas. Se cotejaron
huellas CSV y selecciones, llaves, observados y panel, sin cargar modelosv2, buscar
configuraciones ni reentrenar comparadores. Resultados históricos guardados se distinguen
de recálculo actual de sus métricas; no son reproducciones actuales de sus ajustes.
Fuentes: etapa1/resultados/referencias_guardadas.json y verificar.py, metricas.csv.
Métricas conjuntas y anuales de todas las referencias conservadas, no selección externa.

## Controles, conservación y entregables

Python3.12.14/sklearn1.9.1,54 paquetes exactos/pip check aprobados, semilla20261010.
No instalación ni red. Git inicial limpio antes de fuentes nuevas, rama correcta,
cierre45fa051ffadc0fc25a326605069dd2f93920898f comprobado por asunto y ascendencia
cc215295. Etapa1/fuentes/cerrar.py --verificar ejecutado primero tras verificar entorno.
Snapshot en partida.json; congelacion_operativa.json fija todas las fuentes ejecutables
nuevas antes del fit. Originales/v1/v2/continuidades previas/.gitignore/etapa1 intactos,
solo escritura v3. Continuidad propia actualizada conservando íntegro su antecedente;
la huella anterior se coteja en Git, ninguna excepción para otras rutas.
Conservación/manifiesto se verifican con cerrar.py --verificar, en lectura.
PDF leídos en esta sesión: ninguno, cero páginas; citas heredadas no son nuevas lecturas.

Fuentes Python editables piloto/probar/verificar/cerrar/generar_notebook y
01_resultados_piloto.py. Notebook01_resultados_piloto.ipynb generado/validado con
nbformat y tres celdas realmente ejecutadas mediante Python exec, solo lectura, cero
ajustes adicionales; evidencia en verificacion_notebook.json. No notebook personal.
Resultados internos/externos/ganadores/métricas/meta, modelos, transforms/defaults,
versiones/semilla/huellas, ledger, fallos/advertencias, controles, congelación,
conservación/manifiesto verificables. No controles indispensables pendientes de etapa2.

## Límites y siguiente paso

2021–2025 ya examinados: exploratorio, sin confirmación independiente ni causalidad.
No se demuestra pronóstico anterior a publicar IPM. Persistencia usa únicamente el
puntaje previo; la selección completa incluía candidatos con IPM contemporáneo y no
se auditó disponibilidad operacional por fecha de publicación. No inferir causalidad
ni disponibilidad prospectiva desde la reducción de error.
Casos completos/Guainía238 frente404 y21.012106 puntos (fase1v2/resultados/
diagnostico_medias_disponibles.csv), procedencia local sin autenticación independiente,
comparabilidad IPM, hogares/alumnos, geografía residencia/colegio/enlace ecológico,
dependencia territorial/temporal y pocos años siguen activos.59/esquema82,
causa antigua20212 y fórmula global desconocida archivados con evidencia/motivo
heredados en continuidadv2, sin reapertura por ausencia de información nueva pertinente.

Meta satisfecha habilita considerar notebook personal únicamente tras autorización
separada de etapa3. PROMPT_ETAPA3_NUEVA_SESION.md guardado, no ejecutado. Pendiente
solo revisión/entrega de etapa3 si se autoriza; no entrenamiento final, objetivo4,
simulación ni push. No modificar criterios para mejorar métricas.

Control Git de cierre: cuatro artefactos joblib comprimidos fueron interpretados como
texto por heurística de Git. Se declararon binarios con etapa2/.gitattributes; ningún
byte de modelos ni archivo congelado cambió. Registro_problemas.md §10 explica impacto,
alternativa y resolución. El primer commit local de etapa2 fue6a10eef; complemento
posterior únicamente de clasificación y evidencia, sin ajuste adicional ni push.
