"""Comprobación de resultados guardados; cero ajustes y sin datos personales."""
from pathlib import Path
import hashlib, json, math, os, sys
sys.dont_write_bytecode = True
os.environ.setdefault('MPLCONFIGDIR', '/tmp/mpl_entrega_tesis')
import numpy as np
import pandas as pd
HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parent
V6 = ROOT/'experimento_final_objetivo3_v6/ejecucion_autorizada'
OUT = HERE/'objetivo3'
LABELS = {'pobreza':'Modelo con pobreza ampliado', 'persistencia':'Persistencia', 'seleccion':'Selección final basada en historia'}
def metrics(observed, predicted):
    a=np.asarray(observed,float);b=np.asarray(predicted,float)
    assert len(a)>0 and a.shape==b.shape and np.isfinite(a).all() and np.isfinite(b).all()
    e=b-a
    return dict(n=len(e),MAE=math.fsum(abs(e))/len(e),RMSE=math.sqrt(math.fsum(e*e)/len(e)),sesgo=math.fsum(e)/len(e))
def verify_inputs():
    spec=json.loads((HERE/'INSUMOS.json').read_text())
    for p,h in spec['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    return {'insumos_verificados':len(spec['sha256']), 'fits_nuevos':0}
def data():
    verify_inputs()
    old=pd.read_csv(ROOT/'auditoria/base_analitica_departamento_anio.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    extended=pd.read_csv(ROOT/'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    keys=['codigo_departamento','anio']
    assert len(old)==198 and len(extended)==231 and not extended.duplicated(keys).any()
    match=old[keys+['prom_punt_global','n_punt_global']].merge(extended[keys+['prom_punt_global','n_punt_global']],on=keys,validate='one_to_one')
    assert len(match)==198
    for col in ['prom_punt_global','n_punt_global']:np.testing.assert_array_equal(match[col+'_x'],match[col+'_y'])
    a=pd.read_csv(ROOT/'experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    a=a[a.procedimiento=='procedimiento_v2'][['codigo_departamento','anio','observado','prediccion']].rename(columns={'codigo_departamento':'code','anio':'year','observado':'observed','prediccion':'pobreza'})
    b=pd.read_csv(V6/'fase3/tablas/errores_completos_6600.csv',dtype={'code':str},float_precision='round_trip')
    parts=[]
    for key,cid in [('persistencia','persistencia'),('seleccion','global_v6')]:
        q=b[b.id==cid][['code','year','observed','predicted']].rename(columns={'predicted':key,'observed':'check_'+key})
        assert len(q)==165 and not q.duplicated(['code','year']).any()
        parts.append(q)
    assert len(a)==165 and not a.duplicated(['code','year']).any()
    for q in parts:a=a.merge(q,on=['code','year'],validate='one_to_one')
    for k in LABELS:
        if k!='pobreza':np.testing.assert_array_equal(a.observed,a['check_'+k])
    assert sorted(a.year.unique())==[2021,2022,2023,2024,2025]
    assert a.groupby('year').size().eq(33).all()
    return a[['code','year','observed',*LABELS]].sort_values(['year','code']).reset_index(drop=True)
def results(frame):
    rows=[]
    for name in LABELS:
        for y in [*sorted(frame.year.unique()),'conjunto']:
            q=frame if y=='conjunto' else frame[frame.year==y]
            rows.append({'modelo':name,'etiqueta':LABELS[name],'anio':str(y),**metrics(q.observed,q[name])})
    t=pd.DataFrame(rows)
    primary=json.loads((V6/'fase3/PRIMARIO.json').read_text())
    for key,expected in [('seleccion',primary['global_MAE']),('persistencia',primary['reference_MAE'])]:
        assert math.isclose(t[(t.modelo==key)&(t.anio=='conjunto')].MAE.iloc[0],expected,abs_tol=1e-12)
    assert math.isclose(t[(t.modelo=='pobreza')&(t.anio=='conjunto')].MAE.iloc[0],4.879557188161031,abs_tol=1e-12)
    q=frame[frame.year<2025];np.testing.assert_array_equal(q.seleccion,q.persistencia)
    return t
def figures(frame,table):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    dest=OUT/'figuras';dest.mkdir(parents=True,exist_ok=True)
    f,ax=plt.subplots(figsize=(8,4))
    annual=table[table.anio!='conjunto']
    for k,color,marker in [('pobreza','#9c493d','o'),('persistencia','#4a6476','s'),('seleccion','#23704b','^')]:
        q=annual[annual.modelo==k];ax.plot(q.anio,q.MAE,label=LABELS[k],color=color,marker=marker,linewidth=1.8)
    ax.set(xlabel='Año evaluado',ylabel='Error absoluto medio (puntos Saber 11)',ylim=(0,None))
    ax.legend(fontsize=9);f.text(.5,.01,'33 territorios por año · mismos pares · igual peso territorio-año',ha='center',fontsize=9)
    f.tight_layout(rect=(0,.04,1,1));f.savefig(dest/'01_error_anual.png',dpi=180);plt.close(f)
    f,ax=plt.subplots(figsize=(8,3.7))
    q=table[table.anio=='conjunto'];bars=ax.barh(q.etiqueta,q.MAE,color=['#9c493d','#4a6476','#23704b'])
    for bar,value in zip(bars,q.MAE):ax.text(value+.06,bar.get_y()+bar.get_height()/2,f'{value:.3f}',va='center')
    ax.set(xlabel='Error absoluto medio (puntos Saber 11)',xlim=(0,float(q.MAE.max())+1));ax.invert_yaxis()
    f.text(.5,.01,'165 pares de 2021–2025 · predicciones guardadas · evaluación exploratoria',ha='center',fontsize=9)
    f.tight_layout(rect=(0,.04,1,1));f.savefig(dest/'02_comparacion_misma_muestra.png',dpi=180);plt.close(f)
    return [str(p.relative_to(HERE)) for p in sorted(dest.glob('*.png'))]
def run():
    d=data();t=results(d);(OUT/'tablas').mkdir(parents=True,exist_ok=True)
    d.to_csv(OUT/'tablas/pares_comparables.csv',index=False,float_format='%.17g')
    t.to_csv(OUT/'tablas/metricas_comparables.csv',index=False,float_format='%.17g')
    paths=figures(d,t)
    ev={'funcion':'analisis.run/data/results/figures','notebook':'02_resultados_y_graficas.ipynb','fits_nuevos':0,'predicciones':'Resultados anteriores; métricas reproducidas en esta entrega','fuentes_sha256':json.loads((HERE/'INSUMOS.json').read_text())['sha256'],'salidas_sha256':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.suffix in ('.csv','.png')}}
    (OUT/'EVIDENCIAS.json').write_text(json.dumps(ev,indent=2,ensure_ascii=False)+'\n')
    return t,paths
