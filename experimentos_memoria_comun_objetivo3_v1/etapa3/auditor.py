"""Auditor independiente v1. Sin imports operativos, fits o deserialización."""
from pathlib import Path
import csv, json, math, hashlib, os, sys, subprocess, platform, importlib.metadata as md
from collections import defaultdict
from statistics import median
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=HERE.parent
E2=BASE/'etapa2'
YEARS=[2018,2019,2021,2022,2023,2024,2025]
CAND=['persistencia','memoria','comun','comun_correccion']
COMP=[[],['memoria'],['comun'],['comun','correccion']]
SC={'copy':True,'with_mean':True,'with_std':True}
QR={'alpha':1.0,'fit_intercept':True,'quantile':0.5,'solver':'highs','solver_options':None}
SEED=20261010

def load(p): return json.loads(Path(p).read_text())
def sha(p):
 p=Path(p)
 if p.is_symlink(): return hashlib.sha256(os.readlink(p).encode()).hexdigest()
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''): h.update(block)
 return h.hexdigest()
def save(name,value):
 p=HERE/name; p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists(): raise RuntimeError('Preservar existente: '+str(p))
 p.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def check(condition,location):
 if not condition: raise AssertionError(location)
def command(*args): return subprocess.check_output(args,cwd=ROOT).decode().strip()
def rows(p):
 with Path(p).open(newline='') as f: return list(csv.DictReader(f))
def metrics(a):
 e=[float(r['predicted'])-float(r['observed']) for r in a]
 check(e and all(math.isfinite(v) for v in e),'métricas finitas')
 return {'n':len(e),'MAE':math.fsum(map(abs,e))/len(e),'RMSE':math.sqrt(math.fsum(v*v for v in e)/len(e)),'sesgo':math.fsum(e)/len(e)}
def select(ms):
 pool=[c for c in CAND if ms[c]['MAE']<=min(ms[q]['MAE'] for q in CAND)+0.1]
 pool2=[c for c in pool if ms[c]['RMSE']<=min(ms[q]['RMSE'] for q in pool)+0.1]
 winner=min(pool2,key=lambda c:([0,1,1,2][CAND.index(c)],CAND.index(c)))
 return winner,pool,pool2

def exact(a,b):
 check(len(a)==len(b),'CSV longitud')
 for x,y in zip(a,b):
  check(list(x)==list(y),'CSV columnas/orden')
  for k in x:
   if k in ['code','candidate','policy','context','reason','role','eligible','selected']: check(x[k]==y[k],f'CSV texto {k}')
   else:
    try:
     v,w=float(x[k]),float(y[k]); check(math.isfinite(v) and math.isfinite(w) and v==w,f'CSV exacto {k}')
    except ValueError: check(x[k]==y[k],f'CSV texto {k}')

def reconstruct(levels,e,candidate,role):
 codes=sorted(levels[2018]); hist=[t for t in YEARS if t<e]
 prev=hist[-1]; ds={t:[levels[t][c]-levels[hist[i-1]][c] for c in codes] for i,t in enumerate(hist) if i}
 cs={t:median(v) for t,v in ds.items()}; rs={t:[v-cs[t] for v in ds[t]] for t in ds}
 supervised=[t for i,t in enumerate(hist) if i and t in ds and hist[i-1] in ds]
 matrices={}; inputs={}; keys={}; units={}
 for comp in COMP[CAND.index(candidate)]:
  z=cs if comp=='comun' else ds if comp=='memoria' else rs
  X=[]; y=[]; kk=[]
  for t in supervised:
   p=max(q for q in hist if q<t)
   if comp=='comun': X.append([z[p]]); y.append(z[t]); kk.append([t,p])
   else:
    for j,c in enumerate(codes): X.append([z[p][j]]); y.append(z[t][j]); kk.append([c,t,p])
  matrices[comp]=[X,y]; inputs[comp]=[[z[prev]]] if comp=='comun' and prev in z else [[v] for v in z[prev]] if prev in z else []
  keys[comp]=kk; units[comp]='año' if comp=='comun' else 'territorio-año'
 result={'candidate':candidate,'evaluated':e,'role':role,'previous_year':prev,'previous_score':[levels[prev][c] for c in codes],
 'history_years':hist,'supervised_years':supervised,'d':{str(k):v for k,v in ds.items()},'c':{str(k):v for k,v in cs.items()},'r':{str(k):v for k,v in rs.items()},
 'matrices':matrices,'prediction_inputs':inputs,'keys':keys,'units':units,'defaults':[SC,QR],'seed':SEED}
 context={'candidate':candidate,'evaluated':e,'role':role,'previous_year':prev,'previous_score':result['previous_score'],'history':hist,'supervised':supervised,'matrices':matrices,'prediction_inputs':inputs,'keys':keys,'defaults':[SC,QR],'python':'3.12.14','sklearn':'1.9.1','seed':SEED}
 result['context']=hashlib.sha256(json.dumps(context,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 return result

def preflight():
 lock={k.lower().replace('_','-'):v for line in (ROOT/'experimentos_objetivo3_v5/etapa1/requirements.lock.txt').read_text().splitlines() if '==' in line and not line.startswith('#') for k,v in [line.strip().split('==')]}
 actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions()}
 pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True)
 env={'python':platform.python_version(),'sklearn':actual.get('scikit-learn'),'lock':lock,'actual':actual,'pip_check':{'returncode':pip.returncode,'stdout':pip.stdout,'stderr':pip.stderr},'PYTHONDONTWRITEBYTECODE':os.environ.get('PYTHONDONTWRITEBYTECODE'),'semilla':SEED}
 env['aprobado']=env['python']=='3.12.14' and len(lock)==54 and {k:v for k,v in actual.items() if k!='pip'}==lock and pip.returncode==0 and env['PYTHONDONTWRITEBYTECODE']=='1'
 save('ENTORNO_FASE4.json',env); check(env['aprobado'],'ENTORNO: detener y consultar sin instalar/sustituir')
 # No cálculos analíticos antes de este control.
 protected={}
 listing=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
 for s in listing:
  if s and not s.startswith(str(HERE.relative_to(ROOT))+'/'):
   p=ROOT/s
   if p.is_file() or p.is_symlink(): protected[s]=sha(p)
 save('PARTIDA_FASE4.json',{'protegidos':protected,'raw':'sin lectura/censo/escritura','continuidad_previa_sha256':sha(BASE/'CONTINUIDAD_EXPERIMENTAL.md')})
 preserved=HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md'; check(not preserved.exists(),'continuidad previa existente'); preserved.write_bytes((BASE/'CONTINUIDAD_EXPERIMENTAL.md').read_bytes())
 head=command('git','rev-parse','HEAD'); branch=command('git','branch','--show-current')
 check(head=='75c3a25182af363f47b0d743820f99084e18fed5' and branch=='codex/objetivo3-v5-mae','Git HEAD/rama')
 check(not command('git','diff','--name-only','HEAD'),'Git trabajo posterior versionado')
 check(not command('git','log',head+'..HEAD','--format=%H'),'Git commits posteriores')
 for commit in [head,'109797407d75d2097e5b71f8bcef3fc266bc61d2']:
  check(subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT).returncode==0,'ascendencia '+commit)
 historical=load(BASE/'etapa1/PREFLIGHT_FASE2.json')['historica_v5']
 text=subprocess.check_output(['git','show',historical['commit']+':'+historical['archivo']],cwd=ROOT)
 check(hashlib.sha256(text).hexdigest()==historical['sha256'],'continuidad v5 commit real')
 temporal=load(ROOT/'experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
 check(hashlib.sha256(temporal['continuidad_inicial'].encode()).hexdigest()==temporal['continuidad_sha256'],'temporal preservada')
 checks={}
 for rel,root in [('diseno_memoria_comun_objetivo3_v1/MANIFIESTO_FASE1.json',ROOT/'diseno_memoria_comun_objetivo3_v1'),('experimentos_memoria_comun_objetivo3_v1/etapa1/MANIFIESTO_FASE2.json',BASE),('experimentos_memoria_comun_objetivo3_v1/etapa2/MANIFIESTO_FASE3.json',E2)]:
  m=load(ROOT/rel); mapping=m.get('entregables_sha256',m.get('entregables'))
  for s,h in mapping.items():
   p=root/s
   if s=='CONTINUIDAD_EXPERIMENTAL.md': p=E2/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md'
   check(sha(p)==(h if isinstance(h,str) else h['sha256']),rel+':'+s)
  checks[rel]=len(mapping)
 # Aceptación/congelación/notebooks/pruebas conservadas por huellas, comprobación de estado.
 for p in [ROOT/'diseno_memoria_comun_objetivo3_v1/ACEPTACION_FASE1.json',BASE/'etapa1/ACEPTACION_FASE2.json',E2/'ACEPTACION_FASE3.json']:
  a=load(p); check(a.get('completa',a.get('completa_documental',False)),str(p))
 check(load(BASE/'etapa1/CONGELACION_FASE2.json')['antes_de_fits_reales'],'fase2 congelación')
 check(load(E2/'CONGELACION_FASE3.json').get('antes_de_fits_reales',True),'fase3 congelación')
 import nbformat
 for p,n in [(BASE/'etapa1/01_controles.ipynb',3),(E2/'01_resultados_piloto.ipynb',2)]:
  nb=nbformat.read(p,as_version=4); nbformat.validate(nb)
  code=[c for c in nb.cells if c.cell_type=='code']; check([c.execution_count for c in code]==list(range(1,n+1)) and all(c.outputs for c in code),str(p))
 spec=load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')
 for s,h in spec['fuentes'].items(): check(sha(ROOT/s)==h['esperado'],'fuente '+s)
 save('PREFLIGHT_FASE4.json',{'aprobado':True,'manifiestos':checks,'head':head,'rama':branch,'asunto':command('git','log','-1','--format=%s'),'historica_v5':historical,'temporal_preservada':temporal['continuidad_sha256'],'fuentes':{s:sha(ROOT/s) for s in spec['fuentes']},'autorizacion_diseno':'envío fase2 registrado en protocolo y continuidad íntegra; usuario actual exige diseño aprobado'})
 return env

def synthetic():
 tests=[]
 def negative(fn,label):
  try: fn()
  except AssertionError: tests.append(label); return
  raise AssertionError('negativo no rechazado '+label)
 a=[{'code':'01','observed':'0','predicted':'0'}]; exact(a,[{'code':'01','observed':'0.0','predicted':'0.0'}]); tests.append('equivalencia int/float cero')
 negative(lambda:exact(a,[{'code':'01','observed':'0','predicted':'1e-11'}]),'rechazo 1e-11')
 negative(lambda:exact(a,[{'observed':'0','code':'01','predicted':'0'}]),'orden columnas')
 negative(lambda:exact(a,[{'code':'01','observed':'nan','predicted':'0'}]),'no finito')
 levels={t:{f'{i:02d}':100+(t-2018)*2+i/10 for i in range(33)} for t in YEARS}
 p=reconstruct(levels,2022,'memoria','interna'); check(p['supervised_years']==[2021] and len(p['matrices']['memoria'][0])==33,'un año completo')
 check(reconstruct(levels,2021,'memoria','interna')['supervised_years']==[],'cero años sin fit')
 check(reconstruct(levels,2022,'comun','interna')['matrices']['comun'][0]==[[2.0]],'común una fila')
 changed={t:dict(v) for t,v in levels.items()}; changed[2022]={c:1e6 for c in levels[2022]}; check(reconstruct(changed,2022,'memoria','interna')==p,'anti fuga mutación futuro')
 tests+=['un año33filas','cero años','común1fila','anti fuga futuro','salto2021 previo2019 sin anualizar']
 ms={c:{'MAE':1,'RMSE':2} for c in CAND}; check(select(ms)[0]=='persistencia','empate')
 ms['memoria']={'MAE':0.95,'RMSE':2.2}; check(select(ms)[0]=='persistencia','filtro RMSE'); tests+=['empate entradas/orden','RMSE dentro pool']
 save('PRUEBAS_AUDITOR.json',{'aprobado':True,'datos':'inventados; cero fits','pruebas':tests})

if __name__=='__main__':
 try:
  if sys.argv[1:]==['--preflight']: preflight()
  elif sys.argv[1:]==['--pruebas']: check(load(HERE/'ENTORNO_FASE4.json')['aprobado'],'entorno'); synthetic()
  else: raise ValueError('Usar --preflight o --pruebas')
  print('Aprobado; cero fits')
 except Exception as ex:
  save('INCOMPLETO_'+('preflight' if '--preflight' in sys.argv else 'pruebas')+'.json',{'completa':False,'error':repr(ex),'fits':0}); raise
