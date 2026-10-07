# Continuidad del objetivo 3

Fecha: 2026-10-07 (America/Bogota). Alcance: **únicamente fase 1**.
Estado: avance verificable; auditoría incompleta por insumos y decisiones de procedencia pendientes. No avanzar a fase 2.

## Partida y conservación

- Commit de partida: `c288074795f2c8b1b4865b73f8e08561cecd4448`; Git inicialmente limpio. No existía continuidad: se comenzó con inventario local.
- Inventario: 33 archivos con tamaño/SHA-256 y dos directorios vacíos; incluye doce CSV ignorados. Originales conservados y `.gitignore` intacto. `Resultados Guardados/` y `Entorno de ejecución/` siguen vacíos.
- No se entrenaron modelos, imputaron puntajes, modificaron originales ni adoptó la exclusión de 2021. No se entrega base analítica ni diccionario de una base validada.
- Cierre solicitado: commit `fase 1: avance de auditoría y pendientes`; consultar identificador en Git y respuesta de cierre. No hacer push.

## Bloques completados y evidencia

1. **Documentos y scripts:** ACA2 tiene 58 páginas leídas completas de 126; mapa exacto y 68 pendientes en `auditoria/mapa_tesis.md` y `evidencia/mapa_paginas.csv`. Bloques pertinentes de población, objetivo, transformaciones, tablas y asociación revisados con notas. Dos informes previos completos, incluida inspección gráfica. Scripts originales inspeccionados; no se ejecutó ninguno de modelos. Páginas pendientes fuera del foco no se presentan como revisadas.
2. **Censo:** once periódicos de 59 columnas suman 3.973.901 filas; consolidado de 79 columnas tiene 3.401.100. Controles por bloques sobre todos los registros relevantes. Lectura estructural de ambos niveles: 7.375.001 filas sin ancho incorrecto, tabs ni filas exactas repetidas; no prueba unicidad personal. Fuentes: `controles_todos.csv`, `estructura_duplicados.csv`.
3. **Conservación:** cero filas consolidadas sin correspondencia en proyección de 16 campos en los once periodos disponibles, normalizando únicamente representación numérica y relleno de fecha. Falta fuente 20181. No prueba identidad ni todas las variables. Fuente: `conservacion_registros.csv`.
4. **Panel y 2021:** panel raíz tiene 193 resultados y cinco celdas 2021 faltantes. Sus 15.514 filas de 2021 coinciden con 20211 actual en 168 controles de medias/conteos. Omite 534.706 filas de 20212 existentes en consolidado. Otros cinco años coinciden con todos los grados actuales. Causa histórica del fallo sin demostrarse: recuperación y delimitadores son pistas. Fuentes: `panel2021_vs_periodo20211.csv`, `comparacion_panel_recibido.csv`.
5. **Población:** grado 11 actual suma 2.984.199 filas, 198 celdas, 33 territorios cada año y mínimo 190 en Guainía 2021. Neto preliminar 117.805 = 534.706 omitidas de 20212 menos 416.901 fuera de grado 11; no pérdida aislada de estudiantes. Fuentes: `reconciliacion_anual.csv`, `resumen_tesis.json`.
6. **IPM:** 3.168 cifras coinciden exactamente con hoja/celda del XLSX local; 198 llaves únicas sin nulos, incluido Bogotá. Notas y unidades registradas. Identidad incidencia×intensidad exige convertir incidencia ajustada de fracción a puntos porcentuales; contribuciones difieren hasta 0,1 por redondeo. Fuentes: `cotejo_ipm_celdas.csv`, `notas_ipm.csv`, `identidades_ipm.csv`.
7. **Tesis y calidad:** principales conteos/asociaciones de grado 11 reproducidos; tres diferencias a un decimal entre 24 valores de tabla 7 y dos a dos decimales entre 42 correlaciones de tabla 10. Se conservan sin adaptar criterios. 13.604.400 cotejos de niveles coinciden. Hay 525 discrepancias de fórmula global en 20222, también en periódico: 414 grado 11 y 111 grado 26; no se corrigen ni excluyen. INSE: 683.744 nulos y 4.621 valores >100, umbral exploratorio sin rango oficial afirmado. Fuentes: `cotejo_tabla7_declarado.csv`, `cotejo_tabla10_puntajes.csv`, `niveles_desempeno.csv`, `formula_global20222_detalle_agregado.csv`, `inse_exploratorio.json`.
8. **Sección p. 115:** hipótesis documental presentación/grado 11/cinco años/retirada de Bogotá reproduce 32 correlaciones de tabla 12 a tres decimales. Hay 165 celdas antes y 160 después de retirar Bogotá. No autentica cuatro artefactos ausentes ni justifica exclusiones; contradice colegio/seis años/198 celdas de metodología principal. Fuentes: `cotejo_tabla12_hipotesis.csv`, `resumen_seccion115.json`.
9. **Históricos:** muestra del informe 132/41 y 66/29 coincide con conteos actuales de todos los grados; panel viejo produce 127/50 y 66/29; grado 11 produce 132/61 y 66/39. No son entrenamientos. Métricas/rankings históricos no verificables sin bases con huella, probabilidades/modelos y entorno. Fuentes: `reconciliacion_muestras.csv`, matriz de 59 afirmaciones.

El diagnóstico completo está en `auditoria/diagnostico_calidad.md`; cada afirmación tiene ubicación, dictamen, evidencia y pendiente en `auditoria/auditoria_afirmaciones.csv`. Los controles son resultados agregados separados, no una base aprobada.

## Versiones y procedimientos

Python usado: 3.12.14 del runtime actual; pandas 2.2.3, numpy 2.3.5, openpyxl 3.1.5. Python del sistema: 3.14.7, sin esas bibliotecas. Dependencias de modelos ausentes y no instaladas. Versiones **actuales**, no históricas verificadas. Detalle: `evidencia/entorno_actual.json`, `dependencias_scripts.csv`, `verificacion_cierre.json`.

Orden y limitaciones: `auditoria/procedimientos/README.md`. Se repararon procedimientos nuevos de unidades IPM, alineación de índices y normalización de representación; evidencia afectada regenerada íntegramente sin cambiar criterios/fuentes. Control final compara SHA-256 contra inventario conservado. No sobrescribir ese inventario antes de cotejar nuevas fuentes.

## Pendientes indispensables

- Obtener TXT originales de doce periodos y metadatos, especialmente 20181; procedimiento real de selección a 59 columnas, intermediarios pre-FIX/FIX, logs/mermas de recuperación 20212 y versiones que produjeron panel/consolidado. Sin ellos no se validan filtros iniciales de estudiante/libertad ni cobertura del censo.
- Recuperar identificadores y calendario para unicidad y cobertura; no sustituirlos por proyección de 16 campos.
- Explicar 525 discrepancias globales 20222 con versión/regla oficial de fuente, conservando puntajes recibidos.
- Resolver formalmente construcción pp. 53–69 frente a 115–117. Obtener `unir_datos.py`, `correlaciones_predictoras.py`, `Resultado_de_la_asociacion.xlsx`, `Correlaciones_variables_predictoras.xlsx` o documentar sustitución explícita. No editar originales.
- Para autenticar históricos: bases con huella, modelos/probabilidades, logs y entorno; no entrenar para llenar esa ausencia en fase 1.

## Condición de avance y próxima sesión

Fase 1 no terminada. Se completó lo verificable con insumos locales en los controles descritos; no se valida reconstrucción de extremo a extremo. Fase 2 requiere población, periodos, geografía, denominadores, puntajes y origen trazables, además de construcción coherente con objetivo vigente y decisión documentada sobre contradicciones. 2021 permanece en controles; panel defectuoso no basta para excluirlo.

**Mensaje para siguiente sesión:** continuar únicamente fase 1. Leer esta continuidad y solo su sección del plan. Partir de diagnóstico, matriz y evidencias; no repetir censo salvo nuevas fuentes o discrepancia concreta. Inventariar nuevas fuentes por separado, contrastando huellas actuales; investigar primero selección de 59 columnas, original 20181 y recuperación 20212. Cerrar mermas y fórmula 20222 con evidencia verificable. Mantener pendientes explícitos si no llegan insumos. No entrenar, imputar puntajes, avanzar a fase 2 ni hacer push.
