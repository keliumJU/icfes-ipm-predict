"""Prueba propia de orquestación con niveles inventados; preserva cada corrida."""
from comun import *
from runner import Ledger, execute, BudgetError, InfrastructureFailure
from verificar import validate_outputs
import numpy as np

def rejected(call,error):
    try: call()
    except error: return
    raise AssertionError('No rechazó '+error.__name__)

def main():
    assert environment()['aprobado'] and load(HERE/'PREFLIGHT_FASE3.json')['aprobado']
    folder='resultados/sinteticos/corrida_'+sys.argv[1]
    if safe_path(HERE,folder).exists(): raise IntegrityError('Corrida existente')
    rng=np.random.default_rng(SEED); scores=100+np.arange(33,dtype=float)
    levels={2018:dict(zip(CODES,scores.tolist()))}
    for i,y in enumerate(YEARS[1:]):
        # Segundo escenario inventado fuerza selección ajustada/repetición global.
        scores=scores+2 if sys.argv[1]=='002' else scores+(np.arange(33)-16)*(i+1)/8+(i-2)+rng.integers(-2,3,size=33)
        levels[y]=dict(zip(CODES,scores.tolist()))
    ledger=Ledger(folder+'/piloto','inventado',limit=300,synthetic=True)
    try:
        data=execute(levels,ledger); validation=validate_outputs(data,levels,ledger)
        validate_outputs(json.loads(json.dumps(data)),levels,ledger)
        if sys.argv[1]=='002':
            assert validation['fits']['repeticion']==3 and data['selections'][-1]['candidate']=='memoria'
    finally: ledger.close()
    fresh(folder+'/salidas.json',data)
    for key in ('internal','external','records','unique'): csv_write(folder+'/'+key+'.csv',data[key])
    # CSV exactamente igual; variantes de0, rechazo1e-11 y orden/duplicados.
    a=[{'code':'05','value':0},{'code':'08','value':1}]
    csv_write(folder+'/exacto.csv',a); csv_write(folder+'/equivalente.csv',[dict(r,value=float(r['value'])) for r in a])
    assert exact_csv(HERE/folder/'exacto.csv',HERE/folder/'equivalente.csv',numeric=('value',),keys=('code',))
    csv_write(folder+'/rechazo.csv',[dict(a[0],value=1e-11),a[1]])
    rejected(lambda:exact_csv(HERE/folder/'exacto.csv',HERE/folder/'rechazo.csv',numeric=('value',),keys=('code',)),IntegrityError)
    changed=[dict(r) for r in data['internal']]; changed[0]['predicted']+=1e-11
    rejected(lambda:lineage(changed),IntegrityError)
    # Estado pendiente sin tiempo medido agota; presupuesto cerrado no se renueva.
    crash=Ledger(folder+'/caida','caida',10,True)
    crash.state['attempts'].append({'job':'pendiente','state':'pending'}); crash.save()
    rejected(lambda:Ledger(folder+'/caida','caida',10,True),BudgetError)
    assert load(HERE/folder/'caida/ledger.json')['used']==10
    rejected(lambda:Ledger(folder+'/piloto','inventado',300,True),BudgetError)
    infra=Ledger(folder+'/infra','infra',30,True)
    rejected(lambda:infra.run(levels,2022,'interna','memoria','infra','infrastructure'),InfrastructureFailure)
    assert infra.state['retries']==1 and len(infra.state['attempts'])==2; infra.close()
    numeric=Ledger(folder+'/numerico','numerico',30,True)
    res=numeric.run(levels,2022,'interna','memoria','numerico','numerical')
    assert res['state']=='numerical' and numeric.state['retries']==0 and len(numeric.state['attempts'])==1
    assert numeric.run(levels,2022,'interna','memoria','numerico','numerical')==res; numeric.close()
    terminated=Ledger(folder+'/terminacion','terminacion',30,True)
    rejected(lambda:terminated.run(levels,2022,'interna','memoria','wait','wait',timeout=0.2),BudgetError)
    assert terminated.state['attempts'][-1]['process_terminated']; terminated.close()
    for ext in YEARS[3:]:
        decision=load(HERE/folder/f'piloto/selecciones/e{ext}.json')
        # La decisión persistida antes externas coincide con recalculo.
        assert select_internal(ext,decision['records'])==decision['choice']
    sources={p.name:digest(p) for p in HERE.glob('*.py')}
    fresh(folder+'/CONTROLES.json',{'aprobado':True,'synthetic':True,'fits_panel_real':0,'fits_inventados_piloto':validation['fits_total'],
        'fits_inventados_numero_fallido':1,'grupos':['orquestacion completa/cobertura','seleccion','matrices/fechas/scaler/reuso','linaje exacto','CSV0/1e-11','caida','cierre sin reinicio','infra retry max1','numerico inelegible sin retry','terminacion real'],
        'validacion':validation,'fuentes_sha256':sources,'salidas_sha256':digest(HERE/folder/'salidas.json')})
    print(json.dumps({'aprobado':True,'grupos':10,'fits_inventados':validation['fits_total'],'fits_panel_real':0}))
if __name__=='__main__': main()
