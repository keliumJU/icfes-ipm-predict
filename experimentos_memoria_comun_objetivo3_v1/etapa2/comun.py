"""Utilidades propias fase3; únicas importaciones operativas: etapa1 congelada."""
from pathlib import Path
import sys, os, json, hashlib, time, csv, subprocess, importlib.metadata as metadata
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
E1=HERE.parent/'etapa1'
sys.path.insert(0,str(E1))
from motor import *
from integridad import safe_path, digest, context_hash, exact_csv, prepared_context
from preflight import info, equivalent, git
from ejecucion_sintetica import atomic_json

def load(p): return json.loads(Path(p).read_text())
def write(rel,obj):
    p=safe_path(HERE,rel); p.parent.mkdir(parents=True,exist_ok=True)
    atomic_json(p,obj)
def fresh(rel,obj):
    if safe_path(HERE,rel).exists(): raise IntegrityError('No sobrescribir: '+rel)
    write(rel,obj)
def environment():
    lock={}
    for line in (ROOT/'experimentos_objetivo3_v5/etapa1/requirements.lock.txt').read_text().splitlines():
        if '==' in line and not line.startswith('#'):
            k,v=line.strip().split('=='); lock[k.lower().replace('_','-')]=v
    actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in metadata.distributions()}
    pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
    result={'python':sys.version,'executable':sys.executable,'lock':lock,'actual':actual,
            'pip_check':{'returncode':pip.returncode,'stdout':pip.stdout,'stderr':pip.stderr},
            'PYTHONDONTWRITEBYTECODE':os.environ.get('PYTHONDONTWRITEBYTECODE'),'semilla':SEED}
    ok=(sys.version_info[:3]==(3,12,14) and len(lock)==54 and
        {k:v for k,v in actual.items() if k!='pip'}==lock and actual.get('scikit-learn')=='1.9.1'
        and pip.returncode==0 and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1')
    if ok:
        pipe=new_pipeline(); result['defaults']={type(obj).__name__:obj.get_params() for obj in pipe.named_steps.values()}
        ok=result['defaults']==load(E1/'ENTORNO_FASE2.json')['defaults']
    result['aprobado']=ok
    return result
def csv_write(rel,rows,fields=None):
    p=safe_path(HERE,rel); p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists(): raise IntegrityError('CSV existente')
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0])); w.writeheader(); w.writerows(rows)
def serial_prepared(p,candidate):
    comps=COMPONENTS[candidate_index(candidate)]
    return {'candidate':candidate,'evaluated':p.evaluated,'role':p.role,'previous_year':p.previous_year,
        'previous_score':p.previous_score.tolist(),'history_years':p.history_years,'supervised_years':p.supervised_years,
        'd':{str(y):v.tolist() for y,v in p.d.items()},'c':p.c,'r':{str(y):v.tolist() for y,v in p.r.items()},
        'matrices':{k:[a.tolist() for a in p.matrices[k]] for k in comps},
        'prediction_inputs':{k:p.prediction_inputs[k].tolist() for k in comps},'keys':{k:p.keys[k] for k in comps},
        'units':{k:'año' if k=='comun' else 'territorio-año' for k in comps},
        'defaults':[SCALER,REGRESSOR],'seed':SEED,'context':prepared_context(p,candidate)}

def conservation():
    partida=load(HERE/'resultados/partida.json')
    bad=[]
    for p,e in partida['inventario_protegido'].items():
        try:
            if not equivalent(e,info(p)): bad.append(p)
        except OSError: bad.append(p)
    tracked=git('ls-files','-z').decode().split('\0')[:-1]
    untracked=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    prefix=HERE.relative_to(ROOT).as_posix()+'/'
    continuity=(HERE.parent/'CONTINUIDAD_EXPERIMENTAL.md').relative_to(ROOT).as_posix()
    foreign=[p for p in untracked if p not in partida['inventario_protegido'] and not p.startswith(prefix) and p!=continuity]
    return {'aprobado':not bad and not foreign and tracked==partida['versionados'] and git('rev-parse','HEAD').decode().strip()==partida['head']
            and not git('diff','--name-only','HEAD').decode().strip(),
            'protegidos':len(partida['inventario_protegido']),'diferencias':bad,'ajenos_nuevos':foreign,'versionados':len(tracked),'raw':'sin lectura/censo/escritura'}
