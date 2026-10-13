"""Verifica preparación en lectura, cero fits/modelos/escrituras. No importar runners."""
from pathlib import Path
import os,sys,json,hashlib,subprocess,platform,importlib.metadata as md,csv
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def load(p): return json.loads(Path(p).read_text())
def sha(p):
 p=Path(p)
 if p.is_symlink(): return hashlib.sha256(os.readlink(p).encode()).hexdigest()
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def check(v,where):
 if not v: raise AssertionError(where)
def verify():
 m=load(HERE/'MANIFIESTO_DOCUMENTAL.json');spec=load(HERE/'ESPECIFICACION_V6.json')
 for s,h in m['entregables_sha256'].items(): check(sha(HERE/s)==h,'manifest '+s)
 inventory={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
 check(inventory-set(m['exclusiones_autorreferencia'])==set(m['entregables_sha256']),'inventario documental exacto')
 check(sha(HERE/'CONTINUIDAD_V6.md')==m['continuidad_sha256'],'continuidad inicial')
 check(load(HERE/'ACEPTACION_DOCUMENTAL.json')['completa'] and all(load(HERE/'ACEPTACION_DOCUMENTAL.json')['controles'].values()),'aceptación documental')
 e=load(HERE/'ENTORNO_DOCUMENTAL.json');a={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions()}
 pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
 check(platform.python_version()=='3.12.14' and a.get('scikit-learn')=='1.9.1' and len(e['lock'])==54 and {k:v for k,v in a.items() if k!='pip'}==e['lock'] and pip.returncode==0 and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1','entorno consultar si falla;no instalar/sustituir')
 for s,h in spec['fuentes'].items(): check(sha(ROOT/s)==h,'fuente '+s)
 snapshot=load(HERE/'PARTIDA_DOCUMENTAL.json')
 for s,h in snapshot['protegidos'].items(): check(sha(ROOT/s)==h,'protegido '+s)
 cmd=lambda *x:subprocess.check_output(['git',*x],cwd=ROOT).decode()
 check(cmd('rev-parse','HEAD').strip()==snapshot['head'] and cmd('branch','--show-current').strip()==snapshot['rama'] and not cmd('diff','--name-only','HEAD').strip(),'Git HEAD/rama/posteriores')
 foreign=[s for s in cmd('ls-files','--cached','--others','--exclude-standard','-z').split('\0') if s and s not in snapshot['protegidos'] and not s.startswith('experimento_final_objetivo3_v6/')]
 check(not foreign,'ajenos nuevos '+str(foreign))
 c=spec['candidates'];check(len(c)==39 and len({x['id'] for x in c})==39 and [x['order'] for x in c]==list(range(39)),'39IDs/orden')
 with (HERE/'CANDIDATOS.csv').open(newline='') as f: rr=list(csv.DictReader(f))
 check(len(rr)==39,'CSV39')
 for x,y in zip(c,rr):
  check(x['id']==y['id'] and x['order']==int(y['order']) and x['inputs']==int(y['inputs']) and x['family']==y['family'] and x['history']==y['history'] and x['components']==json.loads(y['components']) and x['params']==json.loads(y['params']) and (x['statistic'] or '')==y['statistic'],'CSVJSON '+x['id'])
 components=sum(len(x['components']) for x in c);constants=sum(x['family'] in ['nivel_territorial','nivel_comun'] for x in c)
 check(components==32 and constants==10,'componentes/estadísticas')
 check(spec['budget']['internal_component_fits']==components*6 and spec['budget']['external_component_fits']==components*4 and spec['budget']['component_fits_max_without_failures']==components*10+8==328,'cota328')
 check(spec['budget']['seconds']==7200 and spec['target_percent']==5 and spec['coverage']=={'internal_original':39*10*33,'selection_records':39*4,'external':40*165,'internal_unique_conditional':39*4*33,'lineage':39*10*33,'global_checks':5},'coverage/budget/meta')
 check(spec['windows']==load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')['ventanas'],'windows heredadas')
 check(not list(HERE.rglob('*.ipynb')) and not list(HERE.rglob('ledger.json')),'documental sinnotebook/ledger')
 return {'aprobado':True,'estado':'preparación documental completa;noejecución','huellas':len(m['entregables_sha256']),'protegidos':len(snapshot['protegidos']),'candidatos':39,'componentes_por_contexto':32,'cota_fits_futura_sin_fallos':328,'presupuesto_futuro_segundos':7200,'fits_ejecutados':0,'modelos_cargados':0,'modo':'solo lectura,sinfit/escrituras','originales_intactos':True}
if __name__=='__main__': print(json.dumps(verify(),ensure_ascii=False))
