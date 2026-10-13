"""Cierre independiente fase2 y verificación en lectura de sus huellas."""
from pathlib import Path
import json
import os
import sys
import subprocess
import importlib.metadata as metadata
import nbformat
from preflight import ROOT,OUT,EXP,DESIGN,BASE,sha,load,write,git,info,equivalent
from integridad import digest

def conservation():
    partida=load(OUT/'PARTIDA_FASE2.json')
    bad=[]
    for p,e in partida['inventario_protegido'].items():
        try:
            if not equivalent(e,info(p)): bad.append(p)
        except OSError: bad.append(p)
    tracked=git('ls-files','-z').decode().split('\0')[:-1]
    untracked=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    foreign=[p for p in untracked if not p.startswith(EXP.name+'/') and p not in partida['inventario_protegido']]
    head=git('rev-parse','HEAD').decode().strip()
    diff=git('diff','--name-only','HEAD').decode().splitlines()
    ok=not bad and not foreign and not diff and tracked==partida['versionados'] and head==partida['git_head']
    return {'aprobado':ok,'protegidos':len(partida['inventario_protegido']),'versionados':len(tracked),
            'diferencias':bad,'ajenos_nuevos':foreign,'git_diff':diff,'head_intacto':head==partida['git_head'],
            'raw':'Ignorado sin lectura/censo/escritura','alcance':'Solo etapa1 propia y continuidad experimental nueva; sin reset/checkout/commit/push'}

def own_inventory(excluded=()):
    result={}
    for folder,dirs,files in os.walk(EXP,followlinks=False):
        for name in sorted(files+[d for d in dirs if (Path(folder)/d).is_symlink()]):
            p=Path(folder)/name
            rel=p.relative_to(EXP).as_posix()
            if rel not in excluded:
                result[rel]=info(p.relative_to(ROOT).as_posix())
    return result

def environment_readonly():
    e=load(OUT/'ENTORNO_FASE2.json')
    actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in metadata.distributions()}
    pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
    return (sys.version_info[:3]==(3,12,14) and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'
            and {k:v for k,v in actual.items() if k!='pip'}==e['lock'] and pip.returncode==0 and e['aprobado'])

def verify_mapping(mapping,base):
    errors=[]
    for p,e in mapping.items():
        try:
            if not equivalent(e,info((base/p).relative_to(ROOT).as_posix())): errors.append(p)
        except OSError: errors.append(p)
    return errors

def verify():
    manifest=load(OUT/'MANIFIESTO_FASE2.json')
    freeze=load(OUT/'CONGELACION_FASE2.json')
    acceptance=load(OUT/'ACEPTACION_FASE2.json')
    errors=verify_mapping(manifest['entregables'],EXP)
    freeze_errors=verify_mapping(freeze['implementacion'],OUT)
    contract_errors=[p for p,h in freeze['documentos_base'].items() if info(p)['sha256']!=h]
    current=own_inventory(manifest['exclusiones_autorreferencia'])
    missing_extra=sorted(set(current)^set(manifest['entregables']))
    conserved=conservation()
    ok=(not errors and not freeze_errors and not contract_errors and not missing_extra and conserved['aprobado']
        and environment_readonly() and acceptance['completa'] and acceptance['congelacion_sha256']==digest(OUT/'CONGELACION_FASE2.json'))
    result={'aprobado':ok,'huellas':len(manifest['entregables']),'diferencias':errors,
            'congelacion_diferencias':freeze_errors,'contrato_diferencias':contract_errors,
            'lista_entregables_diferencias':missing_extra,'conservacion':conserved,'modo':'lectura, sin nuevas pruebas/fits/escrituras'}
    print(json.dumps(result,ensure_ascii=False))
    if not ok: raise RuntimeError('Cierre no válido')
    return result

def close():
    if (OUT/'MANIFIESTO_FASE2.json').exists(): raise RuntimeError('Cierre existente; usar --verificar y preservar')
    envok=environment_readonly()
    conserved=conservation(); write(OUT/'CONSERVACION_FASE2.json',conserved)
    preflight=load(OUT/'PREFLIGHT_FASE2.json')
    cli_files=sorted((OUT/'resultados').glob('CONTROLES_cli_*.json'))
    cli_path=cli_files[-1]; cli=load(cli_path)
    note=load(OUT/'ACEPTACION_NOTEBOOK.json'); nb_report_path=OUT/note['controles']; nb_report=load(nb_report_path)
    reports=[cli,nb_report]
    sourceok=all(digest(OUT/p)==h for rep in reports for p,h in rep['huellas_fuentes'].items())
    nb=nbformat.read(OUT/'01_controles.ipynb',as_version=4); nbformat.validate(nb)
    nbok=(note['aprobado'] and note['notebook_sha256']==digest(OUT/'01_controles.ipynb')
          and note['fuente_sha256']==digest(OUT/'notebook_controles.py') and note['generador_sha256']==digest(OUT/'generar_notebook.py')
          and [c.execution_count for c in nb.cells if c.cell_type=='code']==[1,2,3]
          and all(c.outputs for c in nb.cells if c.cell_type=='code'))
    design_manifest=load(DESIGN/'MANIFIESTO_FASE1.json')
    designok=all(digest(DESIGN/p)==h for p,h in design_manifest['entregables_sha256'].items())
    controls={'fase1_valida_y_conservada':preflight['aprobado'] and designok,'entorno_exacto':envok,
        'suite_cli_valida':cli['aprobado'],'suite_notebook_valida':nb_report['aprobado'],
        'fuentes_probadas_identicas':sourceok,'notebook_validado_ejecutado':nbok,
        'conservacion_integra':conserved['aprobado'],'fits_panel_real_cero':all(r['fits_panel_real']==0 for r in reports)}
    complete=all(controls.values())
    all_reports=[load(p) for p in sorted((OUT/'resultados').glob('CONTROLES_*.json'))]
    fits=sum(r['fits_inventados'] for r in all_reports)
    pending=[k for k,v in controls.items() if not v]
    acceptance={'version':'1.0.0','completa':complete,'congelacion_valida':False,'controles':controls,
        'pendientes_indispensables':pending,'fits_inventados_total_corridas':fits,'fits_panel_real':0,
        'modelos_cargados':0,'presupuesto_real_iniciado':False,'fase3_autorizada':False,
        'corrida_cli_final':str(cli_path.relative_to(OUT)),'corrida_notebook':note['controles'],
        'criterio':'Implementación y controles inventados, no evaluación de eficacia ni aprobación de piloto'}
    if complete:
        from motor import CANDIDATES,INPUTS,COMPONENTS,SCALER,REGRESSOR,FUTURE_CONTRACT
        tested=[p for p in OUT.glob('*.py')]+[OUT/'01_controles.ipynb',OUT/'ACEPTACION_NOTEBOOK.json',OUT/'ENTORNO_FASE2.json',cli_path,nb_report_path]
        freeze={'version':'1.0.0','valida':True,'fecha_cliente':'2026-10-11','timezone':'America/Bogota',
            'antes_de_fits_reales':True,'fits_panel_real':0,'presupuesto_real_iniciado':False,
            'candidatos':[{'id':c,'orden':i,'entradas':INPUTS[i],'componentes':COMPONENTS[i]} for i,c in enumerate(CANDIDATES)],
            'defaults':{'StandardScaler':SCALER,'QuantileRegressor':REGRESSOR},'semilla':20261010,
            'contrato_futuro':FUTURE_CONTRACT,'reglas':'PROTOCOLO_IMPLEMENTACION.md y diseño documental sin cambios',
            'implementacion':{p.relative_to(OUT).as_posix():info(p.relative_to(ROOT).as_posix()) for p in tested+[OUT/'PROTOCOLO_IMPLEMENTACION.md']},
            'documentos_base':{(DESIGN/p).relative_to(ROOT).as_posix():digest(DESIGN/p) for p in ('MANIFIESTO_FASE1.json','ACEPTACION_FASE1.json','PROTOCOLO_FASE1.md','ESPECIFICACION_DOCUMENTAL.json','ENTORNO_FASE1.json')},
            'fuentes_panel_solo_identidad':{p:v['esperado'] for p,v in load(DESIGN/'ESPECIFICACION_DOCUMENTAL.json')['fuentes'].items()},
            'aceptacion_controles':controls,'no_autoriza':'Piloto/fits reales/modelo final/simulación/objetivo4'}
        write(OUT/'CONGELACION_FASE2.json',freeze)
        acceptance.update(congelacion_valida=True,congelacion_sha256=digest(OUT/'CONGELACION_FASE2.json'))
    write(OUT/'ACEPTACION_FASE2.json',acceptance)
    write(OUT/'LECTURAS_FASE2.json',{'revisado':{
        'AGENTS.md':'completo','diseno_memoria_comun_objetivo3_v1/CONTINUIDAD_DISENO.md':'vigente completo',
        'diseno_memoria_comun_objetivo3_v1/PLAN_FASES.md':'apertura inicial completa por incidencia; aplicación solo decisiones comunes y fase2',
        'diseno_memoria_comun_objetivo3_v1/PROTOCOLO_FASE1.md':'§§1–7 completo','diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json':'completa',
        'diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md':'vigente líneas1–110; antecedentes no atribuidos',
        'experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md':'vigente completo',
        'experimentos_objetivo3_v5/CONTINUIDAD_V5.md':'vigente líneas1–98; huella histórica en commit real',
        'fase1_manifiesto_aceptacion_entorno_conservacion_preflight':'completos',
        'fuentes_v2_derivado_v5':'SHA completo, sin matrices reales; cabecera y primera fila derivado inspeccionadas, no nuevo análisis',
        'nueve_manifiestos':'bytes/enlaces completos, sin cargar modelos','continuidad_temporal_etapa1':'solo texto preservado+huella partida etapa2'},
        'pendiente':'Análisis de eficacia, piloto y auditoría fase3/4; PDF no requeridos aquí',
        'PDF_paginas':0,'web_fuentes':0,'incidencias':['Lectura inicial plan completo fuera límite; sin ejecución de otras fases','Consulta conjunta continuidades truncada corregida con rangos acotados']})
    status='COMPLETA Y CONGELADA' if complete else 'INCOMPLETA; CONGELACIÓN NO VÁLIDA'
    (OUT/'README.md').write_text(f'''# Fase2 — {status}

Implementación separada de cuatro candidatos; datos y fits exclusivamente inventados. Cero fits del panel, modelos históricos cargados, ledger real, commit o push.

Entorno exacto y fase1 revalidados en PREFLIGHT_FASE2.json y ENTORNO_FASE2.json. {conserved['protegidos']} antecedentes / {conserved['versionados']} versionados conservados. Suite final: {cli['grupos']} grupos, {cli['controles_negativos']} rechazos; notebook3celdas ejecutadas/nbformat válido. Cada suite realiza {cli['fits_inventados']} fits inventados; total de corridas preservadas {fits}. Ensayo inicial fallido intacto, no acreditado como aceptación.

Orden y reglas en PROTOCOLO_IMPLEMENTACION.md. Fuentes: motor.py, integridad.py, ejecucion_sintetica.py, worker_inventado.py, controles.py. Notebook editable notebook_controles.py + generar_notebook.py → 01_controles.ipynb. Pruebas y estados SOLO resultados/sinteticos. Documentación del diseño intacta; congelación propia en CONGELACION_FASE2.json, aceptación independiente y manifiesto completo.

Verificar en lectura con PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python experimentos_memoria_comun_objetivo3_v1/etapa1/cerrar.py --verificar. No repetir el cierre ni sobrescribir entregables. La continuidad está en la raíz experimental. Fase3 requiere prompt expreso y validación anterior, sin avance automático. La cota46/7200s es contrato futuro, sin saldo heredado.

Todo2021–2025 visto: exploratorio sin confirmación independiente/causalidad; procedencia local, Guainía, IPM hogares-alumnos, colegio-residencia, ecología, dependencia y pocos años vigentes. La aceptación técnica no demuestra mejora ni cierra limitaciones científicas.
''')
    (EXP/'CONTINUIDAD_EXPERIMENTAL.md').write_text(f'''# Continuidad experimental memoria/común — fase2 {status}

2026-10-11 America/Bogota. Primera sesión experimental propia; continuidad previa inexistente, no se inventa estado anterior. Usuario envió prompt fase2 y aprobó diseño. No autoriza piloto ni fits reales. Escrituras únicamente etapa1 propia y esta continuidad nueva.

HEAD {BASE}, asunto `etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora`, rama codex/objetivo3-v5-mae, ascendencia/sin trabajo posterior comprobados en PREFLIGHT_FASE2. Históricav5etapa1 cotejada en commit109797407d75d2097e5b71f8bcef3fc266bc61d2; temporaletapa1 solo continuidad preservada y SHA en etapa2/resultados/partida.json, intacta. Nueve manifiestos históricos y28huellas fase1 válidos. PARTIDA_FASE2 tiene snapshot{conserved['protegidos']}, incluidos{conserved['versionados']}versionados; CONSERVACION_FASE2 íntegra. Raw ignorado sin lectura/censo/escritura. Sin reset/checkout/commit/push.

Python3.12.14/sklearn1.9.1/54lock/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010 verificados antes fits inventados. Ruta /tmp/icfes-v2-fase2-venv/bin/python. Ausencia/diferencia futura: detener/documentar/consultar sin sustituir ni instalar. Fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc cotejados por bytes; sin cálculos/fits reales actuales.

Decisiones usuario y documental aprobada conservadas: población ESTUDIANTE/no libertadS/grado11/seis puntajes positivos presentes/sin calendario/media recibida/geografía colegio/2020excluido/2018nivel histórico/d sin anualizar/2021externafija/165pares/meta5%/igualpeso.2019historial sin respuesta conlag inexistente. Cuatro candidatos0..3 persistencia/memoria/comun/comun_correccion, entradas0,1,1,2, parámetros compartidos sin efectos por código. Común1fila/año, territoriales33; cero pares respaldo sin scaler/fit, uno permitido. StandardScaler→QuantileRegressor0.5/alpha1/highs/defaults exactos, sin recencia. Selección interna exclusiva, bandas0.1 inclusivas/desempate entradas y orden, primario global sin rescate individual.

Implementación propia y nuevas decisiones técnicas detalladas en PROTOCOLO_IMPLEMENTACION: adaptador niveles/duplicados, contexto SHA completo, API historia anterior, separación Pipelines, CSVexacto/intfloat0/rechazo1e-11, linaje1320→528 condicionado/menor externo, cobertura825/16 solo futura, procesos terminables/estados sintéticos/huellas/serial/retry/caída/presupuesto. No import de runners históricos ni modelos. Orquestación de piloto real pendiente de fase3, con pruebas y congelación propias antes ajustes reales; reglas congeladas aquí no cambian.

Evidencia actual: últimas suite CLI y notebook aprobadas, {cli['grupos']} grupos/{cli['controles_negativos']} negativos cada una/{cli['fits_inventados']}fits inventados por corrida. Total{fits}fits inventados de todas corridas preservadas; panelreal0/modeloscargados0. Notebook3celdas realmente ejecutadas por execPython secuencial, validado/releído nbformat, fuente/generador/salidas ligadas por SHA. ACEPTACION_FASE2 completa={complete}; pendientes indispensables={pending}. Congelación propia solo emitida después de controles/entorno/conservación válidos y antes todo ajuste real; huella en aceptación independiente. MANIFIESTO_FASE2 incluye esta continuidad y entregables, exclusiones explícitas de autorreferencia.

Incidencias propias archivadas: lectura plan completo y salida conjunta truncada, luego vigentes acotados; prueba linaje eligió fila única2024 y se corrigió a copia2021; raíz con traversal no rechazada, corregida con control negativo. Ensayo CLI001 fallido/código original en resultados/antecedentes_cli_001, CLI002/003 y notebook posteriores válidos. No alteración de criterios ni reapertura de antecedentes históricos sin información nueva.

Impacto científico: eficacia memoria/común/corrección no evaluada; alternativa implementada con reglas fijas, prueba real pendiente. Fragilidad común1fila y pocos años permanece. Referencia histórica recencia/global sin mejora, no nueva reproducción o métrica actual. Guainía238vs404/diferencia21.012105832431985puntos histórica v2/fase1/resultados/diagnostico_medias_disponibles.csv filas57y90; sin cambiar media. Procedencia local no autenticada/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años. Todos2021–2025vistos: exploratorio sin confirmación independiente/causalidad/pronóstico anticipado demostrado.

Pendientes: usuario debe enviar prompt fase3 separado; revalidar aceptación/manifiesto/congelación/entorno/Git/conservación antes piloto.7200s/cota46=24+16+hasta6 SOLO contrato futuro, sin ledger real ni saldo heredado. No fuentes nuevas, instalaciones, modelo final, notebook de modelos, simulación, objetivo4 ni avance automático. Confirmación científica/disponibilidad requieren alcance separado. Cierre verificable con etapa1/cerrar.py --verificar, en lectura.
''')
    excluded=['etapa1/MANIFIESTO_FASE2.json','etapa1/VERIFICACION_MANIFIESTO_FASE2.json']
    manifest={'version':'1.0.0','completa':complete,'base':'experimentos_memoria_comun_objetivo3_v1/',
        'entregables':own_inventory(excluded),'exclusiones_autorreferencia':excluded,
        'symlinks':'Solo fixtures de rechazo; SHA del texto enlace, no destino',
        'congelacion_sha256':acceptance.get('congelacion_sha256'),'pendientes_indispensables':pending}
    write(OUT/'MANIFIESTO_FASE2.json',manifest)
    if complete:
        proof=verify(); proof['modo']='Verificación posterior a escritura; script --verificar no escribe'
        write(OUT/'VERIFICACION_MANIFIESTO_FASE2.json',proof)
    print(json.dumps({'completa':complete,'entregables':len(manifest['entregables']),'fits_inventados':fits,'fits_panel_real':0,'pendientes':pending}))

if __name__=='__main__':
    if sys.argv[1:]==['--verificar']: verify()
    elif not sys.argv[1:]: close()
    else: raise ValueError('Uso: cerrar.py [--verificar]')
