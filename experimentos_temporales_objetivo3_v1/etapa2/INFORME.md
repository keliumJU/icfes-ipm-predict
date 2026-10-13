# Piloto exploratorio recencia_h2 — informe completo

2026-10-11, America/Bogota. Meta original NO SATISFECHA. Primario fijo: recencia/global,
165 pares (33 territorios × 5 años), igual peso territorio-año.

MAE recencia/global: 3.429267191379531 puntos; MAE persistencia:
3.429267191379531 puntos. Mejora exacta: 0.0%.
Decisión computada sin redondear: 100*(MAEpersistencia−MAEglobal)/MAEpersistencia ≥5.
Delta MAE frente uniforme v5/global: 0.0 puntos, descriptivo sin
umbral nuevo. Los CSV v5/global y v3/persistencia son numéricamente idénticos y no
aportan dos evidencias independientes. Ubicación: resultados/meta.json; procedimiento
autónomo fuentes/auditar.py, referencia reconstruida y cotejada sobre 165 llaves.

La ponderación fue el único cambio material: semivida fija2, ancla máximo train,
todos los años retenidos, media de pesos1; scaler/regresor ponderados o boosting
sample_weight. Entradas/defaults/36IDs/bandas/particiones/semilla20261010 conservados.
2021 persistencia fija sin fit/selección. Cada ventana tuvo ajustes propios; selección
guardada antes externo, deduplicación externa solo por ID. Grupos son secundarios;
ningún grupo/corte/control reemplaza el primario ni rescata la meta.

Ejecución actual: 350 intentos, 402.28817591698316 segundos de
presupuesto7200s, incluyendo spawn/Pipeline/comunicación, sin saldo histórico.
350internos; externas/repeticiones ajustadas constan por etiqueta en ledger.json.
Persistencia sin fit y tiempo separado en tiempos_persistencia.json. Cinco controles
globales aprobados, predicciones repetidas en repeticiones/; atol1e−10 rtol0 solo
para repetición, CSV exactos. Ningún modelo histórico cargado ni nuevos fits uniformes.
Modelos propios de cada ajuste guardados como artefactos auditables, no modelo final.

Auditoría independiente APROBADA: 11880 internas originales, 144 registros, 36IDs,
1155 externas (7×165); 4752 únicas condicionadas tras igualdad exacta de copias y
firmas train/X/y/pesos/defaults/semilla/versiones. Representante menor externo;
linaje completo11880, sin promediar discrepancias. Diez internas acumuladas contienen
cuatro años únicos de validación; no diez años independientes. originales se conservan.
CSV intfloat0 equivalente; pruebas de rechazo1e−11/campos/orden/no finito aprobadas.
Matrices/objetivos/pesos por fila/scaler/warnings y huellas auditados sin deserializar
modelos. Ubicaciones: auditoria_independiente.json, firmas_internas.json, metadatos/,
linaje_internas.csv, predicciones_internas.csv, internas_unicas.csv y tablas/.

Tablas completas: predicciones_errores_pareados.csv contiene errores absolutos,
cuadrados, deltas pareados, dirección exacta−/0/+, magnitudes; metricas_externas.csv
incluye MAE/RMSE/sesgo/n/deltas por procedimiento, año, territorio y cortes2021–2024
frente2025. metricas_internas.csv conserva ventanas originales y síntesis únicas;
registros_144.csv incluye todos los candidatos; selecciones.csv registra35 salidas;
pesos_por_fila_ajuste.csv registra pesos de cada entrenamiento. Gráficos descriptivos
con unidades y n en resultados/graficos/, sin inferencia causal ni nueva selección.

Hallazgo actual: el contraste primario determina no satisfecha para la meta.
Impacto: solo este resultado puede evaluar el objetivo acordado. Alternativa lógica:
conservar persistencia como referencia y reportar todas las salidas/cortes sin rescate;
resuelto en esta fase mediante tablas/auditoría/informe. Eficacia futura y estabilidad
no se deducen de esta evaluación retrospectiva. Más historia o confirmación requiere
fuentes comparables/fechas y autorización separadas; no se descargaron aquí.

Todos2021–2025 ya vistos: resultado EXPLORATORIO, sin confirmación independiente,
causalidad o pronóstico anticipado demostrado. Guainía238vs404/21.012106 puntos es
evidencia histórica en v2/fase1/resultados/diagnostico_medias_disponibles.csv; no
nuevo hallazgo recencia. Procedencia local no autenticada; IPMhogares-alumnos,
geografía colegio frente residencia, enlace ecológico, dependencia y pocos años.
Antecedentes archivados no reabiertos. Meta v5 no satisfecha intacta; no etapa3v5,
simulación/notebookpersonal/objetivo4/entrenamiento final/commit/push/avance automático.

Incidencia propia anterior al primerfit: helper de conservación leyó `destino` en vez
de `enlace` del inventario de symlink. Corregido y recongelado como v2, sin cambiar
criterios científicos. Fallo original/salida y congelaciónv1 conservados; incompleto.json
corresponde exclusivamente a ese intento con fits0, no al estado final. Ver registro.

## Resultado concreto de la selección

Global y los cinco grupos seleccionaron persistencia en2022–2025;2021 fue fijo.
Por eso las siete salidas externas coinciden, todas las diferencias por año y
territorio frente a referencia son0 y el cambio predicho es0 en los165 pares.
Esto muestra que recencia no cambió la política seleccionada en este piloto;
no demuestra que los ajustes ponderados sean idénticos a los uniformes ni que
recencia nunca pueda aportar señal. Ubicación: tablas/selecciones.csv,35filas;
seleccion_2021.json–seleccion_2025.json y predicciones_externas.csv.

|Ventana externa|MAE interno persistencia|Candidato ajustado con menor MAE interno|MAE interno ajustado|Diferencia ajustado−persistencia (puntos)|
|---|---:|---|---:|---:|
|2022|np.float64(2.6402236932057406)|boosting_absoluto_cambio_ipm_03|np.float64(4.084645671895216)|1.4444219786894754|
|2023|np.float64(3.8660950033867016)|boosting_absoluto_nivel_ipm_03|np.float64(5.354612619483248)|1.4885176160965465|
|2024|np.float64(3.6464872456777355)|mediana_nivel_ipm_00|np.float64(4.615343279205507)|0.9688560335277714|
|2025|np.float64(3.7249352319645874)|boosting_absoluto_nivel_ipm_02|np.float64(4.130888996418331)|0.4059537644537432|

Estas diferencias internas son descriptivas: se conserva el selector contractual
MAE/RMSE/bandas0.1/entradas/familia/orden; la tabla no redefine ganadores ni emplea
externas. Todos35 ajustados quedan por encima de persistencia en cada selección
acumulada. Ubicación: tablas/registros_144.csv,36registros porventana, sin nuevas
puntuaciones de2021. Reproducción actual con pesos, distinto de resultados históricos.

RMSE externo global np.float64(4.314920647368904) puntos; sesgo(predicho−observado) np.float64(-2.0960105973100562) puntos.
Dirección exacta correcta 0/165 (np.float64(0.0)%)
bajo signo−/0/+; magnitud media observada np.float64(3.429267191379531) puntos y
predicha np.float64(0.0) puntos. No se interpreta la dirección como
criterio alternativo de éxito. Ubicación: tablas/metricas_externas.csv,corte=global,
procedimiento=global; tablas/predicciones_errores_pareados.csv,165filas global.

Control adicional independiente:360firmas de train y350metadatos cotejados contra
los años exactos anteriores a validación, matrices/objetivos y pesos; escala/suma
ponderada del scaler; cinco persistencias recalculadas sinfit. Resultado aprobado
pruebas_contextos.json,procedimiento fuentes/comprobar_contextos.py. Los3gráficos
se revisaron visualmente completos: ejes/títulos/unidades/n legibles; delta0 territorial
es resultado exacto, no ausencia de cobertura.
