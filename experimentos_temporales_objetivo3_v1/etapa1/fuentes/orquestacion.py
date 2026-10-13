"""Orquestación propia. No CLI de piloto ni autorización operativa de fase2."""
import math
import time
import numpy as np
import pandas as pd
from comun import CS, CONF, GROUPS, KEYS, YEARS, seleccionar, ids_externos, metricas, validate, pesos, sha
from seguridad import guardar, TEST, destino


def plan_contratado():
    internal = [(w['externo'],i['validacion'],c['id']) for w in CONF['ventanas']
                for i in w['internas'] for c in CS if c['familia'] != 'persistencia']
    return dict(internos=internal,cota_internos=len(internal),cota_externos=24,
                cota_repeticiones=4,cota_total=378,segundos_futuros=7200,
                disponible_en_etapa1=False,control_2021='persistencia sin fit',primario='recencia_h2/global')


def dividir(panel,years,test_year,fijo=False):
    expected = [] if fijo and test_year == 2021 else [a for a in YEARS if 2018<a<test_year]
    if years != expected:
        raise ValueError('Partición temporal distinta')
    train = panel[panel.anio.isin(years)].sort_values(KEYS).reset_index(drop=True).copy()
    test = panel[panel.anio == test_year].sort_values(KEYS).reset_index(drop=True).copy()
    codes = set(panel.codigo_departamento)
    if len(test) != len(codes) or set(test.codigo_departamento) != codes:
        raise ValueError('Test incompleto')
    validate(test,finite=['prom_punt_global','puntaje_previo'])
    if years:
        validate(train,finite=['cambio_observado'])
        if len(train) != len(codes)*len(years) or set(train.anio) != set(years):
            raise ValueError('Train incompleto')
        for a in years:
            if set(train[train.anio == a].codigo_departamento) != codes:
                raise ValueError('Train año incompleto')
    return train,test


def predicciones(test,c,model,label,externo):
    delta = np.zeros(len(test)) if c['familia'] == 'persistencia' else model.predict(test[c['entradas']].to_numpy(float))
    if np.shape(delta) != (len(test),) or not np.isfinite(delta).all():
        raise ValueError('Predicciones incompletas/no finitas')
    q = test[KEYS+['anio_previo','puntaje_previo']].copy()
    q['id'],q['ajuste'],q['externo'],q['origen'] = c['id'],label,externo,'inventado'
    q['observado'] = test.prom_punt_global
    q['cambio_predicho'] = delta
    q['prediccion'] = q.puntaje_previo+q.cambio_predicho
    q['error'] = q.prediccion-q.observado
    return q


def ventana_inventada(panel,externo,budget,executor=None):
    if panel.attrs.get('origen') != 'inventado':
        raise ValueError('Panel real prohibido')
    w = next(w for w in CONF['ventanas'] if w['externo'] == externo)
    rows,parts,metas,signatures = [],[],[],{}
    internal_years = [i['validacion'] for i in w['internas']]
    if externo != 2021:
        for c in CS:
            cparts,reason = [],None
            for i in w['internas']:
                train,test = dividir(panel,i['entrenamiento'],i['validacion'])
                label = f"e{externo}_i{i['validacion']}_{c['id']}"
                context = dict(origen='inventado',externo=externo,validacion=i['validacion'],train_anios=i['entrenamiento'])
                model = None
                meta = dict(origen='inventado',sin_fit=True)
                if c['familia'] != 'persistencia':
                    try:
                        model,meta = budget.ajustar(label,c,train,context,executor)
                    except (ValueError,FloatingPointError) as exc:
                        reason = str(exc)
                        break
                q = predicciones(test,c,model,label,externo)
                cparts.append(q)
                _,wm = pesos(train[KEYS])
                signatures[(externo,c['id'],i['validacion'])] = dict(train_llaves=train[KEYS].values.tolist(),
                    train_anios=i['entrenamiento'],pesos=wm,parametros=c['parametros_completos'],
                    entradas=c['entradas'],semilla=20261010,versiones=CONF['version'])
                metas.append(dict(etiqueta=label,metadata=meta))
            if reason:
                rows.append(dict(id=c['id'],estado='inelegible',ventanas=[int(q.anio.iloc[0]) for q in cparts],mae=None,rmse=None,razon=reason))
            else:
                pred = pd.concat(cparts,ignore_index=True)
                m = metricas(pred.observado,pred.prediccion)
                rows.append(dict(id=c['id'],estado='completo',ventanas=internal_years,mae=m['mae'],rmse=m['rmse'],razon=None))
                parts.extend(cparts)
    decision = seleccionar(rows,internal_years,externo)
    selected_before_external = time.monotonic()
    selection_path = destino(budget.path.parent / f'seleccion_{externo}_inventada.json',TEST)
    guardar(selection_path,dict(origen='inventado',externo=externo,decision=decision,
                               instante_monotonico_antes_externo=selected_before_external))
    train,test = dividir(panel,w['entrenamiento'],externo,fijo=True)
    by_id = {}
    for ident in ids_externos(decision):
        c = next(c for c in CS if c['id'] == ident)
        label = f'e{externo}_externo_{ident}'
        model = None
        if c['familia'] != 'persistencia':
            context = dict(origen='inventado',externo=externo,train_anios=w['entrenamiento'],seleccion_antes_externo=selected_before_external,
                           seleccion_archivo=str(selection_path),seleccion_sha256=sha(selection_path))
            model,meta = budget.ajustar(label,c,train,context,executor)
            metas.append(dict(etiqueta=label,metadata=meta))
        by_id[ident] = predicciones(test,c,model,label,externo)
    if 'persistencia' not in by_id:
        by_id['persistencia'] = predicciones(test,CS[0],None,f'e{externo}_externo_persistencia',externo)
    external = []
    for role,ident in {'global':decision['global_id'],**decision['especificaciones'],'persistencia':'persistencia'}.items():
        external.append(by_id[ident].assign(procedimiento=role))
    return dict(decision=decision,externas=pd.concat(external,ignore_index=True),internas=parts,
                metadata=metas,firmas=signatures,seleccion_antes_externo=selected_before_external)


def comprobar_global_inventado(panel,result,externo,budget,executor=None):
    """Cinco comprobaciones contractuales; persistencia sin fit, demás repetición medida."""
    if panel.attrs.get('origen') != 'inventado':
        raise ValueError('Solo inventados')
    w = next(w for w in CONF['ventanas'] if w['externo']==externo)
    train,test = dividir(panel,w['entrenamiento'],externo,fijo=True)
    c = next(c for c in CS if c['id']==result['decision']['global_id'])
    model = None
    meta = dict(origen='inventado',sin_fit=True)
    if c['familia'] != 'persistencia':
        model,meta = budget.ajustar(f"e{externo}_repeticion_{c['id']}",c,train,
            dict(origen='inventado',externo=externo,repeticion=True,train_anios=w['entrenamiento']),executor)
    repeated = predicciones(test,c,model,f'e{externo}_control_global',externo)
    primary = result['externas'][result['externas'].procedimiento.eq('global')].reset_index(drop=True)
    from comun import exact
    exact(repeated[KEYS+['observado']],primary[KEYS+['observado']])
    if c['familia']=='persistencia':
        exact(repeated[KEYS+['prediccion']],primary[KEYS+['prediccion']])
    else:
        np.testing.assert_allclose(repeated.prediccion,primary.prediccion,atol=1e-10,rtol=0)
    return meta
