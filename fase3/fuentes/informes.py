"""Interpretaciones y figuras derivadas exclusivamente de salidas actuales."""
from comun import OUT,read,cfg
import pandas as pd

def resumen_desarrollo():
    t=pd.read_csv(OUT/'comparacion_desarrollo.csv');f=read('congelacion.json')
    best=t.sort_values('mae').groupby('familia',sort=False).head(1)
    print('Mejor MAE bruto por familia (resumen descriptivo, no regla de selección):')
    print(best[['familia','id','mae','rmse','sesgo','r2']].to_string(index=False))
    g=t[t.id==f['ganador_global']].iloc[0]
    minimum=t.mae.min()
    print(f"Ganador congelado: {g.id}, {int(g.n_entradas)} entradas; MAE {g.mae:.6f}, RMSE {g.rmse:.6f}. Mínimo bruto {minimum:.6f}; diferencia {g.mae-minimum:.6f} puntos. La tolerancia y el orden fijados explican diferencias entre ranking bruto y selección.")
    print('Ganadores por especificación con referencia media común:',f['ganadores_especificacion'])
    refs=t[t.familia.isin(['media','ols'])]
    for family in ('ridge','random_forest','gradient_boosting'):
        b=t[t.familia==family].mae.min()
        better=refs[refs.mae<b]
        print(f"Desarrollo: mejor {family} MAE={b:.6f}; referencias con MAE menor: {', '.join(better.id) or 'ninguna'}. Comparación descriptiva tras búsqueda, no independencia estadística.")
    print('Candidatos completos:',len(t),'; fallos registrados:',len(read('fallos.json')),'; advertencias:',len(read('advertencias_desarrollo.json')))

def resumen_reevaluacion():
    t=pd.read_csv(OUT/'metricas_reevaluacion.csv',dtype={'periodo':str});f=read('congelacion.json');gid=f['ganador_global']
    for year in ('2023','2024','conjunto'):
        part=t[t.periodo==year];g=part[part.id==gid].iloc[0]
        print(f"Ganador {gid}, {year}: MAE {g.mae:.6f}, RMSE {g.rmse:.6f}, sesgo {g.sesgo:.6f}, R² {g.r2:.6f}. ΔMAE frente a media {g.delta_mae_media:.6f}.")
        refs=part[part.id.str.startswith('ols_') | (part.id=='media')]
        better=refs[refs.mae<g.mae]
        print('Referencias que superan al ganador en este conjunto:',', '.join(better.id) or 'ninguna','; no se cambia la selección.')
    print('Estas son reevaluaciones temporales actuales, no prueba inédita ni reproducción de métricas históricas. No hubo actualización con 2023, reselección ni interpretación causal.')

def figura():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    t=pd.read_csv(OUT/'metricas_reevaluacion.csv',dtype={'periodo':str});gid=read('congelacion.json')['ganador_global']
    fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
    for mid in dict.fromkeys([gid,'media','ols_ipm','ols_tasas','ols_ambas']):
        part=t[(t.id==mid)&t.periodo.isin(['2023','2024'])].sort_values('periodo')
        ax.plot(part.periodo,part.mae,'o-',label=mid)
    ax.set(xlabel='Año reevaluado (mismo ajuste hasta 2022)',ylabel='MAE, puntos Saber 11',title='Reevaluación temporal: ganador congelado y referencias')
    ax.legend(fontsize=8);ax.grid(alpha=.25);fig.savefig(OUT/'mae_temporal.png',dpi=160);plt.close(fig)
