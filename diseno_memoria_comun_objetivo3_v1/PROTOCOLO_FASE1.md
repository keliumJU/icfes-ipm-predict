# Protocolo documental — memoria temporal y componente común, v1.0.0

Fecha2026-10-11 America/Bogota. Fase1 autorizada por envío expreso del usuario. Diseño completo para revisión; no congelación operativa ni aprobación de fases futuras. Cero fits reales o inventados, notebooks, cargas de modelos, instalaciones, nuevas fuentes, commits o push.

## 1. Objetivo, población y evidencia

Comparar cuatro candidatos que predicen el cambio original del puntaje territorial y un procedimiento global que selecciona únicamente por internas. Primario: procedimiento global; meta original mejoraMAE≥5% respecto a persistencia sobre165pares,33territorios×2021–2025, igual peso territorio-año. MAE=fsum(|predicción−observado|)/n; RMSE=raíz(fsum(error²)/n). El denominador de mejora debe ser positivo finito. Políticas individuales no sustituyen el primario aunque alguna mejore.

Se hereda población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin filtro calendario; media global recibida, geografía del colegio, agregación anual territorial original. No ponderar evaluación por alumnos, hogares ni tamaño. Conteos solo trazabilidad. La sesión cotejó el panel completo, no reaudita raw ni autentica procedencia oficial. Fuente v2 y derivado v5 con huellas en PREFLIGHT_FASE1.json:fuentes. Procedimiento verificable en verificar_semantica.py y SEMANTICA_FASE1.json:231filas/33territorios/198cambios, todos los campos reconstruidos en memoria exactos. Código textual normalizado zfill(2) como historial anterior, sin alterar originales.

Referencias v5/global, v3/persistencia y recencia/global idénticas en165llaves/observados/predicción según SEMANTICA_FASE1.json:referencias. Resultado HISTÓRICO recencia/globalMAE3.429267191379531, mejora0%, meta no satisfecha: experimentos_temporales_objetivo3_v1/etapa2/resultados/meta.json. Aquí no se reprodujeron fits ni se calculó una métrica nueva. No contar estas referencias como tres evidencias independientes.

## 2. Definiciones y candidatos fijos

Sea previo(t) el máximo año disponible estrictamente anterior. d[j,t]=puntaje[j,t]−puntaje[j,previo(t)], sin anualizar; c[t]=mediana de los33 d[j,t]; r[j,t]=d[j,t]−c[t]. c es auxiliar territorial, no nueva media nacional ni reemplazo del objetivo. Puntaje predicho=previo+cambio predicho. 2021 tiene previo2019 e intervalo2; no inventar2020.

| Orden/ID | Entrada y respuesta de ajuste | Cambio predicho | Unidad/entradas |
|---|---|---|---|
|0 persistencia|sin ajuste|0|0entradas derivadas|
|1 memoria|d[j,previo(t)] → d[j,t]|f_memoria(d previo)|territorio-año,1entrada|
|2 comun|c[previo(t)] → c[t]|f_comun(c previo), igual para33territorios|año,1entrada|
|3 comun_correccion|c previo → c; r[j,previo(t)] → r[j,t]|f_comun_propio(c previo)+f_correccion(r previo)|año y territorio-año,2entradas totales|

Cada componente tiene su Pipeline propio StandardScaler(copy=True,with_mean=True,with_std=True) → QuantileRegressor(quantile=0.5,alpha=1.0,fit_intercept=True,solver="highs",solver_options=None). Defaults reales revalidados por get_params sin fit: ENTORNO_FASE1.json:defaults/firmas. No sample_weight ni recencia; sin búsquedas, clipping, imputación, mezcla ni calibración. Alpha1 es propuesta fija documental anterior a resultados nuevos, no valor optimizado. Scaler solo entrenamiento de su componente. No entradas de año/código/conteos/intervalo/IPM/tasas ni efectos territoriales individuales. Corrección comparte parámetros entre territorios. No compartir ajuste común entre candidatos2y3.

## 3. Historia y ausencia de pares

2018 proporciona nivel para d2019, pero carece de d2018. 2019 permanece historial/entrada; NO respuesta supervisada porque falta su cambio anterior. No imputar ese lag. Un año completo de pares requiere33territorios con respuesta y rezago finitos, en años anteriores al evaluado. Con cero años completos estructurales: candidato completo usa persistencia, deja razón explícita, cero scaler/fit. Con un año completo: ajuste futuro permitido; memoria/corrección33filas, común1fila. Con más años se usan todos los completos admisibles, sin recencia.

Con1fila el scaler común produce entrada centrada constante y el regresor aprende principalmente nivel/intercepto; regularización no aporta evidencia de dinámica identificada. Es fragilidad acordada, no motivo para aumentar mínimo o cambiar alpha después de observar desempeño. Faltas inesperadas, duplicados o no finitos son fallo de integridad: detener; no aprovechar respaldo para ocultarlos.

2021EXTERNO permanece fijo en persistencia para todas las políticas y global: sin ajuste, puntuación o selección interna. Las internas2021 dentro de externas2022–2025 sí son puntuadas en el piloto futuro, como respaldos idénticos sin ajuste. Distinción necesaria para preservar las diez internas originales.

## 4. Particiones y trazabilidad anterior a resultados

Ventanas heredadas exactas de experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json:ventanas, serializadas sin cambiar en ESPECIFICACION_DOCUMENTAL.json:ventanas. TRAZABILIDAD_TEMPORAL.csv enumera5externas+10internas, historia de cambios/respuestas supervisadas/rezagos/unidades/regla. No hay matrices entrenadas ni predicciones nuevas.

| Evaluado | Historia de cambios admisible | Respuestas con lag | Filas común / territoriales | Regla futura |
|---|---|---|---|---|
|2021|2019 en internas; externa fija|ninguna|0/0|persistencia|
|2022|2019,2021|2021←2019|1/33|ajuste permitido|
|2023|2019,2021,2022|2021,2022|2/66|ajuste permitido|
|2024|2019,2021,2022,2023|2021,2022,2023|3/99|ajuste permitido|
|2025|2019,2021,2022,2023,2024|2021–2024|4/132|ajuste permitido|

En externa2021 el entrenamiento declarado sigue vacío. En cada interna se usa su historia anterior, no toda la historia de su externa. La entrada de predicción usa d/c/r del previo al evaluado; c/r evaluados no entran en ninguna matriz ni cálculo de scaler. Calcular c de respuestas de entrenamiento solo sobre los33territorios correctos, una fila por año para común. Materializar historia permitida antes de computar estadísticas. Permutar objetivos de validación/futuro no debe alterar matrices, estadísticas o predicción; control pendiente de fase2, no afirmación de prueba realizada. El orden temporal lógico no autentica fechas de publicación ni prueba viabilidad de pronóstico anticipado.

## 5. Selección y ejecución futura — contrato documental propuesto

Solo internas expansivas originales, nunca externas. Cobertura completa y métricas finitas para elegibilidad. Filtrar MAE≤mínimoMAE+0.1; dentro de ese pool filtrar RMSE≤mínimoRMSE+0.1; desempatar por entradas derivadas0,1,1,2 y orden0,1,2,3. Persistencia indispensable. Numérico/convergencia implica inelegibilidad con razón; no fabricar métricas o cobertura. Sin política ganadora válida, cierre incompleto. 2022 necesariamente seleccionará persistencia si las cuatro copias de respaldo2021 son exactas; es implicación documental, pendiente del control, no selección ejecutada.

1320internas originales=4×(1+2+3+4)×33;16registros=4×4selecciones;825externas=(4políticas+global)×165. 528internas únicas=4×4años×33 solo si copias/contexto coinciden exactamente; conservar1320originales y linaje con menor externo representante, no tratar repetición como evidencia independiente. No reutilizar fits entre ventanas ni entre candidatos. Global reutiliza solo salida del MISMO candidato y ventana externa. Ajustar cuatro políticas externas predefinidas; ningún contraste externo permite rescate retrospectivo del primario.

Presupuesto propuesto NUEVO7200segundos, sin saldo ni ledger actual. Cota46componentes sin fallos:24internos (4componentes×[3validaciones2022+2validaciones2023+1validación2024]);16externos (4componentes×4externas); hasta6repeticiones globales (2022globalpersistencia, quedan3externas×máximo2componentes). Pipeline completo scaler+regresor cuenta1ajuste; persistencia/respaldo0. Registro persistente y runner serial terminable; máximo1retry de infraestructura, fallo numérico inelegible, caída sin tiempo medido agota saldo conservadoramente. Toda repetición consume presupuesto. Implementación/controles/congelación propios requieren fase2 autorizada; estos números no son resultados ni compromisos operativos aprobados.

Auditoría futura independiente de matrices, fechas, unidades, referencias, selección, presupuesto, cobertura y linaje. CSV comparación numérica exacta/intfloat0equivalente/rechazo1e-11; repetición ajustadaatol1e-10,rtol0. Meta recalculada sobre mismas165llaves/observados. Implementación no importa runners ni deserializa modelos históricos. Notebook de controles y resultados únicamente en fases autorizadas, desde fuentes Python editables y generador Python con validación, ejecuciones reales sin datos personales.

## 6. Hipótesis y advertencias preservadas

Memoria puede ayudar; común puede ayudar; corrección puede aportar respecto a común. Son hipótesis, no eficacia demostrada. Contrastes individuales son descriptivos exploratorios; global evalúa meta. Todos2021–2025 ya vistos: no confirmación independiente ni causalidad. Dependencia temporal-territorial y pocos años impiden interpretar165pares como165observaciones independientes de dinámica; común tiene solo1–4respuestas por ajuste.

Procedencia local no autenticada. Guainía238frente404/diferencia21.012105832431985puntos es antecedente histórico, evidencia v2/fase1/resultados/diagnostico_medias_disponibles.csv:filas57(periodo20252,código94)y90(anual2025,código94); no cambiar media recibida. IPMhogares frente alumnos y geografía colegio frente residencia, agregación ecológica sin inferencia individual. Nuevos modelos no contienen IPM, pero estas limitaciones siguen en el contexto de procedencia, no se presentan como efecto causal. Problemas archivados sin conexión actual no se reabren; las incidencias técnicas nuevas se registran separadas.

## 7. Aceptación y siguiente fase

Fase1 acepta integridad/Git/entorno/semántica/defaults/documentos/trazabilidad/prompts/conservación, según ACEPTACION_FASE1.json. No acepta controles ejecutables, fits, piloto ni congelación. Autorizar diseño documental no aprueba operativamente fases posteriores. Prompts2–4 independientes, condicionados y solo activos cuando usuario los envía expresamente. No avance automático. Pendientes: aprobación del diseño; implementación/controles; piloto; auditoría; confirmación científica independiente y disponibilidad real, fuera del alcance actual.
