"""Punto de entrada único del piloto expresamente autorizado en esta sesión."""
from comun import *
from congelar import verify_freeze
from panel import validated_panel
from runner import Ledger, execute
from verificar import validate_outputs
import traceback

def main():
    freeze=verify_freeze()
    context=context_hash({'freeze':digest(HERE/'CONGELACION_FASE3.json'),'sources':load(HERE/'SEMANTICA_FASE3.json')['fuentes'],'seed':SEED})
    ledger=Ledger('resultados/piloto',context)
    try:
        levels,proof=validated_panel(); fresh('resultados/piloto/REVALIDACION_PANEL.json',proof)
        data=execute(levels,ledger)
        fresh('resultados/piloto/salidas.json',data)
        validation=validate_outputs(data,levels,ledger); fresh('resultados/VALIDACION_PILOTO.json',validation)
        for key,name in [('internal','predicciones_internas_originales'),('external','predicciones_externas'),('records','registros_seleccion'),('unique','predicciones_internas_unicas')]:
            csv_write('resultados/'+name+'.csv',data[key])
        fresh('resultados/linaje_internas.json',data['lineage']); fresh('resultados/selecciones.json',data['selections'])
        fresh('resultados/comprobaciones_global.json',data['global_checks'])
        # Métricas descriptivas predefinidas; no elige políticas por externas.
        ms=[]
        for policy in CANDIDATES+('global',):
            rows=[r for r in data['external'] if r['policy']==policy]
            ms.append({'policy':policy,**metrics([r['observed'] for r in rows],[r['predicted'] for r in rows])})
        csv_write('resultados/metricas_externas.csv',ms)
        baseline=ms[0]['MAE']; primary=ms[-1]['MAE']
        assert baseline>0 and isfinite(baseline)
        improvement=100*(baseline-primary)/baseline
        fresh('resultados/meta.json',{'primario':'procedimiento global predefinido','n':165,'MAE_persistencia':baseline,'MAE_global':primary,
                'mejora_porcentaje':improvement,'meta_porcentaje':5,'meta_satisfecha':improvement>=5,'seleccion':'exclusivamente internas; políticas externas diagnósticas sin sustitución',
                'interpretacion':'exploratorio, todos2021–2025vistos; sin confirmación independiente/causalidad'})
        ledger.tick(); ledger.save()
        print(json.dumps({'piloto_completo':True,'fits':validation['fits_total'],'used_seconds':ledger.state['used'],'meta':load(HERE/'resultados/meta.json')}))
    except BaseException as exc:
        ledger.tick(); ledger.close()
        write('resultados/INCOMPLETO.json',{'completa':False,'reason':repr(exc),'traceback':traceback.format_exc(),'ledger':ledger.state,'sin_sintesis_dependiente':True})
        raise
if __name__=='__main__': main()
