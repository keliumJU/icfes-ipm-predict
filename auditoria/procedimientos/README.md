# Procedimientos reproducibles de fase1

Todos los programas nuevos leen fuentes y escriben únicamente resultados agregados bajo `auditoria/evidencia/`. No ejecutan scripts de modelos, no entrenan, no imputan puntajes ni cambian `.gitignore`. Lanzar desde la raíz del repositorio; las rutas se resuelven desde cada programa. Inspeccionar cada programa antes de ejecutarlo. Los originales tienen huellas en `../inventario_trazabilidad.csv`.

Intérprete usado en esta sesión:

```bash
/home/kelium/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
```

Dependencias de cálculo: pandas2.2.3, numpy2.3.5, openpyxl3.1.5; biblioteca estándar. Para documentos se requiere `pdftotext` y, opcionalmente, `pdftoppm`. Las versiones son actuales (`../evidencia/entorno_actual.json`); no son el entorno histórico. No se instalan dependencias de modelos.

Ejecutar en este orden con ese intérprete:

```text
auditoria/procedimientos/comprobar_datos.py
auditoria/procedimientos/comprobar_ipm.py
auditoria/procedimientos/comprobar_registros.py
auditoria/procedimientos/contrastar_tesis.py
auditoria/procedimientos/diagnosticos_adicionales.py
auditoria/procedimientos/mapear_documentos.py
auditoria/procedimientos/resumir_evidencia.py
auditoria/procedimientos/contrastar_seccion115.py
auditoria/procedimientos/generar_matriz.py
auditoria/procedimientos/verificar_cierre.py
```

`comprobar_datos.py` recorre toda la información relevante en bloques de100.000 y columnas necesarias. Calcula conteos/flags por periodo, categorías, códigos, denominadores, sumas y medias para recibido y grado11; coteja panel raíz. **En los periódicos faltan estudiante/libertad:** los controles cuyo nombre dice `si_disponible` son escenarios de filtros sobre campos disponibles; no prueban esas condiciones ausentes. `esquema_*.csv` indica cuáles columnas existen. `categorias_*.csv` contabiliza blancos como categoría vacía. La comprobación no altera criterios ni excluye2021.

`comprobar_ipm.py` compara cada valor del CSV y panel contra celdas departamentales/total del XLSX. Lee `data_only=True`; son valores publicados, no nuevas fórmulas de Excel. Registra nombres y celdas; valida llaves y controla incidencia×intensidad/contribuciones eIC. Incidencia ajustada almacenada como fracción se multiplica por100 para comparar porcentajes. La conversión es explícita, no corrección del original.

`comprobar_registros.py` hace una lectura independiente con `csv.reader` de todas las filas y campos, valida ancho, tabs y duplicados exactos por SHA-256 de lista de campos. Luego compara multiconjuntos de16campos entre periódicos y consolidado. Normaliza solo representaciones numéricas enteras y relleno de fechas; no transforma las fuentes. Cero sobrantes en proyección no prueba identidad individual ni igualdad de todas las variables. Se usan matrices de hashes en memoria; no se guardan registros individuales ni hashes en Git. Hace falta memoria para matrices de hasta3,4millones de huellas y sus ordenamientos. Nunca se deduplica la fuente.

`contrastar_tesis.py` agrega grado11 desde controles, calcula medias sin redondeo intermedio, correlaciones de celdas y diferencias2018–2024, niveles completos sobre3.401.100×4 registros, diagnóstico de fórmula global y comparación de20211 contra panel2021. Conserva n propio por prueba. Registra imports víaAST sin importar/ejecutar scripts recibidos. No ajusta una regresión ni estima efectos fijos.

`diagnosticos_adicionales.py` comprueba íntegramente discrepancias de fórmula en20222 en periódico y consolidado y registra campos omitidos de fuente59 frente al esquema del consolidado. No cambia puntajes. `resumir_evidencia.py` compara conteos de particiones históricas y tabla7/tabla10 con cifras declaradas; el conteo de≥250 no es entrenamiento ni recomendación de un umbral.

`mapear_documentos.py` extrae PDFs completos a un temporal, guarda hash y ubicación por página, y conserva una lista explícita de páginas que se leyeron por completo. **No marca automáticamente como revisada una página extraída**.

`contrastar_seccion115.py` contrasta como hipótesis documental la construcción distinta de p. 115 y las 32 correlaciones de tabla 12. Recorre el consolidado por bloques con las columnas necesarias; no ajusta modelos. Las exclusiones descritas se usan solo para comprobar esa afirmación histórica y no se adoptan para la base principal ni para los controles completos de cobertura.

Para reconstruir una inspección visual puntual, por ejemplo:

```bash
pdftoppm -f 66 -l 66 -scale-to 1400 -png -singlefile 'Tesis Vigente/ACA2.pdf' /tmp/aca2_p66
```

`generar_matriz.py` contiene el dictamen editorial de59afirmaciones con fuentes/ubicaciones y pendientes; no inferencias de métricas nuevas. `verificar_cierre.py` verifica conservación mediante SHA-256 de insumos, llaves/niveles y productos requeridos. Las tablas detalladas se enlazan en `../diagnostico_calidad.md`. El Markdown narrativo se revisa editorialmente y no se genera como si todo hallazgo surgiera de una fórmula automática.

La primera ejecución de esta sesión tuvo dos reparaciones de procedimientos nuevos: unidades de incidencia ajustada (fracción frente a%) y alineación de índices departamentales antes de comparar series. Se corrigieron y se regeneraron sus resultados. La primera prueba de proyección requería normalizar ceros iniciales y relleno de fechas; se corrigió y se volvió a leer íntegramente la estructura/proyección. No se modificó ningún insumo ni criterio de población. Se mantiene constancia para no confundir diagnósticos temporales con conclusiones finales.

Una nueva ejecución actualiza archivos de evidencia y versión de entorno/commit observado; no reproduce automáticamente la fecha ni el entorno histórico. Comparar contra las huellas de esta entrega antes de reemplazar el inventario si cambiaron fuentes. La carpeta `evidencia/` no contiene una base analítica aprobada; los dos subconjuntos de agregación son controles separados para reconciliar versiones.
