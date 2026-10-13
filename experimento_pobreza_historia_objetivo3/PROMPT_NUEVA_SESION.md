# Ejecución única: pobreza e historia del puntaje

Trabaja en /home/kelium/Documents/espcarlos/icfes-predict-improved.

## Autorización y entrada

Mi envío expreso de este prompt autoriza ejecutar UNA sola vez el contraste de PLAN.md dentro de experimento_pobreza_historia_objetivo3/, desde preflight hasta entrega, con máximo 7200 segundos totales desde la primera acción de esta nueva sesión. Su existencia o lectura no autoriza ejecución. La sesión anterior fue solo preparación, cerrada por decisión humana con cero fits y sin piloto; no heredar ni reabrir presupuestos anteriores. Este envío autoriza expresamente el presupuesto de la ejecución pendiente, no una repetición de modelos ya evaluados en este contraste.

Leer AGENTS.md, experimento_pobreza_historia_objetivo3/CONTINUIDAD.md y PLAN.md. La carpeta YA EXISTE con documentos preparatorios: no tratar su existencia como evidencia de ejecución ni sobrescribir su preparación. Preservar continuidad anterior propia antes de actualizar. Si se descubre un piloto ya iniciado o cerrado, no repetirlo automáticamente: seguir su cierre, presupuesto y autorización reales.

Determinar si IPM o quince indicadores añaden información a la historia del puntaje para estimaciones condicionales territoriales. No demostrar causalidad ni reducciones reales de pobreza. No ejecutar objetivo4, escenarios, proyecciones, simulaciones, modelo final, nuevo experimento, nuevas fuentes, raw, red, commit/push ni modificar .git, tesis original o experimentos anteriores. Solo escribir aquí y en /tmp.

## Conservación y antecedentes

Leer continuidad principal experimento_final_objetivo3_v6/CONTINUIDAD_V6.md y su referencia ejecucion_autorizada/CONTINUIDAD_V6.md. Revisar solo antecedentes necesarios. La sesión preparatoria ejecutó con éxito, ANTES de crear esta carpeta, el verificador vigente:
experimento_final_objetivo3_v6/ejecucion_autorizada/verificar_entrega.py
Su salida está preservada en preparacion/VERIFICACION_ANTERIOR.json y sus bytes históricos en preparacion/PARTIDA.json.

Ese verificador tiene un control de archivos ajenos que rechazará esta nueva carpeta. No modificarlo, inventar excepciones históricas ni presentar una ejecución parcial como aprobación. Revalidar por un control propio las huellas originales de PARTIDA.json, manifiestos y mappings originales, incluyendo cierres de memoria y continuidades preservadas; distinguir esta comprobación actual del verificador histórico aprobado antes de la carpeta nueva.

Registrar HEAD/asunto/rama/ascendencia/cambios presentes/conservación. Verificar commit histórico real 109797407d75d2097e5b71f8bcef3fc266bc61d2 y trabajo posterior. La continuidad temporal etapa1 solo se reconstruye desde texto/huella de experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json. No reset/limpieza/sobrescritura ajena. Fallo indispensable: cerrar incompleto.

## Entorno exacto

Exigir ANTES de cálculos Python3.12.14/sklearn1.9.1/pip25.0.1/54 distribuciones exactas del lock de experimento_final_objetivo3_v6/ejecucion_autorizada/ENTORNO_DOCUMENTAL.json, pip check, PYTHONDONTWRITEBYTECODE=1, semilla20261010 y un hilo BLAS/OMP.

El entorno fue restaurado offline en /tmp/icfes-v2-fase2-venv; comprobarlo de nuevo. Si falta, este envío autoriza restaurarlo SOLO offline con Python exacto local y las wheels exactas en caché; evidencia en preparacion/RESTAURACION_ENTORNO.json. No modificar runtime compartido ni sustituir versiones. Respetar todos los tags al reconstruir nombres de wheels y conservar bytes/huellas. Si falta una distribución compatible exacta o falla pip check, cerrar bloqueado sin fits. Ninguna descarga o instalación adicional está autorizada.

## Fuentes y población

Principal: experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv
SHA256 6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
Derivada de cotejo: experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv
SHA256 aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc.

Procesar completas mediante código/bloques, resúmenes pequeños en chat. Leer floats round_trip, códigos como strings. Validar 231 filas, 33 territorios por cada año 2018/2019/2021/2022/2023/2024/2025, llaves únicas, finitos, rangos porcentuales de pobreza y coincidencia de historia/cambios.
Mantener población, prom_punt_global recibido, geografía del colegio e igual peso territorio-año; conteos no son predictores. 2018 nivel histórico, 2019 historia nunca respuesta de ajuste, 2020 excluido, previo2021=2019 sin anualizar.
Leer estáticamente DIMENSIONES/TASAS de protocolo/fuentes/configuracion.py para nombres y orden exactos de quince indicadores. No inventar agregados dimensionales ni nuevas variables.

## Respuesta, entradas y candidatos cerrados

Respuesta y_t = prom_punt_global. prev(t)=año disponible anterior.
H=[y_prev(t), y_prev(t)-y_prev(prev(t))]; I=[ipm_t]; D=[quince tasas contemporáneas en orden declarado]; HI=H+I; HD=H+D.
No año/territorio/conteos/identificadores/otras entradas; no IPM+indicadores simultáneos. Pobreza contemporánea es condición de estimación, sin disponibilidad anticipada demostrada.

Orden y total21: persistencia; Ridge para H/I/D/HI/HD y alpha0.1/1/10 dentro de cada grupo; árbol para H/I/D/HI/HD.
Persistencia=y_prev(t), sin fit.
Ridge: Pipeline StandardScaler→Ridge; solver=svd, fit_intercept=True, copy_X=True, positive=False, max_iter=None, tol=0.0001, random_state=20261010 y alpha declarado.
Árbol: Pipeline StandardScaler→DecisionTreeRegressor; criterion=absolute_error, max_depth=2, min_samples_leaf=11, random_state=20261010.
Scaler: copy/with_mean/with_std=True. Restantes parámetros: defaults del entorno exacto, inspeccionados y congelados completos antes de fits. No afinar/añadir candidatos/ventanas/variables por resultados.

Guardar ESPECIFICACION.json y CANDIDATOS.csv completos con IDs/orden/grupos/entradas/parámetros. Preservar PLAN.md y este prompt.

## Ventanas, selección y primario

165 pares externos2021–2025. Externo2021 persistencia fija para todos, sin fit/selección. Para externo2022–2025, internas2021 hasta externo-1: diez ventanas acumuladas; internas2021 respaldo persistencia puntuado. Cada fit usa todas las respuestas desde2021 anteriores al año evaluado.
Pipeline nuevo por candidato/contexto; no modelosprevios ni compartirfits. 200 fits originales =20 candidatos ajustables*(6 contextos internos+4 externos).
Selector: MAE<=mínimo+0.1; RMSE<=mínimo del pool+0.1; menor entradas; orden. Entradas: persistencia0/H2/I1/D15/HI3/HD17.
Histórico: persistencia+RidgeH. Ampliado: persistencia+RidgeH/HI/HD. Con_pobreza: RidgeHI/HD. Selecciones cerradas antes externas correspondientes. Guardar todas las predicciones21 candidatos. Árbol e I/D diagnósticos sin rescate primario.

Primario=100*(MAE_histórico-MAE_ampliado)/MAE_histórico; denominador positivo finito; meta>=5%. Este denominador es nuevo y aprobado antes de resultados. MAE fsum, RMSE reproducible. No cambiar criterio/corte/denominador ni elegir ganador por externa.
Con_pobreza contra histórico secundario; HvsHI/HD a mismoalpha y árboles descriptivos; año/territorio/erroresfirmados/absolutos/sesgo/dirección/grupos/coeficientes/rangos. Si ampliado elige H/persistencia no afirmar uso de pobreza. No p-valores confirmatorios ni escenarios.

## Controles, congelación y presupuesto

Controles inventados de temporalidad/2019solo historia/2020excluido/salto2019→2021/H/no y_t enX/pobreza contemporánea vs futura/futuras respuestas no afectan selección/scalertrain/defaults/selector/reuso mismoIDcontexto/cobertura/llaves/linaje/CSV/rutas/symlinks/fallos/terminación.
Congelar código/reglas/candidatos/tests/fuentes/defaults/entorno/semilla/fuentes del notebook; aceptación operativa propia antes de fits reales.
Ledger serial durable terminable; comunicación/preparación/pausas/fallos/retries/repeticiones incluidos. A5400s absolutos detener nuevos fits, cierre global7200s. Hasta12 repeticiones deduplicadas por ID/contexto de seleccionados en4externos: máximo212fits sinfallos; atol1e-10 rtol0. Único retry total infraestructura; numérico/convergencia sinretry. No ocultar fallos/omitir cobertura. Pendiente tras caída sin medición impide certificar presupuesto.
Guardar matricesX/y/llaves/historia/anios/inputs/unidades/predicciones/params/scaler/coef/intercept/estructuraárbol/advertencias/huellas/identidades/estados/tiempos/terminación. Cerrar piloto antes de análisis y no reabrir saldo.

## Auditoría, notebook y texto último

Auditor independiente probado coninventados, sinfits/importsoperativos/selector/constructores/runners/deserializaciónmodelos. Rehacer selección/métricas y reconstruir predicciones desde paramsguardados; cotejar matrices/fechas/scaler/defaults/inputs/cobertura/copias/linaje/budget/terminación. CSVexacto round_trip, int0=float0, rechazo1e-11. Revalidar referencias solo si mismas165llaves/observados; no independientes.
Notebook resultados con Pythoneditable+generadorPython, nbformatvalidado, celdas realmente ejecutadas y sin nuevosfits. TODAScifras/tablas/figuras nuevas del texto desde celdas llamando funciones compartidas cálculo/guardado; nooutputsmanuales. CSV/JSON/PNG conhuellas, figurasconunidades/n/leyendas y revisiónvisual.

Redactar ÚLTIMO TEXTO_OBJETIVO3_TESIS.md como complemento incorporable. Leer por páginas secciones pertinentes de Tesis Vigente/ACA2.pdf, registrar revisado/pendiente y mantener lenguajeacadémico; sin etiquetas de versiones/historiadeiteraciones en cuerpo. No modificar original ni reemplazar entregasviejas.
Entregar tablascompletas/figuras/notebook/informetécnico/hallazgosimpactoalternativaresolución/lecturas/aceptación/conservación/pendientes/manifiesto/continuidadpropia/verificadorlectura. EVIDENCIAS_TEXTO.csv porafirmaciónnumérica: celda/función/archivo/tabla/llave/n/unidad/huella. Texto cotejado con salidas; citasnoinventadas.

## Interpretación y cierre

Distinguir históricos/recálculos/hipótesis. Todos2021–2025 ya vistos, exploratorio/dependiente/sinconfirmaciónindependiente. Fuente local noautenticada y disponibilidadtemporalsinverificar; aceptación técnica no lo resuelve. Hogaresvsestudiantes/colegiovsresidencia/ecología/pocosaños.
Mejora: qué respalda estudiar posteriormente estimacionescondicionales y qué faltajustificar. Sinmejora: conclusión limitada a estosdatos/modelos, no inexistencia de relación pobrezaeducación. Nunca atribuir cambios delpuntaje causalmente a modificarIPM.
Falloindispensable/timeout/cobertura: incompleto con verificables y pendientes, sin declarar meta ni síntesisdependiente. Comprobar último añoutilizable y evidencia local defecha; siguienteaño solo condicional, sinproyectar. Cierrecontinuidad/manifiesto/verificaciónlectura; ningún avance automático.
