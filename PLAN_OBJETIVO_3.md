# Plan por fases para un informe riguroso del objetivo 3

## 1. Dictamen inicial y decisiones acordadas

**Los resultados de Gemini todavía no son defendibles como evidencia final de tesis.** Hay recomendaciones acertadas —unidad departamento-año, regularización y evaluación temporal—, pero también inconsistencias entre documentos, código y datos, y conclusiones causales sin respaldo.

La revisión de :codex-file-citation{path="/home/kelium/Documents/espcarlos/icfes-predict-improved/prom.pdf" purpose="source"} permite recuperar los objetivos y los modelos previos. :codex-file-citation{path="/home/kelium/Documents/espcarlos/icfes-predict-improved/nueva ivestigacion .pdf" purpose="source"} contiene las recomendaciones de Gemini y su interpretación de resultados. La inspección de :codex-file-citation{path="/home/kelium/Documents/espcarlos/icfes-predict-improved/panel_departamento_anio_unido.csv" purpose="source"} revela problemas que deben resolverse primero.

| Hallazgo verificado | Consecuencia |
|---|---|
| El CSV utiliza `;`, aunque el código mostrado lo lee con separador predeterminado. | Ese código no funciona directamente con el archivo actual. |
| Hay 198 filas y 193 cruces completos; cinco territorios carecen de resultados Saber 11 en 2021. | No existe actualmente el panel completo descrito para modelar. |
| En 2021 aparecen 15.514 estudiantes; los otros años superan 550.000. Algunos promedios provienen de uno o dos estudiantes. | Hay una anomalía grave de cobertura o construcción; su causa aún no está demostrada. |
| El promedio simple departamental de Saber 11 en 2021 es 272,1. | Contradice la caída hasta 2021 narrada en el resumen. |
| Los conteos suman 2.866.394 estudiantes, frente a 2.984.199 declarados. | Debe reconciliarse una diferencia de 117.805 registros. |
| Con los filtros mostrados, el entrenamiento tendría 127 filas y 50 casos ≥250; el PDF informa 132 y 41. | Las métricas publicadas no pueden atribuirse a esta versión de la base. |

**Decisiones acordadas:** predecir el puntaje global promedio mediante regresión, usar IPM del mismo año, conservar la clasificación previa como antecedente auditado, reportar íntegramente resultados adversos y reservar las simulaciones para el objetivo 4.

El informe presentará estimación contemporánea: disponer del IPM del mismo año no equivale a anticipar operativamente el resultado antes de su publicación.

## 2. Fases y condiciones para avanzar

### Fase 1. Auditar la tesis, la base y las afirmaciones previas

**Insumos adicionales:** tesis vigente, archivos de origen y código de limpieza, agregación e integración que aportarás.

- Confirmar el objetivo aprobado y su correspondencia con metodología, población, periodo y resultados.
- Reconstruir la trazabilidad de Saber 11: periodos y calendarios incluidos, grado, filtros, departamento del colegio o residencia, duplicados y denominadores.
- Investigar 2021 sin asumir de antemano que la pandemia explica el problema.
- Verificar procedencia, unidades, cobertura, versiones y comparabilidad de las cifras DANE. Distinguir estimaciones directas y otras metodologías si aparecen.
- Reconciliar conteos, promedios, llaves, cruces y cifras citadas en la tesis.
- Elaborar una matriz de afirmaciones de Gemini: **respaldada, parcialmente respaldada, incorrecta o no verificable**, con evidencia y corrección propuesta.

La auditoría corregirá expresamente estas interpretaciones:

- Clasificar puntajes ≥250 no equivale a estimar el puntaje. El umbral tampoco debe llamarse “satisfactorio” sin respaldo oficial.
- Un coeficiente logístico estandarizado modifica el logaritmo de las odds; no representa directamente puntos porcentuales de probabilidad.
- Un coeficiente penalizado igual a cero no demuestra irrelevancia sustantiva.
- Las importancias Gini, gain y coeficientes no son magnitudes intercambiables ni identifican causas.
- La presencia del INSE no constituye automáticamente fuga de información: depende del propósito y de su disponibilidad. Quedará fuera del modelo principal por el alcance acordado.
- Un menor Brier evalúa conjuntamente distintas propiedades; no prueba por sí solo mejor calibración. [Documentación de calibración](https://scikit-learn.org/stable/modules/calibration.html).
- La incidencia departamental del IPM no es una suma lineal de tasas marginales: la identificación de pobreza utiliza privaciones conjuntas y un umbral en los hogares. [Metodología DANE](https://microdatos.dane.gov.co/index.php/catalog/792).

**Entregables:** diagnóstico de calidad, matriz de auditoría y base analítica documentada.

**Condición de avance:** resolver la construcción y cobertura del resultado. Si 2021 no puede recuperarse con trazabilidad, excluirlo del análisis principal, documentar el cambio de periodo y trabajar con las 165 filas restantes, previa verificación. No imputar puntajes faltantes ni presentar esta exclusión como una reparación de la fuente.

### Fase 2. Cerrar el protocolo antes de entrenar

- Unidad: departamento-año. Resultado: `prom_punt_global`, expresado en puntos Saber 11.
- Cada territorio tendrá el mismo peso en el análisis principal.
- Predictores principales: IPM y sus 15 indicadores. Organizar los indicadores en las cinco dimensiones oficiales; no inventar tasas oficiales de dimensión a partir de promedios arbitrarios.
- Comparar tres especificaciones: IPM solo, 15 indicadores y combinación de ambos.
- Excluir como predictores puntajes por asignatura, percentiles y cualquier variable derivada del resultado. Usar identificadores y conteos para trazabilidad y diagnóstico.
- Usar datos hasta 2022 para desarrollo. Seleccionar mediante ventanas temporales expansivas: entrenar con años anteriores y validar en el siguiente año disponible, conservando juntos todos los territorios de cada año.
- Evaluar posteriormente 2023 y 2024 por separado y conjuntamente, con modelos congelados entrenados hasta 2022.

La validación por departamentos responderá a una pregunta distinta: generalización a territorios no usados para entrenar. Será un contraste secundario dentro del desarrollo; no sustituirá la validación temporal. [Documentación de validación cruzada](https://scikit-learn.org/stable/modules/cross_validation.html).

**Limitación obligatoria:** 2023–2024 ya fueron utilizados para comparar modelos. Su nueva evaluación será una reevaluación temporal sobre años excluidos del ajuste, pero no una prueba completamente inédita.

**Entregable:** protocolo congelado con variables, particiones, métricas, búsquedas y reglas de selección.

### Fase 3. Construir y comparar modelos reproducibles

Referencias y modelos:

- Media del resultado del entrenamiento.
- Regresión lineal con IPM solo.
- Persistencia territorial: último puntaje disponible antes del año evaluado. Se identificará como referencia con información histórica adicional.
- Ridge, ElasticNet, Random Forest Regressor y XGBoost Regressor.

La búsqueda será acotada y registrada:

- Ridge: 13 valores de penalización entre \(10^{-3}\) y \(10^{3}\), en escala logarítmica.
- ElasticNet: la misma escala y proporciones L1 de 0,1; 0,5; 0,9 y 1.
- Random Forest: 500 árboles; profundidades 2, 3 y 4; mínimos por hoja 3, 5 y 8; fracciones de predictores 0,5 y 1.
- XGBoost: 100 o 300 árboles; profundidad 1 o 2; aprendizaje 0,03 o 0,1; regularización L1 de 0 o 1 y L2 de 1 o 10; sin submuestreo y con mínimo de peso por hoja de 5.

Estandarizar dentro de cada partición para los modelos lineales. Mantener semilla 42, registrar versiones y revisar advertencias de convergencia.

**Selección:** menor MAE promedio entre años de validación. Desempatar con RMSE y después con menor complejidad. Elegir usando exclusivamente el desarrollo. Publicar los resultados de todas las familias; no declarar ganador por su resultado en 2023–2024.

**Entregables:** procedimiento reproducible, predicciones por territorio-año, tabla comparativa y modelo seleccionado. Si una referencia supera los modelos complejos, reportarlo.

### Fase 4. Contrastar explicaciones y evaluar robustez

Examinar los resultados desde cuatro perspectivas:

1. **Predictiva:** mejora frente a referencias, estabilidad por año y utilidad del error expresado en puntos.
2. **Longitudinal:** diferencias entre territorios frente a cambios dentro de cada territorio. Recalcular ambas asociaciones con la base validada.
3. **Sustantiva:** indicadores como posibles marcadores de condiciones territoriales, sin atribuirles mecanismos causales no identificados.
4. **Medición:** composición de quienes presentan Saber 11, tamaños departamentales y precisión de las estimaciones del IPM.

Pruebas previstas:

- Comparar las tres especificaciones de predictores.
- Contrastar incluir o excluir 2021 únicamente si se logra reconstruir.
- Evaluar una tendencia numérica de año como sensibilidad; no usar efectos de años futuros aprendidos de la evaluación.
- Examinar errores territoriales, heterogeneidad y sensibilidad al retirar un departamento del entrenamiento.
- Comparar peso territorial uniforme con ponderación por estudiantes como análisis secundario, aclarando que cambia la población representada.
- Estudiar coeficientes estandarizados y aportes de grupos de indicadores mediante exclusión de dimensiones. Tratar la colinealidad como límite de interpretación. [Importancia con predictores correlacionados](https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html).
- Estimar incertidumbre de las diferencias de MAE mediante 2.000 remuestreos pareados por departamento, conservando juntos sus años. Explicar que esto no estima adecuadamente la incertidumbre entre años futuros.

No añadir SHAP por apariencia de sofisticación. Solo incorporarlo si resuelve una pregunta interpretativa concreta y sus unidades quedan correctamente explicadas.

**Entregable:** matriz de robustez que indique qué conclusiones se mantienen, cambian o no pueden sostenerse. Predecir y explicar causalmente son tareas diferentes. [Shmueli, *To Explain or to Predict?*](https://arxiv.org/abs/1101.0891).

### Fase 5. Redactar el informe para la tesis

Crear `informe_objetivo_3.md`, en español académico, con esta estructura:

1. Propósito y correspondencia con el objetivo 3.
2. Datos, población, cobertura y decisiones de calidad.
3. Diseño predictivo y procedimiento de selección.
4. Resultados comparativos y justificación del modelo.
5. Diagnóstico de errores y robustez.
6. Discusión, limitaciones y conclusión.
7. Puente metodológico al objetivo 4.
8. Referencias verificadas.

Tablas principales: muestra analítica, especificaciones, métricas y síntesis de robustez. Figuras: partición temporal, observado frente a predicho, errores territoriales y estabilidad interpretativa.

Los **hallazgos planeados son preguntas por responder**, no resultados anticipados: ¿los indicadores mejoran al IPM solo?, ¿la predicción supera la persistencia?, ¿se mantiene entre años?, ¿captura principalmente diferencias territoriales?

El texto no afirmará que reducir saneamiento precario o informalidad produce mejoras educativas, ni que una intervención educativa es ineficaz. Las simulaciones existentes no identifican esos efectos.

### Fase 6. Revisar y entregar

- Verificar cada cifra contra resultados reproducibles.
- Revisar coherencia con resumen, metodología y objetivos.
- Distinguir resultados, hipótesis explicativas y limitaciones.
- Comprobar referencias, unidades, denominadores y afirmaciones de incertidumbre.
- Probar el Markdown para copiarlo en Google Docs: títulos sencillos, tablas compactas y figuras entregadas por separado.
- Entregar el informe limpio y un anexo técnico independiente.

## 3. Continuidad entre contextos y criterios de aceptación

Cada fase se ejecutará en un contexto nuevo y terminará actualizando `CONTINUIDAD_OBJETIVO_3.md` con:

- Objetivo vigente y decisiones acordadas.
- Archivos utilizados, versiones y huellas de integridad.
- Trabajo realizado y resultados verificados.
- Limitaciones, pendientes y condición de avance.
- Rutas de entregables e instrucción concreta para la siguiente fase.

La nueva sesión deberá leer primero ese documento y el protocolo; no necesitará reconstruir toda la conversación. No se iniciará una fase dependiente de una base todavía no validada.

El informe estará listo cuando sus cifras sean trazables, las particiones respeten el tiempo, el preprocesamiento no use datos de evaluación, todas las comparaciones estén publicadas y ninguna conclusión exceda la evidencia.

**Una conclusión de capacidad predictiva limitada será un resultado válido.** La rigurosidad dependerá de la calidad y transparencia del procedimiento, no de obtener métricas altas ni de confirmar las interpretaciones de Gemini.
