"""Diseño 5.0.0: no runner ni fit automático; destinos propios y ledger solo sintético."""
import sys, os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[key]='1'
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
V5=ROOT/'experimentos_objetivo3_v5'; E1=V5/'etapa1'; OUT=E1/'resultados'
sys.path.insert(0,str(ROOT/'experimentos_objetivo3_v4/etapa1/fuentes'))
import comun_v4 as previo
sys.path.insert(0,str(Path(__file__).resolve().parent))
import json, math, re, types, copy
import numpy as np
import pandas as pd
from sklearn.linear_model import QuantileRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
SEMILLA=20261010
LLAVES=list(previo.LLAVES); COV=list(previo.COV)
GRUPOS=copy.deepcopy(previo.GRUPOS)
ORDEN=['persistencia','mediana','boosting_absoluto']
sha=previo.sha; serial=previo.serial; metricas=previo.metricas
historial=previo.historial; reconstruir=previo.reconstruir; persistencia=previo.persistencia
ANIOS=[2018,2019,2021,2022,2023,2024,2025]
PROCEDIMIENTOS=['global',*GRUPOS,'persistencia']

def destino(path):
    p=Path(path).resolve()
    if not p.is_relative_to(V5.resolve()): raise ValueError('escritura fuera de v5')
    p.parent.mkdir(parents=True,exist_ok=True)
    return p

def guardar(path,obj): previo.compartido.guardar(destino(path),obj)
def read(path): return json.loads(Path(path).read_text())
def check_hashes(mapping):
    for path,h in mapping.items():
        if sha(ROOT/path)!=h: raise ValueError('huella distinta: '+path)

def construir(c):
    if c['familia']=='mediana':
        return Pipeline([('escalado',StandardScaler()),('modelo',QuantileRegressor(**c['parametros']))])
    if c['familia']=='boosting_absoluto': return GradientBoostingRegressor(**c['parametros'])
    raise ValueError('persistencia sin fit o familia ajena')

def candidatos():
    result=[]
    def add(f,g,p,ident):
        c=dict(id=ident,familia=f,especificacion=g,parametros=p,entradas=['puntaje_previo'] if g is None else list(GRUPOS[g]),n_ajustadas=0 if g is None else len(GRUPOS[g]),orden=len(result))
        c['parametros_completos']={} if f=='persistencia' else serial(construir(c).get_params(deep=True))
        result.append(c)
    add('persistencia',None,{},'persistencia')
    for g in GRUPOS:
        for i,a in enumerate((.01,.1,1.)):
            add('mediana',g,dict(alpha=a,quantile=.5,fit_intercept=True,solver='highs',solver_options=None),f'mediana_{g}_{i:02d}')
    for g in GRUPOS:
        for j,lr in enumerate((.03,.1)):
            for k,depth in enumerate((1,2)):
                add('boosting_absoluto',g,dict(loss='absolute_error',learning_rate=lr,max_depth=depth,n_estimators=100,min_samples_leaf=3,subsample=1.,random_state=SEMILLA,n_iter_no_change=None),f'boosting_absoluto_{g}_{2*j+k:02d}')
    assert len(result)==36 and len({c['id'] for c in result})==36
    return result

def ventanas():
    return [dict(externo=y,entrenamiento=[] if y==2021 else [a for a in ANIOS if 2018<a<y],procedimiento='persistencia_fija' if y==2021 else 'seleccion_interna',internas=[dict(validacion=i,entrenamiento=[a for a in ANIOS if 2018<a<i]) for i in ANIOS if 2021<=i<y]) for y in range(2021,2026)]

def dividir(p,train_years,test_year):
    if test_year==2021 and not train_years: return p.iloc[:0].copy(),p[p.anio==2021].sort_values(LLAVES).copy()
    if train_years!=[a for a in ANIOS if 2018<a<test_year]: raise ValueError('entrenamiento no expansivo anterior')
    return previo.dividir(p,train_years,test_year)

def matrices_entrenamiento(p,c):
    if c['familia']=='persistencia':raise ValueError('sin entrenamiento')
    if c['entradas']!=GRUPOS[c['especificacion']]:raise ValueError('entradas no autorizadas')
    if not set(p.anio)<=set(ANIOS[1:]) or p.anio.eq(2020).any():raise ValueError('objetivo no autorizado')
    X=p[c['entradas']].to_numpy(float); y=p.cambio_observado.to_numpy(float)
    if not len(y) or not np.isfinite(X).all() or not np.isfinite(y).all():raise ValueError('sin imputación')
    return X,y

_proxy=types.SimpleNamespace(TOL_MAE=.1,TOL_RMSE=.1,ORDEN=ORDEN)
_selector=types.FunctionType(previo.compartido.seleccionar.__code__,{**previo.compartido.seleccionar.__globals__,'cfg':_proxy})
def seleccionar(rows,expected,externo):
    if externo==2021:
        if rows or expected:raise ValueError('2021 sin puntuar candidatos')
        return dict(global_id='persistencia',especificaciones={s:'persistencia' for s in GRUPOS},candidatos=[])
    w=next((w for w in ventanas() if w['externo']==externo),None)
    if w is None or expected!=[i['validacion'] for i in w['internas']]:raise ValueError('internas incorrectas')
    cs={c['id']:c for c in candidatos()}
    if [r['id'] for r in rows]!=list(cs):raise ValueError('36 candidatos incluidos inelegibles en orden JSON')
    adapted=[]; audit=[]
    for r in rows:
        if set(r)!={'id','estado','ventanas','mae','rmse','razon'}:raise ValueError('campos ajenos a internas/razón ausente')
        c=cs[r['id']]
        eligible=r['estado']=='completo' and r['ventanas']==expected and all(isinstance(r[k],(int,float)) and math.isfinite(r[k]) and r[k]>=0 for k in ('mae','rmse'))
        if not eligible and not r['razon']:raise ValueError('inelegible sin razón')
        if r['estado']!='completo' and not r['razon']:raise ValueError('fallo sin razón')
        adapted.append({**r,'estado':'completo' if eligible else 'inelegible','familia':c['familia'],'especificacion':c['especificacion'],'n_predictores':c['n_ajustadas'],'orden':c['orden']})
        audit.append({**r,'elegible':eligible,'razon':r['razon'] if not eligible else None})
    if not audit[0]['elegible'] or audit[0]['id']!='persistencia':raise ValueError('persistencia indispensable en orden JSON')
    return dict(global_id=_selector(adapted,expected),especificaciones={g:_selector([r for r in adapted if r['especificacion'] in (None,g)],expected) for g in GRUPOS},candidatos=audit)

def ids_externos(decision):
    order={c['id']:c['orden'] for c in candidatos()}
    return sorted({decision['global_id'],*decision['especificaciones'].values()},key=order.__getitem__)

def igualdad_exacta(a,b):
    """Mismos campos, orden, índices y valores; solo dtype inferido no es criterio CSV."""
    pd.testing.assert_frame_equal(a,b,check_dtype=False,check_exact=True)

def cobertura(frame,codes):
    codes=set(codes)
    if len(codes)!=33 or len(frame)!=1155:raise ValueError('cobertura incompleta')
    if set(frame.procedimiento)!=set(PROCEDIMIENTOS):raise ValueError('procedimientos incompletos')
    expected={(c,y) for c in codes for y in range(2021,2026)}
    for role in PROCEDIMIENTOS:
        q=frame[frame.procedimiento==role]
        if len(q)!=165 or q.duplicated(LLAVES).any() or set(map(tuple,q[LLAVES].to_numpy()))!=expected:raise ValueError('llaves incompletas')
        if not np.isfinite(q[['observado','prediccion']].to_numpy(float)).all():raise ValueError('no finito')
    base=frame[frame.procedimiento=='global'].sort_values(LLAVES)[LLAVES+['observado']].reset_index(drop=True)
    for role in PROCEDIMIENTOS:igualdad_exacta(base,frame[frame.procedimiento==role].sort_values(LLAVES)[LLAVES+['observado']].reset_index(drop=True))
    return True

def verificar_reanudacion(contexto,actual,artefactos,b,label):
    if contexto!=actual:raise ValueError('contexto distinto')
    check_hashes(artefactos)
    attempts=[r for r in b.data['ajustes'] if r.get('etiqueta','').startswith(label+'#')]
    if any(r.get('clase_fallo')=='numerico_convergencia' for r in attempts):raise ValueError('inelegible persistente')
    if len(attempts)>2:raise ValueError('intentos excedidos')
    if any(r['estado']=='ok' for r in attempts) and not artefactos:raise ValueError('artefactos ausentes')
    return len(attempts)

class PresupuestoSintetico(previo.compartido.Presupuesto):
    """Interfaz etapa1: solo directorios sintéticos. No ledger operativo del panel."""
    def __init__(self,path,limit=7200):
        p=Path(path).resolve()
        if not p.is_relative_to((OUT/'sinteticos').resolve()):raise ValueError('ledger solo sintético etapa1')
        super().__init__(destino(p),limit)

def ajuste_con_fallos(b,label,estimator,X,y,executor=None):
    attempts=[r for r in b.data['ajustes'] if r.get('etiqueta','').startswith(label+'#')]
    if any(r['estado']=='ok' for r in attempts):raise ValueError('ya completo: verificar artefactos antes de reutilizar')
    if any(r.get('clase_fallo')=='numerico_convergencia' for r in attempts):raise ValueError('inelegible persistente')
    if len(attempts)>=2:raise RuntimeError('infraestructura persistente')
    if b.data['consumido']>=b.limit:raise TimeoutError('sin saldo, sin intento ficticio')
    for attempt in range(len(attempts)+1,3):
        try:return b.ajustar(f'{label}#{attempt}',estimator,X,y,executor=executor)
        except TimeoutError:raise
        except (FloatingPointError,ValueError):
            b.data['ajustes'][-1]['clase_fallo']='numerico_convergencia';guardar(b.path,b.data);raise
        except RuntimeError as exc:
            if not any(s in str(exc) for s in ('OSError','EOFError','BrokenPipeError','ConnectionError')):
                b.data['ajustes'][-1]['clase_fallo']='numerico_convergencia';guardar(b.path,b.data)
                raise ValueError('numérico/convergencia inelegible') from exc
            b.data['ajustes'][-1]['clase_fallo']='infraestructura';guardar(b.path,b.data)
            if attempt==2:raise
        except (OSError,EOFError):
            b.data['ajustes'][-1]['clase_fallo']='infraestructura';guardar(b.path,b.data)
            if attempt==2:raise
