"""Controles adicionales independientes: historia durable, congelación y negativos."""
from auditor import *
import copy

def main():
 check(load(HERE/'AUDITORIA_INDEPENDIENTE.json')['aprobado'],'auditoría')
 ledger=load(E2/'resultados/piloto/ledger.json'); histories=sorted((E2/'resultados/piloto/historia').glob('*.json'))
 previous=None; running=set(); completions={}; states=defaultdict(set)
 for p in histories:
  h=load(p)
  check(h['limit']==7200 and h['context']==ledger['context'] and h['start_monotonic']==ledger['start_monotonic'] and h['start_wall']==ledger['start_wall'],'ledger no reinicio '+p.name)
  check(not h['exhausted'] and h['retries']==0 and h['used']>=0 and len(h['attempts'])<=61,'historia estados '+p.name)
  if previous:
   check(h['used']>=previous['used'] and len(h['attempts'])>=len(previous['attempts']),'tiempo/acumulación '+p.name)
   for a,b in zip(previous['attempts'],h['attempts']):
    check(a['job']==b['job'] and a['context']==b['context'] and a['attempt']==b['attempt'],'identidad historia')
    if a['state']=='success': check(a==b,'no sobrescribir terminado')
   check(not previous['closed'],'ledger no reabierto')
  active=[a for a in h['attempts'] if a['state'] in ['running','pending']]; check(len(active)<=1,'serial')
  for a in h['attempts']:
   check(a['state'] in ['success','pending'],'sin fallos/retries')
   states[a['job']].add(a['state'])
   if a['state']=='pending': running.add(a['job'])
   if a['state']=='success' and not a.get('no_fit'): completions.setdefault(a['job'],h['start_monotonic']+h['used'])
  previous=h
 check(previous==ledger and len(histories)==94,'historia final ledger exacto')
 for a in ledger['attempts']:
  if not a.get('no_fit'):
   check(a['job'] in running,'arranque durable '+a['job'])
   check(a['start_monotonic']>=ledger['start_monotonic'] and a['start_monotonic']+a['seconds_measured']<=completions[a['job']]+1e-10,'tiempo medido arranque-final')
 # Cotejo de congelación/pruebas por bytes, sin importar funciones operativas.
 freeze=load(E2/'CONGELACION_FASE3.json'); check(freeze['antes_de_fits_reales'] and freeze['fits_reales']==0,'congelación prefit')
 for s,h in freeze['fuentes_sha256'].items(): check(sha(E2/s)==h,'freeze fuente '+s)
 f2=load(BASE/'etapa1/CONGELACION_FASE2.json')
 for s,h in f2['implementacion'].items(): check(sha(BASE/'etapa1'/s)==h['sha256'],'freeze etapa1 '+s)
 for s,h in f2['documentos_base'].items(): check(sha(ROOT/s)==h,'documento congelado '+s)
 # Detectar alteraciones con datos inventados usando las mismas funciones auditoras.
 tests=[]
 def reject(fn,label):
  try: fn()
  except AssertionError: tests.append(label); return
  raise AssertionError('No rechaza '+label)
 levels={t:{f'{i:02d}':float(100+i+(t-2018)*3) for i in range(33)} for t in YEARS}
 expected=reconstruct(levels,2023,'memoria','interna')
 for field in ['matrices','keys','prediction_inputs','context','supervised_years','units','previous_year']:
  bad=copy.deepcopy(expected)
  bad[field]=None
  reject(lambda:check(bad[field]==expected[field],field),'rechazo '+field)
 a=[{'code':'01','candidate':'memoria','observed':'2','predicted':'1'}]
 reject(lambda:exact(a,a+a),'cobertura CSV')
 reject(lambda:exact(a,[{'code':'02','candidate':'memoria','observed':'2','predicted':'1'}]),'llave CSV')
 ms={c:{'MAE':2,'RMSE':2} for c in CAND}; ms['memoria']={'MAE':1,'RMSE':1}; ms['persistencia']={'MAE':1.1,'RMSE':1.1}; check(select(ms)[0]=='persistencia','límites inclusivos'); tests.append('bandas inclusivas')
 coef=rows(HERE/'tablas/coeficientes_todos_41.csv')
 check(all(r['intercept_in_median_interval']=='True' for r in coef),'nivel intervalo mediana todos')
 save('AUDITORIA_COMPLEMENTARIA.json',{'aprobado':True,'historia_snapshots':94,'jobs':61,'jobs_con_arranque_durable':len(running),'fits_historicos':41,'fits_nuevos':0,'ledger_cerrado_no_reabierto':True,'congelaciones_bytes_validos':True,'interceptos_intervalo_mediana_todos':True,'pruebas_inventadas':tests,'cronologia':'94 snapshots monotónicos; pending antes de success; terminación guardada y retorno0. Congelación declarada prefit y fuentes ligadas por huellas; no autenticación externa de tiempos.'})
 print('Historia/congelación/negativos aprobados; cero fits')
if __name__=='__main__': main()
