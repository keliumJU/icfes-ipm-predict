# Protocolo prospectivo v3.0.0 — historial territorial

Fecha cliente: 2026-10-10, America/Bogota. Etapa1 exclusivamente. Esta congelación
no autoriza ejecutar el piloto. Partida real `9df055a372b4a0550e6f2682d33acb66fe69babe`;
respecto de `cc21529532668a966d500e435dca65ef11db09a3` solo añade los cuatro
archivos de preparación v3. Rama nueva `codex/objetivo3-v3-historial` desde esa partida.
Diseño del usuario fijado antes de resultados v3; no decisiones metodológicas abiertas.
Fuentes verificables: PLAN_INVESTIGACION_V3.md §§1–3, prompt de etapa1,
configuraciones_congeladas.json y funciones de etapa1/fuentes.

## 1. Fuente, población y objetivo

Única fuente: experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv,
SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
231 registros agregados, 33 territorios por año: 2018/2019/2021/2022/2023/2024/2025.
Población ESTUDIANTE, no libertad S, grado11, seis puntajes presentes/positivos;
sin filtro calendario. Geografía del colegio; media global recibida sin recalcular
ni redondear; peso igual territorio-año. Conteos únicamente trazabilidad. Se conserva
la fuente byte a byte; derivado separado en reconstrucciones/panel_historial.csv.
2020 excluido definitivamente: sin extracción ni sensibilidad. No imputación.

Historial dentro del mismo territorio, ordenado por año autorizado: previo del máximo
año estrictamente anterior. `anio_previo` conserva la llave de procedencia;
`puntaje_previo` copia el observado fuente correspondiente. En2021 previo2019.
2018 conserva su observado pero tiene previo/cambio ausentes, nunca objetivo de ajuste.
198 cambios observables, 165 externas. Cambio = global actual menos previo; sin
anualizar ni fabricar2020. La normalización del código a dos dígitos solo afecta el
derivado, no originales. Todas las columnas originales se conservan como trazabilidad;
solo las entradas congeladas entran en matrices de modelos.

Persistencia predice el previo; ningún estimador ni ajuste ficticio. Registrar duración
de cálculo aparte. Modelos aprenden cambio; predicción final = previo + cambio estimado.
Métricas y selección sobre puntos reconstruidos del global original; no R² del cambio.
Sin clipping, variables nuevas, año/intervalo/código/conteos/otras pruebas Saber como
entradas, ponderación estudiantil ni ajuste final con todos los años.

## 2. Grilla, parámetros y entorno

100 configuraciones exactas: persistencia +99 no media del JSON v2. IDs `delta_`+IDv2;
correspondencia, parámetros explícitos/defaults completos, orden y nombres en
resultados/configuraciones_congeladas.json. Reutilizar `configuracion.construir` fase2v2
en lectura. Por especificación: OLS1/Ridge4/ElasticNet6/SVR6/GradientBoosting8/ExtraTrees8.
Entradas: previo seguido del orden original IPM/tasas/ambas; 2/16/17 entradas.
Persistencia usa un puntaje histórico y tiene cero entradas ajustadas para desempate.
Semilla20261010; Python3.12.14/sklearn1.9.1 y lock íntegro v2, realmente comprobados.
No instalación automática. Todas las versiones están en resultados/entorno.json.

OLS/Ridge/ElasticNet/SVR: Pipeline StandardScaler+modelo, ajuste exclusivamente dentro
de cada entrenamiento; árboles sin escalado. No transformar externamente antes del
presupuesto: el proceso presupuestado debe recibir el Pipeline completo. Parámetros
fijos/defaults idénticos a v2, sin buscar semillas ni cambiar criterios por métricas.

## 3. Ventanas y selección

| Externo | Objetivos de cambio anteriores | Internas |
|---|---|---|
|2021|2019 disponible, sin ajustar|ninguna; persistencia fija|
|2022|2019,2021|2021|
|2023|2019,2021,2022|2021,2022|
|2024|2019,2021,2022,2023|2021,2022,2023|
|2025|2019,2021,2022,2023,2024|2021,2022,2023,2024|

Cada interna entrena todos los cambios observables autorizados estrictamente anteriores,
empezando2019. No validación de modelos2019 ni candidatos puntuados para2021.
2018 aporta historial exclusivamente. Entrenamiento interno distinto de v2; cobertura
externa idéntica165. Entradas contemporáneas del año a predecir y resultados de años
anteriores disponibles por regla expansiva; ningún observado de la validación/externo
entra en ajuste ni selección de su ventana.

Desde2022 registrar100 candidatos, incluso inelegibles; solo candidatos con todas las
internas, convergencia y predicciones finitas pueden ganar. Concatenar internas con peso
igual. Banda MAE≤mínimo+0.1; dentro de ella banda RMSE≤mínimo+0.1; menos entradas ajustadas;
familia persistencia/OLS/Ridge/ElasticNet/SVR/GradientBoosting/ExtraTrees; orden JSON.
Persistencia común elegible en las tres especificaciones. Guardar ganador global y por
especificación antes del externo. No sustituir global retrospectivamente por otra
especificación. Implementación reutiliza algoritmo de bandas v2 con orden v3 mediante
adaptador aislado, sin alterar módulo anterior.

## 4. Presupuesto y cota futuros — no iniciado

7200s acumulados para todos los ajustes: transformaciones, arranque/comunicación, fallos
y repeticiones. Ledger propio persistente, serial y procesos terminables, no reinicio
para recuperar saldo ni cambios al ledger/modelos/saldo v2. Motor reutilizado
`comun.Presupuesto` fase2v2 con restricción de destino v3. El reloj incluye spawn,
fit, comunicaciones y terminación; predicción/persistencia y ejecución total se informan
aparte. Una caída con pendiente no medido agota conservadoramente el saldo; interrupción
medida conserva consumo. Fallo también consume. No aumentar límite al reanudar.

Orden futuro: externos crecientes; candidatos en orden JSON; internas crecientes;
selección persistida antes del externo; IDs externos distintos en orden JSON; cinco
comprobaciones del global, una por año. Persistencia no produce fit; repetición recalculada.
Tolerancia atol1e-10/rtol0. No heredar diez repeticiones v2. Registrar todos los fallos;
no omitir internas/externos ni comunicar procedimiento completo si faltan. Error de
infraestructura: como máximo una repetición, ambas cargadas al ledger; fallo numérico/
convergencia hace candidato inelegible. Agotamiento conserva incompleto, nunca reinicia.
La cota siguiente es sin fallos/reintentos; prevalece7200s.

Cálculo completo:99×(1+2+3+4)=990 internos. Desde2022 hay cuatro roles externos ajustables
(global y tres especificaciones), hasta4 IDs distintos por año:≤16. No asumir que global
coincide con ganador de su especificación; bandas se recalculan. Deduplicar solo IDs
iguales dentro de cada externo. Cuatro repeticiones globales pueden requerir ajuste;
la quinta,2021, es persistencia. Total≤990+16+4=1010; si gana persistencia disminuye.
Comparadores guardados no ajustan. E3-02 conserva1555 como antecedente v2, nunca cota v3.
E3-01 conserva regex temporal completa; no clasificar `_ipm` como interna por subcadena `_i`.
Procedimiento: preparar.py `count_internal/bound`, ventanas y grilla JSON.

## 5. Referencias, evaluación y meta futuras

Persistencia y predicciones GUARDADAS fase3v2: global, v1, media y tresOLS. Verificar
huellas, selección enlazada, idénticas llaves y observados; resultados/referencias_guardadas.json.
Ninguna búsqueda/ajuste nuevo de comparadoresv2. Denominador futuro recalculado desde
predicciones guardadas: positivo y finito; meta exacta100×(MAE_v2−MAE_v3)/MAE_v2≥5%
sobre165 filas y procedimiento completo. Sin redondeo extra ni tres-de-cinco-años.
Informe completo aunque no mejore; notebook personal posterior condicionado a meta.
No nuevo notebook de modelos/simulación en etapa1.

Revisión futura: conjunta, anual, territorial y cortes2021–2024/2025; diferencias
emparejadas firmadas/absolutas/cuadráticas, errores y deterioros completos. RMSE conjunto
sobre errores concatenados; R² sobre global original, no definido si variación cero.
No pruebas nuevas de significancia, selección retrospectiva, causalidad ni pronóstico
antes de publicarse IPM contemporáneo. 2021–2025 ya examinados: exploratorio, sin
confirmación independiente. Ninguna métrica real nueva calculada en esta etapa.

## 6. Controles, conservación y trazabilidad

Reales solo estructura/igualdad/trazabilidad. Sintéticos y dobles separados en
resultados/sinteticos y notebook_sinteticos. Único notebook de controles generado desde
Python editable, nbformat, tres celdas ejecutadas realmente con Python exec, sin kernel.
Matrices, objetivo/reconstrucción, lag, escalado, selección, métricas independientes,
persistencia/repetición, regex y presupuesto comprobados. Rutas de escritura resueltas
obligatoriamente dentro v3. Sin resultados personales.

Manifiestos fase2/3/4 cotejados; continuidad antigua verificada en sus commits0664ac/
b37a2f/cc21529, sin excepciones arbitrarias. Siete fuentes verificadas mediante SHA256,
sin censo raw. Snapshot de todos los versionados conserva fuera v3; planificación
previa intacta salvo continuidad propia que conserva texto documental como antecedente.
PDF leídos ahora: ninguno, cero páginas. No cierres/verificaciones que escriban v2.
Congelación incluye código reutilizado, datos, protocolo, grilla, entorno/lock/referencias
antes de cualquier fit real futuro. Etapa2 debe verificarla y congelar su nuevo motor
antes de iniciar; no editar silenciosamente archivos congelados.

Advertencias activas heredadas: casos completos/Guainía238 vs404 y diferencia21.012106
puntos (fase1v2/resultados/diagnostico_medias_disponibles.csv), procedencia local no
independientemente autenticada, comparabilidad IPM, hogares versus alumnos, residencia
versus colegio/enlace ecológico, dependencia temporal/territorial y pocos años.
Antecedentes59/esquema82, antigua causa20212 y fórmula global desconocida archivados
por ausencia de impacto actual, con evidencia/motivo en continuidadv2 y registros
históricos; no reabrir sin información pertinente. Sin nuevas afirmaciones causales.
