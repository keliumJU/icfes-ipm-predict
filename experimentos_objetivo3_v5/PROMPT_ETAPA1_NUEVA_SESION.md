# Nueva sesión — autorizar exclusivamente etapa1 v5: diseño MAE

Continúa en `/home/kelium/Documents/espcarlos/icfes-predict-improved`. v2/v3/v4/v5 abrevian experimentos_objetivo3_v2/v3/v4/v5.

Autorizo exclusivamente etapa1 v5: diseño, fuentes editables, pruebas sintéticas, reconstrucción y cotejo documental del panel, congelación y cierre. CERO fits del panel real. No ejecutar etapa2 ni piloto, evaluar meta v5, notebook personal, simulación, objetivo4, entrenamiento final, descargas, instalaciones o push. No avanzar automáticamente. Las etapas posteriores requieren otra autorización.

Lee primero AGENTS.md y continuidades vigentes v2/v3/v4/v5. Del PLAN_INVESTIGACION_V5.md lee exclusivamente §§1–2 y §3. La preparación documental partió de HEAD `0f159164e31e671e47a432afb9f2974724dec5c2`, asunto `etapa 2 v4: cerrar piloto29 exploratorio y verificaciones`, rama `codex/objetivo3-v4-correcciones`, Git limpio y v5 inexistente. El commit documental posterior se identifica por asunto `documentar plan v5 y prompt de diseno MAE sin piloto`: comprueba su hash real y sus cuatro archivos, registro y huellas, sin inventarlo. Puede existir trabajo posterior: conservarlo, explicar diferencias, no reset ni sobrescritura. Crear/verificar ahora rama `codex/objetivo3-v5-mae`, sin reutilizar silenciosamente una rama ajena.

Verifica el cierre v4 en lectura con `experimentos_objetivo3_v4/etapa2/fuentes/cerrar.py --verificar`; no invocar el cierre histórico de etapa1 v4 cuya guardia presupone que etapa2 no existe. Leer completo protocolo v4, README, informe, registro, grilla/defaults, controles, congelación, conservación y manifiestos pertinentes. Revisar E2-01 y su fe de erratas: `experimentos_objetivo3_v4/etapa2/ENMIENDA_AUDITORIA_E2_01.md`, `fuentes/verificar_extension.py`, `FE_DE_ERRATAS_E2_01.md` y `resultados/diagnostico_tipos_csv.json`. La diferencia de tipo del cero se ubicó en externo2022/persistencia/cambio_predicho; no alterar el documento congelado ni repetir piloto. No ejecutar cierres/pilotos antiguos que escriban v1/v2/v3/v4.

Los siguientes criterios completos son acuerdos del experimento, no autorización para ejecutar todavía su piloto:

## 1. Objetivo y alcance general

Comprobar si aprender con pérdida orientada al error absoluto mejora al menos 5% el MAE del procedimiento global frente a persistencia/v3. Es una hipótesis pendiente, no una promesa de mejora. La regresión de mediana usa pérdida pinball a cuantíl 0.5 más regularización L1; el boosting usa pérdida absoluta. No se afirma que ambos minimicen exactamente el MAE externo.

Mantener población ESTUDIANTE, no libertad S, grado 11, seis puntajes presentes y positivos, sin filtro de calendario. Conservar la media global recibida sin recalcular ni redondear, geografía del colegio y peso igual territorio-año; conteos solo para trazabilidad.

Fuente única: `experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv`, SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`. Derivado congelado para cotejo: `experimentos_objetivo3_v4/etapa1/reconstrucciones/panel_cambios.csv`, SHA256 `aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc`: 231 filas, 33 territorios y 198 cambios completos. Reconstruir desde el panel autorizado en memoria, comprobar trazabilidad por misma llave y valores completos frente al derivado v4 antes de guardar copia propia v5. No raw ni fuentes adicionales.

2020 definitivamente excluido; 2018 únicamente historial. Previo = máximo año estrictamente anterior del mismo territorio; 2021 tendrá previo 2019. Diferencias sin anualizar, sin fabricar 2020. Modelos aprenden cambio del puntaje; reconstrucción global = puntaje previo + cambio predicho. Objetivo sin estandarizar y métricas/selección en puntaje original. Cambios negativos válidos.

Todas las escrituras experimentales exclusivamente v5. Conservar originales, v1/v2/v3/v4 y sus continuidades, atributos, .gitignore, modelos y ledgers. Reutilizar funciones anteriores solo en lectura con destinos v5. No modificar silenciosamente fuentes congeladas; contradicción material irresoluble exige consulta. No cambiar criterios tras observar resultados. No instalaciones, descargas, push, simulación, objetivo4 ni entrenamiento final.

## 2. Decisiones metodológicas y controles transversales

### Grilla exacta de 36 candidatos

| Grupo, en orden | Entradas, en orden | Cantidad |
|---|---|---:|
| historico | puntaje previo | 1 |
| nivel_ipm | puntaje previo, IPM actual | 2 |
| cambio_ipm | puntaje previo, cambio IPM | 2 |
| cambio_tasas | puntaje previo, cambios de las 15 tasas | 16 |
| cambio_ambas | puntaje previo, cambio IPM, cambios de las 15 tasas | 17 |

El orden y nombres de las 15 tasas se tomarán íntegros de los grupos congelados de `experimentos_objetivo3_v4/etapa1/fuentes/comun_v4.py`, GRUPOS, y se materializarán en v5. No año, códigos, conteos u otros puntajes como predictores.

| Familia, en orden de desempate | Configuración | Número |
|---|---|---:|
| Persistencia | Copiar puntaje previo, sin fit | 1 |
| Regresión de mediana | Cinco grupos × α={0.01, 0.1, 1} | 15 |
| Boosting absoluto | Cinco grupos × learning_rate={0.03, 0.1} × max_depth={1, 2} | 20 |

Mediana: Pipeline completo `StandardScaler` → `QuantileRegressor(quantile=0.5, fit_intercept=True, solver='highs', solver_options=None)` con α acordado. Scaler ajustado exclusivamente con entrenamiento y dentro del proceso presupuestado. Boosting: `GradientBoostingRegressor(loss='absolute_error', n_estimators=100, min_samples_leaf=3, subsample=1.0, random_state=20261010, n_iter_no_change=None)` con learning_rate y profundidad acordados; sin escalado ni parada temprana. Los demás defaults de sklearn 1.9.1 se materializarán íntegramente antes del piloto, sin inferirlos de otra versión.

Orden JSON: persistencia; medianas por grupo y α creciente; boosting por grupo, learning_rate y profundidad crecientes. IDs estables y únicos definidos antes de evaluar. No ampliar grilla, mezclas con persistencia, correcciones comunes, nuevas variables, efectos territoriales, recencia, PCA, imputación o clipping.

### Ventanas y selección

| Externa | Internas | Entrenamiento externo de cambios |
|---|---|---|
| 2021 | Ninguna; persistencia fija | Sin fit |
| 2022 | 2021 | 2019, 2021 |
| 2023 | 2021, 2022 | 2019, 2021, 2022 |
| 2024 | 2021, 2022, 2023 | 2019, 2021, 2022, 2023 |
| 2025 | 2021, 2022, 2023, 2024 | 2019, 2021, 2022, 2023, 2024 |

Cada interna entrena cambios estrictamente anteriores desde 2019. No validación 2019 ni reutilización de ajustes internos entre ventanas externas. En 2021 no ajustar, puntuar ni seleccionar candidatos: persistencia fija para todos los procedimientos.

En 2022–2025, métricas sobre internas completas concatenadas con igual peso territorio-año: banda MAE mínimo +0.1; dentro de ella banda RMSE mínimo +0.1; luego menor número de entradas ajustadas, familia y orden JSON. Persistencia cuenta cero entradas ajustadas y participa en todos los grupos. Cada modelo cuenta todas sus entradas, aunque coeficientes sean cero. Registrar los 36 candidatos, incluidos inelegibles y razones. Selección global y cinco grupos guardadas antes del externo; global puede diferir del ganador de su propio grupo. Deduplicar solo IDs externos idénticos dentro de esa ventana.

Exigir 165 externas completas por cada uno de siete procedimientos: global, cinco grupos y persistencia (1155 filas conjuntas), con 33 territorios × cinco años, sin duplicados ni valores no finitos. No meta parcial.

### Presupuesto, fallos y auditoría futura

Ledger propio persistente de 7200 segundos acumulados, serial y terminable; incluir arranque, Pipeline, comunicación, fallos, reintentos y repeticiones. No reiniciar/ampliar saldo ni usar remanentes anteriores. Persistencia tiene duración aparte, sin fit ficticio. Cota sin fallos/reintentos: **378 = 350 internos (35×10) + ≤24 externos (6×4) + ≤4 repeticiones ajustadas**. No heredar cotas v2/v3/v4.

Cinco comprobaciones globales, una por año, `atol=1e-10`, `rtol=0`; persistencia recalculada sin fit, ganador ajustado repetido con presupuesto. Guardar parámetros completos, entradas, transformaciones, versiones, semilla, advertencias, tiempos, huellas, modelos, predicciones, selecciones, repeticiones y ledger.

Reanudación verifica huellas, artefactos e intentos consumidos. Numérico/convergencia: inelegible persistente. Infraestructura: máximo un reintento presupuestado; segundo fallo detiene. Caída pendiente sin tiempo medido agota conservadoramente el saldo. Integridad, cobertura, persistencia faltante o límite detienen: conservar incompleto, sin rescate ni meta parcial. Verificar importaciones en hijos, rutas restringidas y terminación real de procesos.

### Referencias y meta

Comparadores exclusivamente CSV históricos guardados y sus selecciones/huellas: v1/v2/v3/v4/media/tres OLS; sin cargar modelos, nuevos ajustes ni búsquedas. Principal persistencia/v3: `experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv`; contrastar selecciones y persistencia independiente. Verificar igualdad de 165 llaves/observados; denominador recalculado positivo y finito.

Meta exacta: `100 × (MAE_persistencia/v3 − MAE_v5_global) / MAE_persistencia/v3 ≥ 5`. Referencia histórica 3.429267191379531; umbral orientativo 3.2578038318105547. Decidir con cálculo exacto desde CSV, sin redondeo, tres-de-cinco ni sustitución retrospectiva por un grupo mejor. Entregar informe aunque no mejore.

### Entorno, evidencia y límites

Antes de usar `/tmp/icfes-v2-fase2-venv/bin/python`, comprobar Python 3.12.14, sklearn 1.9.1, los 54 paquetes exactos de `experimentos_objetivo3_v4/etapa1/requirements.lock.txt` y `pip check`. Si falta o difiere, documentar y consultar; no instalar. Usar `PYTHONDONTWRITEBYTECODE=1` y semilla 20261010. La preparación documental no revalida el entorno ni presupone su disponibilidad futura.

2021–2025 ya examinados: mejora exploratoria, sin confirmación independiente, causalidad ni pronóstico anticipado demostrado. Conservar casos completos y Guainía 238 frente a 404 / 21.012106 puntos (`experimentos_objetivo3_v2/fase1/resultados/diagnostico_medias_disponibles.csv`), procedencia local sin autenticación independiente, comparabilidad IPM, hogares/alumnos, colegio/residencia, enlace ecológico, dependencia temporal/territorial y pocos años. Antecedentes archivados no se reabren sin nueva conexión; E3-01 regex temporal completa y E3-02 cota 1555 v2 son antecedentes, no cotas v5.

Todo hallazgo registrará ubicación, impacto, alternativa verificable y resolución dentro del alcance. Distinguir decisiones del usuario, comprobaciones actuales, antecedentes e hipótesis. Documentar lecturas por secciones; PDF solo si pertinente, por páginas y sin presentar lectura histórica como actual.

## Entregables y ejecución autorizada ahora: etapa1

Crear protocolo 5.0.0, fuentes comunes editables, grilla36/defaults íntegros, controles e interfaces; reconstrucción propia separada solo tras cotejo completo. Fuentes previas en lectura y destinos exclusivamente v5. No runner del panel real ni ledger operativo, parámetros aprendidos, modelos reales, predicciones reales nuevas o meta v5.

Probar exclusivamente inventados/dobles:

- Grilla36, orden, matrices1/2/2/16/17, ventanas/anterioridad y reconstrucción.
- Mediana condicional, regularización, fallo/convergencia de HiGHS; scaler ajustado exclusivamente en entrenamiento, en Pipeline completo.
- Boosting con pérdida absoluta, parámetros completos y semilla fija.
- Selección, 36 candidatos incluidos inelegibles, cobertura, global distinto del ganador de grupo y deduplicación únicamente ID idéntico en ventana.
- Importaciones en procesos hijos, rutas, cobertura, artefactos/huellas, reanudación, intentos consumidos, fallo numérico persistente, un reintento de infraestructura, caída pendiente sin medición, límite y terminación real.
- Igualdad exacta de valores CSV aunque pandas infiera cero entero o flotante: comparar valores/llaves/campos/orden, sin exigir dtype idéntico ni usar tolerancia; rechazar diferencia 1e-11 o llaves diferentes. Mantener evidencia de E2-01 sin reabrirlo.

Crear notebook útil de controles desde fuente editable y generador Python, generar y validar .ipynb con nbformat y ejecutar las celdas pertinentes con sintéticos; guardar únicamente salidas realizadas. Reutilizar funciones y parámetros; documentar orden, entradas, salidas, versiones, semilla y advertencias. No notebook de modelos reales, personal o simulación.

Cerrar exclusivamente etapa1 con README/informe/registro de hallazgos, controles, pruebas, congelación, verificación de solo lectura, conservación, manifiesto y continuidad v5. Registrar explícitamente cero fits del panel real, presupuesto real no iniciado y meta no evaluada. Todo hallazgo: ubicación, impacto, alternativa verificable y resolución dentro del alcance; consultar si contradicción material irresoluble. Commit local únicamente v5, sin push.

Guardar PROMPT_ETAPA2_NUEVA_SESION.md autocontenido: futura implementación/pruebas/congelación de orquestación propia antes del primer fit real, piloto36 y auditoría conforme acuerdos, informe incluso sin mejora y notebook útil de resultados desde fuente/generador validado y realmente ejecutado; cierre solo etapa2 y prompt exclusivo etapa3 no ejecutado. NO ejecutar ese prompt ahora. Etapa3 en otra autorización: revisión detallada/notebook personal únicamente si meta global satisfecha. Nunca simulación, objetivo4, entrenamiento final, instalaciones, descargas ni push en este alcance.
