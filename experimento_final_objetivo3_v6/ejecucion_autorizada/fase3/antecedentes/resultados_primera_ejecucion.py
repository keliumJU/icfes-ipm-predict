"""Cálculos y artefactos de tesis. Solo llamados desde notebook02 ejecutado."""
from comun import *
from auditor import error_metrics,equal,readpanel
from referencias import historical_frames
import math,statistics,datetime
import numpy as np
import pandas as pd
OUT=HERE/'fase3';TABLES=OUT/'tablas'
def csvsave(name,rows):
    p=safe(TABLES/(name+'.csv'));p.parent.mkdir(parents=True,exist_ok=True)
    df=rows if isinstance(rows,pd.DataFrame) else pd.DataFrame(rows);df.to_csv(p,index=False,float_format='%.17g');return df
def readcsv(p,**kw):return pd.read_csv(p,float_precision='round_trip',**kw)
def antecedents():
    frames=historical_frames();v3=frames['v3'];p=readpanel()
    v2path='experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv';v2=readcsv(ROOT/v2path,dtype={'codigo_departamento':str});v2=v2[v2.procedimiento=='procedimiento_v2'].copy();v2.codigo_departamento=v2.codigo_departamento.str.zfill(2);v2=v2.sort_values(['anio','codigo_departamento']).reset_index(drop=True)
    check(len(v2)==165,'v2n');equal(v2[['anio','codigo_departamento']],v3[['anio','codigo_departamento']],'v2keys');equal(v2.observado,v3.observado,'v2 observed')
    m3=error_metrics(v3.prediccion,v3.observado);m2=error_metrics(v2.prediccion,v2.observado);improve=100*(m2['MAE']-m3['MAE'])/m2['MAE'];meta=load(ROOT/'experimentos_objetivo3_v3/etapa2/resultados/meta.json')
    check(m3['MAE']==meta['mae_v3'] and m2['MAE']==meta['mae_v2'] and improve==meta['mejora_porcentual_exacta'],'historical v3/meta exact')
    records=[dict(label='v2_global',source=v2path,**m2,improvement_vs_reference=0.,status='recálculo actual de guardados históricos'),dict(label='v3_persistencia',source=v3.attrs['path'],**m3,improvement_vs_reference=improve,status='recálculo actual; mejora frente a v2')]
    for label in ['v5','recencia']:records.append(dict(label=label+'_global',source=frames[label].attrs['path'],**error_metrics(frames[label].prediccion,frames[label].observado),improvement_vs_reference=0.,status='mismas llaves/observados/predicciones v3; no evidencia independiente'))
    mp='experimentos_memoria_comun_objetivo3_v1/etapa2/resultados/predicciones_externas.csv';mem=readcsv(ROOT/mp,dtype={'code':str});mem=mem.sort_values(['external','code'])
    for policy,expected in [('global',1.7979745286559843),('memoria',12.392390281511053)]:
        g=mem[mem.policy==policy];check(len(g)==165,'mem165');equal(g[['external','code']].to_numpy(),v3[['anio','codigo_departamento']].to_numpy(),'memkeys');equal(g.observed,v3.observado,'memobserved')
        m=error_metrics(g.predicted,g.observed);imp=100*(m3['MAE']-m['MAE'])/m3['MAE'];check(imp==expected,'mem historical exact')
        records.append(dict(label='memoria_'+policy,source=mp,**m,improvement_vs_reference=imp,status='exploratorio histórico; no conclusión v6'))
    csvsave('antecedentes_recalculados',records)
    dp='experimentos_objetivo3_v2/fase1/resultados/diagnostico_medias_disponibles.csv';diag=readcsv(ROOT/dp,dtype={'codigo_departamento':str});found=[]
    for lineno in [57,90]:
        row=diag.iloc[lineno-2];check(row.codigo_departamento=='94' and row.n_completos==238 and row.n_global_disponible==404,'Guainía histórico ubicación')
        diff=float(row.media_completos)-float(row.media_global_disponible);check(diff==row.diferencia==21.012105832431985,'Guainía diferencia exacta')
        found.append(dict(file=dp,file_line=lineno,scope=row.alcance,period=row.periodo,code='94',n_complete=int(row.n_completos),n_global=int(row.n_global_disponible),difference=diff))
    csvsave('guainia_historico',found)
    doc=ROOT/'auditoria/fuentes_verificadas.md';check('2026-10-07' in doc.read_text(),'fecha local antecedente')
    availability=dict(last_usable_year=max(p['years']),next_year_conditional=max(p['years'])+1,source_sha=load(HERE/'ESPECIFICACION_V6.json')['fuentes'],local_evidence='auditoria/fuentes_verificadas.md líneas3/7: consulta2026-10-07 y publicación IPM2024 registrada22/04/2025; no acredita publicación/disponibilidad histórica del panel2025',verified_panel_publication_date=None,forecast_executed=False,authenticity='fuente local no autenticada; SHA demuestra conservación, no autenticidad/fecha',local_file_metadata=[dict(file=s,mtime_utc=datetime.datetime.fromtimestamp((ROOT/s).stat().st_mtime,datetime.timezone.utc).isoformat(),meaning='fecha del archivo local; no publicación oficial') for s in load(HERE/'ESPECIFICACION_V6.json')['fuentes']])
    save(OUT/'DISPONIBILIDAD.json',availability)
    print(pd.DataFrame(records)[['label','MAE','RMSE','improvement_vs_reference']].to_string(index=False));print(availability)
    return records
def analyse():
    check(load(OUT/'AUDITORIA.json')['aprobado'],'auditoría indispensable')
    df=readcsv(HERE/'fase2/piloto/externas.csv',dtype={'code':str}).sort_values(['id','year','code']).reset_index(drop=True);spec=load(HERE/'ESPECIFICACION_V6.json');cands={c['id']:c for c in spec['candidates']}
    df['signed_error']=df.predicted-df.observed;df['absolute_error']=df.signed_error.abs();df['observed_delta']=df.observed-df.previous
    df['direction_match']=np.sign(df.predicted_delta)==np.sign(df.observed_delta)
    csvsave('errores_completos_6600',df)
    ref=df[df.id=='persistencia'].sort_values(['year','code']);reference=error_metrics(ref.predicted,ref.observed)['MAE'];check(math.isfinite(reference) and reference>0,'denominador mejora')
    overall=[];annual=[];territory=[];paired=[]
    for id,g in df.groupby('id',sort=False):
        info=cands.get(id,dict(family='selección interna',history='según seleccionado',inputs=None,order=39))
        m=error_metrics(g.predicted,g.observed);imp=100*(reference-m['MAE'])/reference
        overall.append(dict(id=id,family=info['family'],history=info['history'],inputs=info['inputs'],order=info['order'],**m,improvement_percent=imp,direction_matches=int(g.direction_match.sum())))
        for year,gy in g.groupby('year'):
            annual.append(dict(id=id,year=int(year),**error_metrics(gy.predicted,gy.observed),direction_matches=int(gy.direction_match.sum())))
        for code,gc in g.groupby('code'):
            territory.append(dict(id=id,code=code,**error_metrics(gc.predicted,gc.observed),direction_matches=int(gc.direction_match.sum())))
        aligned=g.sort_values(['year','code']);equal(aligned[['year','code']],ref[['year','code']],'pairs keys');equal(aligned.observed,ref.observed,'pairs observed')
        for (_,row),(_,rr) in zip(aligned.iterrows(),ref.iterrows()):paired.append(dict(id=id,year=int(row.year),code=row.code,signed_error=row.signed_error,absolute_error=row.absolute_error,reference_absolute_error=rr.absolute_error,absolute_error_difference=row.absolute_error-rr.absolute_error,improves=row.absolute_error<rr.absolute_error,worsens=row.absolute_error>rr.absolute_error))
    overall=csvsave('metricas_40_procedimientos',sorted(overall,key=lambda r:r['order']));csvsave('metricas_anuales_200',annual);csvsave('metricas_territoriales_1320',territory);paired=csvsave('comparaciones_pareadas_6600',paired)
    contrasts=[];pairs=[]
    def add(a,b,label,factors):pairs.append((a,b,label,factors))
    for cand in cands.values():
        if cand['family'] in ['nivel_territorial','nivel_comun']:add('persistencia',cand['id'],'nivel histórico vs persistencia','estadística histórica')
    for hist in ['all','last2','last3']:
        add('nivel_median_'+hist,'memoria_qr_a0p0_'+hist,'nivel vs rezago QR sin penalización','rezago/optimización mediana')
        for alpha in ['0p01','0p1','1p0']:add('memoria_qr_a0p0_'+hist,'memoria_qr_a'+alpha+'_'+hist,'regularización QR','alpha')
        add('memoria_qr_a1p0_'+hist,'memoria_ridge_a1p0_'+hist,'pérdida cuadrática vs absoluta','pérdida y penalización; efecto no aislado')
        add('memoria_ridge_a1p0_'+hist,'memoria_ridge_a10p0_'+hist,'regularización Ridge','alpha')
    for cand in cands.values():
        if cand['history'].startswith('last'):
            allid=cand['id'].rsplit('_last',1)[0]+'_all';add(allid,cand['id'],'historia completa vs últimos k','historia de respuestas elegibles')
    for depth in [1,2]:add('memoria_qr_a0p0_all',f'memoria_arbol_d{depth}_all','no linealidad pequeña','estimador/no linealidad/hoja; efecto no aislado')
    add('memoria_arbol_d1_all','memoria_arbol_d2_all','profundidad limitada','max_depth')
    for alpha in ['0p0','0p01','0p1','1p0']:add('comun_qr_a'+alpha+'_all','comun_correccion_qr_a'+alpha+'_all','común vs común+corrección','corrección territorial')
    add('nivel_comun_median_all','comun_qr_a0p0_all','nivel común vs rezago común','rezago/optimización mediana')
    for a,b,label,factors in pairs:
        ga=df[df.id==a].sort_values(['year','code']);gb=df[df.id==b].sort_values(['year','code']);ea=ga.absolute_error.to_numpy();eb=gb.absolute_error.to_numpy()
        ma=error_metrics(ga.predicted,ga.observed);mb=error_metrics(gb.predicted,gb.observed)
        contrasts.append(dict(a=a,b=b,contrast=label,factors=factors,n=len(ga),MAE_a=ma['MAE'],MAE_b=mb['MAE'],MAE_difference_b_minus_a=mb['MAE']-ma['MAE'],RMSE_difference_b_minus_a=mb['RMSE']-ma['RMSE'],b_improves=int((eb<ea).sum()),b_worsens=int((eb>ea).sum()),ties=int((eb==ea).sum()),predictions_exactly_equal=bool(np.array_equal(ga.predicted,gb.predicted))))
    csvsave('contrastes_predefinidos_completos',contrasts)
    coefficients=[]
    for m in load(OUT/'COEFICIENTES.json'):
        row={k:m[k] for k in ['job','id','year','component','regressor','n_samples']};row.update(scaler_mean=m['scaler_mean'][0],scaler_scale=m['scaler_scale'][0],coef=m.get('coef',[None])[0],intercept=m.get('intercept'),zero_lag=(m['coef'][0]==0) if 'coef' in m else None,warnings=json.dumps(m['warnings']),repeat=m['job'].startswith('check_'))
        coefficients.append(row)
    csvsave('ajustes_coeficientes_completos',coefficients)
    decisions=[]
    for y in range(2022,2026):
        d=load(HERE/f'fase2/piloto/selections/{y}.json');decisions.append(dict(year=y,selected=d['winner'],mae_min=d['mae_min'],rmse_pool_min=d['rmse_pool_min'],pool_mae='|'.join(d['pool_mae']),pool_rmse='|'.join(d['pool_rmse'])))
    csvsave('decisiones_globales',decisions);csvsave('selecciones_completas_156',readcsv(HERE/'fase2/piloto/selecciones.csv'))
    globalrow=next(r for r in overall.to_dict('records') if r['id']=='global_v6');gp=paired[paired.id=='global_v6'];ledger=load(HERE/'fase2/piloto/ledger.json')
    primary=dict(reference_MAE=reference,global_MAE=globalrow['MAE'],global_RMSE=globalrow['RMSE'],global_bias=globalrow['bias'],improvement_percent=globalrow['improvement_percent'],target_percent=5,target_met=bool(globalrow['improvement_percent']>=5),n=165,territories=33,external_years=list(range(2021,2026)),improves=int(gp.improves.sum()),worsens=int(gp.worsens.sum()),ties=int((~gp.improves&~gp.worsens).sum()),direction_matches=globalrow['direction_matches'],fits=ledger['fits_started'],constant_estimates=ledger['statistical_estimates'],seconds=ledger['elapsed_seconds'])
    save(OUT/'PRIMARIO.json',primary);print(primary);print(pd.DataFrame(decisions).to_string(index=False));return primary
def figures():
    os.environ['MPLCONFIGDIR']=str(OUT/'cache_matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    folder=OUT/'figuras';folder.mkdir(parents=True,exist_ok=True)
    annual=readcsv(TABLES/'metricas_anuales_200.csv');overall=readcsv(TABLES/'metricas_40_procedimientos.csv');errors=readcsv(TABLES/'errores_completos_6600.csv',dtype={'code':str});territory=readcsv(TABLES/'metricas_territoriales_1320.csv',dtype={'code':str})
    files=[]
    fig,axes=plt.subplots(1,2,figsize=(11,4.3),layout='constrained')
    for id,label,color in [('persistencia','Persistencia','#666666'),('global_v6','Procedimiento seleccionado','#147a89')]:
        g=annual[annual.id==id].sort_values('year');axes[0].plot(g.year,g.MAE,'o-',label=label,color=color);axes[1].plot(g.year,g.bias,'o-',label=label,color=color)
    for ax,title in zip(axes,['Error absoluto medio','Sesgo (predicho − observado)']):ax.set(title=title,xlabel='Año externo',ylabel='Puntos de puntaje global',xticks=list(range(2021,2026)));ax.grid(alpha=.2);ax.legend()
    axes[1].axhline(0,color='black',linewidth=.7);fig.suptitle('Comparación exploratoria • n=33 por año; peso igual territorio-año')
    fig.savefig(folder/'01_error_y_sesgo_anual.png',dpi=180);plt.close(fig);files.append('01_error_y_sesgo_anual.png')
    g=errors[errors.id=='global_v6'];fig,ax=plt.subplots(figsize=(7,5),layout='constrained')
    for y,gy in g.groupby('year'):ax.scatter(gy.observed,gy.predicted,label=str(y),s=25,alpha=.7)
    lower=min(g.observed.min(),g.predicted.min());upper=max(g.observed.max(),g.predicted.max());ax.plot([lower,upper],[lower,upper],color='black',linestyle='--',label='Identidad')
    ax.set(xlabel='Puntaje global observado (puntos)',ylabel='Puntaje global previsto (puntos)',title='Procedimiento seleccionado • 165 pares dependientes; 33 territorios');ax.legend(title='Año externo',fontsize=8);ax.grid(alpha=.2)
    fig.savefig(folder/'02_observado_previsto.png',dpi=180);plt.close(fig);files.append('02_observado_previsto.png')
    rg=territory[territory.id=='persistencia'].sort_values('code');gg=territory[territory.id=='global_v6'].sort_values('code');delta=gg.MAE.to_numpy()-rg.MAE.to_numpy();fig,ax=plt.subplots(figsize=(11,4.8),layout='constrained');ax.bar(gg.code,delta,color=['#147a89' if x<0 else '#b55a45' for x in delta]);ax.axhline(0,color='black',linewidth=.8);ax.set(xlabel='Código territorial del colegio (incluye Bogotá)',ylabel='MAE seleccionado − MAE persistencia (puntos)',title='Diferencia descriptiva territorial • n=5 años por territorio; 165 pares');ax.tick_params(axis='x',rotation=90);ax.grid(axis='y',alpha=.2)
    fig.savefig(folder/'03_diferencias_territoriales.png',dpi=180);plt.close(fig);files.append('03_diferencias_territoriales.png')
    save(OUT/'FIGURAS_ORIGEN.json',dict(cell=5,function='resultados.figures',files={n:sha(folder/n) for n in files},inputs={n:sha(TABLES/n) for n in ['metricas_anuales_200.csv','errores_completos_6600.csv','metricas_territoriales_1320.csv']},units='puntos puntaje global',n=165));print(files);return files

def label_candidate(id):
    if id=='global_v6':return 'Procedimiento seleccionado'
    c=next(c for c in load(HERE/'ESPECIFICACION_V6.json')['candidates'] if c['id']==id)
    if c['family']=='persistencia':return 'Persistencia'
    history='historia completa' if c['history']=='all' else 'últimas '+c['history'][4:]+' respuestas anuales'
    if c['family'].startswith('nivel_'):
        return ('Mediana' if c['statistic']=='median' else 'Media')+(' del cambio común' if c['family']=='nivel_comun' else ' del cambio territorial')+'; '+history
    if c['family']=='memoria_arbol':return 'Árbol; profundidad '+str(c['params']['DecisionTreeRegressor']['max_depth'])+'; '+history
    reg=next(k for k in c['params'] if k!='StandardScaler');alpha=c['params'][reg]['alpha']
    family={'memoria_qr':'Regresión de mediana del cambio territorial','memoria_ridge':'Ridge del cambio territorial','comun_qr':'Regresión de mediana del cambio común','comun_correccion_qr':'Cambio común y corrección territorial'}[c['family']]
    return family+'; α='+str(alpha)+'; '+history

def complementary_tables():
    """Recálculo descriptivo de todos los procedimientos IPM ya guardados; cero fits."""
    frames=historical_frames();ref=frames['v3'];path=ROOT/'experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv'
    df=readcsv(path,dtype={'codigo_departamento':str});df.codigo_departamento=df.codigo_departamento.str.zfill(2)
    records=[]
    for name,g in df.groupby('procedimiento',sort=False):
        g=g.sort_values(['anio','codigo_departamento']).reset_index(drop=True)
        check(len(g)==165 and not g.duplicated(['anio','codigo_departamento']).any(),'IPM165')
        equal(g[['anio','codigo_departamento']],ref[['anio','codigo_departamento']],'IPM same keys');equal(g.observado,ref.observado,'IPM observed')
        m=error_metrics(g.prediccion,g.observado);records.append(dict(procedure=name,**m,source=str(path.relative_to(ROOT)),status='recálculo de resultados guardados; no nueva estimación',same165=True))
    csvsave('procedimientos_indicadores_pobreza_recalculados',records)
    # Datos de diseño recalculados desde matrices y fechas guardadas.
    spec=load(HERE/'ESPECIFICACION_V6.json');ledger=load(HERE/'fase2/piloto/ledger.json');panel=readpanel()
    design=dict(level_rows=sum(len(v) for v in panel['levels'].values()),change_rows=sum(len(v) for v in panel['d'].values()),territories=len(panel['codes']),years=panel['years'],external_years=list(range(2021,2026)),external_n=165,candidates=len(spec['candidates']),internal_windows=sum(len(w['internas']) for w in spec['windows']),seed=SEED,first_supervised=2021,historical_level=2018,historical_change=2019,excluded_year=2020,previous2021=panel['prior'][2021],selection_band=.1,target_percent=5)
    save(OUT/'DISENO_RECALCULADO.json',design)
    overall=readcsv(TABLES/'metricas_40_procedimientos.csv');overall.insert(1,'procedimiento',overall.id.map(label_candidate));csvsave('metricas_completas_nombres_academicos',overall)
    annual=readcsv(TABLES/'metricas_anuales_200.csv');aa=annual[annual.id.isin(['persistencia','global_v6'])].copy();aa['procedimiento']=aa.id.map(label_candidate);csvsave('tabla_academica_anual',aa)
    terr=readcsv(TABLES/'metricas_territoriales_1320.csv',dtype={'code':str});ref=terr[terr.id=='persistencia'].sort_values('code').reset_index(drop=True);g=terr[terr.id=='global_v6'].sort_values('code').reset_index(drop=True)
    tt=pd.DataFrame(dict(code=g.code,n=g.n,MAE_selected=g.MAE,MAE_reference=ref.MAE,MAE_difference=g.MAE-ref.MAE,bias=g.bias,direction_matches=g.direction_matches));csvsave('tabla_academica_territorial_completa',tt)
    contrasts=readcsv(TABLES/'contrastes_predefinidos_completos.csv');contrasts['procedimiento_a']=contrasts.a.map(label_candidate);contrasts['procedimiento_b']=contrasts.b.map(label_candidate);csvsave('contrastes_completos_nombres_academicos',contrasts)
    decisions=readcsv(TABLES/'decisiones_globales.csv');decisions['procedimiento']=decisions.selected.map(label_candidate);csvsave('tabla_academica_selecciones',decisions)
    coef=readcsv(TABLES/'ajustes_coeficientes_completos.csv');fits=coef[~coef.repeat];counts=[]
    for (id,component),g in fits.groupby(['id','component']):
        counts.append(dict(id=id,component=component,n_fits=len(g),n_zero_lag=int(g.zero_lag.map(lambda v: str(v).lower()=='true').sum()),linear=int(g.coef.notna().sum()),n_warnings=int(sum(len(json.loads(v)) for v in g.warnings))))
    csvsave('diagnostico_coeficientes_cero',counts)
    save(OUT/'REGISTRO_ANALISIS.json',dict(real_fits_new=0,cells=dict(antecedents=3,analyse=4,figures=5,complementary_tables=6),technical_ids_in_academic_tables=False,historical_methods='PROTOCOLO_V2.md §§1–6: indicadores pobreza; resultados guardados recalculados',thesis_style='ACA2.pdf físicas25,56–60,113–114: impersonal; cautela asociacional; párrafos conectados',objective_alignment='tesis propone aprenderIPM: contraste temporal nuevo evalúa dinámica del resultado, no aporte incremental del IPM; no afirmar validación íntegraH3 ni plan páginas58–59 ejecutado',copies_dependent=True))
    print({'historical_procedures':len(records),'design':design,'full_territories':len(tt),'contrasts':len(contrasts),'new_fits':0})
    return design
