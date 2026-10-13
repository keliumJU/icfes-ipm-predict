"""Cierre verificable de fase1 documental. No fit ni congelación operativa.
Revalida conservación y huellas después de generación, sin modificar antecedentes.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import csv
import os
from verificar_documental import ROOT, OUT, info, equal, git

def read(name): return json.loads((OUT/name).read_text())
def write(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def conservation():
    prep=read('REGISTRO_PREPARACION.json')
    differences=[]
    for name,expected in prep['inventario_protegido'].items():
        try:
            if not equal(expected,info(name)): differences.append(name)
        except (OSError,FileNotFoundError): differences.append(name)
    tracked=git('ls-files','-z').decode().split('\0')[:-1]
    others=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    new_outside=[p for p in others if not p.startswith(OUT.name+'/') and p not in prep['inventario_protegido']]
    preserved={p:sha(OUT/'antecedentes_preparacion'/p)==prep['huellas_propias'][p] for p in ['CONTINUIDAD_DISENO.md','README.md']}
    unchanged={p:sha(OUT/p)==prep['huellas_propias'][p] for p in ['PLAN_FASES.md','PROMPT_FASE1_DISENO.md']}
    head=git('rev-parse','HEAD').decode().strip()
    diff=git('diff','--name-only','HEAD').decode().splitlines()
    own_symlinks=[str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_symlink()]
    ok=not differences and not new_outside and tracked==prep['versionados'] and not diff and all(preserved.values()) and all(unchanged.values()) and head==read('PREFLIGHT_FASE1.json')['git']['head'] and not own_symlinks
    return {'aprobado':ok,'inventario_base':'REGISTRO_PREPARACION.json:inventario_protegido','protegidos':len(prep['inventario_protegido']),'versionados':len(tracked),'lista_versionados_identica':tracked==prep['versionados'],'diferencias_antecedentes':differences,'ajenos_nuevos':new_outside,'diff_versionados':diff,'git_head_igual':head==read('PREFLIGHT_FASE1.json')['git']['head'],'originales_propios_preservados':preserved,'plan_prompt_intactos':unchanged,'symlinks_propios':own_symlinks,'alcance':'Solo archivos propios nuevos/README y continuidad actualizados; originales íntegros archivados. Raw ignorado sin lectura/censo/escritura. Sin reset/checkout/commit/push.'}

def main():
    assert os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'
    spec=read('ESPECIFICACION_DOCUMENTAL.json')
    conf=json.loads((ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json').read_text())
    trace=list(csv.DictReader((OUT/'TRAZABILIDAD_TEMPORAL.csv').open()))
    hist_commit='109797407d75d2097e5b71f8bcef3fc266bc61d2'
    hist_ancestor=subprocess.run(['git','merge-base','--is-ancestor',hist_commit,'HEAD'],cwd=ROOT).returncode==0
    # Auditoría documental independiente de fórmulas de conteo en el generador.
    controls={
        'preflight_antecedentes':read('PREFLIGHT_FASE1.json')['aprobado'],
        'continuidad_historica_commit_ancestro':hist_ancestor,
        'entorno_exacto_y_defaults':read('ENTORNO_FASE1.json')['aprobado'] and spec['pipeline_componentes']['defaults_completos']==read('ENTORNO_FASE1.json')['defaults'],
        'semantica_completa_y_referencias':read('SEMANTICA_FASE1.json')['aprobado'],
        'cuatro_candidatos_orden_entradas':[(c['id'],c['orden'],c['n_entradas_derivadas']) for c in spec['candidatos']]==[('persistencia',0,0),('memoria',1,1),('comun',2,1),('comun_correccion',3,2)],
        'particiones_heredadas_exactas':spec['ventanas']==conf['ventanas'],
        'trazabilidad_5externas_10internas':len(trace)==15 and sum(x['tipo']=='externa' for x in trace)==5 and sum(x['tipo']=='interna' for x in trace)==10,
        '2019_no_respuesta_y_2021_cero_pares':all('2019' not in row['respuestas_supervisadas'].split(';') for row in trace) and all(row['anios_pares_completos']=='0' for row in trace if row['evaluado']=='2021'),
        'unidades_comunes_territoriales':all(int(row['filas_comun'])==int(row['anios_pares_completos']) and int(row['filas_memoria_correccion'])==33*int(row['anios_pares_completos']) for row in trace),
        'objetivo_meta_pesos':spec['evaluacion']['n']==165 and spec['evaluacion']['externos']==list(range(2021,2026)) and '>=5' in spec['evaluacion']['meta'] and spec['pipeline_componentes']['recencia'] is False,
        'no_congelacion_no_fits':spec['fase2_autorizada'] is False and spec['fits_ejecutados']==0 and spec['modelos_cargados']==0,
        'prompts_independientes_condicionados':all('Condición indispensable' in (OUT/p).read_text() and 'envía expresamente' in (OUT/p).read_text() for p in ['PROMPT_FASE2_IMPLEMENTACION.md','PROMPT_FASE3_PILOTO.md','PROMPT_FASE4_AUDITORIA.md']),
        'advertencias_completas':len(spec['advertencias'])==7,
        'sin_notebooks_modelos_ledger':not any(p.suffix in ['.ipynb','.joblib','.pkl'] or p.name=='ledger.json' for p in OUT.rglob('*')),
    }
    audit={'aprobado':all(controls.values()),'controles_documentales':controls,'controles_operativos':'No ejecutados ni aprobados: rezagos/mutación/fits inventados/selección/runner/ledger/CSV adversarial pendientes fase2; documentación no sustituye pruebas.','conteos_documentales':{'internas':4*10*33,'registros':4*4,'externas':5*165,'unicas_condicionadas':4*4*33,'fits_internos':4*(3+2+1),'fits_externos':4*4,'repeticiones_max':3*2},'expectativas_no_resultados':True}
    write('AUDITORIA_DOCUMENTAL_FASE1.json',audit)
    conserved=conservation();write('CONSERVACION_FASE1.json',conserved)
    approved=all(controls.values()) and conserved['aprobado']
    assert approved, 'Fase1 incompleta, revisar controles documentales/conservación'
    write('REGISTRO_FASE1.json',{'version':'1.0.0','fecha_cliente':'2026-10-11','timezone':'America/Bogota','autorizacion':'Usuario envió expresamente promptfase1: exclusivamente diseño documental. No autoriza fases2–4.','estado':'fase1 documental completa','git':read('PREFLIGHT_FASE1.json')['git'],'comprobaciones':['Entorno exacto antes de semántica','9manifiestos íntegros; continuidadv5etapa1 en commitreal y temporal anterior preservada','Fuente/derivado bytes y todos campos exactos','Tres referencias165llaves/observados/predicciones exactas','Defaults get_params sin fits','Protocolos/prompts/decisiones/traza y cierre propios'],'ejecucion':['Verificación entorno con PYTHONDONTWRITEBYTECODE=1; pipcheck/metadata/get_params, sin fit','verificar_documental.py: primera corrida KeyError sha256_texto_enlace; corregida, segunda aprobada','verificar_semantica.py: primera corrida códigos sin zfill; corregida según contrato histórico, segunda aprobada','generar_documentacion.py: documentos generados sin ajustes','cerrar_documentacion.py: conservación y auditoría documental'], 'runtime':'/tmp/icfes-v2-fase2-venv/bin/python','semilla':20261010,'aleatoriedad':False,'incidencias':'REGISTRO_HALLAZGOS.md:Incidencias propias; plan completo leído por error y consultas truncadas corregidas; errores de verificadores sin cambios en datos. Pipcheck0 con aviso de caché no escribible, sin instalación ni fallo de dependencias.','distinciones':{'aprobacion':'Solo realizar fase1 y acuerdos enviados, no aceptación operativa ni ejecución futura','resultados':'MAE histórico citado; cotejos estructurales actuales, ninguna nueva evaluación','hipotesis':'Eficacia memoria/común/corrección pendiente','congelacion':'No realizada, pendiente fase2 autorizada'},'contadores':{k:0 for k in ['fits_reales','fits_inventados','modelos_cargados','notebooks','ledger_operativo','instalaciones','descargas','fuentes_extra','commit','push','pdf_paginas','web','metricas_nuevas']},'conservacion':{'aprobada':conserved['aprobado'],'protegidos':conserved['protegidos'],'versionados':conserved['versionados']},'pendientes':['Aprobación del diseño y envío expreso promptfase2','Implementación/controles/congelación operativa futuros','Piloto y auditoría bajo autorizaciones separadas','Eficacia hipótesis/confirmación independiente/procedencia oficial/disponibilidad real no resueltas']})
    write('ACEPTACION_FASE1.json',{'version':'1.0.0','completa_documental':approved,'aceptacion_documental':'Criterios del encargo fase1 cotejados por auditoría documental, no aprobación operativa del usuario','controles':controls,'conservacion_aprobada':conserved['aprobado'],'especificacion':'ESPECIFICACION_DOCUMENTAL.json','protocolo':'PROTOCOLO_FASE1.md','traza':'TRAZABILIDAD_TEMPORAL.csv','prompts_preparados':[2,3,4],'fits':0,'congelacion_operativa':False,'fase2_autorizada':False,'pendientes_indispensables_fase1':[],'pendiente_aprobacion_usuario':'Diseño para revisión y autorización separada de fase2; no bloquea entrega documental','pendientes_futuros':['Controles ejecutables fase2','Piloto fase3','Auditoría fase4','Confirmación científica y disponibilidad fuera alcance']})
    continuity='''# Continuidad diseño memoria/común — fase1 documental completa

2026-10-11 America/Bogota. Usuario envió expresamente PROMPT_FASE1_DISENO: autoriza SOLOfase1. Preparación anterior íntegra en antecedentes_preparacion/CONTINUIDAD_DISENO.md y README.md, con huellas originales del REGISTRO_PREPARACION.json. No se inventan fases anteriores. Fases2–4 no autorizadas ni ejecutadas. Fitsreales0/inventados0/modeloscargados0/notebooks0/ledgeroperativo0/instalaciones0/descargas0/fuentesextra0/commit0/push0. No congelación operativa.

## Partida y verificaciones actuales

HEAD75c3a25182af363f47b0d743820f99084e18fed5, asunto `etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora`, ramacodex/objetivo3-v5-mae; ascendencia/sin trabajo posterior comprobados. Sin reset/checkout/sobrescritura ajena. Conservación30980antecedentes/29640versionados íntegra al inicio y cierre; sin cambios fuera diseño, raw ignorado sin lectura/censo/escritura. Nueve manifiestos cotejados completos por bytes/links. Continuidad histórica v5etapa1 solo Git109797407d75d2097e5b71f8bcef3fc266bc61d2, SHA33bbdce75635733eae8bad9e14d1900999fd8af6318a55842382b5d2544e13fd, ancestro real. Temporaletapa1 usa versión preservada etapa2/resultados/partida.json:continuidad_inicial y SHAfd3b963135e9e8233470ef36116d82e67ca4a88aae67b7c785d0a9185ba0b8bb. Sin alterar etapa1 ni otras excepciones. PREFLIGHT_FASE1/CONSERVACION_FASE1 contienen procedimientos y evidencia.

Entorno revalidado ANTES semántica: /tmp/icfes-v2-fase2-venv/bin/python, Python3.12.14/sklearn1.9.1/54paqueteslock exactos/pipcheck0/PYTHONDONTWRITEBYTECODE=1/semilla contractual20261010, sin operación aleatoria. Pip aviso caché no escribible sin fallo ni instalaciones. ENTORNO_FASE1 tiene lock/defaults completos obtenidos sin fit. Falta/diferencia futura exige detener/documentar/consultar sin sustitución.

Fuentev2 SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5 SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc revalidados. Cotejo actual completo por bloques1024/reconstrucción en memoria de TODOScampos exactos, códigoszfill2contractual:231filas/33territorios/198cambios, sin escribir datos nuevos. Referencias v5global/v3persistencia/recenciaglobal exactas en165llaves/observados/predicciones; no evidencia independiente ni nueva métrica. SEMANTICA_FASE1 y verificar_semantica.py.

## Decisiones documentales y autoridad

Usuario confirmó panel actual primero/modelos ajustados/permitir1año completo/objetivo original/particiones165pares/meta5%/igualpesoterritorio-año; envío actual autoriza formalizaciónfase1. Cuatro candidatos persistencia/memoria/común/común+corrección. d cambio original sin anualizar, c mediana33auxiliar no nueva media nacional, r=d−c. Común1fila/año; territoriales33filas/año; corrección parámetros compartidos sin efectos por código. StandardScaler(copy=True,with_mean=True,with_std=True)→QuantileRegressor(quantile0.5,alpha1.0,fit_interceptTrue,solverhighs,solver_optionsNone), sin recencia/sample_weight/búsquedas. Alpha fijo propuesto no optimizado; defaults actuales verificados. Entradas año/código/IPM/tasas/conteos/intervalo excluidas. Sin clipping/imputación/calibración.

PoblaciónESTUDIANTE/no libertadS/grado11/seis puntajespositivos presentes/sincalendario/media globalrecibida/geografía colegio; conteos solo trazabilidad.2020excluido/2018nivelhistorial/2021previo2019intervalo2sinanualizar.2019d historial sin respuesta supervisada por faltar d2018. Ceroañoscompletos implica respaldo explícito sin fit;1permite ajuste futuro, común principalmente nivel con una fila (fragilidad advertida). Incompletos inesperados/no finitos detienen integridad, no respaldo silencioso.2021externofijo sinselección; internas2021sípuntuar respaldos futuros. TRAZABILIDAD_TEMPORAL15filas:5externas+10internas, fechas/respuestas/rezagos/unidades.

Nuevas decisiones DOCUMENTALES: IDs/orden, fallo por integridad, serialización/aceptación/trazabilidad. No atribuir aprobación operativa posterior. Primario global con selección únicamente interna/bandasMAE yRMSE0.1/entradas0,1,1,2/orden; políticas individuales diagnósticas, no rescate. Presupuesto7200nuevo/cota46=24+16+máximo6,1320internas/16registros/825externas/528únicas condicionadas son expectativas, no ejecuciones ni ledger. No compartir fit entre ventanas/candidatos; global solo misma salida candidato/ventana. No variar criterio tras resultados. Especificación/protocolo§§1–7/decisiones registran autoridad y evidencia.

## Hallazgos e impacto

Resultado HISTÓRICO recencia/globalMAE3.429267191379531/mejora0%/meta no satisfecha, según temporaletapa2/resultados/meta.json, sin nuevos fits o evaluación. Impacto: falta punto de partida mejor demostrado. Alternativa: contraste memoria/común/corrección con primario fijo; resuelto documentalmente, eficacia pendiente.2019no respuesta/1fila común/referencias compartidas/2021–2025vistos limitan entrenamiento e interpretación; soluciones contractuales en REGISTRO_HALLAZGOS/protocolo. No ampliar fuentes o cambiar criterios para lograr mejora.

Guainía238vs404/diferencia21.012105832431985puntos, HISTÓRICO v2/fase1/resultados/diagnostico_medias_disponibles.csv:filas57y90,código94/2025; media recibida intacta. Procedencia local no autenticada/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años. Todos2021–2025vistos:EXPLORATORIO,sin confirmación independiente/causalidad/pronóstico anticipado demostrado. Fuentes oficiales/fechas/disponibilidad no autenticadas por SHA. Antecedentes archivados ausenciaentorno diagnóstico/helper temporal resueltos no reabiertos; científicos activos no cerrados por aceptación documental.

Incidencias propias: lectura inicial plan completo contraria al alcance solicitado, sin ejecutar fases; salidas extensas truncadas corregidas por código completo/resúmenes acotados; KeyError campo SHA de enlace corregido sin seguirlo; códigos sin zfill corregidos por regla histórica sin cambiar bytes. Corridas finales aprobadas. No errores históricos nuevos ni datos alterados. LECTURAS_FASE1 delimita revisado/pendiente, PDF0páginas/web0.

## Entregables, cierre y siguiente sesión

README/PROTOCOLO_FASE1/ESPECIFICACION_DOCUMENTAL/DECISIONES_FASE1/TRAZABILIDAD_TEMPORAL/TRAZABILIDAD_DOCUMENTAL/LECTURAS_FASE1/REGISTRO_HALLAZGOS/REGISTRO_FASE1/PREFLIGHT/ENTORNO/SEMANTICA/AUDITORIA_DOCUMENTAL/ACEPTACION/CONSERVACION/MANIFIESTO propios; scripts editables de cotejo/documentación/cierre, no implementación de modelos. Prompts independientes2IMPLEMENTACION/3PILOTO/4AUDITORIA preparados y condicionados. Continuidad/README preparación archivados íntegros; plan/prompt1/registro inicial intactos. ACEPTACION_FASE1:completa_documentalTrue; pendientes indispensablesfase1ninguno. MANIFIESTO_FASE1 cubre entregables por SHA con exclusión explícita de sí mismo, verificado después de escritura en VERIFICACION_MANIFIESTO_FASE1.json (también excluida para evitar ciclo).

Pendientes: aprobación del diseño y envío expreso PROMPT_FASE2_IMPLEMENTACION. Fase2 deberá revalidar diseño/anterior/Git/entorno/fuentes; implementar y probar SOLOpropios, notebook controles desde Python+generador validado, congelar antes fits reales; no iniciar piloto automáticamente. Fase3y4 requieren sus prompts y anterior válida. No ejecutar scripts/instalar automáticamente al retomar. Eficacia/confirmación independiente/procedencia/disponibilidad requieren trabajo autorizado separado. Sin etapa3v5/notebookpersonal/simulación/objetivo4/ajustefinal/fuentesextra/commit/push/avanceauto.
'''
    (OUT/'CONTINUIDAD_DISENO.md').write_text(continuity)
    # Comprobar nuevamente después de actualizar continuidad propia.
    write('CONSERVACION_FASE1.json',conservation())
    mapping={str(p.relative_to(OUT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in ['MANIFIESTO_FASE1.json','VERIFICACION_MANIFIESTO_FASE1.json']}
    write('MANIFIESTO_FASE1.json',{'version':'1.0.0','completa_documental':True,'congelacion_operativa':False,'fase2_autorizada':False,'fits':0,'entregables_sha256':mapping,'base_rutas':'diseno_memoria_comun_objetivo3_v1/','exclusiones_autorreferencia':['MANIFIESTO_FASE1.json','VERIFICACION_MANIFIESTO_FASE1.json'],'pendientes_indispensables':[],'advertencia':'Huellas documentales no congelación ni aprobación del usuario para fases futuras.'})
    m=read('MANIFIESTO_FASE1.json')
    actual_files={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file() and p.name not in m['exclusiones_autorreferencia']}
    errors=[p for p,h in m['entregables_sha256'].items() if sha(OUT/p)!=h]
    write('VERIFICACION_MANIFIESTO_FASE1.json',{'aprobado':not errors and actual_files==set(mapping) and read('CONSERVACION_FASE1.json')['aprobado'],'manifiesto_sha256':sha(OUT/'MANIFIESTO_FASE1.json'),'huellas_verificadas':len(mapping),'cobertura_exacta':actual_files==set(mapping),'diferencias':errors,'exclusiones_justificadas':'Manifiesto y su verificación para evitar ciclo; verificación guarda SHA del manifiesto. Sin archivos de modelos/notebooks/ledger.'})
    print(json.dumps({'completa_documental':True,'entregables_con_huella':len(mapping),'conservacion':read('CONSERVACION_FASE1.json')['aprobado'],'manifiesto_verificado':read('VERIFICACION_MANIFIESTO_FASE1.json')['aprobado'],'fits':0,'fase2_autorizada':False}))

if __name__=='__main__':main()
