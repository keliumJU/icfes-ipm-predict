"""Adaptadores prospectivos: importar no ajusta; toda salida está limitada a v3."""
import sys, os
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
V3 = ROOT/'experimentos_objetivo3_v3'
E1 = V3/'etapa1'
sys.path.insert(0, str(ROOT/'experimentos_objetivo3_v2/fase2/fuentes'))
import configuracion as anterior
import comun as compartido
from congelar import serial
import json, types, time, re
import numpy as np
import pandas as pd
SEMILLA = 20261010
LLAVES = anterior.LLAVES
ANIOS = anterior.ANIOS
ORDEN = ['persistencia', *anterior.ORDEN[1:]]
ESPECIFICACIONES = {k:['puntaje_previo',*v] for k,v in anterior.ESPECIFICACIONES.items()}
sha = compartido.sha
metricas = compartido.metricas
condicion_personal = compartido.condicion_personal

def destino(path):
    p = Path(path).resolve()
    if not p.is_relative_to(V3.resolve()): raise ValueError('escritura fuera de v3')
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def guardar(path,obj):
    compartido.guardar(destino(path),obj)

def read(path): return json.loads(Path(path).read_text())

def candidatos():
    old = read(anterior.F2/'resultados/configuraciones_congeladas.json')
    result = [dict(id='persistencia',id_v2=None,familia='persistencia',especificacion=None,
                   parametros={},parametros_completos={},entradas=['puntaje_previo'],n_ajustadas=0,orden=0)]
    for c in old['configuraciones']:
        if c['familia']=='media': continue
        c = {**c,'id_v2':c['id'],'id':'delta_'+c['id'],
             'entradas':ESPECIFICACIONES[c['especificacion']], 'orden':len(result)}
        c['n_ajustadas']=len(c['entradas'])
        assert serial(anterior.construir(c).get_params(deep=True))==c['parametros_completos']
        result.append(c)
    assert len(result)==100 and len({c['id'] for c in result})==100
    return result

def construir(c):
    if c['familia']=='persistencia': raise ValueError('persistencia no tiene estimador ni ajuste')
    return anterior.construir(c)

def historial(p):
    p=compartido.normalizar_codigos(p).sort_values(LLAVES).copy()
    if p.duplicated(LLAVES).any() or not set(p.anio)<=set(ANIOS): raise ValueError('llaves/años inválidos')
    group=p.groupby('codigo_departamento',sort=False)
    p['anio_previo']=group.anio.shift(1).astype('Int64')
    p['puntaje_previo']=group[anterior.RESULTADO].shift(1)
    p['cambio_observado']=p[anterior.RESULTADO]-p.puntaje_previo
    available=p.anio_previo.notna()
    assert (p.loc[available,'anio_previo']<p.loc[available,'anio']).all()
    return p

def ventanas():
    return [dict(externo=y,entrenamiento=[a for a in ANIOS if 2018<a<y],
                 procedimiento='persistencia_fija' if y==2021 else 'seleccion_interna',
                 internas=[dict(validacion=i,entrenamiento=[a for a in ANIOS if 2018<a<i])
                           for i in ANIOS if 2021<=i<y]) for y in range(2021,2026)]

def dividir(p,train_years,test_year):
    if 2018 in train_years or 2020 in train_years: raise ValueError('objetivo sin cambio autorizado')
    train,test=compartido.dividir(p,train_years,test_year)
    if train.cambio_observado.isna().any() or test.puntaje_previo.isna().any(): raise ValueError('historial ausente')
    return train,test

def reconstruir(previo,cambio):
    prev=np.asarray(previo,float); delta=np.asarray(cambio,float)
    if prev.shape!=delta.shape or not np.isfinite(prev).all() or not np.isfinite(delta).all():
        raise ValueError('reconstrucción inválida')
    result=prev+delta
    if not np.isfinite(result).all(): raise ValueError('resultado no finito')
    return result

def persistencia(p):
    started=time.monotonic()
    prev=p.puntaje_previo.to_numpy(float).copy()
    if not np.isfinite(prev).all():raise ValueError('historial ausente')
    return prev,dict(segundos_calculo=time.monotonic()-started,ajustes=0,informacion='un puntaje histórico')

# Reutiliza exactamente el algoritmo de bandas v2, con orden prospectivo propio.
_proxy=types.SimpleNamespace(TOL_MAE=0.1,TOL_RMSE=0.1,ORDEN=ORDEN)
_selector=types.FunctionType(compartido.seleccionar.__code__,{**compartido.seleccionar.__globals__,'cfg':_proxy})
def seleccionar(rows,expected,externo):
    if externo==2021:
        if rows or expected: raise ValueError('2021 sin métricas ni selección de candidatos')
        return {'global_id':'persistencia','especificaciones':{s:'persistencia' for s in ESPECIFICACIONES}}
    w=next(w for w in ventanas() if w['externo']==externo)
    if expected != [i['validacion'] for i in w['internas']]:raise ValueError('internas incompletas')
    allowed={c['id']:c for c in candidatos()}
    adapted=[]
    for r in rows:
        c=allowed[r['id']]
        if any(k not in {'id','estado','ventanas','mae','rmse'} for k in r):raise ValueError('campos ajenos a selección interna')
        adapted.append({**r,'familia':c['familia'],'especificacion':c['especificacion'],
                        'n_predictores':c['n_ajustadas'],'orden':c['orden']})
    if set(allowed)!=set(r['id'] for r in adapted):raise ValueError('deben registrar los 100 candidatos incluso fallidos')
    return dict(global_id=_selector(adapted,expected),especificaciones={s:_selector(
        [r for r in adapted if r['especificacion'] in (None,s)],expected) for s in ESPECIFICACIONES})

def ids_externos(decision):
    return sorted(set([decision['global_id'],*decision['especificaciones'].values()]),
                  key=lambda ident:next(c['orden'] for c in candidatos() if c['id']==ident))

def etiqueta_interna(label):
    return re.fullmatch(r'e(202[2-5])_i(202[1-4])_(delta_.+|persistencia)',label) is not None

class Presupuesto(compartido.Presupuesto):
    """Mismo motor serial/spawn v2; ledger exclusivamente nuevo dentro de v3."""
    def __init__(self,path,limit=7200):
        super().__init__(destino(path),limit)

def matrices_entrenamiento(p,c):
    """Sin fit: prepara X y cambio, rechaza filas sin objetivo y columnas no congeladas."""
    if c['familia']=='persistencia':raise ValueError('persistencia no requiere entrenamiento')
    if c['entradas']!=ESPECIFICACIONES[c['especificacion']]:raise ValueError('entradas no autorizadas')
    if p.cambio_observado.isna().any() or p.anio.eq(2018).any() or p.anio.eq(2020).any():
        raise ValueError('objetivos de cambio no disponibles')
    X=p[c['entradas']].to_numpy(float);y=p.cambio_observado.to_numpy(float)
    if not np.isfinite(X).all() or not np.isfinite(y).all():raise ValueError('datos no finitos, sin imputación')
    return X,y
