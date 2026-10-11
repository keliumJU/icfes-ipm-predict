# Continuidad v5 — preparación documental; investigación no iniciada

Fecha cliente: 2026-10-10, America/Bogota. Solo cuatro documentos preparados; etapas1–3 no iniciadas. No protocolo, grilla/defaults congelados, reconstrucciones, controles ejecutados, notebooks, ledger, modelos, predicciones o métricas nuevos v5. No rama experimental creada. No se ejecutó el prompt.

## Partida comprobada y conservación

HEAD `0f159164e31e671e47a432afb9f2974724dec5c2`, asunto `etapa 2 v4: cerrar piloto29 exploratorio y verificaciones`; rama `codex/objetivo3-v4-correcciones`, Git limpio y carpeta v5 inexistente antes de escribir. No trabajo posterior que conservar en esta partida. REGISTRO_PREPARACION.json contiene inventario versionado y SHA256 antes de escribir, huellas de los tres documentos y comprobación de conservación. Excluye su propia huella y el hash futuro del commit para evitar autorreferencia.

Lecturas actuales: AGENTS.md, continuidades vigentes v2/v3/v4, meta histórica v4 y fe de erratas E2-01; consulta puntual GRUPOS en comun_v4.py e inventario de antecedentes. No lectura sustantiva de planes previos ni análisis nuevo de datasets, modelos, recálculo de métricas o verificación operativa de cierres. PDF: ninguno, cero páginas. Entorno no revalidado ahora: etapa1 lo comprobará íntegramente antes de usarlo.

Originales, v1/v2/v3/v4, sus continuidades, .gitignore, atributos, modelos y ledgers conservados por huella. Todas las escrituras de artefactos solo v5. Commit documental exclusivamente cuatro archivos, asunto `documentar plan v5 y prompt de diseno MAE sin piloto`; obtener hash real en Git tras crearlo, sin autorreferencia ni push.

## Decisiones aprobadas por el usuario antes de evaluación v5

Objetivo ≥5% MAE global frente persistencia/v3. Grilla exacta36: persistencia1; QuantileRegressor15 (cinco grupos × α0.01/0.1/1, cuantíl0.5, solver highs, intercepto, solver_options None) en Pipeline con StandardScaler solo entrenamiento; boosting absoluto20 (cinco grupos × learning_rate0.03/0.1 × profundidad1/2,100 estimadores, hoja mínima3, subsample1, semilla20261010, sin parada temprana ni escalado). Defaults íntegros sklearn1.9.1 se materializarán en etapa1. Orden grupos/α/learning_rate/profundidad creciente y familias persistencia/mediana/boosting. No ampliar después de evaluar.

Población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario; media global recibida, geografía colegio, peso igual territorio-año. Panel único v2 SHA2566cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3. Derivado v4 SHA256aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc:231filas/198cambios, comprobación futura antes de copia v5. 2020 excluido;2018historial;2021previo2019; diferencias sin anualizar. Matrices historico/nivel_ipm/cambio_ipm/cambio_tasas/cambio_ambas1/2/2/16/17, orden v4; objetivo cambio sin escalar, reconstrucción global y métricas en puntos originales. Sin nuevos filtros/variables/efectos/recencia/PCA/imputación/clipping/mezclas/correcciones comunes.

2021 persistencia fija sin fit ni puntuar/seleccionar candidatos. 2022–2025 internas expansivas2021..año anterior; cada interna entrena cambios anteriores desde2019, sin validar2019 ni reutilizar internos entre ventanas. BandasMAE/RMSE0.1, menos entradas ajustadas, familia y JSON; persistencia0, demás todas sus entradas incluso coeficientes0. Registrar36 incluidos inelegibles; guardar global/cinco grupos antes externo, global puede diferir de su grupo, deduplicar soloIDigual en ventana. Siete procedimientos×165externas completas.

Futuro ledger propio7200s acumulados serial/terminable; arranque/Pipeline/comunicación/fallos/reintentos/repeticiones; persistencia duración aparte sin fit ficticio. Cota378=350+≤24+≤4 sin fallos/reintentos; cinco comprobacionesglobales atol1e-10/rtol0. Numérico/convergencia inelegible persistente, infraestructura máximo1reintento, fallo persistente detiene, caída pendiente no medida agota, integridad/cobertura/persistencia/límite detienen sin meta parcial. No saldo previo/reinicio/ampliación.

Meta exacta100×(MAEreferencia−MAEv5global)/MAEreferencia≥5, CSV históricos exclusivamente;165llaves/observados iguales y denominador positivo/finito recalculado. No redondeo/tres-de-cinco/sustitución por mejor grupo. Referencia histórica3.429267191379531 y umbral orientativo3.2578038318105547, no resultado v5. No modelos ni ajustes/búsquedas de comparadores.

## Hallazgos documentales: ubicación, impacto, alternativa y resolución

- v4 no alcanzó meta: etapa2/resultados/meta.json de v4 conserva MAE3.6091786595605684, mejora−5.246353175200156%. Impacto: no hay mejora incremental demostrada por ese procedimiento. Alternativa verificable: probar pérdida absoluta con grilla dirigida y evaluación intacta. Resolución: plan36 aprobado, eficacia pendiente; no afirmar agotamiento de todas las opciones.
- E2-01: v4/etapa2/FE_DE_ERRATAS_E2_01.md precisa externo2022/persistencia/cambio_predicho. Impacto: tipo de cero inferido por CSV puede causar falso rechazo. Alternativa: cotejar valores exactos preservando llaves/campos/orden. Resolución documental: pruebas positivas y negativas exigidas desde etapa1 v5; no alterar fuentes congeladas v4 ni repetir piloto.
- Preparación no equivale a controles experimentales: ubicación PLAN_INVESTIGACION_V5.md §3. Impacto: entorno/pruebas/defaults y derivado aún pendientes. Alternativa: sesión limitada con cero fits reales. Resolución: prompt autocontenido guardado y no ejecutado.

## Advertencias y pendientes

2021–2025 ya vistos: exploratorio, sin confirmación independiente/causalidad/pronóstico anticipado demostrado. Casos completos/Guainía238vs404/21.012106puntos (v2/fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local, comparabilidadIPM/hogares-alumnos/residencia-colegio/enlace ecológico, dependencia temporal/territorial y pocos años. Antecedentes archivados sin nueva conexión no se reabren; E3-01/E3-02cota1555v2 no cotasv5.

Siguiente sesión exclusivamente etapa1: crear/verificar rama codex/objetivo3-v5-mae, leer plan §§1–2/§3, verificar cierre v4 en lectura incluido E2-01/errata, comprobar Python3.12.14/sklearn1.9.1/54paquetes exactos lock/pip check, reconstrucción y cotejo completo, protocolo5.0.0/fuentes/grilla/defaults/pruebas sintéticas/notebook controles/congelación/conservación/manifiesto/continuidad, cero fits reales. Guardar prompt etapa2 sin ejecutarlo. Si entorno falta/difiere, documentar/consultar, no instalar. PYTHONDONTWRITEBYTECODE=1 y semilla20261010.

Etapa2 y etapa3 requieren autorizaciones distintas. Etapa2 probará/congelará orquestación propia antes del primer fit y entregará informe incluso sin mejora; etapa3/notebook personal solo si meta global satisfecha. No simulación, objetivo4, entrenamiento final, descargas, instalaciones, push ni cierre de fases anteriores.
