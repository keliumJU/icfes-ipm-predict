"""Enmienda de clasificación del agregado interno, antes del primer recálculo real.
No altera ajustes, selección, presupuesto ni código operativo congelado.
"""
from verificar_resultados import *
import re

def verify_extended():
 result=verify();out=F3/'resultados';run=out/'piloto';rows=[]
 conf=read(CONFIG);windows={w['externo']:w for w in conf['ventanas']}
 for meta in sorted((run/'ajustes').glob('*/ajuste.json')):
  label=meta.parent.name;info=read(meta)
  m=re.fullmatch(r'e(202[1-5])_i(2019|202[1-4])_(.+)',label)
  if m:
   w=windows[int(m.group(1))];fold=next(i for i in w['internas'] if i['validacion']==int(m.group(2)))
   assert info['entrenamiento']==fold['entrenamiento'] and info['id']==m.group(3)
   expected_year=fold['validacion']
  else:
   m=re.fullmatch(r'e(202[1-5])_(externo|repeticion)_(.+)',label);assert m,label
   w=windows[int(m.group(1))];assert info['entrenamiento']==w['entrenamiento'] and info['id']==m.group(3)
   expected_year=w['externo']
  file=meta.parent/'predicciones.csv'
  if file.exists():q=pd.read_csv(file);assert q.anio.eq(expected_year).all()
 for file in sorted(run.glob('seleccion_*.json')):
  selected=read(file);w=windows[selected['externo']];expected=[i['validacion'] for i in w['internas']]
  assert [r['id'] for r in selected['metricas_internas']]==[c['id'] for c in conf['configuraciones']]
  assert all(r['ventanas']==expected for r in selected['metricas_internas'] if r['estado']=='completo')
 for file in sorted(run.glob('externas_*.csv')):
  external=pd.read_csv(file);year=int(external.externo.iloc[0]);selected=read(run/f'seleccion_{year}.json')
  roles={'procedimiento_v2':selected['global_id'],**{f'procedimiento_{spec}':ident for spec,ident in selected['especificaciones'].items()},'media':'media','referencia_v1':'referencia_v1',**{c['id']:c['id'] for c in conf['configuraciones'] if c['familia']=='ols'}}
  assert set(external.procedimiento)==set(roles)
  for role,ident in roles.items():assert external[external.procedimiento==role].id.eq(ident).all()
 # La subcadena '_i' también está en '_ipm': reconocer la etiqueta temporal completa.
 for file in sorted((run/'ajustes').glob('*/predicciones.csv')):
  match=re.fullmatch(r'e(202[1-5])_i(2019|202[1-4])_(.+)',file.parent.name)
  if match:
   q=pd.read_csv(file,dtype={'codigo_departamento':str},float_precision='round_trip');q['externo']=int(match.group(1));assert q.anio.eq(int(match.group(2))).all();rows.append(q)
 corrected=pd.concat(rows) if rows else pd.DataFrame()
 if result['completo'] and not result['fallos']:assert len(corrected)==49500
 if len(corrected):corrected.to_csv(out/'predicciones_internas.csv',index=False,float_format='%.17g')
 result['particiones_exactas_y_roles_verificados']=True;result['filas_predicciones_internas']=len(corrected);result['enmienda_reporte']='Regex etiqueta temporal completa; no selección ni evaluación alteradas.'
 guardar(out/'verificacion_resultados.json',result);return result
if __name__=='__main__':verify_extended()
