# Continuidad propia de investigación v2

Actualización: 2026-10-10 (America/Bogota). **Fase 1 cerrada localmente**.
Fases posteriores requieren autorización expresa. El piloto no se ha ejecutado.

## Partida comprobada y recuperación

Esta ejecución comienza en `742c66577abaeade216d0498e4ecfd12d4c7abfb`, rama
`codex/objetivo3-v2-piloto`, con `experimentos_objetivo3_v2/` sin seguimiento.
La carpeta contenía plan, prompt, código, auditoría y panel, pero no continuidad,
manifiesto ni conservación final. Se trataron como trabajo encontrado, no como
ejecuciones realizadas en este turno. Se conservaron sus archivos byte a byte.
`fase1/resultados/reproduccion_actual.json` registra sus huellas y la nueva ejecución.
El snapshot encontrado `integridad_inicial.json` no se sustituyó ni se reinventó.

Frente al cierre conocido `fc8dc23de8a85cffcc1c87d47ac740650b27ace5`, el único
commit intermedio añade el Excel 2025 y el candidato, sin otras modificaciones.
La rama solicitada ya estaba activa y se reutilizó. Antecedentes consultados:
AGENTS, continuidad histórica completa, protocolo v1 y decisiones, entrega revisada
fase6 y anexo técnico. Del plan v2 se consultaron contexto y exclusivamente fase1,
líneas1–62. No se leyó fase2 ni se avanzó a ella.

## Decisiones y resultados verificables

- **Usuario:** excluir definitivamente 2020, preservar población/filtros v1, no
  imputar puntajes, no modificar históricos, usar únicamente anexo local 2025.
- **Comprobación actual:** censo por bloques de 100.000 de los dos TXT 20251/20252,
  seguido de segunda lectura completa con pandas; 661.891 registros recibidos,
  14.143+482.356=496.499 elegibles. Cero fallos de ancho/periodo, rangos o código
  elegible. Unicidad de IDs retenidos comprobada, sin certificar personas únicas.
  Dos repeticiones raw tienen una fila elegible por grupo, sin deduplicación.
- **Población conservada:** ESTUDIANTE, no libertad S, seis puntajes disponibles
  y positivos, código del departamento del colegio y grado11. Sin filtro de
  calendario; media aritmética de global recibido, sin recalcularlo ni redondear.
  Geografía del colegio. Cada territorio-año tendrá peso igual, conteos solo
  trazabilidad. IPM/15 tasas/ambas; excluidos INSE, áreas, percentiles, derivados
  de y, códigos, año y conteos como predictores. Estimación contemporánea y ecológica.
- **Comprobación del candidato:** 231 llaves únicas, falta IPM. Sus 15 tasas
  coinciden; sus 13 columnas Saber tienen 3.003 discrepancias respecto del estimando
  y 3.003 coincidencias con conteos/medias sin filtro grado11 (medias a dos decimales).
  **Decisión nueva:** conservar candidato y reconstruir por separado desde raw;
  no alterar población para reproducirlo. `cotejo_candidato.csv` y
  `diagnostico_origen_candidato.csv` conservan llaves y filas verificables.
- **IPM:** 528 entradas nuevas y 3.168 históricas cotejadas por hoja/celda.
  Hojas IPM_Departamentos e IPM_Indicadores_Departamento (espacio final),
  filas12–13 año/Total, W para IPM2025 y X para tasas2025. Cero revisiones
  históricas encontradas; ninguna sustituida. Fecha confirmada A54/A868:
  actualizado el14abril2026, distinta del año observado. No se extraen cifras2020.
- **Diagnóstico:** 503.940 con global disponible frente496.499 completos,
  diferencia7.441. Guainía:238 frente404 y diferencia21,012106 puntos de media.
  Registrar selección descriptiva, sin identificar causa o sesgo poblacional.
  `concentracion_otras_pruebas.csv` y concentración secuencial por territorio/periodo
  documentan proporciones. Históricos de filtros por periodo y conteos territoriales
  2024 comparados, sin repetir censos históricos ni inventar exclusiones territoriales
  históricas ausentes.
- **Decisión sobre2025:** incorporar33 filas. Reconstrucción231 filas, 3.480.698
  registros, 33 territorios en2018/2019/2021/2022/2023/2024/2025. Las198 filas
  históricas son prefijo literal y valores exactos de la basev1; SHA256 del panel
  `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
  20251 tiene26 territorios con casos elegibles, 20252 y anual33. No se exige
  completar territorios sin casos por periodo ni fabricar medias.

## Reproducción actual, conservación y lecturas

Nueva ejecución real en copia temporal desde código encontrado: auditor, revisión
integral de IDs, documentación y ocho pruebas, todos salida0. Se reprodujeron24
archivos exactamente, incluido panel. Las diferencias de JSON son duración/entorno
y tiempo de tests, sin diferencia numérica. `verificacion_reproduccion_actual.json`
registra entorno real; el JSON anterior sigue siendo evidencia encontrada.
Después se ejecutó `completar_controles.py` con reconciliación territorial/periodo.
No se reinstalaron dependencias. Semilla no aplica a estos cálculos deterministas.

Snapshot de311 archivos previos y7 fuentes conservados. Los169 cotejos de manifiestos
encontrados se validan por conservación de su snapshot actual y excepciones históricas
documentadas en commits; ninguna nueva excepción. No se modifican continuidad histórica,
.gitignore, originales ni entregables v1. Sin búsquedas/descargas. **PDF leídos ahora:
ninguno, cero páginas**. Referencias PDF del antecedente son lecturas históricas,
no revisión actual. Plan/prompt encontrados conservados completos.

## Piloto futuro, límites y pendientes

**Usuario:** 100 configuraciones y dos horas acumuladas de entrenamiento, incluidas
referencias y repeticiones. Notebook personal solo si el procedimiento completo
reduce el MAE conjunto al menos5% frente a la configuración ganadora v1 reentrenada
en las mismas ventanas:100×(MAE_referencia−MAE_v2)/MAE_referencia. No exigir3/5años.
Mostrar RMSE/sesgo/resultados por año y territorio, incluso deterioros, e informe
completo aunque no mejore. Umbral práctico, no significancia estadística.
2025 exploratorio, sin reserva inédita. Esto es decisión prospectiva, no resultado.

No quedan controles indispensables pendientes para esta ampliación local. Persisten
procedencia/identidad oficial no autenticadas independientemente, selección por casos
completos, comparabilidad IPM, poblaciones distintas/enlace ecológico y dependencia.
Los esquemas/categorías son compatibles con Saber11 local y no muestran Pre Saber
explícito; no se convierte esa comprobación en autenticación de descarga.
Antecedentes59/20212/regla global desconocida y aceptación editorial externa siguen
en su estado histórico, sin reapertura. No se entrenó, seleccionó, predijo, simuló
ni creó notebook de modelos. No objetivo4 ni push.

Pendiente autorizado solo en sesión futura: fase2 y diseño operativo completo del
piloto, tras autorización expresa. Commit de este cierre identificable por asunto
`fase 1 v2: auditar 2025 y cerrar ampliacion con historico conservado`; su hash
se informa al usuario y se verifica en Git, sin autorreferencia circular.
