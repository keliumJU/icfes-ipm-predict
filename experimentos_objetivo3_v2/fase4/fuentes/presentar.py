"""Tablas comparativas y gráficos descriptivos, sin modelos adicionales."""
import sys
sys.dont_write_bytecode=True
from revision import *
import os,tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'icfes-fase4-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def presentar(met,comp,pair,out=F4/'resultados'):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 refs=[]
 main=met[met.procedimiento=='procedimiento_v2']
 for ident in ('media','ols_ipm_00','ols_tasas_00','ols_ambas_00','referencia_v1'):
  q=main.merge(met[met.procedimiento==ident],on=['periodo','ambito','grupo'],suffixes=('_v2','_referencia'),validate='one_to_one')
  q['referencia']=ident
  for k in ('mae','rmse','sesgo','r2'):q['delta_'+k]=q[k+'_v2']-q[k+'_referencia']
  refs.append(q)
 save(pd.concat(refs,ignore_index=True),out/'comparaciones_referencias.csv')
 chosen=comp[(comp.periodo=='2021-2025')&(comp.procedimiento=='procedimiento_v2')&(comp.ambito.isin(['anual','territorial']))]
 save(chosen,out/'deterioros_v2.csv')
 figures=[]
 fig,ax=plt.subplots(figsize=(9,4.5))
 for role,label in [('procedimiento_v2','v2'),('referencia_v1','v1 fija reentrenada'),('media','Media'),('ols_tasas_00','OLS tasas'),('ols_ambas_00','OLS ambas'),('ols_ipm_00','OLS IPM')]:
  q=met[(met.periodo=='2021-2025')&(met.ambito=='anual')&(met.procedimiento==role)].sort_values('grupo');ax.plot(q.grupo,q.mae,marker='o',label=label)
 ax.set(xlabel='Año externo',ylabel='MAE (puntos)',title='Errores externos por año, igual peso por territorio');ax.legend(ncol=3);fig.tight_layout();path=out/'mae_anual.png';fig.savefig(path,dpi=160);plt.close(fig);figures.append(path)
 q=chosen[chosen.ambito=='territorial'].sort_values('delta_mae');fig,ax=plt.subplots(figsize=(9,9));ax.barh(q.grupo,q.delta_mae,color=['#b53d38' if x>0 else '#247d89' for x in q.delta_mae]);ax.axvline(0,color='black',lw=.7);ax.set(xlabel='MAE v2 − MAE v1 (puntos); positivo = deterioro',ylabel='Código territorio',title='Comparación territorial en 2021–2025');fig.tight_layout();path=out/'delta_mae_territorial.png';fig.savefig(path,dpi=160);plt.close(fig);figures.append(path)
 fig,axes=plt.subplots(1,3,figsize=(12,4))
 for ax,col,label in zip(axes,['delta_error_firmado','delta_error_absoluto','delta_error_cuadratico'],['Error firmado (puntos)','Error absoluto (puntos)','Error cuadrático (puntos²)']):
  ax.hist(pair[col],bins=20,color='#247d89');ax.axvline(0,color='#b53d38');ax.set(xlabel='v2 − v1: '+label,ylabel='Territorio-año')
 fig.suptitle('165 diferencias emparejadas; descriptivas, sin prueba de significancia');fig.tight_layout();path=out/'diferencias_emparejadas.png';fig.savefig(path,dpi=160);plt.close(fig);figures.append(path)
 return figures
if __name__=='__main__':
 m,c,p,r=revisar();presentar(m,c,p);print('Tablas y tres gráficos calculados desde predicciones guardadas.')
