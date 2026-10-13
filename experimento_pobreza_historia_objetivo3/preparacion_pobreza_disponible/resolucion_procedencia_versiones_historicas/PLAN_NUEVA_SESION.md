# Nueva sesión: resolver procedencia y versiones históricas

## Objetivo y autorización

Determinar qué ediciones oficiales de pobreza y Saber 11 corresponden a los archivos locales y desde cuándo estaban efectivamente disponibles. Es una fase documental previa a decidir sobre el posible experimento de aporte adicional de pobreza a la historia académica territorial. No ejecutar el experimento.

Autorización expresa nueva: consultar documentación oficial del DANE y del ICFES y descargar anexos agregados históricos del DANE, exclusivamente para verificar versiones. No descargar microdatos, bases ICFES ni nuevos paneles; no crear datasets analíticos ni sustituir valores locales. No ajustar modelos, repetir el contraste, ejecutar escenarios u objetivo 4, ni heredar candidatos, meta del 5 %, criterios de éxito o presupuestos. No contactar terceros.

## Inicio y conservación

Trabajar en `/home/kelium/Documents/espcarlos/icfes-predict-improved`. Leer AGENTS.md y las continuidades del contraste, de su revisión de alcance y de la preparación documental; después únicamente decisiones, protocolos y pendientes pertinentes. La revisión de alcance está dentro de `experimento_pobreza_historia_objetivo3/revision_alcance_objetivo4/`. Mantener cerrado el contraste anterior.

Esta carpeta contiene solo el plan de arranque y su conservación, no una investigación ejecutada. Al comenzar, leer CONTINUIDAD.md y verificar esta entrega con `python3 -B verificar_plan.py`. Preservar su estado y registrar una nueva partida antes de añadir entregables de investigación. No sobrescribir estos documentos. El verificador anterior de preparación aprobó antes de crear esta carpeta; su inventario cerrado no incluye la ampliación. No modificarlo ni presentar un rechazo posterior por inventario añadido como alteración de sus archivos.

Guardar todos los entregables nuevos exclusivamente en `experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/resolucion_procedencia_versiones_historicas/`, con la investigación en su subcarpeta `investigacion/`. Usar /tmp para temporales. Registrar huellas SHA256 antes de escribir, con exclusiones explícitas. No modificar tesis, entregas anteriores, runtime compartido o .git; no commit/push. Crear primero fuentes .py; no se necesitan notebooks para esta fase. Cualquier notebook justificado debe generarse y validarse desde Python.

## Investigación y cotejo

**DANE.** Revisar IPM y quince indicadores de 2018, 2019 y 2021–2025. Identificar producto, organismo, periodo observado, población, geografía, edición, publicación y revisiones. Priorizar la recalibración de 2018, el anexo de 2019 y las ediciones anteriores a los libros locales de 2024 y 2025.

Registrar cada descarga oficial con URL solicitada y final, fecha de consulta y adquisición actual, edición declarada, huella y evidencia de publicación. Un archivo enlazado hoy desde una página histórica no demuestra que sea el archivo publicado entonces. Conservar por separado primera publicación, revisión, adquisición y modificación local.

Cotejar todas las celdas pertinentes del dominio Total: 33 territorios, IPM y quince tasas de los años locales. Documentar hojas, ubicación, unidades, definiciones, precisión, coincidencias y diferencias. Generar evidencia de comparación y resúmenes de diferencias, sin nuevos paneles ni incorporación de cifras externas al análisis. No repetir auditorías anteriores salvo el cotejo nuevo necesario con una edición oficial. Igualdad numérica, identidad de archivo y disponibilidad histórica son comprobaciones distintas; una huella actual no autentica una fecha pasada.

**ICFES.** Investigar documentalmente ambas aplicaciones de los siete años locales: publicación, revisiones, inventarios, diccionarios y cambios de versión. Revisar únicamente antecedentes locales necesarios de adquisición, huellas y metadatos, sin leer registros personales ni recalcular medias. Exigir evidencia que vincule cada TXT local con una edición oficial. No sustituir fechas de bases anonimizadas por fechas de resultados individuales o agregados con otra población. Si esta autorización no permite resolver la identidad, describir la brecha y la constancia o adquisición que requeriría otra autorización; no descargar bases ICFES.

**Disponibilidad.** Revisar los cortes documentales ya propuestos, sin escoger uno como decisión de uso. Separar disponibilidad de pobreza, historia académica y respuestas de entrenamiento; considerar también la edición elegible en cada corte de los ejemplos históricos. No suponer que un rezago anual garantiza disponibilidad ni retrofechar con actualizaciones o metadatos. Cuando solo exista intervalo, conservarlo y usar su extremo superior como límite conservador únicamente para una edición identificada.

Mantener inicialmente población y respuesta del contraste: 33 territorios, media local prom_punt_global, mismos filtros y aplicaciones, igual peso territorio-año, 2018 nivel histórico, 2019 historia, 2020 excluido, respuestas 2021–2025 y 165 pares nominales; salto 2019→2021 sin anualizar. Conservar persistencia e historia como referencias. Presentar cobertura demostrada, condicionada y no demostrada; cualquier cambio de entradas, ventana o población debe explicarse como pregunta nueva antes de evaluar resultados. No seleccionar cortes, años o modelos por errores favorables. Enero 1 a las 00:00 Bogotá sigue siendo recomendación pendiente, no decisión aceptada.

Comprobar documentalmente si existe un año anual comparable aún no examinado, sin adquirir sus datos ni afirmar independencia sin evidencia. Los años vistos solo permiten evaluación exploratoria. No interpretar predicciones como efectos causales de modificar pobreza.

## Entregables y comprobación

Entregar calendario por fuente/año/edición (fuente, año observado, edición, publicación, evidencia, correspondencia local, estado y limitación como mínimo); registro de procedencia y revisiones; resumen reproducible de cotejos; informe de factibilidad; complemento del protocolo sin ejecución; hallazgos con impacto, alternativa y resolución o pendiente; referencias y extractos con URL, consulta y página/sección/celda; lecturas revisadas y pendientes; manifiesto; verificador de solo lectura y continuidad propia de investigación.

Verificar conservación, integridad y trazabilidad, sin modificar manifiestos o verificadores anteriores. Distinguir esa aprobación de autenticación de fuentes y factibilidad científica. Leer PDF por páginas y secciones, conservando ubicaciones y pendientes.

## Condición de cierre

Dar por resuelto solo lo respaldado por evidencia de producto, edición, valores pertinentes y disponibilidad anterior al corte. Clasificar identidad exacta, igualdad numérica, compatibilidad nominal y ausencia de demostración por separado. No declarar un historial exhaustivo sin revisiones a partir de dos ediciones tardías iguales.

Si quedan controles indispensables abiertos, entregar cierre documental incompleto verificable, con evidencia faltante y alternativa concreta. Indicar qué quedó demostrado y qué decisiones requeriría autorizar después: uso/corte, cobertura y cambios de entradas o ventanas, evaluación exploratoria o prospectiva, criterio práctico, candidatos y presupuesto nuevo. No iniciar adquisiciones fuera del alcance ni ningún experimento automáticamente.
