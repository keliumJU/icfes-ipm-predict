# Protocolo4.0.0 — correcciones de persistencia

Fecha cliente2026-10-10, America/Bogota. Solo etapa1 autorizada. Decisiones del usuario
fijadas antes del diagnóstico; ninguna modificación por errores históricos.
Partida real46193a5a97962abaef39c2c30e599a347731e45f, descendiente15dcf122,
rama codex/objetivo3-v4-correcciones. Evidencia: resultados/partida.json.

## Fuente y conservación

Único panel v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv,
SHA2566cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
231 filas,33 territorios×7años. Original conservado; reconstrucciones/panel_cambios.csv
separado con columnas originales, llave previa, intervalo y16 covariables previas/diferencias.
198 cambios completos comprobados contra misma llave fuente; resultados/trazabilidad_198.csv.
Derivado antecedente v3 cotejado por manifiesto y valores de previo/objetivo.
Conteos, intervalo, códigos, año y otras pruebas son trazabilidad, nunca predictores.
Escrituras exclusivamente v4; antecedentes/modelos/ledgers/continuidades intactos.

## Decisiones normativas del usuario


### Población, historial y objetivo

Conservar ESTUDIANTE/no libertad S/grado11/seis puntajes positivos y presentes/sin
calendario; media global recibida, geografía colegio y peso igual territorio-año.
Conteos solo trazabilidad. Ningún cambio de población para mejorar métricas.
2020 excluido definitivamente. Años autorizados2018/2019/2021/2022/2023/2024/2025.
Previo del máximo año autorizado estrictamente anterior del mismo territorio;2021
previo2019. Sin fabricar2020 ni anualizar/dividir por duración del intervalo.
2018 exclusivamente historial, nunca objetivo de cambio. Cambio observado=global−previo.
Modelos ajustables aprenden cambio; predicción final=previo+cambio predicho.
Selección y métricas sobre puntaje global original, no R² del cambio.

Persistencia predice previo sin fit. Corrección común predice previo+λ×mediana de los
cambios observados de TODAS las filas de entrenamiento autorizado, con igual peso
territorio-año. La mediana para n par es el promedio de los dos valores centrales.
No estimar corrección con internos/externos que se están prediciendo ni corregir
retrospectivamente errores guardados. λ fijo, no estimado. Se estima una estadística
real del objetivo: su ajuste consume presupuesto, sin fingir que es persistencia.

Cada cambio de covariable es actual−valor de la MISMA llave previa que origina el
puntaje previo, orden original de columnas. IPM/tasas actuales y previas tienen
trazabilidad por territorio/año. No anualizar el salto2019→2021. Datos de2018 sirven
para diferencias de2019. La inspección estructural previa en la conversación encontró
198 filas con diferencias disponibles para las16 covariables; etapa1 debe comprobarlo
y guardar evidencia propia, no asumirlo como control v4 ya aprobado.

Cinco grupos congelados, en orden:

|Grupo|Entradas en orden|Número|
|---|---|---|
|historico|puntaje_previo|1|
|nivel_ipm|puntaje_previo, ipm actual|2|
|cambio_ipm|puntaje_previo, cambio ipm|2|
|cambio_tasas|puntaje_previo, cambios de las15 tasas en orden original|16|
|cambio_ambas|puntaje_previo, cambio ipm, cambios de las15 tasas|17|

Sin año/intervalo/código/nombre/conteos/otras pruebas como predictores, efectos
territoriales, ponderación estudiantil, selección nueva de variables, PCA, imputación
ni clipping. Los cambios negativos son válidos; no aplicarles controles de positividad
propios del puntaje o de niveles. Mismo objetivo contemporáneo, no pronóstico anticipado.

### Grilla prospectiva y parámetros

Exactamente29 configuraciones materializadas en resultados/configuraciones_congeladas.json.
Orden JSON futuro: persistencia; tres correcciones conλ0.25/0.5/1; Ridge por grupo
(en orden anterior) y dentroα1/10/100; Huber por grupo y dentroα0.01/1.
Persistencia y correcciones comunes no pertenecen a un grupo exclusivo: participan
en selección global y en los cinco grupos. No rellenar una grilla100 ni añadir familias.

Ridge15: StandardScaler+Ridge, solver='svd', mismos parámetros/defaults congelados
anteriormente salvoα. Huber10: StandardScaler+HuberRegressor, epsilon=1.35,
fit_intercept=True,max_iter=2000,tol=1e-5,warm_start=False,α0.01/1.
Guardar nombres/defaults completos con get_params(deep=True), versiones y semilla20261010.
El constructor de Ridge debe reutilizarse en lectura; solo nueva familia/corrección
en adaptador común v4, sin duplicar lógica por grupo. Métricas, bandas y presupuesto
compartidos se reutilizan con destinos exclusivamente v4 y orden propio aislado.

Entorno de referencia Python3.12.14/sklearn1.9.1 y lock exacto v3/etapa1/
requirements.lock.txt. Huber estaba disponible en la inspección previa; entorno transitorio
/tmp/icfes-v2-fase2-venv/bin/python. Cada sesión comprueba disponibilidad, cada paquete
exacto y pip check antes de usarlo. Si falta o difiere: documentar/consultar; no instalar.
Transformaciones ajustadas únicamente dentro del entrenamiento y del proceso presupuestado.
Sin estandarizar el objetivo, buscar semillas ni modificar hiperparámetros tras diagnósticos.

### Ventanas, selección y evaluación

|Externo|Objetivos anteriores para ajuste externo|Validaciones internas|
|---|---|---|
|2021|2019 disponible, sin ajustar candidatos; persistencia fija|ninguna|
|2022|2019,2021|2021|
|2023|2019,2021,2022|2021,2022|
|2024|2019,2021,2022,2023|2021,2022,2023|
|2025|2019,2021,2022,2023,2024|2021,2022,2023,2024|

Cada interna entrena todos los cambios estrictamente anteriores desde2019.
No validación2019 ni candidatos ajustados/puntuados/seleccionados en2021.
No reutilizar internos entre ventanas externas. Elegible desde2022 solo con todas las
internas exigidas, predicciones finitas y convergencia; registrar también inelegibles.
Errores internos concatenados con peso igual. Banda MAE≤mínimo+0.1; dentro RMSE≤mínimo+0.1;
menos entradas ajustadas; orden persistencia/correccion_comun/ridge/huber; orden JSON.
Persistencia y corrección común cuentan0 covariables ajustadas para desempate; ambas
usan previo, y la corrección estima una estadística del objetivo. Ridge/Huber1/2/2/16/17.

Guardar selección global y por cinco grupos antes del externo. Nunca asumir que global
coincide con ganador de su grupo; deduplicar únicamente ID igual dentro de una ventana.
Guardar global, cinco grupos y persistencia: cada procedimiento165 externas completas.
Comparadoresv1/v2/v3 y media/tresOLS exclusivamente CSV históricos guardados con
huellas/selecciones/llaves/observados cotejados; no búsquedas, ajustes ni cargar modelos
comparadores. Persistencia recalculada independientemente sin fit para cotejarv3.
Meta exacta100×(MAE_persistencia/v3−MAE_v4_global)/MAE_persistencia/v3≥5%, completo,
165 filas idénticas, denominador positivo/finito. Sin redondeo extra, tres-de-cinco,
significancia nueva ni sustituir global por un grupo mejor en externos.

### Presupuesto, fallos y reproducibilidad futuros

7200s acumulados propios para todos los ajustes, transformaciones/spawn/comunicación,
fallos/reintentos/repeticiones; serial y terminable. Ledger persistente v4 jamás reiniciado
ni ampliado, sin tomar saldo remanente v3 ni tocar ledgers/modelos previos. Persistencia
sin fit ficticio y duración separada; corrección común sí presupuestada en proceso.
Caída pendiente no medida agota conservadoramente. Reanudación verifica huellas y
cuenta intentos anteriores. Numérico/convergencia: inelegible. Infraestructura: máximo
un reintento, ambos cargados; persistente detiene. Integridad/cobertura/persistencia
faltante/límite: detener y conservar parciales/incompleto; no meta sobre subconjunto.

Orden: externos crecientes, candidatos JSON, internas crecientes, selección persistida,
IDs externos por JSON, cinco comprobaciones globales una/año. Persistencia recalculada;
atol1e-10/rtol0. Cota SIN fallos/reintentos:28×(1+2+3+4)=280 internos; hasta6 IDs
ajustables externos (global+cinco grupos)×4años=24; hasta4 repeticiones ajustadas,
2021 sin fit:≤308. No deduplicar internos ni asumir coincidencia de ganadores.
E3-01 regex temporal completa yE3-02cota1555v2 son antecedentes resueltos; preservar
ubicación/motivo, no heredar subcadena _i ni cota1010v3/1555v2 como cota v4.


## Comprobaciones actuales e interfaces

Entorno realmente verificado: Python3.12.14/54 paquetes exactos/pip check; entorno.json
con defaults completos serializados en configuraciones_congeladas.json. Grilla29 generada,
no los100 candidatos v3. Ridge reutiliza constructor anterior en lectura; Huber y mediana
adaptados en comun_v4.py. construir no ajusta. matrices_entrenamiento valida entradas
congeladas; historial enlaza covariables a la misma llave previa. seleccionar reutiliza
bandas anteriores con orden propio; exige29 registros, persistencia completa, internas exactas.
IDs externos conserva seis roles y deduplica solo identidad, nunca pertenencia al grupo.
Presupuesto reutiliza motor serial/spawn en lectura, valida destino v4; ajuste_con_fallos
conserva intentos e inelegibilidad numérica al reanudar. Es una interfaz comprobada con
sintéticos, NO orquestación operativa. Etapa2 debe implementar/verificar cobertura,
artefactos/huellas y congelar su propia orquestación antes de fit, con otra autorización.

Controles exclusivamente inventados: resultados/sinteticos y notebook_sinteticos;
controles.py comprueba aislamiento/anterioridad/futuro/salto/diferencias, cinco matrices,
mediana/λ/n par, reconstrucción/métricas independientes/escaladores train, selección,
elegibilidad/IDs, presupuesto/reanudación/intentos/fallos/caída/límite y terminación real.
Notebook diagnóstico/controles desde01_diagnostico_controles.py y generador nbformat;
tres celdas realmente ejecutadas mediante Python exec, sin kernel, sin ajustes reales.
No notebook de modelos/personal/simulación ni ledger operativo.

Diagnóstico actual desde CSV históricos guardados, verificados primero por huella,
selección/llaves/observados y persistencia independiente. Métricas math.fsum y cotejo
con función común; conjunto/años/territorios/cortes y territorio por corte. Diferencias
firmadas/absolutas en puntos y cuadráticas en puntos²; deterioros completos en CSV.
No estimación de medianas reales, correcciones retrospectivas ni meta v4 evaluada.

## Límites y antecedentes

2021–2025 ya examinados: análisis exploratorio, sin confirmación independiente,
causalidad ni pronóstico anticipado demostrado. Casos completos/Guainía238 frente404
y21.012106 puntos: v2/fase1/resultados/diagnostico_medias_disponibles.csv.
Procedencia local no autenticada independientemente; comparabilidad IPM, hogares/alumnos,
geografía colegio/residencia/enlace ecológico, dependencia territorial/temporal y pocos años.
Antecedentes59/esquema82/causa20212/fórmula global desconocida archivados con evidencia
heredada: CONTINUIDAD_V2.md sección vigente “Hallazgos, límites y pendientes”,
CONTINUIDAD_V3.md sección vigente “Hallazgos, límites y pendientes”,
v2/fase4/registro_problemas.md. No nueva conexión: no se reabren.
E3-01 regex completa y E3-02 cota1555v2: v2/fase3/ENMIENDAS_TECNICAS.md;
se conserva el motivo histórico sin usarlo como cota v4. Ningún PDF leído ahora (0 páginas).
