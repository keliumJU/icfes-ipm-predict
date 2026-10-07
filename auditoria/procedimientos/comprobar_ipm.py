"""Cotejo exhaustivo de IPM local y anexo XLSX; lectura, sin reescribir fuentes."""
from pathlib import Path
import json, unicodedata, re
import pandas as pd
import openpyxl

ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'auditoria/evidencia'
BOOK='Fuente del IPM/anex-PMultidimensional-Departamental-2024.xlsx'
YEARS=[2018,2019,2021,2022,2023,2024]
def norm(x):
    s=''.join(c for c in unicodedata.normalize('NFD',str(x)) if unicodedata.category(c)!='Mn')
    return re.sub(r'[^A-Z0-9]+',' ',s.upper()).strip()

def main():
    w=openpyxl.load_workbook(ROOT/BOOK,read_only=True,data_only=True)
    ipm=pd.read_csv(ROOT/'Fuente del IPM/ipm_departamental_limpio_sin_2020.csv',sep=';')
    names={norm(r.departamento):int(r.codigo_departamento) for r in ipm.itertuples()}
    names['BOGOTA D C']=11; names['BOGOTA']=11
    names['SAN ANDRES Y PROVIDENCIA']=88
    cols={norm(c):c for c in ipm.columns if c not in ['codigo_departamento','departamento','anio']}
    source={}; extras={}; notes=[]
    for sn in ['IPM_Departamentos','IPM_Variables_Departamento ','Intensidad_IPM','Incidencia_Ajustada_IPM','Contribuciones IA_IPM','IC_IPM']:
        s=w[sn]; dept=None
        for row in s.iter_rows():
            vals=[c.value for c in row]; first=vals[0]
            if isinstance(first,str) and any(t in first for t in ['Fuente:','Nota:','Actualizado','Datos expandidos']):
                notes.append({'archivo':BOOK,'hoja':sn,'celda':row[0].coordinate,'texto':first})
            if sn=='IPM_Departamentos' and norm(first) in names:
                code=names[norm(first)]
                for y,i in zip([2018,2019,2020,2021,2022,2023,2024],[1,4,7,10,13,16,19]):
                    if y in YEARS: source[(code,y,'ipm')]=(vals[i],sn,row[i].coordinate)
            elif sn=='IPM_Variables_Departamento ':
                if norm(first) in names: dept=names[norm(first)]
                var=cols.get(norm(vals[1]))
                if var and dept:
                    for y,i in zip([2018,2019,2020,2021,2022,2023,2024],[2,5,8,11,14,17,20]):
                        if y in YEARS: source[(dept,y,var)]=(vals[i],sn,row[i].coordinate)
            elif sn in ['Intensidad_IPM','Incidencia_Ajustada_IPM'] and norm(first) in names:
                code=names[norm(first)]; var='intensidad' if sn=='Intensidad_IPM' else 'incidencia_ajustada'
                for y,i in zip([2018,2019,2020,2021,2022,2023,2024],range(1,8)):
                    # Incidencia ajustada is stored as a fraction (format 0.000), unlike H and A.
                    if y in YEARS: extras[(code,y,var)]=(vals[i]*100 if var=='incidencia_ajustada' else vals[i],sn,row[i].coordinate)
            elif sn=='Contribuciones IA_IPM':
                if isinstance(first,str) and 'Contribuciones a la Incidencia' in first:
                    for part in first.splitlines():
                        if norm(part) in names: dept=names[norm(part)]
                if first in ['Educación','Niñez y Juventud','Trabajo','Salud','Vivienda'] and dept:
                    for y,i in zip([2018,2019,2020,2021,2022,2023,2024],range(1,8)):
                        if y in YEARS: extras[(dept,y,'contribucion_'+norm(first))]=(vals[i],sn,row[i].coordinate)
            elif sn=='IC_IPM' and norm(first) in names and row[0].row<70:
                code=names[norm(first)]
                for y,start in [(2023,1),(2024,16)]:
                    for k,i in enumerate(range(start,start+5)):
                        extras[(code,y,['ic_estimacion','error_estandar','ic_inferior','ic_superior','cv'][k])]=(vals[i],sn,row[i].coordinate)
    ledger=[]
    for rowno,r in enumerate(ipm.to_dict('records'),2):
        for c in ipm.columns[3:]:
            k=(int(r['codigo_departamento']),int(r['anio']),c)
            v,sn,cell=source.get(k,(None,'',''))
            ledger.append({'codigo_departamento':k[0],'anio':k[1],'variable':c,'valor_csv':r[c],'fila_csv':rowno,'valor_xlsx':v,'hoja':sn,'celda':cell,'diferencia':float(r[c])-float(v) if isinstance(v,(float,int)) else None})
    ledger=pd.DataFrame(ledger); ledger.to_csv(OUT/'cotejo_ipm_celdas.csv',index=False)
    pd.DataFrame(notes).to_csv(OUT/'notas_ipm.csv',index=False)
    pd.DataFrame([{'codigo_departamento':k[0],'anio':k[1],'variable':k[2],'valor':v,'hoja':sn,'celda':cell} for k,(v,sn,cell) in extras.items()]).to_csv(OUT/'controles_ipm_auxiliares.csv',index=False)
    aux=[]
    for r in ipm.to_dict('records'):
        code,y=int(r['codigo_departamento']),int(r['anio']); intensity=extras[(code,y,'intensidad')][0]; adj=extras[(code,y,'incidencia_ajustada')][0]
        contributions=[v[0] for k,v in extras.items() if k[:2]==(code,y) and k[2].startswith('contribucion_')]
        aux.append({'codigo_departamento':code,'anio':y,'h_por_a':r['ipm']*intensity/100,'incidencia_ajustada':adj,'delta_h_a':r['ipm']*intensity/100-adj,'n_dimensiones':len(contributions),'suma_contribuciones':sum(contributions)})
    aux=pd.DataFrame(aux);aux.to_csv(OUT/'identidades_ipm.csv',index=False)
    hist=pd.read_csv(ROOT/'panel_departamento_anio_unido.csv',sep=';')
    joined=hist.merge(ipm,on=['codigo_departamento','anio'],suffixes=('_panel','_csv'),validate='one_to_one')
    paneldiff=[]
    for c in ipm.columns[2:]:
        if c=='anio': continue
        paneldiff.append({'variable':c,'diferencias_panel_csv':int((joined[c+'_panel']-joined[c+'_csv']).abs().gt(1e-10).sum())})
    pd.DataFrame(paneldiff).to_csv(OUT/'cotejo_ipm_panel.csv',index=False)
    summary={'filas_csv':len(ipm),'duplicados_llaves':int(ipm.duplicated(['codigo_departamento','anio']).sum()),'nulos':int(ipm.isna().sum().sum()),'celdas_cotejadas':len(ledger),'celdas_sin_correspondencia':int(ledger.celda.eq('').sum()),'diferencias_numericas':int(ledger.diferencia.abs().gt(1e-10).sum()),'delta_max_h_a':float(aux.delta_h_a.abs().max()),'suma_contribuciones_min':float(aux.suma_contribuciones.min()),'suma_contribuciones_max':float(aux.suma_contribuciones.max()),'contribuciones_no_exactamente100':int(aux.suma_contribuciones.sub(100).abs().gt(1e-10).sum()),'incertidumbre_2024':{'amplitud_media':sum(extras[(c,2024,'ic_superior')][0]-extras[(c,2024,'ic_inferior')][0] for c in sorted(set(ipm.codigo_departamento)))/33,'cv_mayor10':sum(extras[(c,2024,'cv')][0]>10 for c in sorted(set(ipm.codigo_departamento)))},'anio_2020':'excluido en CSV, conservado en XLSX; no se introduce en controles analíticos'}
    (OUT/'resumen_ipm.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
