"""Preparación documental v6. No implementación de modelos ni ajustes."""
from pathlib import Path
import json,csv,hashlib,os,sys,subprocess,platform,importlib.metadata as md
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
SEED=20261010

def digest(p):
 p=Path(p)
 if p.is_symlink(): return hashlib.sha256(os.readlink(p).encode()).hexdigest()
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def load(p): return json.loads(Path(p).read_text())
def put(name,value):
 p=HERE/name
 if p.exists(): raise RuntimeError('Preservar existente: '+name)
 p.write_text(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT).decode()

def main():
 assert not (HERE/'CONTINUIDAD_V6.md').exists(),'Continuidad propia ya existe; no regenerar'
 lock={k.lower().replace('_','-'):v for line in (ROOT/'experimentos_objetivo3_v5/etapa1/requirements.lock.txt').read_text().splitlines() if '==' in line and not line.startswith('#') for k,v in [line.strip().split('==')]}
 actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions()}
 pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
 assert platform.python_version()=='3.12.14' and len(lock)==54 and {k:v for k,v in actual.items() if k!='pip'}==lock and pip.returncode==0 and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1','entorno exige consultar sin sustituir/instalar'
 # get_params únicamente; cero fits reales o inventados.
 from sklearn.preprocessing import StandardScaler
 from sklearn.linear_model import QuantileRegressor,Ridge
 from sklearn.tree import DecisionTreeRegressor
 defaults={type(x).__name__:x.get_params() for x in [StandardScaler(),QuantileRegressor(),Ridge(),DecisionTreeRegressor()]}
 put('ENTORNO_DOCUMENTAL.json',{'aprobado':True,'python':platform.python_version(),'sklearn':actual['scikit-learn'],'lock':lock,'actual':actual,'pip_check':{'returncode':pip.returncode,'stdout':pip.stdout,'stderr':pip.stderr},'PYTHONDONTWRITEBYTECODE':'1','semilla':SEED,'defaults_sin_fit':defaults,'fits':0})
 head=git('rev-parse','HEAD').strip(); branch=git('branch','--show-current').strip()
 assert head=='75c3a25182af363f47b0d743820f99084e18fed5' and branch=='codex/objetivo3-v5-mae' and not git('diff','--name-only','HEAD').strip()
 for commit in [head,'109797407d75d2097e5b71f8bcef3fc266bc61d2']:
  assert subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT).returncode==0
 snapshot={}
 for s in git('ls-files','--cached','--others','--exclude-standard','-z').split('\0'):
  if s and not s.startswith('experimento_final_objetivo3_v6/'):
   p=ROOT/s
   if p.is_file() or p.is_symlink(): snapshot[s]=digest(p)
 put('PARTIDA_DOCUMENTAL.json',{'protegidos':snapshot,'head':head,'asunto':git('log','-1','--format=%s').strip(),'rama':branch,'posteriores':git('log',head+'..HEAD','--format=%H').splitlines(),'raw':'ignorado; sin lectura/censo/escritura','continuidad_propia_previa':None})
 old=ROOT/'experimentos_memoria_comun_objetivo3_v1/etapa3'
 m=load(old/'MANIFIESTO_FASE4.json')
 for s,h in m['entregables_sha256'].items(): assert digest(old/s)==h,s
 assert digest(old.parent/'CONTINUIDAD_EXPERIMENTAL.md')==m['continuidad_actual_sha256']
 assert load(old/'ACEPTACION_FASE4.json')['completa']
 inherited=load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')
 for s,v in inherited['fuentes'].items(): assert digest(ROOT/s)==v['esperado']
 historic=load(ROOT/'experimentos_memoria_comun_objetivo3_v1/etapa1/PREFLIGHT_FASE2.json')['historica_v5']
 assert hashlib.sha256(subprocess.check_output(['git','show',historic['commit']+':'+historic['archivo']],cwd=ROOT)).hexdigest()==historic['sha256']
 temporal=load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
 assert hashlib.sha256(temporal['continuidad_inicial'].encode()).hexdigest()==temporal['continuidad_sha256']
 # Grilla documental fija: aún no matrices reales, métricas, selección ni piloto.
 candidates=[]
 def add(id,family,history,components,inputs,params,statistic=None):
  candidates.append({'id':id,'order':len(candidates),'family':family,'history':history,'components':components,'inputs':inputs,'params':params,'statistic':statistic})
 add('persistencia','persistencia','all',[],0,{})
 for statistic in ['median','mean']:
  for history in ['all','last1','last2','last3']: add('nivel_'+statistic+'_'+history,'nivel_territorial',history,[],0,{},statistic)
 for history in ['all','last2','last3']:
  for alpha in [0.0,0.01,0.1,1.0]:
   q=dict(defaults['QuantileRegressor'],alpha=alpha)
   add('memoria_qr_a'+str(alpha).replace('.','p')+'_'+history,'memoria_qr',history,['memoria'],1,{'StandardScaler':defaults['StandardScaler'],'QuantileRegressor':q})
 for history in ['all','last2','last3']:
  for alpha in [1.0,10.0]:
   q=dict(defaults['Ridge'],alpha=alpha,random_state=SEED)
   add('memoria_ridge_a'+str(alpha).replace('.','p')+'_'+history,'memoria_ridge',history,['memoria'],1,{'StandardScaler':defaults['StandardScaler'],'Ridge':q})
 for depth in [1,2]:
  q=dict(defaults['DecisionTreeRegressor'],criterion='absolute_error',max_depth=depth,min_samples_leaf=11,random_state=SEED)
  add('memoria_arbol_d'+str(depth)+'_all','memoria_arbol','all',['memoria'],1,{'StandardScaler':defaults['StandardScaler'],'DecisionTreeRegressor':q})
 for statistic in ['median','mean']: add('nivel_comun_'+statistic+'_all','nivel_comun','all',[],0,{},statistic)
 for alpha in [0.0,0.01,0.1,1.0]:
  q=dict(defaults['QuantileRegressor'],alpha=alpha)
  for family,components,inputs in [('comun_qr',['comun'],1),('comun_correccion_qr',['comun','correccion'],2)]:
   add(family+'_a'+str(alpha).replace('.','p')+'_all',family,'all',components,inputs,{'StandardScaler':defaults['StandardScaler'],'QuantileRegressor':q})
 assert len(candidates)==39 and sum(len(c['components']) for c in candidates)==32
 with (HERE/'CANDIDATOS.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['order','id','family','history','components','inputs','statistic','params']);w.writeheader()
  for c in candidates: w.writerow({**c,'components':json.dumps(c['components']),'params':json.dumps(c['params'],sort_keys=True)})
 spec={'version':'6.0.0','estado':'protocolo documental cerrado; implementación/piloto NO ejecutados','autorizacion_actual':'solo preparar protocolo/plan/archivos/prompt, según envío humano','fecha_cliente':'2026-10-11','timezone':'America/Bogota','semilla':SEED,'fuentes':{s:v['esperado'] for s,v in inherited['fuentes'].items()},'entorno':inherited['entorno'],'poblacion':inherited['poblacion_heredada'],'years':inherited['anios'],'windows':inherited['ventanas'],'candidates':candidates,'primary':'global_v6 seleccionado exclusivamente por internas','reference':'persistencia/v3, mismas165llaves/observados; no referencia memoria retrospectiva','target_percent':5,'selection':{'MAE_band':0.1,'RMSE_band':0.1,'ties':['inputs','order'],'inclusive':True,'external_2021':'persistencia fija, sin fit/scoring/selection'},'history_rule':'Seleccionar respuestas completas elegibles desde2021, después aplicar últimos k años; conservar niveles previos necesarios y lag anterior, nunca futuro.2019 solo historial. Con menos de k usar todos los disponibles; cero años respalda persistencia. Común mismo conjunto temporal del candidato.','estimation':'median: promedio de los dos valores centrales cuando n sea par;mean:fsum/n. Nivelterritorial apila33respuestas por año; nivelcomun una mediana territorial por año.','no_inputs':['year','code','interval','IPM','counts','evaluated_d','evaluated_c','evaluated_r'],'budget':{'seconds':7200,'new_ledger':True,'internal_component_fits':192,'external_component_fits':128,'global_repeat_component_fits_max':8,'component_fits_max_without_failures':328,'retry_infrastructure_max':1,'no_reuse_balance':True,'statistical_estimates_without_sklearn_fit':{'internal':60,'external':40,'global_checks_max':4,'max':104},'measurement':'desde runner real hasta cierre durable, incluyendo arranque/comunicación/constantes/repeticiones/fallos/retries/pausas; preparación/sintéticos separados'},'coverage':{'internal_original':12870,'selection_records':156,'external':6600,'internal_unique_conditional':5148,'lineage':12870,'global_checks':5},'notebook_contract':'todos los cálculos/tablas/figuras/números nuevos del texto originados en celdas realmente ejecutadas;fuente.py+generador.py;nbformat;archivos de salida con manifiesto;sin datos personales','forecast_horizon_years':1,'objective4_execution_authorized':False,'new_data_installations_commits_push_authorized':False}
 put('ESPECIFICACION_V6.json',spec)
 put('PROTOCOLO_V6.md',PROTOCOL)
 put('PLAN_V6.md',PLAN)
 put('PROMPT_NUEVA_SESION_V6.md',PROMPT)
 put('README.md',README)
 put('CONTINUIDAD_V6.md',CONTINUITY)
 put('DECISIONES_Y_HALLAZGOS.md',DECISIONS)
 readings=['AGENTS.md','experimentos_memoria_comun_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md','experimentos_memoria_comun_objetivo3_v1/etapa3/PROPUESTAS_FUTURAS.md','experimentos_objetivo3_v3/etapa2/resultados/meta.json','diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json']
 put('LECTURAS_DOCUMENTALES.json',{'archivos':{s:{'sha256':digest(ROOT/s),'revisado':'completo; JSON procesado íntegro'} for s in readings},'otros':'metadatos de entorno/get_params;manifiesto/aceptaciónfase4;históricav5commitreal;temporal texto preservado;fuentes_verificadas solo referencias locales de fechas, no autenticación nueva','planes_anteriores':'No leídos; nueva continuidad inexistente al inicio, inventario propio de partida','PDF_paginas':0,'web':0,'pendientes':'implementación/pruebas/freeze/piloto/auditoría/notebook/texto tesis;disponibilidad real no autenticada'})
 put('REGISTRO_DOCUMENTAL.json',{'primer_control_fase4':{'aprobado':True,'huellas':54,'protegidos':32266,'fits':0,'modo':'lectura; ejecutado antes crear esta carpeta'},'manifiesto_fase4_revalidado':len(m['entregables_sha256']),'historica_v5':historic,'temporal_preservada_sha256':temporal['continuidad_sha256'],'fuentes':spec['fuentes'],'autorizacion':'Preparación documental ahora; ejecución solo por envío humano del prompt en nueva sesión. No ejecutar prompt por leerlo.','candidatos_propuestos':39,'fits_actuales':0,'presupuesto_actual_iniciado':False,'plazo_usuario':'Objetivos listos hoy; presentación martes. No garantía de duración ni cierre científico por plazo.','ultima_version':True})
 # No se altera ninguna continuidad/manifestación previa; estado propio nuevo.
 bad=[s for s,h in snapshot.items() if digest(ROOT/s)!=h]
 foreign=[s for s in git('ls-files','--cached','--others','--exclude-standard','-z').split('\0') if s and s not in snapshot and not s.startswith('experimento_final_objetivo3_v6/')]
 assert not bad and not foreign and not git('diff','--name-only','HEAD').strip()
 put('CONSERVACION_DOCUMENTAL.json',{'aprobado':True,'protegidos':len(snapshot),'diferencias':bad,'ajenos_nuevos':foreign,'raw':'sin lectura/censo/escritura','continuidades_anteriores':'intactas; no actualizar cierres anteriores para añadir v6'})
 put('ACEPTACION_DOCUMENTAL.json',{'completa':True,'aceptacion':'coherencia e integridad documental; NO implementación/congelación/piloto ni aprobación de eficacia','controles':{'entorno_exacto':True,'originales_conservados':True,'fase4_previa_valida':True,'candidatos39_y_cota328_documentados':True,'primario_y_meta_fijos':True,'notebook_trazabilidad_y_texto_exigidos':True,'prompt_condicionado':True},'pendientes_indispensables_documentales':[],'pendientes_ejecucion':['Envío humano del prompt','Implementación y pruebas','Congelación antesfit','Piloto7200','Auditor independiente','Notebook ejecutado y texto tesis','Cierre completo o incompleto'],'fits':0,'modelos_cargados':0,'objective4':False})
 exclusions=['MANIFIESTO_DOCUMENTAL.json','VERIFICACION_DOCUMENTAL.json']
 put('MANIFIESTO_DOCUMENTAL.json',{'entregables_sha256':{p.relative_to(HERE).as_posix():digest(p) for p in HERE.rglob('*') if p.is_file() and p.name not in exclusions},'exclusiones_autorreferencia':exclusions,'estado':'preparación documental completa','continuidad_sha256':digest(HERE/'CONTINUIDAD_V6.md')})
 print('Paquete documental creado:39candidatos;0fits;originales intactos')

PROTOCOL='''# Protocolo6.0.0 — último experimento exploratorio y entrega del objetivo3

Fecha2026-10-11 America/Bogota. Autoridad actual: usuario pide cerrar protocolo/crear plan/archivos/prompt para ejecutar en NUEVA sesión. Esta sesión solo preparación documental. No ejecutar ajustes reales/inventados, crear matrices/notebooks de modelos, instalar, buscar fuentes, commit/push, modelo final, proyectar2026 u objetivo4. El envío humano posterior del prompt autoriza su flujo condicionado; la existencia/lectura del archivo no autoriza ejecución.

## 1. Pregunta, primario y límites

¿Puede un procedimiento predefinido que contraste nivel histórico, rezago, regularización y cantidad de historia reducir al menos5% el MAE frente a persistencia/v3 sobre las mismas165llaves/observados? Primario: global_v6, selección exclusivamente interna. Las39políticas individuales son contrastes exploratorios completos, no ganadores externos que sustituyan al primario. Referencia exacta3.429267191379531; umbral orientativo3.2578038318105547. Calcular100×(MAEref−MAEglobal)/MAEref con denominador positivo finito. No sumar porcentajes de mejoras con bases distintas. V3/meta registra29.721754266970148%frentev2 y ganador persistencia; no18% ni aprendizaje IPM demostrado. Memoria reciente12.392390281511053%solo descriptivo;global1.7979745286559843%. Son antecedentes, deben recalcularse en notebook antes de usarse numéricamente en texto final.

Todos2021–2025vistos y grilla inspirada en hallazgos previos: exploratorio, sin prueba independiente, causalidad ni promesa5%. El plazo no justifica redefinir población, selección, métricas, meta o declarar resultados incompletos como completos. No nuevas versiones ni experimentos automáticos después de v6; entregar informe incluso sin mejora.

## 2. Población, objetivo y tiempo

Conservar ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario/media global recibida/geografía colegio;33territorios/peso igual territorio-año.2018nivel histórico,2020excluido,2019historial sin respuesta supervisada por lag inexistente. d[j,t]=puntaje[j,t]−puntaje[j,previo(t)], máximo previo estrictamente anterior, sin anualizar el salto2019–2021. c[t]=mediana de33d, auxiliar no media nacional; r[j,t]=d[j,t]−c[t]. Puntaje previsto=previo+cambio previsto, sin clipping, mezcla o calibración. No introducir año/código/intervalo/conteos/IPM/tasas como entradas. No es un modelo de efectos de intervenciones.

Ventanas exactas en ESPECIFICACION_V6.json/windows:externas2021–2025;2021externa fija persistencia para todas políticas/global, sin ajuste/puntuación/selección. Para externas2022–2025 internas2021..externo−1 (1+2+3+4=10). Internas2021 respaldadas y puntuadas. Predicción siempre solo historia anterior, nunca2025para2024. Rangos con años posteriores serían reconstrucción y quedan fuera.

## 3. Grilla fija39 candidatos y orden de desempate

Autoridad: detalles técnicos nuevos decididos en preparación tras usuario aprobar último experimento acotado, proyección un año,7200s/meta5%/entrega notebook+texto. No se observaron resultados v6 al elegirlos. CANDIDATOS.csv/ESPECIFICACION_V6.json son el contrato de IDs/orden/params completos, no una búsqueda abierta.

1. Persistencia(1):cambio0,0entradas.
2. Niveles territoriales(8):mediana o media de respuestas d históricas apiladas33filas/año;historia all/last1/last2/last3;0entradas predictoras. Aprenden una estadística histórica aunque no llamen sklearn.fit. Mediana par=promedio de centrales;media=fsum/n. No se reproduce retrospectivamente un extremo de mediana para conseguir mejor métrica.
3. MemoriaQR(12):dprevio→d,alpha0/0.01/0.1/1,history all/last2/last3,quantile0.5/highs/interceptTrue;1entrada. Rango fijo incluye regularización nula y tres órdenes de magnitud, para separar hipótesis de rezago y regularización, sin refinamiento posterior. No atribuir diferencias causalmente solo a alpha.
4. MemoriaRidge(6):mismoX/y,alpha1/10 y all/last2/last3;1entrada. Contraste pequeño de pérdida cuadrática y estabilización, no búsqueda de óptimo.
5. Memoriaárbol(2):mismoX/y,historyall,criterionabsolute_error,depth1/2,min_samples_leaf11;1entrada. Contraste no lineal limitado por pocos años;11filas equivalen a un tercio del primer año territorial, sin inferir independencia de33territorios. No boosting/grillas arbitrarias ni nuevas variables.
6. Niveles comunes(2):media/mediana de c por año con historyall,1fila/año,0entradas predictoras; igual peso años.
7. ComúnQR y común+correcciónQR(8):historyall,alpha0/0.01/0.1/1;común cprevio→c con1fila/año;corrección rprevio→r con33filas/año;1/2entradas. Cada candidato tiene común propio; ambos componentes de corregido usan su alpha pero Pipelines independientes. Permite estudiar corrección bajo regularizaciones distintas del antecedentealpha1; no asumir utilidad/inutilidad universal.

Todos componentes ajustados:Pipeline nuevo StandardScaler(copyTrue,with_meanTrue,with_stdTrue)→regresor indicado. Árbol usa mismo scaler por contrato uniforme; no se exige que escalar aporte al árbol. Defaults completos obtenidos sinfit del entorno en ESPECIFICACION/ENTORNO_DOCUMENTAL;random_state20261010 para Ridge/árbol. QR no recibe random_state inexistente. Sin sample_weight/recencia, selección automática adicional, ajustes compartidos entre candidatos/ventanas o cachéfit. Fijar todos los defaults antes del primerfit. No cargar/deserializar modelos históricos.

## 4. Cantidad de historia y respaldos

Primero determinar respuestas completas con lag disponible y33territorios desde2021 anteriores al evaluado. Después all conserva todas y lastk toma últimosk años de esas RESPUESTAS;mantener los niveles y rezagos anteriores requeridos para formar esas filas. No cortar niveles antes de verificar lag, ni incluir2019como respuesta. Con menos dek años usar todos los disponibles; cero años obliga persistencia declarada sinfit/estimación;uno permite ajuste (común1fila,territorial33). Duplicados, falta inesperada de territorios o nofinito son integridad fallida, no respaldo silencioso.

Niveles territoriales/comunes usan ese mismo conjunto de respuestas elegibles; no introducir d2019en su estimación para favorecerlos. Comparación sinrezago/rezago queda sobre historia comparable. No mezclar territorio con año como predictor. Las grillas lastk pueden coincidir en historia pequeña: registrar equivalencia, no contarlas como evidencia independiente ni compartir ajustes. La deduplicación de internas solo procede dentro del MISMO ID y año con contexto/copia exactos.

## 5. Selección y salidas fijas

Por ventana, concatenar internas de cada ID con mismo peso. MAE=fsum(abs(error))/n;RMSE=sqrt(fsum(error²)/n). Elegibilidad exige cobertura completa/finita. PoolMAE≤mínimo+0.1 inclusivo; dentro poolRMSE≤mínimoRMSE+0.1 inclusivo; desempatar por entradas predictoras0/1/2 y orden fijo. Niveles constantes cuentan0entradas X, aunque aprendan respuestas históricas; persistencia va primero en el orden. Es nueva convención explícita antes de v6, no criterio histórico inventado. No cambiar bandas, preferir recencia o política externa por resultados. No external2021en selección. Guardar decisiones antes de externas de cada ventana.

Cobertura:12870internas originales=39×10×33;156registros=39×4;6600externas=(39+global)×165;5148únicas=39×4×33 solo copias/contextos exactos,linaje12870y representante menor externo. Conservar originales y contextos de entrenamiento que excluyan externo para comparar copias. Global reutiliza salida del mismo ID/ventana;cinco checks con previo exacto, recomputación constante mismo contexto o repetición ajustada conatol1e-10/rtol0. No cambiar métricas para rescatar éxito. Auditar CSVexactos/intfloat0/rechazo1e-11.

Además del primario:comparaciones pareadas constantes/rezagos/alphas/history/pérdidas/común/corrección,MAE/RMSE/sesgo/signos por año/territorio,coef/scaler/predicción. Todos descriptivos; controlar que cambie solo el factor del contraste cuando sea posible. No atribuir diferencias en combinaciones a un único factor. No tratar165pares o copias internas como observaciones independientes. Sin p-valores confirmatorios, exactitud por tolerancia inventada ni umbral de categoría nuevo.

## 6. Presupuesto y fallos

Nuevo ledger7200s, sin heredar saldos;NO iniciado en preparación. ComponentePipeline completo cuenta1fit.39candidatos suman32componentes por contexto ajustable;192internos=32×6,128externos=32×4,hasta8repeticiones=2×4;cota328sin fallos. Aparte constantes:60estimaciones internas+40externas+hasta4recomputacionesglobales=104máximo, presupuestadas en tiempo aunque no son fits sklearn. No ocultar aprendizaje de constantes bajo etiqueta sinmodelo. Preparación y tests inventados tiempos separados y claramente rotulados.

Runner serial durable y terminable, medición monotónica continua desde creación ledger antes de primertrabajo hasta cierre, incluidos arranque/comunicación/constantes/repeticiones/fallos/retries/pausas. Un retry máximo de infraestructura en el piloto;numérico/convergencia inelegible, sin retry. Si impide coberturas indispensables, detener y cerrar incompleto sin síntesis dependiente. Pendiente tras caída sin tiempo medido agota conservadoramente;no reiniciar/ampliar7200ni reabrir cierre. No eliminar un candidato fallido para inventar cobertura39. Registrar procesos terminados. Cerrar ledger al terminar piloto/checks antes de auditoría y redacción, que son0fits y no reutilizan saldo.

## 7. Entorno, fuentes y comprobaciones

Exigir antes de cálculos:Python3.12.14/sklearn1.9.1/54lock exactos/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010. Entorno/tmp/icfes-v2-fase2-venv. Ausencia/diferencia:documentar/consultar, sin instalación/sustitución. Fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc. Solo fuentes actuales;sinraw/nuevasfuentes/red.

GitHEAD/asunto/rama/ascendencia/posteriores/conservación;no reset/sobrescribir ajenos. Continuidades históricas en commits reales;temporal solo preservada/huella partidaetapa2;fase2memoria continuidad íntegra preservada. Cierres previos no se modifican para tolerar carpeta nueva;verificar sus mappings/continuidades históricas. Fase4memoria íntegra ya revalidada antes crear este paquete,registro propio. Manifestación original y aceptación de v6documental obligatorias antes implementar.

Pruebas inventadas útiles:fuentes/llaves/fechas/cobertura/lag/lastk/2019/noanualización,anti-fuga mutando futuros,mediana par/mean/cero-un año/unidades,defaults/scalertrain/Pipelines propios,constantes/aporte común/reconstrucción,selección/pools inclusivos/entradas/orden,linaje/copias/contextos/reuso/globalfitynofit,CSV/routes/symlinks/terminación/caída/retry/presupuesto/no reabrir. Congelar fuentes/candidatos/rules/defaults/tests/notebookcontroles/entorno ANTES ajustes reales. Auditor independiente posterior no importa selector/constructores/runners ni deserializa;reconstruye desde fuentes y guardados. Coef0no atribuir soloalpha sin contraste;inspeccionar estabilidad/coef/no finitos.

## 8. Notebook y texto listo para tesis

Entregables principales futuros:02_resultados_objetivo3.ipynb desde fuenteeditablePython+generadorPython validado/releído nbformat, celdas realmente ejecutadas (kernel oexecsecuencial explícito),y TEXTO_OBJETIVO3_TESIS.md listo para incorporar. Notebook controla el análisis:funciones compartidas Python para cálculos/plots, llamadas desde sus celdas que generan CSV/JSON/PNG finales;no cifras o gráficos nuevos calculados únicamente fuera de notebook y copiados. Guardados piloto son entradas,no salidas de ejecución ficticia. Separar notebook01controles y02resultados;no notebookpersonal ni objetivo4. No datos personales, solo agregados.

Todas cifras nuevas del texto salen de salidas notebook. Generar EVIDENCIAS_TEXTO.csv con identificador de afirmación,celda/función,archivo/tabla/llave/unidad/n/sha;verificar valores contra salidas, incluidas cifras históricas utilizadas (v3/meta,etc) recalculadas/cotejadas allí. No inventar resultados o citas;afirmaciones bibliográficas solo documentos locales verificados y ubicación, sin nuevas fuentes. Figuras con unidades/n/peso/códigos, revisión visual, versionadas porSHA;cada figura originada desde notebook. Entregar tablas completas, no solo mejores cortes.

Texto:objetivo/población/cronología/referencia/metodología/historialexperimental/resultadosprimarios/contrastes/limitaciones/conclusión honesta/puente a objetivo4. Escribir incluso si no mejora;si incompleto, describir controles fallidos y no sintetizar métricas dependientes. No convertir grilla amplia y años vistos en confirmación. Plazo usuario:entrega hoy para presentación martes;no prometer duración o suficiencia científica por presión.

## 9. Puente al objetivo4 y cierre

Objetivo4 humano aclarado:proyectar solo el siguiente año,puntaje global promedio territorial. Verificar último año del panel esperado2025 y evidencias locales de disponibilidad;sin autenticar publicación por hashes. Documentar horizonte2026CONDICIONAL si el último año utilizable fuera2025, no emitir predicciones2026 ahora. Ningún nuevo dato o simulación. BuenMAE no obliga a usarIPM;la proyección de puntajes no es efecto de modificar pobreza.

MetaNO no impide concluir científicamente objetivo3;no autoriza rescatar otra política, modelo final ni avanzar automáticamente al4. Informe puede declarar referencia o método exploratorio útil con límites, y ausencia de mejora adicional. Decisión de aplicación/objetivo4 requiere autorización separada;incertidumbre no se inventa con pocos años, se documenta necesidad de diseño/evaluación de cobertura.

Preservar procedencia local no autenticada,Guainía238vs404/21.012105832431985puntos histórico v2 diagnóstico_medias_disponibles filas57y90,IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años. Aceptación técnica no acredita autenticidad/disponibilidad/causalidad/confirmación. Archivar antecedentes sin impacto actual con evidencia;no reabrir sin nueva información. Cerrar cada fase con lecturas,hallazgos/impacto/alternativa/resolución,aceptación/conservación/manifiesto/pendientes/continuidad propia preservando anterior. Sin commit/push/instalaciones/fuentesextra/otra versión/otro experimento automático.
'''

PLAN='''# Plan v6 — última versión y entrega del objetivo3

## Decisiones comunes

Autorización presente:preparar documentos,prompt y archivos;0fits. Usuario:entrega hoy,presentación martes;horizonte un año;7200sajustes;notebookytexto listoparatesis,figuras/cálculos originados en notebook;sin requisitos extra del director;mantener5%adicional y cierre honesto. Protocolo6.0.0 y ESPECIFICACION son decisiones nuevas antes de resultados. Escribir solo carpeta propia nueva;originales y cierres previos intactos. Leer al retomar continuidad propia y solo fase activa de este plan más decisiones comunes;protocolo completo es contrato transversal.

### Fase0 — preparación documental (sesión actual)

Inventario al no existir continuidadv6. Revalidar entorno/sources/Git/fase4memoria y conservar todo. Crear protocolo/grilla39/JSON/plan/decisiones/lecturas/registro/continuidad/aceptación/conservación/manifiesto/verificador y prompt. Cero notebooks/matrices/fit reales o inventados/ledger. Cierre documental no es freeze operativo ni resultado. Nueva sesión por envío humano del prompt.

### Fase1 — implementación, controles y congelación

Verificar paquete documental,originales/entorno/referencias;implementar motores comunes propios y adaptadorpanel,selector/runner/ledgerserial y controles inventados. Crear notebook01controles con fuentePython/generador/nbformat y ejecución real. Probar39políticas y32componentes por contexto sin cambios científicosescondidos. No fits reales hasta aceptación válida y freeze propio que cubra fuentes/defaults/semilla/entorno/candidatos/reglas/tests/notebook. Si indispensable falla,resolver dentro de contrato o cerrar incompleto;no iniciarpiloto. Al entrar leer únicamente esta sección y decisiones comunes. Preservar continuidad anterior de fase0 antes actualizar.

### Fase2 — piloto único acotado

Condicionado a fase1completa/congelada,por autorización del prompt enviado. Crear ledger NUEVO7200s;ejecutar exactamentegrilla39yventanas guardadas,sin nuevas búsquedas/no extender.32componentes×6internas+32×4externas+hasta8rep=328cota,estimacionesconstantesmáx104aparte tiempo contabilizado.12870originales/156registros/6600externas/5148únicas condicionales/linaje/cinco globalchecks. Selección antes externas,repeticionesincluidas,ningúnreusocandidatos/ventanas,saldo no heredado. Cerrar ledger al terminarpiloto;fallo presupuesto/cobertura/integridad obliga incompleto. No modificar criterios al ver externas. No auditora interpretativo reentrenar. Al entrar leer únicamente esta sección y decisiones comunes.

### Fase3 — auditoría independiente, notebook y texto de tesis

Revalidar acepta/manifiesta/freeze/conserva/panel/entorno/tests/notebook/ledger/artifacts;auditor independente cero nuevosfits/importsoperativos/deserialización. Reconstruir fechas/matrices/scalers/coef/constantes/defaults/referencias165/pools/linaje/global/CSV/cobertura/presupuesto/terminación. Pruebas inventadas del auditor,sin fits. Con controles completos,notebook02ejecuta recálculos/tablas/figuras/cotejos históricos/origen cifras texto;validarnbformat/ejecución/generadorfuentes. Emitir TEXTO_OBJETIVO3_TESIS.md y EVIDENCIAS_TEXTO.csv;visualizar figuras/QA. Si incompleto,notebook/reporte de controles verificables sin resultados dependientes ni outputsfabricados. Concluir primario fijo5%sin rescate;políticasdiagnósticasexploratorias. Documentar próximoañocondicional2026 y disponibilidad no autenticada,sin ejecutarobjetivo4. No modelofinal/otra versión/otra fase. Cierre incluso sinmejora,con continuidad originalpreservada/pendientes científicos/manifiesto/conservación/verificación. Al entrar leer solo esta sección y decisiones comunes.

## Flujo autorizado en nueva sesión

El envío humano expreso de PROMPT_NUEVA_SESION_V6.md autoriza fases1→2→3 en esa sesión,solo al pasar controles entre fases;no hay autorización por lectura del archivo. No pedir aprobación repetida para transiciones ya incluidas. Si faltan recursos/entorno o decisión material fuera contrato,documentar/consultar,sin sustituir/instalar. Tiempo del ajuste7200no abarca preparación/redacción;priorizar cierre y entrega,no una versiónposterior.
'''

PROMPT='''# Nueva sesión — última versión v6: experimento único y texto del objetivo3

Trabajar en /home/kelium/Documents/espcarlos/icfes-predict-improved.

Mi envío expreso de este prompt autoriza ejecutar exclusivamente fases1→2→3 de experimento_final_objetivo3_v6/PLAN_V6.md:implementar/probar/congelar,un piloto exploratorio predefinido y auditoría independiente/notebook/texto listo para tesis. Es la última versión;necesito la entrega hoy para presentar la tesis el martes. No autoriza objetivo4/proyecciones2026/simulación/modelo final/notebook personal/nuevas fuentes/instalaciones/commit/push/otra versión u otro experimento. La existencia o lectura del prompt no autoriza ejecución.

## Entrada y contrato

LeerAGENTS.md,experimento_final_objetivo3_v6/CONTINUIDAD_V6.md y antecedentes vigentes. DelPLAN_V6leer solo decisiones comunes y sección correspondiente a la fase que se inicia;al pasar a siguienteleer esa sección. LeerPROTOCOLO_V6.md completo,ESPECIFICACION_V6.json y CANDIDATOS.csv;son contrato cerrado,sin decisión pendiente de hiperparámetros. Primero ejecutar en lectura:
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python experimento_final_objetivo3_v6/verificar_documental.py

Revalidar fase4memoria por mappings originales y continuidad histórica preservada,sin modificar su cierre para aceptarcarpeta nueva. Revalidar fase1/fase2memoria huellas originales y fase2continuidad íntegra preservada en etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md. GitHEAD/asunto/rama/ascendencia/trabajo posterior/conservación;históricav5etapa1encommitreal109797407d75d2097e5b71f8bcef3fc266bc61d2;temporaletapa1solo texto/huella de experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json. No reset/sobrescritura ajena ni excepción documental inventada. Si entorno/fuente/control indispensable falla,documentar y cerrar incompleto;no fabricar faltantes ni síntesis dependiente.

ExigirANTES cálculosPython3.12.14/sklearn1.9.1/54lockexactos/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010. Entorno/tmp/icfes-v2-fase2-venv. Falta/diferencia:consultar sin sustituir/instalar. Fuentesv2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc. No raw/nuevosdatos/red. Procesar panel completo mediante código/bloques,chat con resúmenes pequeños. Escribir SOLO experimento_final_objetivo3_v6/,continuidad propia preservando su anterior en antecedentes por fase;no tocar experimentos previos ni .git.

## Fase1 y piloto

Implementación propia reusable y controles inventados/notebook01fuentePython+generador/nbformat con celdas realmenteejecutadas. No nuevosfitsreales antes aceptación y congelación operativa propia,cubrientecódigo/candidatos/reglas/defaults/tests/notebook/entorno/semilla. Verificar defaults sin alterar especificación. Probar temporalidad,lastk después de respuestas elegibles,no2019respuesta,2020excluido/2018nivel/2021previo2019sinanualizar/cero-respaldo/unofit/33vs1/anti-fuga/constantesmediana-parmedia/defaults/Pipelines/scalertrain/reconstrucción/selector/pools/linaje/reuso/CSV0y1e-11/rutas/symlinks/serialterminación/retry/caída/presupuesto.

Ejecutar SOLO39candidatos de ESPECIFICACION,IDs/orden/params completos exactos. Preguntas:nivelhistórico,aporterezago,regularización,historiacompletaúltimosk,pérdida/no linealidad pequeña ycomún/corrección. No afinaralpha/probarvalores extra/recentwindow nueva/variablesnuevas por resultados. UnPipeline nuevo por componente/candidato/ventana;no compartir fits,no cargar modelosprevios. Estadísticasconstantes son estimaciones históricas,contabilizarlas aunque nosklearnfit.

Mantener población/mediarecibida/colegiogeografía/igualpeso/165pares/meta5%.Windows exactas:2021externafija sinfit/scoring/selection;internas2021respaldos puntuados;10internasacumuladas2021–2024. Select MAE≤min+0.1→RMSE≤min delpool+0.1→entradaspredictoras0/1/2→orden;constantes0entradas,persistencia primero. Primario global_v6,referenciapersistencia/v3idéntica165llaves/observados;MAEfsum/RMSE/mejora denominadorpositivo finito. No elegir mejorpolítica externa como primario ni otra métrica/corte para declarar éxito.

Ledger NUEVO7200segundos,nohereda/noamplía;serialdurableterminable;arranque/comunicación/constantes/fallos/retries/repeticiones/pausas incluidas.192internos+128externos+hasta8rep=328componentesmáxsinfallos;máx104estimacionesconstantes separadas. Unretry máximo infraestructura;numérico/convergenciainelegible,sinretry;faltacobertura/integridad/timeoutobliga incompleto;pendiente sin medición agotasaldo. Guardar matricesX/y/llaves/d/c/r/inputs/aniosprevios/unidades/defaults/semilla/versiones/scaler/coef/intercept/advertencias/huellas/estados/tiempos/terminación. Selecciones antes externas.12870internasoriginales/156registros/6600externas/5148únicas solo contextoscopiasexactos conlinaje12870y menor externo. Globalsolo mismoIDyventana;5checks previoexacto/recomputaciónconstante/repeticiónfitatol1e-10rtol0. Cerrarpiloto/ledger antes análisis/entrega,no reabrir saldo.

## Fase3 y entrega hoy

Auditorindependiente probado coninventados sinfit;no importarselector/constructores/runnersoperativos ni deserializarmodelospropios/históricos;usarbytes/metadatos/coef/scalerguardados. Cotejar matrices/fechas/scales/defaults/inputs/unidades/constantes/selección/reuso/coverage/copias/linaje/presupuesto/terminación/CSVexacto,intfloat0equivalente,rechazo1e-11. Revalidar referencias v3persistencia/v5global/recenciaglobal mismas165llaves/observados;no evidenciasindependientes. No repetirfits ni usar saldoremanente.

Crear02_resultados_objetivo3.ipynb desdePythoneditable/generadorPython,nbformatvalidado y celdas realmenteejecutadas,sin datos personales. TODAScifras/tablas/figuras nuevas del texto deben originarse en celdas del notebook que llamen funciones compartidas para cálculo/guardado. No llenaroutputsmanuales ni copiarcálculos hechosúnicamente fuera del notebook. GuardarCSV/JSON/PNG con huellas;figuras unidades/n/leyendas y revisiónvisual. Recalcular/cotejar antecedentesnuméricos en notebook antes citarlos:V3MAE3.429267191379531vsV2MAE4.879557188161031/mejora29.721754266970148%;memoriaglobal1.7979745286559843%y políticamemoria12.392390281511053%exploratorio;son antecedentes no conclusionesv6.

EntregarTEXTO_OBJETIVO3_TESIS.md listo para incorporar,notebook,tablas completas,figuras seleccionadas del notebook,informe técnico/registrohallazgos/lecturas/aceptación/conservación/manifiesto/pendientes/continuidad. EVIDENCIAS_TEXTO.csv asocia cadaafirmaciónnumérica a celda/función/archivo/tabla/llave/n/unidad/huella;controlar texto contra salidas y evitarcitasinventadas. Comparaciones poraño/territorio/erroresfirmados/absolutos/sesgo/dirección/nivelvsrezago/regularización/historia/comúncorrección descriptivas.165pares/copiasdependientes,no p-valoresconfirmatorios. Distinguirhistóricos/recálculosactuales/hipótesis;explicar hallazgosimpacto/alternativaverificable/resolución sin rediseñar evaluación.

Informe incluso sin alcanzar5%;siincompleto,salidassolo verificablesysinmeta/síntesis dependiente. No cambiarcriterios nireabrirpiloto para obtener mejores métricas. Fuente local noautenticada,Guainía238vs404/21.012105832431985puntos histórica v2filas57y90,IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocosaños. Todos2021–2025vistos:exploratorio,sin confirmación independiente/causalidad/pronósticoanticipadodemostrado. Aceptacióntécnica noresuelveautenticidad/disponibilidadtemporal. Comprobar último año utilizable y evidencia local de fecha,documentar siguienteañoCONDICIONAL (2026siúltimo2025),sin proyectar ni iniciarobjetivo4. Cerrarcontinuidad/manifiesto/verificaciónenlectura;nootra versión/experimento/avanceautomático.
'''

README='''# V6 — última versión: paquete documental listo para nueva sesión

Esta carpeta conserva preparación/documentos, no resultados ni modelos.39candidatos predefinidos,primario global,meta5%adicional frente persistencia/v3,7200sdepiloto. Cuatrofamilias ajustadas y referenciasconstantes/historia,328componentesmáximosinfallos. Plan para implementación→piloto→auditoría/notebook/texto del objetivo3 en nueva sesión,condicionado a controles válidos.0fitsactuales.

Archivo para enviar íntegro en nueva sesión:PROMPT_NUEVA_SESION_V6.md. La lectura/existencia del prompt no autoriza ejecutarlo. Protocolo:PROTOCOLO_V6.md;contratoJSON:ESPECIFICACION_V6.json;lista: CANDIDATOS.csv;fases:PLAN_V6.md;estado:CONTINUIDAD_V6.md. PreparaciónverificableconPYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python experimento_final_objetivo3_v6/verificar_documental.py. No regenerar crear_paquete.py sobreexistentes.

Entrega futura:02_resultados_objetivo3.ipynbconfuentePython/generador/ejecuciónreal/nbformat y TEXTO_OBJETIVO3_TESIS.md,figuras originadasen notebook y EVIDENCIAS_TEXTO.csv. Usuario necesita entregahoy,horizonteun año;sin proyecciónobjetivo4actual. Informar incluso sinmejora;no promesaéxito. Fuentes/entorno/criterios/herencia/limitaciones íntegros. No instalación/nuevosdatos/commit/push/modelofinal/notebookpersonal/otrasversionesautomáticas.
'''

CONTINUITY='''# Continuidad propia v6 — preparación documental COMPLETA, no piloto

2026-10-11 America/Bogota. Inicio de v6 sincontinuidadprevia:se comenzó coninventario, no se inventóestado anterior. Usuario pidiócrearplan/protocolo/archivos/prompt para ejecución en nuevas sesión. Esta autorización actual es DOCUMENTAL;0fitsreales/inventados/0modeloscargados/0matrices/0notebooks/0ledger/0instalaciones/0fuentesnuevas/0commits/push. Es última versión porusuario.

Usuario:entregaobjetivoshoy,presentacióntesismartes,horizonteun año,7200sajustes,notebookytexto listoparatesis con todos cálculos/figuras desde notebook,sinrequisitosextra director. Acepta5%adicional primario y cierre honesto aunque no mejore;2021–2025vistos exploratorio. Objetivo4aclaradoproyecciónpuntajes,noescenariosintervención;NOejecutar4ahora. Ultimoañoyfecha disponibilidadsecomprobarán localmente,2026solo horizontecondicional siúltimo2025,sin autenticación nueva ni predicción.

Antescrearcarpeta:cerrar_fase4.py --verificar aprobado54huellas/32266protegidos. Originales/cierres/continuidadespreviasintactos segúnPARTIDA/CONSERVACION_DOCUMENTAL. GitHEAD75c3a25182af363f47b0d743820f99084e18fed5/asuntoetapa2v5cerrarpiloto36MAEyauditoriasinmejora/ramacodex/objetivo3-v5-mae/ascendencia/sinposterioresversionados. Históricav5encommitreal109797407d75d2097e5b71f8bcef3fc266bc61d2;temporalsolo textopreservado/huellapartidaetapa2. No actualizarcierresprevios para aceptar nuevasrutas. EntornoPython3.12.14/sklearn1.9.1/54lock/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010yget_params sinfitrevalidados. Fuentesv2/derivadov5 huellascontractuales intactas;sin reauditarraw/disponibilidadoficial.

Antecedentes numéricosguardados,no métricasv6:V3mejora29.721754266970148%frenteV2,MAE3.429267191379531vs4.879557188161031,ganadorpersistencia, no18%niaprendizajeIPM. Fase4memoriaglobal mejora1.7979745286559843%,meta5%no;políticamemoria12.392390281511053%soloexploratorio;11ajustesrezagocoef0,constantehistórica;común/correcciónigualesycorrección0. Tablaevidencia/propuestasfase4justificangrilla final,sinhipótesiscausales.

NUEVAS decisiones técnicodocumentales cerradas ANTESresultadosv6:39IDs/orden/params completos enJSON/CSV;1persistencia,8niveles territoriales median/meanall-last1-last2-last3,12memoriaQRalpha0/.01/.1/1all-last2-last3,6Ridgealpha1/10mismashistorias,2árbolMAEdepth1/2leaf11all,2nivelescomunesall,8QRcomún/comúncorrecciónalpha0/.01/.1/1all.32componentesajustables porcontexto;328cota=192+128+8,7200nuevo;constantesmáx104estimacionesporseparadoen tiempo. Esto es una exploración fijayacotada,noprobar todo ilimitado. Más historia vs reciente/regularización/nivelvsrezago/pérdida son contrastesexploratorios, no garantizarmejora. No nuevasentradas/IPM/código/año;sinrecencia pesos/no futuros.

Contrato conserva población/mediarecibida/geografíacolegio/2018nivel/2019historialno respuesta/2020excluido/dsinanualizar/2021externafija/165pares/igualpeso/meta5%. Respuestas elegiblesconlagdesde2021antes evaluado,luego lastk;mantenerniveles/lag necesario;menosdek usa disponibles;ceroparesrespaldasinfityunopermitido;común1fila/año/territorial33. Mediana parespromediocentrales;meanfsum/n. Nuevaconvenciónempate:constantes0entradaspredictoras aunqueaprendanrespuestas;persistenciaordenprimero. Bandas0.1MAE/RMSE y solo internas intactas;primarioglobal,nunca mejorpolíticaexterna.12870internas/156registros/6600externas/5148únicascondicionales/linaje12870/5checks. No convertirestosnúmeros enresultadosejecutados.

Futuroflujo prompt1→2→3condicionado,presupuesto0iniciadoahora. Generar01controlesy02resultadosdesdefuentePython/generador/nbformat/ejecuciónreal. Todas cifras/gráficas nuevasdeltextoTESISdesde notebook/celdasfunciones,guardadospilotoentradas,antecedentesnuméricosrecálculonotebook antescitar. EVIDENCIAS_TEXTO.csv/localizaciones/QAfiguras/entregainclusosinmejora. Auditoriindependientesinimportsoperativos/deserialización/fit. Ledger cerrado nocache/no saldoheredado/no reabrir. Si fallaindispensable,incompletohonesto. Preparación/documentaciónnoeficaciademostrada ni freezeoperativo.

Pendientes:envíohumanoPROMPT_NUEVA_SESION_V6.md;implementación/control/freeze/piloto/auditor/notebook/texto/cierre. No decisionescientíficasfaltantes para diseñargrilla;faltasentorno/realesdisponibilidad o materialfuera contrato requierenconsultasininstalar/sustituir. Científicosactivos autenticidad/disponibilidad/confirmación/aporterezago;procedencia local,Guainía238vs404/21.012105832431985puntosv2filas57y90,IPMhogares-alumnos,colegio-residencia,ecología/dependencia/pocosaños. No reabrirantecedentesarchivadossin nuevaevidencia;aceptacióntécnicanosustituyeconfirmación.

Verificarpaqueteconverificar_documental.py enlectura;noejecutarcrear_paquete.pydenuevo.No ejecuciónautomática porpromptguardado,noobjetivo4/modelofinal/otra versión/simulación/instalación/commit/push.
'''

DECISIONS='''# Decisiones, hallazgos y justificación antes de resultadosv6

| Autoridad/ID | Evidencia y decisión | Impacto | Alternativa/resolución |
|---|---|---|---|
| UsuarioU1 | Conversación:entrega hoy/presentaciónmartes;últimoexperimento7200s;horizonte1año | Acotar esfuerzo y cerrar incluso sinmejora. | Grilla39fija,prompt de flujo completo condicionado;nootra versión. |
| UsuarioU2 | Notebook/texto para tesis,figuras/cálculos desde notebook | Trazabilidad requerida,evitar cifras inventadas. | Notebookejecutado genera salidas/EVIDENCIAS_TEXTO;QA/cotejo. |
| UsuarioU3 | Acepta meta5%adicional,primario sin rescate | No redefinir éxito. | Seleccióninterna/persistenciav3referencia,cierre honesto. |
| ComprobaciónC1 | v3/etapa2/resultados/meta.json:29.721754266970148%frentev2,MAE3.429267191379531 | Aclarar referencia histórica,no18%;ganadorpersistencia. | Notebookfuturo coteja mismas165llaves/observados;no reproducirfits históricos. |
| ComprobaciónC2 | fase4memoria/tablas/coeficientes_todos_41.csv yPROPUESTAS_FUTURAS.md:rezago0/nivelconstante | Buena memoriadiagnóstica no acredita dinámica. | Constantes matchedhistory/QRregularizacióncoarse/lag,Ridge yárbol acotado. Preguntaspendientes,resueltas en diseño no eneficacia. |
| ComprobaciónC3 | fase4memoria/tablas/decisiones_internas.csv:pools2022–2025 | Ventaja externa posterior no seleccionable anticipadamente. | Conservarselector/bandas;lastk afecta entrenamientodelcandidato,no selector retrospectivo. |
| NuevaN1 |39candidatos/32componentes,cota328+104estimaciones | Buscar mejora sinbúsquedaabierta,viablecontractualmente7200noETAgarantizada. | Identificarfamilias/params y detener porledger,no ampliar grilla. |
| NuevaN2 |Constantes tienen0Xpredictoras/medianparpromedio centrales/2019norespuesta | Evitar equivalencias confundidas concoef0historico yventaja de datosdistintos. | Mismorespuestahistorialagadecuada/ordenpersistenciaprimero,beforev6. |
| NuevaN3 |Último2025esperado;fecha disponibilidadnoautenticada |2026no proyecciónoperativademostrada. | Verificaciónlocal/documental futura,horizontecondicional,sinobjetivo4actual/nuevasfuentes. |

La configuracióndegrilla es nueva,no heredada de fases cerradas. Su amplitud respondesolicitudhumana pero no representa agotamiento de todos algoritmos/hiperparámetros. No resultadosv6consultados;0fits/0métricasv6. Defaults completos sinfit/versionesobservadas enENTORNO_DOCUMENTAL,losintervalos sonfijos justificados como contrastes gruesos, no valoresóptimos. Protocolopuede cerrarseahora;suimplementación válida/capacidadpredictiva requieren fases futuras.

Advertencias activas:procedencia/temporalidad/ecología/dependencia/pocos años/todos2021–2025vistos. Archivadosanteriores no reabiertossin informaciónnueva. Plazo no elimina estoscontroles. Cada fase futura actualizará hallazgos/impacto/alternativa/resoluciónycontinuidadpropia.
'''

if __name__=='__main__': main()
