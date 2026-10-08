# Continuidad del objetivo 3

Actualización: 2026-10-08 (America/Bogota). Alcance ejecutado: **solo fase 1**.
Estado: **fase 1 cerrada para la reconstrucción analítica local validada, con salvedades históricas documentadas**. No se ejecutó ni se autoriza implícitamente fase 2.

## Partida y conservación

- Primera auditoría: inicio `c288074795f2c8b1b4865b73f8e08561cecd4448`, cierre de avance `77c286f43a3c6d811fc68ba9399fd5ec99277528`.
- Esta sesión parte de `77c286f43a3c6d811fc68ba9399fd5ec99277528`. Git tenía un cambio del usuario en `.gitignore`: renombraba la carpeta ignorada y añadía `raw_data`. Se conserva y no se incluye en el commit de auditoría.
- El usuario aportó `raw_data/` y renombró la carpeta a `Datos anteriores a la unificacion/`. Los once CSV renombrados y el consolidado tienen las mismas huellas previas. Los 49 archivos relevantes y dos directorios vacíos están inventariados; 28 datasets ignorados siguen fuera de Git.
- No se alteró ningún original. `Resultados Guardados/` y `Entorno de ejecución/` siguen vacíos. No se entrenaron modelos, imputaron puntajes, editaron PDFs ni excluyó 2021.
- Commit de cierre solicitado: `fase 1: auditoría de datos y evidencia`. Consultar identificador en Git o respuesta de cierre. No hacer push.

## Resultado nuevo y evidencia

1. **Doce TXT completos:** se auditaron 4.039.755 registros de 2018, 2019, 2021, 2022, 2023, 2024 y sus dos periodos. Los cuatro TXT de 2020/2025 se inventarían e inspeccionan por encabezado, fuera del análisis. Cero filas de ancho incorrecto y cero periodos discordantes. Evidencia: `auditoria/evidencia/actualizacion_20261008/esquemas_raw.csv`, `filtros_raw.csv`.
2. **Filtros:** 3.433.542 estudiantes, 3.432.366 sin libertad S, 3.401.100 con seis puntajes positivos/disponibles y código de colegio, 2.984.199 grado 11. Reproducen tabla 4. Cadena FIX concurrente: 3.432.344; FIX+final: 3.401.100. No se mezclan mermas secuenciales y concurrentes. Se comprueban 608.458 bilingüismos faltantes antes del reemplazo escrito; la auditoría no imputa ni usa bilingüismo. Evidencia: `filtros_raw.csv`.
3. **IDs/calendarios:** IDs de registro no faltantes ni repetidos dentro/entre periodos; no son prueba de personas únicas. Grado 11 incluye calendario A 2.901.089, B 78.075, OTRO 5.034, faltante 1. No se añadió filtro A/B. Evidencia: `resumen_raw.json`, `calendarios_raw.csv`. IDs y firmas solo en memoria, no versionados.
4. **Conservación bidireccional:** todos los 3.401.100 finales coinciden con raw filtrado en 16 campos críticos; cero sobrantes o firmas ambiguas en doce periodos. Once periódicos 59 conservan las filas raw en la misma proyección. No se certifican todos los atributos socioeconómicos. Evidencia: `conservacion_raw_final.csv`, `conservacion_raw_periodicos.csv`.
5. **20212:** raw 606.030; elegibles 534.706; grado 11 480.252, todos conservados. El usuario recuerda error de lectura antiguo; no se exige recrearlo ni se declara demostrada su causa técnica. El panel raíz viejo omite 20212; se conserva como versión histórica distinta y no se usa como base actual.
6. **Fórmula global:** 525 diferencias retenidas ya existen en TXT 20222; 414 grado 11, 111 grado 26, delta+1..12, discapacidad N. Los TXT completos tienen 527 diferencias entre casos con cinco pruebas positivas; dos de 20181 no sobreviven filtros. Se conservan globales de fuente; no se conoce regla/versión aritmética, ni se atribuye recalificación/error manual. Evidencia: `formula20222_raw.csv`, `filtros_raw.csv`.
7. **Agregación independiente:** segunda lectura raw por bloques para grado 11 y seis pruebas. Sus conteos/sumas coinciden con los del consolidado en 2.574 cotejos (198 celdas×13 variables). Evidencia: `agregados_grado11_raw.csv`, `cotejo_agregacion_raw_final.csv`.
8. **Base validada:** `auditoria/base_analitica_departamento_anio.csv`, 198 llaves únicas, 33 territorios/año, 2.984.199 registros, sin nulos; medias sin redondeo intermedio y denominadores propios. Colegio/grado 11, incluye Bogotá/2021, sin 2020/2025. IPM+15 tasas se unen uno a uno por código/año; cifras cotejadas previamente contra XLSX local. `auditoria/diccionario_base_analitica.csv` documenta unidades, fuente y advertencias. Validación: `validacion_reconstruccion.json`, `verificacion_cierre.json` en carpeta fechada.
9. **Propuesta al grupo:** `auditoria/propuesta_correccion_tesis.md` ofrece sustitución de pp 115–117 para coherencia con pp 53–69; `tabla12_propuesta_198.csv` recalcula 16 asociaciones de base principal. No se modifica ACA2 ni se afirma aceptación del grupo. IPM/global: r 198 celdas−0,7215676; r 33 medias−0,7521243. No causalidad ni selección automática de variables.
10. **Matriz:** 59 afirmaciones, actualizadas con columnas de dictámenes/evidencias/pendientes 20261007. Métricas previas permanecen históricas reportadas, no reproducidas. Ausencia de probabilidades/modelos no impide auditar la base actual y no se llena entrenando.

## Evidencia anterior conservada

Diagnóstico 20261007 guardado en `auditoria/historico/diagnostico_calidad_20261007.md`; sus CSV/JSON permanecen como entrega fechada anterior. Mapa PDF igual: 58 páginas de ACA2 leídas completas, 68 fuera del foco pendientes, dos informes completos. La actualización no simula lecturas adicionales. IPM: 3.168 cifras locales cotejadas sin diferencias, notas de comparabilidad conservadas. Descriptivos: niveles 13.604.400 coincidencias, INSE 683.744 nulos/4.621>100 exploratorio, tres diferencias de precisión en tabla 7 y dos en tabla 10. Referencias y ubicaciones en diagnóstico actual/matriz.

## Salvedades y acciones posteriores

- No hay metadatos que autentiquen URL/fecha/versión de descarga. Se validan los TXT locales con huellas, no una descarga oficial.
- El criterio histórico de selección 59 columnas y esquema 82 no se recuperó. La construcción nueva explícita evita depender de ellos; la conservación comprobada se limita a campos críticos.
- Causa antigua del error 20212 y logs pre-FIX no autenticados. El usuario permite dejar ese problema histórico documentado y continuar con final conservado.
- Regla oficial que explica 525 diferencias aritméticas desconocida. Se cierran procedencia y conservación; la advertencia de fuente queda, sin nuevo filtro ni puntaje recalculado.
- Artefactos y entorno de modelos históricos ausentes. AUC/Brier/rankings no son resultados reproducidos ni se transfieren a regresión.
- El grupo debe decidir/editar la propuesta de tesis. La auditoría entrega la propuesta y su evidencia; no afirma que ya se adoptó.

Estas salvedades no se ocultan ni se tratan como causas demostradas. No quedan controles indispensables pendientes para la construcción local declarada; autenticaciones históricas distintas siguen con dictamen no verificable.

## Reproducción y próxima sesión

Secuencia vigente en `auditoria/procedimientos/README.md`: `auditar_raw_20261008.py`, `actualizar_entrega_20261008.py`, `verificar_cierre_20261008.py`. No ejecutar inventarios/procedimientos antiguos con rutas renombradas: sobrescribirían estados históricos. Los nuevos usan el commit `77c286f` como referencia fija. Python 3.12.14, pandas 2.2.3, numpy 2.3.5, openpyxl 3.1.5 son versiones actuales, no históricas.

**Mensaje para siguiente sesión:** leer esta continuidad y únicamente la sección del plan que autorice el usuario. Si pide continuar fase 1, partir de los nuevos controles y revisar solo nueva evidencia o discrepancia concreta; no repetir censos completos sin razón. Si autoriza fase 2, usar la base validada con población/colegio/años y salvedades explícitas, sin alterar criterios para mejorar métricas. Esta sesión no ejecutó protocolo, selección, entrenamiento ni escenarios. Mantener originales, cambio de `.gitignore` del usuario y datasets ignorados. No hacer push.
