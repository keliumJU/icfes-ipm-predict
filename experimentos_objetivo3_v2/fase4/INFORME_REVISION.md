# Revisión del piloto y notebook personal — fase 4

Fecha cliente: 2026-10-10, America/Bogota. Fase 4 cerrada localmente.
Partida real `b37a2f338f0708958a412f5a0efa09f33861322b`, igual al cierre conocido fase3;
rama `codex/objetivo3-v2-piloto`, Git inicialmente limpio. No diferencias ni cambios
previos que conservar. Únicamente fase4 y continuidad v2 se actualizan.
Plan consultado: exclusivamente fase4, líneas116–134 (encabezado y requisitos hasta
el cierre de fase; el encabezado siguiente se usó solo como delimitador).
PDF efectivamente leídos: ninguno, cero páginas. No nuevas consultas externas.

## Condición exacta y resultado

Se confirma desde CSV: MAE v2 **4.879557188161031**, MAE v1 fija reentrenada
**5.979303244989078**. Mejora exacta **18.392545281085766%**, con denominador
positivo y las mismas165 llaves de33 territorios ×5 años. Supera el umbral práctico≥5%
sin redondeo adicional, sin exigir tres-de-cinco-años ni sustituir el procedimiento
global por otro ganador elegido desde errores externos. **Notebook personal entregado.**
Fuente: resultados/verificacion.json; cálculo reutilizado `condicion_personal` de fase2.

## Métricas conjuntas de todos los procedimientos

Fuente: resultados/metricas.csv, periodo2021-2025, ámbito conjunto.
MAE/RMSE/sesgo en puntos; R² adimensional. Sesgo=predicción−observado.

| procedimiento | n | mae | rmse | sesgo | r2 |
|---|---|---|---|---|---|
| media | 165 | 14.642482640 | 17.555927413 | -2.808165371 | -0.020532922 |
| ols_ambas_00 | 165 | 8.097991321 | 10.138071897 | -1.811655136 | 0.659677863 |
| ols_ipm_00 | 165 | 9.493906856 | 12.251515978 | 1.121004728 | 0.502996865 |
| ols_tasas_00 | 165 | 7.361572045 | 8.975052324 | -2.413729854 | 0.733281313 |
| procedimiento_ambas | 165 | 4.821934449 | 6.122265920 | -0.758413782 | 0.875890838 |
| procedimiento_ipm | 165 | 9.304227621 | 11.799012334 | 2.251462740 | 0.539032002 |
| procedimiento_tasas | 165 | 4.939188124 | 6.201588823 | -0.966951640 | 0.872653972 |
| procedimiento_v2 | 165 | 4.879557188 | 6.194961009 | -0.975864269 | 0.872926023 |
| referencia_v1 | 165 | 5.979303245 | 7.312387472 | -0.668284784 | 0.822949214 |

Comparaciones v2−media, tres OLS y v1 en resultados/comparaciones_referencias.csv,
conjuntas/anuales/territoriales y para los tres periodos. Delta negativo de MAE/RMSE
favorece v2; delta de sesgo indica dirección y requiere comparar su magnitud para
hablar de reducción. Especificaciones comparadas descriptivamente; no se cambia la principal.

## Separación 2021–2024 y 2025

| periodo | procedimiento | n | mae | rmse | sesgo | r2 |
|---|---|---|---|---|---|---|
| 2021-2025 | procedimiento_v2 | 165 | 4.879557188 | 6.194961009 | -0.975864269 | 0.872926023 |
| 2021-2025 | referencia_v1 | 165 | 5.979303245 | 7.312387472 | -0.668284784 | 0.822949214 |
| 2021-2024 | procedimiento_v2 | 132 | 4.845373000 | 6.110623990 | -0.397297249 | 0.871577570 |
| 2021-2024 | referencia_v1 | 132 | 5.868851781 | 7.181023350 | -0.196979853 | 0.822645407 |
| 2025 | procedimiento_v2 | 33 | 5.016293942 | 6.521411449 | -3.290132348 | 0.864340528 |
| 2025 | referencia_v1 | 33 | 6.421109102 | 7.815796012 | -2.553504507 | 0.805144194 |

Mejoras descriptivas separadas: 2021-2024: 17.439165602%; 2025: 21.878076481%. No sustituyen el umbral
principal fijado para2021–2025. Fuente: resultados/metricas.csv, ámbito conjunto.
Cada periodo concatena errores; RMSE no promedia raíces. La aportación de2025 al
MAE conjunto es exactamente una quinta parte por sus33 de165 filas, sin peso por
conteos estudiantiles. El MAE conjunto combina4/5 del MAE2021–2024 y1/5 del MAE2025.
2025 continúa exploratorio, sin reserva inédita; publicación del IPM posterior al año
observado impide presentar este análisis retrospectivo como pronóstico disponible entonces.

## Comparación anual y deterioros territoriales

| grupo | procedimiento | n | mae | rmse | sesgo | r2 |
|---|---|---|---|---|---|---|
| 2021 | procedimiento_v2 | 33 | 5.859134383 | 7.038898282 | 4.804965671 | 0.810014087 |
| 2022 | procedimiento_v2 | 33 | 3.871884670 | 5.102581863 | -1.051297860 | 0.905418459 |
| 2023 | procedimiento_v2 | 33 | 3.743593526 | 4.634708525 | -1.772181621 | 0.923263014 |
| 2024 | procedimiento_v2 | 33 | 5.906879419 | 7.231593766 | -3.570675185 | 0.819864536 |
| 2025 | procedimiento_v2 | 33 | 5.016293942 | 6.521411449 | -3.290132348 | 0.864340528 |
| 2021 | referencia_v1 | 33 | 6.007725604 | 7.039452182 | 4.514174481 | 0.809984186 |
| 2022 | referencia_v1 | 33 | 5.547370891 | 6.833990679 | -0.791459354 | 0.830341670 |
| 2023 | referencia_v1 | 33 | 5.031237609 | 6.002791879 | -1.767424780 | 0.871273945 |
| 2024 | referencia_v1 | 33 | 6.889073018 | 8.601020838 | -2.743209760 | 0.745181368 |
| 2025 | referencia_v1 | 33 | 6.421109102 | 7.815796012 | -2.553504507 | 0.805144194 |

Cero años deterioran el MAE y ocho territorios lo deterioran frente a v1:

| grupo | delta_mae | delta_rmse |
|---|---|---|
| 05 | 0.827572296 | 1.361456860 |
| 13 | 0.107900682 | -0.057676280 |
| 15 | 0.134024306 | 0.446227814 |
| 25 | 0.796736111 | 0.870257189 |
| 68 | 0.908353850 | 0.819203553 |
| 73 | 0.150032582 | 0.370879048 |
| 76 | 0.359595521 | 0.424396836 |
| 94 | 0.912637003 | 1.176954929 |

Códigos corresponden a geografía del colegio, según panel/fase2. Fuente exacta:
resultados/deterioros_v2.csv (incluye también filas sin deterioro). En código13 el MAE
empeora y RMSE mejora; los criterios resumen pérdidas diferentes, sin contradicción.
Todos los33 territorios y nueve procedimientos se conservan en metricas.csv. R²
territorial se calcula contra la media de cinco observados del territorio: baja variación
puede producir R² negativo. Para2025 territorial n=1, R² es no definido/celda vacía,
no cero. No inferir significancia a partir de pocos años o del umbral práctico.

## 165 diferencias emparejadas

Archivo completo: resultados/diferencias_emparejadas.csv, llaves código−año; conserva
IDs/ajustes/selección_sha256/y/predicciones y errores de ambos procedimientos.
- `delta_error_firmado` = e_v2−e_v1, puntos: describe dirección, no ordena exactitud.
- `delta_error_absoluto` = |e_v2|−|e_v1|, puntos: positivo indica peor error absoluto.
- `delta_error_cuadratico` = e_v2²−e_v1², puntos²: positivo indica peor pérdida cuadrática.

Deterioran61 pares; mejora agregada no implica
mejora uniforme. Promediar delta absoluto equivale a diferencia de MAE; promedio delta
cuadrático equivale a diferencia de MSE, no de RMSE. No pruebas nuevas de significancia.
Gráficos: resultados/mae_anual.png, delta_mae_territorial.png y diferencias_emparejadas.png.
Fuentes: revisión.py `independent` importado de fase3, `presentar` y CSV completos.

## Auditoría, referencias y trazabilidad

Manifiestos fase2/fase3 y congelaciones cotejados sin regenerarlos; siete fuentes
originales cotejadas por SHA256, sin censo raw. La continuidad incluida en cada manifiesto
se verifica en su commit de cierre, porque su actualización posterior está autorizada;
no se usa esa excepción para otros archivos. Evidencia: integridad_consulta.json,
partida.json y conservacion_final.json. Registro de conservación fase3 leído y contrastado
con su snapshot de versionados y fuentes. Parámetros/defaults100, referencia v1 fija,
lock íntegro, Python3.12.14 y pip check comprobados; semilla20261010.

Auditoría actual de1552 registros y51216 predicciones de artefactos: huellas de modelos
(sin cargarlos ni ajustarlos), CSV y configuración/entorno;33 filas/validación, llaves
únicas, observados contra panel, anterioridad y años exactos; medias/varianzas/escalas
solo entrenamiento;500 puntuaciones internas recálculo y selección global/por especificación
según bandas congeladas. Verifica orden del ledger, roles y vínculo selección−externo
por SHA256. Fecha registrada y código congelado apoyan secuencia, pero la huella sola
no certifica una cronología física externa. Diez repeticiones históricas cotejadas
nuevamente desde CSV: diferencia máxima0. No nuevas repeticiones de entrenamiento.

1500 internos+42 externos+10 repeticiones, cero fallos;49.500 internas, nueve procedimientos
con165 externas cada uno. Consumo histórico verificado1540.906905419055 de7200s;
esta fase añade0 ajustes y no consume saldo. Enmiendas E3-01(regex temporal completa)
y E3-02(cota descriptiva1555) conservadas; no cambios a100 candidatos ni presupuesto.
Evidencia de recálculo actual: resultados/verificacion.json, distinta de ejecución fase3.

## Notebook entregado y reproducción voluntaria

notebooks/01_notebook_personal.ipynb desde fuentes/01_notebook_personal.py y generador
Python/nbformat. **5 celdas de código ejecutadas realmente en modo verificar
mediante Python exec**, con3 gráficos incrustados; sin kernel Jupyter ni entrenamiento.
Fuente/huellas y modo documentados en resultados/verificacion_notebook.json. Recalcula
controles/tablas/gráficos en resultados/notebook_verificacion, separado de fase3.

El modo opcional lanza fuentes/reejecutar.py en un subproceso y reutiliza Runner/presupuesto/
construcción/selección compartidos, configuración congelada y semilla fija. Guarda piloto
nuevo en fase4/reproducciones/ con nombre único y ledger propio, máximo7200s para todo
el piloto nuevo. Estimación observada~25.7min, sin garantía en otro equipo. No reutiliza
modelos ni reinicia el ledger original; los resultados nuevos se verifican por separado.
Esta capacidad se inspeccionó/compiló; **no se ejecutó un reentrenamiento completo**.
Ante fallo/interrupción conservar estado/ledger; no afirmar éxito ni reanudar borrándolos.
No se ajusta modelo final con todos los años ni se genera simulación.

## Impacto, alternativas y límites

La mejora conjunta habilita entrega; alternativa resuelta: conservar global predefinido
sin seleccionar ambas retrospectivamente. Ocho territorios y61 pares con deterioro
impiden afirmar beneficio uniforme; alternativa resuelta: tablas completas y gráficos,
sin modificar población, ponderación, variables, criterio ni exclusiones.

Persisten casos completos/Guainía(238 frente404, diferencia descriptiva21.012106 puntos:
fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local sin autenticación
independiente, comparabilidad IPM(protocolo congelado§8), población hogares versus alumnos,
residencia versus colegio/enlace ecológico, dependencia temporal/territorial y pocos años.
Son advertencias activas; no efectos causales ni sesgos causalmente cuantificados.
Antecedentes59/esquema82, causa antigua20212 y fórmula global desconocida siguen archivados
con evidencia/motivo heredados, sin nueva evidencia de impacto ni reapertura.

No quedan controles indispensables pendientes de fase4. Reejecución voluntaria no realizada
es una opción del notebook, no prueba pendiente para cerrar esta revisión. Nueva fase,
simulación/objetivo4, ajuste final, descargas o push requieren autorización posterior.
Cierre: resultados/manifiesto_cierre.json y conservación; commit local descriptivo
identificado fuera del manifiesto para evitar autorreferencia.
