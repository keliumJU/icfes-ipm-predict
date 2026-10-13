"""Reconstrucción independiente de guardados y tablas exploratorias. Cero fits."""
from auditor import *
import numpy as np

def table(name,data):
 p=HERE/'tablas'/name; p.parent.mkdir(exist_ok=True)
 check(not p.exists(),'no sobrescribir '+name)
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)

def panel():
 spec=load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')
 source,derived=[sorted(rows(ROOT/s),key=lambda r:(r['codigo_departamento'].zfill(2),int(r['anio']))) for s in spec['fuentes']]
 codes=sorted({r['codigo_departamento'].zfill(2) for r in source})
 check(len(codes)==33 and len(source)==len(derived)==231,'panel cobertura')
 levels={t:{} for t in YEARS}
 for a,b in zip(source,derived):
  for k,v in a.items():
   if k=='codigo_departamento': check(v.zfill(2)==b[k].zfill(2),'panel código normalizado')
   elif k=='departamento': check(v==b[k],'panel '+k)
   else:
    if v=='': check(b[k]=='','panel vacío '+k)
    else: check(float(v)==float(b[k]),'panel fuente campo '+k)
  t=int(a['anio']); c=a['codigo_departamento'].zfill(2); check(c not in levels[t],'duplicado fuente'); levels[t][c]=float(a['prom_punt_global'])
  if t==2018:
   check(b['anio_previo']==b['puntaje_previo']==b['cambio_observado']==b['intervalo']=='','nivel2018')
  else:
   prev=max(y for y in YEARS if y<t)
   check(float(b['anio_previo'])==prev and float(b['intervalo'])==t-prev,'máximo previo/intervalo')
   old=next(r for r in source if r['codigo_departamento'].zfill(2)==c and int(r['anio'])==prev)
   check(float(b['puntaje_previo'])==float(old['prom_punt_global']),'puntaje previo')
   check(float(b['cambio_observado'])==float(a['prom_punt_global'])-float(old['prom_punt_global']),'d sin anualizar')
   for k,v in b.items():
    if k.startswith('previo_'):
     check(float(v)==float(old[k[7:]]),'derivado '+k)
    elif k.startswith('cambio_') and k!='cambio_observado':
     cov=k[7:]; check(float(v)==float(a[cov])-float(old[cov]),'derivado '+k)
  check(b['fuente_sha256']==spec['fuentes'][list(spec['fuentes'])[0]]['esperado'],'fuente columna SHA')
 check(all(sorted(v)==codes for v in levels.values()),'códigos completos')
 return levels,codes

def audit():
 check(load(HERE/'PREFLIGHT_FASE4.json')['aprobado'] and load(HERE/'PRUEBAS_AUDITOR.json')['aprobado'],'entrada')
 levels,codes=panel(); ledger=load(E2/'resultados/piloto/ledger.json')
 check(ledger['closed'] and ledger['limit']==7200 and not ledger['synthetic'] and not ledger['exhausted'] and ledger['retries']==0,'ledger cerrado')
 results={}; coefficients=[]; counts=defaultdict(int); time_sum=0
 for a in ledger['attempts']:
  job=a['job']; check(a['state']=='success' and a['attempt']==1 and a['seconds_measured']>=0,'ledger estado '+job)
  p=E2/a['output']; check(sha(p)==a['output_sha256'],'output bytes '+job); r=load(p)
  check(not r['synthetic'] and r['state']=='success' and not r['warnings'],'estado salida '+job)
  e=r['evaluated']; c=r['candidate']; role=r['role']; expected=reconstruct(levels,e,c,role)
  for k,v in expected.items(): check(r[k]==v,job+': reconstrucción '+k)
  check(a['context']==r['context'],'context ledger '+job)
  should_fit=c!='persistencia' and bool(expected['supervised_years']) and not(e==2021 and role=='externa')
  expected_n=len(COMP[CAND.index(c)]) if should_fit else 0
  check(r['fits']==a['pipeline_fits_started']==expected_n,'fits esperados '+job)
  check(set(r['pipelines'])==(set(COMP[CAND.index(c)]) if should_fit else set()),'pipelines separados '+job)
  preds=np.zeros(33)
  for comp,v in r['pipelines'].items():
   s=v['scaler']; q=v['regressor']; X,y=expected['matrices'][comp]; X=np.array(X,dtype=float)
   check(s['params']==SC and q['params']==QR,'defaults sin recencia '+job)
   check(s['n_samples_seen']==len(X),'n scaler '+job)
   mean=np.mean(X,axis=0); var=np.mean((X-mean)**2,axis=0)
   check(np.allclose(mean,s['mean'],atol=1e-12,rtol=0) and np.allclose(var,s['var'],atol=1e-12,rtol=0),'scaler entrenado '+job)
   check(np.allclose(np.where(var==0,1,np.sqrt(var)),s['scale'],atol=1e-12,rtol=0),'scale '+job)
   inp=np.array(expected['prediction_inputs'][comp]); change=((inp-np.array(s['mean']))/np.array(s['scale']))@np.array(q['coef'])+q['intercept']
   preds+=change if comp!='comun' else change[0]
   coef=q['coef'][0]; inter=q['intercept']; ordered=sorted(y); lower=ordered[(len(y)-1)//2]; upper=ordered[len(y)//2]
   check(len(q['coef'])==1 and math.isfinite(inter),'coef 1 entrada '+job)
   coefficients.append({'job':job,'role':role,'evaluated':e,'candidate':c,'component':comp,'n_train':len(X),'years_train':len(expected['supervised_years']),'coef_lag_standardized':coef,'intercept_points':inter,'median_lower_points':lower,'median_upper_points':upper,'intercept_in_median_interval':lower<=inter<=upper,'delta_constant':bool(coef==0),'source':str(p.relative_to(ROOT))+'#pipelines/'+comp})
  check(np.array_equal(preds,np.array(r['delta'])),'cambio reconstruido exacto '+job)
  check(np.array_equal(np.array(expected['previous_score'])+preds,np.array(r['score'])),'puntaje reconstruido exacto '+job)
  if not should_fit: check(r['reason'] in ['persistencia','cero_pares','externa2021_fija'],'respaldo declarado '+job)
  else:
   req=E2/a['request']; check(sha(req)==a['request_sha256'],'request '+job)
   request=load(req); check(request['levels']=={str(t):levels[t] for t in YEARS if t<e},'solo historia request '+job)
   check(request['context']==r['context'] and request['role']==role and request['candidate']==c and request['evaluated']==e and not request['synthetic'],'request contexto '+job)
   check(a['returncode']==0 and a['process_terminated'] and a['seconds_measured']>=r['seconds_worker'],'terminación y comunicación '+job)
   progress=load(p.parent/'progreso.json'); check(all(f['state']=='complete' for f in progress['fits']) and len(progress['fits'])==expected_n,'progreso completo '+job)
   check(r['python']=='3.12.14' and r['sklearn']=='1.9.1','version job '+job)
   for f in progress['fits']: check([f['X'],f['y']]==expected['matrices'][f['component']],'progress matriz '+job)
  check(job not in results,'job único'); results[job]=r
  counts['interna' if job.startswith('int_') else 'externa' if job.startswith('ext_') else 'repeticion']+=expected_n
  time_sum+=a['seconds_measured']
 check(dict(counts)=={'externa':16,'interna':24,'repeticion':1} and sum(counts.values())==41<=46,'41fits cota46')
 check(time_sum<=ledger['used']<7200,'tiempo incluye arranque/comunicación/pausas')
 check(ledger['used']==58.63946153299912,'consumo histórico')
 # Cobertura contractual de jobs y ventanas sin reuso entre candidatos.
 expected_jobs={f'ext_e{e}_{c}' for e in range(2021,2026) for c in CAND}|{f'int_e{e}_v{v}_{c}' for e in range(2022,2026) for v in range(2021,e) for c in CAND}|{'rep_e2025_memoria'}
 check(set(results)==expected_jobs,'jobs exactos separados')
 spec=load(ROOT/'diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json')
 windows=[{'externo':e,'entrenamiento':[] if e==2021 else [y for y in YEARS[1:] if y<e],'procedimiento':'persistencia_fija' if e==2021 else 'seleccion_interna','internas':[{'validacion':v,'entrenamiento':[y for y in YEARS[1:] if y<v]} for v in range(2021,e)]} for e in range(2021,2026)]
 check(spec['ventanas']==windows,'ventanas exactas diez internas acumuladas')
 data=load(E2/'resultados/piloto/salidas.json')
 for key,name,n in [('internal','predicciones_internas_originales',1320),('external','predicciones_externas',825),('records','registros_seleccion',16),('unique','predicciones_internas_unicas',528)]:
  a=rows(E2/('resultados/'+name+'.csv')); b=rows(E2/('resultados/control_csv/'+name+'.csv')); check(len(a)==n,'cobertura '+name); exact(a,b)
  expected=[{k:str(v) for k,v in r.items()} for r in data[key]]; exact(a,expected)
 internal=data['internal']; external=data['external']; records=data['records']
 check({(r['external'],r['validation'],r['candidate'],r['code']) for r in internal}=={(e,v,c,k) for e in range(2022,2026) for v in range(2021,e) for c in CAND for k in codes},'1320 llaves')
 check({(r['external'],r['policy'],r['code']) for r in external}=={(e,c,k) for e in range(2021,2026) for c in CAND+['global'] for k in codes},'825 llaves')
 for r in internal+external:
  e=r['external']; v=r['validation']; c=r['candidate']; k=r['code']; j=codes.index(k)
  job=f'int_e{e}_v{v}_{c}' if r in internal else f'ext_e{e}_{c}'
  saved=results[job]
  for field,val in [('observed',levels[v][k]),('predicted',saved['score'][j]),('delta',saved['delta'][j]),('previous_score',saved['previous_score'][j]),('previous_year',saved['previous_year']),('context',saved['context']),('interval',v-saved['previous_year'])]: check(r[field]==val,'fila '+job+'/'+k+':'+field)
 selections=[]; decision_rows=[]
 for e in range(2022,2026):
  ms={c:metrics([r for r in internal if r['external']==e and r['candidate']==c]) for c in CAND}; winner,pool,pool2=select(ms)
  selection={'external':e,'candidate':winner,'pool_MAE':pool,'pool_RMSE':pool2}; selections.append(selection)
  for c in CAND:
   rec=next(r for r in records if r['external']==e and r['candidate']==c)
   check(rec['eligible'] and rec['selected']==(c==winner) and rec['n']==ms[c]['n'] and rec['MAE']==ms[c]['MAE'] and rec['RMSE']==ms[c]['RMSE'],'selección interna '+str(e)+c)
   decision_rows.append({'external':e,'candidate':c,**ms[c],'in_pool_MAE':c in pool,'in_pool_RMSE':c in pool2,'selected':c==winner,'inputs':[0,1,1,2][CAND.index(c)]})
 check(selections==data['selections']==load(E2/'resultados/selecciones.json'),'selecciones exactas')
 for r in external:
  if r['policy']=='global':
   c='persistencia' if r['external']==2021 else next(q['candidate'] for q in selections if q['external']==r['external'])
   own=next(q for q in external if q['external']==r['external'] and q['policy']==c and q['code']==r['code'])
   check(r['candidate']==c and {k:v for k,v in r.items() if k!='policy'}=={k:v for k,v in own.items() if k!='policy'},'global solo mismo candidato ventana')
 groups=defaultdict(list)
 for r in internal: groups[(r['validation'],r['candidate'],r['code'])].append(r)
 uniques=[]; lineage=[]
 for key in sorted(groups):
  g=sorted(groups[key],key=lambda r:r['external']); rep=g[0]
  for r in g:
   check({k:v for k,v in r.items() if k!='external'}=={k:v for k,v in rep.items() if k!='external'},'copia/contexto exacto '+str(key))
   lineage.append({'external':r['external'],'key':list(key),'representative_external':rep['external']})
  uniques.append(rep)
 check(uniques==data['unique'] and lineage==data['lineage']==load(E2/'resultados/linaje_internas.json'),'528 únicas/1320linaje menor externo')
 checks=load(E2/'resultados/comprobaciones_global.json'); check(len(checks)==5 and checks==data['global_checks'],'cinco global checks')
 for rec in checks:
  e=rec['external']; c=rec['candidate']; r=results[f'ext_e{e}_{c}']
  if c=='persistencia': difference=max(abs(a-b) for a,b in zip(r['score'],r['previous_score'])); check(difference==0,'previo exacto')
  else:
   rep=results[f'rep_e{e}_{c}']; check(rep['context']==r['context'],'repetición mismo contexto'); difference=max(abs(a-b) for a,b in zip(r['score'],rep['score'])); check(difference<=1e-10,'atol1e-10 rtol0')
  check(rec['context']==r['context'] and rec['max_difference']==difference and rec['approved'],'check global exacto')
 # Referencias solo guardados; no modelos; mismas llaves/observados.
 refs=[]
 for s,policy in [('experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv','persistencia'),('experimentos_objetivo3_v5/etapa2/resultados/predicciones_externas.csv','global'),('experimentos_temporales_objetivo3_v1/etapa2/resultados/predicciones_externas.csv','global')]:
  a=[r for r in rows(ROOT/s) if r['procedimiento']==policy]; check(len(a)==165,'referencia165')
  check({(int(r['anio']),r['codigo_departamento'].zfill(2)) for r in a}=={(e,k) for e in range(2021,2026) for k in codes},'referencia llaves')
  for r in a:
   e=int(r['anio']); k=r['codigo_departamento'].zfill(2); own=next(q for q in external if q['policy']=='persistencia' and q['external']==e and q['code']==k)
   check(float(r['observado'])==own['observed'] and float(r['prediccion'])==own['predicted'],'referencia exacta')
  refs.append({'source':s,'policy':policy,'n':165,'exact':True,'independiente':False})
 table('coeficientes_todos_41.csv',coefficients); table('decisiones_internas.csv',decision_rows); table('referencias.csv',refs)
 totals=[{'policy':c,**metrics([r for r in external if r['policy']==c])} for c in CAND+['global']]
 base=totals[0]['MAE']; check(base>0 and math.isfinite(base),'denominador positivo finito')
 for r in totals: r['improvement_percent']=100*(base-r['MAE'])/base
 table('metricas_165.csv',totals)
 paired=[]
 for r in external:
  b=next(q for q in external if q['external']==r['external'] and q['code']==r['code'] and q['policy']=='persistencia'); err=r['predicted']-r['observed']; berr=b['predicted']-b['observed']; change=r['observed']-r['previous_score']
  paired.append({'year':r['external'],'code':r['code'],'policy':r['policy'],'observed_points':r['observed'],'predicted_points':r['predicted'],'observed_change_points':change,'predicted_change_points':r['delta'],'signed_error_points':err,'absolute_error_points':abs(err),'persistence_absolute_error_points':abs(berr),'benefit_points':abs(berr)-abs(err),'direction_match':int(np.sign(change)==np.sign(r['delta']))})
 table('errores_pareados_825.csv',paired)
 byyear=[]; bycode=[]
 for field,target in [('year',byyear),('code',bycode)]:
  for value in sorted({r[field] for r in paired}):
   for c in CAND+['global']:
    a=[r for r in paired if r[field]==value and r['policy']==c]; n=len(a); er=[r['signed_error_points'] for r in a]; benefits=[r['benefit_points'] for r in a]
    target.append({field:value,'policy':c,'n':n,'MAE_points':math.fsum(map(abs,er))/n,'RMSE_points':math.sqrt(math.fsum(v*v for v in er)/n),'bias_points':math.fsum(er)/n,'benefit_MAE_points':math.fsum(benefits)/n,'improve_pairs':sum(v>0 for v in benefits),'worsen_pairs':sum(v<0 for v in benefits),'tie_pairs':sum(v==0 for v in benefits),'direction_match_pairs':sum(r['direction_match'] for r in a)})
 table('por_anio.csv',byyear); table('por_territorio.csv',bycode)
 correction=[]
 for e in range(2021,2026):
  a=[r for r in external if r['policy']=='comun' and r['external']==e]; b=[r for r in external if r['policy']=='comun_correccion' and r['external']==e]
  check([r['predicted'] for r in a]==[r['predicted'] for r in b],'común/corrección exacto '+str(e)); correction.append({'year':e,'n':33,'equal_exact':True})
 table('correccion_comun.csv',correction)
 historical=load(E2/'resultados/meta.json'); global_metric=next(r for r in totals if r['policy']=='global'); memory=next(r for r in totals if r['policy']=='memoria')
 discrepancies={k:{'historico':historical[k],'recalculado':v} for k,v in [('MAE_persistencia',base),('MAE_global',global_metric['MAE']),('mejora_porcentaje',global_metric['improvement_percent'])] if historical[k]!=v}
 check(not discrepancies,'discrepancia meta: '+str(discrepancies))
 summary={'aprobado':True,'fits_nuevos':0,'modelos_cargados':0,'n':165,'primary':'global predefinido','persistence':totals[0],'global':global_metric,'memory_exploratory':memory,'target_5_satisfied':global_metric['improvement_percent']>=5,'historical_discrepancies':discrepancies,'fits_historicos':dict(counts),'ledger_used_seconds':ledger['used'],'sum_measured_attempt_seconds':time_sum,'memoria_coefficients_zero_all':all(r['coef_lag_standardized']==0 for r in coefficients if r['component']=='memoria'),'memoria_n_adjustments':sum(r['component']=='memoria' for r in coefficients),'correction_zero_all':all(r['coef_lag_standardized']==r['intercept_points']==0 for r in coefficients if r['component']=='correccion'),'selections':selections,'global_2025':next(r for r in byyear if r['year']==2025 and r['policy']=='global'),'global_territory_5years_improve':sum(r['benefit_MAE_points']>0 for r in bycode if r['policy']=='global'),'global_territory_5years_worsen':sum(r['benefit_MAE_points']<0 for r in bycode if r['policy']=='global'),'coverage':{'internal':1320,'records':16,'external':825,'unique':528,'lineage':1320,'global_checks':5},'limits':'exploratorio; años2021–2025vistos; dependencia; sin causalidad/confirmación'}
 save('AUDITORIA_INDEPENDIENTE.json',summary)
 print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
 try: audit()
 except Exception as ex:
  save('INCOMPLETO_AUDITORIA.json',{'completa':False,'error':repr(ex),'fits':0}); raise
