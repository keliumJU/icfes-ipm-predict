# Diagnóstico objetivo3 v1 — resultados descriptivos, sin nuevos fits

Fecha cliente2026-10-11,America/Bogota. A–E ejecutados exclusivamente sobre guardados.
La distribución del cambio y las asociaciones anuales observadas varían. Estos
resultados justifican estudiar estabilidad temporal y escasez de historia; no
identifican una causa definitiva del fracaso ni demuestran eficacia de recencia.
Ningún nuevo punto de partida predictivo mejor queda validado. Persistencia sigue
siendo referencia respaldada por estos guardados; v5metaNOsatisfecha permanece intacta.

## Integridad, conservación y entorno

Fuenteúnicav2 SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;derivadov5 SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc. Reconstrucción actual enmemoria
exacta en todos campos/llaves/orden/valores:231filas/33territorios/198cambios.
Evidencia resultados/preflight_actual.json; procedimiento comun_diagnostico.load_panel.
Fuente/derivado no reescritos.Inventario protegido exacto de29640versionados,
comprobado antes de análisis y de nuevo al cierre (conservacion/manifiesto final).

El entorno temporal ausente se restauró con autorización expresa del usuario:
Python3.12.14 del runtime local;54wheels exactos de caché local,bytes conservados,
sin red. sklearn1.9.1/54paqueteslock/pip check aprobados. Pip es herramienta de
instalación excluida del lock igual que contrato histórico. Evidencia:
resultados/restauracion_entorno/wheels.json,entorno_verificado.json y entorno_diagnostico.json.
Excepción autorizada exclusivamente reconstrucción/instalación del entorno;sin fits.

## Cambios observados y particiones originales

Tabla completa estabilidad_anual.csv, llaves periodo=año. Cuantiles lineales,
desviaciónddof1,IQR,rango ysignos exactos;33territorios cada año,198cambios completos.

|Año|n|Media puntos|Mediana puntos|IQR puntos|Negativos|Ceros|Positivos|
|---|---:|---:|---:|---:|---:|---:|---:|
|2019|33|-5.815757|-5.716775|2.399272|33|0|0|
|2021|33|-1.407090|-1.200614|3.888980|23|0|10|
|2022|33|4.506233|4.578600|2.151415|2|0|31|
|2023|33|2.250916|2.668274|1.437207|2|0|31|
|2024|33|3.635062|3.082523|3.050207|2|0|31|
|2025|33|1.494932|1.976252|2.704959|6|0|27|

2019 fue negativo en33/33;2021 en23/33;2022–2024 positivos31/33cadaaño;2025positivos27/33.
2021 compara2019:intervalo2,sin anualizar;resto intervalos1. No eliminar2019 ni salto.
Transiciones en transiciones_signo.csv y transiciones_resumen.csv:10/33cambian signo
2019→2021,23/33en2021→2022,4/33en2022→2023,4/33en2023→2024,6/33en2024→2025.
Trayectorias completas33 y resúmenes territoriales conservados. No años/territorios
independientes ni diagnóstico de ruptura causal.

Contrastes_particiones_originales.csv conserva10particiones originales para objetivo
y18entradas,n_train33/66/99/132,n_valid33. Para valid2022,train2019/2021 mediana−4.094537
frentevalid4.578600 (delta8.673137puntos);se repite por diseño en externas2023/2024/2025.
Impacto: historia previa puede describir otra distribución. Alternativa: estudiar
memoria temporal con protocolo separado; resolución actual mantener todos años y
comparaciones completas. No se prueba que recencia reduzca error.

## Variación y asociaciones

Unión exacta18entradas GRUPOSv5 (ordenprimeraaparición);variacion_entradas.csv contiene
126resúmenes,0constantes exactas/no finitos0,mínimo23valoresúnicos entre resúmenes
anuales. Redundancia_exacta.csv:1071pares,0idénticos;asociaciones_objetivo.csv:252registros,
asociaciones_entre_entradas.csv:2142registros. Pearson/Spearman,rangosmedios,globaln198/
anualn33;en estos datos0correlaciones indefinidas. Controles inventados verifican
salida vacía con razón/n ante constante/insuficiencia/no finitos, nunca correlación0.

Spearman cambio_ipm–objetivo agregado−0.063199;2019−0.025407,2023−0.332553,2025+0.389102.
IPM–objetivo2019−0.034094,2023+0.378238. Spearman agregado previo–IPM−0.765016
(tabla entreentradas,periodo=global). Variación de signo observado no demuestra
inestabilidad de una relación subyacente;agregación mezcla tiempo y territorio.
Impacto: no concluir capacidad predictiva/inutilidad intrínseca por correlación.
Alternativa: comparar aporte incremental prospectivo; resolución tablas completas,
sin p-valores,importancias,selecciónautomática ni umbrales para futurasgrillas.

## Errores guardados y ausencia de pseudo-repetición

Auditoría exacta de360artefactos internos/350metas de ajustes históricos,entradastrain/
test,parámetros completos,semilla/versiones/huellas/llaves/observados/previos/predicciones.
Solo hash de modelos;no carga ni reproducción de sus fits. Copias coinciden exactamente:
11880originales→4752únicas=36×4×33,representante menor externo. Linaje11880filas en
linaje_copias.csv;firmas/meta en auditoria_metadatos_copias.csv. Diezparticiones
acumuladas contienen cuatrovalidaciones únicas2021–2024;no10años independientes.
Análisis por ventana original conserva11880filas,sin deduplicarlo ni cambiar métricas.

144registros guardados cotejados por math.fsum;máximadiferencia2.6645352591003757e−15,
atol1e−12/rtol0soloacumuladores. CSVllaves/valores exactos,sin tolerancia,int/float0válido.
Resultados/cotejo_144_metricas_guardadas.csv (en tablas),auditoria_aritmetica_independiente.csv:
187resúmenes contrastados mediante sumasracionalesFraction sobreerroresIEEEexactos.

Internas únicas,n132porcandidato:MAEpersistencia=3.72493523196459;35ajustados
MAEentre4.75803669983113y5.76129477634711;todosdeltaMAE>0.
Por año,n33/configuración:0de35mejoranen2021,2022,2023;33de35en2024.
Evidencia metricas_internas_unicas.csv,conteos_ventaja_interna_por_anio.csv y
minimos_internos_retrospectivos.csv (descripción,NO nuevosganadores).
Sesgosajustados -5.285045a-4.156112puntos;
direcciónacertada0.340909a0.530303.
Impacto:errores de dirección/sesgo son descriptivamente observables;alternativa
examinar patrones temporales;resolución errores completos,ninguna causa única.
Magnitudes/errores de cambio/deltasabsolutos/cuadráticos completos en errores_*.csv.
Direcciónexacta distingue−/0/+;persistencia acierta0porqueobservados no son0,
pero conserva menorMAE;acierto direccional no reemplaza métrica global.

Externas1155=7×165,33territorios×5años,todosprocedimientosigualespersistencia:
MAEglobal=3.42926719137953,RMSE=4.3149206473689,sesgo=-2.09601059731006,deltaMAE0.
Esto reproduce aritmética actual de resultados históricos, no fits. Errores por
procedimiento/año/territorio/2021–2024/2025 completos;las35configuraciones no seleccionadas
no tienen externas y no se fabrican. Ventaja de algún candidato en2024 no crea
ganador externo ni autoriza alterar selecciones/meta. Error ysesgo de persistencia permanecen.

## Hipótesis, alternativas e incertidumbre

Matriz_hipotesis.csv registra7hipótesis con evidenciafavor/contra,n,ubicación/llave,
impacto,alternativa,resolución/pendiente. H1/H5/H7 apoyadas descriptivamente;
H2signouniforme/H3constantesduplicadascontradichas;H4causaredundancia/H6eficaciarecencia
insuficientemente evaluadas. Alternativas_y_pruebas_futuras.csv desarrolla4alternativas:
recencia,simplificación,máshistoria,conservarpersistencia. Recencia/máshistoria
merecen estudio,ninguna acredita un punto de partida mejor. Simplificación no queda
justificada como remedio suficiente;no todo error procede de muchas variables.

Prueba futura discriminante: protocolo separado antes de resultados que contraste
memoria temporal y disponibilidad de más historia, conserve referencia/evaluación
acordadas y procure años independientes. Para simplificación,comparación de aporte
incremental con tiempo controlado. No fijar grilla/hiperparámetros ni iniciar experimento.
No promesa de5%,selecciónfinal ni efecto causal.2021–2025vistos:exploratorio.

## Advertencias, entregables y pendientes

Conservar Guainía238vs404/21.012106puntos: evidenciahistóricav2/fase1/resultados/
diagnostico_medias_disponibles.csv,no recálculo actual de casos. Procedencia local
no autenticada,IPMhogares frentealumnos,colegiofrenteresidencia/enlaceecológico,
dependenciatemporal-territorial,pocosaños. No pronósticoanticipadodemostrado ni
confirmaciónindependiente. Antecedentes59/esquema82/causa20212/fórmuladesconocida/
E2-01/E3-01/E3-02conservados,no nueva conexión que justifique reabrirlos.
PDFactual0páginas;lecturas históricas no presentadas como actuales.

Pruebas9grupos inventados aprobadas;22tablasA–D+3tablasE/resumen;5PNGdescriptivos
revisados visualmente. Notebook/fuente/generador/verificaciónreal y cierre final
en README/resultados/continuidad. Conservación/manifiesto se sellan después de
notebook/documentación;consultar aceptación_final.json para aceptación definitiva.
Sin pendientes de integridad conocidos;eficaciaalternativas e historia/confirmación
independiente son pendientes científicos,requieren otra autorización.
Sin commit/push/ajustes/simulación/objetivo4/notebookpersonal/entrenamientofinal.
