# Protocolo temporal propuesto 1.0.0 — recencia frente a historia uniforme

Fecha: 2026-10-11, America/Bogota. **Diseño documental completo; ejecución no
autorizada.** No es etapa3 v5 ni una excepción a su meta no satisfecha. El usuario
autorizó esta fase de diseño, todavía sin entrenar. Este protocolo es una propuesta
revisable; la implementación y el piloto requieren autorizaciones separadas.

## 1. Pregunta y evidencia que la motiva

¿Cambiar únicamente los pesos temporales del entrenamiento, conservando el
procedimiento de selección y evaluación de v5, mejora el MAE global frente a su
procedimiento uniforme y a persistencia?

El diagnóstico cerrado muestra cambios de distribución entre años y errores
concentrados de forma distinta: 0 de 35 configuraciones ajustadas superan
persistencia en 2021/2022/2023 por separado, y 33 de 35 en 2024. Ninguna mejora
el conjunto interno único. Esto motiva una comparación temporal, no establece
que recencia funcione, que 2019 deba eliminarse o que falte señal intrínseca.

Evidencia: `diagnostico_objetivo3_v1/fase1/tablas/matriz_hipotesis.csv`, H1/H5/H6/H7;
`conteos_ventaja_interna_por_anio.csv`, cuatro filas; `contrastes_particiones_originales.csv`,
variable=cambio_observado. Rutas completas, huellas y límites en EVIDENCIA_Y_DECISIONES.md.

## 2. Decisiones heredadas que se conservan

- Población ESTUDIANTE; no libertad S; grado 11; seis puntajes presentes y positivos;
  sin filtro de calendario; media global recibida, sin recalcular ni redondear.
- Geografía del colegio, no residencia; conteos únicamente para trazabilidad.
- Fuente única v2: `experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv`;
  SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
- Derivado v5: `experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv`;
  SHA256 `aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc`.
- 231 filas, 33 territorios; 2018 solo historial; 198 cambios; 2020 excluido;
  previo = máximo año anterior del mismo territorio; 2021 compara 2019.
- Cambio observado en puntos originales, sin anualizar el intervalo 2019–2021;
  reconstrucción = puntaje previo + cambio predicho; negativos válidos.
- Mismos 36 candidatos, grupos, entradas, orden, parámetros y defaults completos v5:
  1 persistencia, 15 regresiones de mediana, 20 boosting absoluto. Sin nuevas familias,
  variables, filtros, eliminación de años/territorios, PCA, imputación o clipping.
- Semilla 20261010; particiones originales y selección por MAE/RMSE con bandas 0.1,
  menos entradas ajustadas, familia y orden JSON. Persistencia cuenta 0; demás todas
  sus entradas, aunque algún coeficiente sea cero. No selección usando externas.
- **Todas las métricas, selección y meta conservan igual peso territorio-año.**
  La nueva ponderación afecta solo el aprendizaje, como cambio material explícito (§3).

## 3. Único cambio material propuesto: pesos del entrenamiento

Esquema primario `recencia_h2`, semivida fija **2 años calendario**. Para un
entrenamiento recibido, sea `a_max` el máximo año presente y `n` su número de filas:

```
peso_bruto_i = 2 ** (-(a_max - anio_i) / 2.0)
peso_i = n * peso_bruto_i / math.fsum(pesos_brutos)
```

Calcular en orden estable de llaves, únicamente con el entrenamiento recibido.
Mismo peso para los 33 territorios de un mismo año; todos los pesos positivos,
sin truncar ni eliminar años. Normalizar a media 1, para separar la distribución
temporal de la escala global de los pesos. No ponderar métricas o evaluación.
No usar el año externo, observados de validación, todo el panel o fechas desconocidas
para determinar `a_max`. Año sigue siendo metadata, no una nueva columna de X.

La semivida 2 es una **decisión nueva de diseño**, no una declaración del usuario,
un resultado histórico ni un parámetro optimizado. Propone un contraste único:
una separación de dos años reduce a la mitad el peso bruto; retiene toda la historia
y reconoce el salto calendario sin anualizar el objetivo. No se probarán otras
semividas en este experimento ni se cambiará esta después de observar resultados.
Su elección no se presume óptima y deberá aprobarse al autorizar la implementación.

Mediana: aplicar el mismo vector al StandardScaler y al QuantileRegressor, mediante
`escalado__sample_weight` y `modelo__sample_weight`. Scaler solo train: registrar y
auditar media/varianza ponderadas y suma de pesos. Boosting: `sample_weight` en su
entrenamiento, sin agregar scaler. Persistencia no tiene estimador ni fit.
No escalar el objetivo ni alterar regularización/defaults de los candidatos.

Con pesos uniformes, usar vector exactamente 1 y la ruta original sin parámetros
sample_weight en todos los pasos, para que el caso uniforme no cambie el cálculo
por una ruta numérica de escalado diferente. Probar esta equivalencia con datos
inventados; no realizar ahora ni en fase1 reproducciones sobre panel real.

El soporte de pesos fue inspeccionado en código instalado sklearn1.9.1, sin importar
estimadores ni ajustar. Compatibilidad integral del Pipeline, routing y los modelos
queda pendiente de pruebas inventadas en la fase de implementación; no se afirma
que esas pruebas ya estén realizadas. Ver registro de lecturas y referencias locales.

## 4. Procedimientos y contraste que distingue hipótesis

|Procedimiento|Origen futuro|Papel|
|---|---|---|
|Recencia global|Nueva selección interna con los mismos 36 candidatos y pesos §3|Primario, definido antes de externas|
|Uniforme v5 global|CSV guardado v5, 165 pares; sin volver a ajustar o cargar modelos|Control de la política temporal|
|Persistencia|Previo independiente cotejado con CSV v3, mismos 165 pares|Referencia contractual|

El uniforme global v5 y persistencia coinciden exactamente en los guardados actuales.
No son dos evidencias independientes. Describir el contraste recencia–uniforme
además del contraste recencia–persistencia, sin duplicar el n.

Se guardarán las siete salidas originales de la arquitectura para recencia:
global, cinco grupos y persistencia, cada una con 165 filas (1.155 en total).
El primario es **solo recencia/global**, nunca el mejor grupo externo. Los grupos
son secundarios descriptivos. Las referencias son archivos guardados; no fabricar
externas históricas ausentes para las 35 configuraciones no seleccionadas de v5.

No hay una búsqueda entre "uniforme o recencia" después de las externas: el primario
es recencia fijada. Si falla, se informa sin rescate. El control y los secundarios
no pueden sustituirlo para declarar cumplimiento de la meta.

La comparación evalúa una política de aprendizaje y selección, no identifica qué
coeficiente, covariable o paso produjo una diferencia, ni un efecto causal.
La simplificación queda fuera para no mezclarla con recencia: todos los candidatos
y grupos se mantienen. Más historia no se incorpora porque no existe historia
adicional autorizada y comparable en el panel; ese estudio requeriría otra fuente,
verificación de comparabilidad y autorización propia.

## 5. Particiones y evaluación: sin cambios oportunistas

|Externa|Internas originales|Train externo de cambios|
|---|---|---|
|2021|Ninguna; todos los procedimientos usan persistencia fija|Sin fit|
|2022|2021|2019,2021|
|2023|2021,2022|2019,2021,2022|
|2024|2021,2022,2023|2019,2021,2022,2023|
|2025|2021,2022,2023,2024|2019,2021,2022,2023,2024|

Cada interna entrena cambios estrictamente anteriores desde 2019. No validar 2019
ni reutilizar ajustes entre ventanas externas. En interna2021, train2019 tiene pesos
uniformes; no ofrece contraste temporal por sí sola. Diez internas acumuladas contienen
solo cuatro años de validación únicos; preservar copias y verificar linaje exacto.
Sintetizar únicas solo si coinciden predicciones y contexto, sin promediar discrepancias.
4.752 únicas=36×4×33 es expectativa futura condicionada, no resultado de recencia.

Meta original, con 165 llaves/observados idénticos y denominador positivo/finito:

```
100 * (MAE_persistencia - MAE_recencia_global) / MAE_persistencia >= 5
```

Referencia histórica 3.429267191379531 puntos; el denominador se recalcula desde
guardados cuando se autorice piloto. Nunca decidir con cifras redondeadas, tres
de cinco años, un grupo mejor, filtrado de territorios o una meta parcial.

MAE = fsum(abs(prediccion-observado))/n; RMSE = sqrt(fsum(error²)/n);
sesgo = fsum(error)/n. Deltas pareados absolutos y cuadrados; dirección exacta−/0/+,
magnitud; n y unidades explícitos. Resúmenes globales/anuales/territoriales y cortes
2021–2024 frente 2025, sin cambiar el primario de cinco años. CSV en lectura
round_trip: valores/llaves/campos/orden exactos; int/float0 equivalente; tolerancia
1e−12/rtol0 solo acumuladores internos; repeticiones de entrenamiento 1e−10/rtol0,
sin usar esa tolerancia para permitir cambios en CSV/observados o linaje.

El contraste MAE_recencia−MAE_uniforme se informa sin crear un nuevo umbral de éxito.
Cumplir 5% seguiría siendo resultado exploratorio en estos años ya vistos.

## 6. Qué historia hay y qué evaluación independiente falta

Inventario actual de la única fuente, leído completo solo para años/llaves:
2018,2019,2021,2022,2023,2024,2025,33 filas por año. No hay otros años en esa fuente.
2018 no ofrece cambio anterior;2020 sigue excluido;no fabricar historia ni cambiar
el objetivo para aumentar n. Ningún raw/fuente adicional fue examinado o incorporado.

Todos los resultados 2021–2025 ya fueron vistos y motivaron este protocolo.
No se puede convertir 2025 en holdout inédito, reservar ahora algunos territorios
como independientes ni sumar copias/candidatos como nuevas observaciones. Este
piloto propuesto puede comparar procedimientos exploratoriamente, no confirmar mejora.

Confirmación independiente requeriría uno o más bloques temporales cuyos objetivos
no se hubieran inspeccionado al congelar un protocolo futuro, población/definiciones
comparables y covariables disponibles en la fecha real de predicción. **No se ha
comprobado disponibilidad de tales bloques ni se fija aquí un año futuro como existente.**
Primero verificar fuentes/fechas/comparabilidad con otra autorización; si no existen,
dejar pendiente confirmación. Un año adicional tampoco demuestra estabilidad general
por sí solo. No crear un mínimo universal de años ni un cálculo de potencia ficticio.

## 7. Implementación, controles y límites futuros

Fase1 futura: autorización separada; constructor común desde JSON v5, función de
pesos parametrizada, worker/runner propios y destinos restringidos. Pruebas inventadas
antes de cualquier fit real, notebook de controles desde fuente editable/generador
Python, nbformat y celdas realmente ejecutadas. Congelar código, defaults, pesos,
entradas, entorno y pruebas, sin ledger operativo ni resultados reales nuevos.

Controles obligatorios: pesos positivos/normalizados/iguales dentro de año; solo
train; intervalos1/2; ausencia de anualización/filtrado; ruta uniforme idéntica;
scaler ponderado train y parámetros completos; mediana/boosting reciben los pesos;
bandas/36IDs/2021fijo/selección antes externo/global distinto grupo/dedup por ID;
CSV exacto/intfloat0/1e−11/llaves/orden/duplicados/omisiones/no finitos; copias/linaje;
rutas/symlinks/imports/terminación/fallos/reanudación/cobertura; cálculo aritmético
independiente y referencias guardadas. Pruebas no alteran v1–v5 o diagnóstico.

Fase2 futura: otra autorización después de fase1 válida. Piloto serial, nuevo ledger
7200s completo incluyendo arranque/Pipeline/comunicación/fallos/reintentos/repeticiones;
no heredar saldos ni ampliar. Persistencia tiempo aparte sin fit. Cota sin fallos:
350 internos+≤24externos+≤4repeticiones=378. Pruebas de uniformidad solo inventadas,
no sumar reproducciones reales del procedimiento v5 como si fueran gratis.
Cinco comprobaciones globales, persistencia recalculada o ganador ajustado repetido.
Todo ajuste real consume ledger, también si se usa con propósito de control.

Fallos: numérico/convergencia → inelegible con razón; infraestructura → máximo un
retry, segundo detiene; caída sin tiempo medido agota conservadoramente. Falta de
integridad/cobertura/referencia, pesos inválidos, imports/routing incompatible,
discrepancia de copias o límite → incompleto, sin rescate ni meta parcial.
No inferir que tiene que fallar o mejorar a partir del diseño actual.

Antes de usar el entorno: Python3.12.14/sklearn1.9.1/54paquetes exactos del lock v4/
pip check, PYTHONDONTWRITEBYTECODE=1, semilla20261010. Entorno ausente/diferente se
documenta y consulta; no sustituir versiones silenciosamente. Esta fase documental
no volvió a ejecutar pip check ni afirma congelación operativa de sklearn.

## 8. Conservación y advertencias

Este diseño escribe solo en `diseno_temporal_objetivo3_v1/`. El diagnóstico queda
cerrado e intacto, incluso su continuidad; el diseño tiene continuidad propia.
Una ejecución futura escribirá solo en `experimentos_temporales_objetivo3_v1/`,
etapa1/etapa2 y continuidad propia. Conservar originales/v1–v5/diagnóstico/diseño,
protocolos, atributos, .gitignore, modelos y ledgers. No commit/push sin autorización.

Casos completos/Guainía238vs404/21.012106 puntos conservados como evidencia histórica
en v2/fase1/resultados/diagnostico_medias_disponibles.csv; procedencia local no
autenticada;IPM hogares frente alumnos;colegio frente residencia/enlace ecológico;
dependencia temporal/territorial y pocos años. No causalidad, confirmación independiente
o pronóstico anticipado demostrado. Antecedentes archivados no se reabren sin nueva
conexión. V5 meta no satisfecha permanece intacta;no notebook personal/simulación/
objetivo4/entrenamiento final. Entregar informe aunque ninguna alternativa mejore.
