"""Infraestructura propia v6. No lectura raw ni cargas de modelos."""
from pathlib import Path
import json, hashlib, os, sys, subprocess, platform, importlib.metadata as md
HERE = Path(__file__).resolve().parent
OWNROOT = HERE.parent
ROOT = OWNROOT.parent
SEED = 20261010
def load(p): return json.loads(Path(p).read_text())
def sha(p):
    p=Path(p)
    if p.is_symlink(): return hashlib.sha256(os.readlink(p).encode()).hexdigest()
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def check(v, label):
    if not v: raise AssertionError(label)
def safe(p):
    p=Path(p).absolute()
    check(p.is_relative_to(HERE) and '..' not in p.parts,'ruta fuera v6/traversal')
    check(all(not q.is_symlink() for q in [p,*p.parents] if q.is_relative_to(HERE)),'symlink rechazado')
    return p
def save(p,x):
    p=safe(p); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('w') as f:
        f.write(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp,p)
    fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def environment():
    e=load(HERE/'ENTORNO_DOCUMENTAL.json')
    actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions()}
    pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
    check(platform.python_version()=='3.12.14' and len(e['lock'])==54 and {k:v for k,v in actual.items() if k!='pip'}==e['lock'] and pip.returncode==0 and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1','entorno: consultar sin sustituir/instalar')
    return dict(python=platform.python_version(),lock=e['lock'],pip_check=pip.stdout,semilla=SEED,PYTHONDONTWRITEBYTECODE='1')
def conservation():
    s=load(HERE/'PARTIDA_DOCUMENTAL.json')
    for p,h in s['protegidos'].items(): check(sha(ROOT/p)==h,'original '+p)
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT).decode().strip()
    check(git('rev-parse','HEAD')==s['head'] and git('branch','--show-current')==s['rama'] and git('log','-1','--format=%s')==s['asunto'] and not git('diff','--name-only','HEAD'),'Git conservación')
    foreign=[p for p in git('ls-files','--cached','--others','--exclude-standard','-z').split('\0') if p and p not in s['protegidos'] and not p.startswith(OWNROOT.name+'/')]
    check(not foreign,'archivos ajenos nuevos')
    old=load(HERE/'PARTIDA_PROPIA.json')
    for path,h in old['original_attempt_sha256'].items():
        q=HERE/'antecedentes/CONTINUIDAD_CIERRE_ANTERIOR.md' if path=='CONTINUIDAD_V6.md' else OWNROOT/path
        check(sha(q)==h,'intento cerrado conservado '+path)
    check(sha(OWNROOT/'MANIFIESTO_FINAL.json')==old['manifest_sha256'],'manifiesto previo intacto')
    return dict(aprobado=True,protegidos=len(s['protegidos']),intento_anterior_huellas=len(old['original_attempt_sha256']),diferencias=[],head=s['head'],rama=s['rama'],asunto=s['asunto'])
def historical():
    base=ROOT/'experimentos_memoria_comun_objetivo3_v1'; counts={}
    for folder,name,key in [(ROOT/'diseno_memoria_comun_objetivo3_v1','MANIFIESTO_FASE1.json','entregables_sha256'),(base,'etapa1/MANIFIESTO_FASE2.json','entregables'),(base/'etapa2','MANIFIESTO_FASE3.json','entregables_sha256'),(base/'etapa3','MANIFIESTO_FASE4.json','entregables_sha256')]:
        m=load(folder/name)
        for s,h in m[key].items():
            p=base/'etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md' if folder==base and s=='CONTINUIDAD_EXPERIMENTAL.md' else folder/s
            check(sha(p)==(h['sha256'] if isinstance(h,dict) else h),'mapping histórico '+str(p))
        counts[name]=len(m[key])
    m=load(base/'etapa2/MANIFIESTO_FASE3.json')
    check(sha(base/'etapa3/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md')==m['continuidad_actual_sha256'],'continuidad fase3')
    m=load(base/'etapa3/MANIFIESTO_FASE4.json')
    check(sha(base/'CONTINUIDAD_EXPERIMENTAL.md')==m['continuidad_actual_sha256'],'continuidad fase4')
    for n in ['etapa1/ACEPTACION_FASE2.json','etapa2/ACEPTACION_FASE3.json','etapa3/ACEPTACION_FASE4.json']:
        check(load(base/n)['completa'],'aceptación histórica '+n)
    h=load(base/'etapa1/PREFLIGHT_FASE2.json')['historica_v5']
    check(h['commit']=='109797407d75d2097e5b71f8bcef3fc266bc61d2','commit real')
    check(hashlib.sha256(subprocess.check_output(['git','show',h['commit']+':'+h['archivo']],cwd=ROOT)).hexdigest()==h['sha256'],'v5 histórica')
    check(subprocess.run(['git','merge-base','--is-ancestor',h['commit'],'HEAD'],cwd=ROOT).returncode==0,'ascendencia')
    t=load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
    check(hashlib.sha256(t['continuidad_inicial'].encode()).hexdigest()==t['continuidad_sha256'],'temporal texto/huella')
    return dict(aprobado=True,mappings=counts,v5=h,temporal_sha=t['continuidad_sha256'],cierres_originales_modificados=False)
def preflight():
    e=environment(); spec=load(HERE/'ESPECIFICACION_V6.json')
    for s,h in spec['fuentes'].items(): check(sha(ROOT/s)==h,'fuente '+s)
    return dict(aprobado=True,entorno=e,conservacion=conservation(),historia=historical(),fuentes=spec['fuentes'])
