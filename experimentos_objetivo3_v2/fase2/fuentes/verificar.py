"""Nueve controles reales, con datos agregados estructurales y pruebas sintéticas separadas."""
import sys
sys.dont_write_bytecode=True
import json,math,time,tempfile,subprocess,traceback
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator,RegressorMixin
import configuracion as cfg
from comun import *

class Espia(RegressorMixin,BaseEstimator):
 def fit(self,X,y):self.vistos_=np.array(X);self.y_=np.array(y);return self
 def predict(self,X):return np.repeat(float(self.y_.mean()),len(X))
class Lento(BaseEstimator):
 def fit(self,X,y):time.sleep(5);return self

def rechaza(call,exceptions=(AssertionError,ValueError)):
 try:call()
 except exceptions:return
 raise AssertionError('Entrada inválida fue aceptada')

def sintetico():
 return pd.DataFrame([dict(codigo_departamento=f'{d:02}',anio=a,x=float(i+d),y=float(d*2+i))
  for i,a in enumerate(cfg.ANIOS) for d in range(33)])

def huellas():
 initial=json.loads((cfg.F2/'resultados/integridad_inicial.json').read_text())
 controls=[]
 manifests=[('experimentos_objetivo3_v2/fase1/resultados/manifiesto_cierre.json',initial['commit_partida'])]
 old=json.loads((cfg.ROOT/'experimentos_objetivo3_v2/fase1/resultados/integridad_inicial.json').read_text())
 closures={'protocolo/evidencia/manifiesto_cierre.json':'7e95ffe823c3d08f345620c0f9bc65dc72fae7d5',
  'fase3/resultados/manifiesto_cierre.json':'9a22b8adc406423fa6829b75e77d7473deffe710',
  'fase4/resultados/manifiesto_cierre.json':'da48e1a4f85d206e8753fbad85b78ba2e3858b1a',
  'fase5/resultados/manifiesto_cierre.json':'9becbc3239a540dfa8f31f45c281ac3a61361d19',
  'fase6/resultados/manifiesto_cierre.json':'fc8dc23de8a85cffcc1c87d47ac740650b27ace5'}
 manifests+=list(closures.items())
 for file,commit in manifests:
  manifest=json.loads((cfg.ROOT/file).read_text())
  for p,expected in manifest.get('entregables_sha256',manifest).items():
   current=sha(cfg.ROOT/p);state='vigente coincide'
   if expected!=current:
    assert p=='CONTINUIDAD_OBJETIVO_3.md' or (p=='informe_objetivo_3.md' and file.startswith('fase5')) or p=='experimentos_objetivo3_v2/CONTINUIDAD_V2.md'
    historic=subprocess.check_output(['git','show',f'{commit}:{p}'],cwd=cfg.ROOT)
    assert __import__('hashlib').sha256(historic).hexdigest()==expected
    state='versión histórica cotejada en commit; actual conservada/continuidad v2 autorizada'
   controls.append(dict(manifiesto=file,archivo=p,esperado=expected,actual=current,estado=state,commit_historico=commit))
 for p,spec in old['fuentes'].items():assert sha(cfg.ROOT/p)==spec['sha256']
 return dict(cotejos=len(controls),detalles=controls,fuentes_conservadas=len(old['fuentes']),recenso_raw=False)

def control_panel():
 p=cargar_panel()
 for variant in (pd.concat([p,p.iloc[:1]]),p.iloc[:-1],p.assign(anio=2020),p.assign(ipm=np.nan)):
  rechaza(lambda:validar_panel(variant))
 assert normalizar_codigos(pd.DataFrame({'codigo_departamento':['5','05','8','08']})).codigo_departamento.tolist()==['05','05','08','08']
 rechaza(lambda:normalizar_codigos(pd.DataFrame({'codigo_departamento':['5.5']})))
 return dict(filas=len(p),territorios=p.codigo_departamento.nunique(),por_anio=p.groupby('anio').size().to_dict(),
  historicas_exactas=198,prefijo_literal=True,panel_sha256=sha(cfg.BASE))

def control_union():
 p=cargar_panel();left=p[[*cfg.LLAVES,cfg.RESULTADO]];right=p[[*cfg.LLAVES,*cfg.ESPECIFICACIONES['ambas']]]
 joined=unir(left,right,cfg.ESPECIFICACIONES['ambas']);assert len(joined)==231
 bad=right.copy();bad.loc[0,'codigo_departamento']='99'
 null=right.copy();null.loc[0,'ipm']=np.nan
 for l,r in ((pd.concat([left,left.iloc[:1]]),right),(left,pd.concat([right,right.iloc[:1]])),(left,bad),(left,right.iloc[:-1]),(left,null)):
  rechaza(lambda:unir(l,r,['ipm']))
 return dict(union_validada=231,pruebas_negativas=5,base_unica='panel validado; unión descompuesta solo como control')

def control_agregacion():
 a=agregar([100,200,300]);assert a==dict(n=3,suma=600.0,media=200.0)
 b=agregar([200,300]);assert b['media']==250
 for values in ([100,None,300],[],[0,200],[100,float('inf')]):rechaza(lambda:agregar(values))
 # Periodos desiguales: sumar registros/denominadores, no promediar medias de periodos.
 first=agregar([100]);second=agregar([200,300,400]);annual=(first['suma']+second['suma'])/(first['n']+second['n'])
 assert annual==250 and annual!=(first['media']+second['media'])/2
 return dict(ejemplos_sinteticos=[a,b],media_anual_conocida=annual,nulos_rechazados=True)

def control_temporal():
 p=cargar_panel();s=sintetico();detail=[]
 for w in cfg.ventanas():
  tr,te=dividir(p,w['entrenamiento'],w['externo'])
  synthetic_train,synthetic_test=dividir(s,w['entrenamiento'],w['externo'])
  pipe=Pipeline([('escalado',StandardScaler()),('doble',Espia())])
  pipe.fit(synthetic_train[['x']],synthetic_train.y)
  assert pipe.named_steps['doble'].y_.tolist()==synthetic_train.y.tolist()
  assert pipe.named_steps['escalado'].n_samples_seen_==len(synthetic_train)
  for inner in w['internas']:
   a,b=dividir(tr,inner['entrenamiento'],inner['validacion'])
   assert a.anio.max()<b.anio.min()<w['externo'] and w['externo'] not in set(a.anio)|set(b.anio)
  detail.append(dict(externo=w['externo'],n_train=len(tr),n_externo=len(te),internas=len(w['internas'])))
 rechaza(lambda:dividir(p,[2018,2021],2021))
 rechaza(lambda:dividir(p[p.anio!=2018],[2018],2021))
 return dict(ventanas=detail,ajustes_solo_dobles=True,seleccion_externa_prohibida=True)

def control_escalado():
 s=sintetico();tr,te=dividir(s,[2018,2019],2021)
 def fit(train):
  pipe=Pipeline([('escalado',StandardScaler()),('doble',Espia())]);pipe.fit(train[['x']],train.y);return pipe
 first=fit(tr);poison=s.copy();poison.loc[poison.anio>=2021,['x','y']]=1e100
 tr2,te2=dividir(poison,[2018,2019],2021);second=fit(tr2)
 for attr in ('mean_','scale_','var_'):np.testing.assert_array_equal(getattr(first['escalado'],attr),getattr(second['escalado'],attr))
 np.testing.assert_array_equal(first['doble'].vistos_,second['doble'].vistos_)
 constant=StandardScaler().fit([[5],[5]]);assert constant.scale_[0]==1
 return dict(datos='sintéticos',media=first['escalado'].mean_.tolist(),escala=first['escalado'].scale_.tolist(),extremo_externo=1e100,parametros_inalterados=True,columna_constante_escala=1)

def control_metricas(out):
 rows=[dict(id='doble',externo=2021,codigo_departamento=str(i),anio=2021,observado=y,prediccion=p)
  for i,(y,p) in enumerate(zip([1,2,3],[2,2,1]))]
 file=out/'predicciones_sinteticas.csv';m=guardar_predicciones(file,rows)
 raw=__import__('csv').DictReader(file.open());errors=[];ys=[]
 for r in raw:errors.append(float(r['prediccion'])-float(r['observado']));ys.append(float(r['observado']))
 independent=dict(n=len(errors),mae=sum(abs(e) for e in errors)/3,rmse=math.sqrt(sum(e*e for e in errors)/3),sesgo=sum(errors)/3,
  r2=1-sum(e*e for e in errors)/sum((y-sum(ys)/3)**2 for y in ys))
 for k in m:assert math.isclose(m[k],independent[k],abs_tol=1e-12)
 assert m['mae']==1 and m['r2']==-1.5 and math.isclose(m['rmse'],math.sqrt(5/3))
 assert metricas([1,1],[0,2])['r2'] is None
 rechaza(lambda:metricas([1],[float('nan')]))
 rechaza(lambda:guardar_predicciones(file,rows+rows[:1]))
 assert condicion_personal(10,9.5,True)['entregar']
 assert not condicion_personal(10,9.5001,True)['entregar']
 assert not condicion_personal(10,9,False)['entregar']
 assert not condicion_personal(0,0,True)['entregar']
 return dict(datos='sintéticos',metricas=m,recalculo_independiente=independent,archivo=str(file.relative_to(cfg.F2)),umbral_5_verificado=True)

def control_seleccion():
 def row(id,mae,rmse,n,fam,order,**extra):return dict(id=id,mae=mae,rmse=rmse,n_predictores=n,familia=fam,orden=order,ventanas=2,estado='completo',**extra)
 rows=[row('a',1,2,16,'extra_trees',5),row('b',1.1,2.1,1,'ols',1),row('c',1.100001,0,0,'media',0)]
 assert seleccionar(rows,2)=='b'
 assert seleccionar([row('x',1,2.10001,0,'media',0),row('y',1.05,2,1,'ols',1)],2)=='y'
 assert seleccionar([row('x',1,2,1,'ridge',0),row('y',1,2,1,'ols',1)],2)=='y'
 assert seleccionar([row('x',1,2,1,'ridge',3),row('y',1,2,1,'ridge',2)],2)=='y'
 partial=row('incompleto',0,0,0,'media',0);partial['ventanas']=1
 assert seleccionar(rows+[partial],2)=='b'
 rechaza(lambda:seleccionar([dict(rows[0],mae_externo=0)],2))
 rechaza(lambda:seleccionar([partial],2))
 # Cambiar datos del año externo no aporta argumentos al selector.
 assert seleccionar(rows,2)==seleccionar(list(reversed(rows)),2)
 cs=cfg.candidatos();assert len({c['id'] for c in cs})==100
 from collections import Counter
 counts=Counter(c['especificacion'] for c in cs);assert counts=={None:1,'ipm':33,'tasas':33,'ambas':33}
 frozen=json.loads((cfg.F2/'resultados/configuraciones_congeladas.json').read_text())
 assert len(frozen['configuraciones'])==100 and frozen['ventanas']==cfg.ventanas()
 return dict(pruebas_sinteticas=8,conteos={str(k):v for k,v in counts.items()},reglas='bandas MAE/RMSE 0.1; entradas; familia; orden congelado')

def control_presupuesto(out):
 with tempfile.TemporaryDirectory(prefix='icfes-f2-budget-') as d:
  path=Path(d)/'ledger.json';b=Presupuesto(path,2)
  called=[]
  def executor(remaining,model,X,y):called.append(remaining);return 'doble',0.75
  assert b.ajustar('referencia_doble',None,None,None,executor)=='doble'
  b=Presupuesto(path,2);assert b.data['consumido']==0.75
  b.ajustar('repeticion_doble',None,None,None,executor)
  rechaza(lambda:b.ajustar('tercero',None,None,None,executor),(TimeoutError,))
  n=len(called);rechaza(lambda:b.ajustar('prohibido',None,None,None,executor),(TimeoutError,));assert len(called)==n
  ledger=b.data
  pending=Path(d)/'pending.json';guardar(pending,dict(limite=2.,consumido=0.,pendiente=True,ajustes=[]))
  assert Presupuesto(pending,2).data['consumido']==2
  rechaza(lambda:Presupuesto(path,3))
  # Terminación real de proceso con doble lento; jamás modelo candidato.
  real=Presupuesto(Path(d)/'real.json',1.5)
  rechaza(lambda:real.ajustar('doble_lento',Lento(),[[0]],[0]),(TimeoutError,))
  assert real.data['consumido']==1.5
  real_ledger=real.data
 guardar(out/'presupuesto_sintetico.json',dict(virtual=ledger,proceso_real_doble=real_ledger,limite_piloto=cfg.LIMITE_SEGUNDOS))
 return dict(datos='dobles sintéticos',virtual=ledger,proceso_interrumpido=real_ledger,presupuesto_panel_consumido=0)

def control_notebook():
 import nbformat,re
 source=cfg.F2/'fuentes/01_protocolo_verificacion.py';nbpath=cfg.F2/'notebooks/01_protocolo_verificacion.ipynb'
 nb=nbformat.read(nbpath,as_version=4);nbformat.validate(nb)
 chunks=re.split(r'^# %%([^\n]*)\n',source.read_text(),flags=re.M)
 expected=[body.strip() for flag,body in zip(chunks[1::2],chunks[2::2])]
 assert [c.source for c in nb.cells]==expected
 for c in nb.cells:
  if c.cell_type=='code':compile(c.source,str(source),'exec');assert '/home/' not in c.source and 'fit(' not in c.source
 assert 'raw_data' not in '\n'.join(expected)
 return dict(validacion_nbformat=True,fuente_editable_coincide=True,celdas=len(nb.cells),datos_personales=False,ejecucion_kernel='resultado separado verificacion_notebook.json al terminar generador')

def ejecutar_verificacion(output='controles.json'):
 out=cfg.F2/'resultados';out.mkdir(exist_ok=True)
 freeze=json.loads((out/'congelacion_previa.json').read_text())
 assert sha(cfg.F2/'PROTOCOLO_V2.md')==freeze['protocolo_sha256']
 assert sha(out/'configuraciones_congeladas.json')==freeze['configuraciones_sha256']
 for p,h in freeze['fuentes_sha256'].items():assert sha(cfg.ROOT/p)==h
 tests=[control_panel,control_union,control_agregacion,control_temporal,control_escalado,
        lambda:control_metricas(out),control_seleccion,lambda:control_presupuesto(out),control_notebook]
 names=['panel_conservacion','union','agregacion','separacion_temporal','escalado','metricas','seleccion_desempates','presupuesto','notebook']
 results=[]
 for number,(name,test) in enumerate(zip(names,tests),1):
  start=time.monotonic()
  try:detail=test();results.append(dict(control=number,nombre=name,aprobado=True,evidencia=detail,segundos=time.monotonic()-start))
  except BaseException:
   results.append(dict(control=number,nombre=name,aprobado=False,traceback=traceback.format_exc()))
   guardar(out/output,dict(aprobado=False,controles=results));raise
 previous=huellas();guardar(out/'huellas_anteriores.json',previous)
 report=dict(aprobado=True,controles=results,controles_aprobados=9,huellas_previas=previous['cotejos'],
  ajustes_candidatos_panel=0,predicciones_panel=0,simulaciones=0,pruebas_sinteticas=True,pdf_leidos=[])
 guardar(out/output,report)
 print('9 controles aprobados; cero ajustes y predicciones sobre el panel real.')
 return report
if __name__=='__main__':ejecutar_verificacion()
