"""Solo recencia_h2; selección interna precede toda evaluación externa."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import time,json,hashlib
import numpy as np,pandas as pd
from seguridad import ROOT,OUT,E1,guardar,leer,sha,checkpoint,destino
from comun import *
from particiones import dividir,predicciones
from motor import Presupuesto,FalloNumerico
from preflight import entorno,entries,check_entries

def escribir_csv(p,q):
    p=destino(p)
    if p.exists():exact(csv(p),q.reset_index(drop=True));return
    p.parent.mkdir(parents=True,exist_ok=True);q.to_csv(p,index=False)
    exact(csv(p),q.reset_index(drop=True))
def firma(train,c):
    _,wm=pesos(train[KEYS])
    return dict(train_llaves=train[KEYS].values.tolist(),X=train[c['entradas']].to_numpy(float).tolist(),y=train.cambio_observado.tolist(),pesos=wm,entradas=c['entradas'],parametros=c['parametros_completos'],semilla=SEED,versiones=dict(python='3.12.14',sklearn='1.9.1'))
def main():
    entorno();assert leer(OUT/'preflight.json')['aprobado']
    freeze=leer(OUT/'congelacion_operativa_v2.json')
    check_entries(freeze['fuentes']);check_entries(leer(OUT/'partida.json')['protegidos'])
    p,q=reconstruir();referencias(p);comprobar_defaults();p.attrs['origen']='recencia_h2'
    context=dict(origen='recencia_h2',congelacion_sha256=sha(OUT/'congelacion_operativa_v2.json'),fuente_sha256=SPEC['heredado']['fuente_sha256'],derivado_sha256=SPEC['heredado']['derivado_sha256'],semilla=SEED,esquema='recencia_h2',entorno_sha256=sha(OUT/'entorno.json'))
    budget=Presupuesto(context);all_internal=[];all_external=[];records=[];signatures=[];checks=[];persist_times=[]
    for w in CONF['ventanas']:
        ext=w['externo'];years=[i['validacion'] for i in w['internas']];rows=[]
        if ext!=2021:
            for c in CS:
                parts=[];reason=None
                for i in w['internas']:
                    train,test=dividir(p,i['entrenamiento'],i['validacion']);train.attrs['origen']='recencia_h2'
                    label=f'e{ext}_i{i["validacion"]}_{c["id"]}';model=None
                    sig=firma(train,c);path=OUT/'predicciones_por_ajuste'/f'{label}.csv'
                    ctx=dict(origen='recencia_h2',externo=ext,validacion=i['validacion'],firma_sha256=hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest())
                    if c['familia']!='persistencia':
                        try:model,meta=budget.ajustar(label,c,train,ctx)
                        except FalloNumerico as e:reason=str(e);break
                    start=time.monotonic();pred=predicciones(test,c,model,label,ext)
                    if c['familia']=='persistencia':persist_times.append(dict(ajuste=label,segundos=time.monotonic()-start,sin_fit=True))
                    escribir_csv(path,pred);parts.append(pred)
                    signatures.append(dict(externo=ext,id=c['id'],validacion=i['validacion'],firma=sig))
                if reason:
                    rows.append(dict(id=c['id'],estado='inelegible',ventanas=[int(x.anio.iloc[0]) for x in parts],mae=None,rmse=None,razon=reason))
                else:
                    pred=pd.concat(parts,ignore_index=True);m=metricas(pred.observado,pred.prediccion)
                    rows.append(dict(id=c['id'],estado='completo',ventanas=years,mae=m['mae'],rmse=m['rmse'],razon=None));all_internal.extend(parts)
            records.extend(dict(externo=ext,**r) for r in rows)
        decision=seleccionar(rows,years,ext);selection=OUT/f'seleccion_{ext}.json'
        doc=dict(externo=ext,decision=decision,antes_externo=True,origen='recencia_h2',criterio='internas exclusivamente')
        if selection.exists():assert leer(selection)==doc
        else:guardar(selection,doc)
        train,test=dividir(p,w['entrenamiento'],ext,fijo=True);train.attrs['origen']='recencia_h2';by_id={}
        for ident in ids_externos(decision):
            c=next(c for c in CS if c['id']==ident);label=f'e{ext}_externo_{ident}';model=None
            if c['familia']!='persistencia':
                sig=firma(train,c)
                ctx=dict(origen='recencia_h2',externo=ext,seleccion_sha256=sha(selection),firma_sha256=hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest())
                model,meta=budget.ajustar(label,c,train,ctx)
            start=time.monotonic();by_id[ident]=predicciones(test,c,model,label,ext)
            if c['familia']=='persistencia':persist_times.append(dict(ajuste=label,segundos=time.monotonic()-start,sin_fit=True))
            escribir_csv(OUT/'predicciones_por_ajuste'/f'{label}.csv',by_id[ident])
        if 'persistencia' not in by_id:
            start=time.monotonic();by_id['persistencia']=predicciones(test,CS[0],None,f'e{ext}_externo_persistencia',ext)
            persist_times.append(dict(ajuste=f'e{ext}_externo_persistencia',segundos=time.monotonic()-start,sin_fit=True))
        external=pd.concat([by_id[ident].assign(procedimiento=role) for role,ident in {'global':decision['global_id'],**decision['especificaciones'],'persistencia':'persistencia'}.items()],ignore_index=True)
        escribir_csv(OUT/f'externas_{ext}.csv',external);all_external.append(external)
        c=next(c for c in CS if c['id']==decision['global_id']);model=None;label=f'e{ext}_repeticion_{c["id"]}'
        if c['familia']!='persistencia':
            sig=firma(train,c);ctx=dict(origen='recencia_h2',externo=ext,repeticion=True,seleccion_sha256=sha(selection),firma_sha256=hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest())
            model,meta=budget.ajustar(label,c,train,ctx)
        start=time.monotonic();rep=predicciones(test,c,model,label,ext);primary=external[external.procedimiento.eq('global')].reset_index(drop=True)
        exact(rep[KEYS+['observado']],primary[KEYS+['observado']])
        if c['familia']=='persistencia':
            exact(rep[KEYS+['prediccion']],primary[KEYS+['prediccion']]);persist_times.append(dict(ajuste=label,segundos=time.monotonic()-start,sin_fit=True))
        else:np.testing.assert_allclose(rep.prediccion,primary.prediccion,atol=1e-10,rtol=0)
        escribir_csv(OUT/'repeticiones'/f'{ext}.csv',rep);checks.append(dict(externo=ext,id=c['id'],aprobado=True,sin_fit=c['familia']=='persistencia',atol=0 if c['familia']=='persistencia' else 1e-10,rtol=0))
        checkpoint(OUT/'progreso.json',dict(ventana_completa=ext,intentos=len(budget.data['ajustes']),segundos=budget.data['consumido']))
    internal=pd.concat(all_internal,ignore_index=True);external=pd.concat(all_external,ignore_index=True)
    escribir_csv(OUT/'predicciones_internas.csv',internal);escribir_csv(OUT/'predicciones_externas.csv',external)
    for name,obj in [('registros_internos.json',records),('firmas_internas.json',signatures),('comprobaciones_globales.json',checks),('tiempos_persistencia.json',persist_times)]:
        if not (OUT/name).exists():guardar(OUT/name,obj)
    assert len(records)==144 and len(external)==1155 and len(internal)==11880,'Cobertura indispensable incompleta'
    assert len(budget.data['ajustes'])<=378 or any(r['clase_fallo']=='infraestructura' for r in budget.data['ajustes'])
    checkpoint(OUT/'ejecucion.json',dict(completa=True,intentos=len(budget.data['ajustes']),segundos=budget.data['consumido'],internas=len(internal),externas=len(external),registros=len(records),primario='recencia_h2/global'))
if __name__=='__main__':
    try:main()
    except BaseException as e:
        checkpoint(OUT/'incompleto.json',dict(estado='INCOMPLETO',tipo=type(e).__name__,razon=str(e),sin_rescate=True))
        raise
