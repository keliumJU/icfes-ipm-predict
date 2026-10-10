"""Pruebas previas: datos sintéticos y dobles, jamás errores del panel real."""
import sys
sys.dont_write_bytecode=True
from piloto import *
import tempfile,copy,warnings

from sklearn.base import BaseEstimator
class Lento(BaseEstimator):
 def fit(self,X,y):time.sleep(10);return self

def double(remaining,model,X,y):
 assert len(X)==len(y)
 with warnings.catch_warnings(record=True) as captured:
  warnings.simplefilter('always');model.fit(X,y)
 return (model,[dict(categoria=w.category.__name__,mensaje=str(w.message)) for w in captured]),0.01

def test():
 conf=read(CONFIG);conf['configuraciones']=[c for c in conf['configuraciones'] if c['id'] in ('media','ols_ipm_00')];conf['ventanas']=conf['ventanas'][:2]
 p=cargar_panel().copy()
 # Descartar todos los valores reales excepto llaves estructurales.
 for j,col in enumerate(cfg.ESPECIFICACIONES['ambas']):p[col]=np.arange(len(p))%27+j*0.01
 p[cfg.RESULTADO]=200.+np.arange(len(p))%11
 with tempfile.TemporaryDirectory(dir='/tmp') as temp:
  r=Runner(temp,p,conf,double);r.run();spent=r.budget.data['consumido'];count=len(r.budget.data['ajustes']);r2=Runner(temp,p,conf,double);r2.run()
  assert spent==r2.budget.data['consumido'] and count==len(r2.budget.data['ajustes'])
  before=read(Path(temp)/'seleccion_2021.json')
  changed=p.copy();changed.loc[changed.anio==2021,cfg.RESULTADO]=1e20
  changed.loc[changed.anio==2021,cfg.ESPECIFICACIONES['ambas']]=1e20
  other=Path(temp)/'extreme';rr=Runner(other,changed,conf,double);rr.window(conf['ventanas'][0]);after=read(other/'seleccion_2021.json')
  assert before['metricas_internas']==after['metricas_internas'] and before['global_id']==after['global_id']
  # Guardados antes de externos, mismos artefactos al reanudar, claves independientes.
  assert all(read(f)['origen']=='sintetico' for f in Path(temp).glob('ajustes/*/ajuste.json'))
  limit=Presupuesto(Path(temp)/'limite.json',0.015);c=conf['configuraciones'][0]
  limit.ajustar('primero',cfg.construir(c),np.zeros((2,1)),np.array([1.,2.]),executor=double)
  try:limit.ajustar('segundo',cfg.construir(c),np.zeros((2,1)),np.array([1.,2.]),executor=double);raise AssertionError('No detuvo')
  except TimeoutError:pass
  resumed=Presupuesto(Path(temp)/'limite.json',0.015);assert resumed.data['consumido']==0.015
  try:resumed.ajustar('prohibido',cfg.construir(c),None,None);raise AssertionError('Reinicio')
  except TimeoutError:pass
  crash=Path(temp)/'caida.json';guardar(crash,dict(limite=1.0,consumido=0.1,pendiente=True,ajustes=[]));assert Presupuesto(crash,1).data['consumido']==1
  # Worker real: solo datos sintéticos; prueba separación/persistencia de Pipeline.
  real=Runner(Path(temp)/'worker',p,conf,limit=30);tr,te=dividir(p,[2018],2019)
  pred=real.predict('synthetic_worker',conf['configuraciones'][1],tr,te);assert len(pred)==33
  info=read(real.out/'ajustes/synthetic_worker/ajuste.json');assert info['transformacion_ajustada']['n_samples_seen']==33
  interrupt=Presupuesto(Path(temp)/'interrumpible.json',1.5)
  try:interrupt.ajustar('lento_sintetico',Lento(),[[0]],[0]);raise AssertionError('No terminó proceso')
  except TimeoutError:pass
  assert interrupt.data['consumido']==1.5
  termination=interrupt.data['ajustes'][-1]['segundos']
  proof=dict(terminacion_proceso_sintetico_segundos=termination,aprobado=True,origen='datos_sinteticos_y_dobles',controles=['orquestacion ventanas y selección','extremo externo sin influencia en selección','selección persistida antes de externos','artefactos y huellas','reanudación sin ajustes duplicados','presupuesto global persistente y límite','caída pendiente agota saldo','worker real con Pipeline y entrenamiento exclusivo'],ajustes_panel_real=0,segundos_presupuesto_panel=0,ajustes_dobles=count,worker_sintetico_segundos=real.budget.data['consumido'],pdf_leidos=[])
 guardar(F3/'resultados/pruebas_sinteticas.json',proof);print('Pruebas sintéticas aprobadas.',flush=True)
if __name__=='__main__':test()
