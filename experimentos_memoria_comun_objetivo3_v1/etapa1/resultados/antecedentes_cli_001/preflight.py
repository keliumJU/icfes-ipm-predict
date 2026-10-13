"""Solo lectura de antecedentes y entorno; escribe evidencias propias fase2."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import importlib.metadata as metadata

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
EXP = OUT.parent
DESIGN = ROOT / 'diseno_memoria_comun_objetivo3_v1'
BASE = '75c3a25182af363f47b0d743820f99084e18fed5'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(Path(path).read_text())

def write(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def info(path):
    p = ROOT / path
    if p.is_symlink():
        target = os.readlink(p)
        return {'tipo':'symlink', 'destino':target, 'sha256':sha(target.encode())}
    return {'tipo':'archivo', 'sha256':sha(p.read_bytes())}

def equivalent(a, b):
    a = {'sha256':a} if isinstance(a,str) else a
    return (a.get('sha256',a.get('sha256_texto_enlace'))==b['sha256']
            and ('symlink' in a.get('tipo','archivo'))==(b['tipo']=='symlink')
            and (b['tipo']!='symlink' or a.get('destino',a.get('target',a.get('enlace')))==b['destino']))

def environment():
    prior = load(DESIGN/'ENTORNO_FASE1.json')
    lock = {}
    for line in (ROOT/'experimentos_objetivo3_v5/etapa1/requirements.lock.txt').read_text().splitlines():
        if '==' in line and not line.startswith('#'):
            name,version=line.strip().split('=='); lock[name.lower().replace('_','-')]=version
    actual = {d.metadata['Name'].lower().replace('_','-'):d.version for d in metadata.distributions()}
    differences={k:[v,actual.get(k)] for k,v in lock.items() if actual.get(k)!=v}
    extras={k:v for k,v in actual.items() if k not in lock and k!='pip'}
    pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
    ok=(sys.version_info[:3]==(3,12,14) and len(lock)==54 and lock==prior['lock']
        and not differences and not extras and pip.returncode==0
        and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1')
    result={'aprobado':ok,'python':sys.version,'executable':sys.executable,'lock':lock,
            'diferencias':differences,'extras_sin_pip':extras,'pip_check':{'returncode':pip.returncode,'stdout':pip.stdout,'stderr':pip.stderr},
            'PYTHONDONTWRITEBYTECODE':os.environ.get('PYTHONDONTWRITEBYTECODE'),'semilla':20261010}
    if ok:
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import QuantileRegressor
        result['defaults']={'StandardScaler':StandardScaler().get_params(),'QuantileRegressor':QuantileRegressor().get_params()}
        result['aprobado']=result['defaults']==prior['defaults']
    write(OUT/'ENTORNO_FASE2.json',result)
    if not result['aprobado']:
        raise RuntimeError('Entorno diferente: detener y consultar; no sustituir ni instalar')
    return result

def main():
    environment()
    prep=load(DESIGN/'REGISTRO_PREPARACION.json')
    errors=[]
    for p,e in prep['inventario_protegido'].items():
        if not equivalent(e,info(p)): errors.append(p)
    manifest=load(DESIGN/'MANIFIESTO_FASE1.json')
    design_errors=[p for p,h in manifest['entregables_sha256'].items() if sha((DESIGN/p).read_bytes())!=h]
    accept=load(DESIGN/'ACEPTACION_FASE1.json')
    indispensable=(accept['completa_documental'] and all(accept['controles'].values())
                   and accept['conservacion_aprobada'] and not accept['pendientes_indispensables_fase1']
                   and load(DESIGN/'CONSERVACION_FASE1.json')['aprobado'])
    hist='109797407d75d2097e5b71f8bcef3fc266bc61d2'
    hp='experimentos_objetivo3_v5/CONTINUIDAD_V5.md'
    historic_bytes=git('show',hist+':'+hp)
    hist_sha=sha(historic_bytes)
    temporal=load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
    temporal_bytes=temporal['continuidad_inicial'].encode()
    temporal_sha=sha(temporal_bytes)
    manifests={}
    for mp in prep['verificaciones_antecedentes']:
        doc=load(ROOT/mp)
        mapping=next(doc[k] for k in ('entregables_sha256','entregables','artefactos_sha256','archivos_sha256') if k in doc)
        bad=[]
        for p,expected in mapping.items():
            if p==hp and '/etapa1/' in mp:
                actual={'tipo':'archivo','sha256':hist_sha}
            elif p=='experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md' and '/etapa1/' in mp:
                actual={'tipo':'archivo','sha256':temporal_sha}
            else:
                q='experimentos_objetivo3_v5/etapa2/resultados/piloto/'+p if mp.endswith('piloto/indice_integridad.json') else p
                actual=info(q)
            if not equivalent(expected,actual): bad.append(p)
        manifests[mp]={'huellas':len(mapping),'diferencias':bad,'aprobado':not bad}
    spec=load(DESIGN/'ESPECIFICACION_DOCUMENTAL.json')
    sources={p:info(p)['sha256']==v['esperado'] for p,v in spec['fuentes'].items()}
    head=git('rev-parse','HEAD').decode().strip()
    tracked=git('ls-files','-z').decode().split('\0')[:-1]
    untracked=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    posterior=git('log','--format=%H %s',BASE+'..HEAD').decode().splitlines()
    ancestors={ref:subprocess.run(['git','merge-base','--is-ancestor',ref,head],cwd=ROOT).returncode==0 for ref in (BASE,hist)}
    diff=git('diff','--name-only','HEAD').decode().splitlines()
    new_foreign=[p for p in untracked if not p.startswith(EXP.name+'/') and p not in prep['inventario_protegido'] and not p.startswith(DESIGN.name+'/')]
    ok=(not errors and not design_errors and indispensable and all(v['aprobado'] for v in manifests.values())
        and all(sources.values()) and hist_sha=='33bbdce75635733eae8bad9e14d1900999fd8af6318a55842382b5d2544e13fd'
        and temporal_sha==temporal['continuidad_sha256']=='fd3b963135e9e8233470ef36116d82e67ca4a88aae67b7c785d0a9185ba0b8bb'
        and head==BASE and all(ancestors.values()) and not posterior and not diff and tracked==prep['versionados'] and not new_foreign)
    result={'aprobado':ok,'git':{'head':head,'asunto':git('log','-1','--format=%s').decode().strip(),'rama':git('branch','--show-current').decode().strip(),
            'ascendencia':ancestors,'trabajo_posterior':posterior,'diff':diff,'status':git('status','--short').decode().splitlines(),'versionados':len(tracked),'ajenos_nuevos':new_foreign},
            'antecedentes':{'n':len(prep['inventario_protegido']),'diferencias':errors},'manifiestos':manifests,
            'fase1':{'valida':indispensable,'huellas':len(manifest['entregables_sha256']),'diferencias':design_errors},'fuentes':sources,
            'historica_v5':{'commit':hist,'archivo':hp,'sha256':hist_sha},'temporal_preservada':{'ubicacion':'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json:continuidad_inicial','sha256':temporal_sha},
            'autorizacion':'Usuario envió prompt fase2 y aprobó diseño; no piloto ni fits reales'}
    write(OUT/'PREFLIGHT_FASE2.json',result)
    if not ok: raise RuntimeError('Control indispensable anterior no resuelto')
    # Snapshot nuevo de TODOS los antecedentes no ignorados; no censo de raw ni .git.
    snapshot={p:info(p) for p in tracked+untracked if not p.startswith(EXP.name+'/')}
    partida=OUT/'PARTIDA_FASE2.json'
    if not partida.exists():
        write(partida,{'git_head':head,'versionados':tracked,'inventario_protegido':snapshot,
              'continuidad_previa_experimental':None,'raw':'Ignorado, sin lectura/censo/escritura',
              'semilla':20261010,'presupuesto_real_iniciado':False,'saldo_heredado':None})
    print(json.dumps({'aprobado':ok,'antecedentes':len(snapshot),'manifiestos':len(manifests),'fase1_huellas':len(manifest['entregables_sha256'])}))

if __name__=='__main__':
    main()
