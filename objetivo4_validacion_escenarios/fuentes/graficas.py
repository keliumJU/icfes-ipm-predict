"""Figuras calculadas exclusivamente de predicciones verificadas."""
from pathlib import Path
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from modelos import HERE,OUT,metrics

def run():
    dest=HERE/'figuras';dest.mkdir(exist_ok=True)
    p=pd.read_csv(OUT/'predicciones.csv');m=pd.read_csv(OUT/'metricas.csv',dtype={'anio':str})
    q=m.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global" and anio=="conjunto"').set_index('spec')
    names=['base','ipm','componentes','promedio_territorial','persistencia'];labels=['Composición y tiempo','Además IPM','Dimensiones y tasas','Promedio territorial','Último puntaje disponible']
    for name in names:
        z=p.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global" and spec==@name')
        assert abs(metrics(z.observed,z.predicted)['MAE']-q.loc[name,'MAE'])<1e-10
    q.loc[names].reset_index().to_csv(dest/'datos_errores.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,4));vals=q.loc[names,'MAE'].to_numpy();ax.barh(labels,vals,color=['#64748b','#2563eb','#0891b2','#94a3b8','#475569']);ax.invert_yaxis();ax.set_xlabel('Error absoluto medio, puntos del puntaje global');ax.set_title('Entrenamiento hasta 2023 · evaluación 2024–2025')
    for i,v in enumerate(vals):ax.text(v+.08,i,f'{v:.2f}',va='center')
    ax.set_xlim(0,max(vals)*1.2);fig.tight_layout();fig.savefig(dest/'errores_2024_2025.png',dpi=180);plt.close(fig)
    s=pd.read_csv(OUT/'escenarios.csv');a=s[s.admitido & s.reduccion_pp.gt(0)].copy()
    assert a.prediccion_escenario.notna().all();np.testing.assert_allclose(a.diferencia,a.prediccion_escenario-a.prediccion_base,atol=1e-10)
    fig,ax=plt.subplots(figsize=(8,2.4))
    if len(a):
        summary=a.groupby('escenario').diferencia.agg(['mean','min','max','size'])
        summary.to_csv(dest/'datos_escenarios.csv')
        labels=[f'{i} (n={int(r["size"])})' for i,r in summary.iterrows()]
        ax.barh(labels,summary['mean'],color='#2563eb',height=.35);ax.errorbar(summary['mean'],range(len(summary)),xerr=np.vstack([summary['mean']-summary['min'],summary['max']-summary['mean']]),fmt='none',ecolor='#475569',capsize=4)
        ax.set_ylim(-.6,len(summary)-.4)
        ax.invert_yaxis();ax.axvline(0,color='gray',lw=.8);ax.set_xlabel('Diferencia media; líneas: mínimo–máximo admitidos')
    else:ax.text(.5,.5,'Ningún escenario supera los controles de soporte',ha='center',va='center',transform=ax.transAxes)
    ax.set_title('Escenarios admitidos · cambios condicionales, no causales');fig.tight_layout();fig.savefig(dest/'escenarios_admitidos.png',dpi=180);plt.close(fig)
    return [str(p.relative_to(HERE)) for p in sorted(dest.glob('*.png'))]
