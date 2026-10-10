# Protocolo objetivo 3 v2.0.2 — congelación previa al piloto

Fecha de decisiones: 2026-10-10, America/Bogota. Exclusivamente fase 2.
Partida real y cierre conocido coinciden: `7c71c13e68420a2a4dd8f894efd7a540da8af7b5`,
rama `codex/objetivo3-v2-piloto`, Git limpio. Este protocolo no autoriza fase 3.
Usuario fija población, cien configuraciones, semilla, dos horas y condición de entrega.
Las decisiones operativas nuevas de §§3–7 se fijan antes de observar predicciones v2.

## 1. Panel, estimando y conservación

Única base principal: `../fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv`.
SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
231 filas, 33 territorios completos por año en 2018, 2019, 2021–2025;
198 filas históricas exactas, además del prefijo literal del CSV v1
(`auditoria/base_analitica_departamento_anio.csv`, SHA256
`609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866`).
Se verifica estructura y huellas; no se regenera fase 1 ni se repite censo raw.
2020 queda definitivamente excluido: sin auditoría, extracción ni sensibilidad.
El consolidado candidato no se usa como base principal ni como fuente de predictores.

Resultado `prom_punt_global`: media aritmética del global recibido de registros
ESTUDIANTE, no libertad S, seis puntajes presentes/positivos, código departamento del
colegio y grado 11, sin filtro calendario. Sin imputar, recalcular ni redondear puntajes.
Geografía del colegio; denominador de registros, no certificación de personas únicas.
Peso igual por territorio-año (`sample_weight=None`); conteos solo trazabilidad.
Fundamento histórico: protocolo v1 §§1–3; decisiones fase1 v2 y auditoría fase1,
resultados/agregados_anuales_2025.csv, tabla_filtros_resumen.csv y diagnóstico de medias.

## 2. Entradas y transformaciones

Tres especificaciones exactas `ipm`, `tasas` (15) y `ambas` (16), con nombres y orden
heredados en lectura de `protocolo/fuentes/configuracion.py`; exportados íntegros en
`resultados/configuraciones_congeladas.json`. Porcentajes originales 0–100; y en puntos.
Sin INSE, áreas, percentiles, derivados de y, año, códigos o conteos como entradas.
Sin correlación supervisada para elegir variables, imputación, PCA, interacciones,
logaritmos, winsorización ni normalización de y. No recortar predicciones.
OLS, Ridge, Elastic Net y SVR: Pipeline StandardScaler + estimador, con media/varianza
aprendidas exclusivamente dentro de cada entrenamiento interno o externo. Constantes
con escala 1. Árboles sin escalado. Semilla v2 `20261010`, sin buscar semillas.

## 3. Ventanas completas y prevención de fuga — decisión nueva

Cinco evaluaciones externas expansivas. Cada evaluación tiene búsqueda interna propia
sobre sus años anteriores. Así el MAE del procedimiento completo se mide fuera de la
selección de cada ventana. Se resuelve el mínimo temporal de la primera evaluación
usando dos años anteriores, sin inventar validación anidada cuando solo hay un año.
Esto amplía la evaluación v1, conservando años completos y anterioridad.

| Externo | Entrenamiento externo (33 filas/año) | Validaciones internas expansivas | n externo |
|---|---|---|---:|
| 2021 | 2018, 2019 (66) | 2019 entrenando 2018 | 33 |
| 2022 | 2018, 2019, 2021 (99) | 2019, 2021 | 33 |
| 2023 | 2018, 2019, 2021, 2022 (132) | 2019, 2021, 2022 | 33 |
| 2024 | 2018, 2019, 2021, 2022, 2023 (165) | 2019, 2021, 2022, 2023 | 33 |
| 2025 | 2018, 2019, 2021, 2022, 2023, 2024 (198) | 2019, 2021, 2022, 2023, 2024 | 33 |

Cada interna entrena todos los años autorizados estrictamente anteriores a su validación.
No particiones por posición de fila ni splits aleatorios. Orden por código-año.
Las 165 predicciones externas concatenadas reciben igual peso. Años externos previos
pueden entrar en ventanas posteriores por esta regla fijada, sin decisiones manuales
según sus errores. Ningún valor externo participa en ajuste/escalado/selección de su ventana.
La lectura estructural de todo el panel en fase 2 no calcula errores reales.
2025 es exploratorio y no reserva inédita; exposición previa histórica reduce fuerza
confirmatoria. El procedimiento puede elegir candidatos distintos en cada año: el
resultado principal evalúa el procedimiento, no un ganador único elegido con errores externos.

## 4. Exactamente 100 configuraciones de búsqueda y referencias

33 por especificación: OLS 1; Ridge 4 (alpha 0.1/1/10/100);
Elastic Net 6 (alpha 0.01/0.1/1 × l1_ratio 0.2/0.8, max_iter 20000);
SVR radial 6 (C 1/10/100 × epsilon 0.1/1, gamma scale);
Gradient Boosting 8 (100/300 árboles × aprendizaje 0.03/0.1 × profundidad 1/2,
hoja mínima 3, subsample 1); Extra Trees 8 (300 árboles × max_features 0.5/1.0 ×
hoja mínima 1/3/6/10, profundidad sin límite, n_jobs 1). Más una media del entrenamiento.
Las cuatro referencias media/OLS ya pertenecen a esas cien configuraciones y pueden ganar.
Lineales con intercepto; Ridge solver svd; Elastic Net selection cyclic; árboles squared_error.
Parámetros fijos/defaults completos y de pipelines exportados desde sklearn 1.9.1
sin ajustar ningún estimador. `construir` reutiliza clases/transformaciones por familia.

Comparador obligatorio adicional, **sin búsqueda ni elegibilidad en selección v2**:
configuración ganadora v1 `gradient_boosting_ambas_07`, tomada de
`fase3/resultados/congelacion.json`, parametros_completos. Se reentrenará sobre las mismas
cinco ventanas externas y 16 entradas, con los parámetros íntegros de estructura y **semilla 20261010**, como exige el usuario
para esta reproducción prospectiva. La semilla histórica 20261008 queda registrada como
antecedente; se aplica la misma semilla prospectiva v2 al reentrenamiento del comparador. No reutilizar modelos joblib ya ajustados
ni MAE histórico como denominador. Esta referencia fija no eleva las cien configuraciones
de búsqueda: es un ajuste de comparación impuesto por el usuario, presupuestado aparte.
La identidad de la referencia y sus parámetros son resultados históricos; no sus nuevas métricas.

## 5. Selección, tolerancias y desempates

En cada externo, evaluar todas las cien configuraciones en sus internas predefinidas;
concatenar errores internos con igual peso, sin redondeo. Elegibilidad: todas las internas
completas, convergencia satisfecha, predicciones finitas. No promediar ventanas faltantes.
Regla heredada v1 para bandas: MAE ≤ mínimo + 0.1 puntos; dentro de esa banda RMSE ≤
mínimo de la banda + 0.1 puntos. Luego menos entradas (media=0), familia en orden
media, OLS, Ridge, Elastic Net, SVR, Gradient Boosting, Extra Trees y finalmente orden
estable en JSON. El orden nuevo sigue lineales/kernel/árboles y grilla aprobada;
no afirma superioridad ni complejidad universal. Tolerancia práctica, no significancia.
Guardar ganador global y de cada especificación, con media común elegible en las tres.
Congelar selección/huellas por ventana antes de predecir su año externo; errores externos
nunca se entregan al selector. No elegir retrospectivamente un ganador con las cinco evaluaciones.

## 6. Métricas, reportes y condición del notebook personal

Para e=predicción−observado: MAE=media(|e|), RMSE=raíz(media(e²)), sesgo=media(e),
R²=1−suma(e²)/suma((y−media(y))²). Denominador R² cero: no definido (null).
Principal: MAE conjunto de 165 filas; RMSE conjunto no es promedio de raíces anuales.
Guardar llaves/ID/ventana/y/predicción/error, origen real o sintético y huellas. Recalcular
métricas independientemente desde CSV guardados; validar cobertura idéntica por comparador.
Reportar por año, territorio y conjunto, referencias media/OLS/v1, especificaciones,
ganadores de ventana, todas las configuraciones internas, fallos y deterioros.
No convertir predicciones ecológicas contemporáneas en efectos causales.

Entregar notebook personal solo si el procedimiento completo termina y
`mejora = 100 × (MAE_referencia_v1_reentrenada − MAE_v2) / MAE_referencia_v1_reentrenada ≥ 5`.
Denominador positivo/finito; comparación con idénticas ventanas y filas, sin tolerancia
adicional ni redondeo al comprobar 5. No exigir mejora en tres de cinco años. Ningún año
ni territorio necesita mejorar para esta regla, pero sus deterioros deben mostrarse.
Es umbral práctico de entrega, no significancia estadística. Informe completo siempre,
aunque no mejore o el presupuesto impida completar. Fase 2 no entrega ese notebook.

## 7. Gestión de fallos y presupuesto prospectivo

Límite global **7200 segundos acumulados** para todos los ajustes, incluidos transformadores
en Pipeline, referencias, fallos y repeticiones. Contar tiempo de pared monotónico del
proceso de ajuste y su comunicación, conservador respecto del entrenamiento puro.
Ejecución serial; BLAS/OMP un hilo; Extra Trees n_jobs 1. Ledger persistente, sin reiniciar
al reanudar; caída con ajuste pendiente agota conservadoramente saldo no demostrable.
Cada proceso recibe solo entrenamiento, se termina al agotar saldo; no iniciar ajustes
sin saldo. No dar dos horas por candidato ni por notebook. La eliminación del ledger
para seguir entrenando viola protocolo. Medición de terminación tiene latencia de sistema;
no se puede prometer precisión física de reloj cero. La latencia se registra y no habilita
ajustes adicionales. Cambios de presupuesto necesitan autorización previa.

Plan máximo sin fallos: 100 × (1+2+3+4+5)=1500 ajustes internos, hasta ocho ajustes externos
por año (ganador global/por especificación, media, tres OLS deduplicados por ID, más v1):
≤40, y diez repeticiones de reproducibilidad (cinco ganadores globales y cinco v1) dentro
del mismo saldo. Total ≤1550 ajustes; el tope de tiempo prevalece sobre el conteo.
Orden determinista: externo creciente, candidatos por orden JSON, internas crecientes,
seleccionar, ajustar referencias y ganadores por orden JSON, v1, guardar externos;
repeticiones al concluir cinco años. No reutilizar ajustes internos entre externos en
este piloto: simplifica trazabilidad y elimina decisiones de cache según duración.
Reutilizar por ID únicamente ajustes externos idénticos ya realizados en la misma ventana.
No ajustar un modelo final sobre todos los años en este piloto ni realizar contrastes nuevos.
Las diez repeticiones comparan predicciones a tolerancia absoluta 1e−10 puntos, rtol=0;
si difieren, registrar y no declarar procedimiento completo hasta resolver infraestructura.

Integridad/rangos/fuga/cobertura: detener, sin corregir población ni imputar. Fallo numérico
persistente o ConvergenceWarning: candidato inelegible en esa evaluación; guardar ID,
ventana, parámetros, versiones, advertencias y traceback; sin ampliar grilla. No clipping
si predicción finita fuera de 0–500: conservar y advertir. Infraestructura: corregir y
repetir mismo ajuste contabilizando ambos; máximo una repetición por ajuste, detener si
persiste. Si falta referencia v1 o media/OLS para un externo, detener comparación. Si se
agota saldo, guardar parciales con estado incompleto, sin extrapolar ni comprobar umbral
sobre subset; no seguir usando un ganador para años faltantes. Toda repetición no prevista
consume saldo y se registra: el conteo 1550 es plan sin fallos, no permiso para superar tiempo.

## 8. Advertencias, evidencia y alcance

Casos completos condicionan población; Guainía mantiene advertencia de selección descriptiva
(fase1/resultados/diagnostico_medias_disponibles.csv: 238 completos frente a 404 con global,
diferencia de medias 21.012106 puntos). No identificar causalmente causa/sesgo desde ese cotejo.
IPM y Saber corresponden a poblaciones distintas; residencia de hogares frente a colegio,
enlace ecológico, dependencia territorial/temporal y pocos años. Procedencia local no
autenticada independientemente; cambios de comparabilidad documentados en protocolo v1 §8
y notas de fase1 se conservan, sin corregir cifras arbitrariamente.
Antecedentes 59/esquema82, causa histórica 20212 y regla global desconocida siguen archivados
con evidencia y motivo en decisiones históricas; sin nueva evidencia de impacto no se reabren.
**PDF efectivamente leídos en esta fase: ninguno, cero páginas**. Citas PDF de documentos
previos son antecedentes de lectura ajena a esta ejecución, no nuevos cotejos.

Nueve controles: `fuentes/verificar.py`, evidencias reales en `resultados/controles.json` y
`controles_notebook.json`. Pruebas de escalado/selección/predicciones/presupuesto son
sintéticas/dobles, separadas de lectura estructural del panel. Único notebook generado:
`notebooks/01_protocolo_verificacion.ipynb`, desde Python editable y nbformat, con ejecución
real de modo verificación en kernel. No notebooks de entrenamiento/simulación ni objetivo 4.
Entorno exacto v1 disponible en caché local, recuperado sin red a entorno temporal compatible;
versiones efectivas/lock en resultados/entorno.json y requirements.lock.txt. Fuentes y
protocolo tienen huellas congeladas antes de los controles. Fase 3 requiere autorización
expresa; commit local exclusivamente fase2 y continuidad v2, sin push.

## Enmienda técnica previa a resultados predictivos — códigos territoriales

Control 1 inicial detenido (resultados/antecedentes/control_inicial_formato_codigos.json):
la fuente histórica serializa 05/08 y las filas 2025 serializan 5/8. La lectura textual
sin normalizar produce 35 cadenas, aunque son 33 códigos numéricos de colegio.
Alternativa resuelta: `normalizar_codigos` valida códigos de uno/dos dígitos y los lleva
solo en memoria a dos dígitos; exige exactamente los 33 códigos históricos, sin recodificar
territorios. Se aplica antes de unión/partición, nunca escribe el panel. Se conserva el
prefijo de 198 líneas y la comparación de valores históricos. La congelación inicial se
archiva y se congela versión corregida antes de repetir controles. Cero predicciones
reales observadas. No cambia población, geografía ni criterios de evaluación.

## Enmienda de semilla por instrucción del usuario — previa al piloto

Se corrige la interpretación inicial que había conservado 20261008 en el comparador v1.
La instrucción explícita «Usa semilla 20261010» prevalece en el reentrenamiento futuro,
también en esa referencia. Se conserva estructura/defaults ganadores v1 y se registra
su semilla original separadamente. No hubo ajustes ni predicciones reales; la configuración
inicial y pruebas de verificación se archivan en resultados/antecedentes/v201_*.json.
Se congela v2.0.2 y se repiten los controles/notebook tras esta corrección.
