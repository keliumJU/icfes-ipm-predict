# Informe de piloto etapa2 v4 — meta no satisfecha

Fecha cliente2026-10-10, America/Bogota. Autorización exclusivamente etapa2;
protocolo4.0.0 intacto. Resultado experimental exploratorio completo, no confirmación
independiente. Cierre verificable por controles/conservación/manifiesto y commit local.
No etapa3/notebook personal/simulación/objetivo4/ajuste final/descargas/instalaciones/push.

## Resultado principal y criterio conservado

MAE v4 global=3.6091786595605684; referencia principal persistencia/v3=
3.429267191379531. Ambos165 externas completas con mismas llaves/observados.
Referencia recalculada desde CSV guardados con math.fsum, positiva/finita e igual
al MAE histórico3.429267191379531. Persistencia recalculada independientemente,
idéntica a v3 guardado. Evidencia: resultados/meta.json/verificacion.json/metricas.csv,
predicciones_externas.csv; procedimiento verificar_extension.py → verificar.py.

Meta exacta100×(MAE_referencia−MAE_v4_global)/MAE_referencia =
**-5.246353175200156%**, inferior a5%; **no satisfecha**.
Es deterioro de MAE del5.246353175200156%, no mejora. Sin redondeo para decidir,
tres-de-cinco-años, nueva significancia, sustitución por un grupo o corrección
retrospectiva. El notebook útil de resultados se entrega; notebook personal no.
RMSE v4=np.float64(4.546778998773351); sesgo pred−observado=np.float64(-2.300737440412616);R² conjunto=np.float64(0.9315478399592954).
Métricas siempre sobre puntaje global reconstruido, no cambio aprendido.

## Ventanas y procedimientos

|Año|MAE v4 global|MAE persistencia|Ganador global|
|---|---|---|---|
|2021|2.6402236932057406|2.6402236932057406|persistencia|
|2022|5.991523654472851|5.0919663135676627|correccion_comun_00|
|2023|3.2072717302598033|3.2072717302598033|persistencia|
|2024|3.9602791908251427|3.9602791908251427|persistencia|
|2025|2.2465950290393066|2.2465950290393066|persistencia|

Global y cinco grupos eligieron correccion_comun_00(λ0.25) en2022 y persistencia
en2021/2023/2024/2025;2021 es fija sin seleccionar/puntuar candidatos.
Ganadores completos: resultados/ganadores.csv y piloto/seleccion_AAAA.json,
guardados antes del externo. Todos los grupos coinciden con global EN ESTA ejecución,
no supuesto del algoritmo. Persistencia mantiene su procedimiento independiente.
Los siete procedimientos tienen165 externas cada uno,1155 filas conjuntas.
Corrección2022 estimó mediana de TODAS las66 filas train2019/2021, sin usar2022;
ver entradas_entrenamiento.csv/ajuste.json bajo
piloto/ajustes/e2022_externo_correccion_comun_00. El signo de la corrección procede de
los cambios de entrenamiento; su error externo no autoriza modificarλ/mediana/criterios.

2022 aumenta MAE respecto a persistencia; los otros cuatro años son iguales a ella.
Impacto: la corrección seleccionada internamente no aporta beneficio externo y esta
grilla no logra la meta frente a la referencia principal. Alternativa verificable:
conservar procedimiento global realmente seleccionado, errores/ganadores/referencia
completos e informar el deterioro, sin rescatar retrospectivamente persistencia o un
modelo/grupo alternativo. Resolución aplicada: meta falsa/informe aunque no mejore;
revisión ulterior exige etapa3 autorizada. No atribuir contribución causal del IPM.

## Ejecución real y auditoría

Grilla29/defaults/grupos/orden idénticos etapa1:1persistencia sin fit,3correcciones
comunes,15Ridge,10Huber.280 internos independientes por ventana externa,1 externo
ajustado deduplicado y1 repetición ajustada: **282 ajustes/282 intentos**,
sin fallos, reintentos ni advertencias. Cota308 sin fallos respetada.
9570 predicciones internas guardadas(29×10×33).116 registros de selección interna,
29 por2022–2025,2021 sin métricas/selección candidatos. Persistencia cuenta0
covariables ajustadas; corrección cuenta0 pero su estadística sí es fit presupuestado.
Ridge/Huber matrices1/2/2/16/17 y scaler solo train; objetivo cambio, sin clipping,
imputación,PCA,efectos territoriales ni nuevos filtros.

Ledger propio acumulado: **259.8488030679364s/7200**;
saldo=6940.151196932064s. Persistencia cálculo aparte=
0.0003405500028748065s; cero fit ficticio. Invocación total piloto=
292.9112300589986s; incluye trabajo de artefactos/predicción
fuera del fit. Presupuesto incluye arranque/spawn/Pipeline completo en fit/mediana/
comunicación/fallos/reintentos/limpieza/repeticiones ajustadas. Sin tomar saldo v3,
reiniciar o ampliar. Ledger/resultados previos intactos.

Cinco comprobaciones globales, una por año:2022 repite corrección con nuevo fit,
cuatro persistencias recalculadas. Diferencia máxima0 puntos, atol1e-10/rtol0.
Evidencia: piloto/reproducibilidad.json, repeticiones/predicciones guardadas,
ledger e índice/contexto. Auditoría recorre todas las particiones/llaves/años/matrices/
parámetros/semilla/transformaciones/medianas/huellas/entradas/predicciones/selecciones,
orden exacto de ajustes e intentos; no carga modelos ni ajusta.282 modelos propios
validados por huella. Reanudación/contexto/intentos/fallos/presupuesto/caída/terminación
probados con inventados/dobles; fuentes finales ligadas a controles por SHA.

## Partida, fuentes, conservación y extensiones

Git real7f25ad066386965a75058e96b4716cdd8a9adb52 coincidió con cierre conocido
etapa1; rama codex/objetivo3-v4-correcciones limpia, sin trabajo posterior ni reset.
AGENTS y continuidades vigentes primero. Plan v4 exclusivamente §§1–2 y §4;
protocolo/README/informe/registro/grilla/defaults/controles/congelación/conservación/
manifiesto etapa1 revisados. Ningún PDF leído actualmente(0 páginas).

Python3.12.14/sklearn1.9.1/54 versiones exactas lock/pip check comprobados antes
usar entorno y durante auditoría; sin instalar/descargar. Fuente única v2/fase1/
reconstrucciones/base_analitica_departamento_anio_v2.csv SHA256
6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
Derivado231filas/198cambios SHA256
aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc,
reconstruido en memoria/cotejado íntegramente sin reescribir etapa1. Trazabilidad16
covariables misma llave;2020 excluido definitivamente,2018 solo historial,
2021 previo2019/salto sin anualizar. Población y agregación acordadas intactas.

Comparadoresv1/v2/v3/media/tresOLS exclusivamente CSV históricos: huellas/selecciones/
llaves/observados comprobados, sin cargar modelos/buscar/ajustar. Recálculos actuales
no son reentrenamientos ni efectos causales. Valores íntegros en metricas.csv.
Fuentes comunes propias reutilizan en lectura los adaptadores/constructor/métricas/
bandas/Presupuesto previos. Orquestación nueva congelada ANTES del primer fit real;
fuentes/modelos originales no modificados. Todas las escrituras de artefactos v4;
conservación compara snapshot inicial salvo continuidad propia, cuyo antecedente
se conserva íntegro y se coteja con Git. Atributo binario nuevo solo etapa2.

Primera auditoría se detuvo por dtype de cero entero/flotante en CSV combinado,
externo2022/procedimiento persistencia. FE_DE_ERRATAS_E2_01.md corrige la mención
2021 del documento congelado; diagnóstico completo en diagnostico_tipos_csv.json.
**E2-01**, ENMIENDA_AUDITORIA_E2_01.md/verificar_extension.py: extensión independiente
congelada antes del primer cálculo de meta, sin tocar fuentes congeladas ni ajustar;
comparación exacta de valores/columnas/llaves permite solo inferencia distinta de
pandas. Pruebas rechazan perturbación1e-11 y llaves distintas; auditoría completa
aprobada y ledger intacto. Incidencia preservada en registro/resultado de extensión.
No modificación de tolerancias/criterios ni contradicción material irresoluble.

Notebook01_resultados_piloto.ipynb desde fuente editable01_resultados_piloto.py y
generador Python; nbformat valida, tres celdas pertinentes ejecutadas realmente por
Python exec, salidas del piloto guardado; sin kernel Jupyter ni nuevos ajustes.
Orden/entradas/salidas/entorno/semilla en README. No notebook personal o de modelos.

## Límites y pendientes

2021–2025 ya examinados: análisis exploratorio, sin confirmación independiente,
causalidad ni pronóstico anticipado demostrado. Casos completos/Guainía238vs404 y
21.012106puntos(v2/fase1/resultados/diagnostico_medias_disponibles.csv), procedencia
local no autenticada independientemente, comparabilidad IPM,hogares/alumnos,
residencia/colegio/enlace ecológico, dependencia territorial/temporal y pocos años.
Antecedentes59/esquema82/causa20212/fórmula global desconocida permanecen archivados
con evidencia/motivo heredados; no nueva conexión pertinente ni reapertura.
E3-01(regex temporal completa)/E3-02(cota1555v2) antecedentes, no cotas v4.

Sin controles indispensables pendientes tras cierre de etapa2. La meta no se
satisface y no se entrega notebook personal. Etapa3/revisión detallada requiere
otra sesión/autorización; prompt exclusivo guardado, NO ejecutado. No simulación,
objetivo4, entrenamiento final, instalaciones/descargas ni push.
