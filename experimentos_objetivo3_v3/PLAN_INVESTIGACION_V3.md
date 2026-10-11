# Plan aprobado v3 — historial territorial y modelos de cambio

Fecha: 2026-10-10, America/Bogota. Estado: **plan preparado, investigación no iniciada**.
Este documento registra las decisiones aprobadas en conversación. No es un protocolo
ya congelado ni evidencia de entrenamiento. La nueva sesión autorizará solo etapa 1.

## 1. Objetivo, partida y conservación

Explorar una reducción exacta del MAE conjunto de al menos 5% frente al procedimiento
global v2, en idénticas 165 filas externas (33 territorios × 2021–2025). No garantiza
mejora. Estos externos ya se conocen; la investigación es exploratoria y una eventual
mejora necesitará confirmación con un año todavía no evaluado.

Cierre conocido v2: `cc21529532668a966d500e435dca65ef11db09a3`.
Rama actual al preparar documentos: `codex/objetivo3-v2-piloto`; Git inicialmente limpio.
La preparación documental permanece en esa rama. No se crea rama v3 en este turno.
En la nueva sesión crear/reutilizar `codex/objetivo3-v3-historial` desde la partida real
comprobada, que puede incluir un commit posterior con estos documentos. Registrar y
explicar diferencias respecto del cierre conocido; no asumir que deben desaparecer.

Única base: `../experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv`,
SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
Todas las escrituras nuevas, incluida continuidad, protocolos, paneles derivados y
reproducciones, quedan dentro de `experimentos_objetivo3_v3/`. Conservar originales,
v1/v2, sus continuidades y `.gitignore`. No sobrescribir trabajo encontrado ni modificar
protocolos antiguos. Sin censo raw, descargas, simulación, objetivo4, ajuste final ni push.

Fuentes de antecedente: continuidad v2; protocolo v2.0.2 §§1–8; configuraciones y lock
fase2; evidencias fase3; fase4/resultados/verificacion.json e INFORME_REVISION.md.
MAE v2 guardado: 4.879557188161031. Es antecedente verificado en fase4, no resultado
nuevo de v3. Al evaluar v3 se comprobará el denominador nuevamente desde CSV guardados.

## 2. Decisiones metodológicas aprobadas

### Población, historial y objetivo de cambio

Conservar ESTUDIANTE, no libertad S, grado11, seis puntajes presentes/positivos,
geografía del colegio, sin filtro calendario; media global recibida, sin recalcular ni
redondear. Igual peso por territorio-año; conteos solo trazabilidad. 2020 definitivamente
excluido, sin auditoría, extracción ni sensibilidades.

Ordenar dentro de territorio por año autorizado. `anio_previo` es el máximo año
estrictamente anterior disponible; `puntaje_previo` es el global medio de ese registro.
En 2021 el previo es 2019. No inventar 2020 ni anualizar/dividir el cambio por el salto.
2018 conserva valor e información de origen, pero no tiene previo ni cambio observado;
no imputar ambos ni usarlo como objetivo de entrenamiento del cambio.

Persistencia predice `puntaje_previo` sin estimador ajustado. Modelos de cambio aprenden
`cambio_observado = prom_punt_global - puntaje_previo`; reconstruyen
`prediccion = puntaje_previo + cambio_predicho`.
La selección y los reportes usan predicciones reconstruidas en puntos del puntaje
original; R² se calcula sobre ese resultado, no sobre el cambio.

Entradas en orden: `puntaje_previo` seguido de las columnas originales de IPM, tasas o
ambas, respetando su orden congelado. Especificaciones: 2, 16 y 17 entradas respectivamente.
Código y nombre del territorio son llaves/contexto, nunca entradas numéricas/categóricas.
Sin año, duración del intervalo, conteos, otras pruebas Saber ni variables adicionales.
IPM/tasas del mismo año mantienen la estimación contemporánea: no es un pronóstico
anterior a publicar el IPM. No interpretar escenarios/predicciones como efectos causales.

### Configuraciones, selección y presupuesto

Exactamente 100 configuraciones nuevas: persistencia más las 99 configuraciones
no correspondientes a la media en el JSON congelado v2 (33 por especificación).
Reutilizar construcción y parámetros íntegros/defaults por familia sin duplicar lógica.
IDs v3: `persistencia` y prefijo `delta_` seguido del ID v2; guardar correspondencia.
No añadir la media como candidato v3. La media/OLS/v1/v2 anteriores son comparadores
externos guardados, sin nuevas búsquedas ni reentrenamientos de esos procedimientos.

Semilla 20261010; entorno de referencia Python3.12.14/sklearn1.9.1 y lock exacto v2.
Comprobar existencia/versiones antes de asumirlo; no instalar automáticamente.
OLS/Ridge/ElasticNet/SVR: escalado solo dentro del entrenamiento; árboles sin escalado.
Sin imputación, clipping, nuevas transformaciones, selección supervisada de entradas
ni búsqueda de semillas.

Desde 2022, candidatos elegibles deben completar todas las internas exigidas, con
predicciones finitas y convergencia. Concatenar errores internos con peso igual. Bandas
MAE mínimo+0.1, después RMSE mínimo de esa banda+0.1; menor número entradas ajustadas;
orden persistencia/OLS/Ridge/ElasticNet/SVR/GradientBoosting/ExtraTrees; orden JSON.
Persistencia no estima coeficientes y tiene cero entradas ajustadas para este desempate;
su dependencia de un puntaje anterior debe declararse, no presentarla como ausencia de
información. Guardar ganador global y por especificación; persistencia elegible en todas.
No sustituir el procedimiento global con resultados externos de una especificación.

Presupuesto futuro único: 7200 segundos acumulados para todos los ajustes del piloto
v3, con transformaciones, arranque/comunicación, fallos y repeticiones. Ledger propio,
serial e interrumpible, sin reinicios para recuperar saldo. Reutilizar/deduplicar solo
ajustes externos idénticos por ID dentro de una ventana. Los modelos/ledger v2 son lectura.
Persistencia no produce un ajuste ficticio; registrar cálculo/predicción y su duración
aparte. El protocolo deberá distinguir tiempo de ajuste y tiempo total de ejecución.

Cinco comprobaciones de repetición del procedimiento global, una por año externo;
persistencia se recalcula sin ajuste. Tolerancia atol1e-10, rtol0. No heredar diez
repeticiones de v2. La etapa1 calculará y documentará la cota aritmética de ajustes
sin fallos desde esta grilla y sus roles; prevalece el límite temporal obligatorio.

### Ventanas aprobadas

| Prueba externa | Objetivos utilizables para entrenamiento externo del cambio | Validaciones internas | Procedimiento |
|---|---|---|---|
| 2021 | 2019 disponible, sin entrenamiento de modelos | ninguna completa | persistencia fija para global y especificaciones |
| 2022 | 2019, 2021 | 2021 | selección interna |
| 2023 | 2019, 2021, 2022 | 2021, 2022 | selección interna |
| 2024 | 2019, 2021, 2022, 2023 | 2021, 2022, 2023 | selección interna |
| 2025 | 2019, 2021, 2022, 2023, 2024 | 2021, 2022, 2023, 2024 | selección interna |

Cada interna entrena únicamente con años anteriores que tienen cambio observado.
No fabricar validación de modelos en 2019 ni métricas de candidatos no evaluados en2021.
El historial usado para predecir un externo puede incluir resultados de años anteriores,
igual que su entrenamiento expansivo, pero nunca el resultado del mismo año ni posterior.
Aunque v3 tiene distinto entrenamiento interno que v2, todas las pruebas externas
son las mismas165 filas. Declarar esa diferencia al interpretar la comparación.

## 3. Etapa 1 — diseño, congelación y controles (solo nueva sesión)

1. AGENTS/continuidades primero; inventario si falta continuidad v3. Consultar del plan
   esta etapa y sus definiciones comunes (§§1–2), sin ejecutar etapas posteriores.
2. Registrar Git/partida/cambios existentes; crear/reutilizar la rama v3 de forma segura.
   Verificar fuentes/huellas/manifiestos pertinentes sin regenerar anteriores. Verificar
   continuidades históricas de manifiestos en sus commits, no inventar excepciones.
3. Crear panel derivado agregado separado con llaves, observado, año/puntaje previo,
   cambio y trazabilidad. Procesar las231 filas completas mediante código; validación
   estructural198 cambios disponibles y165 externas, sin métricas predictivas reales.
4. Reutilizar funciones compartidas con adaptación de rutas exclusiva v3. Elaborar
   protocolo prospectivo nuevo, registrar cambios respecto de v2 y congelar grilla100,
   orden/semilla/ventanas/defaults/versiones, antes de cualquier ajuste real posterior.
5. Probar controles sintéticos y dobles: anterioridad y aislamiento territorial de lag;
   2018 sin objetivo; salto2019→2021 sin anualizar; política2021; construcción/reconstrucción;
   errores/métricas sobre puntaje original; escalado sin fuga; selección/persistencia;
   huellas/cobertura; presupuesto persistente, interrupción y límite.
   Con panel real, únicamente controles estructurales, igualdad y trazabilidad.
6. Crear un notebook de controles útil desde fuentes Python editables y generador Python;
   generar/validar .ipynb y ejecutar realmente su modo de controles. No JSON manual,
   notebooks de entrenamiento ni salidas de ejecuciones no realizadas.
7. Cerrar con README, protocolo nuevo, congelaciones/configuraciones, versión/lock,
   fuentes, panel derivado, resultados reales de controles, registro de problemas,
   manifiesto/conservación, continuidad propia y commit local descriptivo sin push.
   Guardar un prompt autocontenido que autorice solo etapa2 en una sesión posterior.

No ajustar candidatos sobre el panel real, calcular errores/MAE/predicciones reales,
seleccionar modelos por ese panel ni consumir presupuesto del piloto en esta etapa.
Una falla indispensable impide declarar cierre hasta resolverla. Decisiones materiales
no resolubles con contexto/evidencia requieren consulta previa; no modificar criterios
para mejorar métricas. Pruebas sintéticas deben separarse explícitamente del panel real.

## 4. Etapa 2 — piloto (requiere autorización posterior)

Leer continuidad v3 y exclusivamente esta etapa/definiciones congeladas. Verificar
conservación, entorno y controles. Ejecutar serialmente las100 configuraciones según
ventanas, política2021, orden y presupuesto congelados. Persistir selección antes de
externo; modelos/entradas/transformaciones/versiones/advertencias/huellas/predicciones,
repeticiones y ledger completo. No reusar ajustes internos entre externas.

Guardar predicciones del procedimiento global, procedimientos por especificación y
persistencia; reconstruir puntos antes de métricas. Artefactos/llaves/origen trazables.
Numerical/convergencia: candidato inelegible sin ampliar grilla; referencia persistencia
faltante, fuga/integridad/cobertura: detener. Infraestructura: máximo una repetición del
mismo ajuste con ambos tiempos contabilizados, detener si persiste. Presupuesto agotado:
conservar parciales/incompleto, no comprobar meta sobre subconjunto ni continuar
borrando ledger. No clipping de predicciones finitas fuera del rango: conservar/advertir.

Cerrar esta etapa con evidencia y continuidad propias; no entregar notebook personal
ni avanzar automáticamente a revisión. Crear prompt exclusivo para etapa3.

## 5. Etapa 3 — revisión y entrega (requiere autorización posterior)

Recalcular desde CSV guardados, sin reentrenar. Verificar huellas, anterioridad, llaves,
roles, referencias, selección, ledger y reproducibilidad. Comparar sobre las mismas165
filas con persistencia y predicciones guardadas v2 global, v1 fija reentrenada, media y
las tres OLS; no reutilizar el MAE histórico v1 como denominador de la meta v3.

Meta principal: `100*(MAE_v2 - MAE_v3)/MAE_v2 >= 5`, denominador finito/positivo,
procedimiento completo, sin redondeo/tolerancia adicional ni condición tres-de-cinco-años.
Es criterio práctico de entrega, no prueba de significancia. No escoger configuración
con errores externos, ni eliminar territorios/años deteriorados para satisfacerlo.

Entregar MAE/RMSE/sesgo/R² por conjunto/año/territorio, 2021–2024 separado y2025;
diferencias emparejadas de error firmado/absoluto/cuadrático, errores y deterioros
anuales/territoriales, ganadores e internas/fallos, presupuesto y límites.
R² con denominador cero: no definido; RMSE conjunto desde errores concatenados.
Informe completo incluso sin mejora o con piloto incompleto; no presentar subset como
cumplimiento de meta. No nuevas pruebas de significancia.

Solo si satisface la meta, entregar notebook personal desde Python/generador/nbformat,
modo predeterminado verificar sin entrenar y reejecución voluntaria completa aparte.
Ejecutar realmente la verificación, distinguirla de reentrenamiento no realizado.
Conservar casos completos/Guainía, procedencia local, comparabilidad IPM, diferencias
hogares/alumnos/colegio/residencia, dependencia y pocos años. Antecedentes históricos
archivados permanecen así sin nueva evidencia. Cerrar con evidencia/pendientes/
continuidad/manifiesto/conservación/commit local. Ninguna fase posterior autorizada.
