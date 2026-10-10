"""Recálculo independiente desde CSV guardados; no ajusta ningún estimador."""
from piloto import *
import math,csv

def independent(y,p):
 y=list(map(float,y));p=list(map(float,p));n=len(y);assert n and len(p)==n
 assert all(math.isfinite(v) for v in y+p)
 e=[b-a for a,b in zip(y,p)];mean=math.fsum(y)/n;den=math.fsum((v-mean)**2 for v in y)
 return dict(n=n,mae=math.fsum(abs(v) for v in e)/n,rmse=math.sqrt(math.fsum(v*v for v in e)/n),sesgo=math.fsum(e)/n,r2=None if den==0 else 1-math.fsum(v*v for v in e)/den)

def same(a,b):
 for key in ('mae','rmse','sesgo','r2'):
  if a[key] is None:assert b[key] is None
  else:assert math.isclose(a[key],b[key],abs_tol=1e-10,rel_tol=1e-12),(key,a,b)

def select(rows):
 eligible=[r for r in rows if r['estado']=='completo'];best=min(r['mae'] for r in eligible);eligible=[r for r in eligible if r['mae']<=best+0.1];best=min(r['rmse'] for r in eligible);eligible=[r for r in eligible if r['rmse']<=best+0.1]
 return min(eligible,key=lambda r:(r['n_predictores'],cfg.ORDEN.index(r['familia']),r['orden']))['id']

def verify():
 out=F3/'resultados';run=out/'piloto';p=cargar_panel();conf=read(CONFIG);state=read(run/'estado.json');byid={c['id']:c for c in conf['configuraciones']};ref=conf['referencia_historica'].copy();ref['entradas']=conf['especificaciones']['ambas'];byid[ref['id']]=ref
 versions=read(out/'entorno.json');ledger=read(run/'ledger.json');assert not ledger['pendiente']
 elapsed=math.fsum(a['segundos'] for a in ledger['ajustes'] if a['segundos'] is not None)
 assert ledger['consumido']<=7200
 fits=[];failure=[];prediction_count=0;internal_all=[];selections=[]
 for meta in sorted((run/'ajustes').glob('*/ajuste.json')):
  info=read(meta);fits.append(info);assert info['origen']=='real';assert info['semilla']==20261010
  assert info['parametros_completos']==byid[info['id']]['parametros_completos']
  assert info['versiones_sha256']==sha(out/'entorno.json') and info['congelacion_sha256']==sha(out/'congelacion_operativa.json')
  tr=p[p.anio.isin(info['entrenamiento'])].sort_values(cfg.LLAVES);assert tr[cfg.LLAVES].values.tolist()==info['llaves_entrenamiento']
  if info['estado']!='ok':failure.append(info);continue
  assert sha(meta.parent/'modelo.joblib')==info['modelo_sha256']
  transform=info['transformacion_ajustada']
  if transform:
   X=tr[info['entradas']].to_numpy(float);assert transform['n_samples_seen']==len(tr)
   np.testing.assert_allclose(transform['mean'],X.mean(0),atol=1e-12,rtol=1e-12);np.testing.assert_allclose(transform['var'],X.var(0),atol=1e-10,rtol=1e-12)
  file=meta.parent/'predicciones.csv'
  if not file.exists():continue
  assert sha(file)==info['predicciones_sha256'];pred=pd.read_csv(file,dtype={'codigo_departamento':str},float_precision='round_trip');assert len(pred)==33 and not pred.duplicated(cfg.LLAVES).any();assert pred.origen.eq('real').all()
  assert max(info['entrenamiento'])<pred.anio.min();test=p[p.anio==int(pred.anio.iloc[0])].sort_values(cfg.LLAVES)
  assert pred[cfg.LLAVES].values.tolist()==test[cfg.LLAVES].values.tolist();np.testing.assert_array_equal(pred.observado,test[cfg.RESULTADO]);np.testing.assert_allclose(pred.error,pred.prediccion-pred.observado,atol=1e-12,rtol=1e-12)
  prediction_count+=len(pred)
  if '_i' in info['etiqueta'] and '_intento' not in info['etiqueta']:
   pred['externo']=int(info['etiqueta'].split('_')[0][1:]);internal_all.append(pred)
 for w in conf['ventanas']:
  selection=run/f"seleccion_{w['externo']}.json"
  if not selection.exists():continue
  s=read(selection);selections.append(s)
  for score in s['metricas_internas']:
   files=[run/'ajustes'/f"e{w['externo']}_i{i['validacion']}_{score['id']}"/'predicciones.csv' for i in w['internas']]
   if score['estado']=='completo':
    q=pd.concat([pd.read_csv(f,float_precision='round_trip') for f in files]);assert len(q)==33*len(w['internas']);same(independent(q.observado,q.prediccion),score)
  assert s['global_id']==select(s['metricas_internas'])
  for spec,ident in s['especificaciones'].items():assert ident==select([r for r in s['metricas_internas'] if r['especificacion'] in (None,spec)])
 if internal_all:pd.concat(internal_all).to_csv(out/'predicciones_internas.csv',index=False,float_format='%.17g')
 extfiles=sorted(run.glob('externas_*.csv'));ext=pd.concat([pd.read_csv(f,dtype={'codigo_departamento':str},float_precision='round_trip') for f in extfiles]) if extfiles else pd.DataFrame()
 complete=bool(state['completo']);summary={};metrics=[];coverage={}
 if len(ext):
  assert not ext.duplicated(['procedimiento',*cfg.LLAVES]).any()
  for role,g in ext.groupby('procedimiento'):
   keys=set(map(tuple,g[cfg.LLAVES].values));coverage[role]=len(keys)
   if complete:assert len(g)==165 and keys==set(map(tuple,p[p.anio.isin(range(2021,2026))][cfg.LLAVES].values))
   for scope,groupcol in [('conjunto',None),('anual','anio'),('territorial','codigo_departamento')]:
    groups=[('todos',g)] if groupcol is None else g.groupby(groupcol)
    for key,z in groups:
     m=independent(z.observado,z.prediccion);metrics.append(dict(procedimiento=role,ambito=scope,grupo=str(key),**m))
     if scope=='conjunto':summary[role]=m
  for row in ext.itertuples():
   selection=run/f'seleccion_{row.externo}.json';assert row.seleccion_sha256==sha(selection)
   src=run/'ajustes'/row.ajuste/'predicciones.csv';q=pd.read_csv(src,dtype={'codigo_departamento':str},float_precision='round_trip');z=q[q.codigo_departamento==row.codigo_departamento];assert len(z)==1 and float(z.prediccion.iloc[0])==row.prediccion
  ext.to_csv(out/'predicciones_externas.csv',index=False,float_format='%.17g')
 pd.DataFrame(metrics).to_csv(out/'metricas.csv',index=False,float_format='%.17g');guardar(out/'fallos.json',dict(ajustes_fallidos=failure,advertencias=[dict(etiqueta=f['etiqueta'],advertencias=f.get('advertencias',[]),fuera_0_500=f.get('fuera_0_500',0)) for f in fits if f.get('advertencias') or f.get('fuera_0_500',0)]))
 if complete:
  repeats=read(run/'reproducibilidad.json');assert len(repeats['repeticiones'])==10 and all(r['max_diferencia']<=1e-10 for r in repeats['repeticiones'])
  for r in repeats['repeticiones']:
   original=pd.read_csv(run/'ajustes'/f"e{r['externo']}_externo_{r['id']}"/'predicciones.csv',float_precision='round_trip');repeat=pd.read_csv(run/'ajustes'/f"e{r['externo']}_repeticion_{r['id']}"/'predicciones.csv',float_precision='round_trip');assert float(np.max(np.abs(original.prediccion-repeat.prediccion)))==r['max_diferencia']
  assert len(ledger['ajustes'])==len(fits) or failure
  improvement=100*(summary['referencia_v1']['mae']-summary['procedimiento_v2']['mae'])/summary['referencia_v1']['mae'] if summary['referencia_v1']['mae']>0 else None
 else:improvement=None
 # Deterioros explícitos vs referencia v1, por año y territorio.
 deterioration=[]
 if len(metrics):
  m=pd.DataFrame(metrics);baseline=m[m.procedimiento=='referencia_v1']
  for role in m.procedimiento.unique():
   if role=='referencia_v1':continue
   merged=m[m.procedimiento==role].merge(baseline,on=['ambito','grupo'],suffixes=('','_v1'))
   for r in merged.itertuples():deterioration.append(dict(procedimiento=role,ambito=r.ambito,grupo=r.grupo,delta_mae=r.mae-r.mae_v1,delta_rmse=r.rmse-r.rmse_v1,deteriora_mae=r.mae>r.mae_v1))
 pd.DataFrame(deterioration).to_csv(out/'deterioros.csv',index=False,float_format='%.17g')
 pd.DataFrame([{k:v for k,v in f.items() if k in ('id','etiqueta','estado','n','semilla')}|dict(segundos=f['tiempo']['segundos']) for f in fits]).to_csv(out/'ajustes_resumen.csv',index=False)
 pd.DataFrame([dict(externo=s['externo'],global_id=s['global_id'],**s['especificaciones']) for s in selections]).to_csv(out/'ganadores.csv',index=False)
 pd.DataFrame([dict(externo=s['externo'],**score) for s in selections for score in s['metricas_internas']]).to_csv(out/'metricas_internas.csv',index=False,float_format='%.17g')
 result=dict(aprobado=True,completo=complete,ajustes=len(ledger['ajustes']),segundos_consumidos=ledger['consumido'],segundos_observados=elapsed,saldo=7200-ledger['consumido'],cobertura=coverage,metricas_conjuntas=summary,mejora_porcentaje=improvement,umbral_futuro_satisfecho=improvement is not None and improvement>=5,notebook_personal_entregado=False,predicciones_artefactos_verificadas=prediction_count,fallos=len(failure),pdf_leidos=[],procedimiento_calculo='biblioteca estándar math.fsum, e=pred-y; grupos CSV, sin medias de métricas parciales')
 guardar(out/'verificacion_resultados.json',result);print(json.dumps({k:result[k] for k in ('completo','ajustes','segundos_consumidos','mejora_porcentaje','fallos')},ensure_ascii=False));return result
if __name__=='__main__':verify()
