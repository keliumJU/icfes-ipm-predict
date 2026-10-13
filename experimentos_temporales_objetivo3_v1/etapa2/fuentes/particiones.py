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
    q['id'],q['ajuste'],q['externo'],q['origen'] = c['id'],label,externo,'recencia_h2'
    q['observado'] = test.prom_punt_global
    q['cambio_predicho'] = delta
    q['prediccion'] = q.puntaje_previo+q.cambio_predicho
    q['error'] = q.prediccion-q.observado
    return q

