"""Comprobación propia; no ejecuta ni modifica verificadores históricos."""
from infra import *
import ast, sys, subprocess, platform, importlib.metadata as md, shutil
BASE='experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
DERIVED='experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv'
SOURCES={BASE:'6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3',DERIVED:'aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc'}
def git(*a): return subprocess.check_output(['git',*a],cwd=ROOT).decode().strip()
def mapping(folder,name,key,replacements=None):
    m=load(folder/name); replacements=replacements or {}
    for s,h in m[key].items():
        p=replacements.get(s,folder/s)
        check(sha(p)==(h['sha256'] if isinstance(h,dict) else h),'mapping '+str(p))
    return len(m[key])
def conservation():
    b=load(HERE/'preparacion/PARTIDA.json')
    for n,h in b['protegidos'].items(): check(sha(ROOT/n)==h,'original '+n)
    for k,args in [('head',('rev-parse','HEAD')),('rama',('branch','--show-current')),('asunto',('log','-1','--format=%s')),('tracked_diff',('diff','--name-only','HEAD'))]: check(git(*args)==b[k],'git '+k)
    paths=git('ls-files','--cached','--others','--exclude-standard','-z').split('\0')
    check(not [p for p in paths if p and p not in b['protegidos'] and not p.startswith(HERE.name+'/')],'ajenos nuevos')
    # preparación permanece íntegra, excepto continuidad con copia explícita previa
    pm=load(HERE/'MANIFIESTO_PREPARACION.json')
    for n,h in pm['sha256'].items():
        p=HERE/'antecedentes/CONTINUIDAD_PREPARACION.md' if n=='CONTINUIDAD.md' and (HERE/'antecedentes/CONTINUIDAD_PREPARACION.md').exists() else HERE/n
        check(sha(p)==h,'preparación '+n)
    old=ROOT/'experimento_final_objetivo3_v6';v=old/'ejecucion_autorizada'
    counts={'documental':mapping(old,'MANIFIESTO_DOCUMENTAL.json','entregables_sha256',{'CONTINUIDAD_V6.md':old/'fase1/antecedentes/CONTINUIDAD_ANTERIOR.md'}), 'vigente':mapping(v,'MANIFIESTO_FINAL.json','sha256')}
    final=load(v/'MANIFIESTO_FINAL.json');check(sha(old/'CONTINUIDAD_V6.md')==final['continuidad_principal_sha'],'continuidad principal')
    for phase,nextphase in [(1,2),(2,3)]:
        counts[f'vigente_fase{phase}']=mapping(v,f'fase{phase}/MANIFIESTO.json','sha256')
        check(sha(v/f'fase{nextphase}/antecedentes/CONTINUIDAD_ANTERIOR.md')==load(v/f'fase{phase}/MANIFIESTO.json')['continuidad_sha'],'continuidad fase')
    counts['congelacion_vigente']=mapping(v,'fase1/CONGELACION.json','sha256')
    prior=load(v/'PARTIDA_PROPIA.json')
    for n,h in prior['original_attempt_sha256'].items():
        check(sha(v/'antecedentes/CONTINUIDAD_CIERRE_ANTERIOR.md' if n=='CONTINUIDAD_V6.md' else old/n)==h,'intento anterior '+n)
    check(sha(old/'MANIFIESTO_FINAL.json')==prior['manifest_sha256'],'manifiesto anterior')
    mem=ROOT/'experimentos_memoria_comun_objetivo3_v1'
    for folder,name,key,repl in [(ROOT/'diseno_memoria_comun_objetivo3_v1','MANIFIESTO_FASE1.json','entregables_sha256',{}),(mem,'etapa1/MANIFIESTO_FASE2.json','entregables',{'CONTINUIDAD_EXPERIMENTAL.md':mem/'etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md'}),(mem/'etapa2','MANIFIESTO_FASE3.json','entregables_sha256',{}),(mem/'etapa3','MANIFIESTO_FASE4.json','entregables_sha256',{})]:counts[name]=mapping(folder,name,key,repl)
    for phase in [3,4]:
        m=load(mem/f'etapa{phase-1}/MANIFIESTO_FASE{phase}.json')
        p=mem/'etapa3/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md' if phase==3 else mem/'CONTINUIDAD_EXPERIMENTAL.md'
        check(sha(p)==m['continuidad_actual_sha256'],'mem continuidad')
    for n in ['etapa1/ACEPTACION_FASE2.json','etapa2/ACEPTACION_FASE3.json','etapa3/ACEPTACION_FASE4.json']:check(load(mem/n)['completa'],'mem cierre')
    h=load(mem/'etapa1/PREFLIGHT_FASE2.json')['historica_v5'];commit='109797407d75d2097e5b71f8bcef3fc266bc61d2'
    check(h['commit']==commit,'commit registrado')
    check(hashlib.sha256(subprocess.check_output(['git','show',commit+':'+h['archivo']],cwd=ROOT)).hexdigest()==h['sha256'],'commit bytes')
    check(subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT).returncode==0,'ascendencia')
    temporal=load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
    check(hashlib.sha256(temporal['continuidad_inicial'].encode()).hexdigest()==temporal['continuidad_sha256'],'temporal texto huella')
    return dict(aprobado=True,modo='cotejo propio actual; no verificador histórico',protegidos=len(b['protegidos']),mappings=counts,head=b['head'],rama=b['rama'],asunto=b['asunto'],tracked_diff=b['tracked_diff'],status=git('status','--porcelain=v1'),historico=h,trabajo_posterior=git('log','--format=%H %s',commit+'..HEAD'),temporal_sha=temporal['continuidad_sha256'],verificador_historico=load(HERE/'preparacion/VERIFICACION_ANTERIOR.json'))
def environment():
    e=load(ROOT/'experimento_final_objetivo3_v6/ejecucion_autorizada/ENTORNO_DOCUMENTAL.json')
    actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions()}
    check(platform.python_version()=='3.12.14' and actual.get('pip')=='25.0.1' and len(e['lock'])==54 and {k:v for k,v in actual.items() if k!='pip'}==e['lock'],'entorno exacto')
    check(os.environ.get('PYTHONDONTWRITEBYTECODE')=='1','sin bytecode')
    for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:check(os.environ.get(key)=='1','hilo '+key)
    p=subprocess.run([sys.executable,'-m','pip','check'],text=True,capture_output=True);check(p.returncode==0,'pip check')
    import sklearn
    from threadpoolctl import threadpool_info
    check(sklearn.__version__=='1.9.1' and all(x['num_threads']==1 for x in threadpool_info()),'sklearn/hilos')
    return dict(aprobado=True,python=platform.python_version(),actual=actual,lock=e['lock'],pip_check=dict(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr),variables={k:v for k,v in os.environ.items() if k.endswith('NUM_THREADS') or k in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS']},threadpools=threadpool_info(),semilla=SEED,ejecutable=sys.executable)
def tasas():
    tree=ast.parse((ROOT/'protocolo/fuentes/configuracion.py').read_text())
    dims=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DIMENSIONES' for t in n.targets))
    tnode=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TASAS' for t in n.targets))
    check(ast.unparse(tnode.value)=='[v for grupo in DIMENSIONES.values() for v in grupo]','TASAS declarada')
    t=[x for vs in dims.values() for x in vs];check(len(t)==15 and len(set(t))==15,'15 tasas')
    return t,dims
def run():
    deadline();check(not (HERE/'piloto/ledger.json').exists(),'piloto existente; no repetición automática')
    e=environment()  # ANTES de cálculos analíticos
    c=conservation()
    for n,h in SOURCES.items():check(sha(ROOT/n)==h,'fuente '+n)
    check(not any(p.is_symlink() for p in HERE.rglob('*')),'sin symlinks propios')
    closure=load(HERE/'preparacion/CIERRE_PREPARACION.json');check(closure['real_fits']==closure['synthetic_fits']==0 and not closure['pilot_started'],'preparación cero')
    dest=HERE/'antecedentes/CONTINUIDAD_PREPARACION.md';check(not dest.exists(),'preservación única');save(dest,(HERE/'CONTINUIDAD.md').read_text())
    save(HERE/'AUTORIZACION_SESION.md',(HERE/'PROMPT_NUEVA_SESION.md').read_text())
    save(HERE/'INICIO.json',dict(start_epoch=START,start_utc='2026-10-12T18:07:59Z',max_total_seconds=7200,stop_new_fits_seconds=5400,autorizacion='envío humano expreso en sesión actual',prompt_sha=sha(HERE/'AUTORIZACION_SESION.md'),preparacion_cerrada=True,saldo_heredado=False))
    save(HERE/'preflight/ENTORNO.json',e);save(HERE/'preflight/CONSERVACION.json',c)
    save(HERE/'preflight/FUENTES.json',SOURCES)
    save(HERE/'preflight/TEMPORAL_ETAPA1_TEXTO.md',load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')['continuidad_inicial'])
    print(json.dumps(dict(aprobado=True,protegidos=c['protegidos'],python=e['python'],distribuciones=len(e['lock']),elapsed_seconds=elapsed())))
if __name__=='__main__':run()
