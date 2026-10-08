# Propuesta de corrección para el grupo

Preparada el 8 de octubre de 2026. Es una propuesta para incorporar en ACA2; el PDF original no se modifica. Las ubicaciones se refieren a páginas físicas del PDF vigente.

## Ajuste de población y construcción

Mantener en las pp. 53–69 la población de grado 11, la asignación al departamento del colegio y los años 2018, 2019, 2021, 2022, 2023 y 2024. Las cifras comprobadas son 2.984.199 registros y 198 celdas departamento-año, con 33 territorios por año. No retirar 2021 ni Bogotá por problemas del panel anterior: el consolidado final contiene 20212 y el anexo de IPM contiene Bogotá en todos los años estudiados.

Texto propuesto para sustituir la explicación de la p. 115:

> La asociación departamental se construye con registros de Saber 11 de estudiantes de grado 11 correspondientes a las dos aplicaciones de cada año entre 2018 y 2024, sin incluir 2020. Cada registro se asigna al departamento de ubicación del colegio. Se conservan estudiantes sin privación de libertad reportada, con código departamental de colegio disponible y puntajes positivos y disponibles en las cinco pruebas y en el global. El resultado es el promedio de puntaje global dentro de cada departamento-año, calculado como suma de puntajes dividida entre su número de registros. No se imputan puntajes. La unión con el IPM y las tasas de privación utiliza el código departamental y el año, con una fila por llave. La construcción comprobada contiene 2.984.199 registros y 198 celdas, correspondientes a 33 territorios y seis años, incluido Bogotá y el año 2021.

La referencia a «estudiantes» describe registros de aplicación; no debe interpretarse como seguimiento de personas únicas. El identificador de la fuente es de registro y no permite por sí solo demostrar unicidad de personas entre exámenes.

## Tabla 12 y sección añadida

No conservar los valores actuales de tabla 12 atribuyéndoles la nueva población: se reproducen bajo otra construcción, con departamento de presentación, cinco años y 32 territorios. Eso demuestra la diferencia entre versiones. Sustituir la tabla por un cálculo explícito sobre las 198 celdas del resultado principal, o mantenerla en un anexo rotulado «exploración histórica con otra población».

La tabla alternativa `evidencia/actualizacion_20261008/tabla12_propuesta_198.csv` presenta las 16 asociaciones de IPM y tasas de privación con el puntaje global: correlación en 198 celdas y correlación entre las medias de los 33 territorios. Estas dos medidas responden a preguntas distintas y ninguna demuestra efectos causales. No usar cortes de correlación calculados con toda la serie para fijar automáticamente predictores de una evaluación posterior.

Texto propuesto para las pp. 116–117:

> Las correlaciones se presentan como descripción de la asociación observada. Se distinguen las correlaciones calculadas sobre las 198 celdas departamento-año de las calculadas sobre las medias de los 33 territorios. Las tasas de privación marginales no se suman para obtener la incidencia de pobreza: esta utiliza privaciones conjuntas y el umbral de identificación del IPM. Las asociaciones no identifican causas ni efectos de intervenciones. La selección y evaluación del modelo departamental requieren un protocolo independiente de este análisis descriptivo.

## Puntajes y antecedentes de modelos

Conservar los puntajes globales suministrados por la fuente. La fórmula aritmética estándar se utiliza como control de consistencia, sin reemplazar puntajes oficiales recibidos. Si un caso ya difiere en el TXT, debe rotularse como diferencia presente en la fuente, no como error introducido al unificar ni como una recalificación demostrada.

Texto propuesto para diferenciar los antecedentes del objetivo 3:

> Los informes previos reportaron resultados de clasificadores que distinguían promedios departamentales menores o mayores que 250. Esos resultados se conservan como antecedentes históricos reportados, cuya ejecución no se ha reproducido en esta auditoría. El objetivo vigente estima el puntaje global promedio, una variable continua. Por tanto, las métricas, coeficientes e importancias de esos clasificadores no se trasladan como resultados del modelo propuesto ni se interpretan como impactos de política.

## Evidencia y decisión pendiente de edición

- Población principal: `auditoria/evidencia/reconciliacion_anual.csv`, `resumen_tesis.json`; ACA2 pp. 53–69 y 73.
- Construcción distinta: `auditoria/evidencia/cotejo_tabla12_hipotesis.csv`, `resumen_seccion115.json`; ACA2 pp. 115–117.
- IPM completo: `auditoria/evidencia/cotejo_ipm_celdas.csv`, incluidas las seis filas anuales de Bogotá.
- Verificación nueva de originales: `auditoria/evidencia/actualizacion_20261008/`, procedimiento `auditar_raw_20261008.py`.

Esta propuesta registra la sustitución metodológica que se recomienda al grupo; no afirma que el grupo ya la aceptó ni que editó la tesis. Los cuatro artefactos históricos citados en pp. 115–117 siguen ausentes. Una sustitución documentada permite cerrar su auditoría como antecedentes de otra construcción, sin exigir recrear su ejecución ni entrenar modelos.
