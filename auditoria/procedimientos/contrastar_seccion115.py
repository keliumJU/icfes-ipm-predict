"""Control de la construcción alternativa DESCRITA en ACA2 pp.115–117.

Solo intenta reproducir una afirmación previa. Las exclusiones de 2021/Bogotá
se aplican únicamente a este contraste rotulado, NO al resultado principal,
ni a una base validada. No selecciona variables ni entrena modelos.
"""
from pathlib import Path
from collections import Counter
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'auditoria/evidencia'
def main():
    accum={}
    for df in pd.read_csv(ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv',usecols=['ESTU_GRADO','ESTU_COD_DEPTO_PRESENTACION','PERIODO','PUNT_GLOBAL'],dtype=str,chunksize=100000):
        d=pd.to_numeric(df.ESTU_COD_DEPTO_PRESENTACION,errors='coerce')
        year=pd.to_numeric(df.PERIODO,errors='coerce').astype('Int64').astype(str).str[:4].astype(int)
        grade=pd.to_numeric(df.ESTU_GRADO,errors='coerce');score=pd.to_numeric(df.PUNT_GLOBAL,errors='coerce')
        keep=grade.eq(11)&year.isin([2018,2019,2022,2023,2024])&d.notna()&score.notna()
        t=pd.DataFrame({'codigo_departamento':d[keep],'anio':year[keep],'puntaje':score[keep]})
        for key,g in t.groupby(['codigo_departamento','anio']):
            a=accum.setdefault((int(key[0]),int(key[1])),Counter());a['suma']+=g.puntaje.sum();a['n']+=len(g)
    ag=pd.DataFrame([{'codigo_departamento':c,'anio':y,'n':a['n'],'media':a['suma']/a['n']} for (c,y),a in accum.items()])
    ipm=pd.read_csv(ROOT/'Fuente del IPM/ipm_departamental_limpio_sin_2020.csv',sep=';')
    merged=ag.merge(ipm,on=['codigo_departamento','anio'],how='left',indicator=True,validate='one_to_one')
    # Bogotá is NOT missing from the actual IPM; exclusion is a hypothesis reproducing the prose only.
    hypothetical=merged[merged.codigo_departamento.ne(11)&merged.ipm.notna()].copy()
    means=hypothetical.groupby('codigo_departamento').mean(numeric_only=True)
    published={
        'Inadecuada eliminacion de excretas':(-.815,-.791),'Sin acceso a fuente de agua mejorada':(-.809,-.788),'ipm':(-.740,-.709),'Rezago escolar':(-.736,-.666),'Material inadecuado de paredes exteriores':(-.713,-.670),'Hacinamiento critico':(-.690,-.629),'Barreras a servicios para cuidado de la primera infancia':(-.663,-.561),'Analfabetismo':(-.642,-.606),'Material inadecuado de pisos':(-.531,-.519),'Trabajo informal':(-.502,-.491),'Bajo logro educativo':(-.449,-.442),'Inasistencia escolar':(-.446,-.408),'Desempleo de larga duracion':(-.381,-.298),'Barreras de acceso a servicios de salud':(.051,-.001),'Sin aseguramiento en salud':(.066,-.003),'Trabajo infantil':(.109,.071)}
    rows=[]
    for c,(between,cells) in published.items():
        b=means[c].corr(means.media);s=hypothetical[c].corr(hypothetical.media)
        rows.append({'variable':c,'r_entre_departamentos_declarada':between,'r_entre_departamentos_control':b,'r_celdas_declarada':cells,'r_celdas_control':s,'coincide_entre_3decimales':abs(round(b,3)-between)<1e-10,'coincide_celdas_3decimales':abs(round(s,3)-cells)<1e-10,'condicion':'hipótesis de filtros de p115; no prueba fuente histórica ni valida exclusiones'})
    result=pd.DataFrame(rows);result.to_csv(OUT/'cotejo_tabla12_hipotesis.csv',index=False)
    summary={'celdas_presentacion_cinco_anios_con_ipm_actual':int(merged.ipm.notna().sum()),'celdas_si_se_retira_bogota_para_contrastar_texto':len(hypothetical),'bogota_ipm_actual_faltante':int(merged[merged.codigo_departamento.eq(11)].ipm.isna().sum()),'coincidencias_entre':int(result.coincide_entre_3decimales.sum()),'coincidencias_celdas':int(result.coincide_celdas_3decimales.sum()),'variables':len(result),'exclusiones_no_adoptadas_para_base_principal':True}
    (OUT/'resumen_seccion115.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
