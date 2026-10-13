"""Implementación temporal propia. Lectura real solo para integridad; fits inventados."""
import sys
import os
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import math
import copy
import warnings
import numpy as np
import pandas as pd
import sklearn
from sklearn import config_context
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import QuantileRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.exceptions import ConvergenceWarning
from seguridad import ROOT, E1, OUT, TEST, sha, leer

SEED = 20261010
KEYS = ['codigo_departamento','anio']
YEARS = [2018,2019,2021,2022,2023,2024,2025]
SPEC_PATH = ROOT/'diseno_temporal_objetivo3_v1/ESPECIFICACION_PROPUESTA.json'
CONFIG_PATH = ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json'
SPEC = leer(SPEC_PATH)
CONF = leer(CONFIG_PATH)
CS = copy.deepcopy(CONF['configuraciones'])
GROUPS = copy.deepcopy(CONF['grupos'])
INPUTS = list(dict.fromkeys(x for cols in GROUPS.values() for x in cols))
ROLES = ['global', *GROUPS, 'persistencia']


def serial(value):
    if isinstance(value, dict):
        return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [serial(v) for v in value]
    if isinstance(value,np.ndarray):
        return value.tolist()
    if isinstance(value,np.generic):
        return value.item()
    if value is None or isinstance(value,(str,int,float,bool)):
        return value
    return repr(value)


def candidate(c):
    if c not in CS:
        raise ValueError('Candidato distinto al congelado')
    return c


def construir(c):
    candidate(c)
    if c['familia'] == 'mediana':
        return Pipeline([('escalado',StandardScaler()),('modelo',QuantileRegressor(**c['parametros']))])
    if c['familia'] == 'boosting_absoluto':
        return GradientBoostingRegressor(**c['parametros'])
    raise ValueError('Persistencia sin estimador/fit')


def comprobar_defaults():
    assert len(CS) == 36 and len({c['id'] for c in CS}) == 36
    assert SPEC['heredado']['candidatos'] == CS and SPEC['heredado']['grupos'] == GROUPS
    assert SPEC['heredado']['ventanas'] == CONF['ventanas']
    assert len(INPUTS) == 18
    for c in CS[1:]:
        assert c['entradas'] == GROUPS[c['especificacion']]
        if serial(construir(c).get_params(deep=True)) != c['parametros_completos']:
            raise ValueError('Defaults incompatibles: ' + c['id'])
    return True


def csv(path):
    return pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip')


def exact(a,b):
    if a.columns.tolist() != b.columns.tolist() or a.shape != b.shape or not a.index.equals(b.index):
        raise ValueError('Campos/orden/índice/cobertura')
    for col in a:
        ma,mb = a[col].isna(),b[col].isna()
        if not np.array_equal(ma,mb):
            raise ValueError('Ausencias diferentes')
        if not np.array_equal(a.loc[~ma,col].to_numpy(),b.loc[~mb,col].to_numpy()):
            raise ValueError('CSV distinto: igualdad exacta, sin tolerancia')


def validate(frame,keys=KEYS,expected=None,finite=()):
    if frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise ValueError('Llaves ausentes/duplicadas')
    if expected is not None:
        exact(frame[keys].reset_index(drop=True),expected.reset_index(drop=True))
    if finite and not np.isfinite(frame[list(finite)].to_numpy(float)).all():
        raise ValueError('Valores no finitos')


def historial(source,cov):
    p = source.sort_values(KEYS).reset_index(drop=True).copy()
    validate(p)
    g = p.groupby('codigo_departamento',sort=False)
    p['anio_previo'] = g.anio.shift(1).astype('Int64')
    p['puntaje_previo'] = g.prom_punt_global.shift(1)
    p['cambio_observado'] = p.prom_punt_global-p.puntaje_previo
    for col in cov:
        p['previo_'+col] = g[col].shift(1)
        p['cambio_'+col] = p[col]-p['previo_'+col]
    p['intervalo'] = p.anio-p.anio_previo
    return p


def reconstruir():
    inherited = SPEC['heredado']
    source_path,panel_path = (ROOT/inherited[k] for k in ('fuente_archivo','derivado_archivo'))
    assert sha(source_path) == inherited['fuente_sha256']
    assert sha(panel_path) == inherited['derivado_sha256']
    s = csv(source_path)
    s.codigo_departamento = s.codigo_departamento.str.zfill(2)
    cov = [x.removeprefix('cambio_') for x in GROUPS['cambio_ambas'][1:]]
    p = historial(s,cov)
    p['fuente_sha256'] = inherited['fuente_sha256']
    exact(p,csv(panel_path))
    exact(p[s.columns],s.sort_values(KEYS).reset_index(drop=True))
    q = p[p.anio > 2018].copy()
    assert set(s.anio) == set(YEARS) and len(p) == 231 and len(q) == 198
    assert p.codigo_departamento.nunique() == 33
    assert q.groupby('anio').size().to_dict() == {a:33 for a in YEARS[1:]}
    assert q[q.anio == 2021].anio_previo.eq(2019).all()
    assert set(q.intervalo) == {1,2}
    validate(q,finite=['cambio_observado',*INPUTS])
    return p,q


def pesos(train_keys, esquema='recencia_h2'):
    """No recibe validación, externo, X ni y. Semivida única fija de 2 años."""
    if train_keys.columns.tolist() != KEYS:
        raise ValueError('Solo llaves train en orden autorizado')
    validate(train_keys,finite=['anio'])
    exact(train_keys.reset_index(drop=True),train_keys.sort_values(KEYS).reset_index(drop=True))
    years = train_keys.anio.to_numpy(float)
    if not len(years) or not np.equal(years,np.floor(years)).all():
        raise ValueError('Train vacío/años no enteros')
    if esquema not in ('recencia_h2','uniforme'):
        raise ValueError('Esquema ajeno; sin búsqueda')
    anchor = int(max(years))
    raw = [1. if esquema == 'uniforme' else 2.**(-(anchor-int(a))/2.) for a in years]
    total = math.fsum(raw)
    if len(set(raw)) == 1:
        w = np.ones(len(raw))
    else:
        w = np.array([len(raw)*v/total for v in raw])
    if not np.isfinite(w).all() or not (w>0).all() or not math.isclose(math.fsum(w),len(w),abs_tol=1e-12,rel_tol=0):
        raise ValueError('Pesos inválidos; no truncar')
    return w,dict(esquema=esquema,semivida=2.,ancla_train=anchor,n=len(w),
                  anios_train=sorted(set(map(int,years))),llaves=train_keys.values.tolist(),
                  pesos_brutos=raw,suma_brutos=total,pesos=w.tolist(),suma_pesos=math.fsum(w),
                  normalizacion='n*wbruto/fsum(wbruto); media1',uniforme=bool(np.array_equal(w,np.ones(len(w)))))


def matrices(train,c):
    candidate(c)
    if c['familia'] == 'persistencia' or c['entradas'] != GROUPS[c['especificacion']]:
        raise ValueError('Entradas o familia no ajustable')
    if not set(train.anio) <= set(YEARS[1:]):
        raise ValueError('Años ajenos')
    validate(train,finite=[*c['entradas'],'cambio_observado'])
    if not len(train):
        raise ValueError('Train vacío')
    exact(train[KEYS].reset_index(drop=True),train[KEYS].sort_values(KEYS).reset_index(drop=True))
    return train[c['entradas']].to_numpy(float),train.cambio_observado.to_numpy(float)


def fit_kwargs(c,w):
    candidate(c)
    if c['familia'] == 'persistencia':
        raise ValueError('Persistencia sin fit')
    w = np.asarray(w,float)
    if w.ndim != 1 or not len(w) or not np.isfinite(w).all() or not (w>0).all():
        raise ValueError('Peso inválido')
    if np.array_equal(w,np.ones(len(w))):
        return {}
    return ({'escalado__sample_weight':w,'modelo__sample_weight':w}
            if c['familia'] == 'mediana' else {'sample_weight':w})


def ajustar_inventado(c,train,contexto,constructor=construir):
    if contexto.get('origen') != 'inventado' or train.attrs.get('origen') != 'inventado':
        raise ValueError('Etapa1 permite exclusivamente ajustes inventados')
    X,y = matrices(train,c)
    w,meta = pesos(train[KEYS])
    kwargs = fit_kwargs(c,w)
    estimator = constructor(c)
    np.random.seed(SEED)
    with config_context(enable_metadata_routing=False), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        estimator.fit(X,y,**kwargs)
    notes = [dict(categoria=n.category.__name__,mensaje=str(n.message)) for n in caught]
    if any(issubclass(n.category,(ConvergenceWarning,RuntimeWarning)) for n in caught):
        raise ValueError('Numérico/convergencia; candidato inelegible: '+str(notes))
    transforms = {}
    if c['familia'] == 'mediana' and hasattr(estimator,'named_steps'):
        scaler = estimator.named_steps['escalado']
        transforms = dict(media=serial(scaler.mean_),varianza=serial(scaler.var_),
                          escala=serial(scaler.scale_),suma_pesos=serial(scaler.n_samples_seen_))
        mean = np.array([math.fsum(float(wi)*float(xi) for wi,xi in zip(w,X[:,j]))/math.fsum(w) for j in range(X.shape[1])])
        var = np.array([math.fsum(float(wi)*(float(xi)-float(mean[j]))**2 for wi,xi in zip(w,X[:,j]))/math.fsum(w) for j in range(X.shape[1])])
        np.testing.assert_allclose(scaler.mean_,mean,atol=1e-12,rtol=0)
        np.testing.assert_allclose(scaler.var_,var,atol=1e-12,rtol=0)
    return estimator,dict(origen='inventado',contexto=contexto,pesos=meta,id=c['id'],
            entradas=c['entradas'],parametros=c['parametros_completos'],transformaciones=transforms,
            routing=False,ruta_fit=list(kwargs),semilla=SEED,sklearn=sklearn.__version__,
            python=__import__('platform').python_version(),advertencias=notes)


def metricas(y,pred):
    y,pred = np.asarray(y,float),np.asarray(pred,float)
    if y.ndim != 1 or y.shape != pred.shape or not len(y) or not np.isfinite(y).all() or not np.isfinite(pred).all():
        raise ValueError('Métricas sin cobertura/finito')
    e = pred-y
    return dict(n=len(e),mae=math.fsum(abs(float(x)) for x in e)/len(e),
                rmse=math.sqrt(math.fsum(float(x)**2 for x in e)/len(e)),sesgo=math.fsum(e)/len(e))


def seleccionar(rows,expected,externo):
    if externo == 2021:
        if rows or expected:
            raise ValueError('2021 fijo sin selección interna')
        return dict(global_id='persistencia',especificaciones={g:'persistencia' for g in GROUPS},candidatos=[])
    windows = next((w for w in CONF['ventanas'] if w['externo'] == externo),None)
    if windows is None or expected != [i['validacion'] for i in windows['internas']]:
        raise ValueError('Internas ajenas')
    if [r['id'] for r in rows] != [c['id'] for c in CS]:
        raise ValueError('36 IDs en orden obligatorio')
    eligible = []
    for r,c in zip(rows,CS):
        if set(r) != {'id','estado','ventanas','mae','rmse','razon'}:
            raise ValueError('Solo métricas internas/razón')
        ok = r['estado'] == 'completo' and r['ventanas'] == expected and all(
            isinstance(r[k],(int,float)) and math.isfinite(r[k]) and r[k]>=0 for k in ('mae','rmse'))
        if not ok and not r['razon']:
            raise ValueError('Inelegible sin razón')
        if ok:
            eligible.append({**r,**{k:c[k] for k in ('familia','especificacion','n_ajustadas','orden')}})
    if not eligible or eligible[0]['id'] != 'persistencia':
        raise ValueError('Persistencia indispensable')
    def winner(pool):
        minimum = min(r['mae'] for r in pool)
        pool = [r for r in pool if r['mae'] <= minimum+.1]
        minimum = min(r['rmse'] for r in pool)
        pool = [r for r in pool if r['rmse'] <= minimum+.1]
        return min(pool,key=lambda r:(r['n_ajustadas'],CONF['orden_familias'].index(r['familia']),r['orden']))['id']
    return dict(global_id=winner(eligible),especificaciones={g:winner([r for r in eligible if r['especificacion'] in (None,g)]) for g in GROUPS},candidatos=rows)


def ids_externos(decision):
    order = {c['id']:c['orden'] for c in CS}
    if set(decision['especificaciones']) != set(GROUPS):
        raise ValueError('Grupos incompletos')
    return sorted({decision['global_id'],*decision['especificaciones'].values()},key=order.__getitem__)


def cobertura(frame,codes):
    codes = set(codes)
    if len(codes) != 33 or len(frame) != 1155 or set(frame.procedimiento) != set(ROLES):
        raise ValueError('Cobertura incompleta')
    expected = {(c,y) for c in codes for y in range(2021,2026)}
    common = None
    for role in ROLES:
        q = frame[frame.procedimiento == role].sort_values(KEYS).reset_index(drop=True)
        validate(q,finite=['observado','prediccion'])
        if len(q) != 165 or set(map(tuple,q[KEYS].values)) != expected:
            raise ValueError('Llaves incompletas')
        if common is None:
            common = q[KEYS+['observado']]
        exact(common,q[KEYS+['observado']])
    return True


def colapsar(frame,firmas):
    key = ['id',*KEYS]
    validate(frame,['externo',*key],finite=['observado','prediccion','cambio_predicho'])
    fields = ['observado','puntaje_previo','anio_previo','prediccion','cambio_predicho','error','origen']
    if (frame.groupby(key,sort=False)[fields].nunique(dropna=False)>1).any().any():
        raise ValueError('Copias discrepantes: no promediar')
    for (ident,year),part in frame.groupby(['id','anio'],sort=False):
        signatures = [firmas[(int(ext),ident,int(year))] for ext in part.externo.unique()]
        if any(s != signatures[0] for s in signatures):
            raise ValueError('Linaje discrepante')
    unique = frame.sort_values(['externo',*key]).drop_duplicates(key,keep='first').reset_index(drop=True)
    representative = unique.set_index(key).externo
    lineage = frame[['externo',*key,'ajuste']].copy()
    lineage['externo_representante'] = [int(representative.loc[tuple(r)]) for r in lineage[key].itertuples(index=False,name=None)]
    return unique,lineage


def referencias(panel):
    fields = KEYS+['observado','prediccion']
    v5path = ROOT/'experimentos_objetivo3_v5/etapa2/resultados/predicciones_externas.csv'
    v3path = ROOT/'experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv'
    v5,v3 = csv(v5path),csv(v3path)
    a = v5[v5.procedimiento == 'global'].sort_values(KEYS).reset_index(drop=True)
    b = v3[v3.procedimiento == 'procedimiento_v3'].sort_values(KEYS).reset_index(drop=True)
    p = panel[panel.anio.between(2021,2025)].sort_values(KEYS).reset_index(drop=True)
    independent = p[KEYS].copy()
    independent['observado'] = p.prom_punt_global
    independent['prediccion'] = p.puntaje_previo
    assert len(a) == len(b) == len(independent) == 165
    validate(a,finite=['observado','prediccion'])
    validate(b,finite=['observado','prediccion'])
    exact(a[fields],b[fields])
    exact(a[fields],independent)
    assert a.id.eq('persistencia').all() and b.id.eq('persistencia').all()
    return dict(aprobado=True,pares=165,iguales_exactamente=True,independencia_del_nuevo_fit=True,
                evidencias_independientes_entre_si=False,archivos={str(p.relative_to(ROOT)):sha(p) for p in (v5path,v3path)},
                procedimiento='Lectura round_trip; llaves/campos/orden/observados/predicción exactos vs previo reconstruido; sin MAE nuevo')
