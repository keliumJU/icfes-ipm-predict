# Respuestas y tratamiento de los pendientes

Fecha: 2026-10-08. Fuente del antecedente personal: mensaje del usuario en esta sesión, no un log de ejecución histórica. Alcance conservado: fase 1, sin modelos.

| Punto | Respuesta del usuario | Tratamiento de auditoría |
|---|---|---|
| 20212 | Recuerda un error de lectura; la cohorte está en el consolidado final | No intentar recrear el fallo ni excluir 2021. Comprobar pertenencia y puntajes contra el TXT actual. Conservar el defecto del panel raíz como hallazgo histórico y usar reconstrucción separada |
| 1 | TXT aportados en `raw_data`; carpeta previa renombrada | Inventariar los 16 TXT, auditar completos los doce del universo, conservar 2020/2025 fuera del análisis y cotejar SHA de once CSV renombrados y consolidado |
| 2 | No conoce criterios de selección de 59 columnas; remite a preparación | Revisar los cinco scripts. No atribuirles una selección que no contienen. Registrar esquema y conservación observados; reconstruir población analítica con reglas explícitas desde TXT, sin depender de aquel recorte |
| 3 | Solicita explicación | `ESTU_CONSECUTIVO` identifica el registro de aplicación; ayuda a detectar duplicación del registro, no identifica necesariamente una persona a través de exámenes. `COLE_CALENDARIO` distingue A/B/OTRO/faltante. Ambos existen en los TXT y se controlan sin publicar IDs |
| 4 | Solicita explicación y cree que raw permite resolver | Hay globales recibidos que difieren de la fórmula calculada con las cinco pruebas. Cotejar con TXT distingue diferencia ya presente en fuente de alteración al unificar. Conservar globales y no deducir una regla especial sin evidencia |
| 5 | No controla toda la redacción del grupo; pide propuesta registrada | Guardar `propuesta_correccion_tesis.md` y tabla de reemplazo explícita; no editar ACA2. Distinguir propuesta de acuerdo ya adoptado. La ausencia de archivos históricos se resuelve como limitación documentada, no recreando modelos |
| 6 | Solicita explicación | AUC y Brier escritos en un informe no prueban que se obtuvieron con el archivo actual. Las predicciones/modelos permitirían recomputarlos. Sin esos artefactos, rotular «históricos reportados, no reproducidos». No constituye un requisito de entrenar ni impide auditar la base actual |

## Resultado de los controles ya concluidos

Los 3.401.100 registros del consolidado coinciden bidireccionalmente con el filtrado de los TXT en 16 campos críticos; cero casos sobrantes y cero firmas ambiguas en los doce periodos, incluido 20181 y 20212 (`actualizacion_20261008/conservacion_raw_final.csv`). Esto verifica periodo, grado, geografía codificada, fecha de nacimiento, género y seis puntajes; no todos los atributos socioeconómicos.

Los filtros secuenciales reproducen 4.039.755 registros recibidos, 3.433.542 estudiantes, 3.432.366 tras excluir libertad S, 3.401.100 con seis puntajes positivos/disponibles y código de colegio, y 2.984.199 grado 11 (`filtros_raw.csv`). Se verifican 608.458 bilingüismos faltantes antes del reemplazo documentado; la auditoría no realiza esa imputación ni depende de bilingüismo.

La población de grado 11 incluye calendario A: 2.901.089, B: 78.075, OTRO: 5.034 y faltante: 1 (`calendarios_raw.csv`). No se agregó un nuevo filtro de calendario para mejorar concordancia. «Dos periodos de aplicación» no significa que cada registro pertenezca exclusivamente a A o B.

Las 525 diferencias de fórmula retenidas ya existen en raw: 414 grado 11 y 111 grado 26 en 20222. En el conjunto raw con cinco pruebas positivas existen 527 discrepancias aritméticas; dos adicionales no permanecen tras todos los filtros. La regla que explica esas diferencias no se ha autenticado. Es una advertencia de fuente, no motivo para recalcular, imputar o excluir puntajes (`formula20222_raw.csv`, `filtros_raw.csv`).

## Lo que continúa como desconocido

No hay metadatos que autentiquen URL/fecha de descarga, criterio histórico de selección a 59 columnas, logs del fallo de lectura ni artefactos de los modelos previos. Se preservan como limitaciones de autenticación histórica. La reconstrucción actual se apoya en archivos locales identificados por huella y reglas comprobadas; no se declara reproducido aquello que falta.
