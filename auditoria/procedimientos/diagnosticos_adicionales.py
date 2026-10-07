"""Diagnósticos secundarios íntegros en 20222 y esquema; no corrige observaciones."""
from pathlib import Path
from collections import Counter
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'auditoria/evidencia'
SCORES=['punt_global','punt_matematicas','punt_lectura_critica','punt_c_naturales','punt_sociales_ciudadanas','punt_ingles']
def main():
    counters=Counter()
    for filename,sep,tag in [('Datos anteriores a la limpieza/Examen_Saber_11_20222_limpio.csv',';','periodico_limpio'),('Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv',',','consolidado')]:
        path=ROOT/filename; header=list(pd.read_csv(path,sep=sep,nrows=0).columns)
        names={c.lower():c for c in header};needed=['periodo','estu_grado','estu_discapacidad']+SCORES
        for df in pd.read_csv(path,sep=sep,usecols=[names[c] for c in needed],dtype=str,chunksize=100000):
            df.columns=df.columns.str.lower(); df=df[pd.to_numeric(df.periodo,errors='coerce').eq(20222)].copy()
            for c in SCORES:df[c]=pd.to_numeric(df[c],errors='coerce')
            valid=df[SCORES].notna().all(axis=1)&df[SCORES].gt(0).all(axis=1)
            df=df[valid]; formula=np.floor((3*(df.punt_matematicas+df.punt_lectura_critica+df.punt_c_naturales+df.punt_sociales_ciudadanas)+df.punt_ingles)*5/13+0.5)
            bad=df.punt_global.ne(formula)
            d=df[bad].copy();d['delta']=d.punt_global-formula[bad]
            for (delta,grade,disability),n in d.groupby(['delta','estu_grado','estu_discapacidad'],dropna=False).size().items():counters[(tag,delta,grade,disability)]+=int(n)
    pd.DataFrame([{'archivo':t,'periodo':20222,'delta_global_reportado_menos_formula':delta,'grado':grade,'discapacidad_reportada':dis,'n':n} for (t,delta,grade,dis),n in counters.items()]).to_csv(OUT/'formula_global20222_detalle_agregado.csv',index=False)
    # Trace actual omissions between the 79-column consolidated data and 59-column sources.
    final=pd.read_csv(ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv',nrows=0).columns.str.lower().tolist()
    raw=pd.read_csv(ROOT/'Datos anteriores a la limpieza/Examen_Saber_11_20212_limpio.csv',sep=';',nrows=0).columns.str.lower().tolist()
    pd.DataFrame([{'columna':c,'en_consolidado':c in final,'en_59_columnas':c in raw,'tipo':'derivada' if c in ['depto_analisis','anio'] else 'campo_omitido_sin_procedimiento_suministrado'} for c in sorted(set(final)-set(raw))]).to_csv(OUT/'columnas_omitidas_59.csv',index=False)
    print('Discrepancias formula20222',sum(v for k,v in counters.items() if k[0]=='consolidado'))
if __name__=='__main__':main()
