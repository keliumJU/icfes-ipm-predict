"""Implementación v1. Sin loaders de datos/modelos ni runners históricos.

La sesión fase2 llama exclusivamente con niveles inventados. Orden estable
territorio/año; selección en puntos originales y peso igual territorio-año.
"""
from dataclasses import dataclass
from math import fsum, sqrt, isfinite
import warnings
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import QuantileRegressor
from sklearn.exceptions import ConvergenceWarning

SEED = 20261010
YEARS = (2018, 2019, 2021, 2022, 2023, 2024, 2025)
CODES = ('05','08','11','13','15','17','18','19','20','23','25','27','41','44','47','50','52','54','63','66','68','70','73','76','81','85','86','88','91','94','95','97','99')
CANDIDATES = ('persistencia','memoria','comun','comun_correccion')
INPUTS = (0,1,1,2)
COMPONENTS = ((), ('memoria',), ('comun',), ('comun','correccion'))
SCALER = {'copy':True,'with_mean':True,'with_std':True}
REGRESSOR = {'quantile':0.5,'alpha':1.0,'fit_intercept':True,'solver':'highs','solver_options':None}
FUTURE_CONTRACT = {'presupuesto_segundos':7200,'internos':24,'externos':16,'repeticiones_max':6,'cota_sin_fallos':46,'saldo_heredado':None}

class IntegrityError(ValueError):
    pass

class NumericalFailure(RuntimeError):
    pass

def levels_from_rows(rows):
    """Adaptador de niveles: detecta duplicados antes de construir diccionarios.

    Código textual zfill(2), sin alterar ninguna fuente. No lee archivos.
    """
    result={}
    for row in rows:
        code=str(row['codigo_departamento']).zfill(2)
        year=row['anio']
        if code not in CODES or type(year) is not int or year not in YEARS:
            raise IntegrityError('Código/año no contractual')
        if code in result.setdefault(year,{}): raise IntegrityError('Llave duplicada')
        score=float(row['prom_punt_global'])
        if not isfinite(score): raise IntegrityError('Nivel no finito')
        result[year][code]=score
    return result

def candidate_index(candidate):
    if candidate not in CANDIDATES: raise IntegrityError('Candidato desconocido')
    return CANDIDATES.index(candidate)

def new_pipeline():
    return Pipeline([('scaler',StandardScaler(**SCALER)),('regressor',QuantileRegressor(**REGRESSOR))])

def window(external):
    if external not in YEARS[2:]: raise IntegrityError('Externa no contractual')
    if external==2021: return {'externo':2021,'entrenamiento':[],'procedimiento':'persistencia_fija','internas':[]}
    history=[y for y in YEARS[1:] if y<external]
    return {'externo':external,'entrenamiento':history,'procedimiento':'seleccion_interna',
            'internas':[{'validacion':v,'entrenamiento':[y for y in YEARS[1:] if y<v]} for v in YEARS[2:] if v<external]}

@dataclass
class Prepared:
    evaluated: int
    role: str
    previous_year: int
    previous_score: np.ndarray
    supervised_years: tuple
    history_years: tuple
    d: dict
    c: dict
    r: dict
    matrices: dict
    prediction_inputs: dict
    keys: dict

def prepare(levels, evaluated, role='interna'):
    """Materializa SOLO años anteriores antes de calcular cualquier estadística.

    levels es {anio:{codigo:puntaje}}; la función nunca lee valores evaluados
    o futuros. Ausencia/territorios incorrectos en historia detienen integridad.
    """
    if evaluated not in YEARS[2:] or role not in ('interna','externa'):
        raise IntegrityError('Fecha/rol no contractual; 2019 no es respuesta evaluable')
    history=tuple(y for y in YEARS if y<evaluated)
    scores={}
    for y in history:
        if y not in levels or set(levels[y])!=set(CODES) or len(levels[y])!=33:
            raise IntegrityError(f'Historia incompleta/33territorios incorrectos: {y}')
        a=np.asarray([levels[y][c] for c in CODES],dtype=float)
        if not np.isfinite(a).all(): raise IntegrityError('Historia no finita')
        scores[y]=a
    previous=max(history)
    d={y:scores[y]-scores[history[i-1]] for i,y in enumerate(history) if i>0}
    c={y:float(np.median(a)) for y,a in d.items()}
    r={y:a-c[y] for y,a in d.items()}
    paired=tuple(y for y in history[2:] if history[history.index(y)-1] in d)
    if role=='externa' and evaluated==2021: paired=()
    matrices={}; keys={}
    for component,values in (('memoria',d),('comun',c),('correccion',r)):
        xs=[]; ys=[]; ks=[]
        for y in paired:
            lag=history[history.index(y)-1]
            if not lag<y<evaluated: raise IntegrityError('Fecha no anterior')
            if component=='comun':
                xs.append([values[lag]]); ys.append(values[y]); ks.append((y,lag))
            else:
                xs.extend([[v] for v in values[lag]]); ys.extend(values[y]); ks.extend((code,y,lag) for code in CODES)
        matrices[component]=(np.asarray(xs,dtype=float).reshape(-1,1),np.asarray(ys,dtype=float))
        keys[component]=tuple(ks)
    inputs={'memoria':d[previous].reshape(-1,1).copy(),'comun':np.asarray([[c[previous]]]),'correccion':r[previous].reshape(-1,1).copy()}
    return Prepared(evaluated,role,previous,scores[previous].copy(),paired,history,d,c,r,matrices,inputs,keys)

def fit_predict(prepared, candidate, factory=new_pipeline):
    """Componentes separados; cada Pipeline completo cuenta un fit.

    Sin sample_weight, entradas identificadoras, postproceso ni reuso entre
    llamadas. Un fallo numérico invalida el candidato completo.
    """
    idx=candidate_index(candidate)
    if idx==0 or not prepared.supervised_years:
        delta=np.zeros(33)
        reason='persistencia' if idx==0 else ('externa2021_fija' if prepared.role=='externa' and prepared.evaluated==2021 else 'cero_pares')
        return {'candidate':candidate,'delta':delta,'score':prepared.previous_score+delta,'pipelines':{},'fits':0,'reason':reason}
    pipelines={}; delta=np.zeros(33)
    for component in COMPONENTS[idx]:
        X,y=prepared.matrices[component]
        pipeline=factory()
        if any(pipeline is old for old in pipelines.values()): raise IntegrityError('Pipeline compartido')
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error',ConvergenceWarning)
                pipeline.fit(X.copy(),y.copy())
                prediction=np.asarray(pipeline.predict(prepared.prediction_inputs[component].copy()),dtype=float)
            expected=1 if component=='comun' else 33
            if prediction.shape!=(expected,) or not np.isfinite(prediction).all():
                raise NumericalFailure('Predicción inválida')
        except (ValueError, ArithmeticError, ConvergenceWarning) as exc:
            raise NumericalFailure(str(exc)) from exc
        delta+=prediction[0] if component=='comun' else prediction
        pipelines[component]=pipeline
    return {'candidate':candidate,'delta':delta,'score':prepared.previous_score+delta,'pipelines':pipelines,'fits':len(pipelines),'reason':'ajuste'}

def metrics(observed,predicted):
    a=np.asarray(observed,dtype=float); b=np.asarray(predicted,dtype=float)
    if a.ndim!=1 or a.shape!=b.shape or not len(a) or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise IntegrityError('Métricas requieren cobertura finita')
    errors=(b-a).tolist()
    return {'MAE':fsum(abs(e) for e in errors)/len(errors),'RMSE':sqrt(fsum(e*e for e in errors)/len(errors)),'n':len(errors)}

def select_internal(external, records):
    """records: cuatro métricas agregadas SOLO de internas y cobertura íntegra."""
    if external==2021: raise IntegrityError('2021 externa no selecciona ni puntúa')
    expected_n=len(window(external)['internas'])*33
    if len(records)!=4 or {r['candidate'] for r in records}!=set(CANDIDATES):
        raise IntegrityError('Cuatro registros obligatorios, incluidos inelegibles')
    eligible=[]
    for rec in records:
        if rec.get('role')!='interna' or rec.get('external')!=external:
            raise IntegrityError('Selección solo interna/misma ventana')
        valid=(rec.get('eligible') is True and rec.get('n')==expected_n
               and all(isfinite(rec.get(k,float('nan'))) and rec[k]>=0 for k in ('MAE','RMSE')))
        if valid: eligible.append(rec)
        elif not rec.get('reason'): raise IntegrityError('Inelegibilidad debe tener razón')
    if not any(r['candidate']=='persistencia' for r in eligible): raise IntegrityError('Persistencia indispensable')
    m=min(r['MAE'] for r in eligible)
    pool1=[r for r in eligible if r['MAE']<=m+0.1]
    rmin=min(r['RMSE'] for r in pool1)
    pool2=[r for r in pool1 if r['RMSE']<=rmin+0.1]
    chosen=min(pool2,key=lambda r:(INPUTS[candidate_index(r['candidate'])],candidate_index(r['candidate'])))
    return {'candidate':chosen['candidate'],'pool_MAE':[r['candidate'] for r in pool1], 'pool_RMSE':[r['candidate'] for r in pool2]}

def exact_coverage(keys, expected):
    keys=list(keys); expected=list(expected)
    if len(keys)!=len(set(keys)) or len(expected)!=len(set(expected)) or set(keys)!=set(expected):
        raise IntegrityError('Cobertura/llaves incorrectas')
    return True

def expected_internal_keys():
    return [(e,v['validacion'],candidate,code) for e in YEARS[3:] for v in window(e)['internas'] for candidate in CANDIDATES for code in CODES]

def expected_external_keys():
    return [(e,policy,code) for e in YEARS[2:] for policy in CANDIDATES+('global',) for code in CODES]

def lineage(rows):
    """No descarta originales: contexto y copia exactos antes de deduplicar.

    Row: external,validation,candidate,code,observed,predicted,context. El
    contexto excluye externo pero incluye identidad de matrices/defaults/semilla.
    """
    keys=[(r['external'],r['validation'],r['candidate'],r['code']) for r in rows]
    exact_coverage(keys,expected_internal_keys())
    groups={}
    for row in rows:
        key=(row['validation'],row['candidate'],row['code'])
        groups.setdefault(key,[]).append(row)
    unique=[]; links=[]
    for key,copies in sorted(groups.items()):
        rep=min(copies,key=lambda r:r['external'])
        if not all(isfinite(r[k]) for r in copies for k in ('observed','predicted')):
            raise IntegrityError('Linaje no finito')
        for r in copies:
            if any(r[k]!=rep[k] for k in ('observed','predicted','context')):
                raise IntegrityError('Copias/contextos diferentes: no deduplicar')
            links.append({'external':r['external'],'key':key,'representative_external':rep['external']})
        unique.append(dict(rep))
    return unique,links

def reuse_global(result, source_candidate, source_external, target_candidate, target_external):
    if source_candidate!=target_candidate or source_external!=target_external or result['candidate']!=source_candidate:
        raise IntegrityError('Global solo reusa mismo candidato/ventana')
    return np.asarray(result['score']).copy()
