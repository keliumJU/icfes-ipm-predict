# Decisión académica y preparación del objetivo 4

## Autorización y estado

El usuario aceptó proceder con la recomendación de conservar el contraste, revisar procedencia y disponibilidad y definir la validación antes de ajustar modelos o construir escenarios. Esta etapa es documental y local. No ejecuta el objetivo 4, modifica la tesis original, reabre presupuestos, ajusta modelos ni incorpora fuentes. El protocolo siguiente es una propuesta; no una ejecución ni una modificación retroactiva de criterios.

El contraste cerrado se conserva como evidencia exploratoria de aporte incremental de pobreza a la historia del puntaje. No sustituye el diseño íntegro de la tesis. El texto incorporable vigente sigue siendo `../TEXTO_OBJETIVO3_TESIS.md`; esta revisión no altera sus cifras, evidencias, fuentes Python o notebook ejecutado.

## Qué permite concluir

El resultado primario no respalda una ganancia suficiente al incorporar pobreza bajo las reglas acordadas. La selección ampliada no utilizó pobreza. Esto limita la justificación de usar ese procedimiento para escenarios de reducción del IPM. No demuestra inexistencia de asociación entre pobreza y educación. Evidencia: `../resultados/PRIMARIO.json`, `../resultados/tablas/selecciones.csv` y texto académico, secciones de resultados y limitaciones.

La variación entre años y entre métricas constituye un diagnóstico, no una autorización para excluir años, cambiar la métrica primaria o escoger retrospectivamente el mejor candidato. Evidencia: `../resultados/tablas/metricas_anuales.csv` y `comparaciones_mismo_alpha.csv`. No se producen nuevas métricas en esta revisión.

## Correspondencia con la tesis

Ubicaciones revisadas: `Tesis Vigente/ACA2.pdf`, página 25 (objetivos), páginas 58–60 (diseño, validación y escenarios); copias de texto preservadas en `../correccion_documental/TESIS_P25.txt` y `TESIS_P58_60.txt`.

El objetivo 4 contiene dos tareas: validación sobre años no empleados en entrenamiento y estimación condicional bajo escenarios de reducción de pobreza. El diseño escrito propone además composición de población, otras familias regularizadas, robustez con Matemáticas y validación territorial. Este contraste responde una pregunta incremental más acotada y no acredita la ejecución de esas tareas adicionales.

La separación entre entrenamiento y evaluación de cada ventana sí se verificó. La independencia respecto de decisiones anteriores de investigación no está garantizada: los años ya fueron examinados. No se debe presentar una nueva partición de los mismos años como prueba independiente. Tampoco se conoce la disponibilidad anticipada de pobreza contemporánea.

## Ruta propuesta antes de ejecutar la validación

1. Integrar académicamente el contraste como resultado exploratorio limitado y explicar la diferencia con el diseño original. La incorporación a la tesis y cualquier cambio de sus objetivos requieren una decisión académica expresa; aquí se entrega el complemento, sin modificar el original.
2. Resolver procedencia y calendario mediante documentación verificable por fuente y año. La matriz `REVISION_EVIDENCIA_LOCAL.md` identifica qué se comprobó y qué falta. No confundir huella, coherencia local, fecha de modificación del archivo o fecha de actualización de un anexo con fecha efectiva de disponibilidad pública.
3. Elegir explícitamente el uso: estimación contemporánea condicionada a pobreza conocida o predicción para una fecha de corte. Solo la segunda exige que cada entrada esté disponible antes de esa fecha. No cambiar entre ambos usos después de observar errores.
4. Si se propone una nueva validación, fijar antes de ejecutarla población, unidad territorial, respuesta, entradas disponibles, fecha de corte, años de entrenamiento/evaluación, tratamiento del salto temporal, candidatos, selección, métrica y referencia, regla de aceptación, cobertura, incertidumbre/dependencia y presupuesto. Mantener la comparación con persistencia y con historia sola. No transferir automáticamente el umbral ni el saldo del contraste cerrado a una pregunta nueva.
5. Preferir un año comparable aún no examinado, si existe y su disponibilidad/procedencia puede documentarse. Si solo se dispone de años vistos, etiquetar la evaluación como exploratoria. No seleccionar un año favorable ni afirmar que ya hay un año nuevo utilizable.
6. Decidir sobre escenarios en una etapa separada. Su interpretación seguiría siendo condicional y asociacional. Requerirían un modelo justificado para ese uso, soporte de los valores propuestos y coherencia de las variables. La exactitud predictiva por sí sola no convierte modificar IPM en una intervención causal.

## Preguntas que podrían justificar trabajo posterior

**Prioridad: ¿la pobreza realmente disponible antes de una fecha de predicción aporta información adicional a la historia?** La comparación actual usa pobreza contemporánea, cuya disponibilidad anticipada no está demostrada. La alternativa verificable es construir primero un calendario de disponibilidad y, solo después, definir entradas con rezago o una regla de último dato disponible. Es una pregunta nueva: cambia las entradas y exige autorización y protocolo nuevos. No presupone que un rezago anual sea suficiente; depende del calendario real. Su evaluación sobre años ya vistos seguiría siendo exploratoria.

**Pregunta diagnóstica: ¿por qué el comportamiento con pobreza difiere entre años?** Las tablas existentes permiten describir errores por año y territorio sin ajustes nuevos. No permiten atribuir el patrón a pandemia, calidad de datos o cambios de medición sin evidencia adicional. Una revisión descriptiva explícitamente autorizada podría formular hipótesis; excluir un año por su error sería una decisión retrospectiva y no confirmatoria.

**Pregunta de población: ¿es estable el resultado ante la definición de casos completos?** El informe histórico de auditoría de datos documenta diferencias entre medias de casos completos y de puntaje global disponible. Es un antecedente de sensibilidad poblacional, no una causa demostrada del error del modelo. Cambiar respuesta o población implicaría otro estimando y un estudio separado, nunca reemplazar el contraste cerrado.

Se recomienda priorizar calendario/procedencia y la primera pregunta, no abrir una búsqueda de modelos más complejos con los mismos años para alcanzar una mejora deseada.

## Condición de salida

Puede cerrarse esta preparación documental. La validación prospectiva y los escenarios siguen pendientes; ninguna ejecución queda activada. Faltan documentos de procedencia, fechas efectivas de disponibilidad, definición del uso y aprobación de un protocolo concreto. Todo notebook futuro partirá de archivos `.py` editables y de un generador Python; no se creará directamente ni se editará su JSON a mano.
