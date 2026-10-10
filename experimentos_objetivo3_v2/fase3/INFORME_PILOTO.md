# Informe del piloto temporal — fase 3 v2

Fecha del cliente: 2026-10-10, America/Bogota. **Procedimiento completo**.
Partida real `0664ac21100982006d1a20670c7e987879444dc6` coincide exactamente con cierre conocido fase2;
rama `codex/objetivo3-v2-piloto` reutilizada, sin cambios previos ajenos. Solo fase3 autorizada.
PDF efectivamente leídos: ninguno, cero páginas. Los PDFs citados en antecedentes no se releen.

## Resultado principal y condición futura

18.392545281086% (valor sin redondeo adicional en verificacion_resultados.json: 18.392545281085766). Umbral futuro ≥5%: True.
Cálculo: 100×(MAE v1 reentrenada−MAE procedimiento v2)/MAE v1 reentrenada.
Se usan idénticas 165 llaves externas y ponderación igual por territorio-año; el RMSE
conjunto procede de los errores concatenados, no del promedio de raíces anuales.
El umbral es práctico, no significancia estadística; no se exige mejora en tres años.
Se entrega informe completo con todos los deterioros. **No se entrega notebook personal**:
su revisión/entrega pertenece a fase4 y no está autorizada en esta solicitud.

| procedimiento | n | mae | rmse | sesgo | r2 |
|---|---|---|---|---|---|
| media | 165 | 14.64248264 | 17.55592741 | -2.80816537 | -0.02053292 |
| ols_ambas_00 | 165 | 8.09799132 | 10.13807190 | -1.81165514 | 0.65967786 |
| ols_ipm_00 | 165 | 9.49390686 | 12.25151598 | 1.12100473 | 0.50299687 |
| ols_tasas_00 | 165 | 7.36157204 | 8.97505232 | -2.41372985 | 0.73328131 |
| procedimiento_ambas | 165 | 4.82193445 | 6.12226592 | -0.75841378 | 0.87589084 |
| procedimiento_ipm | 165 | 9.30422762 | 11.79901233 | 2.25146274 | 0.53903200 |
| procedimiento_tasas | 165 | 4.93918812 | 6.20158882 | -0.96695164 | 0.87265397 |
| procedimiento_v2 | 165 | 4.87955719 | 6.19496101 | -0.97586427 | 0.87292602 |
| referencia_v1 | 165 | 5.97930324 | 7.31238747 | -0.66828478 | 0.82294921 |

Fuente verificable: resultados/metricas.csv, ámbito conjunto; recálculo independiente
con math.fsum en fuentes/verificar_resultados.py, independent. Los CSV se guardan con
17 cifras significativas, sin redondeo para selección/condición. Tabla solo redondeada
para lectura; valores íntegros en CSV/JSON. No se usan métricas históricas como denominador.
La especificación ambas tiene menor MAE externo que el procedimiento global en esta
ejecución; es comparación descriptiva, no autorización para sustituir retrospectivamente
el procedimiento principal. La condición futura usa exclusivamente procedimiento_v2.

## Ganadores y evaluación anual

| externo | global_id | ipm | tasas | ambas |
|---|---|---|---|---|
| 2021 | extra_trees_ambas_04 | svr_ipm_05 | extra_trees_tasas_04 | extra_trees_ambas_04 |
| 2022 | extra_trees_tasas_04 | gradient_boosting_ipm_00 | extra_trees_tasas_00 | extra_trees_ambas_00 |
| 2023 | extra_trees_tasas_00 | gradient_boosting_ipm_01 | extra_trees_tasas_00 | extra_trees_ambas_00 |
| 2024 | extra_trees_tasas_00 | gradient_boosting_ipm_00 | extra_trees_tasas_00 | extra_trees_ambas_00 |
| 2025 | extra_trees_tasas_04 | svr_ipm_04 | extra_trees_tasas_00 | extra_trees_ambas_00 |

Fuente: resultados/ganadores.csv y piloto/seleccion_AAAA.json. Cada selección incluye
las 100 métricas internas, huella e instante anteriores a evaluar el externo; la media
es elegible en las tres especificaciones. El resultado principal corresponde al
procedimiento que selecciona por año, sin ganador único escogido retrospectivamente.

| procedimiento | grupo | n | mae | rmse | sesgo | r2 |
|---|---|---|---|---|---|---|
| procedimiento_v2 | 2021 | 33 | 5.85913438 | 7.03889828 | 4.80496567 | 0.81001409 |
| procedimiento_v2 | 2022 | 33 | 3.87188467 | 5.10258186 | -1.05129786 | 0.90541846 |
| procedimiento_v2 | 2023 | 33 | 3.74359353 | 4.63470853 | -1.77218162 | 0.92326301 |
| procedimiento_v2 | 2024 | 33 | 5.90687942 | 7.23159377 | -3.57067519 | 0.81986454 |
| procedimiento_v2 | 2025 | 33 | 5.01629394 | 6.52141145 | -3.29013235 | 0.86434053 |
| referencia_v1 | 2021 | 33 | 6.00772560 | 7.03945218 | 4.51417448 | 0.80998419 |
| referencia_v1 | 2022 | 33 | 5.54737089 | 6.83399068 | -0.79145935 | 0.83034167 |
| referencia_v1 | 2023 | 33 | 5.03123761 | 6.00279188 | -1.76742478 | 0.87127395 |
| referencia_v1 | 2024 | 33 | 6.88907302 | 8.60102084 | -2.74320976 | 0.74518137 |
| referencia_v1 | 2025 | 33 | 6.42110910 | 7.81579601 | -2.55350451 | 0.80514419 |

Fuente: resultados/metricas.csv, ámbito anual. Se incluyen media, tres OLS, referencia v1
y los procedimientos IPM/tasas/ambas completos en ese mismo archivo. La referencia fija
v1 gradient_boosting_ambas_07 se reentrena por ventana con estructura/defaults congelados
y semilla prospectiva20261010; 20261008 queda solo como antecedente, sin cargar joblib v1.

## Deterioros y resultados territoriales

| grupo | delta_mae | delta_rmse | deteriora_mae |
|---|---|---|---|
| 2021 | -0.14859122 | -0.00055390 | False |
| 2022 | -1.67548622 | -1.73140882 | False |
| 2023 | -1.28764408 | -1.36808335 | False |
| 2024 | -0.98219360 | -1.36942707 | False |
| 2025 | -1.40481516 | -1.29438456 | False |

Delta positivo implica mayor error v2 frente a referencia v1. Fuente:
resultados/deterioros.csv, procedimiento_v2. Deteriora MAE en
0 de cinco años y 8 de33
territorios. Todos los MAE/RMSE/sesgo/R² territoriales, incluidos deterioros, se entregan
en metricas.csv (cinco observaciones por territorio y procedimiento); no se ocultan territorios.
R² territorial usa variación de los cinco observados de ese territorio, sin atribución causal.

| procedimiento | grupo | n | mae | rmse | sesgo | r2 |
|---|---|---|---|---|---|---|
| procedimiento_v2 | 05 | 5 | 2.44382982 | 3.47543175 | 2.36847561 | -0.90852084 |
| procedimiento_v2 | 08 | 5 | 5.44927522 | 7.28539300 | 3.87804966 | -1.22814477 |
| procedimiento_v2 | 11 | 5 | 2.03437614 | 2.21404929 | -2.03437614 | 0.24550675 |
| procedimiento_v2 | 13 | 5 | 2.86923032 | 4.01943899 | 1.37240861 | 0.47741379 |
| procedimiento_v2 | 15 | 5 | 5.09692651 | 5.93013644 | -5.09692651 | -0.69319422 |
| procedimiento_v2 | 17 | 5 | 3.25412445 | 4.70274301 | 0.74006003 | -0.51667773 |
| procedimiento_v2 | 18 | 5 | 3.28283058 | 3.96326116 | 0.04787030 | 0.38550916 |
| procedimiento_v2 | 19 | 5 | 5.05862633 | 6.11963564 | 4.75116152 | -1.74405995 |
| procedimiento_v2 | 20 | 5 | 2.69836439 | 3.85340541 | 0.60059437 | 0.58961394 |
| procedimiento_v2 | 23 | 5 | 6.03664557 | 6.81795174 | -4.23939521 | 0.15187946 |
| procedimiento_v2 | 25 | 5 | 4.68330511 | 5.19076679 | -3.97200249 | -1.74079326 |
| procedimiento_v2 | 27 | 5 | 4.65242738 | 5.18606895 | 4.65242738 | -0.96867365 |
| procedimiento_v2 | 41 | 5 | 5.07915049 | 5.64081375 | -1.93938494 | 0.17012691 |
| procedimiento_v2 | 44 | 5 | 3.61767328 | 4.25509641 | -3.43954327 | -0.15354341 |
| procedimiento_v2 | 47 | 5 | 4.39375272 | 5.08656848 | 4.39375272 | -0.96503778 |
| procedimiento_v2 | 50 | 5 | 3.87068392 | 4.91307490 | -1.52900408 | 0.05490204 |
| procedimiento_v2 | 52 | 5 | 5.62060300 | 6.40959081 | -5.62060300 | -1.17705307 |
| procedimiento_v2 | 54 | 5 | 7.11372951 | 7.99990239 | -6.62999422 | -1.06398160 |
| procedimiento_v2 | 63 | 5 | 7.76443283 | 8.65580036 | -7.54425626 | -0.38822681 |
| procedimiento_v2 | 66 | 5 | 4.58299219 | 4.89088377 | -0.57214156 | -3.38374894 |
| procedimiento_v2 | 68 | 5 | 11.04992473 | 11.95147950 | -11.04992473 | -5.50856531 |
| procedimiento_v2 | 70 | 5 | 4.28826502 | 4.84441686 | -1.72357258 | 0.28244863 |
| procedimiento_v2 | 73 | 5 | 5.44494139 | 6.13475828 | 5.44494139 | -0.99887652 |
| procedimiento_v2 | 76 | 5 | 2.25370745 | 3.51003685 | 1.41937961 | 0.27358825 |
| procedimiento_v2 | 81 | 5 | 4.22948873 | 5.12070653 | -1.12840565 | -0.58741208 |
| procedimiento_v2 | 85 | 5 | 5.83869478 | 6.02162582 | -3.93726317 | -0.05021336 |
| procedimiento_v2 | 86 | 5 | 3.72892674 | 4.36254455 | -0.67948901 | 0.15036711 |
| procedimiento_v2 | 88 | 5 | 2.59690557 | 2.98121098 | -2.59690557 | -0.20960331 |
| procedimiento_v2 | 91 | 5 | 9.20400217 | 10.78168899 | 9.20400217 | -14.48896998 |
| procedimiento_v2 | 94 | 5 | 10.55765924 | 12.21940018 | -7.15233951 | -0.93539123 |
| procedimiento_v2 | 95 | 5 | 3.55322339 | 4.23967889 | -0.46092000 | 0.49505615 |
| procedimiento_v2 | 97 | 5 | 4.33921500 | 5.85244614 | 4.04421769 | -3.35860356 |
| procedimiento_v2 | 99 | 5 | 4.33745323 | 5.13075760 | -3.77441402 | -0.45623329 |
| referencia_v1 | 05 | 5 | 1.61625753 | 2.11397489 | 0.96440723 | 0.29387916 |
| referencia_v1 | 08 | 5 | 8.64559547 | 9.58096862 | 7.72129246 | -2.85350807 |
| referencia_v1 | 11 | 5 | 3.58971922 | 4.07717059 | -3.58971922 | -1.55857736 |
| referencia_v1 | 13 | 5 | 2.76132963 | 4.07711527 | 0.86137135 | 0.46230866 |
| referencia_v1 | 15 | 5 | 4.96290221 | 5.48390863 | -3.38274520 | -0.44796420 |
| referencia_v1 | 17 | 5 | 5.05274128 | 7.19287266 | 5.05274128 | -2.54809761 |
| referencia_v1 | 18 | 5 | 4.71737678 | 5.63643684 | -3.92822677 | -0.24285174 |
| referencia_v1 | 19 | 5 | 8.79854908 | 9.55139715 | 8.79854908 | -5.68461305 |
| referencia_v1 | 20 | 5 | 3.60131328 | 4.05656564 | -0.65330505 | 0.54520025 |
| referencia_v1 | 23 | 5 | 7.11259067 | 9.61313438 | -4.56754594 | -0.68608616 |
| referencia_v1 | 25 | 5 | 3.88656899 | 4.32050960 | -1.90348413 | -0.89881735 |
| referencia_v1 | 27 | 5 | 9.61857307 | 10.83513507 | 9.61857307 | -7.59341558 |
| referencia_v1 | 41 | 5 | 5.53487004 | 6.30269632 | -2.52029779 | -0.03605050 |
| referencia_v1 | 44 | 5 | 5.66773158 | 6.73424763 | -5.66773158 | -1.88930440 |
| referencia_v1 | 47 | 5 | 6.20369105 | 7.41954326 | 4.68671959 | -3.18095464 |
| referencia_v1 | 50 | 5 | 4.13050074 | 6.39951440 | -1.82168280 | -0.60348203 |
| referencia_v1 | 52 | 5 | 7.98533520 | 8.53837377 | -7.98533520 | -2.86330263 |
| referencia_v1 | 54 | 5 | 8.10687944 | 8.41119329 | -5.85016463 | -1.28166390 |
| referencia_v1 | 63 | 5 | 8.64078965 | 9.41397576 | -8.06093464 | -0.64207170 |
| referencia_v1 | 66 | 5 | 5.14142442 | 6.27398070 | 0.27714124 | -6.21368787 |
| referencia_v1 | 68 | 5 | 10.14157088 | 11.13227594 | -9.48695174 | -4.64689681 |
| referencia_v1 | 70 | 5 | 5.71191563 | 6.02413174 | -2.38929144 | -0.10958073 |
| referencia_v1 | 73 | 5 | 5.29490881 | 5.76387923 | 5.29490881 | -0.76449650 |
| referencia_v1 | 76 | 5 | 1.89411193 | 3.08564002 | 0.76113576 | 0.43862894 |
| referencia_v1 | 81 | 5 | 6.56983565 | 7.09615440 | -2.14443588 | -2.04842854 |
| referencia_v1 | 85 | 5 | 6.75379821 | 7.84898752 | -4.99703992 | -0.78433867 |
| referencia_v1 | 86 | 5 | 4.80684588 | 5.27480792 | -0.26032515 | -0.24212375 |
| referencia_v1 | 88 | 5 | 3.92834454 | 4.59190252 | -1.01148538 | -1.86974206 |
| referencia_v1 | 91 | 5 | 9.43244361 | 11.00076926 | 9.43244361 | -15.12482645 |
| referencia_v1 | 94 | 5 | 9.64502224 | 11.04244525 | -5.78393232 | -0.58051821 |
| referencia_v1 | 95 | 5 | 4.33140413 | 5.47848888 | 0.77878262 | 0.15686187 |
| referencia_v1 | 97 | 5 | 5.68800793 | 6.06017992 | 4.69600231 | -3.67351406 |
| referencia_v1 | 99 | 5 | 7.34405833 | 7.68434871 | -4.99283153 | -2.26649570 |

## Ejecución, presupuesto y fallos

1552 ajustes contabilizados, 1540.906905 segundos de7200;
saldo 5659.093095. Tiempo observado incluido arranque/comunicación de procesos:
1540.906905s. Ledger persistente resultados/piloto/ledger.json;
ajustes_resumen.csv y registros por ajuste. Ejecución serial spawn, BLAS/OMP un hilo,
Extra Trees n_jobs1; cada trabajador recibe solo entrenamiento, interrumpible al agotar
saldo. No se reinicia presupuesto al reanudar ni se reutilizan internas entre externos.
La cota descriptiva8 externos/1550 totales de protocolo §7 tiene un error aritmético:
pueden existir9 IDs externos distintos (global, tres especificaciones, media, tres OLS,
v1). Enmienda E3-02 en ENMIENDAS_TECNICAS.md/conteo_enmienda.json corrige solo cota
a≤1555 sin fallos, conservando todos los roles, orden,100 configuraciones y7200s.
No se cambia selección ni se repite entrenamiento; se deduplican solo IDs iguales.

Ajustes fallidos: 0; registros con advertencias o predicciones fuera0–500:
0. Evidencia íntegra en resultados/fallos.json y cada ajuste.json.
Todas las advertencias capturadas se conservan; sin clipping, nuevas semillas/grillas ni
transformaciones. Diez repeticiones al final (cinco ganadores globales y cinco v1), mismo
saldo y tolerancia absoluta1e−10/rtol0: piloto/reproducibilidad.json y recálculo de sus CSV.
No se ajusta modelo final sobre todos los años; no llamadas a modelos de lenguaje al entrenar.

## Trazabilidad y comprobaciones

Única base: fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv,
SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`. 231 filas,33 territorios por2018/2019/2021–2025;
198 históricas exactas y prefijo literal. Normalización05/5 y08/8 solo en memoria.
No se usa candidato ni se repite censo raw; 2020 excluido definitivamente, sin auditoría/sensibilidad.
Población/filtros/media global recibida/geografía del colegio/IPM (1), tasas (15), ambas (16), peso igual
se conservan según protocolo2.0.2 §§1–2 y continuidad. No se cambian criterios según resultados.

Manifiesto fase2, congelación,100 parámetros completos, ventanas y lock comprobados
antes del primer ajuste: integridad_inicial.json, entorno.json. Entorno compatible existente
Python3.12.14/sklearn1.9.1, sin preparación adicional, instalación o red. Pruebas sintéticas
y dobles aprobadas antes del piloto: pruebas_sinteticas.json/log, separadas de resultados
reales y presupuesto del panel; incidencias iniciales conservadas. Congelación operativa
previa a ajuste: congelacion_operativa.json. Enmienda de agregado interno por regex
reconoce etiqueta temporal completa, sin modificar código congelado/selección/evaluación:
fuentes/enmienda_reporte.py y registro_problemas F3-05.

Verificación independiente: verificacion_resultados.json, cobertura `{'media': 165, 'ols_ambas_00': 165, 'ols_ipm_00': 165, 'ols_tasas_00': 165, 'procedimiento_ambas': 165, 'procedimiento_ipm': 165, 'procedimiento_tasas': 165, 'procedimiento_v2': 165, 'referencia_v1': 165}`;
51216 predicciones por artefacto revisadas y
49500 filas internas agregadas. Predicciones externas
con llaves, ID, ajuste, observado, predicción/error y selección_sha256 en
predicciones_externas.csv; internas en predicciones_internas.csv. Modelos v2 completos,
transformaciones ajustadas, entradas, parámetros, semilla, versiones por huella, tiempos,
fallos y huellas en piloto/ajustes/ETIQUETA. Las repeticiones tienen IDs propios.
Anterioridad,33 filas por validación, observados contra panel, parámetros, escaladores y
cobertura idéntica auditados sin acceder a errores externos desde el selector.

Notebook01_resultados_piloto.ipynb generado y validado con nbformat desde fuente Python
editable; tres celdas de código ejecutadas realmente mediante Python exec, sin kernel
Jupyter ni entrenamiento adicional. Modo explícito en metadata/verificacion_notebook.json.
Contiene lectura de artefactos ya verificados; no presenta salidas de ajustes no ejecutados.

## Conservación, advertencias y pendientes

386 archivos versionados previos y siete fuentes originales intactos,
con huellas en conservacion_final.json. Única actualización previa autorizada:
CONTINUIDAD_V2.md. Fases1–2/originales/v1/CONTINUIDAD_OBJETIVO_3.md/.gitignore intactos.
Todas las entregas nuevas están en fase3; sin descargas de datos, simulación, objetivo4,
push ni ejecución de fase4. Manifest incluye entregables nuevos y continuidad v2;
commit local se informa fuera del manifiesto para evitar autorreferencia.

Persisten casos completos/Guainía (238 frente404, diferencia descriptiva21.012106 puntos:
fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local sin autenticación
independiente, comparabilidad IPM (protocolo v1 §8/notas fase1), colegio versus residencia
de hogares/enlace ecológico, dependencia temporal/territorial y pocos años. No se
atribuyen efectos causales ni sesgos cuantificados causalmente. 2025 exploratorio,
no reserva inédita. Antecedentes59/esquema82, causa antigua20212 y regla global desconocida
siguen archivados sin nueva evidencia, según registro_problemas.md.

Pendiente únicamente trabajo posterior autorizado expresamente: revisión de fase4 y
notebook personal condicionado. Estado completo, mejora y presupuesto verificables en
verificacion_resultados.json; no se avanza automáticamente aunque el umbral se satisfaga.
