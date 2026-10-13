# Propuesta de protocolo, sin ejecución

Versión documental 1.0, 12/10/2026. Pregunta nueva: ¿la información de pobreza efectivamente disponible antes de una fecha de predicción aporta información adicional a la historia del puntaje académico territorial? Estado: propuesta incompleta; no habilita modelos, escenarios, objetivo 4 ni avance automático.

No se heredan presupuestos, candidatos ni meta del 5 %; cualquier ejecución requiere autorización nueva.

## Declaraciones y comprobaciones

**Declaración humana actual:** exclusivamente preparación documental, consultas oficiales, conservación de originales, entregables dentro de esta carpeta, temporales en /tmp. No presupuestos heredados, ajustes, datos analíticos nuevos ni elección retrospectiva por errores favorables.

**Decisiones históricas preservadas**, sin modificar el contraste: media recibida `prom_punt_global`, población de registros estudiante/no libertad S/grado11/seis puntajes positivos/disponibles/código de departamento del colegio, sin filtro de calendario. Unidad departamento-año, 32 departamentos más Bogotá, igual peso territorial. Historia de 2018 y 2019, 2020 excluido, respuestas 2021–2025, 165 pares. Cambio anterior sin anualizar, con salto 2019→2021. IPM de personas y tasas de privación por hogares residentes, dominio Total; identificadores/conteos no como entradas. Evidencia: `../PROTOCOLO.md`, `../CONTINUIDAD.md`, auditoría v2.

**Comprobaciones actuales:** fechas de productos e intervalos según `REFERENCIAS.json`, calendario y registro de revisiones; conservación por huellas; metadatos locales compatibles, sin identidad oficial de valores demostrada. No se calculó desempeño, no se inspeccionaron errores para elegir cortes/candidatos.

## Decisiones nuevas propuestas antes de toda evaluación

El corte se expresa como fecha/hora America/Bogota. Se recomienda valorar **1 de enero 00:00 del año objetivo**, pendiente de aceptación humana del uso anual anticipado. La documentación identifica eventos, pero no puede decidir cuándo necesita el usuario el pronóstico. `CORTES_PROPUESTOS.csv` muestra entradas nominales condicionadas. No se convierte un corte recomendado en criterio acordado.

Para un corte c y territorio d, una observación es elegible únicamente si (a) su periodo observado ya existe, (b) la edición y los valores usados fueron efectivamente publicados antes de c y (c) el producto y población/geografía corresponden a los acordados. Si la fecha solo se conoce por día, utilizar un corte posterior al día o mantener incertidumbre; si se conoce un intervalo, usar su extremo superior como límite conservador solo para la edición realmente identificada. Nunca usar fecha de carga web, mtime, adquisición tardía o revisión posterior para retrofechar valores.

Propuesta de entradas:

- **Persistencia:** último `y` elegible al corte, con el mismo universo territorial y respuesta.
- **Historia sola:** dos últimos `y` elegibles y cambio entre ambos sin anualizar. Si las medias previstas del contraste no están disponibles, declarar qué historia más antigua se usaría, su antigüedad y si mantiene suficiente cobertura. Resolver antes de errores. No usar un `y` publicado posteriormente ni la respuesta del año objetivo como entrada.
- **Historia + IPM:** historia más último IPM elegible del territorio, dominio Total.
- **Historia + quince tasas:** historia más vector completo de tasas elegibles, conservando el orden DIMENSIONES/TASAS del contraste. Preferir mismo año y edición para las quince; no ensamblar silenciosamente vintages distintos ni mezclar IPM con tasas. Si solo parte del vector se autentica, el grupo de quince no es elegible sin una pregunta nueva.

La regla de “último publicado” se propone sin estimar valores faltantes ni interpolar. No equivale a `t−1`: en la opción enero, las edades nominales de pobreza son 2, 3, 2, 2, 2 años para respuestas 2021–2025, dentro del universo local excluyendo 2020. Pueden variar también las edades del puntaje. Añadir edad como predictor, anualizar el cambio, reintroducir 2020 o añadir otras variables son cambios materiales y requerirían justificación/protocolo antes de evaluar. No se decide hacerlos aquí.

Población y respuesta iniciales se mantienen. La primera comprobación futura sería disponibilidad documental de entradas en **todos los 165 pares nominales**, separada del valor de respuesta. No reducir población silenciosamente. Si fallan requisitos, mostrar cobertura por grupo/referencia y definir prospectivamente una regla común. Una comparación en intersección disponible podría responder una pregunta de población más estrecha; debe justificarse como pregunta nueva, sin reemplazar el contraste cerrado. No imputar historia/pobreza ni excluir un año por error. La cobertura certificada actual es cero por controles pendientes, no por falta de observaciones locales.

El corte julio requeriría revisar aplicaciones ya observadas y uso real. Una predicción solo de calendario A altera respuesta y población; una estimación de media anual con B observado altera la información de partida. Son protocolos nuevos separados, pendientes de autorización.

## Entrenamiento y evaluación pendientes de especificación

La historia de disponibilidad debe reconstruirse **también para cada ejemplo de entrenamiento**: usar sus entradas tal como existían en el corte simulado de ese año. Para entrenar en c, cada respuesta histórica debe estar publicada en su edición elegible antes de c. No basta filtrar `año < objetivo`, ni formar todas las filas con un anexo final revisado. Guardar por entrada el año observado, edición, fecha documentada, fuente/huella y edad; distinguir disponibilidad pública de adquisición del investigador.

Se proponen referencias persistencia e historia sola en la misma cobertura y cortes. La comparación de ampliada contra historia responde aporte incremental; persistencia sigue siendo referencia adicional. No hay lista de candidatos o selector aprobado. No se heredan las 21 configuraciones, regularizaciones, reglas de desempate, respaldo 2021 o umbral 5 % del contraste anterior.

Antes de autorizar fits se deben acordar: ventanas acumuladas/alternativa, disponibilidad mínima de respuestas para ajustar, tratamiento de cortes con historia insuficiente, lista acotada de candidatos/parámetros, selección únicamente en ventanas anteriores, métrica primaria y agregación, criterio práctico de mejora, incertidumbre temporal/territorial, comparaciones secundarias, semilla/entorno y presupuesto nuevo. MAE con igual peso por territorio-año es una recomendación coherente con la respuesta previa, pendiente de acuerdo; RMSE y sesgo podrían ser secundarios, nunca rescate retrospectivo. Toda comparación debe usar exactamente los mismos pares dentro del universo acordado y presentar también cobertura. No buscar modelos/años para obtener una meta.

No se fijan errores mínimos, dirección esperada, efecto causal ni resultado de aceptación. Pocos años y dependencia entre territorios limitan confirmación; ninguna prueba estadística de independencia se inventa aquí. La elección de incertidumbre debe quedar sellada antes de observar evaluación.

## Evaluación exploratoria o prospectiva

2021–2025 ya vistos: cualquier reevaluación es exploratoria, aunque las ventanas estén separadas. No se presentan como conjunto reservado independiente. 2026 es candidato cronológico condicional con solo evidencia de un resumen preliminar B; no hay año anual comparable aún no examinado demostrado. Debe verificarse historial de acceso/examen de resultados y reservarse antes de decisiones de ajuste. Como el 12/10/2026 ya transcurrió parte o todo su periodo, una reconstrucción de corte anterior no sería un pronóstico emitido prospectivamente ahora.

Una futura evaluación prospectiva requeriría elegir un corte aún futuro, congelar en él documentos y archivos autorizados con huellas, sellar protocolo/candidatos sin respuesta y evaluar cuando se publique una respuesta comparable. Un año futuro no se presupone disponible/comparable ni se incorpora ahora.

## Requisitos para solicitar autorización del experimento

1. Resolver o aceptar explícitamente un alcance distinto para procedencia/vintages: sin identidad histórica indispensable, no certificar factibilidad retrospectiva.
2. Decidir el uso y fecha de corte; justificar cualquier cambio de entradas, ventana/población y la cobertura resultante antes de evaluar.
3. Aprobar evaluación, candidatos, selección, criterio práctico y presupuesto nuevo, sin herencia automática.
4. Definir carácter exploratorio y, si existiese un año reservado, demostrar su comparabilidad e historial de no examen.
5. Autorizar por separado cualquier adquisición de datos o ejecución; primero fuentes .py editables y generador/validación de notebooks cuando la fase lo requiera.

La preparación termina aquí. No hay notebook porque no añade valor a estas tablas documentales; los procedimientos son Python editables, sin importar runtime científico compartido. Escenarios de modificación de pobreza y objetivo 4 permanecen fuera de alcance. Las predicciones no representan efectos causales.
