"""Interfaces v4: importar/construir no ajusta. Escrituras exclusivamente v4."""
import sys, os
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
V4 = ROOT/'experimentos_objetivo3_v4'
E1 = V4/'etapa1'
OUT = E1/'resultados'
sys.path.insert(0,str(ROOT/'experimentos_objetivo3_v3/etapa1/fuentes'))
import comun_v3 as v3
# La importación heredada antepone carpetas anteriores; los hijos spawn deben
# resolver siempre los módulos propios v4 antes de módulos con el mismo nombre.
sys.path.insert(0,str(Path(__file__).resolve().parent))
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import HuberRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import json, types, re, math
anterior = v3.anterior
compartido = v3.compartido
sha, metricas, serial = v3.sha, v3.metricas, v3.serial
SEMILLA, LLAVES = v3.SEMILLA, v3.LLAVES
ventanas, dividir = v3.ventanas, v3.dividir
reconstruir, persistencia = v3.reconstruir, v3.persistencia
ORDEN = ['persistencia','correccion_comun','ridge','huber']
COV = anterior.ESPECIFICACIONES['ambas']
GRUPOS = dict(historico=['puntaje_previo'],nivel_ipm=['puntaje_previo','ipm'],
    cambio_ipm=['puntaje_previo','cambio_ipm'],
    cambio_tasas=['puntaje_previo',*['cambio_'+s for s in anterior.ESPECIFICACIONES['tasas']]],
    cambio_ambas=['puntaje_previo',*['cambio_'+s for s in COV]])

def destino(path):
    p=Path(path).resolve()
    if not p.is_relative_to(V4.resolve()): raise ValueError('escritura fuera de v4')
    p.parent.mkdir(parents=True,exist_ok=True)
    return p
def guardar(path,obj): compartido.guardar(destino(path),obj)
def read(path): return json.loads(Path(path).read_text())

def historial(panel):
    p=v3.historial(panel)
    for s in COV:
        p['previo_'+s]=p.groupby('codigo_departamento',sort=False)[s].shift(1)
        p['cambio_'+s]=p[s]-p['previo_'+s]
    p['intervalo']=p.anio-p.anio_previo
    return p

class CorreccionComun(RegressorMixin,BaseEstimator):
    """Estima solo mediana del objetivo recibido; X únicamente determina n predicciones."""
    def __init__(self,lam=1.): self.lam=lam
    def fit(self,X,y):
        y=np.asarray(y,float)
        if y.ndim!=1 or not len(y) or len(X)!=len(y) or not np.isfinite(y).all():raise ValueError('train inválido')
        if self.lam not in (.25,.5,1.):raise ValueError('lambda no autorizado')
        self.mediana_=float(np.median(y));self.n_train_=len(y)
        return self
    def predict(self,X):
        if not hasattr(self,'mediana_'):raise ValueError('sin ajuste')
        return np.full(len(X),self.lam*self.mediana_)

def construir(c):
    if c['familia']=='persistencia':raise ValueError('persistencia sin fit')
    if c['familia']=='correccion_comun':return CorreccionComun(**c['parametros'])
    if c['familia']=='ridge':return anterior.construir(c)
    if c['familia']=='huber':return Pipeline([('escalado',StandardScaler()),('modelo',HuberRegressor(**c['parametros']))])
    raise ValueError('familia no autorizada')

def candidatos():
    result=[]
    def add(family,group,params,ident):
        entries=['puntaje_previo'] if group is None else GRUPOS[group]
        c=dict(id=ident,familia=family,especificacion=group,parametros=params,
            entradas=entries,n_ajustadas=0 if group is None else len(entries),orden=len(result))
        c['parametros_completos']={} if family=='persistencia' else serial(construir(c).get_params(deep=True))
        result.append(c)
    add('persistencia',None,{},'persistencia')
    for i,lam in enumerate((.25,.5,1.)):add('correccion_comun',None,dict(lam=lam),f'correccion_comun_{i:02d}')
    for family,alphas in [('ridge',(1,10,100)),('huber',(.01,1))]:
        for group in GRUPOS:
            for i,alpha in enumerate(alphas):
                params={**anterior.FIJOS['ridge'],'alpha':alpha} if family=='ridge' else dict(alpha=alpha,epsilon=1.35,fit_intercept=True,max_iter=2000,tol=1e-5,warm_start=False)
                add(family,group,params,f'{family}_{group}_{i:02d}')
    assert len(result)==29
    return result

def matrices_entrenamiento(p,c):
    if c['familia']=='persistencia':raise ValueError('sin entrenamiento')
    expected=['puntaje_previo'] if c['familia']=='correccion_comun' else GRUPOS[c['especificacion']]
    if c['entradas']!=expected:raise ValueError('entradas no autorizadas')
    if p.anio.isin([2018,2020]).any():raise ValueError('objetivo no autorizado')
    X=p[expected].to_numpy(float);y=p.cambio_observado.to_numpy(float)
    if not len(y) or not np.isfinite(X).all() or not np.isfinite(y).all():raise ValueError('sin imputación')
    return X,y

_proxy=types.SimpleNamespace(TOL_MAE=.1,TOL_RMSE=.1,ORDEN=ORDEN)
_selector=types.FunctionType(compartido.seleccionar.__code__,{**compartido.seleccionar.__globals__,'cfg':_proxy})
def seleccionar(rows,expected,externo):
    if externo==2021:
        if rows or expected:raise ValueError('2021 sin selección')
        return dict(global_id='persistencia',especificaciones={s:'persistencia' for s in GRUPOS})
    w=next(w for w in ventanas() if w['externo']==externo)
    if expected!=[i['validacion'] for i in w['internas']]:raise ValueError('internas incorrectas')
    cs={c['id']:c for c in candidatos()}
    if len(rows)!=29 or {r['id'] for r in rows}!=set(cs):raise ValueError('29 candidatos incluso fallidos')
    adapted=[]
    for r in rows:
        if set(r)!={'id','estado','ventanas','mae','rmse'}:raise ValueError('campos ajenos a internas')
        c=cs[r['id']]
        adapted.append({**r,'familia':c['familia'],'especificacion':c['especificacion'],'n_predictores':c['n_ajustadas'],'orden':c['orden']})
    p=adapted[0]
    if p['estado']!='completo' or p['ventanas']!=expected or not all(math.isfinite(p[k]) for k in ('mae','rmse')):raise ValueError('persistencia indispensable')
    return dict(global_id=_selector(adapted,expected),especificaciones={s:_selector([r for r in adapted if r['especificacion'] in (None,s)],expected) for s in GRUPOS})
def ids_externos(decision):
    order={c['id']:c['orden'] for c in candidatos()}
    return sorted({decision['global_id'],*decision['especificaciones'].values()},key=order.__getitem__)
def etiqueta_interna(label):
    match=re.fullmatch(r'e(202[2-5])_i(202[1-4])_(.+)',label)
    return bool(match and int(match[2])<int(match[1]) and match[3] in {c['id'] for c in candidatos()})

class Presupuesto(compartido.Presupuesto):
    def __init__(self,path,limit=7200):super().__init__(destino(path),limit)

def ajuste_con_fallos(b,label,estimator,X,y,executor=None):
    """Interfaz de control: intentos persistentes; el orquestador futuro debe verificar artefactos."""
    previous=[r for r in b.data['ajustes'] if r.get('etiqueta','').startswith(label+'#')]
    if any(r['estado']=='ok' for r in previous):raise ValueError('ajuste completado; verificar artefacto antes de reutilizar')
    if any(r.get('clase_fallo')=='numerico_convergencia' for r in previous):raise ValueError('inelegible persistente')
    if len(previous)>=2:raise RuntimeError('infraestructura persistente')
    for attempt in range(len(previous)+1,3):
        try:return b.ajustar(f'{label}#{attempt}',estimator,X,y,executor=executor)
        except (FloatingPointError,ValueError):
            b.data['ajustes'][-1]['clase_fallo']='numerico_convergencia';guardar(b.path,b.data)
            raise
        except RuntimeError as exc:
            infrastructure=any(s in str(exc) for s in ('OSError','EOFError','BrokenPipeError','ConnectionError'))
            if not infrastructure:
                b.data['ajustes'][-1]['clase_fallo']='numerico_convergencia';guardar(b.path,b.data)
                raise ValueError('numérico/convergencia inelegible') from exc
            if attempt==2:raise
        except (OSError,EOFError):
            if attempt==2:raise
