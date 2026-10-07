"""Recomprobación de afirmaciones descriptivas; no selección ni entrenamiento de modelos."""
from pathlib import Path
from collections import Counter
import json, subprocess, ast
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'auditoria/evidencia'
SCORES=['PUNT_GLOBAL','PUNT_MATEMATICAS','PUNT_LECTURA_CRITICA','PUNT_C_NATURALES','PUNT_SOCIALES_CIUDADANAS','PUNT_INGLES']
LIMITS={'MATEMATICAS':[35,50,70],'LECTURA_CRITICA':[35,50,65],'C_NATURALES':[40,55,70],'SOCIALES_CIUDADANAS':[40,55,70]}

def main():
    ag=pd.read_csv(OUT/'agregados_Saber_11_Listo_2018_2024.csv')
    ipm=pd.read_csv(ROOT/'Fuente del IPM/ipm_departamental_limpio_sin_2020.csv',sep=';')
    grade=ag[ag.subconjunto.eq('grado11_control')].copy()
    # Recover unrounded means from summed scores and their own counts, not rounded cell means.
    for c in SCORES:grade['prom_'+c.lower()]=grade['sum_'+c.lower()]/grade['n_'+c.lower()]
    joined=grade.merge(ipm,on=['codigo_departamento','anio'],validate='one_to_one')
    yearly=[]
    for y,g in joined.groupby('anio'):
        yearly.append({'anio':y,'filas_grado11_actual':int(g.n_estudiantes_saber.sum()),'celdas':len(g),'ipm_media':g.ipm.mean(),'media_global_simple':g.prom_punt_global.mean(),'de_global_simple':g.prom_punt_global.std(ddof=1),'media_global_estudiantes':g.sum_punt_global.sum()/g.n_punt_global.sum(),'min_n':g.n_estudiantes_saber.min(),'r_ipm_global':g.ipm.corr(g.prom_punt_global)})
    pd.DataFrame(yearly).to_csv(OUT/'contraste_tabla7.csv',index=False)
    changes=joined.pivot(index='codigo_departamento',columns='anio',values=['ipm','prom_punt_global'])
    r_changes=(changes['ipm'][2024]-changes['ipm'][2018]).corr(changes['prom_punt_global'][2024]-changes['prom_punt_global'][2018])
    before=joined[joined.anio.eq(2018)].set_index('codigo_departamento').sort_index();middle=joined[joined.anio.eq(2019)].set_index('codigo_departamento').sort_index();pandemic=joined[joined.anio.eq(2021)].set_index('codigo_departamento').sort_index();after=joined[joined.anio.eq(2024)].set_index('codigo_departamento').sort_index()
    summary={'filas_grado11':int(grade.n_estudiantes_saber.sum()),'filas_excluidas_por_grado':int(ag.loc[ag.subconjunto.eq('recibido'),'n_estudiantes_saber'].sum()-grade.n_estudiantes_saber.sum()),'r_ipm_global_198':joined.ipm.corr(joined.prom_punt_global),'r_cambios_2018_2024_33':r_changes,'departamentos_bajan_2018_2019':int((middle.prom_punt_global<before.prom_punt_global).sum()),'departamentos_suben_2021_2024':int((after.prom_punt_global>pandemic.prom_punt_global).sum()),'condicion':'reproducción interna desde consolidado suministrado; no valida origen ni cadena previa'}
    # Exact consistency of all four reported performance levels, all 3,401,100 rows.
    counters=Counter(); pieces=[];inse=Counter(); global_formula=Counter()
    cols=['PERIODO','COLE_COD_DEPTO_UBICACION','ESTU_GRADO','ESTU_PRIVADO_LIBERTAD','ESTU_ESTUDIANTE','ESTU_INSE_INDIVIDUAL']+SCORES+['DESEMP_'+c for c in LIMITS]
    for df in pd.read_csv(ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv',usecols=cols,dtype=str,chunksize=100_000):
        for c in SCORES:df[c]=pd.to_numeric(df[c],errors='coerce')
        df['__periodo']=pd.to_numeric(df.PERIODO,errors='raise').astype(int)
        for area,limits in LIMITS.items():
            actual=pd.to_numeric(df['DESEMP_'+area],errors='coerce')
            expected=1+sum(df['PUNT_'+area].gt(c).astype(int) for c in limits)
            bad=actual.isna()|actual.ne(expected)
            for per,idx in df.groupby('__periodo').groups.items():
                counters[(per,area,'comparaciones')]+=len(idx);counters[(per,area,'discrepancias')]+=int(bad.loc[idx].sum())
        # The mathematical global formula is an extra diagnostic; differences may require ICFES exceptions.
        formula=(3*sum(df[c] for c in SCORES[1:5])+df.PUNT_INGLES)*5/13
        formula=np.floor(formula+0.5)
        for per,idx in df.groupby('__periodo').groups.items():global_formula[per]+=int(df.PUNT_GLOBAL.loc[idx].ne(formula.loc[idx]).sum())
        v=pd.to_numeric(df.ESTU_INSE_INDIVIDUAL,errors='coerce');inse['nulos']+=int(v.isna().sum());inse['mayores100_exploratorio_no_rango_oficial']+=int(v.gt(100).sum())
        inse['max']=max(inse['max'],v.max());inse['min']=min(inse.get('min',float('inf')),v.min())
        # Reconstruct ONLY 20211 for direct comparison to anomalous historical 2021.
        d=df[df.__periodo.eq(20211)].copy()
        if len(d):
            d['codigo_departamento']=pd.to_numeric(d.COLE_COD_DEPTO_UBICACION)
            pieces.append(d.groupby('codigo_departamento')[SCORES].agg(['sum','count']))
    pd.DataFrame([{'periodo':p,'prueba':a,'control':c,'n':n} for (p,a,c),n in counters.items()]).to_csv(OUT/'niveles_desempeno.csv',index=False)
    pd.DataFrame([{'periodo':p,'discrepancias_formula_global':n} for p,n in global_formula.items()]).to_csv(OUT/'formula_global.csv',index=False)
    (OUT/'inse_exploratorio.json').write_text(json.dumps(dict(inse),indent=2))
    source=pd.concat(pieces).groupby(level=0).sum(); hist=pd.read_csv(ROOT/'panel_departamento_anio_unido.csv',sep=';').query('anio==2021').set_index('codigo_departamento')
    ledger=[]
    for code,row in source.iterrows():
        for c in SCORES:
            count=int(row[(c,'count')]); mean=round(float(row[(c,'sum')])/count,2)
            ledger.append({'codigo_departamento':code,'variable':c,'n_20211_consolidado':count,'n_panel2021':hist.loc[code,'n_'+c.lower()],'prom_20211_consolidado':mean,'prom_panel2021':hist.loc[code,'prom_'+c.lower()],'delta_n':count-hist.loc[code,'n_'+c.lower()],'delta_prom':mean-hist.loc[code,'prom_'+c.lower()]})
    pd.DataFrame(ledger).to_csv(OUT/'panel2021_vs_periodo20211.csv',index=False)
    summary['comparaciones_niveles']=sum(v for k,v in counters.items() if k[2]=='comparaciones');summary['discrepancias_niveles']=sum(v for k,v in counters.items() if k[2]=='discrepancias')
    (OUT/'resumen_tesis.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary,ensure_ascii=False))
    # Dependency inventory records code locations without importing or running supplied scripts.
    deps=[]
    for folder in ['Scripts de preparacion','Scripts de análisis y modelos']:
        for path in sorted((ROOT/folder).glob('*.py')):
            tree=ast.parse(path.read_text(encoding='utf-8-sig'))
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):mods=[a.name for a in node.names]
                elif isinstance(node,ast.ImportFrom):mods=[node.module]
                else:continue
                for mod in mods:deps.append({'archivo':str(path.relative_to(ROOT)),'linea':node.lineno,'modulo':mod,'ejecutado':'no'})
    pd.DataFrame(deps).to_csv(OUT/'dependencias_scripts.csv',index=False)

if __name__=='__main__': main()
