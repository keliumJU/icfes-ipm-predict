# Decisiones previas a los cálculos de auditoría

2026-10-10, America/Bogota. Primera lectura HEAD `fc8dc23de8a85cffcc1c87d47ac740650b27ace5`; rama nueva `codex/objetivo3-v2-piloto`. Durante la preparación el usuario incorporó sus dos fuentes en `742c66577abaeade216d0498e4ecfd12d4c7abfb`: **partida efectiva de auditoría**. El control de HEAD rechazó la partida anterior antes de crear snapshot o calcular datos; se inspeccionó el diff (solo dos altas) y se registró el nuevo commit. Ambos archivos se conservan sin incluirlos en el commit de v2. Solo fase 1 autorizada.

## Usuario y referencia operativa

El plan aprobado incorpora 2025 a exploración y excluye definitivamente 2020, sin atribuir esa exclusión a nulos no comprobados. El protocolo v1 sigue congelado como referencia histórica; la ampliación v2 es independiente. No se cambia ningún filtro: estudiante, no libertad S, seis puntajes positivos/disponibles, código departamental del colegio, grado11; sin filtro de calendario. Denominadores son registros, no personas únicas.

## Procedimiento concreto de fase 1

- No ejecutar scripts históricos: escriben evidencia anterior. Leer su código para reproducir filtros; escribir un auditor nuevo exclusivamente en v2.
- Procesar ambos TXT 2025 con CSV por bloques de 100.000 registros; validar ancho y periodo de cada fila. Leer todas las filas, guardar solo resúmenes agregados.
- Conservar la semántica histórica de valores ausentes (`''`, `NA`, `N/A`, `NULL`, `null`, `NaN`, `nan`, `None`, `<NA>`), normalización de categorías y coerción numérica. Separar nulo de no numérico, cero, negativo y fuera del rango 0–500 global/0–100 áreas (protocolo §6 y escalas de la fuente). Un fuera de rango elegible es problema activo, no exclusión nueva silenciosa.
- Código numérico entero del departamento del colegio y correspondencia con los 33 códigos de base son controles de validez; no cambiar geografía por residencia/presentación. Auditar IDs únicamente en memoria; no certifican personas únicas.
- Calcular tanto cadena secuencial histórica como filtros concurrentes/combinaciones. Describir nulos por territorio-periodo con categoría separada de geografía desconocida; no redistribuirla.
- Diagnóstico disponible-global: mismos filtros administrativos y global positivo, sin exigir áreas completas. Compararlo con casos completos, sin sustituir y ni inferir ausencia de sesgo.
- Leer solo las dos hojas departamentales del XLSX2025, encabezados, cifras totales de los años autorizados y notas. No extraer cifras2020. Cotejar las15 tasas del candidato y el histórico por llave/celda; cambios históricos del anexo quedan registrados, no sustituyen la base.
- Comparar columnas críticas (conteos y medias de los seis puntajes), sin usar INSE, percentiles ni `_merge` como X. Tolerancia de cotejo de medias `1e-10` puntos; conteos/sumas enteros exactos. Es tolerancia de representación, no ajuste de cifras.
- Si el candidato difiere de raw con filtros acordados, conservarlo como fuente candidata y construir 2025 desde raw validado. Esto resuelve trazabilidad sin cambiar criterios. Documentar diferencias completas, no trasladarlas a la base.
- Exportar ampliación solo con cobertura33, entradas completas y todos los controles indispensables aprobados. Preservar literalmente las líneas históricas del CSV original, además de su igualdad de valores.

Los tests de modelos y el notebook condicionado corresponden a fases posteriores. En esta fase solo controles de datos y pruebas negativas de auditoría. No estimadores, predicciones ni simulaciones. No lecturas PDF ni búsquedas externas previstas; si hacen falta, registrar el alcance efectivo.

## Enmienda de control previa a exportar la ampliación

La primera auditoría completa quedó detenida por dos repeticiones de ID raw. Se guardó su dictamen en `resultados/antecedentes/primera_verificacion_ids_raw.json`, sin generar panel. La revisión integral de IDs y filas (`identificadores_repetidos_revision.json`) demuestra dos grupos de dos filas distintas, cada uno con una sola fila elegible y otra sin grado11; no hay duplicación de filas completas en esos grupos. El control indispensable de unicidad se aplica a la población retenida, y el control raw permanece como advertencia explícita. No se borra ni deduplica ninguna fila, ni se cambia el denominador o filtro. Se añade prueba específica de IDs elegibles y se repite el censo con el mismo protocolo. No hay resultados predictivos observados.

Para explicar la discrepancia del consolidado se añade agregación descriptiva con los mismos filtros pero sin grado11 (`05_codigo_colegio`), nunca destinada a la base principal. Se coteja con el candidato y, en años históricos, con agregados ya guardados del consolidado anterior. Las medias redondeadas se comparan únicamente para diagnosticar procedencia, no para seleccionar y ni alterar la precisión de la reconstrucción.
