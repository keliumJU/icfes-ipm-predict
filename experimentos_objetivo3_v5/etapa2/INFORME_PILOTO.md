# Informe del piloto36 v5 — meta global no satisfecha

Fecha cliente2026-10-10, America/Bogota. Exclusivamente etapa2 autorizada y ejecutada.
Protocolo5.0.0 y decisiones del usuario intactos. Resultado exploratorio, sin
confirmación independiente, interpretación causal ni pronóstico anticipado demostrado.

## Resultado principal y condición pendiente

MAE global actual desde CSV guardados=3.429267191379531; persistencia/v3 histórica
recalculada=3.429267191379531. Denominador positivo/finito,165 llaves y
observados idénticos. Fórmula exacta100×(referencia−global)/referencia=
0.0%. Condición≥5% NO satisfecha, sin redondeo,
tres-de-cinco ni sustitución retrospectiva por grupo. Siete procedimientos idénticos
a persistencia en2021–2025; global y cada grupo seleccionaron persistencia.
No contribución incremental del aprendizaje o las covariables demostrada por este
procedimiento. No afirmar agotamiento de otras hipótesis ni eficacia causal.

Ubicaciones: resultados/meta.json; predicciones_externas.csv; ganadores.csv;
piloto/seleccion_2021.json..seleccion_2025.json; procedimiento de recálculo
fuentes/verificar.py:independent/verificar usa math.fsum desde CSV round_trip.
Etapa3 y notebook personal no ejecutados; su condición de meta permanece pendiente.
Prompt exclusivo condicionado guardado en etapa2, no ejecutado; no avance automático.

## Partida, entorno y decisiones verificadas

Cierre real etapa1 Git109797407d75d2097e5b71f8bcef3fc266bc61d2, asunto exacto
`etapa 1 v5: congelar diseno MAE y controles sin piloto`; HEAD/rama
codex/objetivo3-v5-mae inicialmente limpia y sin trabajo posterior. Verificación
etapa1 --verificar en lectura antes de crear etapa2. No reset/sobrescritura;
continuidad histórica cotejada en su commit real, ninguna excepción para otra ruta.
Partida/snapshot/lecturas/entorno y preflight revalidan fuente autorizada SHA
6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadoSHA
 aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc,
231filas/33territorios/198cambios, todos campos/llaves/orden/valores contra
reconstrucción en memoria. Sin raw/fuentes nuevas. Python3.12.14/sklearn1.9.1,
54paquetes exactos lock/pip check revalidados; sin instalación/descarga.

Declaraciones del usuario conservadas: ESTUDIANTE/no libertadS/grado11/seis puntajes
presentes positivos/sin calendario; media global recibida sin recalcular/redondear,
geografía colegio/peso igual territorio-año/conteos trazabilidad.2020excluido,
2018historial,máximo año anterior mismo territorio/2021previo2019,sin anualizar.
Aprendizaje de cambio sin escalar objetivo; previo+predicho, métricas originales.
Grilla36 y defaults íntegros congelados: persistencia1,mediana15,boosting20;
entradas1/2/2/16/17 y orden15tasas v4. Pipeline mediana solo entrenamiento;
boosting pérdida absoluta/semilla20261010/sin scaler/parada temprana.

Decisiones nuevas de implementación antes de fit: adaptación propia de estructura
v4 en piloto.py/verificar.py, lectura sin importar runner v4 ni ejecutar29candidatos;
constructor/selección comunes v5 en lectura; worker.py/motor.py propios. Destinos
restringidos etapa2 con symlinks comprobados. Índice/contexto/huellas/intentos antes
proceso, reanudación verifica artefactos/modelos/matrices/llaves/observados/años/
parámetros/transforms/semilla/versiones. Numérico/convergencia inelegible persistente,
infra máximo1retry/segundo detiene; caída pendiente agota, sin ampliar/reiniciar saldo.
Integridad/cobertura/persistencia/límite detienen incompleto sin meta parcial.

## Pruebas, congelación y auditoría integral

Suite final inventada/dobles aprobada: experimentos_objetivo3_v5/etapa2/resultados/sinteticos/orquestacion_um4la86w; seis grupos amplios,
350 internos,36 registros por selección,7×165externas,global distinto de ganadorgrupo,
6IDs posibles/dedup solo identidad, reanudación completa sin fits adicionales,
artefactos/contexto/ledger/fallos/CSV int-float exacto/rutas/imports/HiGHS/
convergencia/terminación límite e interrupción sin procesos restantes. Fuentes,
defaults,entradas y entorno ligados por SHA en pruebas_sinteticas.json y
congelacion_operativa.json ANTES del primer fit real. Ensayo preliminar rechazado
conservado separado, no usado como evidencia válida. Registro detalla impacto,
alternativa y resolución de incidencias anteriores al fit.

Actual piloto completo:350ajustes/350intentos=350internos+0externos+0repeticiones
ajustadas. Cero fallos,reintentos,advertencias reales; cota378 sin fallos intacta.
Ledger persistente nuevo 460.98687669297215s/7200,
saldo 6739.013123307028s; arranque/Pipeline/comunicación/fallos/retries/
repeticiones presupuestados. Persistencia 0.0005300240081851371s aparte,
sin fit ficticio. Tiempo invocación run 570.9927992220037s;
no se confunde con consumo de ajustes. Cinco comprobacionesglobales recalculadas
sin fit, diferencia máxima0,atol1e-10/rtol0; no ganador ajustado que repetir.

Auditor íntegro:350internos potenciales documentados,360artefactos de predicción
interna (350ajustados+10persistencia),11880filas internas; selecciones36 por cuatro
ventanas=144 registros incluidos inelegibles si los hubiera.2021sin puntuar/seleccionar
candidatos.1155externas=7×165,33territorios×5años, mismas llaves/observados,
sin duplicados/no finitos; IDs/roles/modelos por hash/años/orden/intentos/inputs/
transforms/semilla/versiones/huellas verificados sin cargar modelos de auditoría.
Auditoría complementaria verifica escalas StandardScaler por aritmética y ausencia
de hijos restantes, cero ajustes. Referencias exclusivamente CSV/selecciones/huellas
v1/v2/v3/v4/media/tresOLS, persistencia independiente igual a v3; cero nuevos ajustes
históricos, modelos comparadores no cargados. Resultados/verificacion.json,
auditoria_complementaria.json,piloto/ledger.json/índice/contexto/reproducibilidad.

## Métricas conjuntas y anuales

Cada fila conjunta contiene165pares; cada año33. Métricas conjuntas de todos
procedimientos y referencias (precisión de visualización sin intervenir meta):

|procedimiento|n|mae|rmse|sesgo|r2|
|---|---|---|---|---|---|
|global|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|historico|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|nivel_ipm|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|cambio_ipm|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|cambio_tasas|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|cambio_ambas|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|persistencia|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|referencia_v3|165|3.429267191379531|4.314920647368904|-2.0960105973100562|0.9383511339117978|
|referencia_v2|165|4.879557188161031|6.194961008561882|-0.9758642686030827|0.8729260233776192|
|referencia_v1|165|5.979303244989078|7.31238747219388|-0.6682847841766807|0.8229492143632028|
|referencia_media|165|14.642482640334222|17.55592741338506|-2.808165371154866|-0.020532921973687834|
|referencia_ols_ipm|165|9.493906856300677|12.251515978188971|1.1210047277695108|0.5029968653655981|
|referencia_ols_tasas|165|7.36157204452346|8.975052323917225|-2.413729854081822|0.7332813129218823|
|referencia_ols_ambas|165|8.097991321094774|10.138071897479104|-1.8116551361739601|0.6596778627036145|
|referencia_v4|165|3.6091786595605684|4.546778998773351|-2.300737440412616|0.9315478399592954|

Global anual; siete procedimientos iguales:

|periodo|n|mae|rmse|sesgo|r2|
|---|---|---|---|---|---|
|2021|33|2.6402236932057406|3.5097490978755155|1.4070902157455416|0.9527649735560404|
|2022|33|5.091966313567663|5.553520055345682|-4.506232893548528|0.8879625762913481|
|2023|33|3.2072717302598033|4.010835597004481|-2.250915534656569|0.9425315335825616|
|2024|33|3.9602791908251427|4.921069321485291|-3.63506241817535|0.9165838491604789|
|2025|33|2.2465950290393066|3.1030713458162262|-1.4949323559153742|0.9692850056093002|

Métricas completas por33territorios de cada procedimiento/referencia en metricas.csv,
periodo territorio_CODIGO. Comparaciones exactas conjuntas/anuales/territoriales en
comparaciones_por_periodo.csv. Los165pares completos en diferencias_emparejadas.csv;
delta_error_absoluto en puntos y delta_error_cuadratico en puntos². Deterioros.csv,
deterioros_anuales.csv y deterioros_territoriales.csv conservan encabezados con cero
filas porque v5=persistencia exactamente. Esto no implica ausencia de error predictivo:
MAE3.429267… y sesgo−2.096010… permanecen. No sustituir MAE por sesgo,delta cuadrático
por RMSE ni elegir otra configuración usando externas. Internas y ganadores completos
en metricas_internas.csv/ganadores.csv/seleccionesJSON, sin rescate retrospectivo.

## Entregables ejecutados, conservación y límites

Notebook útil notebooks/01_resultados_piloto.ipynb desde fuente editable
fuentes/01_resultados_piloto.py y generadorPython. nbformat validado;3celdas realmente
ejecutadas con Python exec solo desde resultados guardados, sin kernel ni ajustes.
Muestra auditoría,métricas,meta,selecciones,años y todos deterioros. Salidas solo reales,
fuente/notebook SHA en verificacion_notebook.json. No notebook personal ni simulación.

README/informe/registro/controles/auditoría/congelación/conservación/manifiesto/
continuidad permiten verificar cierre local exclusivamente etapa2. Continuidad
etapa1 íntegra al final y cotejada en commit1097974; originales,v1/v2/v3/v4/continuidades/
atributos/.gitignore/modelos/ledgers anteriores intactos por snapshotSHA. Únicamente
actualización continuidad propia y nuevos entregables etapa2; commit local solo v5,
hash obtenido después del commit y fuera de manifiesto, sin push/autorreferencia.

Límites activos: casos completos y Guainía238vs404/21.012106 puntos (evidencia histórica
v2/fase1/resultados/diagnostico_medias_disponibles.csv, no nuevo cálculo de casos),
procedencia local sin autenticación independiente, comparabilidadIPM/hogares-alumnos,
colegio-residencia/enlace ecológico, dependencia temporal/territorial y pocos años.
2021–2025ya vistos: exploratorio, sin confirmación independiente/causalidad/pronóstico
anticipado demostrado. Antecedentes archivados no reabiertos sin información nueva.
E2-01 y fe de erratasv4 intactos; E3-01/E3-02cota1555v2 no cotasv5. PDF actual0páginas.
Sin controles indispensables pendientes de etapa2. La meta de etapa3 sigue pendiente;
no avance automático, notebook personal, simulación,objetivo4,entrenamiento final,
instalaciones,descargas ni push.

Incidencia documental final resuelta:150escalas verificadas (15medianas×10internas);
primer cierre antes actualizacióncontinuidad archivado en antecedentes_cierre_precontinuidad,
nuevo cierre actual tras completar continuidad. Ningún cambio al piloto/ledger/criterios.
