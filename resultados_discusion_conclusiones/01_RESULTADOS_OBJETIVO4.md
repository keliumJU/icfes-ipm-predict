# Resultados de la validación y los escenarios del objetivo 4

La validación permitió cuantificar el error del modelo departamental y comparar su desempeño con referencias históricas. Los escenarios permitieron identificar tres comparaciones condicionales con reducción efectiva del IPM que superaron los controles establecidos. Estos resultados no representan efectos de políticas ni una proyección para 2026.

## Validación temporal del modelo

El ejercicio principal entrenó con 2018, 2019 y 2021–2023, correspondientes a 165 observaciones, y evaluó 2024–2025, con 66. Cada modelo permaneció fijo para ambos años evaluados. La selección de parámetros se realizó únicamente dentro del entrenamiento, mediante ventanas temporales. La respuesta fue la media global recibida de Saber 11 por departamento del colegio y año. Los filtros y los conteos auditados se conservaron.

| Especificación o referencia | MAE | RMSE | R² |
| --- | --- | --- | --- |
| Composición y tiempo | 12,538 | 14,729 | 0,283 |
| Composición y tiempo más IPM | 9,704 | 12,031 | 0,521 |
| Composición y tiempo más dimensiones e indicadores | 8,479 | 10,251 | 0,653 |
| Promedio territorial del entrenamiento | 7,405 | 8,076 | 0,784 |
| Último puntaje disponible | 3,103 | 4,114 | 0,944 |

Fuente: E3, corte 2023, selector temporal, respuesta global, conjunto de 66 observaciones. MAE y RMSE se expresan en puntos del puntaje global; R² no es un porcentaje de aciertos.

Añadir pobreza disminuyó el error frente a la especificación de composición y tiempo, pero ninguna de las dos especificaciones con pobreza superó las referencias históricas. El último puntaje disponible fue la referencia de menor MAE en esta comparación. Para 2025 utiliza el puntaje observado de 2024, mientras los modelos permanecen congelados desde 2023; esa actualización informativa debe considerarse al interpretar la comparación.

Se conservó también el corte previsto originalmente: entrenamiento hasta 2022 con 132 observaciones y evaluación 2023–2024 con 66. Los MAE fueron 11,935 para composición y tiempo, 9,807 al añadir IPM y 7,880 al usar dimensiones e indicadores. El promedio territorial obtuvo 5,599 y la persistencia 3,584. Los dos cortes se presentan separados porque cambian los años evaluados y la información de entrenamiento (E3).

La precisión se expresa mediante errores porque el resultado es numérico. Un MAE de 9,704 significa que la estimación se alejó, en promedio, 9,704 puntos del puntaje observado. Para expresar un porcentaje de predicciones aceptables sería necesario definir previamente un margen de error justificable; no se escogió ese margen después de observar resultados.

## Comprobaciones adicionales

La selección dejando un año fuera se mantuvo como sensibilidad de la metodología escrita. En el corte hasta 2023, sus MAE globales fueron 12,455 para base, 9,704 para IPM y 7,582 para componentes. Esa selección puede utilizar años posteriores al año interno retirado y no equivale a una simulación estrictamente temporal; no reemplazó retrospectivamente el selector principal por obtener una cifra menor (E3).

Al dejar un departamento completo fuera, se repitió la selección y el ajuste con los otros 32. Los MAE fueron 10,987 para base, 9,300 para IPM y 7,153 para componentes. Se trata de transferencia territorial durante los años de desarrollo, no de una prueba sobre años futuros. Las 99 decisiones de las tres especificaciones documentan la exclusión del territorio evaluado (E4).

La robustez con el porcentaje de estudiantes en niveles 3–4 de Matemáticas obtuvo MAE de 9,576 para base, 8,720 para IPM y 6,024 para componentes, en puntos porcentuales. La persistencia obtuvo 2,559. Excluir 2021 del entrenamiento produjo MAE global de 12,323, 10,804 y 8,130, respectivamente, conservando 2024–2025 para evaluación. Estas comprobaciones no modifican la respuesta principal ni ofrecen respaldo para una superioridad general frente a persistencia (E3).

Los años evaluados ya habían sido examinados durante la investigación. Las reglas actuales separan su uso del entrenamiento y la selección, pero no convierten estos años en una reserva inédita. Las entradas de pobreza y composición del año evaluado son observadas contemporáneamente: la validación es retrospectiva y condicional, sin certificación de disponibilidad anterior al examen.

## Escenarios propuestos y controles

Se empleó el modelo auxiliar con IPM agregado, seleccionado dentro del entrenamiento hasta 2023: Lasso con alpha 1. La referencia corresponde a las entradas observadas de 2025. Se mantuvieron constantes el tiempo, las proporciones de evaluados en establecimientos oficiales y zona urbana y el número de evaluados. La comparación se calcula entre dos predicciones del mismo modelo, no entre una predicción hipotética y un puntaje observado.

Se revisaron cinco propuestas para cada uno de los 33 territorios. Las reducciones se expresan en puntos porcentuales de IPM, no en porcentajes relativos. La convergencia propone reducir el IPM de los territorios por encima de 13,0 hasta ese valor, mediana no ponderada de los 33 territorios en 2025. No se interpreta como la incidencia nacional del DANE.

| Propuesta | Combinaciones revisadas | Admitidas | Con reducción efectiva admitida | Rechazadas |
| --- | --- | --- | --- | --- |
| Referencia sin cambio | 33 | 6 | 0 | 27 |
| IPM menos 1 punto | 33 | 3 | 3 | 30 |
| IPM menos 3 puntos | 33 | 0 | 0 | 33 |
| IPM menos 5 puntos | 33 | 0 | 0 | 33 |
| Convergencia a la mediana departamental | 33 | 4 | 0 | 29 |
| Total | 165 | 13 | 3 | 152 |

Fuente: E5; evidencia/resumen_escenarios.csv. “Revisadas” incluye propuestas rechazadas por soporte, cuyas predicciones hipotéticas no se publicaron. No corresponde afirmar que se obtuvieron 165 simulaciones válidas.

Los controles exigieron IPM válido y dentro del rango de entrenamiento y del rango histórico del mismo departamento; también rangos de composición y tamaño y cercanía conjunta a observaciones de entrenamiento. Tanto la referencia como el escenario debían pasar. El año 2025 extrapola la tendencia aprendida hasta 2023: estos controles no certifican soporte temporal (E5).

## Resultados de los escenarios admitidos

Solo las reducciones de un punto en Meta, Sucre y Tolima superaron todos los controles para un cambio efectivo.

| Departamento | IPM de referencia | IPM propuesto | Puntaje estimado de referencia | Puntaje estimado del escenario | Diferencia |
| --- | --- | --- | --- | --- | --- |
| Meta | 12,3 | 11,3 | 255,338 | 255,912 | +0,574 |
| Sucre | 25,4 | 24,4 | 243,957 | 244,530 | +0,574 |
| Tolima | 12,2 | 11,2 | 254,176 | 254,749 | +0,574 |

Fuente: E5, admitido y reducción mayor que cero; evidencia/escenarios_efectivos.csv. Son puntajes estimados por el modelo, no resultados académicos observados bajo una intervención.

La diferencia coincide entre los tres territorios porque el modelo lineal utiliza un coeficiente común de IPM de −0,573608 puntos globales por punto porcentual del índice. No se identificó una respuesta causal particular de cada departamento. Tampoco se estableció un umbral de relevancia educativa que permita llamar importante a esta magnitud.

Las seis referencias sin cambio admitidas corresponden a Antioquia, Caldas, Meta, Sucre, Tolima y Putumayo. Las cuatro entradas admitidas de convergencia son Antioquia, Caldas, Meta y Tolima: ya estaban por debajo de la mediana, por lo que la reducción y la diferencia son cero. No constituyen ejemplos de convergencia efectiva.

No se admitieron reducciones de tres o cinco puntos ni convergencias efectivas. El principal motivo de rechazo fue el rango histórico departamental; numerosos valores de 2025 ya quedaban fuera del rango de entrenamiento. Estos rechazos indican falta de soporte bajo un protocolo conservador, no una demostración de que esas reducciones sean socialmente imposibles. Se conservaron los motivos de todas las propuestas en el archivo completo E5.

## Alcance del objetivo

El cuarto objetivo cuenta con evaluación temporal, referencias y robusteces verificables, y tres escenarios locales condicionales. Su cumplimiento literal conserva brechas: la promesa de una reserva nunca vista no es recuperable retrospectivamente y los escenarios dimensionales proporcionales no se ejecutaron porque no se demostró coherencia entre tasas marginales e IPM. La alternativa académica es acotar expresamente el objetivo a validación retrospectiva y escenarios del índice agregado con soporte comprobado, conservando los rechazos.

## Fuentes de resultados

Fuente: E3, objetivo4_validacion_escenarios/resultados/metricas.csv y predicciones.csv; E4, DECISIONES_TERRITORIALES.json y residuos_departamentales.csv en la misma carpeta; E5, escenarios.csv, SOPORTE.json y coeficientes_modelo_escenarios.csv en la misma carpeta. El registro EVIDENCIAS_Y_REFERENCIAS.md ofrece los procedimientos y las ubicaciones complementarias.
