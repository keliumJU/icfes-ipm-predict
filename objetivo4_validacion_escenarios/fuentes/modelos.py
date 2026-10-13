"""Diseño focal predefinido; sin ajuste al importar. Transformaciones train-only."""
from pathlib import Path
import json,time,warnings,hashlib,sys,importlib.metadata as md
sys.dont_write_bytecode=True
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge,Lasso,ElasticNet
from sklearn.exceptions import ConvergenceWarning
from sklearn.neighbors import NearestNeighbors
import joblib
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parent;OUT=HERE/'resultados'
BASE=['tiempo','indicador2021','prop_oficial','prop_urbana','n_punt_global'];KEY=['codigo_departamento','anio'];SEED=20261012
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def panel():
    d=pd.read_csv(HERE/'preparacion/panel_enriquecido.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    assert len(d)==231 and not d.duplicated(KEY).any() and d.groupby('anio').size().eq(33).all()
    return d
def specs(d):
    # Orden de tasas proviene del contrato base; no selección por correlación.
    import importlib.util
    spec=importlib.util.spec_from_file_location('config_base_lectura',ROOT/'protocolo/fuentes/configuracion.py')
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    return {'base':BASE,'ipm':BASE+['ipm'],'componentes':BASE+sorted(c for c in d if c.startswith('contrib_'))+c.TASAS}
def candidates():
    rows=[]
    for fam,pars in [('Ridge',[{'alpha':a} for a in [.1,1,10,100,1000]]),('Lasso',[{'alpha':a} for a in [.01,.1,1,10]]),('ElasticNet',[{'alpha':a,'l1_ratio':r} for a in [.01,.1,1] for r in [.2,.8]])]:
        for p in pars:rows.append(dict(id=f'{fam}_{len(rows):02d}',family=fam,params=p,order=len(rows)))
    assert len(rows)==15
    return rows
def estimator(c):
    if c['family']=='Ridge':reg=Ridge(**c['params'],solver='svd')
    else:
        cls=Lasso if c['family']=='Lasso' else ElasticNet
        reg=cls(**c['params'],max_iter=100000,tol=1e-6,random_state=SEED,selection='cyclic')
    return make_pipeline(StandardScaler(),reg)
def metrics(y,p):
    y=np.asarray(y,float);p=np.asarray(p,float);assert y.shape==p.shape and len(y)>0 and np.isfinite(y).all() and np.isfinite(p).all()
    e=p-y;den=np.sum((y-y.mean())**2)
    return dict(n=len(y),MAE=float(np.mean(abs(e))),RMSE=float(np.sqrt(np.mean(e**2))),sesgo=float(np.mean(e)),R2=float(1-np.sum(e**2)/den) if den>0 else None)
def select(scores):
    minimum=min(r['MAE'] for r in scores);pool=[r for r in scores if r['MAE']<=minimum+.1]
    minimum=min(r['RMSE'] for r in pool);pool=[r for r in pool if r['RMSE']<=minimum+.1]
    return min(pool,key=lambda r:r['order'])['id']
def folds(years,method):
    return [(years[:i],year) for i,year in enumerate(years) if i] if method=='temporal' else [([y for y in years if y!=year],year) for year in years]
class Budget:
    def __init__(self):self.start=None;self.count=0
    def before(self):
        if self.start is None:self.start=time.monotonic()
        if time.monotonic()-self.start>3600 or self.count>=12000:raise TimeoutError('Límite nuevo de ajustes; cierre incompleto')
        self.count+=1
    def fit(self,c,tr,te,cols,target):
        self.before();m=estimator(c)
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always');m.fit(tr[cols],tr[target])
        if any(issubclass(w.category,ConvergenceWarning) for w in ws):raise RuntimeError('Convergencia fallida: '+c['id'])
        np.testing.assert_allclose(m[0].mean_,tr[cols].mean().to_numpy(),atol=1e-10)
        p=m.predict(te[cols]);assert np.isfinite(p).all()
        return m,p
def develop(d,years,method,target,budget,label):
    sp=specs(d);rows=[];winners={};models={};decisions=[]
    for name,cols in sp.items():
        scores=[]
        for c in candidates():
            predictions=[];observed=[]
            for ys,y in folds(years,method):
                tr=d[d.anio.isin(ys)];te=d[d.anio==y];assert len(tr)>0 and len(te)>0
                if method=='temporal':assert tr.anio.max()<y
                _,p=budget.fit(c,tr,te,cols,target);predictions.extend(p);observed.extend(te[target])
            scores.append(dict(spec=name,**c,**metrics(observed,predictions)))
        winner=select(scores);winners[name]=winner;rows.extend(scores)
        c=next(c for c in candidates() if c['id']==winner);train=d[d.anio.isin(years)]
        m,_=budget.fit(c,train,train,cols,target);models[name]=m
        decisions.append(dict(exercise=label,target=target,method=method,spec=name,winner=winner,years=years,cols=cols,params=m.get_params(deep=True).__repr__()))
    return winners,models,rows,decisions
def predictions(d,years,evalyears,target,models,label,method):
    rows=[];scores=[];te=d[d.anio.isin(evalyears)];sp=specs(d)
    for name,m in models.items():
        p=m.predict(te[sp[name]])
        q=te[KEY].copy();q['observed']=te[target].to_numpy();q['predicted']=p;q['spec']=name;q['exercise']=label;q['method']=method;q['target']=target;rows.append(q)
    train=d[d.anio.isin(years)]
    territorial=train.groupby('codigo_departamento')[target].mean()
    for name in ['promedio_territorial','persistencia']:
        vals=[]
        for r in te.itertuples():
            if name=='promedio_territorial':vals.append(territorial[r.codigo_departamento])
            else:
                prior=d[(d.codigo_departamento==r.codigo_departamento)&(d.anio<r.anio)].sort_values('anio').iloc[-1];vals.append(prior[target])
        q=te[KEY].copy();q['observed']=te[target].to_numpy();q['predicted']=vals;q['spec']=name;q['exercise']=label;q['method']=method;q['target']=target;rows.append(q)
    return pd.concat(rows,ignore_index=True)
def summarise(p):
    rows=[]
    for keys,q in p.groupby(['exercise','method','target','spec']):
        for y in [*sorted(q.anio.unique()),'conjunto']:
            v=q if y=='conjunto' else q[q.anio==y]
            rows.append(dict(zip(['exercise','method','target','spec'],keys),anio=str(y),**metrics(v.observed,v.predicted)))
    return pd.DataFrame(rows)
def scenarios(d,m):
    tr=d[d.anio<=2023];base=d[d.anio==2025].copy();cols=specs(d)['ipm'];supportcols=['prop_oficial','prop_urbana','n_punt_global','ipm']
    scaler=StandardScaler().fit(tr[supportcols]);z=scaler.transform(tr[supportcols]);nn=NearestNeighbors(n_neighbors=2).fit(z)
    threshold=float(np.quantile(nn.kneighbors(z)[0][:,1],.95));bounds={c:(float(tr[c].min()),float(tr[c].max())) for c in supportcols}
    med=float(base.ipm.median());rows=[];ranges=tr.groupby('codigo_departamento').ipm.agg(['min','max'])
    for r in base.itertuples():
        one=base[base.codigo_departamento==r.codigo_departamento].copy();basepred=float(m.predict(one[cols])[0])
        def admissible(q):
            reasons=[]
            for c in supportcols:
                val=float(q[c].iloc[0]);lo,hi=bounds[c]
                if not lo<=val<=hi:reasons.append('rango_global_'+c)
            val=float(q.ipm.iloc[0]);lo,hi=ranges.loc[r.codigo_departamento]
            if not 0<=val<=100:reasons.append('ipm_invalido')
            if not lo<=val<=hi:reasons.append('rango_ipm_territorio')
            distance=float(nn.kneighbors(scaler.transform(q[supportcols]),n_neighbors=1)[0][0,0])
            if distance>threshold:reasons.append('distancia_conjunta')
            return reasons,distance
        reasons0,dist0=admissible(one)
        for name,reduction in [('sin_cambio',0),('menos_1pp',1),('menos_3pp',3),('menos_5pp',5),('convergencia_mediana',max(0,r.ipm-med))]:
            q=one.copy();q['ipm']=r.ipm-reduction;reasons,dist=admissible(q);accepted=not reasons and not reasons0
            pred=float(m.predict(q[cols])[0]) if accepted else None
            rows.append(dict(codigo_departamento=r.codigo_departamento,departamento=r.departamento,anio=2025,escenario=name,ipm_base=r.ipm,ipm_escenario=r.ipm-reduction,reduccion_pp=reduction,admitido=accepted,motivos='|'.join(['base:'+v for v in reasons0]+reasons),distancia=dist,distancia_base=dist0,prediccion_base=basepred if not reasons0 else None,prediccion_escenario=pred,diferencia=pred-basepred if accepted else None))
    support=dict(cols=supportcols,bounds=bounds,nn_p95=threshold,mediana_33_no_ponderada=med,tiempo_fuera_soporte='2025 extrapola tendencia entrenada hasta 2023',criterio_fijado='PLAN_Y_PROTOCOLO.md',sin_intervalos_causales=True)
    return pd.DataFrame(rows),support
def bootstrap(pred):
    q=pred.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global"')
    a=q[q.spec=='ipm'];base=q[q.spec=='base'];z=a.merge(base,on=KEY,suffixes=('_ipm','_base'),validate='one_to_one')
    assert np.array_equal(z.observed_ipm,z.observed_base)
    diff=(abs(z.predicted_ipm-z.observed_ipm)-abs(z.predicted_base-z.observed_base)).groupby(z.codigo_departamento).mean().to_numpy()
    rng=np.random.default_rng(SEED);draw=diff[rng.integers(0,len(diff),(2000,len(diff)))].mean(axis=1)
    return dict(diferencia_mae_ipm_menos_base=float(diff.mean()),p025=float(np.quantile(draw,.025)),p975=float(np.quantile(draw,.975)),replicas=2000,alcance='dispersión condicional de errores fijos por territorio; no selección/ajuste/años futuros ni p-valor confirmatorio')
def run():
    assert not (OUT/'EJECUCION.json').exists(), 'Entrega ya ejecutada; reproducir en copia separada'
    OUT.mkdir(exist_ok=True);(OUT/'modelos').mkdir(exist_ok=True);d=panel();b=Budget();allpred=[];scores=[];decisions=[];mainmodel=None
    freeze={'protocol_sha':sha(HERE/'PLAN_Y_PROTOCOLO.md'),'preparation_sha':sha(HERE/'preparacion/panel_enriquecido.csv'),'candidates':candidates(),'specs':specs(d),'versions':{k:md.version(k) for k in ['numpy','pandas','scikit-learn']},'fuentes_sha':{p.name:sha(p) for p in (HERE/'fuentes').glob('*.py')},'semilla':SEED}
    (OUT/'CONGELACION_PREVIA.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
    try:
        for cut,ev in [(2023,[2024,2025]),(2022,[2023,2024])]:
            years=sorted(d[d.anio<=cut].anio.unique().tolist())
            for target in ['prom_punt_global','mat34']:
                for method in ['temporal','loyo']:
                    label=f'corte{cut}';w,m,s,de=develop(d,years,method,target,b,label);scores.extend([{**r,'exercise':label,'target':target,'method':method} for r in s]);decisions.extend(de)
                    # Guardar decisión/modelos antes de evaluar años externos.
                    (OUT/'DECISIONES.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
                    for name,model in m.items():joblib.dump(model,OUT/'modelos'/f'{label}_{target}_{method}_{name}.joblib')
                    allpred.append(predictions(d,years,ev,target,m,label,method))
                    if cut==2023 and target=='prom_punt_global' and method=='temporal':mainmodel=m['ipm']
                    print(label,target,method,w,'fits',b.count,flush=True)
        years=[2018,2019,2022,2023];label='sin2021';w,m,s,de=develop(d,years,'temporal','prom_punt_global',b,label);scores.extend([{**r,'exercise':label,'target':'prom_punt_global','method':'temporal'} for r in s]);decisions.extend(de)
        (OUT/'DECISIONES.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n');allpred.append(predictions(d,years,[2024,2025],'prom_punt_global',m,label,'temporal'))
        # Nested territorial selection: omitted territory excluded from selection and fit.
        years=[2018,2019,2021,2022,2023];dev=d[d.anio.isin(years)]
        territorial=[];territorial_decisions=[];territorial_scores=[]
        for code in sorted(d.codigo_departamento.unique()):
            train=dev[dev.codigo_departamento!=code];te=dev[dev.codigo_departamento==code]
            w,m,s,de=develop(train,years,'temporal','prom_punt_global',b,'territorial_'+code)
            territorial_decisions.extend([{**r,'omitido':code,'territorios_train':sorted(train.codigo_departamento.unique().tolist())} for r in de])
            territorial_scores.extend([{**r,'omitido':code} for r in s])
            (OUT/'DECISIONES_TERRITORIALES.json').write_text(json.dumps(territorial_decisions,ensure_ascii=False,indent=2)+'\n')
            for name,model in m.items():
                q=te[KEY].copy();q['observed']=te.prom_punt_global.to_numpy();q['predicted']=model.predict(te[specs(d)[name]]);q['spec']=name;q['exercise']='territorial_anidado';q['method']='temporal';q['target']='prom_punt_global';territorial.append(q)
            print('Territorio omitido',code,'fits',b.count,flush=True)
        allpred.append(pd.concat(territorial,ignore_index=True));pred=pd.concat(allpred,ignore_index=True)
        pred.to_csv(OUT/'predicciones.csv',index=False,float_format='%.17g');summarise(pred).to_csv(OUT/'metricas.csv',index=False,float_format='%.17g')
        pd.DataFrame(scores).to_csv(OUT/'seleccion_desarrollo.csv',index=False)
        pd.DataFrame(territorial_scores).to_csv(OUT/'seleccion_territorial.csv',index=False)
        sc,support=scenarios(d,mainmodel);sc.to_csv(OUT/'escenarios.csv',index=False,float_format='%.17g');(OUT/'SOPORTE.json').write_text(json.dumps(support,ensure_ascii=False,indent=2)+'\n')
        (OUT/'DISPERSION.json').write_text(json.dumps(bootstrap(pred),ensure_ascii=False,indent=2)+'\n')
        result=dict(completo=True,fits=b.count,seconds=time.monotonic()-b.start,escenarios_admitidos=int(sc.admitido.sum()),escenarios_rechazados=int((~sc.admitido).sum()),seleccion_sin_reserva=True,prueba_inedita=False)
        (OUT/'EJECUCION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result);return result
    except BaseException as e:
        (OUT/'INCIDENCIA.json').write_text(json.dumps(dict(error=str(e),fits=b.count,seconds=time.monotonic()-b.start if b.start else 0,completo=False),ensure_ascii=False,indent=2)+'\n');raise
if __name__=='__main__':run()
