# Informe etapa1 v4 — diagnóstico histórico y diseño congelado

Solo etapa1, sin piloto, fecha cliente2026-10-10. Entregables verificables en README y
resultados/manifiesto_cierre.json; controles estructurales propios no inferidos de preparación.
Git46193a5 descendiente15dcf122, diferencias solo cuatro documentos previos v4; rama nueva
creada sin reset. Preparación: tres huellas y15349 archivos snapshot iguales, registro
cotejado byte a byte en Git, sin autorreferencia JSON. Evidencia: partida.json/
integridad_antecedentes.json/conservacion_final.json y REGISTRO_PREPARACION.json.

Reproducción actual limitada a cálculos de CSV históricos guardados, no reproducción de
entrenamientos. v3/global igual a persistencia en165 llaves/observados, selección enlazada
por año. Referencias v1/v2/media/tresOLS conservadas; ningún modelo comparador cargado.
MAE histórico declarado3.429267191379531, recálculo independiente idéntico. No métrica,
predicción ni meta v4 nueva. Denominador histórico positivo/finito; futura meta deberá
recalcularse otra vez en165 externas completas antes de juzgar≥5%, sin redondeo.

Métricas completas (puntos; CSV fuente resultados/metricas_historicas.csv):

```csv
referencia,ambito,periodo,n,mae,rmse,sesgo
v3,conjunto,2021–2025,165,3.4292671913795312,4.3149206473689041,-2.0960105973100562
v3,corte,2021–2024,132,3.7249352319645874,4.5679220984006141,-2.2462801576587266
v3,corte,2025,33,2.2465950290393066,3.1030713458162262,-1.4949323559153742
v3,anio,2021,33,2.6402236932057406,3.5097490978755155,1.4070902157455416
v3,anio,2022,33,5.0919663135676627,5.5535200553456816,-4.5062328935485283
v3,anio,2023,33,3.2072717302598033,4.0108355970044807,-2.2509155346565688
v3,anio,2024,33,3.9602791908251427,4.921069321485291,-3.6350624181753499
v3,anio,2025,33,2.2465950290393066,3.1030713458162262,-1.4949323559153742
v2,conjunto,2021–2025,165,4.8795571881610309,6.194961008561882,-0.97586426860308273
v2,corte,2021–2024,132,4.8453729996839057,6.110623990266836,-0.39729724869510707
v2,corte,2025,33,5.0162939420695309,6.5214114489358757,-3.2901323482349851
v2,anio,2021,33,5.859134383253795,7.0388982820580033,4.8049656714304643
v2,anio,2022,33,3.8718846703591603,5.1025818628272699,-1.0512978597889484
v2,anio,2023,33,3.7435935263623121,4.634708525272158,-1.7721816212855557
v2,anio,2024,33,5.9068794187603553,7.2315937659312013,-3.5706751851363885
v2,anio,2025,33,5.0162939420695309,6.5214114489358757,-3.2901323482349851
```

2022: el sesgo persistencia−observado es−4.506233 puntos y MAE5.091966 frente
v2=3.871885. Como persistencia copia el observado previo, su sesgo negativo describe
un global actual medio mayor que el previo. Es una identidad descriptiva del CSV,
no explicación causal del cambio ni evidencia de ajuste incremental de IPM.
En2021 el sesgo tiene signo positivo; corrección común futura podría cambiar dirección
según train. No se calcula ni aplica ninguna corrección real ahora.
El sesgo conjunto−2.096011 tiene mayor magnitud quev2−0.975864 pese al menor MAE:
las métricas describen propiedades distintas; conservar ambos sin sustituir el criterio.

Deterioros MAE frentev2:2022, territorios13/20/41/76/95 y66 pares. Todos guardados,
incluidos deterioros RMSE/agregados contra cada comparador y cada corte territorial.
Resultados/diferencias_emparejadas.csv usa delta=v3−referencia; positivo en pérdida
absoluta significa deterioro. Delta cuadrático en puntos² no es diferencia de RMSE.
Datos completos no seleccionados retrospectivamente por error.

Estructura real:231 filas,198 cambios completos en16 covariables,33 territorios,
165 externas,2021 previo2019/intervalo2;2018 solo historial. Cinco matrices1/2/2/16/17.
Resultados/estructura_real.json/trazabilidad_198.csv y preparar.historial/cotejo fuente.
Grilla exactamente29:1+3+15+10; parámetros/defaults/versiones/semilla registrados.
Medianas/correcciones solo sintéticas. Cota futura308 sin fallos,280+24+4; no saldo v3.

Siete grupos sintéticos aprobados; controles.json conserva detalles por prueba,
reanudación e intentos con ledgers de prueba, proceso realmente terminado por límite.
Tres celdas notebook ejecutadas, salidas reales/nbformat validado; no kernel Jupyter.
Congelación cubre fuentes propias/reutilizadas, parámetros, panel, entorno/lock,
referencias/selecciones y controles antes de futuro fit. Etapa2 congelará nuevo motor.
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

Pendientes de etapa1: ninguno indispensable tras verificación de cierre. Pendiente futuro:
autorización etapa2/piloto, notebook personal/fases posteriores requieren autorización propia.
No etapa3v3, simulación, objetivo4, entrenamiento final, descargas, instalaciones ni push.
