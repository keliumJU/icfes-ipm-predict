"""Diseño cerrado, construcción de matrices y selector operativo."""
from infra import *
import math, numpy as np, pandas as pd
YEARS=[2018,2019,2021,2022,2023,2024,2025]
H=['puntaje_previo','cambio_previo']
def metrics(y,p):
    e=[float(a)-float(b) for a,b in zip(p,y)];n=len(e);check(n>0,'métrica vacía')
    return dict(n=n,MAE=math.fsum(abs(x) for x in e)/n,RMSE=math.sqrt(math.fsum(x*x for x in e)/n),sesgo=math.fsum(e)/n)
def select(scores,candidates,eligible):
    pool=[{**scores[c['id']],**c} for c in candidates if c['id'] in eligible]
    m=min(c['MAE'] for c in pool);pool=[c for c in pool if c['MAE']<=m+0.1]
    r=min(c['RMSE'] for c in pool);pool=[c for c in pool if c['RMSE']<=r+0.1]
    return min(pool,key=lambda c:(len(c['inputs']),c['order']))['id']
def build(base,tasas):
    b=base.sort_values(['codigo_departamento','anio']).copy()
    g=b.groupby('codigo_departamento',sort=False)
    b['anio_previo']=g.anio.shift(1);b['puntaje_previo']=g.prom_punt_global.shift(1)
    b['anio_previo_previo']=g.anio.shift(2);b['puntaje_previo_previo']=g.prom_punt_global.shift(2)
    b['cambio_previo']=b.puntaje_previo-b.puntaje_previo_previo
    b['cambio_observado']=b.prom_punt_global-b.puntaje_previo
    return b
def validate_sources():
    from preflight import BASE,DERIVED,SOURCES,tasas
    t,dims=tasas()
    for name,h in SOURCES.items():check(sha(ROOT/name)==h,'source hash')
    base=pd.read_csv(ROOT/BASE,float_precision='round_trip',dtype={'codigo_departamento':str})
    derived=pd.read_csv(ROOT/DERIVED,float_precision='round_trip',dtype={'codigo_departamento':str})
    coding=[]
    for name,df in [('principal',base),('derivada',derived)]:
        check(df.codigo_departamento.str.fullmatch(r'\d{1,2}').all(),'formato código')
        for row in df[['codigo_departamento','anio','departamento']].to_dict('records'):
            coding.append(dict(fuente=name,**row,codigo_canonico=row['codigo_departamento'].zfill(2)))
        df['codigo_departamento']=df.codigo_departamento.str.zfill(2)
    check(base.groupby('codigo_departamento').departamento.nunique().max()==1,'nombre estable por código')
    csv_save(HERE/'preflight/NORMALIZACION_CODIGOS.csv',pd.DataFrame(coding))
    save(HERE/'preflight/HALLAZGO_CODIGOS.json',dict(hallazgo='05/08 históricos frente a5/8 en2025;33 cada año,35 strings literales',impacto='llaves literales impiden unir historia; no diferencia de territorios',alternativa='zfill(2) en principal y derivada, solo en memoria y nuevas matrices; verificar nombres y unicidad',resolucion='normalización de representación sin alterar población/criterios/bytes originales, antes de resultados',fits_al_detectar=0))
    check(len(base)==231 and sorted(base.anio.unique())==YEARS,'231 siete años')
    check(not base.duplicated(['codigo_departamento','anio']).any(),'llaves únicas')
    codes=sorted(base.codigo_departamento.unique());check(len(codes)==33 and all(base[base.anio==y].codigo_departamento.sort_values().tolist()==codes for y in YEARS),'33 por año')
    check(np.isfinite(base.select_dtypes(include='number').to_numpy()).all(),'finitos fuente')
    check(((base[['ipm',*t]]>=0)&(base[['ipm',*t]]<=100)).all().all(),'porcentajes')
    check(base.prom_punt_global.between(0,500).all(),'puntaje rango')
    b=build(base,t);k=['codigo_departamento','anio']
    a=b.set_index(k).sort_index();z=derived.set_index(k).sort_index();check(a.index.equals(z.index),'cotejo llaves')
    for col in base.columns:
        if col in k:continue
        if pd.api.types.is_numeric_dtype(a[col]):check(np.array_equal(a[col].values,z[col].values,equal_nan=True),'cotejo '+col)
        else:check(a[col].equals(z[col]),'cotejo texto')
    for col in ['anio_previo','puntaje_previo','cambio_observado']:check(np.array_equal(a[col].values,z[col].values,equal_nan=True),'historia '+col)
    for col in ['ipm',*t]:
        prev=b.groupby('codigo_departamento')[col].shift(1);ch=b[col]-prev
        zi=z.reindex(b.set_index(k).index)
        check(np.array_equal(prev.values,zi['previo_'+col].values,equal_nan=True),'pobreza anterior '+col)
        check(np.array_equal(ch.values,zi['cambio_'+col].values,equal_nan=True),'cambio '+col)
    panel=b[b.anio>=2021][k+['departamento','prom_punt_global','anio_previo','anio_previo_previo','puntaje_previo_previo',*H,'cambio_observado','ipm',*t]].sort_values(['anio','codigo_departamento']).reset_index(drop=True)
    check(len(panel)==165 and np.isfinite(panel.select_dtypes(include='number').values).all(),'165 panel finito')
    check((panel[panel.anio==2021].anio_previo==2019).all() and (panel[panel.anio==2021].anio_previo_previo==2018).all(),'salto')
    csv_save(HERE/'preflight/PANEL.csv',panel)
    save(HERE/'preflight/POBLACION.json',dict(aprobado=True,filas_fuente=len(base),territorios=codes,anios=YEARS,pares_externos=len(panel),tasas=t,dimensiones=dims,lectura='round_trip, códigos string',igual_peso=True,conteos_predictores=False,geografia='colegio',respuesta='prom_punt_global recibido',ipm_unidad='% personas',tasas_unidad='% hogares',historia_sin_anualizar=True,cotejo_exacto=True))
    return panel,t
def params():
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import Ridge
    from sklearn.tree import DecisionTreeRegressor
    return dict(scaler=StandardScaler(copy=True,with_mean=True,with_std=True).get_params(),ridge=Ridge(solver='svd',fit_intercept=True,copy_X=True,positive=False,max_iter=None,tol=.0001,random_state=SEED).get_params(),tree=DecisionTreeRegressor(criterion='absolute_error',max_depth=2,min_samples_leaf=11,random_state=SEED).get_params())
def specification(t):
    p=params();groups={'H':H,'I':['ipm'],'D':t,'HI':H+['ipm'],'HD':H+t}
    cs=[dict(id='persistencia',order=0,group='persistencia',family='persistencia',inputs=[],params={},scaler=None)]
    for group in groups:
        for alpha in [.1,1.,10.]:cs.append(dict(id=f'Ridge_{group}_{alpha:g}',order=len(cs),group=group,family='Ridge',inputs=groups[group],params={**p['ridge'],'alpha':alpha},scaler=p['scaler']))
    for group in groups:cs.append(dict(id='Arbol_'+group,order=len(cs),group=group,family='Arbol',inputs=groups[group],params=p['tree'],scaler=p['scaler']))
    sets={'historico':[c['id'] for c in cs if c['family']=='persistencia' or c['family']=='Ridge' and c['group']=='H'], 'ampliado':[c['id'] for c in cs if c['family']=='persistencia' or c['family']=='Ridge' and c['group'] in ['H','HI','HD']], 'con_pobreza':[c['id'] for c in cs if c['family']=='Ridge' and c['group'] in ['HI','HD']]}
    spec=dict(candidates=cs,groups=groups,policies=sets,defaults=p,seed=SEED,response='prom_punt_global',external_years=list(range(2021,2026)),train_rule='2021 <= anio < evaluado',inner_rule='2021..externo-1 acumuladas;2021 persistencia',selector=dict(mae_tolerance=.1,rmse_tolerance=.1,complexity='numero entradas',tie='order'),primary='100*(MAE_historico-MAE_ampliado)/MAE_historico',threshold_percent=5,original_fits=200,max_repetitions=12,max_fits_without_failures=212,repeat_atol=1e-10,repeat_rtol=0,units={'H':'puntos global Saber 11','I':'porcentaje de personas','D':'porcentaje de hogares'},source_hashes=load(HERE/'preflight/FUENTES.json'),availability='pobreza contemporánea condicionante; no disponibilidad anticipada demostrada')
    spec['pipeline_defaults']={'memory':None,'verbose':False,'transform_input':None}
    spec['documentary_constants']={'alpha':[.1,1,10],'max_depth':2,'min_samples_leaf':11,'indicadores':15,'tolerancias':.1,'anios_historia':[2018,2019],'anios_eval':[2021,2022,2023,2024,2025],'pares_por_territorio':5,'primer_externo':2021,'exclusion':2020,'universo_anios':YEARS}
    save(HERE/'ESPECIFICACION.json',spec)
    csv_save(HERE/'CANDIDATOS.csv',pd.DataFrame([dict(id=c['id'],orden=c['order'],grupo=c['group'],familia=c['family'],n_inputs=len(c['inputs']),inputs=json.dumps(c['inputs'],ensure_ascii=False),parametros=json.dumps(c['params'],sort_keys=True),scaler=json.dumps(c['scaler'],sort_keys=True)) for c in cs]))
    return spec
def contexts(panel,c,evaluated):
    train=panel[(panel.anio>=2021)&(panel.anio<evaluated)].copy();test=panel[panel.anio==evaluated].copy()
    check(len(test)==33 and (train.anio<evaluated).all() and not (train.anio<2021).any(),'temporalidad contexto')
    def pack(d):return dict(keys=d[['codigo_departamento','anio']].to_dict('records'),years=d.anio.tolist(),X=d[c['inputs']].to_numpy().tolist(),y=d.prom_punt_global.tolist(),history=d[['anio_previo','anio_previo_previo','puntaje_previo','puntaje_previo_previo','cambio_previo']].to_dict('records'),inputs=c['inputs'],units=load(HERE/'ESPECIFICACION.json')['units'],persistence=d.puntaje_previo.tolist())
    return dict(train=pack(train),test=pack(test),evaluated_year=evaluated)
