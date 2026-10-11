# Plan de investigación v5 — entrenamiento orientado a MAE

Versión documental 1.0. Fecha cliente: 2026-10-10, America/Bogota.
Estado: preparación documental; investigación no iniciada.

Esta entrega crea únicamente PLAN_INVESTIGACION_V5.md, CONTINUIDAD_V5.md, PROMPT_ETAPA1_NUEVA_SESION.md y REGISTRO_PREPARACION.json. No crea rama experimental ni ejecuta el prompt. Partida comprobada: `0f159164e31e671e47a432afb9f2974724dec5c2`, rama `codex/objetivo3-v4-correcciones`, Git limpio y v5 inexistente. Commit local documental exclusivamente v5: `documentar plan v5 y prompt de diseno MAE sin piloto`.

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

## 3. Etapa1 — diseño, pruebas sintéticas y congelación

Solo se autorizará al enviar el prompt de nueva sesión; esta preparación NO la inicia.

1. Leer AGENTS.md y las secciones vigentes de CONTINUIDAD_V2/V3/V4/V5; del nuevo plan exclusivamente §§1–2 y §3. Comprobar Git real: rama, estado, ascendencia y cambios respecto al cierre v4 `0f159164e31e671e47a432afb9f2974724dec5c2` y al commit documental v5, identificable por asunto `documentar plan v5 y prompt de diseno MAE sin piloto`. Conservar trabajo posterior, explicar diferencias; no reset ni sobrescritura. Crear/verificar rama `codex/objetivo3-v5-mae` únicamente ahora.
2. Verificar cierre v4 en lectura mediante `experimentos_objetivo3_v4/etapa2/fuentes/cerrar.py --verificar`, incluido E2-01, extensión, pruebas y `experimentos_objetivo3_v4/etapa2/FE_DE_ERRATAS_E2_01.md`. No invocar el cierre histórico de etapa1 v4 cuya guardia presupone ausencia de etapa2; no ejecutar cierres/pilotos previos que escriban. Leer completos protocolo v4, README/informe/registro, grilla/defaults, controles, congelación, conservación y manifiestos necesarios para verificar antecedentes.
3. Comprobar entorno exacto conforme §2 antes de usarlo. Reconstruir cambios en memoria y cotejar panel/derivado/huellas/231 filas/198 cambios/trazabilidad; después guardar copia propia v5. Esto no autoriza fits reales, estadísticas aprendidas de entrenamiento ni predicciones reales nuevas v5.
4. Crear protocolo 5.0.0, fuentes comunes editables, grilla/defaults completos, interfaces de ejecución y controles. No iniciar runner del panel real ni ledger operativo. Preparar notebook útil de controles desde fuente editable y generador Python; generar y validar con nbformat, ejecutar celdas pertinentes con datos inventados y registrar salidas reales/versiones/semilla. No editar JSON manualmente ni duplicar lógica por modelo.
5. Probar exclusivamente sintéticos/dobles: grilla36 y orden; matrices y entradas; ventanas/anterioridad/reconstrucción; mediana condicional y regularización; fallo/convergencia HiGHS; scaler solo entrenamiento; boosting absoluto y semilla; selección completa/inelegibles/cobertura/global distinto de ganador de grupo/deduplicación. Probar importaciones en hijos, rutas, artefactos/huellas, reanudación, intentos, fallos, caída, presupuesto y terminación real. Casos CSV: aceptar mismos valores exactos aunque cero sea int o float por inferencia pandas; mantener llaves/campos/orden y rechazar valores diferentes (incluida perturbación 1e-11) o llaves distintas, sin tolerancia para ese cotejo.
6. Cerrar etapa1 con README/informe/registro de hallazgos, controles, congelación, conservación, manifiesto y continuidad; verificación en lectura reproducible. Afirmar cero fits del panel real y no evaluar meta v5. Guardar prompt autocontenido exclusivo etapa2, NO ejecutarlo. Commit local únicamente v5, sin push. Orquestación propia nueva de etapa2 tendrá que probarse y congelarse antes del primer fit real; las interfaces de etapa1 no sustituyen ese requisito.

## 4. Etapa2 — otra autorización: orquestación y piloto36

Implementar orquestación propia; probarla con sintéticos/dobles y congelarla antes del primer fit real. Ejecutar piloto serial/terminable de 36 candidatos bajo §2 y protocolo 5.0.0, con ledger propio 7200s. Auditar cobertura, artefactos, modelos propios, selecciones, referencias CSV, repeticiones, intentos y presupuesto. Verificar siete procedimientos completos y cálculo exacto de meta.

Entregar informe aunque no mejore, métricas conjuntas/anuales/territoriales y todos deterioros. Notebook útil de resultados desde fuente editable y generador Python, validado y celdas pertinentes realmente ejecutadas desde resultados guardados. Cerrar solo etapa2: README/informe/registro, controles, verificación, conservación, manifiesto, continuidad y commit local solo v5. Guardar prompt exclusivo etapa3 sin ejecutarlo. No entrenamiento final ni notebook personal.

## 5. Etapa3 — otra autorización y condición de meta

Revisión detallada y notebook personal únicamente si la meta global se satisface. Si no, informar incumplimiento y conservar el experimento; no rescate retrospectivo. No simulación, objetivo4, entrenamiento final, instalaciones, descargas ni push. Este plan no autoriza ni cierra fases posteriores de v3/v4.

## 6. Evidencia documental y pendientes

Decisiones §§1–5 proceden del plan explícitamente aprobado por el usuario, antes de cualquier evaluación v5. Antecedentes: `experimentos_objetivo3_v3/etapa2/resultados/meta.json` y `experimentos_objetivo3_v4/etapa2/resultados/meta.json`; v4 conserva MAE 3.6091786595605684 y mejora −5.246353175200156%, meta falsa. Son resultados históricos leídos, no reproducciones actuales ni resultados v5. No permiten concluir que se hayan probado todas las posibilidades: la hipótesis de pérdida absoluta está pendiente.

Conservación y partida verificables en REGISTRO_PREPARACION.json; el registro no incluye su propia huella ni el hash futuro del commit. Entorno, pruebas, protocolo/defaults, reconstrucción y cierre v4 operativo siguen pendientes para etapa1; no se consideran controles aprobados por escribir este plan. La siguiente sesión empieza con PROMPT_ETAPA1_NUEVA_SESION.md y termina en el cierre de etapa1.
