"""Auditoría de solo lectura de fase3, salidas restringidas a fase4."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
F4=ROOT/'experimentos_objetivo3_v2/fase4'
sys.path.insert(0,str(ROOT/'experimentos_objetivo3_v2/fase3/fuentes'))
from verificar_resultados import independent,same,select
from piloto import read,sha,guardar,cargar_panel,cfg,serial
import pandas as pd,numpy as np,math,re,subprocess,platform,importlib.metadata as md
F3=ROOT/'experimentos_objetivo3_v2/fase3'
CONFIG=cfg.F2/'resultados/configuraciones_congeladas.json'

def csv(p):return pd.read_csv(p,dtype={'codigo_departamento':str},float_precision='round_trip')
def save(frame,path):
 path=Path(path).resolve();assert path.is_relative_to(F4.resolve());path.parent.mkdir(parents=True,exist_ok=True)
 frame.to_csv(path,index=False,float_format='%.17g')

def integridad():
 count=0
 for phase in (cfg.F2,F3):
  manifest=read(phase/'resultados/manifiesto_cierre.json')
  for p,h in manifest['entregables_sha256'].items():
   if p=='experimentos_objetivo3_v2/CONTINUIDAD_V2.md':
    import hashlib
    commit='0664ac21100982006d1a20670c7e987879444dc6' if phase==cfg.F2 else 'b37a2f338f0708958a412f5a0efa09f33861322b'
    assert hashlib.sha256(subprocess.check_output(['git','show',f'{commit}:{p}'],cwd=ROOT)).hexdigest()==h,p
   else:assert sha(ROOT/p)==h,p
   count+=1
 freeze=read(cfg.F2/'resultados/congelacion_previa.json')
 for p,h in freeze['fuentes_sha256'].items():assert sha(ROOT/p)==h,p
 assert sha(CONFIG)==freeze['configuraciones_sha256'] and sha(cfg.F2/'PROTOCOLO_V2.md')==freeze['protocolo_sha256']
 operative=read(F3/'resultados/congelacion_operativa.json')
 for p,h in operative['codigo'].items():assert sha(ROOT/p)==h,p
 initial=read(F3/'resultados/integridad_inicial.json')
 for p,h in initial['snapshot_versionados'].items():
  if p!='experimentos_objetivo3_v2/CONTINUIDAD_V2.md':assert sha(ROOT/p)==h,p
 sources=read(F3/'resultados/conservacion_fuentes.json')
 # Se conserva íntegro el registro y se verifica cada fuente documentada.
 def check_sources(obj):
  nonlocal count
  if isinstance(obj,dict):
   for k,v in obj.items():
    if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) and (ROOT/k).is_file():assert sha(ROOT/k)==v;count+=1
    else:check_sources(v)
  elif isinstance(obj,list):
   for v in obj:check_sources(v)
 check_sources(sources)
 versions={}
 for line in (cfg.F2/'requirements.lock.txt').read_text().splitlines():
  name,version=line.split('==');versions[name]=md.version(name);assert versions[name]==version
 assert platform.python_version()=='3.12.14'
 conf=read(CONFIG);assert conf['version']=='2.0.2' and len(conf['configuraciones'])==100 and conf['ventanas']==cfg.ventanas()
 for c in conf['configuraciones']+[conf['referencia_historica']]:assert serial(cfg.construir(c).get_params(deep=True))==c['parametros_completos']
 return dict(aprobado=True,huellas_manifiestos_y_fuentes=count,python=platform.python_version(),paquetes=versions,pip_check=subprocess.check_output([sys.executable,'-m','pip','check']).decode().strip(),pdf_leidos=[])

def revisar(source=F3/'resultados',out=F4/'resultados'):
 source=Path(source);out=Path(out).resolve();assert out.is_relative_to(F4.resolve())
 panel=cargar_panel();conf=read(CONFIG);run=source/'piloto';ledger=read(run/'ledger.json');state=read(run/'estado.json')
 assert state['completo'] and not ledger['pendiente'] and ledger['limite']==7200 and ledger['consumido']<=7200
 assert len(ledger['ajustes'])<=1555 and all(a['estado']=='ok' for a in ledger['ajustes'])
 if source==F3/'resultados':assert len(ledger['ajustes'])==1552
 assert math.isclose(math.fsum(a['segundos'] for a in ledger['ajustes']),ledger['consumido'],abs_tol=1e-9)
 byid={c['id']:c for c in conf['configuraciones']};ref=conf['referencia_historica'].copy();ref['entradas']=conf['especificaciones']['ambas'];byid[ref['id']]=ref
 windows={w['externo']:w for w in conf['ventanas']};frames={};internals=[];counts=dict(internos=0,externos=0,repeticiones=0)
 for meta in sorted((run/'ajustes').glob('*/ajuste.json')):
  info=read(meta);label=meta.parent.name;m=re.fullmatch(r'e(202[1-5])_(i(2019|202[1-4])|externo|repeticion)_(.+)',label);assert m,label
  w=windows[int(m[1])];fold=next(i for i in w['internas'] if i['validacion']==int(m[3])) if m[3] else None
  years=fold['entrenamiento'] if fold else w['entrenamiento'];year=fold['validacion'] if fold else w['externo']
  c=byid[m[4]];assert info['id']==c['id'] and info['etiqueta']==label and info['entrenamiento']==years and info['entradas']==c['entradas']
  assert info['estado']=='ok' and info['origen']=='real' and info['semilla']==20261010 and info['parametros_completos']==c['parametros_completos']
  assert info['versiones_sha256']==sha(source/'entorno.json') and info['congelacion_sha256']==sha(source/'congelacion_operativa.json') and info['panel_sha256']==conf['panel_sha256']
  assert sha(meta.parent/'modelo.joblib')==info['modelo_sha256'] and sha(meta.parent/'predicciones.csv')==info['predicciones_sha256']
  tr=panel[panel.anio.isin(years)].sort_values(cfg.LLAVES);test=panel[panel.anio==year].sort_values(cfg.LLAVES)
  assert max(years)<year and tr[cfg.LLAVES].values.tolist()==info['llaves_entrenamiento'] and info['n']==len(tr)
  transform=info['transformacion_ajustada']
  if transform:
   X=tr[info['entradas']].to_numpy(float);assert transform['n_samples_seen']==len(tr)
   np.testing.assert_allclose(transform['mean'],X.mean(0),atol=1e-12,rtol=1e-12);np.testing.assert_allclose(transform['var'],X.var(0),atol=1e-10,rtol=1e-12)
   np.testing.assert_allclose(transform['scale'],np.where(X.var(0)==0,1,np.sqrt(X.var(0))),atol=1e-10,rtol=1e-12)
  q=csv(meta.parent/'predicciones.csv');assert len(q)==33 and not q.duplicated(cfg.LLAVES).any() and q.origen.eq('real').all() and q.id.eq(c['id']).all() and q.ajuste.eq(label).all()
  assert q[cfg.LLAVES].values.tolist()==test[cfg.LLAVES].values.tolist();np.testing.assert_array_equal(q.observado,test[cfg.RESULTADO]);np.testing.assert_allclose(q.error,q.prediccion-q.observado,atol=1e-12,rtol=1e-12)
  independent(q.observado,q.prediccion);frames[label]=q
  kind='internos' if fold else 'repeticiones' if m[2]=='repeticion' else 'externos';counts[kind]+=1
  if fold:q=q.copy();q['externo']=w['externo'];internals.append(q)
 assert counts['internos']==1500 and counts['repeticiones']==10 and counts['externos']<=45
 if source==F3/'resultados':assert counts['externos']==42
 for a in ledger['ajustes']:assert a['etiqueta'].removesuffix('_intento1') in frames
 internal=pd.concat(internals,ignore_index=True);assert len(internal)==49500
 
 if not (source/'predicciones_internas.csv').exists():save(internal,source/'predicciones_internas.csv')
 saved=csv(source/'predicciones_internas.csv');pd.testing.assert_frame_equal(internal.sort_values(['externo','ajuste',*cfg.LLAVES]).reset_index(drop=True),saved[internal.columns].sort_values(['externo','ajuste',*cfg.LLAVES]).reset_index(drop=True))
 external=[];winners=[]
 for year,w in windows.items():
  s=read(run/f'seleccion_{year}.json');assert s['congelacion_sha256']==sha(source/'congelacion_operativa.json')
  assert [r['id'] for r in s['metricas_internas']]==[c['id'] for c in conf['configuraciones']]
  for score in s['metricas_internas']:
   assert score['estado']=='completo' and score['ventanas']==[i['validacion'] for i in w['internas']]
   q=pd.concat([frames[f"e{year}_i{i['validacion']}_{score['id']}"] for i in w['internas']]);same(independent(q.observado,q.prediccion),score)
  assert s['global_id']==select(s['metricas_internas'])
  for spec,ident in s['especificaciones'].items():assert ident==select([r for r in s['metricas_internas'] if r['especificacion'] in (None,spec)])
  roles={'procedimiento_v2':s['global_id'],**{f'procedimiento_{k}':v for k,v in s['especificaciones'].items()},'media':'media','referencia_v1':'referencia_v1',**{c['id']:c['id'] for c in conf['configuraciones'] if c['familia']=='ols'}}
  ext=csv(run/f'externas_{year}.csv');assert set(ext.procedimiento)==set(roles)
  for role,ident in roles.items():
   q=ext[ext.procedimiento==role];assert len(q)==33 and q.id.eq(ident).all() and q.seleccion_sha256.eq(sha(run/f'seleccion_{year}.json')).all()
   src=frames[f'e{year}_externo_{ident}'];pd.testing.assert_frame_equal(q[src.columns].reset_index(drop=True),src.reset_index(drop=True))
  external.append(ext);winners.append(dict(externo=year,global_id=s['global_id'],**s['especificaciones']))
 expected_order=[]
 for year,w in windows.items():
  s=read(run/f'seleccion_{year}.json')
  for c in conf['configuraciones']:
   for i in w['internas']:expected_order.append(f"e{year}_i{i['validacion']}_{c['id']}_intento1")
  ids={s['global_id'],*s['especificaciones'].values(),'media',*[c['id'] for c in conf['configuraciones'] if c['familia']=='ols']}
  for ident in [c['id'] for c in conf['configuraciones'] if c['id'] in ids]+['referencia_v1']:expected_order.append(f'e{year}_externo_{ident}_intento1')
 for year in windows:
  for ident in (read(run/f'seleccion_{year}.json')['global_id'],'referencia_v1'):expected_order.append(f'e{year}_repeticion_{ident}_intento1')
 assert [a['etiqueta'] for a in ledger['ajustes']]==expected_order
 ext=pd.concat(external,ignore_index=True)
 if not (source/'predicciones_externas.csv').exists():save(ext,source/'predicciones_externas.csv')
 saved=csv(source/'predicciones_externas.csv');pd.testing.assert_frame_equal(ext,saved)
 expected=set(map(tuple,panel[panel.anio.between(2021,2025)][cfg.LLAVES].values));assert not ext.duplicated(['procedimiento',*cfg.LLAVES]).any()
 for role,q in ext.groupby('procedimiento'):assert len(q)==165 and set(map(tuple,q[cfg.LLAVES].values))==expected
 repeats=read(run/'reproducibilidad.json');assert repeats['aprobado'] and len(repeats['repeticiones'])==10
 for r in repeats['repeticiones']:
  original=frames[f"e{r['externo']}_externo_{r['id']}"];repeat=frames[f"e{r['externo']}_repeticion_{r['id']}"];delta=float(np.max(np.abs(original.prediccion-repeat.prediccion)));assert delta==r['max_diferencia'] and delta<=1e-10
 metrics=[]
 for period,mask in [('2021-2025',ext.anio.between(2021,2025)),('2021-2024',ext.anio.between(2021,2024)),('2025',ext.anio.eq(2025))]:
  for role,g in ext[mask].groupby('procedimiento'):
   for scope,col in [('conjunto',None),('anual','anio'),('territorial','codigo_departamento')]:
    for key,q in ([('todos',g)] if col is None else g.groupby(col)):
     metrics.append(dict(periodo=period,procedimiento=role,ambito=scope,grupo=str(key),**independent(q.observado,q.prediccion)))
 met=pd.DataFrame(metrics)
 if not (source/'metricas.csv').exists():save(met[met.periodo=='2021-2025'].drop(columns='periodo'),source/'metricas.csv')
 historical=csv(source/'metricas.csv');current=met[met.periodo=='2021-2025'].drop(columns='periodo').reset_index(drop=True)
 for r in current.itertuples():
  old=historical[(historical.procedimiento==r.procedimiento)&(historical.ambito==r.ambito)&(historical.grupo.astype(str).str.zfill(2)==str(r.grupo).zfill(2))];assert len(old)==1;same(r._asdict(),old.iloc[0].to_dict())
 baseline=met[met.procedimiento=='referencia_v1'];comp=met[met.procedimiento!='referencia_v1'].merge(baseline,on=['periodo','ambito','grupo'],suffixes=('','_v1'),validate='many_to_one')
 for k in ('mae','rmse','sesgo','r2'):comp['delta_'+k]=comp[k]-comp[k+'_v1']
 comp['deteriora_mae']=comp.delta_mae>0;comp['deteriora_rmse']=comp.delta_rmse>0
 pair=ext[ext.procedimiento=='procedimiento_v2'].merge(ext[ext.procedimiento=='referencia_v1'],on=cfg.LLAVES,suffixes=('_v2','_v1'),validate='one_to_one');assert len(pair)==165
 pair['delta_error_firmado']=pair.error_v2-pair.error_v1;pair['delta_error_absoluto']=abs(pair.error_v2)-abs(pair.error_v1);pair['delta_error_cuadratico']=pair.error_v2**2-pair.error_v1**2
 summary=met[(met.periodo=='2021-2025')&(met.ambito=='conjunto')].set_index('procedimiento');a=float(summary.loc['procedimiento_v2','mae']);b=float(summary.loc['referencia_v1','mae'])
 from comun import condicion_personal
 condition=condicion_personal(b,a,True)
 for name,frame in [('metricas.csv',met),('comparaciones_v1.csv',comp),('diferencias_emparejadas.csv',pair),('ganadores.csv',pd.DataFrame(winners))]:save(frame,out/name)
 controls=dict(aprobado=True,completo=True,conteos=counts,ajustes=len(ledger['ajustes']),predicciones_internas=49500,predicciones_por_artefacto=sum(map(len,frames.values())),cobertura={r:len(g) for r,g in ext.groupby('procedimiento')},segundos_piloto=ledger['consumido'],repeticiones=10,max_diferencia_repeticiones=max(r['max_diferencia'] for r in repeats['repeticiones']),mae_v2=a,mae_v1=b,condicion=condition,ajustes_nuevos_revision=0,fuente=str(source.relative_to(ROOT)),trazabilidad='Selecciones recalculadas exclusivamente desde internas; huella vincula externos. Fecha guardada no certifica por sí sola cronología física.',enmiendas_conservadas=['E3-01 regex temporal completa','E3-02 cota descriptiva 1555; tope7200'],pdf_leidos=[])
 guardar(out/'verificacion.json',controls);return met,comp,pair,controls

if __name__=='__main__':
 guardar(F4/'resultados/integridad_consulta.json',integridad());_,_,_,r=revisar();print(r)
