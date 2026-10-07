"""Lectura integral CSV: estructura, filas exactas repetidas y conservación proyectada.

SHA-256 por fila lógica completa para duplicados exactos; no reemplaza un ID individual.
Proyección compartida solo como prueba de pertenencia multiconjunto, no identidad personal.
Los hashes de fila y cualquier valor individual se conservan únicamente en /tmp.
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, tempfile, re
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'auditoria/evidencia'
KEYS=['periodo','cole_cod_depto_ubicacion','cole_cod_mcpio_ubicacion','estu_cod_reside_depto','estu_cod_reside_mcpio','estu_cod_depto_presentacion','estu_cod_mcpio_presentacion','estu_grado','estu_fechanacimiento','estu_genero','punt_global','punt_ingles','punt_lectura_critica','punt_matematicas','punt_sociales_ciudadanas','punt_c_naturales']
NUM=set(KEYS)-{'estu_fechanacimiento','estu_genero'}
def digest(values):return hashlib.sha256(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode()).digest()
def normal(v,c):
    v=v.strip()
    if c in NUM and re.fullmatch(r'[+-]?\d+(?:\.0+)?',v): return str(int(v.split('.')[0]))
    if c=='estu_fechanacimiento':
        parts=v.split('/')
        if len(parts)==3: return '/'.join([parts[0].zfill(2),parts[1].zfill(2),parts[2]])
    return v
def scan(f,sep):
    exact=[]; projected={}; widths=Counter(); tab_rows=0; period_counts=Counter()
    with f.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.reader(stream,delimiter=sep); header=[c.strip().lower() for c in next(reader)]; idx=[header.index(c) for c in KEYS]
        for row in reader:
            widths[len(row)]+=1
            if len(row)!=len(header):continue
            tab_rows+=any('\t' in v for v in row)
            exact.append(digest(row))
            vals=[normal(row[i],c) for c,i in zip(KEYS,idx)]
            p=vals[0]; period_counts[p]+=1
            projected.setdefault(p,[]).append(digest(vals))
    a=np.array(exact,dtype='S32'); unique,counts=np.unique(a,return_counts=True)
    report={'archivo':str(f.relative_to(ROOT)),'columnas':len(header),'filas':sum(widths.values()),'anchos':json.dumps(dict(widths)),'filas_ancho_incorrecto':sum(v for k,v in widths.items() if k!=len(header)),'filas_con_tab_en_campos':int(tab_rows),'filas_repetidas_exactas_exceso':int(np.maximum(counts-1,0).sum()),'grupos_repetidos_exactos':int((counts>1).sum()),'metodo':'SHA-256 de lista de campos CSV completos; no prueba unicidad de persona; hashes no publicados'}
    return report,{p:np.array(v,dtype='S32') for p,v in projected.items()}
def main():
    reports=[]; sources={}
    for f in sorted((ROOT/'Datos anteriores a la limpieza').glob('*.csv')):
        r,p=scan(f,';');reports.append(r);sources.update(p);print(f.name,r['filas_repetidas_exactas_exceso'],flush=True)
    r,final=scan(ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv',',');reports.append(r)
    rows=[]
    for p,a in final.items():
        if p not in sources:
            rows.append({'periodo':p,'filas_final':len(a),'filas_fuente':None,'no_en_fuente_exceso_multiconjunto':None,'estado':'fuente periódica ausente'});continue
        ua,ca=np.unique(a,return_counts=True);ub,cb=np.unique(sources[p],return_counts=True)
        pos=np.searchsorted(ub,ua);found=(pos<len(ub));safe=np.minimum(pos,len(ub)-1); found &= ub[safe]==ua
        available=np.where(found,cb[safe],0)
        unmatched=int(np.maximum(ca-available,0).sum())
        rows.append({'periodo':p,'filas_final':len(a),'filas_fuente':len(sources[p]),'no_en_fuente_exceso_multiconjunto':unmatched,'estado':('coincidencia en proyección compartida' if unmatched==0 else 'proyección con diferencias no resueltas')+'; no prueba identidad ni filtros iniciales'})
    pd.DataFrame(reports).to_csv(OUT/'estructura_duplicados.csv',index=False)
    pd.DataFrame(rows).to_csv(OUT/'conservacion_registros.csv',index=False)
    print('Cierre',r,flush=True)
if __name__=='__main__': main()
