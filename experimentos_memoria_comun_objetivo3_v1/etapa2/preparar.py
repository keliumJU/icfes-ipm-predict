"""Preflight propio en lectura de antecedentes; cero ajustes."""
from comun import *

def main():
    # Se ejecutó cerrar.py --verificar en lectura antes de crear esta etapa.
    env=environment()
    if (HERE/'ENTORNO_FASE3.json').exists():
        assert digest(HERE/'ENTORNO_FASE3.json')==digest(HERE/'antecedentes/preflight_001/ENTORNO_FASE3.json')
    write('ENTORNO_FASE3.json',env)
    if not env['aprobado']: raise RuntimeError('Entorno diferente: detener y consultar')
    from cerrar import verify
    # verify aún puede verificar inventario original si se evalúa explícitamente su mapping;
    # etapa2 es nueva y queda fuera de su lista congelada, no se modifica etapa1.
    from cerrar import verify_mapping, conservation as old_conservation, environment_readonly
    manifest=load(E1/'MANIFIESTO_FASE2.json'); freeze=load(E1/'CONGELACION_FASE2.json'); acc=load(E1/'ACEPTACION_FASE2.json')
    bad=verify_mapping(manifest['entregables'],HERE.parent)
    badfreeze=verify_mapping(freeze['implementacion'],E1)
    contracts=[p for p,h in freeze['documentos_base'].items() if info(p)['sha256']!=h]
    phase2=not bad and not badfreeze and not contracts and acc['completa'] and acc['congelacion_valida'] and not acc['pendientes_indispensables'] and digest(E1/'CONGELACION_FASE2.json')==acc['congelacion_sha256'] and old_conservation()['aprobado'] and environment_readonly()
    assert phase2
    previous=HERE.parent/'CONTINUIDAD_EXPERIMENTAL.md'
    copy=safe_path(HERE,'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md'); copy.parent.mkdir(exist_ok=True)
    if copy.exists(): raise IntegrityError('Antecedente existente')
    copy.write_bytes(previous.read_bytes()); assert digest(copy)==digest(previous)
    prep=load(ROOT/'diseno_memoria_comun_objetivo3_v1/REGISTRO_PREPARACION.json')
    hp='experimentos_objetivo3_v5/CONTINUIDAD_V5.md'; hist='109797407d75d2097e5b71f8bcef3fc266bc61d2'
    historic=git('show',hist+':'+hp); h=hashlib.sha256(historic).hexdigest()
    temporal=load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
    th=hashlib.sha256(temporal['continuidad_inicial'].encode()).hexdigest()
    assert h=='33bbdce75635733eae8bad9e14d1900999fd8af6318a55842382b5d2544e13fd'
    assert th==temporal['continuidad_sha256']=='fd3b963135e9e8233470ef36116d82e67ca4a88aae67b7c785d0a9185ba0b8bb'
    fresh('antecedentes/temporal_etapa1_preservada.json',{'texto':temporal['continuidad_inicial'],'sha256':th,'ubicacion':'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json:continuidad_inicial'})
    safe_path(HERE,'antecedentes/v5_etapa1_commit.md').write_bytes(historic)
    checks={}
    for mp in prep['verificaciones_antecedentes']:
        doc=load(ROOT/mp); mapping=next(doc[k] for k in ('entregables_sha256','entregables','artefactos_sha256','archivos_sha256') if k in doc)
        wrong=[]
        for p,expected in mapping.items():
            if p==hp and '/etapa1/' in mp: actual={'tipo':'archivo','sha256':h}
            elif p=='experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md' and '/etapa1/' in mp: actual={'tipo':'archivo','sha256':th}
            else: actual=info('experimentos_objetivo3_v5/etapa2/resultados/piloto/'+p if mp.endswith('piloto/indice_integridad.json') else p)
            if not equivalent(expected,actual): wrong.append(p)
        checks[mp]={'huellas':len(mapping),'diferencias':wrong}; assert not wrong
    head=git('rev-parse','HEAD').decode().strip(); base='75c3a25182af363f47b0d743820f99084e18fed5'
    ancestors={ref:subprocess.run(['git','merge-base','--is-ancestor',ref,head],cwd=ROOT).returncode==0 for ref in (base,hist)}
    posterior=git('log','--format=%H %s',base+'..HEAD').decode().splitlines()
    assert head==base and all(ancestors.values()) and not posterior
    tracked=git('ls-files','-z').decode().split('\0')[:-1]
    untracked=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    prefix=HERE.relative_to(ROOT).as_posix()+'/'
    continuity=previous.relative_to(ROOT).as_posix()
    snapshot={p:info(p) for p in tracked+untracked if not p.startswith(prefix) and p!=continuity}
    fresh('resultados/partida.json',{'head':head,'versionados':tracked,'inventario_protegido':snapshot,
         'continuidad_previa_sha256':digest(copy),'continuidad_previa':'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md',
         'raw':'ignorado sin lectura/censo/escritura','fecha_cliente':'2026-10-11','timezone':'America/Bogota'})
    spec=load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')
    sources={p:digest(ROOT/p) for p in spec['fuentes']}
    assert all(sources[p]==v['esperado'] for p,v in spec['fuentes'].items())
    fresh('PREFLIGHT_FASE3.json',{'aprobado':True,'fase2':{'valida':phase2,'huellas':len(manifest['entregables']),'diferencias':bad,'freeze_diferencias':badfreeze,'contrato_diferencias':contracts},
          'git':{'head':head,'asunto':git('log','-1','--format=%s').decode().strip(),'rama':git('branch','--show-current').decode().strip(),'ascendencia':ancestors,'posterior':posterior,'status':git('status','--short').decode().splitlines()},
          'manifiestos':checks,'fuentes':sources,'historica_v5':{'commit':hist,'sha256':h},'temporal_preservada':{'sha256':th},'conservacion':conservation(),'primer_control':'cerrar.py --verificar aprobado, sin escritura/fits, 234huellas/31010protegidos',
          'autorizacion':'Envío humano exclusivo fase3/piloto predefinido; diseño aprobado en fase2; sin instalaciones/commit/push/fase4'})
    print(json.dumps({'aprobado':True,'protegidos':len(snapshot),'manifiestos':len(checks),'fits':0}))
if __name__=='__main__': main()
