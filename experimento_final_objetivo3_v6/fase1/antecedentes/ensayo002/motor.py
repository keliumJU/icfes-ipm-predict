"""Construcción temporal, estimadores nuevos y selección cerrada v6."""
from comun import *
import math, statistics, warnings
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import QuantileRegressor, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.exceptions import ConvergenceWarning
CLASSES={'StandardScaler':StandardScaler,'QuantileRegressor':QuantileRegressor,'Ridge':Ridge,'DecisionTreeRegressor':DecisionTreeRegressor}
def defaults():
    e=load(HERE/'ENTORNO_DOCUMENTAL.json')
    for n,cls in CLASSES.items(): check(cls().get_params()==e['defaults_sin_fit'][n],'defaults '+n)
    for cand in load(HERE/'ESPECIFICACION_V6.json')['candidates']:
        for n,p in cand['params'].items(): check(CLASSES[n](**p).get_params()==p,'parámetros completos '+cand['id'])
    return True
def panel():
    spec=load(HERE/'ESPECIFICACION_V6.json'); paths=list(spec['fuentes'])
    a=pd.read_csv(ROOT/paths[0],dtype={'codigo_departamento':str},float_precision='round_trip')
    b=pd.read_csv(ROOT/paths[1],dtype={'codigo_departamento':str},float_precision='round_trip')
    keys=['codigo_departamento','anio'];a=a.sort_values(keys).reset_index(drop=True);b=b.sort_values(keys).reset_index(drop=True)
    check(a[keys].equals(b[keys]),'llaves fuente/derivado')
    check(np.array_equal(a.prom_punt_global.to_numpy(),b.prom_punt_global.to_numpy()),'niveles fuente/derivado exactos')
    codes=sorted(a.codigo_departamento.unique()); years=spec['years']
    check(len(codes)==33 and len(a)==231 and not a.duplicated(keys).any() and sorted(a.anio.unique())==years,'panel completo')
    levels={int(y):a[a.anio==y].sort_values(keys).prom_punt_global.to_numpy() for y in years}
    check(all(len(v)==33 and np.isfinite(v).all() for v in levels.values()),'cobertura niveles')
    p=build_panel(levels,codes)
    for y in years[1:]:
        rows=b[b.anio==y].sort_values(keys)
        check(np.array_equal(rows.cambio_observado.to_numpy(),p['d'][y]),'d derivado exacto')
        check(np.array_equal(rows.puntaje_previo.to_numpy(),levels[p['previous'][y]]),'previo derivado exacto')
        check((rows.anio_previo==p['previous'][y]).all(),'fecha previa derivado')
    return p
def build_panel(levels,codes):
    years=sorted(levels);check(2020 not in years and len(codes)==33,'años/códigos')
    for v in levels.values():check(len(v)==33 and np.isfinite(v).all(),'integridad panel')
    previous={y:years[i-1] for i,y in enumerate(years) if i}
    d={y:np.asarray(levels[y])-np.asarray(levels[q]) for y,q in previous.items()}
    c={y:statistics.median(v.tolist()) for y,v in d.items()}
    r={y:v-c[y] for y,v in d.items()}
    return dict(levels=levels,codes=codes,years=years,previous=previous,d=d,c=c,r=r)
def context(p,cand,year):
    check(year in p['previous'],'año evaluable')
    ys=[y for y in p['years'] if 2021<=y<year and y in p['d'] and p['previous'][y] in p['d']]
    if cand['history']!='all': ys=ys[-int(cand['history'][4:]):]
    q=p['previous'][year];ctx=dict(id=cand['id'],year=year,history=cand['history'],eligible_years=ys,previous=q,inputs=cand['inputs'],units='puntos globales; cambio sin anualizar',seed=SEED,params=cand['params'],components={},prior_levels={str(y):p['levels'][y].tolist() for y in p['years'] if y<year},prior_d={str(y):p['d'][y].tolist() for y in p['d'] if y<year},prior_c={str(y):p['c'][y] for y in p['c'] if y<year},prior_r={str(y):p['r'][y].tolist() for y in p['r'] if y<year},prediction_keys=[[j,year] for j in p['codes']],previous_score=p['levels'][q].tolist())
    for comp in cand['components']:
        common=comp=='comun';field={'memoria':'d','comun':'c','correccion':'r'}[comp]
        arr=lambda y:np.atleast_1d(p[field][y])
        X=np.concatenate([arr(p['previous'][y]) for y in ys]) if ys else np.array([])
        Y=np.concatenate([arr(y) for y in ys]) if ys else np.array([])
        keys=[[('comun' if common else j),y] for y in ys for j in (['comun'] if common else p['codes'])]
        ctx['components'][comp]=dict(X=X.reshape(-1,1).tolist(),y=Y.tolist(),keys=keys,previous_years=[p['previous'][y] for y in ys],predict_X=arr(q).reshape(-1,1).tolist())
    if cand['family'] in ['nivel_territorial','nivel_comun']:
        field='d' if cand['family']=='nivel_territorial' else 'c'
        ctx['statistic_values']=[float(v) for y in ys for v in np.atleast_1d(p[field][y])]
        ctx['statistic']=cand['statistic']
    return ctx
def pipeline(cand):
    n=next(n for n in cand['params'] if n!='StandardScaler')
    return Pipeline([('scaler',StandardScaler(**cand['params']['StandardScaler'])),('regressor',CLASSES[n](**cand['params'][n]))])
def estimate(cand,ctx,progress=None):
    parts={};metadata={};count=0;stats=0
    if cand['family']=='persistencia' or not ctx['eligible_years']:
        delta=np.zeros(33);state='persistencia' if cand['family']=='persistencia' else 'respaldo_cero'
    elif cand['family'] in ['nivel_territorial','nivel_comun']:
        values=ctx['statistic_values'];v=statistics.median(values) if cand['statistic']=='median' else math.fsum(values)/len(values)
        delta=np.full(33,v);stats=1;state='estimacion_constante';metadata['statistic_value']=v
        if progress:progress(dict(statistical_estimates=1,component=None,state='constante'))
    else:
        state='ajustado'
        for comp,data in ctx['components'].items():
            if progress:progress(dict(component=comp,state='antes_fit',fits_started=1))
            model=pipeline(cand);X=np.asarray(data['X']);Y=np.asarray(data['y']);XP=np.asarray(data['predict_X'])
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter('always');model.fit(X,Y)
            check(not any(issubclass(w.category,ConvergenceWarning) for w in ws),'convergencia inelegible sinretry')
            out=model.predict(XP);check(np.isfinite(out).all(),'numérico inelegible sinretry')
            scaler=model.named_steps['scaler'];reg=model.named_steps['regressor']
            m=dict(scaler_mean=scaler.mean_.tolist(),scaler_var=scaler.var_.tolist(),scaler_scale=scaler.scale_.tolist(),n_samples=int(scaler.n_samples_seen_),warnings=[dict(category=w.category.__name__,message=str(w.message)) for w in ws],regressor=type(reg).__name__,predicted_component=out.tolist())
            if hasattr(reg,'coef_'):m.update(coef=np.atleast_1d(reg.coef_).tolist(),intercept=float(reg.intercept_))
            else:
                t=reg.tree_;m['tree']={n:getattr(t,n).tolist() for n in ['children_left','children_right','feature','threshold','value']}
            metadata[comp]=m;parts[comp]=out;count+=1
            if progress:progress(dict(component=comp,state='fit_terminado',fits_completed=1))
        delta=parts.get('memoria',np.full(33,float(parts['comun'][0])) if 'comun' in parts else np.zeros(33))
        if 'correccion' in parts:delta=delta+parts['correccion']
    score=np.asarray(ctx['previous_score'])+delta
    check(np.isfinite(score).all(),'reconstrucción finita')
    return dict(context=ctx,metadata=metadata,predicted_delta=delta.tolist(),prediction=score.tolist(),state=state,fits=count,statistical_estimates=stats)
def metrics(pred,obs):
    e=[float(a)-float(b) for a,b in zip(pred,obs)]
    check(len(e)>0 and all(math.isfinite(v) for v in e),'métricas finitas')
    return dict(MAE=math.fsum(map(abs,e))/len(e),RMSE=math.sqrt(math.fsum(v*v for v in e)/len(e)),bias=math.fsum(e)/len(e),n=len(e))
def select(records):
    m=min(x['MAE'] for x in records);pool=[x for x in records if x['MAE']<=m+0.1]
    r=min(x['RMSE'] for x in pool);pool2=[x for x in pool if x['RMSE']<=r+0.1]
    winner=min(pool2,key=lambda x:(x['inputs'],x['order']))['id']
    return dict(winner=winner,mae_min=m,rmse_pool_min=r,pool_mae=[x['id'] for x in pool],pool_rmse=[x['id'] for x in pool2],records=records)
def exact_csv(a,b,keys):
    a=a.sort_values(keys).reset_index(drop=True);b=b.sort_values(keys).reset_index(drop=True)
    check(list(a.columns)==list(b.columns) and a.shape==b.shape,'CSV forma')
    for c in a:
        check(np.array_equal(a[c].to_numpy(),b[c].to_numpy()),'CSV exacto '+c)
    return True
