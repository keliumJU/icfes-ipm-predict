"""Orquestación serial v2: reutiliza construcción, partición, selección y ledger de fase2."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'experimentos_objetivo3_v2/fase2/fuentes'))
import json,traceback,platform,importlib.metadata as md,subprocess,time
from datetime import datetime,timezone
import numpy as np,pandas as pd,joblib
import configuracion as cfg
from comun import sha,guardar,cargar_panel,dividir,metricas,seleccionar,Presupuesto
from congelar import serial
F3=ROOT/'experimentos_objetivo3_v2/fase3'
CONFIG=cfg.F2/'resultados/configuraciones_congeladas.json'

def read(p):return json.loads(Path(p).read_text())
def inputs(p,c):return p[c['entradas']].to_numpy(float) if c.get('entradas') else np.zeros((len(p),1))
def now():return datetime.now(timezone.utc).isoformat()

def preflight():
 out=F3/'resultados';snapshot={p:sha(ROOT/p) for p in subprocess.check_output(['git','ls-files'],cwd=ROOT).decode().splitlines() if (ROOT/p).is_file()}
 manifest=read(cfg.F2/'resultados/manifiesto_cierre.json')
 for p,h in manifest['entregables_sha256'].items():assert sha(ROOT/p)==h,p
 freeze=read(cfg.F2/'resultados/congelacion_previa.json')
 for p,h in freeze['fuentes_sha256'].items():assert sha(ROOT/p)==h,p
 assert sha(CONFIG)==freeze['configuraciones_sha256'] and sha(cfg.F2/'PROTOCOLO_V2.md')==freeze['protocolo_sha256']
 versions={line.split('==')[0]:md.version(line.split('==')[0]) for line in (cfg.F2/'requirements.lock.txt').read_text().splitlines()}
 assert all(versions[l.split('==')[0]]==l.split('==')[1] for l in (cfg.F2/'requirements.lock.txt').read_text().splitlines())
 assert platform.python_version()=='3.12.14'
 p=cargar_panel();conf=read(CONFIG)
 assert len(conf['configuraciones'])==100 and conf['ventanas']==cfg.ventanas()
 for c in conf['configuraciones']+[conf['referencia_historica']]:assert serial(cfg.construir(c).get_params(deep=True))==c['parametros_completos']
 guardar(out/'integridad_inicial.json',dict(commit_partida=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),rama=subprocess.check_output(['git','branch','--show-current']).decode().strip(),git_inicial=subprocess.check_output(['git','status','--porcelain']).decode(),snapshot_versionados=snapshot,manifest_fase2_verificado=len(manifest['entregables_sha256']),panel_sha=sha(cfg.BASE),filas=len(p),historicas_exactas=198,territorios_por_anio=33,pdf_leidos=[]))
 guardar(out/'entorno.json',dict(python=platform.python_version(),ejecutable=sys.executable,paquetes=versions,pip_check=subprocess.check_output([sys.executable,'-m','pip','check']).decode().strip(),preparacion='Entorno fase2 existente comprobado; sin instalación ni red.',semilla=cfg.SEMILLA))
 print('Preflight aprobado: manifiesto, panel, parámetros y lock exactos.',flush=True)

class Runner:
 def __init__(self,out,panel,conf,executor=None,limit=7200):
  self.out=Path(out);self.out.mkdir(parents=True,exist_ok=True);self.panel=panel;self.conf=conf;self.executor=executor
  self.budget=Presupuesto(self.out/'ledger.json',limit);self.versions=platform.python_version();self.byid={c['id']:c for c in conf['configuraciones']}
  ref=conf['referencia_historica'].copy();ref['entradas']=conf['especificaciones']['ambas'];self.byid[ref['id']]=ref
 def fit(self,label,c,train):
  target=self.out/'ajustes'/label;target.mkdir(parents=True,exist_ok=True);meta=target/'ajuste.json';artifact=target/'modelo.joblib'
  if meta.exists():
   old=read(meta)
   if old['estado']=='ok':assert sha(artifact)==old['modelo_sha256'];return joblib.load(artifact),old
   if old['estado'] in ('numerico','limite'):return None,old
  base=dict(id=c['id'],etiqueta=label,entrenamiento=sorted(train.anio.unique().tolist()),llaves_entrenamiento=train[cfg.LLAVES].values.tolist(),n=len(train),parametros_completos=c['parametros_completos'],entradas=c.get('entradas',[]),semilla=cfg.SEMILLA,origen='sintetico' if self.executor else 'real',panel_sha256=self.conf.get('panel_sha256'),versiones_sha256=sha(F3/'resultados/entorno.json'),congelacion_sha256=sha(F3/'resultados/congelacion_operativa.json') if (F3/'resultados/congelacion_operativa.json').exists() else None)
  for attempt in range(2):
   try:
    result=self.budget.ajustar(label+f'_intento{attempt+1}',cfg.construir(c),inputs(train,c),train[cfg.RESULTADO].to_numpy(float),executor=self.executor)
    model,captured=result
    joblib.dump(model,artifact,compress=3)
    transform={}
    if hasattr(model,'named_steps'):
     s=model.named_steps['escalado'];transform=dict(mean=s.mean_.tolist(),scale=s.scale_.tolist(),var=s.var_.tolist(),n_samples_seen=int(s.n_samples_seen_))
     np.testing.assert_allclose(s.mean_,inputs(train,c).mean(axis=0),rtol=1e-12,atol=1e-12)
    info={**base,'estado':'ok','advertencias':captured,'transformacion_ajustada':transform,'modelo_sha256':sha(artifact),'tiempo':self.budget.data['ajustes'][-1],'intento':attempt+1}
    guardar(meta,info);return model,info
   except BaseException as e:
    numerical=isinstance(e,(ValueError,FloatingPointError)) or 'convergencia' in str(e)
    state='limite' if isinstance(e,TimeoutError) else 'numerico' if numerical else 'infraestructura'
    info={**base,'estado':state,'traceback':traceback.format_exc(),'intento':attempt+1,'tiempo':self.budget.data['ajustes'][-1] if self.budget.data['ajustes'] else None}
    guardar(target/f'fallo_{attempt+1}.json',info);guardar(meta,info)
    if state=='limite':raise
    if numerical:return None,info
    if attempt:raise
 def predict(self,label,c,train,test):
  target=self.out/'ajustes'/label;file=target/'predicciones.csv'
  if file.exists():
   info=read(target/'ajuste.json');assert sha(file)==info['predicciones_sha256'];return pd.read_csv(file,dtype={'codigo_departamento':str},float_precision='round_trip')
  model,info=self.fit(label,c,train)
  if model is None:return None
  pred=model.predict(inputs(test,c))
  if not np.isfinite(pred).all():
   guardar(target/'prediccion_no_finita.json',dict(etiqueta=label,prediccion=repr(pred)));return None
  frame=test[cfg.LLAVES].copy();frame['id']=c['id'];frame['ajuste']=label;frame['observado']=test[cfg.RESULTADO].to_numpy();frame['prediccion']=pred;frame['error']=pred-frame.observado;frame['origen']='sintetico' if self.executor else 'real'
  frame.to_csv(file,index=False,float_format='%.17g');info['predicciones_sha256']=sha(file);info['fuera_0_500']=int(((pred<0)|(pred>500)).sum());guardar(target/'ajuste.json',info);return frame
 def window(self,w):
  year=w['externo'];scores=[];expected=[i['validacion'] for i in w['internas']]
  # Selector receives ONLY internal saved predictions and metrics.
  for c in self.conf['configuraciones']:
   parts=[];valid=[]
   for internal in w['internas']:
    tr,te=dividir(self.panel,internal['entrenamiento'],internal['validacion'])
    p=self.predict(f"e{year}_i{internal['validacion']}_{c['id']}",c,tr,te)
    if p is not None:parts.append(p);valid.append(internal['validacion'])
   score=dict(id=c['id'],familia=c['familia'],especificacion=c['especificacion'],n_predictores=len(c['entradas']),orden=c['orden'],ventanas=valid,estado='completo' if valid==expected else 'inelegible')
   if valid==expected:
    joined=pd.concat(parts);score.update(metricas(joined.observado,joined.prediccion))
   scores.append(score)
  selection=self.out/f'seleccion_{year}.json'
  decision=dict(externo=year,global_id=seleccionar(scores,expected),especificaciones={s:seleccionar([r for r in scores if r['especificacion'] in (None,s)],expected) for s in self.conf['especificaciones']},metricas_internas=scores,instante_antes_evaluacion=now(),congelacion_sha256=sha(F3/'resultados/congelacion_operativa.json') if (F3/'resultados/congelacion_operativa.json').exists() else None)
  if selection.exists():old=read(selection);assert old['global_id']==decision['global_id'] and old['especificaciones']==decision['especificaciones'];decision=old
  else:guardar(selection,decision)
  roles={'procedimiento_v2':decision['global_id'],**{f'procedimiento_{s}':v for s,v in decision['especificaciones'].items()},'media':'media',**{c['id']:c['id'] for c in self.conf['configuraciones'] if c['familia']=='ols'},'referencia_v1':'referencia_v1'}
  tr,te=dividir(self.panel,w['entrenamiento'],year);preds={}
  ordered=[c['id'] for c in self.conf['configuraciones'] if c['id'] in roles.values()]+['referencia_v1']
  for ident in ordered:
   p=self.predict(f'e{year}_externo_{ident}',self.byid[ident],tr,te)
   if p is None:raise RuntimeError('Referencia/ganador externo fallido: '+ident)
   preds[ident]=p
  rows=[]
  for role,ident in roles.items():
   p=preds[ident].copy();p['procedimiento']=role;p['externo']=year;p['seleccion_sha256']=sha(selection);rows.append(p)
  pd.concat(rows).to_csv(self.out/f'externas_{year}.csv',index=False,float_format='%.17g')
  print(f'Externo {year} completado; ajustes acumulados {len(self.budget.data["ajustes"])}; {self.budget.data["consumido"]:.1f}s.',flush=True)
 def run(self):
  for w in self.conf['ventanas']:self.window(w)
  repeats=[]
  for w in self.conf['ventanas']:
   year=w['externo'];winner=read(self.out/f'seleccion_{year}.json')['global_id'];tr,te=dividir(self.panel,w['entrenamiento'],year)
   for ident in (winner,'referencia_v1'):
    new=self.predict(f'e{year}_repeticion_{ident}',self.byid[ident],tr,te)
    original=pd.read_csv(self.out/'ajustes'/f'e{year}_externo_{ident}'/'predicciones.csv',float_precision='round_trip')
    assert new is not None
    delta=float(np.max(np.abs(new.prediccion.to_numpy()-original.prediccion.to_numpy())))
    assert np.allclose(new.prediccion,original.prediccion,atol=1e-10,rtol=0)
    repeats.append(dict(externo=year,id=ident,max_diferencia=delta))
  guardar(self.out/'reproducibilidad.json',dict(aprobado=True,repeticiones=repeats))
  guardar(self.out/'estado.json',dict(completo=True,consumido=self.budget.data['consumido'],ajustes=len(self.budget.data['ajustes']),terminado=now()))

def freeze():
 guardar(F3/'resultados/congelacion_operativa.json',dict(instante=now(),codigo={str(p.relative_to(ROOT)):sha(p) for p in sorted((F3/'fuentes').glob('*.py'))},configuraciones_sha256=sha(CONFIG),panel_sha256=sha(cfg.BASE),entorno_sha256=sha(F3/'resultados/entorno.json'),pruebas_sha256=sha(F3/'resultados/pruebas_sinteticas.json'),semilla=cfg.SEMILLA,limite=7200,orden='externos crecientes; JSON candidatos; internas crecientes; selección persistida; externos por JSON; v1; diez repeticiones al final',motor='comun.Presupuesto spawn, serial, worker solo entrenamiento'))

def main():
 if '--preflight' in sys.argv:preflight();return
 if '--freeze' in sys.argv:freeze();return
 frozen=read(F3/'resultados/congelacion_operativa.json')
 for p,h in frozen['codigo'].items():assert sha(ROOT/p)==h,p
 assert sha(CONFIG)==frozen['configuraciones_sha256'] and sha(cfg.BASE)==frozen['panel_sha256']
 runner=Runner(F3/'resultados/piloto',cargar_panel(),read(CONFIG))
 try:runner.run()
 except BaseException:
  guardar(runner.out/'estado.json',dict(completo=False,consumido=runner.budget.data['consumido'],ajustes=len(runner.budget.data['ajustes']),traceback=traceback.format_exc()));raise
if __name__=='__main__':main()
