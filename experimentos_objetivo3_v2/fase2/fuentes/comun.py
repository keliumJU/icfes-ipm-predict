"""Funciones compartidas. Ninguna operación predictiva sobre panel real en fase 2."""
import sys
sys.dont_write_bytecode=True
import json,hashlib,math,time,multiprocessing,traceback,warnings
from pathlib import Path
import numpy as np
import pandas as pd
import configuracion as cfg

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()

def guardar(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n');tmp.replace(path)

def cargar_panel():
 assert sha(cfg.BASE)==cfg.BASE_SHA
 assert sha(cfg.HISTORICO)==cfg.HISTORICO_SHA
 original=cfg.HISTORICO.read_bytes().splitlines(keepends=True)
 assert cfg.BASE.read_bytes().splitlines(keepends=True)[:199]==original
 panel=normalizar_codigos(pd.read_csv(cfg.BASE,dtype={'codigo_departamento':str},float_precision='round_trip'))
 validar_panel(panel)
 historical=normalizar_codigos(pd.read_csv(cfg.HISTORICO,dtype={'codigo_departamento':str},float_precision='round_trip'))
 pd.testing.assert_frame_equal(panel.iloc[:198].reset_index(drop=True),historical)
 return panel

def normalizar_codigos(p):
 p=p.copy()
 codes=p.codigo_departamento.astype(str)
 if not codes.str.fullmatch(r'[0-9]{1,2}').all():raise ValueError('código no entero de uno/dos dígitos')
 p['codigo_departamento']=codes.str.zfill(2)
 return p

def validar_panel(p):
 assert len(p)==231 and not p.duplicated(cfg.LLAVES).any()
 assert set(p.anio)==set(cfg.ANIOS)
 territory=set(p.codigo_departamento)
 assert territory==set('05 08 11 13 15 17 18 19 20 23 25 27 41 44 47 50 52 54 63 66 68 70 73 76 81 85 86 88 91 94 95 97 99'.split())
 for year,g in p.groupby('anio'):assert len(g)==33 and set(g.codigo_departamento)==territory
 mandatory=[*cfg.ESPECIFICACIONES['ambas'],cfg.RESULTADO,'n_punt_global','n_estudiantes_saber']
 assert not p[mandatory].isna().any().any()
 assert np.isfinite(p[mandatory].to_numpy(dtype=float)).all()
 assert p[cfg.ESPECIFICACIONES['ambas']].ge(0).all().all() and p[cfg.ESPECIFICACIONES['ambas']].le(100).all().all()
 assert p[cfg.RESULTADO].gt(0).all() and p[cfg.RESULTADO].le(500).all()
 assert p.n_punt_global.gt(0).all() and (p.n_punt_global==p.n_estudiantes_saber).all()
 assert (p.n_punt_global%1==0).all()

def unir(left,right,required):
 left=normalizar_codigos(left);right=normalizar_codigos(right)
 for p in (left,right):
  if p[cfg.LLAVES].isna().any().any() or p.duplicated(cfg.LLAVES).any():raise ValueError('llave ausente/duplicada')
 if set(map(tuple,left[cfg.LLAVES].to_numpy()))!=set(map(tuple,right[cfg.LLAVES].to_numpy())):raise ValueError('llaves sin correspondencia')
 joined=left.merge(right,on=cfg.LLAVES,validate='one_to_one')
 if joined[required].isna().any().any():raise ValueError('entrada indispensable ausente')
 return joined

def agregar(values):
 # Valores recibidos de casos elegibles; nulos son error, jamás ceros/denominadores ocultos.
 v=np.asarray(values,dtype=float)
 if not len(v) or not np.isfinite(v).all() or (v<=0).any():raise ValueError('casos elegibles incompletos')
 return {'n':len(v),'suma':float(v.sum()),'media':float(v.mean())}

def dividir(p,train_years,test_year):
 assert set(train_years) <= set(cfg.ANIOS) and test_year in cfg.ANIOS
 assert train_years and max(train_years)<test_year
 train=p[p.anio.isin(train_years)].sort_values(cfg.LLAVES).copy()
 test=p[p.anio==test_year].sort_values(cfg.LLAVES).copy()
 assert len(train)==33*len(train_years) and len(test)==33
 assert set(train.anio)==set(train_years) and set(test.anio)=={test_year}
 assert not set(map(tuple,train[cfg.LLAVES].to_numpy())) & set(map(tuple,test[cfg.LLAVES].to_numpy()))
 return train,test

def metricas(y,pred):
 y=np.asarray(y,float);pred=np.asarray(pred,float)
 if y.shape!=pred.shape or y.ndim!=1 or not len(y) or not np.isfinite(y).all() or not np.isfinite(pred).all():raise ValueError('predicciones invalidas')
 e=pred-y;den=float(np.sum((y-y.mean())**2))
 return dict(n=len(y),mae=float(np.mean(np.abs(e))),rmse=float(np.sqrt(np.mean(e**2))),
             sesgo=float(e.mean()),r2=None if den==0 else float(1-np.sum(e**2)/den))

def guardar_predicciones(path,rows):
 p=pd.DataFrame(rows)
 if p.duplicated(['id','externo',*cfg.LLAVES]).any():raise ValueError('predicciones duplicadas')
 metricas(p.observado,p.prediccion)
 p.to_csv(path,index=False,float_format='%.17g')
 return metricas(pd.read_csv(path,float_precision='round_trip').observado,pd.read_csv(path,float_precision='round_trip').prediccion)

def seleccionar(rows,expected_windows):
 # Solo recibir métricas internas; campos externos deliberadamente prohibidos.
 eligible=[]
 ids=set()
 for r in rows:
  if 'mae_externo' in r or 'y_externo' in r:raise ValueError('fuga de evaluación externa')
  if r['id'] in ids:raise ValueError('ID duplicado')
  ids.add(r['id'])
  if r.get('estado')=='completo' and r.get('ventanas')==expected_windows and all(math.isfinite(r[k]) for k in ('mae','rmse')):eligible.append(r)
 if not eligible:raise ValueError('sin candidatos completos')
 minimum=min(r['mae'] for r in eligible);eligible=[r for r in eligible if r['mae']<=minimum+cfg.TOL_MAE]
 minimum=min(r['rmse'] for r in eligible);eligible=[r for r in eligible if r['rmse']<=minimum+cfg.TOL_RMSE]
 return min(eligible,key=lambda r:(r['n_predictores'],cfg.ORDEN.index(r['familia']),r['orden']))['id']

def condicion_personal(mae_ref,mae_v2,completo):
 if not completo or not math.isfinite(mae_ref) or not math.isfinite(mae_v2) or mae_ref<=0:return dict(entregar=False,mejora=None)
 improvement=100*(mae_ref-mae_v2)/mae_ref
 return dict(entregar=improvement>=5,mejora=improvement)

def _worker(conn,estimator,X,y):
 try:
  from threadpoolctl import threadpool_limits
  with threadpool_limits(limits=1),warnings.catch_warnings(record=True) as captured:
   warnings.simplefilter('always');estimator.fit(X,y)
  conn.send(('ok',estimator,[dict(categoria=w.category.__name__,mensaje=str(w.message)) for w in captured]))
 except BaseException:conn.send(('error',traceback.format_exc(),[]))
 finally:conn.close()

class Presupuesto:
 """Ledger persistente, serial, reloj monotónico. Un proceso puede ser interrumpido."""
 def __init__(self,path,limit=cfg.LIMITE_SEGUNDOS):
  self.path=Path(path);self.limit=float(limit)
  if not math.isfinite(self.limit) or self.limit<=0:raise ValueError('límite inválido')
  self.data=json.loads(self.path.read_text()) if self.path.exists() else dict(limite=self.limit,consumido=0.0,pendiente=False,ajustes=[])
  if self.data['limite']!=self.limit:raise ValueError('presupuesto no ampliable')
  if self.data['pendiente']:
   # Tras caída no se puede demostrar duración: agotar de forma conservadora.
   self.data['consumido']=self.limit;self.data['pendiente']=False
   self.data['ajustes'].append(dict(estado='interrupcion_no_medida',segundos=None));guardar(self.path,self.data)
 def ajustar(self,label,estimator,X,y,executor=None):
  remaining=self.limit-self.data['consumido']
  if remaining<=0:raise TimeoutError('presupuesto agotado')
  self.data['pendiente']=True;guardar(self.path,self.data)
  started=time.monotonic();state='error';duration=None
  try:
   if executor is not None:
    # Doble inyectado únicamente por pruebas: duración y límite controlados.
    result,duration=executor(remaining,estimator,X,y)
    if duration<0 or not math.isfinite(duration):raise ValueError('duración inválida')
    if duration>=remaining:raise TimeoutError('límite del doble')
    state='ok';return result
   ctx=multiprocessing.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
   process=ctx.Process(target=_worker,args=(child,estimator,X,y));process.start();child.close()
   try:
    if not parent.poll(max(0,remaining-(time.monotonic()-started))):raise TimeoutError('límite entrenamiento')
    status,result,captured=parent.recv()
    if status!='ok':raise RuntimeError(result)
    if any(w['categoria']=='ConvergenceWarning' for w in captured):raise RuntimeError('convergencia no satisfecha: '+str(captured))
    state='ok';return result,captured
   finally:
    if process.is_alive():process.terminate()
    process.join();parent.close()
  except TimeoutError:
   state='limite';raise
  finally:
   elapsed=duration if duration is not None else time.monotonic()-started
   self.data['consumido']=min(self.limit,self.data['consumido']+elapsed)
   if state=='limite':self.data['consumido']=self.limit
   self.data['pendiente']=False
   self.data['ajustes'].append(dict(etiqueta=label,estado=state,segundos=elapsed))
   guardar(self.path,self.data)
