# Continuidad propia de investigación v2 — estado vigente

Actualización:2026-10-10, America/Bogota. **Fases1–3 cerradas localmente**.
Esta continuación autoriza y ejecuta únicamente fase3 con protocolo2.0.2 congelado.
Fase4 y notebook personal no ejecutados ni entregados; requieren autorización expresa.
El estado anterior se conserva íntegro más abajo como antecedente sin vigencia operativa.

## Partida, alcance y conservación

HEAD real `0664ac21100982006d1a20670c7e987879444dc6` coincide con cierre conocido de fase2.
Rama `codex/objetivo3-v2-piloto` reutilizada; Git limpio antes de crear fase3. No trabajo
previo sobrescrito. AGENTS/continuidad primero; del plan solo fase3, líneas104–115.
Protocolo2.0.2, configuraciones, registro/código compartido y antecedentes v1 necesarios
en lectura. PDF efectivamente leídos:ninguno, cero páginas; citas anteriores son históricas.
Manifiesto fase2/congelación y huellas comprobados sin regenerar fases1–2.
Siete fuentes originales intactas por huella binaria, sin repetir censo raw.
Snapshot versionados y cierre verificables en fase3/resultados/integridad_inicial.json y
conservacion_final.json. Solo nuevos entregables fase3 y esta continuidad se incluyen
en commit local descriptivo; su hash se informa fuera del manifiesto, sin autorreferencia.
Sin modificaciones de originales/fases1–2/v1/CONTINUIDAD_OBJETIVO_3.md/.gitignore ni push.

## Decisiones concretas vigentes: usuario, comprobaciones y enmiendas

**Usuario y protocolo congelado:** único panel fase1, SHA256
`6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
Población ESTUDIANTE, no libertad S, seis puntajes presentes/positivos, geografía del
colegio, grado11, sin filtro calendario; media global recibida, sin recalcular/redondear.
Peso igual por territorio-año; conteos solo trazabilidad. IPM(1), tasas(15), ambas(16);
2020 excluido definitivamente, sin auditoría ni sensibilidades. Normalización territorial
solo en memoria. Cien configuraciones exactas, semilla prospectiva20261010, bandas0.1
MAE y luego RMSE, menor número entradas, familias/orden JSON; sin criterios modificados
según métricas. Referencia v1 estructural fija reentrenada con20261010;20261008 histórico.
Cinco externas2021–2025, todas las anteriores autorizadas en entrenamiento; internas
expansivas desde2018→2019,1/2/3/4/5 validaciones. Transformaciones exclusivamente dentro
del entrenamiento, sin clipping, imputación ni ajustes finales con todos los años.

**Comprobaciones actuales:**231 filas,33 territorios por año;198 históricas exactas y
prefijo literal. Parámetros/defaults/lock exactos y entorno existente comprobados
Python3.12.14/sklearn1.9.1, pip check aprobado; no instalación ni red. Datos sintéticos y
dobles prueban separación/selección/persistencia/reanudación/límite/terminación antes del
piloto, sin métricas reales ni gasto del presupuesto del panel. Código operativo,
parámetros, versiones, orden y entradas congelados antes del primer ajuste real.

**Enmiendas técnicas fase3, sin modificar congelados:**
- E3-01: clasificar agregado interno mediante regex temporal completa; subcadena `_i`
  también coincide con `_ipm` externo. Solo extensión de reporte, sin impacto en
  selección/evaluación;49.500 internas y particiones exactas verificadas.
- E3-02: corregir cota descriptiva de §7: pueden existir9 IDs externos distintos
  (global, tres especificaciones, media, tres OLS, v1), no8; cota sin fallos≤1555, no1550.
  Evidencia por conteos antes de leer métricas; conservar roles/deduplicar IDs es única
  alternativa que no modifica selección/cobertura. Tope obligatorio7200s intacto.
  Conteo efectivo1500 internos+42 externos+10 repeticiones=1552, sin repetir ajustes.

Evidencia/impacto/alternativa/decisión/comprobación en fase3/ENMIENDAS_TECNICAS.md y
registro_problemas.md; incidencias sintéticas previas conservadas separadamente.

## Resultados realmente ejecutados y verificados

**Procedimiento completo.** 1552 ajustes, cero fallos; tiempo acumulado
1540.906905419055s de7200 y saldo5659.093094580945s. Ledger persistente serial
con procesos interrumpibles, transformaciones/comunicación/referencias/repeticiones
incluidas, sin reiniciar al reanudar. Diez repeticiones, diferencia máxima0 puntos.
Los modelos históricos no se cargan; todos los ajustes son artefactos v2 nuevos.

Nueve procedimientos/comparadores con165 externas cada uno, mismas llaves;49.500
predicciones internas,51.216 predicciones por artefacto verificadas. Recálculo independiente
con math.fsum desde CSV guardados confirma anterioridad, particiones exactas, roles,
observados contra panel, transformaciones, parámetros y huellas. Principales resultados:

| Procedimiento | MAE | RMSE | Sesgo pred−observado | R² conjunto |
|---|---|---|---|---|
| v2 global por ventana |4.879557188161031|6.194961008561882|−0.9758642686030827|0.8729260233776192|
| v1 fija reentrenada |5.979303244989078|7.31238747219388|−0.6682847841766807|0.8229492143632028|

Mejora exacta100×(MAE v1−MAE v2)/MAE v1 = **18.392545281085766%**.
Denominador positivo y mismas165 filas; satisface umbral futuro≥5% sin redondeo adicional.
No se exige mejora tres-de-cinco-años ni se interpreta umbral como significancia.
MAE mejora en cinco años, deteriora en8 de33 territorios: resultados/deterioros.csv y
metricas.csv. Ambas tiene MAE externo4.821934448903931, menor que global, pero no se
selecciona retrospectivamente con externos ni se sustituye el criterio principal.

Ganadores globales:2021 extra_trees_ambas_04;2022 extra_trees_tasas_04;
2023/2024 extra_trees_tasas_00;2025 extra_trees_tasas_04. Cada selección global/por
especificación se guardó antes del externo. No ganador único elegido con esos errores.
Fuentes completas: fase3/resultados/ganadores.csv, seleccion_AAAA.json en piloto/,
metricas_internas.csv, metricas.csv, predicciones_internas.csv/predicciones_externas.csv,
verificacion_resultados.json, fallos.json, piloto/ledger.json/reproducibilidad.json y
ajustes/ETIQUETA/ (modelo, parámetros, entradas, transformaciones, versiones/semilla,
tiempo, advertencias, huellas y predicciones). Advertencias capturadas íntegras.

Informe completo fase3/INFORME_PILOTO.md, fuentes editables/README/generador y único
notebook útil01_resultados_piloto.ipynb: tres celdas de lectura realmente ejecutadas
mediante Python exec, validado con nbformat; no kernel Jupyter ni entrenamiento extra.
No salidas de ejecuciones no realizadas. Conservación/manifiesto verificables en
fase3/resultados/conservacion_final.json y manifiesto_cierre.json.

## Advertencias activas y pendientes

Casos completos y Guainía (238 vs404; diferencia descriptiva21.012106 puntos), procedencia
local sin autenticación independiente, comparabilidad IPM, geografía colegio versus
residencia de hogares/enlace ecológico, dependencia temporal/territorial y pocos años.
No se interpretan predicciones como efectos causales. 2025 exploratorio, no reserva
inédita. Antecedentes59/esquema82, causa antigua20212 y regla global desconocida siguen
archivados con ubicación/motivo heredados; no reapertura sin evidencia nueva pertinente.
No queda control indispensable del piloto pendiente. Falta únicamente autorización
expresa de fase4 para revisión/notebook personal condicionado, ahora con umbral satisfecho.
No simulación, objetivo4, nuevo ajuste final, descarga de datos, push ni fase4 en esta fase.

---

## Antecedente conservado del cierre de fase2 — sin vigencia operativa

Las declaraciones siguientes de piloto no ejecutado/fase3 pendiente corresponden al
cierre anterior y quedan superadas por el estado vigente de arriba.

# Continuidad propia de investigación v2 — estado vigente

Actualización: 2026-10-10, America/Bogota. **Fases 1 y 2 cerradas localmente**.
Solo fase2 autorizada/ejecutada en esta continuación. **Piloto no ejecutado**;
fase3 exige autorización expresa. No notebook personal ni resultados predictivos nuevos.

## Partida y alcance de esta continuación

HEAD real `7c71c13e68420a2a4dd8f894efd7a540da8af7b5` coincide exactamente con cierre
conocido fase1. Rama `codex/objetivo3-v2-piloto` reutilizada; Git inicialmente limpio.
Snapshot360 archivos versionados y siete fuentes en fase2/resultados/integridad_inicial.json.
AGENTS/continuidad leídos primero; del plan solo fase2 líneas63–103; protocolo v1 y
antecedentes necesarios en lectura. PDF ahora: ninguno, cero páginas.
No se repitió censo raw, no se regeneró fase1 y no se usó candidato como base principal.

## Decisiones vigentes — usuario, comprobaciones y nuevas

**Usuario:** panel validado de fase1, exclusión definitiva2020 (sin auditoría/sensibilidades),
población/filtros/media global recibida/geografía del colegio/peso igual, IPM/tasas/ambas;
100 configuraciones, semilla20261010, presupuesto7200 segundos acumulados incluido
referencias/repeticiones; notebook personal solo con mejora MAE conjunta≥5% frente v1
reentrenada en las mismas ventanas, sin tres-de-cinco-años, informe aunque no mejore.
2025 exploratorio, no reserva inédita; no causalidad ni significancia del umbral.

**Comprobación:**231 filas y33 territorios en2018/2019/2021–2025;198 filas históricas
exactas y prefijo literal. Panel SHA256
`6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
05/08 históricos frente5/8 en2025: representación normalizada únicamente en memoria
a dos dígitos y33 códigos conocidos validados, sin tocar CSV (enmienda técnica).
217 cotejos de manifiestos fase1/v1 y siete fuentes comprobados; excepciones históricas
continuidad/informe verificadas en sus commits. Conservación_final.json registra359
versionados intactos y única actualización autorizada de continuidad v2.

**Decisiones nuevas, previas a resultados predictivos:** protocolo v2.0.2
fase2/PROTOCOLO_V2.md, configuración íntegra en resultados/configuraciones_congeladas.json.
Cinco evaluaciones externas expansivas2021–2025 (33 filas cada una), entrenamiento
con todos los años anteriores autorizados. Internas expansivas desde2019 anteriores
al externo:1/2/3/4/5 ventanas. Selección propia por externo, concatenación de165 errores
externos del procedimiento completo; no ganador escogido con errores externos.
Bandas0.1 puntos MAE/RMSE, menor número entradas, orden media/OLS/Ridge/ElasticNet/SVR/GB/ET,
orden JSON. Transformaciones solo dentro del entrenamiento; sin imputación/clipping.
33 candidatos por especificación + media; cuatro referencias media/OLS ya incluidas.
Comparador fijo v1 gradient_boosting_ambas_07 con estructura/defaults históricos; aplica
semilla20261010 por instrucción del usuario y registra20261008 como antecedente, sin
convertirse en candidato adicional de búsqueda. No reutilizar joblib/MAE históricos.
Hasta1550 ajustes prospectivos sin fallos, referencias/repeticiones incluidas; tope7200s
prevalece. Ledger persistente/procesos terminables, fallo/cobertura/umbral definidos antes
 del piloto. No final sobre todos los años ni nuevos contrastes en el piloto diseñado.

## Verificación realmente ejecutada y entregables

Nueve controles aprobados por Python y repetidos en notebook de verificación realmente
ejecutado con kernel y nbformat (dos celdas código). Panel/union/particiones leen solo
agregados reales estructurales. Escalado/selección/métricas/predicciones/presupuesto:
datos sintéticos y dobles, nunca resultados reales de los33 territorios. Predicciones
sintéticas de3 filas con recálculo independiente, extremo externo1e100 sin influencia,
selección/tolerancias/negativos, presupuesto persistente y terminación real de doble lento.
Cero candidatos ajustados/cero predicciones sobre panel real/cero segundos de piloto.

Entorno transitorio v1 ausente, recuperado offline de caché local con mismos paquetes:
Python3.12.14/sklearn1.9.1, pip check aprobado, lock/versiones efectivas registrados.
Kernel inicial bloqueado por sockets del aislamiento e interrumpido; ejecución fuera
 del aislamiento autorizada y exitosa. Primer fallo de formato territorial y congelación
con semilla v1 inicialmente interpretada se conservan en fase2/resultados/antecedentes/;
correcciones antes de cualquier ajuste real, con evidencia/impacto/alternativa/decisión
 en registro_problemas.md. No hay control indispensable de fase2 pendiente.

Rutas: fase2/PROTOCOLO_V2.md, README.md, INFORME_CIERRE.md, registro_problemas.md,
fuentes/*.py compartidas/editables/generador, requirements.lock.txt,
notebooks/01_protocolo_verificacion.ipynb y resultados/ (controles, congelación,
conservación, manifiesto, huellas y evidencias reales de pruebas). Sin notebooks de
entrenamiento, simulación o personal. No alteraciones originales/fase1/entregables v1/
CONTINUIDAD_OBJETIVO_3.md/.gitignore, descargas de datos, objetivo4 ni push.
Commit local descriptivo de cierre fase2 solo nuevas rutas y esta continuidad;
su identificador se informa al usuario, sin autorreferencia de manifiesto.

## Limitaciones y siguiente paso

Persisten casos completos/Guainía, procedencia local no autenticada independientemente,
comparabilidad IPM, enlace ecológico colegio/residencia y dependencia temporal/territorial.
59/esquema82, causa antigua20212 y regla global desconocida siguen archivados con
ubicación/motivo históricos; no se reabren sin nueva evidencia pertinente. No transformar
predicciones contemporáneas en efectos causales ni umbral en significancia.
Pendiente únicamente trabajo futuro autorizado expresamente: fase3/orquestación/piloto
100 configuraciones y dos horas, reporte completo con MAE/RMSE/sesgo/anuales/territoriales
incluidos deterioros; notebook personal condicionado al procedimiento completo≥5%.

---

## Registro histórico de cierre de fase1 — conservado como antecedente

Lo siguiente describe la ejecución anterior; sus pendientes de fase2 están superados
por el estado vigente de arriba. Sus advertencias y comprobaciones permanecen.

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
