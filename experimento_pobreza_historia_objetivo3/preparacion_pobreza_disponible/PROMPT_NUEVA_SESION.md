# Preparación documental: pobreza disponible antes de predecir

Trabaja en `/home/kelium/Documents/espcarlos/icfes-predict-improved`.

**Pregunta científica:** ¿la información de pobreza efectivamente disponible antes de una fecha de predicción puede aportar información adicional a la historia del puntaje académico territorial?

Esta sesión autoriza exclusivamente la preparación documental de ese posible experimento. Consulta documentación oficial sobre procedencia, publicación y revisiones. No autoriza ajustes, nuevos datasets analíticos, escenarios ni ejecución del objetivo 4. No heredes presupuestos anteriores.

Lee AGENTS.md y las continuidades de `experimento_pobreza_historia_objetivo3/` y `revision_alcance_objetivo4/`. Revisa su decisión y protocolo, sus pendientes y únicamente los antecedentes necesarios. El contraste anterior está cerrado: no repetirlo ni modificar sus criterios.

Conserva originales y registra huellas antes de escribir. Guarda los entregables únicamente en `experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/` y archivos temporales en `/tmp`. Si existe trabajo previo en esa carpeta, lee su continuidad y preserva su estado antes de continuar. No modificar tesis original, experimentos anteriores, runtime compartido o `.git`; no commit/push.

**Primero, reconstruye la disponibilidad documental.** Para IPM, quince indicadores y puntajes Saber 11 de los años locales utilizados, identifica producto, organismo, periodo observado, población, geografía, fecha efectiva de publicación, revisiones y evidencia verificable. Distingue primera publicación, edición revisada, fecha de adquisición y modificación local. No uses una nota de actualización para inventar disponibilidad histórica.

Se permiten consultas a sitios oficiales del DANE y del ICFES y documentos oficiales necesarios para esa comprobación. No descargar microdatos, raw ni nuevos paneles; no incorporar cifras externas al análisis. Guarda referencias y extractos documentales pertinentes, con URL, fecha de consulta y página o ubicación. Marca explícitamente lo no demostrado.

Comprueba si las publicaciones documentadas corresponden a la edición de los datos locales. Si solo puedes demostrar que existía alguna publicación, pero no que los valores locales estaban disponibles entonces, registra esa diferencia. No certifiques retrospectivamente una predicción factible usando datos revisados posteriormente sin advertirlo.

**Después, prepara la especificación del posible experimento.** Distingue estimación contemporánea de predicción anticipada. Presenta las fechas de corte que la documentación permite justificar, las entradas disponibles en cada corte y la cobertura que resultaría. No supongas que un rezago anual garantiza disponibilidad.

Mantén como referencias persistencia e historia del puntaje. Conserva inicialmente la población y respuesta del contraste anterior. Cualquier cambio necesario de entradas, ventana o población debe explicarse como una pregunta nueva, antes de evaluar resultados. No escoger cortes, años o modelos por errores previamente favorables.

No fijes silenciosamente una fecha de predicción que represente una decisión de uso: recomienda una opción sustentada y deja esa decisión pendiente si la evidencia no la determina. No heredes automáticamente la meta del 5 %, candidatos ni presupuesto de ajustes.

Identifica si existe un año comparable aún no examinado, sin incorporar sus datos ni afirmar independencia cuando no puede demostrarse. Los años ya vistos solo permitirían evaluación exploratoria. No atribuyas cambios del puntaje causalmente a modificar pobreza.

**Entregables:** calendario documental por fuente/año; registro de procedencia y revisiones; informe de factibilidad; propuesta de protocolo sin ejecución; hallazgos con impacto, alternativa y resolución o pendiente; lecturas; manifiesto; verificador de lectura y continuidad.

En el calendario registra como mínimo: fuente, año observado, edición, fecha de publicación, evidencia, correspondencia con archivo local, estado de comprobación y limitación.

Si hacen falta herramientas de procesamiento, crea primero fuentes `.py`. Solo genera `.ipynb` desde un generador Python cuando aporte valor; nunca crees notebooks directamente.

Cierra indicando qué quedó comprobado, qué falta y qué decisiones requeriría autorizar el experimento. Si procedencia o disponibilidad indispensables no se resuelven, entrega un cierre documental incompleto verificable, sin modelos. Ningún avance automático.
