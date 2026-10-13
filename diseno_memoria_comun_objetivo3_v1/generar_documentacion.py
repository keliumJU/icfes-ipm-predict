"""Genera exclusivamente artefactos documentales fase1, sin fits ni notebooks.
Entradas: plan fase1, preflight/entorno/semántica y particiones históricas.
No es implementación experimental ni congelación. Salidas solo en esta carpeta.
"""
from pathlib import Path
import json
import hashlib

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
def read(p): return json.loads((OUT/p).read_text())
def dump(p,d): (OUT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def doc(p,s): (OUT/p).write_text(s.strip()+'\n')

def main():
    assert all(read(p)['aprobado'] for p in ['PREFLIGHT_FASE1.json','ENTORNO_FASE1.json','SEMANTICA_FASE1.json'])
    archive=OUT/'antecedentes_preparacion'; archive.mkdir(exist_ok=True)
    for name in ['CONTINUIDAD_DISENO.md','README.md']:
        target=archive/name
        if not target.exists(): target.write_bytes((OUT/name).read_bytes())
    conf=json.loads((ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json').read_text())
    defaults=read('ENTORNO_FASE1.json')['defaults']
    warnings=['Procedencia local no autenticada; huellas verifican identidad, no autenticidad oficial.','Guainía: 238 frente404 y diferencia21.012105832431985 puntos, antecedente histórico v2; no corregir media recibida.','IPM mide hogares, no alumnos; enlace ecológico.','Geografía del colegio, no residencia.','Agregación territorial no permite inferencia individual ni causal.','Dependencia temporal y territorial; pocos años; no tratar copias como años independientes.','Todos2021–2025 ya vistos: exploratorio sin confirmación independiente ni pronóstico anticipado demostrado.']
    candidates=[
        {'id':'persistencia','orden':0,'n_entradas_derivadas':0,'componentes':[],'cambio_predicho':'0'},
        {'id':'memoria','orden':1,'n_entradas_derivadas':1,'componentes':[{'nombre':'memoria','X':'d[j,previo(t)]','y':'d[j,t]','unidad':'territorio-año','filas_por_anio':33}],'cambio_predicho':'f_memoria(d[j,previo(t)])'},
        {'id':'comun','orden':2,'n_entradas_derivadas':1,'componentes':[{'nombre':'comun','X':'c[previo(t)]','y':'c[t]','unidad':'año','filas_por_anio':1}],'cambio_predicho':'f_comun(c[previo(t)])'},
        {'id':'comun_correccion','orden':3,'n_entradas_derivadas':2,'componentes':[{'nombre':'comun','X':'c[previo(t)]','y':'c[t]','unidad':'año','filas_por_anio':1},{'nombre':'correccion','X':'r[j,previo(t)]','y':'r[j,t]','unidad':'territorio-año','filas_por_anio':33}],'cambio_predicho':'f_comun_propio(c[previo(t)])+f_correccion(r[j,previo(t)])'}]
    spec={'version':'1.0.0','fecha_cliente':'2026-10-11','timezone':'America/Bogota','estado':'diseño documental fase1 completo; no congelación operativa','autorizacion_actual':'Solo fase1 enviada expresamente por usuario','fase2_autorizada':False,'fits_ejecutados':0,'modelos_cargados':0,'semilla':20261010,'entorno':{'python':'3.12.14','sklearn':'1.9.1','lock':'experimentos_objetivo3_v5/etapa1/requirements.lock.txt','paquetes':54,'PYTHONDONTWRITEBYTECODE':'1','pip_check_obligatorio':True,'falta_o_diferencia':'detener, documentar y consultar; no sustituir ni instalar'},'fuentes':read('PREFLIGHT_FASE1.json')['fuentes'],'poblacion_heredada':{'tipo':'ESTUDIANTE','no_libertad':'S','grado':11,'puntajes':'seis presentes y positivos','calendario':'sin filtro','media':'global recibida sin reconstruir promediando subpruebas','geografia':'colegio','agregacion':'media anual territorial recibida; conteos solo trazabilidad','verificacion_actual':'Cotejo íntegro fuente/derivado; no reauditoría de raw ni autenticación oficial'},'llaves':['codigo_departamento','anio'],'normalizacion_codigo':'texto zfill(2), contrato histórico; sin alterar bytes originales','anios':[2018,2019,2021,2022,2023,2024,2025],'definiciones':{'previo(t)':'máximo año disponible estrictamente anterior en panel permitido','d[j,t]':'prom_punt_global[j,t]-prom_punt_global[j,previo(t)]','c[t]':'mediana de33 d[j,t]; estadística auxiliar no media nacional ni objetivo nuevo','r[j,t]':'d[j,t]-c[t]','prediccion_puntaje':'puntaje_previo[j,t]+cambio_predicho[j,t]','intervalo':'t-previo(t), solo trazabilidad sin anualizar'},'historia':{'2018':'solo nivel inicial; sin d observado','2019':'d disponible, solo historial/entrada rezagada; no respuesta con lag inexistente','2020':'excluido sin imputar','pares_supervisados':'años completos de33 pares con respuesta y rezago observado, ambos estrictamente anteriores al evaluado','un_anio':'ajuste futuro permitido; comun1fila, territoriales33filas','cero_anios':'persistencia explícita para candidato completo, sin scaler ni regresor','incompleto_no_finito':'fallo de integridad, detener; no convertir ausencia inesperada en respaldo silencioso','externo2021':'persistencia fija para cuatro políticas y global, sin ajuste/puntuación/selección'},'candidatos':candidates,'pipeline_componentes':{'orden':['StandardScaler','QuantileRegressor'],'defaults_completos':defaults,'sample_weight':None,'recencia':False,'busquedas':False,'alpha':'1.0 fijo propuesto por plan; no optimizado','ajuste_scaler':'solo X entrenamiento del componente, nunca evaluación','modelo_comun':'una fila por año sin replicar33veces','correccion':'parámetros compartidos sin efectos por código','no_inputs':['año','código','intervalo','conteos','IPM','tasas','d evaluado','c evaluado','r evaluado'],'postproceso':'sin clipping, imputación, mezclas ni calibración'},'ventanas':conf['ventanas'],'anti_fuga':{'formacion':'materializar solo historia admisible antes de computar estadísticas; c/r del año evaluado no entran en fit ni predict','entradas_evaluadas':'d/c/r del máximo año previo; el resultado evaluado se lee solo después para puntuar','mutacion_futura':'fase2 debe probar que cambiar validación o años posteriores no altera matrices, estadísticas, scaler ni predicción','disponibilidad_real':'orden cronológico lógico; fechas de publicación no autenticadas, sin claim operativo'},'evaluacion':{'primario':'procedimiento de selección global predefinido','externos':[2021,2022,2023,2024,2025],'n':165,'peso':'igual territorio-año, sin conteos/pesos recencia','error':'prediccion-observado','MAE':'fsum(abs(error))/n','RMSE':'sqrt(fsum(error**2)/n)','meta':'100*(MAE_persistencia-MAE_global)/MAE_persistencia>=5','denominador':'positivo finito, mismas165llaves/observados','interpretacion':'exploratoria; políticas individuales solo diagnósticas'},'seleccion_documental_futura':{'externo2021':'fijo, sin selección','resto':'internas expansivas exactas; pool con cobertura íntegra y métricas finitas','pool1':'MAE <= minimo MAE +0.1','pool2':'sobre pool1, RMSE <= minimo RMSE +0.1','desempate':['n_entradas_derivadas','orden_candidato'],'inelegible':'fallo numérico o cobertura incompleta con razón; persistencia indispensable; no fabricar filas','sin_rescate':'no usar externas para seleccionar o redefinir primario'},'contrato_futuro_propuesto':{'autorizacion':'Cada fase requiere envío expreso de su prompt y anterior válida; ningún presupuesto iniciado','predicciones_internas_originales':1320,'registros_seleccion':16,'predicciones_externas':825,'internas_unicas_condicionadas':528,'dedup':'solo copias y contexto exactos con linaje y menor externo; no compartir fits entre ventanas ni candidatos','presupuesto_segundos':7200,'cota_componentes_sin_fallos':{'internos':24,'externos':16,'repeticiones_globales_max':6,'total':46},'unidad_fit':'scaler+regresor completo de un componente; respaldo/persistencia0','reuso_global':'solo mismo candidato y ventana externa; nunca entre candidatos o ventanas','fallos':'runner serial terminable, ledger persistente; máximo1retry infraestructura; numérico inelegible; caída sin tiempo medido agota saldo; repetición consume','audit_CSV':'exactitud numérica; int/float0 equivalente; rechazar1e-11','audit_repeticiones':'atol1e-10,rtol0'},'advertencias':warnings,'aprobaciones':{'usuario':'panel actual, ajuste estadístico desde1año, conservar objetivo/particiones/meta; envío actual autoriza diseño','nuevas_decisiones_documentales':'IDs/contrato serializado/fallos de integridad/cobertura de evidencia; sin afirmación de aprobación operativa','pendiente':'aprobación explícita del diseño y autorización fase2; implementación y controles válidos antes piloto'}}
    dump('ESPECIFICACION_DOCUMENTAL.json',spec)
    doc('PROTOCOLO_FASE1.md',r'''
# Protocolo documental — memoria temporal y componente común, v1.0.0

Fecha2026-10-11 America/Bogota. Fase1 autorizada por envío expreso del usuario. Diseño completo para revisión; no congelación operativa ni aprobación de fases futuras. Cero fits reales o inventados, notebooks, cargas de modelos, instalaciones, nuevas fuentes, commits o push.

## 1. Objetivo, población y evidencia

Comparar cuatro candidatos que predicen el cambio original del puntaje territorial y un procedimiento global que selecciona únicamente por internas. Primario: procedimiento global; meta original mejoraMAE≥5% respecto a persistencia sobre165pares,33territorios×2021–2025, igual peso territorio-año. MAE=fsum(|predicción−observado|)/n; RMSE=raíz(fsum(error²)/n). El denominador de mejora debe ser positivo finito. Políticas individuales no sustituyen el primario aunque alguna mejore.

Se hereda población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin filtro calendario; media global recibida, geografía del colegio, agregación anual territorial original. No ponderar evaluación por alumnos, hogares ni tamaño. Conteos solo trazabilidad. La sesión cotejó el panel completo, no reaudita raw ni autentica procedencia oficial. Fuente v2 y derivado v5 con huellas en PREFLIGHT_FASE1.json:fuentes. Procedimiento verificable en verificar_semantica.py y SEMANTICA_FASE1.json:231filas/33territorios/198cambios, todos los campos reconstruidos en memoria exactos. Código textual normalizado zfill(2) como historial anterior, sin alterar originales.

Referencias v5/global, v3/persistencia y recencia/global idénticas en165llaves/observados/predicción según SEMANTICA_FASE1.json:referencias. Resultado HISTÓRICO recencia/globalMAE3.429267191379531, mejora0%, meta no satisfecha: experimentos_temporales_objetivo3_v1/etapa2/resultados/meta.json. Aquí no se reprodujeron fits ni se calculó una métrica nueva. No contar estas referencias como tres evidencias independientes.

## 2. Definiciones y candidatos fijos

Sea previo(t) el máximo año disponible estrictamente anterior. d[j,t]=puntaje[j,t]−puntaje[j,previo(t)], sin anualizar; c[t]=mediana de los33 d[j,t]; r[j,t]=d[j,t]−c[t]. c es auxiliar territorial, no nueva media nacional ni reemplazo del objetivo. Puntaje predicho=previo+cambio predicho. 2021 tiene previo2019 e intervalo2; no inventar2020.

| Orden/ID | Entrada y respuesta de ajuste | Cambio predicho | Unidad/entradas |
|---|---|---|---|
|0 persistencia|sin ajuste|0|0entradas derivadas|
|1 memoria|d[j,previo(t)] → d[j,t]|f_memoria(d previo)|territorio-año,1entrada|
|2 comun|c[previo(t)] → c[t]|f_comun(c previo), igual para33territorios|año,1entrada|
|3 comun_correccion|c previo → c; r[j,previo(t)] → r[j,t]|f_comun_propio(c previo)+f_correccion(r previo)|año y territorio-año,2entradas totales|

Cada componente tiene su Pipeline propio StandardScaler(copy=True,with_mean=True,with_std=True) → QuantileRegressor(quantile=0.5,alpha=1.0,fit_intercept=True,solver="highs",solver_options=None). Defaults reales revalidados por get_params sin fit: ENTORNO_FASE1.json:defaults/firmas. No sample_weight ni recencia; sin búsquedas, clipping, imputación, mezcla ni calibración. Alpha1 es propuesta fija documental anterior a resultados nuevos, no valor optimizado. Scaler solo entrenamiento de su componente. No entradas de año/código/conteos/intervalo/IPM/tasas ni efectos territoriales individuales. Corrección comparte parámetros entre territorios. No compartir ajuste común entre candidatos2y3.

## 3. Historia y ausencia de pares

2018 proporciona nivel para d2019, pero carece de d2018. 2019 permanece historial/entrada; NO respuesta supervisada porque falta su cambio anterior. No imputar ese lag. Un año completo de pares requiere33territorios con respuesta y rezago finitos, en años anteriores al evaluado. Con cero años completos estructurales: candidato completo usa persistencia, deja razón explícita, cero scaler/fit. Con un año completo: ajuste futuro permitido; memoria/corrección33filas, común1fila. Con más años se usan todos los completos admisibles, sin recencia.

Con1fila el scaler común produce entrada centrada constante y el regresor aprende principalmente nivel/intercepto; regularización no aporta evidencia de dinámica identificada. Es fragilidad acordada, no motivo para aumentar mínimo o cambiar alpha después de observar desempeño. Faltas inesperadas, duplicados o no finitos son fallo de integridad: detener; no aprovechar respaldo para ocultarlos.

2021EXTERNO permanece fijo en persistencia para todas las políticas y global: sin ajuste, puntuación o selección interna. Las internas2021 dentro de externas2022–2025 sí son puntuadas en el piloto futuro, como respaldos idénticos sin ajuste. Distinción necesaria para preservar las diez internas originales.

## 4. Particiones y trazabilidad anterior a resultados

Ventanas heredadas exactas de experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json:ventanas, serializadas sin cambiar en ESPECIFICACION_DOCUMENTAL.json:ventanas. TRAZABILIDAD_TEMPORAL.csv enumera5externas+10internas, historia de cambios/respuestas supervisadas/rezagos/unidades/regla. No hay matrices entrenadas ni predicciones nuevas.

| Evaluado | Historia de cambios admisible | Respuestas con lag | Filas común / territoriales | Regla futura |
|---|---|---|---|---|
|2021|2019 en internas; externa fija|ninguna|0/0|persistencia|
|2022|2019,2021|2021←2019|1/33|ajuste permitido|
|2023|2019,2021,2022|2021,2022|2/66|ajuste permitido|
|2024|2019,2021,2022,2023|2021,2022,2023|3/99|ajuste permitido|
|2025|2019,2021,2022,2023,2024|2021–2024|4/132|ajuste permitido|

En externa2021 el entrenamiento declarado sigue vacío. En cada interna se usa su historia anterior, no toda la historia de su externa. La entrada de predicción usa d/c/r del previo al evaluado; c/r evaluados no entran en ninguna matriz ni cálculo de scaler. Calcular c de respuestas de entrenamiento solo sobre los33territorios correctos, una fila por año para común. Materializar historia permitida antes de computar estadísticas. Permutar objetivos de validación/futuro no debe alterar matrices, estadísticas o predicción; control pendiente de fase2, no afirmación de prueba realizada. El orden temporal lógico no autentica fechas de publicación ni prueba viabilidad de pronóstico anticipado.

## 5. Selección y ejecución futura — contrato documental propuesto

Solo internas expansivas originales, nunca externas. Cobertura completa y métricas finitas para elegibilidad. Filtrar MAE≤mínimoMAE+0.1; dentro de ese pool filtrar RMSE≤mínimoRMSE+0.1; desempatar por entradas derivadas0,1,1,2 y orden0,1,2,3. Persistencia indispensable. Numérico/convergencia implica inelegibilidad con razón; no fabricar métricas o cobertura. Sin política ganadora válida, cierre incompleto. 2022 necesariamente seleccionará persistencia si las cuatro copias de respaldo2021 son exactas; es implicación documental, pendiente del control, no selección ejecutada.

1320internas originales=4×(1+2+3+4)×33;16registros=4×4selecciones;825externas=(4políticas+global)×165. 528internas únicas=4×4años×33 solo si copias/contexto coinciden exactamente; conservar1320originales y linaje con menor externo representante, no tratar repetición como evidencia independiente. No reutilizar fits entre ventanas ni entre candidatos. Global reutiliza solo salida del MISMO candidato y ventana externa. Ajustar cuatro políticas externas predefinidas; ningún contraste externo permite rescate retrospectivo del primario.

Presupuesto propuesto NUEVO7200segundos, sin saldo ni ledger actual. Cota46componentes sin fallos:24internos (4componentes×[3validaciones2022+2validaciones2023+1validación2024]);16externos (4componentes×4externas); hasta6repeticiones globales (2022globalpersistencia, quedan3externas×máximo2componentes). Pipeline completo scaler+regresor cuenta1ajuste; persistencia/respaldo0. Registro persistente y runner serial terminable; máximo1retry de infraestructura, fallo numérico inelegible, caída sin tiempo medido agota saldo conservadoramente. Toda repetición consume presupuesto. Implementación/controles/congelación propios requieren fase2 autorizada; estos números no son resultados ni compromisos operativos aprobados.

Auditoría futura independiente de matrices, fechas, unidades, referencias, selección, presupuesto, cobertura y linaje. CSV comparación numérica exacta/intfloat0equivalente/rechazo1e-11; repetición ajustadaatol1e-10,rtol0. Meta recalculada sobre mismas165llaves/observados. Implementación no importa runners ni deserializa modelos históricos. Notebook de controles y resultados únicamente en fases autorizadas, desde fuentes Python editables y generador Python con validación, ejecuciones reales sin datos personales.

## 6. Hipótesis y advertencias preservadas

Memoria puede ayudar; común puede ayudar; corrección puede aportar respecto a común. Son hipótesis, no eficacia demostrada. Contrastes individuales son descriptivos exploratorios; global evalúa meta. Todos2021–2025 ya vistos: no confirmación independiente ni causalidad. Dependencia temporal-territorial y pocos años impiden interpretar165pares como165observaciones independientes de dinámica; común tiene solo1–4respuestas por ajuste.

Procedencia local no autenticada. Guainía238frente404/diferencia21.012105832431985puntos es antecedente histórico, evidencia v2/fase1/resultados/diagnostico_medias_disponibles.csv:filas57(periodo20252,código94)y90(anual2025,código94); no cambiar media recibida. IPMhogares frente alumnos y geografía colegio frente residencia, agregación ecológica sin inferencia individual. Nuevos modelos no contienen IPM, pero estas limitaciones siguen en el contexto de procedencia, no se presentan como efecto causal. Problemas archivados sin conexión actual no se reabren; las incidencias técnicas nuevas se registran separadas.

## 7. Aceptación y siguiente fase

Fase1 acepta integridad/Git/entorno/semántica/defaults/documentos/trazabilidad/prompts/conservación, según ACEPTACION_FASE1.json. No acepta controles ejecutables, fits, piloto ni congelación. Autorizar diseño documental no aprueba operativamente fases posteriores. Prompts2–4 independientes, condicionados y solo activos cuando usuario los envía expresamente. No avance automático. Pendientes: aprobación del diseño; implementación/controles; piloto; auditoría; confirmación científica independiente y disponibilidad real, fuera del alcance actual.
''')
    doc('DECISIONES_FASE1.md','''
# Decisiones, autoridad y límites

2026-10-11. Cada fila distingue autoridad de comprobación. No observar resultados nuevos de evaluación: fits0/métricas nuevas0.

|ID|Decisión|Procedencia/estado|Ubicación verificable|
|---|---|---|---|
|D01|Panel actual primero, sin fuentes extra|Usuario, confirmado antes de fase1|PLAN_FASES.md:Propósito y decisiones acordadas; antecedentes_preparacion/CONTINUIDAD_DISENO.md:Decisiones|
|D02|Ajuste desde1año completo; cero respaldo|Usuario y envío fase1; fragilidad aceptada para diseño, no prueba operativa|Prompt actual/PROMPT_FASE1_DISENO.md; protocolo§3|
|D03|Población/agregación/objetivo2021fijo/particiones165/meta5%/igualpeso|Usuario, conservado|protocolo§1,3,4; ESPECIFICACION_DOCUMENTAL.json:poblacion_heredada/evaluacion/ventanas|
|D04|d sin anualizar, c mediana33, r=d−c|Plan autorizado para formalizar documentalmente|PLAN_FASES.md:Fase1; protocolo§2|
|D05|4IDs y orden; entradas0/1/1/2|Formalización documental nueva del orden del plan|ESPECIFICACION_DOCUMENTAL.json:candidatos|
|D06|Scaler/Quantile0.5alpha1highs, sin recencia/búsqueda|Propuesta fija del plan formalizada; defaults comprobados, no optimización|ENTORNO_FASE1.json:defaults; protocolo§2|
|D07|2019sin respuesta supervisada; lag2019para2021|Regla enviada por usuario y comprobación de historia completa|SEMANTICA_FASE1.json; TRAZABILIDAD_TEMPORAL.csv|
|D08|Común1fila/año, territoriales33; parámetros corrección compartidos|Plan fase1; no efectos individuales|protocolo§2–4|
|D09|Falta inesperada/incompleto/no finito detiene, no respaldo silencioso|Decisión nueva de integridad coherente con cero pares estructurales; no cambia población|ESPECIFICACION_DOCUMENTAL.json:historia; control futuro fase2|
|D10|Reproducir todas columnas v5 y referencias exactas sin fits|Comprobación actual, no nueva métrica ni eficacia|verificar_semantica.py; SEMANTICA_FASE1.json|
|D11|Bandas0.1/globalprimario/desempates/cobertura/fallos|Contrato documental de fases futuras, propuesto para revisión; no congelado|protocolo§5; ESPECIFICACION_DOCUMENTAL.json:seleccion_documental_futura|
|D12|7200nuevo/cota46/1320/16/825/528condicional|Expectativas documentales; presupuesto no iniciado; no saldos heredados|protocolo§5, procedimiento de conteo explícito|
|D13|Todos2021–2025vistos, exploratorio/no causal|Estado histórico vigente preservado|Continuidad diagnóstico:Hallazgos; continuidad temporal cierre; protocolo§6|
|D14|Git/antecedentes intactos, excepción solo continuidad histórica real|Comprobación actual|PREFLIGHT_FASE1.json:git/manifiestos; CONSERVACION_FASE1.json|
|D15|No avance automático, aprobación/autorizar cada fase|Usuario actual; diseño no congelación|PROMPT_FASE2_IMPLEMENTACION.md/PROMPT_FASE3_PILOTO.md/PROMPT_FASE4_AUDITORIA.md|

No se atribuye aprobación posterior al usuario. El envío actual aprueba realizar fase1, no declara aceptada una implementación inexistente. Todo cambio material futuro debe justificarse y autorizarse antes de observar nuevas evaluaciones. No variar umbrales, historia mínima, agregación o variables para mejorar métricas.
''')
    doc('TRAZABILIDAD_DOCUMENTAL.md','''
# Trazabilidad de afirmaciones

|Afirmación/tipo|Archivo y sección/tabla/procedimiento|
|---|---|
|Estado inicial preparación, histórico propio|antecedentes_preparacion/CONTINUIDAD_DISENO.md completo; REGISTRO_PREPARACION.json:huellas_propias|
|Diagnóstico vigente, histórico|diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md:líneas1–105; manifiesto101huellas cotejado|
|Temporal cerrado sin mejora, histórico|experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md:líneas1–73; etapa2/resultados/meta.json|
|Continuidad temporal previa íntegra, histórica preservada|experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json:continuidad_inicial/continuidad_sha256, SHAfd3b963135e9e8233470ef36116d82e67ca4a88aae67b7c785d0a9185ba0b8bb; PREFLIGHT:manifiestos etapa1|
|Continuidad v5etapa1 versionada, histórico real|Git109797407d75d2097e5b71f8bcef3fc266bc61d2:experimentos_objetivo3_v5/CONTINUIDAD_V5.md; SHA33bbdce75635733eae8bad9e14d1900999fd8af6318a55842382b5d2544e13fd; PREFLIGHT|
|HEAD/rama/ascendencia/sin posteriores, comprobación actual|PREFLIGHT_FASE1.json:git, comandos lectura de verificar_documental.py|
|Huella fuente/derivado, comprobación actual|PREFLIGHT_FASE1.json:fuentes, sha256 bytes; no autenticación oficial|
|Entorno/defaults, comprobación actual|ENTORNO_FASE1.json completo:54lock exactos, pipcheck0, get_params, sin fit|
|231/33/198 y campos completos, reproducción estructural actual|SEMANTICA_FASE1.json y verificar_semantica.py:chunksize1024, shift por territorio, igualdad exacta|
|165referencias idénticas, comprobación actual|SEMANTICA_FASE1.json:referencias; tres CSV completos leídos; no calcular MAE nuevo|
|Ventanas y rezagos, formalización actual|TRAZABILIDAD_TEMPORAL.csv:15filas; ESPECIFICACION_DOCUMENTAL.json:ventanas exactas de configuraciones_congeladasv5|
|1320/16/825/528/46, expectativas documentales|PROTOCOLO_FASE1.md§5, productos y conteos explícitos; sin predicciones/ajustes|
|Memoria/común/corrección puede ayudar, hipótesis|PROTOCOLO_FASE1.md§6; ningún contraste nuevo ejecutado|
|Guainía, advertencia histórica|experimentos_objetivo3_v2/fase1/resultados/diagnostico_medias_disponibles.csv:filas57y90, código94,2025|
|Procedencia/ecología/dependencia y pocos años, limitaciones heredadas|Continuidades diagnóstico/temporal vigentes; PROTOCOLO_FASE1.md§6|
|Conservación actual|CONSERVACION_FASE1.json:comparación contra inventario30980, Git y originales propios preservados|

No PDF leído en esta fase:0páginas; documentos históricos se citan por archivo/sección/llaves, no como lectura nueva de sus fuentes primarias. Control de procedencia local sigue abierto científicamente; huellas no lo resuelven.
''')
    doc('REGISTRO_HALLAZGOS.md','''
# Hallazgos, impacto, alternativa y resolución

|ID/tipo|Hallazgo y evidencia|Impacto|Alternativa lógica verificable|Resolución en fase1/pendiente|
|---|---|---|---|---|
|H01 histórico|Recencia/global mejora0%; meta.json temporal|No punto de partida mejor demostrado|Contrastar memoria/común/corrección con primario fijo|4candidatos documentados, eficacia pendiente|
|H02 estructural actual|2019d disponible, d2018ausente; SEMANTICA y trace|No respuesta supervisada2019; no fitinternas2021|Excluir solo respuesta2019, mantener historial y respaldo0pares|Formalizado§3 sin imputar ni eliminar historia|
|H03 limitación diseño|Un año común=1fila, scaler constante|Dinámica común frágil, aprende principalmente nivel|Permitir regla aprobada, advertir y auditar unidades|Defaults y unidades formalizados; no subir mínimo|
|H04 actual|165referencias exactasv3/v5/temporal|No evidencia independiente adicional|Una referencia sobre mismas llaves|Cotejo completo, no contar triple evidencia|
|H05 histórico|2021–2025ya vistos, continuidades|Sesgo exploratorio/confirmación pendiente|Declarar alcance exploratorio y dejar evidencia independiente futura separada|Advertencias en protocolo/spec/continuidad|
|H06 actual|9manifiestos/30980antecedentes íntegros|Diseño puede partir sin reparar experimentos ajenos|Excepción precisa v5commitreal y continuidad temporal preservada|Verificador exacto, sin modificar etapa1|
|H07 histórico|Guainía238vs404, tabla v2filas57/90|Procedencia/media recibida requiere cautela|Preservar media y advertencia con ubicación|No reabrir corrección histórica sin nueva información|

Incidencias propias: lectura inicial del PLAN completo contraria al alcance solicitado (sin activar fases); salidas de lectura masiva truncadas (partida/preparación y consultas de metadatos), corregidas con procesamiento completo por código y resúmenes acotados, no se atribuye lectura humana de contenido truncado. Verificador inicial KeyError por campo sha256_texto_enlace en symlinks: detenido antes del cotejo, corregido sin seguir enlaces. Semántica inicial comparó códigos no normalizados y falló; aplicado zfill(2) ya contractual en historial temporal, no corrección de datos ni tolerancia nueva. Corridas finales aprobadas. Incidencias de esta sesión no se confunden con fallos históricos del análisis.

Antecedentes archivados: ausencia previa de entorno diagnóstico (resuelta según continuidad vigente y ahora ENTORNO_FASE1); helperdestino/symlink del temporal (resuelto/recongelado antes de sus fits, continuidadtemporal§incidencia). Evidencia intacta; sin nuevo impacto activo, no se reabren. Problemas científicos activos: confirmación independiente, procedencia oficial/disponibilidad y eficacia de hipótesis, fuera de fase1. No se cierran por aprobación documental.
''')
    common='''Trabajar en /home/kelium/Documents/espcarlos/icfes-predict-improved. Este prompt solo autoriza su fase cuando el usuario lo envía expresamente; su existencia o lectura no autoriza ejecución. Leer AGENTS.md, continuidad propia y antecedentes vigentes; del PLAN_FASES.md solo la fase solicitada y decisiones comunes. Verificar Git HEAD/asunto/rama/ascendencia/trabajo posterior y conservación sin reset ni sobrescribir ajenos. Cotejar continuidades históricas en su commit real; temporaletapa1 solo continuidad preservada y huella en etapa2/resultados/partida.json, sin modificarla. Mantener originales, fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc. Antes de cálculos exigir Python3.12.14/sklearn1.9.1/54lock/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010; falta/diferencia exige documentar y consultar sin sustituciones o instalaciones. No fuentes nuevas/commit/push/modelofinal/simulación/objetivo4 ni avance automático. Conservar población/media recibida/geografía colegio/2020excluido/2018historial/d sinanualizar/2021externofijo/165pares/meta5%/igualpeso. 2019historial sin respuesta conlag inexistente. Advertencias procedencia local/Guainía/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años; todos2021–2025vistos, exploratorio sin confirmación independiente ni causalidad. Cerrar incluso incompleto con entregables verificables, conservación, manifiesto, aceptación, pendientes y continuidad.'''
    doc('PROMPT_FASE2_IMPLEMENTACION.md', '# Nueva sesión — fase2 implementación y controles\n\n'+common+'''

Condición indispensable: fase1 documental válida por MANIFIESTO_FASE1.json/ACEPTACION_FASE1.json/conservación/entorno/especificación, y aprobación expresa de este diseño por el usuario al enviar este prompt. Detener si control indispensable anterior no resuelto. El envío autoriza fase2, no piloto ni fits reales. Leer PROTOCOLO_FASE1 y ESPECIFICACION_DOCUMENTAL; distinguir contrato documental de implementación congelada.

Crear SOLO experimentos_memoria_comun_objetivo3_v1/etapa1/ y continuidad experimental propia en su raíz, sin modificar diseño ni anteriores. Implementar4candidatos exactos con funciones/parámetros reutilizados, Pipelines separados, sin importar runners históricos ni cargar modelos. Pruebas con datos inventados y fits inventados exclusivamente para controles: fechas/rezagos anteriores y máximo previo/salto2019–2021, 33territorioscorrectos, d/c/r, una fila común por año/33territoriales, parámetros compartidos sin efectos por código, 1año permitido/0sinfitrespaldo, no respuesta2019, externa2021fija versus internas2021puntuadas con respaldo, scaler solo entrenamiento, invariancia al mutar validación/futuro, reconstrucción previo+cambio, defaults exactos y sin recencia, selección/bandas0.1/desempates0,1,1,2yorden, cobertura/CSVexactos/intfloat0equivalente/rechazo1e-11, linaje/copias/contexto, rutas/symlinks, terminación/fallos/presupuesto/retry/reanudación/conservación.

Generar notebook de controles desde fuente Python editable y generador Python, nbformat/validación/celdas realmente ejecutadas. No notebook de modelos, no ledger real iniciado ni fits del panel. Congelar implementación/defaults/reglas/candidatos/entorno/pruebas después de controles indispensables válidos y antes de ajustes reales. Cota46/7200solo contrato futuro, sin saldo heredado. No cerrar incompleto como congelación válida. Preparar continuidad y aceptación independientes con huellas para siguiente fase; no iniciar fase3 automáticamente.
''')
    doc('PROMPT_FASE3_PILOTO.md','# Nueva sesión — fase3 piloto exploratorio\n\n'+common+'''

Condición indispensable: diseño fase1 aprobado y fase2 completa/congelada con controles indispensables aprobados, manifiesto/conservación/fuentes/defaults/entorno revalidados; usuario envía expresamente este prompt. Si falta, cerrar incompleto sin piloto. Este envío autoriza fits reales solo del piloto predefinido, no rediseño, notebook personal ni entrenamiento final.

Escribir SOLO experimentos_memoria_comun_objetivo3_v1/etapa2/ y continuidad experimental propia. Revalidar fuente/panel/165referencias antes fit, sin deserializar históricos.4candidatos sin búsqueda: persistencia, memoria, común, común+corrección; scaler/Quantile0.5alpha1highs/defaults congelados, sin recencia. Un año completo permite fit; cero respaldo declarado; común1fila/año. Usar ventanas exactas, diez internas acumuladas, 2021externofijo. Primario procedimiento global predefinido; seleccionar solo internas con poolMAEmin+0.1→RMSEmin+0.1→entradas0/1/1/2→orden. No sustituir por política externa ganadora.

Conservar1320internas originales(4×10×33),16registros(4×4selecciones),825externas(4políticas+global×165).528únicas solo si copias/contexto exactos con linaje y menor externo representante. No compartir ajustes entre ventanas/candidatos; común y común+corrección tienen comunes propios. Ajustar4políticasexternas para contraste completo; global reutiliza solo MISMO candidato/ventana. Registros completos de X/y/llaves/d/c/r/fechas/unidades/scaler/defaults/semilla/versiones/advertencias/huellas/tiempos/estados/predicción/selección.

Presupuesto nuevo7200segundos; ledger persistente y runner serial terminable. Cota46componentes sin fallos=24internos+16externos+máximo6repeticionesglobales, no permiso de sobrepasar saldo; Pipelinecompleto cuenta1, respaldos0. Un retry máximo infraestructura, numérico/convergencia inelegible con razón, caída sin tiempo medido agota conservadoramente saldo, toda repetición consume. Repetición global de cada externa con mismo contexto o previo exacto si persistencia; atol1e-10/rtol0 para ajuste. No fabricate outputs de fits no hechos; interrupción/cobertura incompleta impide cierre completo y síntesis dependientes. Guardar evidencia suficiente de auditoría futura, no declarar éxito antes de controles válidos. No avanzar automáticamente a fase4.
''')
    doc('PROMPT_FASE4_AUDITORIA.md','# Nueva sesión — fase4 auditoría, interpretación y cierre\n\n'+common+'''

Condición indispensable: fases1y2válidas, pilotofase3 completo con entregables/ledger/manifiesto/conservación revalidados y autorización por envío expreso. Si piloto incompleto, documentar lo ocurrido sin cerrar controles irresueltos ni sintetizar resultados dependientes. Este envío autoriza auditoría de guardados, no nuevos fits/búsquedas/rediseño/instalaciones. No deserializar modelos históricos; modelos nuevos auditados por bytes y metadatos salvo autorización separada indispensable.

Escribir SOLO experimentos_memoria_comun_objetivo3_v1/etapa3/ y continuidad experimental propia. Implementar auditor independiente sin importar selector/constructores de matrices operativos para cotejo. Verificar fechas/máximo previo/ausencia2019respuestas/0y1año/2021fijo/unidades1comúnpor año y33territoriales/defaults/c/rprevios/ausenciafuga/scaler solo train/reconstrucción puntaje. Referencias mismas165llaves/observados v3persistencia/v5global/recenciaglobal, sin contar independencia. CSV exactos e intfloat0equivalente, rechazar1e-11, repeticiones guardadasatol1e-10/rtol0. Auditar selección exclusivamente interna/bandas/desempates/inelegibilidad, cobertura1320/16/825y528condicional con originales/linaje/contexto, presupuesto7200/cota46yfallos/retries/terminación; no fabricar faltantes.

Recalcular persistencia y global sobre mismas165llaves, peso igual, MAEfsum/RMSE/errores; meta100*(MAEpersistencia−MAEglobal)/MAEpersistencia≥5con denominadorfinito positivo. Primario fijo global, no rescate por otra política/grupo/corte. Comparaciones memoria/persistencia, común/persistencia y corrección/común descriptivas; todos2021–2025vistos, sin causalidad/confirmación independiente. Distinguir histórico/reproducción guardados/hipótesis.

Entregar informe incluso sin mejora, tablas completas y gráficos con unidades/n, notebook solo resultados desde fuente Python editable/generador Python/nbformat/celdas realmente ejecutadas, sin datos personales. Registro, lecturas, aceptación, conservación, manifiesto y continuidad propios. No cerrar científico procedencia/confirmación por controles técnicos. No iniciar nuevos modelos, simulación u otra fase automáticamente.
''')
    dump('LECTURAS_FASE1.json',{'pdf_paginas':0,'web':0,'fuentes_adicionales':0,'lecturas':[{'archivo':'AGENTS.md','alcance':'completo'},{'archivo':'antecedentes_preparacion/CONTINUIDAD_DISENO.md','alcance':'completo, antes actualización'},{'archivo':'PLAN_FASES.md','alcance':'lectura inicial completa por error; trabajo restringido a decisiones comunes y fase1; fases posteriores no ejecutadas'},{'archivo':'diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md','alcance':'vigente líneas1–105; salida inicial incluyó antecedentes archivados sin reapertura'},{'archivo':'experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md','alcance':'completa líneas1–73, lectura acotada corregida tras salida truncada'},{'archivo':'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json','alcance':'procesamiento JSON completo, solo continuidad_inicial/huella usados; protegidos no afirmados lectura humana'},{'archivo':'REGISTRO_PREPARACION.json','alcance':'JSON completo procesado; inventario/huellas/manifiestos revalidados, salida de cat truncada no contada como lectura completa en chat'},{'archivo':'PREFLIGHT_FASE1.json:manifiestos','alcance':'nueve índices completos y todos bytes/links cotejados, sin ejecutar fuentes/modelos'},{'archivo':'Git109797407d75d2097e5b71f8bcef3fc266bc61d2:experimentos_objetivo3_v5/CONTINUIDAD_V5.md','alcance':'blob completo cotejado SHA contra manifiesto etapa1 real'},{'archivo':'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json','alcance':'JSON completo procesado; ventanas consultadas, no ejecución grilla histórica'},{'archivo':'experimentos_temporales_objetivo3_v1/etapa2/fuentes/comun.py','alcance':'líneas1–38/90–133/225–258; fórmulas historial/selector lectura, no imports'},{'archivo':'experimentos_objetivo3_v5/etapa1/fuentes/comun_v5.py','alcance':'líneas1–95, lectura de reglas; no imports'},{'archivo':'SEMANTICA_FASE1.json:fuente/derivado/referencias','alcance':'datasets completos por bloques1024, igualdad exacta; sin evaluación nueva'},{'archivo':'experimentos_temporales_objetivo3_v1/etapa2/resultados/meta.json','alcance':'completo, resultado histórico'},{'archivo':'experimentos_objetivo3_v2/fase1/resultados/diagnostico_medias_disponibles.csv','alcance':'cabecera/filas57y90código94 y coincidencias de búsqueda; resto no revisión semántica nueva'}],'pendiente':['Pruebas operativas/controles inventados de fase2','Piloto y auditoría futuros bajo autorización','Fuentes primarias/autenticación/fechas de disponibilidad no ampliadas en esta fase']})
    doc('README.md','''
# Diseño memoria temporal y componente común — fase1 documental completa

2026-10-11. Empezar por CONTINUIDAD_DISENO.md, PROTOCOLO_FASE1.md, ESPECIFICACION_DOCUMENTAL.json y DECISIONES_FASE1.md. TRAZABILIDAD_TEMPORAL.csv contiene5externas+10internas y sus rezagos/unidades. Evidencia: PREFLIGHT_FASE1.json, ENTORNO_FASE1.json, SEMANTICA_FASE1.json, LECTURAS_FASE1.json, REGISTRO_FASE1.json, ACEPTACION_FASE1.json, CONSERVACION_FASE1.json, MANIFIESTO_FASE1.json. Trazabilidad y hallazgos documentan impacto/alternativas/resolución.

Solo diseño documental: cero fits, modelos cargados, notebooks, ledger operativo, instalaciones, nuevas fuentes, commit/push. No congelación operativa ni eficacia demostrada. Todas2021–2025vistas; exploratorio sin causalidad/confirmación independiente. Continuidad/README anteriores íntegros en antecedentes_preparacion/. PLAN_FASES/PROMPT_FASE1/REGISTRO_PREPARACION permanecen originales.

Scripts propios de documentación, no implementación de modelos: verificar_documental.py (cotejo byte/links/Git), verificar_semantica.py (reconstrucción en memoria y referencias exactas), generar_documentacion.py (textos/spec), cerrar_documentacion.py (conservación/aceptación/manifiesto). Ejecutados con PYTHONDONTWRITEBYTECODE=1 y /tmp/icfes-v2-fase2-venv/bin/python; versiones en ENTORNO_FASE1, semilla contractual20261010 sin aleatoriedad. Orden de esta sesión: entorno→preflight→semántica→documentación→cierre. No ejecutar automáticamente al retomar: primero autorización/continuidad/fase. La regeneración textual no constituye aprobación.

Prompts independientes2implementación/controles,3piloto,4auditoría preparados, condicionados a fase previa válida y envío expreso. Próximo pendiente: aprobación del diseño y autorización fase2; no avance automático. No hay un modelo nuevo ni predicciones nuevas que entregar.
''')
    print('Documentos y prompts generados; cierre pendiente, fits0.')

if __name__=='__main__': main()
