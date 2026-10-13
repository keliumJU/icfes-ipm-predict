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
    for id,label,color in [('persistencia','Persistencia','#666666'),('global_v6','Global v6','#147a89')]:
        g=annual[annual.id==id].sort_values('year');axes[0].plot(g.year,g.MAE,'o-',label=label,color=color);axes[1].plot(g.year,g.bias,'o-',label=label,color=color)
    for ax,title in zip(axes,['Error absoluto medio','Sesgo (predicho − observado)']):ax.set(title=title,xlabel='Año externo',ylabel='Puntos de puntaje global',xticks=list(range(2021,2026)));ax.grid(alpha=.2);ax.legend()
    axes[1].axhline(0,color='black',linewidth=.7);fig.suptitle('Comparación exploratoria • n=33 por año; peso igual territorio-año')
    fig.savefig(folder/'01_error_y_sesgo_anual.png',dpi=180);plt.close(fig);files.append('01_error_y_sesgo_anual.png')
    g=errors[errors.id=='global_v6'];fig,ax=plt.subplots(figsize=(7,5),layout='constrained')
    for y,gy in g.groupby('year'):ax.scatter(gy.observed,gy.predicted,label=str(y),s=25,alpha=.7)
    lower=min(g.observed.min(),g.predicted.min());upper=max(g.observed.max(),g.predicted.max());ax.plot([lower,upper],[lower,upper],color='black',linestyle='--',label='Identidad')
    ax.set(xlabel='Puntaje global observado (puntos)',ylabel='Puntaje global previsto (puntos)',title='Global v6 • 165 pares dependientes; 33 territorios');ax.legend(title='Año externo',fontsize=8);ax.grid(alpha=.2)
    fig.savefig(folder/'02_observado_previsto.png',dpi=180);plt.close(fig);files.append('02_observado_previsto.png')
    rg=territory[territory.id=='persistencia'].sort_values('code');gg=territory[territory.id=='global_v6'].sort_values('code');delta=gg.MAE.to_numpy()-rg.MAE.to_numpy();fig,ax=plt.subplots(figsize=(11,4.8),layout='constrained');ax.bar(gg.code,delta,color=['#147a89' if x<0 else '#b55a45' for x in delta]);ax.axhline(0,color='black',linewidth=.8);ax.set(xlabel='Código territorial del colegio (incluye Bogotá)',ylabel='MAE global v6 − MAE persistencia (puntos)',title='Diferencia descriptiva territorial • n=5 años por territorio; 165 pares');ax.tick_params(axis='x',rotation=90);ax.grid(axis='y',alpha=.2)
    fig.savefig(folder/'03_diferencias_territoriales.png',dpi=180);plt.close(fig);files.append('03_diferencias_territoriales.png')
    save(OUT/'FIGURAS_ORIGEN.json',dict(cell=5,function='resultados.figures',files={n:sha(folder/n) for n in files},inputs={n:sha(TABLES/n) for n in ['metricas_anuales_200.csv','errores_completos_6600.csv','metricas_territoriales_1320.csv']},units='puntos puntaje global',n=165));print(files);return files
def thesis():
    p=load(OUT/'PRIMARIO.json');hist=readcsv(TABLES/'antecedentes_recalculados.csv');annual=readcsv(TABLES/'metricas_anuales_200.csv');contr=readcsv(TABLES/'contrastes_predefinidos_completos.csv');dec=readcsv(TABLES/'decisiones_globales.csv');evidence=[]
    def ev(claim,value,file,key,n,unit,cell,function):
        evidence.append(dict(claim=claim,value=str(value),cell=cell,function=function,file=str(file.relative_to(HERE)),table=file.stem,key=key,n=n,unit=unit,sha256=sha(file)));return value
    def num(key,precision=6):return f'{ev(key,p[key],OUT/"PRIMARIO.json",key,p["n"],"porcentaje" if "percent" in key else "puntos" if any(x in key for x in ["MAE","RMSE","bias"]) else "conteo",4,"resultados.analyse"):.{precision}f}'
    def texttable(df,cols,file,cell,function):
        lines=['| '+' | '.join(cols)+' |','| '+' | '.join(['---']*len(cols))+' |']
        for idx,row in df.iterrows():
            cells=[]
            for col in cols:
                val=row[col]
                if isinstance(val,(float,np.floating)):render=f'{val:.6f}'
                else:render=str(val)
                ev(f'{file.stem}:fila{idx}:{col}',val,file,f'row={idx};column={col}',row.get('n',165),'puntos/porcentaje/conteo según columna',cell,function);cells.append(render)
            lines.append('| '+' | '.join(cells)+' |')
        return '\n'.join(lines)
    v3=hist[hist.label=='v3_persistencia'].iloc[0];mglobal=hist[hist.label=='memoria_global'].iloc[0];mm=hist[hist.label=='memoria_memoria'].iloc[0]
    for label,row in [('v3',v3),('memglobal',mglobal),('memoria',mm)]:
        for key in ['MAE','improvement_vs_reference']:ev(label+'_'+key,row[key],TABLES/'antecedentes_recalculados.csv',f'label={row.label};{key}',165,'puntos' if key=='MAE' else 'porcentaje',3,'resultados.antecedents')
    tablehist=texttable(hist[['label','MAE','RMSE','improvement_vs_reference']],['label','MAE','RMSE','improvement_vs_reference'],TABLES/'antecedentes_recalculados.csv',3,'resultados.antecedents')
    globalannual=annual[annual.id.isin(['persistencia','global_v6'])][['id','year','n','MAE','RMSE','bias','direction_matches']]
    tableannual=texttable(globalannual,list(globalannual.columns),TABLES/'metricas_anuales_200.csv',4,'resultados.analyse')
    tabledec=texttable(dec[['year','selected']],['year','selected'],TABLES/'decisiones_globales.csv',4,'resultados.analyse')
    # Contrastes fijados en el código antes de observar resultados; no seleccionar por MAE externo.
    fixed=[('nivel_median_all','memoria_qr_a0p0_all'),('memoria_qr_a0p0_all','memoria_qr_a1p0_all'),('memoria_qr_a1p0_all','memoria_qr_a1p0_last2'),('memoria_qr_a1p0_all','memoria_ridge_a1p0_all'),('memoria_qr_a0p0_all','memoria_arbol_d1_all'),('comun_qr_a0p0_all','comun_correccion_qr_a0p0_all')]
    selected=pd.concat([contr[(contr.a==a)&(contr.b==b)] for a,b in fixed]);ctcols=['a','b','MAE_a','MAE_b','MAE_difference_b_minus_a','b_improves','b_worsens','ties'];tablecontrast=texttable(selected[ctcols],ctcols,TABLES/'contrastes_predefinidos_completos.csv',4,'resultados.analyse')
    gu=readcsv(TABLES/'guainia_historico.csv');ev('Guainía completo',gu.iloc[0].n_complete,TABLES/'guainia_historico.csv','row0;n_complete',gu.iloc[0].n_complete,'registros',3,'resultados.antecedents');ev('Guainía global',gu.iloc[0].n_global,TABLES/'guainia_historico.csv','row0;n_global',gu.iloc[0].n_global,'registros',3,'resultados.antecedents');ev('Guainía diferencia',gu.iloc[0].difference,TABLES/'guainia_historico.csv','row0;difference',gu.iloc[0].n_complete,'puntos',3,'resultados.antecedents')
    av=load(OUT/'DISPONIBILIDAD.json');ev('último año',av['last_usable_year'],OUT/'DISPONIBILIDAD.json','last_usable_year',231,'año',3,'resultados.antecedents');ev('siguiente condicional',av['next_year_conditional'],OUT/'DISPONIBILIDAD.json','next_year_conditional',231,'año',3,'resultados.antecedents')
    result='se alcanzó' if p['target_met'] else 'no se alcanzó'
    text=f'''# Objetivo 3. Evaluación exploratoria de procedimientos de predicción del puntaje global territorial

## Objetivo, unidad de análisis y fuente

Se evaluó si un procedimiento predefinido de selección temporal podía reducir el error absoluto medio respecto a la persistencia, manteniendo la población y la evaluación acordadas. La unidad de evaluación fue el territorio-año de ubicación del colegio. Se conservaron estudiantes de grado once, sin privación de libertad reportada y con puntajes presentes y positivos en las cinco pruebas y el global, sin filtro por calendario. El resultado fue la media global recibida; no se reemplazó por un promedio de subpruebas. Los territorios tuvieron igual peso, por lo que este resultado no es una media nacional ponderada por estudiantes.

Las fuentes fueron el panel analítico v2 y su derivado de cambios v5, identificados por SHA-256 en ESPECIFICACION_V6.json. Su conservación y coherencia aritmética se verificaron localmente. Esta validación no autentica el origen oficial ni demuestra cuándo los datos habrían estado disponibles para emitir una predicción anticipada.

## Diseño temporal y procedimiento

Se conservaron los niveles desde 2018 y se excluyó 2020. Cada cambio fue la diferencia respecto al máximo año previo disponible del mismo territorio, sin anualizar: para 2021, el previo fue 2019. El cambio de 2019 se utilizó como historial, pero no como respuesta supervisada, porque no existe un cambio previo de 2018. Las respuestas elegibles de entrenamiento comenzaron en 2021 y siempre precedieron al año evaluado. Las variantes con últimos años se aplicaron después de determinar estas respuestas elegibles, conservando los niveles y rezagos necesarios.

La evaluación externa reunió {int(num('n',0))} pares de {int(num('territories',0))} territorios entre 2021 y 2025. La ventana externa de 2021 quedó fijada en persistencia, sin ajuste, puntuación ni selección. Para cada año posterior, se puntuaron las ventanas internas acumuladas anteriores. Con cero respuestas elegibles se utilizó persistencia explícita; una respuesta anual completa permitió estimar, con una fila anual para el componente común y filas territoriales para memoria y corrección.

El contrato fijó 39 candidatos: persistencia; niveles históricos mediante media o mediana, con historia completa o últimos años; regresión de mediana con rezago y regularización; Ridge; árboles pequeños; nivel común; regresión del cambio común; y cambio común más corrección territorial. El componente común fue la mediana de los cambios territoriales; la corrección fue el cambio territorial menos ese componente. Año, código, intervalos, conteos, IPM y tasas de privación no entraron como predictores. Por ello, este contraste no permite interpretar cambios de pobreza como causas del puntaje.

Cada componente ajustado utilizó un Pipeline nuevo con StandardScaler estimado exclusivamente en entrenamiento y su regresor con todos los parámetros fijados. Los cambios previstos se sumaron al puntaje previo sin clipping ni calibración. Las constantes históricas también fueron estimaciones y se contabilizaron aunque no utilizaran sklearn.fit. La mediana par promedió los dos valores centrales y la media utilizó suma precisa dividida entre el número de respuestas.

La selección siguió exclusivamente las ventanas internas: candidatos con MAE hasta el mínimo más 0,1; dentro de ese grupo, RMSE hasta su mínimo más 0,1; luego menor número de entradas predictoras y orden fijo. Las constantes contaron como cero entradas y persistencia ocupó el primer lugar en el orden. El resultado primario fue global_v6; ninguna política escogida por su error externo lo sustituyó. El MAE y RMSE se calcularon sobre errores en puntos de puntaje global, con igual peso por territorio-año y suma precisa.

## Antecedentes y recálculos actuales

Los antecedentes se recalcularon desde predicciones guardadas en el notebook de resultados antes de citarlos. La persistencia v3 tuvo MAE {v3.MAE:.6f} y redujo el MAE de v2 en {v3.improvement_vs_reference:.6f} %. El ganador de esa comparación fue persistencia; no constituye demostración de aprendizaje del IPM. Las referencias globales v5 y recencia coincidieron exactamente con v3 en llaves, observados y predicciones y, por tanto, no aportan evidencia independiente.

En el experimento anterior de memoria/común, el global mejoró {mglobal.improvement_vs_reference:.6f} %, mientras la política individual de memoria mejoró {mm.improvement_vs_reference:.6f} %. Esta última cifra es exploratoria y no reemplaza el resultado global de aquel experimento. Ambos antecedentes motivaron contrastes fijados antes de observar v6; no se reinterpretaron como conclusiones actuales.

Tabla 1. Recálculos de guardados históricos. El porcentaje de v3 usa v2 como base; las políticas de memoria usan persistencia. No sumar estos porcentajes.

{tablehist}

## Resultado primario v6

Global_v6 obtuvo MAE **{num('global_MAE')} puntos**, RMSE **{num('global_RMSE')} puntos** y sesgo **{num('global_bias')} puntos**, frente al MAE de persistencia de **{num('reference_MAE')} puntos**. La mejora relativa fue **{num('improvement_percent')} %**. Por el criterio previamente establecido, **{result} la meta de {num('target_percent',0)} % adicional**. Esta conclusión se refiere exclusivamente al procedimiento global seleccionado con datos internos.

En la comparación pareada, el global redujo el error absoluto en {int(num('improves',0))} pares, lo aumentó en {int(num('worsens',0))} y empató en {int(num('ties',0))}. La dirección del cambio coincidió en {int(num('direction_matches',0))} pares; esta medida descriptiva no sustituye el MAE ni demuestra acierto en la magnitud del cambio. Los empates y copias son dependientes y no deben tratarse como replicaciones independientes.

Tabla 2. Selecciones guardadas antes de generar predicciones externas. El primer año externo mantuvo persistencia fija.

{tabledec}

Tabla 3. Errores por año. Sesgo positivo indica sobreestimación. Cada fila conserva igual peso territorial.

{tableannual}

![Error y sesgo anual](fase3/figuras/01_error_y_sesgo_anual.png)

![Observado y previsto](fase3/figuras/02_observado_previsto.png)

![Diferencias territoriales](fase3/figuras/03_diferencias_territoriales.png)

## Contrastes descriptivos e interpretación

La tabla siguiente presenta contrastes fijados en el código de análisis antes de observar los resultados: nivel frente a rezago, regularización, historia completa frente a últimos años, pérdida, no linealidad pequeña y componente común con corrección. La diferencia es MAE del segundo menos MAE del primero; un valor negativo favorece al segundo. Las tablas completas conservan todas las políticas y contrastes, sin usar el mejor error externo como nuevo primario.

{tablecontrast}

Los coeficientes, interceptos y escalas de cada ajuste se conservan en ajustes_coeficientes_completos.csv. Un coeficiente de rezago cero implica que ese ajuste utilizó un nivel histórico constante; no demuestra ausencia universal de dinámica ni identifica por sí solo la regularización como causa. La comparación de niveles y rezagos con historia comparable permite examinar esa hipótesis descriptivamente. Los contrastes QR–Ridge y QR–árbol cambian más de un aspecto del estimador, por lo que sus diferencias no se atribuyen exclusivamente a pérdida o no linealidad. Las comparaciones entre historia completa y últimos años conservan las mismas reglas de elegibilidad.

La posible coincidencia entre común y común más corrección debe interpretarse bajo los parámetros y ventanas examinados. Las medias y medianas comunes usan igual peso por año; los niveles territoriales apilan respuestas territoriales. Estas unidades de entrenamiento son distintas y ninguna equivale a una muestra nacional de estudiantes independientes. La selección acumulada puede reaccionar tarde ante un cambio de nivel; esta explicación permanece como hipótesis y no se corrigió retrospectivamente alterando ventanas o reglas.

El impacto de las diferencias por año y territorio es mostrar dónde el procedimiento reduce o aumenta el error, no justificar una selección posterior de años favorables. La alternativa verificable fue conservar el primario y reportar errores firmados, absolutos, sesgo y dirección completos, junto con los contrastes fijados. Esta alternativa se resolvió en el notebook, sin ampliar el experimento ni repetir ajustes para mejorar métricas.

## Integridad técnica, límites y conclusión

El piloto serial cerró su presupuesto antes de la auditoría y el análisis. Ejecutó {int(num('fits',0))} componentes ajustados y {int(num('constant_estimates',0))} estimaciones constantes en {num('seconds',3)} segundos. La auditoría independiente reconstruyó matrices, fechas, escalas, coeficientes, constantes, selección, copias, linaje y cobertura desde bytes y metadatos guardados, sin importar el selector o runner ni cargar modelos o realizar nuevos ajustes. La igualdad de CSV se verificó exactamente; la repetición de ajustes y la comprobación aritmética del scaler tienen tolerancias expresas en el informe técnico, que no reemplazan la igualdad de datos serializados.

Todos los años de evaluación ya se habían observado en el desarrollo experimental. Por tanto, los resultados son exploratorios, sin confirmación temporal independiente, causalidad ni pronóstico anticipado demostrado. Los pares comparten territorios y años, las copias internas no son nuevas observaciones y hay pocos años de entrenamiento. No se reportan p-valores confirmatorios ni intervalos de incertidumbre inventados.

La fuente local permanece sin autenticación oficial y sin fecha de disponibilidad histórica del panel demostrada. El antecedente de Guainía registra {int(gu.iloc[0].n_complete)} registros completos frente a {int(gu.iloc[0].n_global)} con puntaje global disponible, con diferencia de {gu.iloc[0].difference:.6f} puntos; consta en diagnóstico_medias_disponibles.csv de v2, filas de archivo 57 y 90. Se conservó la media recibida y no se reabrió esa comparación para buscar una mejora. El IPM mide hogares, mientras Saber 11 reúne estudiantes; la ubicación del colegio no equivale a residencia. Estas diferencias de población, agregación y geografía limitan interpretaciones ecológicas.

El objetivo se cierra con el resultado primario descrito, incluso cuando la meta adicional no se alcance. La aceptación técnica acredita coherencia y conservación del procedimiento, no autenticidad de datos, disponibilidad temporal ni confirmación científica. El último año utilizable comprobado en el panel local fue {av['last_usable_year']}. El siguiente año sería {av['next_year_conditional']} solo de forma condicional a fuentes comparables y disponibilidad verificable, con autorización separada. En esta entrega no se proyectaron puntajes, no se ejecutó el objetivo siguiente y no se seleccionó ni entrenó un modelo final.

## Trazabilidad y anexos

El notebook fase3/02_resultados_objetivo3.ipynb, generado desde notebook_resultados.py por generar_notebook.py, ejecutó las funciones compartidas que produjeron las tablas, figuras y cifras de este texto. EVIDENCIAS_TEXTO.csv vincula afirmaciones a celda, función, archivo, tabla, llave, tamaño, unidad y huella. Las tablas completas están en fase3/tablas/; el informe técnico y el manifiesto delimitan los controles y sus tolerancias. Las referencias documentales son locales verificadas: PROTOCOLO_V6.md §§1–9, ESPECIFICACION_V6.json, antecedentes_recalculados.csv, DISPONIBILIDAD.json y auditoria/fuentes_verificadas.md líneas3–7 (registro de consulta anterior, no certificación histórica del panel). No se añadieron citas bibliográficas no verificadas.
'''
    save(HERE/'TEXTO_OBJETIVO3_TESIS.md',text)
    csvsave('evidencias_texto',evidence);(HERE/'EVIDENCIAS_TEXTO.csv').write_bytes((TABLES/'evidencias_texto.csv').read_bytes())
    # Cada fuente ligada se comprueba antes de cerrar; los números son interpolaciones de esas salidas.
    for e in evidence:check(sha(HERE/e['file'])==e['sha256'],'evidence source changed')
    save(OUT/'CONTROL_TEXTO.json',dict(aprobado=True,claims=len(evidence),text_sha=sha(HERE/'TEXTO_OBJETIVO3_TESIS.md'),evidence_sha=sha(HERE/'EVIDENCIAS_TEXTO.csv'),method='texto interpolado directamente desde salidas notebook; cada tabla/valor ligado por función/archivo/llave/SHA; sin copiar cálculo externo',cell=6,function='resultados.thesis'))
    print({'text':str(HERE/'TEXTO_OBJETIVO3_TESIS.md'),'evidence_rows':len(evidence)});return len(evidence)
