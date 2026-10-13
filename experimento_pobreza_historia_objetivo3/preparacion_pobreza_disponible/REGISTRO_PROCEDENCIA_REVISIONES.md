# Procedencia, ediciones y revisiones

Registro documental v1, 12/10/2026. IDs oficiales y ubicaciones en `REFERENCIAS.json`; huellas iniciales en `PARTIDA_DOCUMENTAL.json` y metadatos actuales en `METADATOS_LOCALES.json`. No se incorporaron cifras externas ni se descargaron microdatos/anexos de datos.

## Cadena local preservada

La base del contraste cerrado es `experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv`, SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`. Población, transformaciones, periodos y agregación constan en `experimento_pobreza_historia_objetivo3/PROTOCOLO.md` y auditoría v2, secciones Resultado y población e IPM. Estos controles históricos no se repitieron; esta fase solo comprobó huellas y metadatos. No se recalculó media ni se leyó contenido de registros individuales.

Los TXT locales están nombrados `raw_data/Examen_Saber_11_<año><1/2>.txt`; el calendario incluye cada aplicación de los siete años utilizados. Sus huellas, tamaño y modificación local se guardan en `METADATOS_LOCALES.json`. La compatibilidad de nombre/formato con DataIcfes es evidencia parcial; no demuestra que se descargaron del portal ni identifica versión, primera publicación, historial de revisiones o fecha de adquisición. La reconstrucción propia no es un producto oficial ICFES; descargar agregados oficiales con otra población cambiaría el estimando.

Los anexos locales DANE 2024 y 2025 están intactos:

| Archivo | SHA256 | Nota/edición local | Correspondencia documental |
|---|---|---|---|
| `Fuente del IPM/anex-PMultidimensional-Departamental-2024.xlsx` | `22ed318b6dc8b6f679c6fed59c2ab6da4a592de7de4f8c0b1607233878283381` | Histórico 2018–2024, CNPV 2018; OOXML modified 21/04/2025 | Compatible con producto D2024 fechado 22/04/2025; no cotejo exacto remoto. |
| `Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx` | `73caab08046d6b35f80326b1b6f2e9b1cb8ad75a2ac4946515fda320ffaaf447` | Histórico 2018–2025, CNPV 2018; nota 14/04/2026 | Compatible con D2025; no identidad exacta acreditada. |

La auditoría previa v2 cotejó valores históricos de los dos libros y no encontró diferencias frente a la base v1. Es una **comprobación local histórica entre dos ediciones tardías**, no prueba de estabilidad desde cada publicación inicial. No se reejecutó en esta fase. `METADATOS_LOCALES.json` recoge hojas y rótulos ahora; las ubicaciones de años y notas se toman de los CSV históricos `encabezados_ipm_2025.csv` y `notas_ipm_2025.csv`. No se extraen nuevos valores.

La imagen local `Fuente del IPM/archivo-IPM-descargado.png` muestra una fila “Anexo departamental”, 14/04/2026, XLS, 470 KB. Se inspeccionó completa. Sin URL visible, fecha de captura, registro de descarga ni huella del objeto remoto, no certifica descarga o adquisición. Solo concuerda con el rótulo de D2025. No se transforma el nombre de la imagen en evidencia de procedencia.

## Eventos oficiales y límites

| Evento | Evidencia | Interpretación y estado |
|---|---|---|
| Comunicado departamental de IPM 2018 fechado 12/07/2019 | D2018ORIGINAL, PDF p. 1; página histórica DANE separa serie Censo 2005 | Edición anterior; no autoriza usar valores locales recalibrados en cortes de 2019. Primera publicación absoluta no certificada. |
| Recalibración 2018 y publicación 2019, 14/07/2020 | DRECALIBRACION, pp. 1–3 | Cambió base censal/factores; nota declara no comparabilidad con serie previa. No acredita todas las tasas departamentales ese día. |
| Anexo departamental 2019 fechado 21/12/2020 | D2019, tabla por departamentos | Fecha de edición/actualización; primera fecha del producto no identificada. No inventar primera disponibilidad con esta nota. |
| Anexos departamentales 2021–2025 | D2021–D2025 | Fechas de productos, no certificado de cada valor local en esas fechas. |
| Boletín 2023 corregido el 07/05/2024 | D2023CORRECCION, nota de tabla; corrección p. 3 | Tipografía del año observado; no prueba modificación de anexo/cifras. No se generaliza “sin revisiones”. |
| Comunicado 2025 reemplazado el 20/04/2026 | D2025, nota en tabla | Precisión de redacción sobre personas; no revision demostrada de anexo. |
| Ajuste PDET 22/12/2023 | DPDET, nota informativa | Otro universo/producto; antecedente excluido de problemas activos del total departamental por falta de vínculo. Reabrir solo con evidencia nueva. |
| Nota local sobre operativo ECV 2021 y cambio de nivel del agua 2019→2020 | CSV histórico `notas_ipm_2025.csv`, A52/A866 y A868 | Advertencia de medición local; no fecha de publicación ni causa de errores predictivos. 2020 permanece excluido. |
| Carga anonimizada Saber 11 2021 calendario A | I2021CARGA, p. 146 | Septiembre–diciembre 2021 según informe, sin fecha exacta ni vintage. No supone disponibilidad de B. |
| Revisión/publicación Saber 11 2023 A+B | I2023CARGA, p. PDF 112 | Enero–marzo 2024 según informe; fecha exacta, primera edición e igualdad de puntajes pendientes. |
| Transformación de DataIcfes y desagregaciones nuevas | I2023CARGA p. PDF 111, IDATA, INUEVAS | Contexto de reediciones/documentación. No evidencia concreta de recalificación del puntaje local. |
| Fechas actuales de sábanas y cuadros de salida ICFES | IAGREGADOS, IESTADISTICAS | Publicación/actualización de productos distintos; no sustituye calendario de los TXT ni fecha de cálculo propio. |

## Cuatro fechas que no se confunden

1. **Primera publicación:** fecha efectiva del producto y edición pertinente. No demostrada para todos los archivos/celdas exactos; los intervalos institucionales se conservan como intervalos.
2. **Edición revisada:** nueva versión o reemplazo documentado. Recalibración CNPV y reemplazos de texto se registran con alcance distinto. No hay un historial exhaustivo de revisiones de cada anexo/TXT.
3. **Adquisición:** fecha y medio de obtención del objeto local. No hay recibo/log autenticado en antecedentes necesarios revisados; se marca NO DEMOSTRADA, no “no existe en todo el repositorio”. Los PDF/imágenes oficiales descargados ahora son documentos de esta consulta; no adquisición de datos históricos.
4. **Modificación local:** mtime actual del sistema de archivos y modified OOXML son verificables pero editables. Se conservan por separado, nunca como disponibilidad pública. Ambos libros tienen created OOXML 2007-01-25: evidencia de metadato heredado de plantilla, no existencia de cifras 2024/2025 en 2007.

Sin descargar nuevas bases o paneles, la alternativa actual es explicitar la brecha de identidad de versión y producir un cierre incompleto. Resolverla podría requerir certificados oficiales o documentación archivada con huellas; cualquier futura adquisición de datos queda pendiente de autorización distinta.
