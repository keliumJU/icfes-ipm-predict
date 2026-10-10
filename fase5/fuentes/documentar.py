"""Tablas, figuras e informe a partir de CSV congelados; sin estimadores."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/icfes-fase5-matplotlib')
from pathlib import Path
import json, platform, hashlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'fase5/resultados'; FIG=ROOT/'fase5/figuras'
WIN='gradient_boosting_ambas_07'
IDS=['media','ols_ipm','gradient_boosting_ipm_02','ols_tasas','gradient_boosting_tasas_07','ols_ambas',WIN]
FUENTES={}
def leer(ruta):
    FUENTES[ruta]=hashlib.sha256((ROOT/ruta).read_bytes()).hexdigest()
    return pd.read_csv(ROOT/ruta,float_precision='round_trip',dtype={'codigo_departamento':str})
def tabla(df,nombre):
    df.to_csv(OUT/(nombre+'.csv'),index=False)
    def f(v):
        if isinstance(v,(float,np.floating)): return f'{v:.6f}'
        return str(v)
    return '\n'.join(['| '+' | '.join(df.columns)+' |','| '+' | '.join(['---']*len(df.columns))+' |']+['| '+' | '.join(f(v) for v in row)+' |' for row in df.itertuples(index=False,name=None)])
def guardar(fig,nombre):
    fig.savefig(FIG/(nombre+'.png'),dpi=170,bbox_inches='tight')
    fig.savefig(FIG/(nombre+'.svg'),bbox_inches='tight')
    svg = FIG/(nombre+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)
def metricas(df):
    e=df.prediccion.to_numpy()-df.observado.to_numpy(); y=df.observado.to_numpy()
    return [len(df),np.mean(abs(e)),np.sqrt(np.mean(e**2)),np.mean(e),1-np.sum(e**2)/np.sum((y-y.mean())**2)]
def generar():
    OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
    base=leer('auditoria/base_analitica_departamento_anio.csv')
    dev=leer('fase3/resultados/comparacion_desarrollo.csv')
    met=leer('fase3/resultados/metricas_reevaluacion.csv')
    terr=leer('fase4/resultados/metricas_agrupadas.csv')
    boot=leer('fase4/resultados/bootstrap_resumen.csv')
    assoc=leer('fase4/resultados/asociaciones_longitudinales.csv')
    coef=leer('fase4/resultados/coeficientes_ols_congelados.csv')
    pdv=leer('fase3/resultados/predicciones_desarrollo.csv')
    pte=leer('fase3/resultados/predicciones_reevaluacion.csv')
    ptr=leer('fase4/resultados/predicciones_territoriales.csv')
    mt=leer('fase4/resultados/metricas_territorio.csv')
    col=leer('fase4/resultados/colinealidad.csv')
    influence=leer('fase4/resultados/influencia_grupos_errores.csv')
    sizes=leer('fase4/resultados/diagnostico_tamanos.csv')
    # Recalcular métricas de todos los resultados existentes, nunca predicciones nuevas.
    comprobaciones=[]
    for preds,metrics,keys,ctx in [(pdv,dev,['id'],'seleccion'),(pte,met,['id','periodo'],'temporal'),(ptr,terr,['id'],'territorial')]:
        for _,r in metrics.iterrows():
            p=preds[preds.id==r.id]
            if ctx=='temporal' and str(r.periodo)!='conjunto': p=p[p.anio==int(r.periodo)]
            valores=metricas(p)
            for k,v in zip(['n','mae','rmse','sesgo','r2'],valores):
                if k in r.index: assert np.isclose(v,float(r[k]),rtol=0,atol=1e-10),(ctx,r.id,k)
            comprobaciones.append({'contexto':ctx,'id':r.id,'periodo':str(r.get('periodo','agrupado')),'n':len(p),'metricas_coinciden':True})
    muestra=base.groupby('anio',as_index=False).agg(territorios=('codigo_departamento','nunique'),celdas=('codigo_departamento','size'),registros=('n_estudiantes_saber','sum'),min_registros=('n_estudiantes_saber','min'),max_registros=('n_estudiantes_saber','max'))
    muestra['uso']=np.where(muestra.anio<=2022,'Desarrollo','Reevaluación temporal expuesta')
    assert muestra.registros.sum()==2984199 and len(base)==198
    tablas={'MUESTRA':tabla(muestra,'tabla_muestra')}
    espec=pd.DataFrame([['IPM',1,'Incidencia (% personas)','Media común; OLS; Ridge; RF; GBR'],['Tasas',15,'Tasas marginales (% hogares)','Media común; OLS; Ridge; RF; GBR'],['Ambas',16,'Incidencia y tasas','Media común; OLS; Ridge; RF; GBR']],columns=['Especificación','Entradas','Unidad local','Familias comparadas'])
    tablas['ESPEC']=tabla(espec,'tabla_especificaciones')
    fam=dev.loc[dev.groupby('familia').mae.idxmin(),['familia','id','mae','rmse','sesgo','r2']].sort_values('mae')
    tablas['FAMILIAS']=tabla(fam,'tabla_familias_seleccion')
    tablas['SELECCION']=tabla(dev.set_index('id').loc[IDS].reset_index()[['id','n_entradas','mae','rmse','sesgo','r2']],'tabla_seleccion_referencias')
    tablas['RESERVA']=tabla(met[met.periodo.astype(str)=='conjunto'][['id','n','mae','rmse','sesgo','r2']],'tabla_reevaluacion_conjunta')
    tablas['ANUAL']=tabla(met[met.id==WIN][['periodo','n','mae','rmse','sesgo','r2']],'tabla_ganador_temporal')
    tablas['TERRITORIAL']=tabla(terr[['id','n','mae','rmse','sesgo','r2']],'tabla_territorial')
    tablas['BOOT']=tabla(boot,'tabla_remuestreo')
    tablas['ASOC']=tabla(assoc[['variable','r_entre_territorios','r_dentro_territorio','r_doble_centrado']],'tabla_asociaciones')
    robust=pd.DataFrame([
        ['Diferencia tasas−ambas territorial','−0.241788; percentiles [−0.569529; 0.045591]','Ventaja puntual de tasas; rango cruza cero','bootstrap_resumen.csv; territorial_desarrollo'],
        ['Ganador−OLS IPM temporal','−3.206676; [−5.669490; −0.962579]','Dispersión condicional favorable; reserva expuesta','bootstrap_resumen.csv; temporal_cerrado_2023_2024'],
        ['Omitir errores de un territorio; ambas','MAE entre 7.500620 y 8.251786','Influencia de composición con errores fijos','influencia_grupos_errores.csv; ambas'],
        ['Soporte marginal territorial','126 valores fuera de rango / 4224 entradas','No acredita soporte conjunto; tasas repetidas','soporte_territorial.csv; fase4/informe.md'],
        ['Colinealidad','Condición 1 / 12.644109 / 30.647008','Rango completo; separación de aportes limitada','colinealidad.csv; IPM/tasas/ambas'],
        ['Tamaño de celda Saber desarrollo','190–79542 registros','No mide precisión de la encuesta IPM','diagnostico_tamanos.csv'],
    ],columns=['Diagnóstico','Resultado existente','Alcance','Fuente en fase4/resultados'])
    tablas['ROBUST']=tabla(robust,'tabla_sintesis_robustez')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    years=[2018,2019,2021,2022,2023,2024]
    fig,ax=plt.subplots(figsize=(12,4.5))
    rows=[['Ajuste','Validación','','','',''],['Ajuste','Ajuste','Validación','','',''],['Ajuste','Ajuste','Ajuste','Validación','',''],['Ajuste final','Ajuste final','Ajuste final','Ajuste final','Reevaluación','Reevaluación']]
    colors={'Ajuste':'#bed8e7','Validación':'#f4cf83','':'#eeeeee','Ajuste final':'#8eb5cf','Reevaluación':'#caadd9'}
    for i,row in enumerate(rows):
        for j,c in enumerate(row):
            ax.add_patch(plt.Rectangle((j-.48,i-.38),.96,.76,color=colors[c])); ax.text(j,i,c or '—',ha='center',va='center',fontsize=9)
    ax.set(xlim=(-.6,5.6),ylim=(3.6,-.6),xticks=range(6),xticklabels=[f'{y}\n33 territorios' for y in years],yticks=range(4),yticklabels=['Ventana 1','Ventana 2','Ventana 3','Modelo congelado'],title='Partición temporal: selección expansiva y reevaluación cerrada')
    ax.text(0,-.15,'',transform=ax.transAxes)
    fig.subplots_adjust(bottom=.24)
    fig.text(.15,.01,'2020 ausente del universo; entradas del mismo año. 2023–2024 previamente expuestos.',fontsize=10)
    guardar(fig,'01_particion_temporal')
    fig,axs=plt.subplots(1,3,figsize=(14,4.8),sharex=True,sharey=True)
    for ax,p,title in zip(axs,[pdv[pdv.id==WIN],pte[pte.id==WIN],ptr[ptr.id==WIN]],['Selección: 2019, 2021, 2022\n99 predicciones; optimismo de selección','Reevaluación temporal: 2023–2024\n66 predicciones; reserva expuesta','Diagnóstico territorial: 2018–2022\n132 predicciones; selección previa']):
        for year,g in p.groupby('anio'): ax.scatter(g.observado,g.prediccion,label=str(year),s=28,alpha=.8)
        ax.plot([180,300],[180,300],color='#555555',linestyle='--'); ax.set(title=title,xlabel='Observado (puntos)',xlim=(180,300),ylim=(180,300)); ax.legend(fontsize=8)
        ax.set_aspect('equal')
    axs[0].set_ylabel('Predicho (puntos)'); fig.suptitle('GBR ambas: configuración ganadora aplicada en cada diseño',y=1.03)
    guardar(fig,'02_observado_predicho')
    temporal=pte[pte.id==WIN].groupby('departamento').error.apply(lambda s:abs(s).mean())
    territorial=mt[mt.id==WIN].set_index('departamento').mae
    names=territorial.sort_values().index
    fig,axs=plt.subplots(1,2,figsize=(13,12),sharey=True)
    for ax,data,title,color in zip(axs,[temporal,territorial],['Reevaluación temporal 2023–2024\n2 errores por territorio; reserva expuesta','Diagnóstico territorial 2018/2019/2021/2022\n4 errores por territorio; selección previa'],['#725491','#247b91']):
        ax.barh(names,data.reindex(names),color=color); ax.set(title=title,xlabel='MAE por territorio (puntos)',xlim=(0,30)); ax.grid(axis='x',alpha=.2)
    fig.suptitle('Heterogeneidad territorial del error: GBR ambas',y=.94)
    guardar(fig,'03_errores_territoriales')
    cf=coef.pivot(index='variable',columns='id',values='coef_por_sd_entrenamiento')
    names=assoc.variable.to_list(); ypos=np.arange(len(names))
    fig,axs=plt.subplots(1,2,figsize=(17,12),gridspec_kw={'width_ratios':[1.15,1]})
    for k,label,color in [('r_entre_territorios','Entre territorios (33 medias)','#24647b'),('r_dentro_territorio','Dentro (132 desviaciones)','#bf7829'),('r_doble_centrado','Doble centrado (132 filas)','#7a5195')]:
        axs[0].scatter(assoc[k],ypos,label=label,color=color,s=40)
    axs[0].set(yticks=ypos,yticklabels=names,xlim=(-1,1),xlabel='Correlación de Pearson',title='Asociaciones de desarrollo con puntaje global'); axs[0].invert_yaxis(); axs[0].axvline(0,color='gray',linewidth=.8); axs[0].legend(loc='upper center',bbox_to_anchor=(.5,-.08),fontsize=9)
    for id,label,marker in [('ols_tasas','OLS tasas','o'),('ols_ambas','OLS ambas','s')]:
        axs[1].scatter(cf.reindex(names)[id],ypos,label=label,marker=marker,s=35)
    axs[1].scatter(cf.reindex(names).ols_ipm,ypos,label='OLS IPM',marker='^',s=45)
    axs[1].set(yticks=ypos,yticklabels=[],xlabel='Puntos por una DE de entrenamiento',title='Coeficientes OLS congelados (132 filas hasta 2022)'); axs[1].invert_yaxis(); axs[1].axvline(0,color='gray',linewidth=.8); axs[1].legend(loc='upper center',bbox_to_anchor=(.5,-.08))
    fig.suptitle('Estabilidad interpretativa descriptiva: asociaciones y especificaciones OLS\nNo son efectos causales ni importancias del GBR',y=.94)
    guardar(fig,'04_estabilidad_interpretativa')
    plantilla=(ROOT/'fase5/fuentes/informe_plantilla.md').read_text()
    for key,value in tablas.items(): plantilla=plantilla.replace('{{'+key+'}}',value)
    assert '{{' not in plantilla
    (ROOT/'informe_objetivo_3.md').write_text(plantilla)
    registro={'fecha_cliente':'2026-10-09','versiones_documentacion':{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__},'fuentes_sha256':FUENTES,'comprobaciones_metricas':comprobaciones,'modelos_ajustados':0,'predicciones_nuevas':0,'remuestreos_nuevos':0,'semilla':'No aplica: visualización y resumen deterministas de resultados existentes','tablas':list(tablas),'figuras':{'01_particion_temporal':'Protocolo§4; años y cardinalidades de base existente','02_observado_predicho':'GBR ambas; tres diseños separados; CSV de predicciones existentes','03_errores_territoriales':'GBR ambas; MAE temporal por grupo desde errores existentes y MAE territorial fase4','04_estabilidad_interpretativa':'Desarrollo; asociaciones fase4 y coeficientes OLS congelados, sin nuevos ajustes'}}
    (OUT/'generacion.json').write_text(json.dumps(registro,ensure_ascii=False,indent=2)+'\n')
    return registro
if __name__=='__main__':
    r=generar(); print('Informe, 10 tablas, cuatro figuras PNG/SVG; métricas existentes cotejadas:',len(r['comprobaciones_metricas']))
