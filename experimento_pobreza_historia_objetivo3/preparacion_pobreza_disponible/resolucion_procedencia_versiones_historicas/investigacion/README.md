# Investigación documental de procedencia y ediciones

Entrega propia, versión 1.0, 12/10/2026. Empezar por `INFORME_FACTIBILIDAD.md`; decisiones y límites en `COMPLEMENTO_PROTOCOLO.md`, `HALLAZGOS_Y_PENDIENTES.md` y `CONTINUIDAD.md`. Resultado científico: cierre documental incompleto. La entrega de documentación y conservación sí es verificable.

## Entregables

- `CALENDARIO_EDICIONES.csv`: 494 filas por fuente, año, indicador/aplicación y edición; fechas, correspondencia, estados y límites; sin valores analíticos.
- `CORTES_REVISADOS.csv`: quince opciones previas, sin adoptar fecha de uso; pobreza, historia y etiquetas separadas.
- `ADQUISICIONES.jsonl`, `REFERENCIAS.json`, `EXTRACTOS_DOCUMENTALES.md`, `LECTURAS.json`, `INDICE_PDF.json`, `BUSQUEDAS_Y_LECTURAS.md`: procedencia, URL, huellas y lectura por ubicación. Índice automático no es lectura humana.
- `RESUMEN_COTEJO.csv/json`, `COTEJO_CELDAS.csv`, `DIFERENCIAS.csv`, `ESTRUCTURA_Y_NOTAS.json`: comparación reproducible de todas las celdas Total pertinentes. Evidencia por ubicación, sin panel nuevo; solo diferencias contienen cifras.
- `PROCEDENCIA_TXT.json`: metadatos de catorce TXT, sin lectura de registros; identidad histórica pendiente.
- `evidencia/`: copias oficiales adquiridas ahora; originales locales permanecen intactos. Anexo 2020 solo soporta cotejo 2018/2019; no se exportan sus cifras 2020.
- `PARTIDA.json`, `CONTROL_DOCUMENTAL.json`, `CIERRE.json`, `MANIFIESTO.json`, `VERIFICACION.json`, `verificar.py`: conservación, integridad, coherencia y límites.

## Procedimientos y orden

Fuentes Python creadas antes de adquisiciones/procesamiento. No se requieren notebooks. No hay semilla (sin aleatoriedad), modelos, nuevos cálculos de puntajes ni ejecución del contraste. Versiones efectivas en `CONTROL_DOCUMENTAL.json`.

1. `fuentes/iniciar.py`: partida previa de 39.010 archivos regulares externos a investigación, con exclusiones heredadas explícitas y resultado del verificador de arranque. No volver a ejecutarlo sobre entrega existente.
2. `fuentes/adquirir.py` y `fuentes/documentos.py`: solo sitios oficiales y lista documental autorizada; registran URL solicitada/final, adquisición actual y SHA256; no sobrescriben adquisiciones. No ejecutarlos sin autorización de red/al alcance vigente.
3. `fuentes/inspeccionar.py`: inspección de estructura y localización PDF; textos temporales en /tmp. `fuentes/paginas.py`: extracción de páginas especificadas, sin marcar revisión automáticamente.
4. `fuentes/cotejar.py`: bloques completos de dos hojas por libro; IPM y quince tasas, Total; llaves completas y cardinalidades 33×16 por año; Decimal exacto y comparación separada a un decimal. Rótulos territoriales equivalentes declarados. Comprueba tipos numéricos y formatos. XLS usa lectura de valores BIFF; XLSX no tiene fórmulas en celdas cotejadas. No cambia unidades ni divide porcentajes por 100.
5. `fuentes/generar_documentacion.py`: calendario, referencias, lecturas, cortes y controles a partir de cotejos y documentos identificados. Documentos interpretativos Markdown son editables y no contienen resultados de ejecuciones inexistentes.
6. `fuentes/cerrar.py`: manifiesto nuevo y verificación propia. El verificador anterior mantiene su inventario histórico cerrado y no se adapta a la ampliación.

Runtime documental: `/home/kelium/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. `xlrd==2.0.2` solo en `/tmp/icfes_vintage_deps`; no cambios en runtime compartido. Verificación de huellas/coherencia sin dependencias: `python3 -B verificar.py`, desde esta carpeta. Reproducción de cotejo solo lectura, con el runtime documental y lector XLS disponible: `python3 -B verificar.py --cotejo` (usar ejecutable documental anterior). No hace descargas ni escribe salidas; el cotejo temporal se realiza en memoria.

Si se requiere regenerar evidencias, hacerlo en otra entrega autorizada preservando esta; no regenerar y cambiar un manifiesto cerrado. Las exclusiones cubren .git/runtime/cache y destinos de enlaces según la partida: no se afirma certificación retrospectiva de ese universo excluido. El verificador detecta cambios y nuevas escrituras fuera de investigación en su universo regular; la conservación no demuestra disponibilidad histórica.
