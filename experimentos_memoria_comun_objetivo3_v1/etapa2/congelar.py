"""Congela orquestación probada antes del primer fit real; no altera etapa1."""
from comun import *

def verify_freeze():
    freeze=load(HERE/'CONGELACION_FASE3.json')
    assert freeze['antes_de_fits_reales'] and freeze['fits_reales']==0
    for p,h in freeze['fuentes_sha256'].items(): assert digest(safe_path(HERE,p))==h
    for p,h in freeze['etapa1_sha256'].items(): assert digest(E1/p)==h
    assert environment()['aprobado'] and conservation()['aprobado']
    return freeze
def main():
    controls=load(HERE/'resultados/sinteticos/corrida_002/CONTROLES.json')
    assert controls['aprobado'] and controls['fits_panel_real']==0
    assert all(digest(HERE/p)==h for p,h in controls['fuentes_sha256'].items())
    assert environment()['aprobado'] and conservation()['aprobado']
    assert load(HERE/'SEMANTICA_FASE3.json')['aprobado']
    assert not (HERE/'resultados/piloto/ledger.json').exists()
    fresh('CONGELACION_FASE3.json',{'version':'1.0.0','fecha_cliente':'2026-10-11','timezone':'America/Bogota',
          'antes_de_fits_reales':True,'fits_reales':0,'reglas':'fase1 aprobada/fase2 congelada/PROTOCOLO_ETAPA2.md',
          'fuentes_sha256':{p.name:digest(p) for p in HERE.glob('*.py')} | {'PROTOCOLO_ETAPA2.md':digest(HERE/'PROTOCOLO_ETAPA2.md'),
              'ENTORNO_FASE3.json':digest(HERE/'ENTORNO_FASE3.json'),'PREFLIGHT_FASE3.json':digest(HERE/'PREFLIGHT_FASE3.json'),
              'SEMANTICA_FASE3.json':digest(HERE/'SEMANTICA_FASE3.json'),'resultados/sinteticos/corrida_002/CONTROLES.json':digest(HERE/'resultados/sinteticos/corrida_002/CONTROLES.json')},
          'etapa1_sha256':{p:digest(E1/p) for p in ('motor.py','integridad.py','ejecucion_sintetica.py','preflight.py','CONGELACION_FASE2.json','ACEPTACION_FASE2.json','MANIFIESTO_FASE2.json')},
          'semilla':SEED,'presupuesto_nuevo':7200,'saldo_heredado':None,'cota':46,'candidatos':CANDIDATES,'ventanas':[window(y) for y in YEARS[2:]],
          'controles_inventados':controls['grupos'],'no_autoriza':'fase4/modelo final/notebook personal/simulación/objetivo4/fuentes nuevas/instalaciones/commit/push'})
    verify_freeze(); print(json.dumps({'congelada':True,'fits_reales':0}))
if __name__=='__main__': main()
