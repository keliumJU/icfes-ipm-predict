# Nueva sesión — autorizar únicamente etapa1 v4, sin piloto

Continúa en `/home/kelium/Documents/espcarlos/icfes-predict-improved`.
Aquí v2/v3/v4 abrevian experimentos_objetivo3_v2/experimentos_objetivo3_v3/
experimentos_objetivo3_v4, respectivamente.
Este prompt GUARDADO no se ejecutó en la preparación documental. Autoriza únicamente
etapa1 de experimentos_objetivo3_v4: diagnóstico descriptivo histórico, diseño,
protocolo4.0.0, derivados, grilla, congelación y controles sintéticos/dobles.
No etapa2/piloto, nuevos fits/correcciones del panel, etapa3/notebook personal,
simulación, objetivo4, entrenamiento final, push, descargas ni instalaciones automáticas.

Lee primero AGENTS.md, continuidadesv2/v3 vigentes y CONTINUIDAD_V4.md. Del planv4
lee exclusivamente definiciones comunes §§1–2 y etapa1 (§3); límites heredados constan
en continuidadv4. Protocolo completo v3/etapa1/PROTOCOLO_V3.md, README/informe/controles/
congelación/manifiesto/conservación y resultados guardadosv3 en lectura. No ejecutar
cierres/congelaciones/verificaciones que escriban v1/v2/v3. `v3/etapa2/fuentes/cerrar.py
--verificar` es lectura; no ejecutar su modo cierre. No llamar scripts de piloto previos.

Comprueba Git real, estado/rama/ascendencia/cambios. Partida al preparar documentos:
15dcf122897d16bfde0e50da316d8f6c6dffdfd4, rama codex/objetivo3-v3-historial, Git limpio.
Puede existir commit documental posterior; buscar asunto
`documentar plan v4 y prompt de diseno sin piloto`, no inventar hash ni exigir HEAD
antiguo. Verificar REGISTRO_PREPARACION.json: huellas de tres documentos y conservación
snapshot anterior; su propia huella se verifica en Git, no autorreferencia JSON.
Crear/verificar codex/objetivo3-v4-correcciones desde partida real después de analizar
ascendencia/diferencias; conservar todo trabajo encontrado, no reset ni sobrescritura.
Todas las escrituras exclusivamente v4, incluidas continuidad, pruebas y notebooks.
Originales/v1/v2/v3, sus continuidades, .gitignore y atributos previos intactos.

Entorno exacto de referencia Python3.12.14/sklearn1.9.1 y todos los paquetes de
v3/etapa1/requirements.lock.txt. Comprobar cada paquete y pip check antes de asumir
existencia de /tmp/icfes-v2-fase2-venv/bin/python. Huber disponible en comprobación
histórica, no asumido ahora. Si falta o difiere, documentar/consultar; no instalar.
Usar PYTHONDONTWRITEBYTECODE=1, rutas de escritura limitadas a v4. Semilla20261010.

Único panel fuente v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv:
SHA2566cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
Derivado antecedente v3/etapa1/reconstrucciones/panel_historial.csv con huellas.
No raw ni fuentes adicionales. Conservar ESTUDIANTE/no libertad S/grado11/seis
puntajes positivos/presentes/sin calendario; media global recibida, geografía colegio,
peso igual territorio-año.2020 definitivamente excluido sin extracción/sensibilidad;
2018 exclusivamente historial; previo mismo territorio máximo autorizado anterior;
2021 previo2019 sin fabricar2020 ni anualizar. Código/año/intervalo/conteos/otras
pruebas no predictores; sin imputación/clipping/efectos territoriales/PCA ni nuevos filtros.

Objetivo v4: misma estimación contemporánea, modelos aprenden cambio=global−previo,
reconstruyen global; selección/métricas en puntaje original. Referencia principal
persistencia/v3, MAE histórico3.429267191379531 (v3/etapa2/resultados/meta.json).
Meta FUTURA: mejora exacta≥5% sobre165 externas completas2021–2025, denominador
positivo/finito recalculado desde CSV guardados, sin redondeo ni tres-de-cinco.
En esta etapa no hay resultados v4 ni se comprueba su meta. Referenciasv1/v2/v3/media/
tresOLS exclusivamente guardadas; verificar huellas/selecciones/llaves/observados,
no nuevos ajustes, búsquedas ni cargar modelos comparadores.

Grilla EXACTA29, en orden: persistencia1; corrección común3 conλ0.25/0.5/1;
Ridge15 (cinco grupos, dentroα1/10/100); Huber10 (cinco grupos, dentroα0.01/1).
Persistencia predice previo sin fit. Corrección común=previo+λ×mediana de cambios de
TODAS las filas de entrenamiento autorizado, igual peso territorio-año; n par media
de dos centrales; solo entrenamiento, estima una estadística y será presupuestada.
No estimar medianas/correcciones con datos reales en etapa1; únicamente sintéticos.

Cinco grupos, orden/número de entradas:
1.historico:puntaje_previo(1).
2.nivel_ipm:puntaje_previo+IPM actual(2).
3.cambio_ipm:puntaje_previo+cambio IPM(2).
4.cambio_tasas:puntaje_previo+cambios15tasas en orden original(16).
5.cambio_ambas:puntaje_previo+cambio IPM+cambios15tasas(17).
Cada diferencia=actual−valor de la MISMA llave previa del puntaje. No anualizar;
2018 aporta covariables para diferencia2019; comprobar198 filas completas y conservar
trazabilidad/evidencia. Cambios negativos válidos. Ridge solver='svd', parámetros/defaults
anteriores idénticos salvoα. Huber epsilon1.35/fit_interceptTrue/max_iter2000/tol1e-5/
warm_startFalse. StandardScaler dentro entrenamiento/proceso para ambos; guardar defaults
completos/versión/semilla, reutilizar funciones/modelos comunes sin lógica duplicada por grupo.

Ventanas FUTURAS, idénticas v3:2021 persistencia fija sin fit/métricas/selección modelos;
2022 internas2021;2023 internas2021/2022;2024 internas2021/2022/2023;
2025 internas2021/2022/2023/2024. Cada interna entrena cambios estrictamente anteriores
desde2019, no2018 objetivo ni validación2019. Externo entrena cambios anteriores
2019/2021/…según ventana.100candidatos v3 NO trasladados; v4 son29.
Selección interna completa: bandas MAE/RMSE0.1, menos entradas ajustadas, familias
persistencia/correccion_comun/ridge/huber, orden JSON. Persistencia/corrección0 covariables
ajustadas; ambas usan previo y la corrección estima estadística del objetivo. Guardar
global y cinco grupos, persistencia/correcciones comunes elegibles en todos. No asumir
global igual a ganador de su grupo; deduplicar únicamente ID externo igual por ventana.

Piloto FUTURO7200s acumulados propios, serial/terminable, Pipeline completo, arranque/
comunicación/fallos/repeticiones incluidos. Sin reiniciar/ampliar saldo ni usar remanente
v3; ledgers/modelos anteriores intactos. Persistencia duración aparte sin fit ficticio;
corrección común cuenta como ajuste real. Cota sin fallos/reintentos308=280internos
(28×10)+≤24externos(6roles×4años)+≤4repeticiones ajustadas. Cinco comprobaciones globales
una/año, persistencia recalculada, atol1e-10/rtol0. AntecedentesE3-01 regex temporal completa
/E3-02cota1555v2 preservados; no heredar subcadena _i ni cotas previas como v4.
Numérico/convergencia inelegible; infraestructura máximo un reintento presupuestado,
persistente detiene; caída pendiente no medida agota conservadoramente. Integridad/
cobertura/persistencia faltante/límite detienen, conservar incompleto sin meta parcial.

Diagnóstico actual SOLO desde CSV v3 guardados: conjunto/años/territorios/cortes
2021–2024vs2025, sesgo, diferencias firmadas/absolutas/cuadráticas y todos deterioros.
Verificar primero llaves/observados/huellas. Explicar2022 y sesgo sin atribuciones
causales. No cambiar grilla/criterios por ese diagnóstico ni corregir externos vistos.
Diagnóstico v4 no ejecuta/cierra etapa3v3 ni entrega notebook personal. Hallazgos
relevantes: ubicación/impacto/alternativa/resolución; contradicción material irresoluble
exige consulta antes de actuar. Distinguir histórico, recálculo actual e hipótesis.

Crear únicamente etapa1: protocolo4.0.0, derivado separado, grilla29/defaults/entorno/
referencias, fuentes comunes/editables y controles. Sintéticos/dobles: anterioridad/
aislamiento/futuro/salto/diferencias; matrices1/2/2/16/17; mediana/λ/n par solo train;
reconstrucción/métricas independientes; escalado sin fuga; selección/grupos/elegibilidad/
IDs distintos; presupuesto/reanudación/intentos/fallos/caída/límite/terminación real;
repetición/regex/huellas/rutas. No ajustar datos reales ni crear ledger operativo.
Notebook útil diagnóstico/controles desde Python editable y generador Python que produce
/valida.ipynb; documentar orden/entradas/salidas/versiones/semilla, ejecutar celdas útiles
sin guardar salidas ficticias. No notebook de modelos/personal/simulación. Congelar
huellas antes de futuro primer fit; etapa2 congelará su nueva orquestación antes de fit.

2021–2025 ya examinados: exploratorio, sin confirmación independiente/causalidad ni
pronóstico anticipado demostrado. Mantener casos completos/Guainía238vs404 y21.012106
puntos (v2/fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local,
comparabilidad IPM, dependencia temporal/territorial/enlace ecológico. Antecedentes
59/esquema82/causa20212/fórmula global desconocida archivados con evidencia/motivo
heredados, no reabrir sin nueva conexión. PDF solo si necesarios, secciones/páginas,
ubicaciones y revisado/pendiente; no declarar lecturas históricas como actuales.

Cerrar únicamente etapa1 con entregables verificables, informe/README/registro de
hallazgos, conservación/manifiesto/congelación, continuidadv4 y commit local solo v4,
sin push. Guardar prompt exclusivo etapa2 para otra sesión, NO ejecutarlo automáticamente.
El piloto real, notebook personal, nuevas fases y entrenamiento final requieren otra
autorización; no utilizar esta autorización de controles como permiso de entrenamiento.
