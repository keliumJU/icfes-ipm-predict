# Plan aprobado v4 — correcciones de persistencia y nuevas representaciones temporales

Fecha cliente: 2026-10-10, America/Bogota. Estado: **preparación documental;
investigación no iniciada**. Este plan aprobado no es un protocolo congelado ni
una autorización actual para ejecutar etapas. Solo se guardan los cuatro documentos
de preparación y un commit documental local, sin push.

En este documento v2/v3/v4 abrevian las carpetas experimentos_objetivo3_v2/
experimentos_objetivo3_v3/experimentos_objetivo3_v4, respectivamente.

## 1. Objetivo, partida, conservación y antecedentes

Explorar una mejora exacta del MAE global de al menos5% frente a persistencia/v3,
sobre las mismas165 externas:33 territorios×2021–2025. Mantener estimación
contemporánea territorial. No prometer mejora ni presentar evaluación conocida como
confirmación independiente. Cualquier confirmación necesitará datos aún no examinados.

Partida documental comprobada:15dcf122897d16bfde0e50da316d8f6c6dffdfd4,
rama codex/objetivo3-v3-historial, Git limpio. Es complemento del cierre real v3
6a10eef06f26189298b65edd1aa61f29afcb7f68. No inventar commit de cierre nuevo.
La rama de investigación codex/objetivo3-v4-correcciones se creará/verificará únicamente
en la siguiente sesión desde la partida real, que puede incluir este commit documental.
Conservar cualquier trabajo nuevo y explicar diferencias antes de reutilizar una rama.

Escrituras exclusivamente experimentos_objetivo3_v4/. Originales/v1/v2/v3, sus
continuidades, protocolos, modelos, ledgers, .gitignore y atributos previos intactos.
Sin fuentes adicionales, descargas, instalaciones automáticas, censo raw ni extracción/
sensibilidad2020. No simulación, objetivo4, ajuste final ni push. Etapa3v3 permanece
pendiente: el diagnóstico preparatorio v4 no la ejecuta/cierra ni entrega notebook personal.

Único panel fuente: experimentos_objetivo3_v2/fase1/reconstrucciones/
base_analitica_departamento_anio_v2.csv, SHA256
6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
Derivado antecedente: experimentos_objetivo3_v3/etapa1/reconstrucciones/panel_historial.csv.
Código/huellas/lock antecedente: v3/etapa1 y v3/etapa2, funciones v2 en lectura.
Continuidades v2/v3, v3/etapa2/INFORME_PILOTO.md y meta.json/verificacion.json
dentro de v3/etapa2/resultados/ son antecedentes verificables. Usar huellas/manifiestos correspondientes; no ejecutar
cierres/congelaciones/verificaciones que escriban antecedentes.

Referencia histórica v3: MAE3.429267191379531, RMSE4.3149206473689041,
sesgo pred−observado−2.0960105973100562; global/especificaciones eligieron persistencia.
2022 deterioró MAE frentev2. Ubicación: v3/etapa2/resultados/metricas.csv,
ganadores.csv/meta.json y selecciones en piloto/. No se recalculan errores ahora.
El valor documental no sustituye el recálculo futuro desde CSV con165 llaves/observados,
denominador positivo/finito y referencia íntegra. No probar la meta sobre un subconjunto.

## 2. Decisiones metodológicas aprobadas

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

Exactamente29 configuraciones; este documento define la grilla, NO la genera/congela.
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

## 3. Etapa1 — diagnóstico, diseño, congelación y controles (solo nueva sesión)

Leer AGENTS y continuidadesv2/v3/v4 vigentes primero; de este plan únicamente §§1–2
y §3. Verificar Git real/ascendencia/diferencias y manifiestos/conservación de antecedentes
en lectura. Crear/verificar rama v4 desde partida real conservando documentación/trabajo.
Comprobar entorno exacto, paquetes y pip check; no asumir entorno /tmp disponible.

Diagnóstico descriptivo desde prediccionesv3 guardadas: conjunto/años/territorios/
cortes2021–2024 y2025, errores firmados/absolutos/cuadráticos, sesgo y todos deterioros
frente referencias guardadas. Cotejar llaves/observados/huellas primero. No nuevos ajustes,
ni estimar correcciones reales, ni puntuación de candidatos v4. El diagnóstico no cambia
grilla/ventanas/filtros ni permite correcciones retrospectivas. Contradicción material
irresoluble se consulta antes de actuar; hallazgos/impacto/alternativa/resolución registrados.
Este diagnóstico v4 no modifica/cierra etapa3v3 ni entrega notebook personal.

Crear protocolo4.0.0 con estas decisiones; derivado separado con llaves previas/
diferencias y grilla29/defaults; funciones comunes/adaptadores v4 en lectura de módulos
anteriores. Evidencias reales limitadas a estructura/integridad/trazabilidad y diagnóstico
histórico guardado. No estimadores ajustados en panel, correcciones reales ni ledger operativo.

Sintéticos/dobles separados: aislamiento territorial/anterioridad/salto/futuro,
198 cambios y matrices1/2/2/16/17; mediana entrenada solo en pasado/λ exactos/n par;
reconstrucción y métricas independientes; persistencia sin fit; escaladores solo train;
bandas/grupos/IDs distintos/ineligibles; presupuesto serial/reanudación/intentos/caída/
fallos/límite/terminación; tolerancias/regex/huellas/rutas. Ajustar sintéticos no cuenta
como consumo del panel; no atribuir esos resultados a modelos reales.

Notebook útil de diagnóstico/controles generado desde Python editable y generador Python
que valida .ipynb. Reutilizar lógica/parámetros; guardar solo salidas de celdas realmente
ejecutadas, orden/entradas/salidas/versiones/semilla. No notebook de modelos/personal/
simulación. Congelar fuentes/datos/grilla/defaults/entorno/referencias/controles antes
de cualquier fit real futuro; etapa2 congelará su orquestación propia antes del primer fit.
Cerrar etapa1 con informe, README, registro, verificación/conservación/manifiesto,
continuidadv4 y commit local solo v4, sin push. Guardar prompt exclusivo etapa2, no ejecutarlo.

## 4. Etapa2 — orquestación y piloto29 (autorización posterior separada)

Leer continuidad y únicamente §§1–2/§4; verificar cierre/entorno/controles. Implementar,
probar con dobles, congelar orquestación y ejecutar ventanas seriales bajo protocolo4.0.0.
Guardar datos/entradas/transformaciones/parámetros/versiones/advertencias/huellas/modelos/
predicciones/selecciones antes externo/repeticiones/ledger. Verificar cobertura completa,
referencias, selección interna y cinco comprobaciones. Informe aunque no mejore; sin
notebook personal ni entrenamiento final. Conservar incompleto si faltan resultados.
Cerrar únicamente etapa2 con continuidad/control/conservación/manifiesto/commit local;
prompt exclusivo etapa3 guardado, no avanzar automáticamente.

## 5. Etapa3 — revisión y entrega (autorización posterior separada)

Leer continuidad y únicamente §§1–2/§5; revisión desde artefactos guardados, cero ajustes.
Resultados conjuntos/anuales/territoriales/cortes2021–2024vs2025, diferencias firmadas/
absolutas/cuadráticas y todos deterioros con unidades/denominadores explícitos.
Notebook personal solo con meta global≥5% verificada; informe completo aun sin mejora.
Fuentes/generador Python para notebook, salidas realmente ejecutadas. Cerrar etapa3
sin simulación/objetivo4/ajuste final/push ni nueva fase automática.

## 6. Advertencias y tratamiento de hallazgos

2021–2025 ya examinados: exploratorio, sin confirmación independiente/causalidad ni
pronóstico anticipado demostrado. IPM contemporáneo; persistencia usa previo pero
no se auditó disponibilidad operacional por fecha. Cambio entre observaciones no es
cambio anual en el salto2019→2021. No interpretar escenarios como efectos causales.
Mantener casos completos/Guainía238vs404 y21.012106 puntos (v2/fase1/resultados/
diagnostico_medias_disponibles.csv), procedencia local, comparabilidad IPM, hogares/
alumnos, residencia/colegio/enlace ecológico y dependencia territorial/temporal/pocos años.
Antecedentes59/esquema82/causa antigua20212/fórmula global desconocida siguen archivados
con evidencia/motivo heredados; no reabrir sin nueva conexión pertinente.
Cada hallazgo relevante: ubicación verificable, impacto, alternativa lógica y resolución
si no cambia objetivos/criterios. Cambios materiales se justifican/consultan antes de
observar evaluación nueva; no cambiar criterios para mejores métricas. PDF únicamente
si necesarios, por secciones/páginas, distinguiendo lectura actual de histórica.
