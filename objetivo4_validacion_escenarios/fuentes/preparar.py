"""Agregación focal de fuentes locales; no datos individuales en salidas."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,json,re,unicodedata,time,sys,hashlib
sys.dont_write_bytecode=True
import numpy as np
import pandas as pd
import openpyxl
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parent;OUT=HERE/'preparacion'
YEARS=[2018,2019,2021,2022,2023,2024,2025]
SCORES=['punt_global','punt_matematicas','punt_lectura_critica','punt_c_naturales','punt_sociales_ciudadanas','punt_ingles']
FIELDS=['periodo','estu_estudiante','estu_privado_libertad','estu_grado','cole_cod_depto_ubicacion','cole_naturaleza','cole_area_ubicacion','desemp_matematicas']+SCORES
BASE=ROOT/'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def norm(s):return re.sub(r'[^A-Z0-9]+',' ',''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn').upper()).strip()
def dimensions(base):
    names={norm(r.departamento):r.codigo_departamento for r in base.itertuples()}
    names.update({'BOGOTA': '11','BOGOTA D C':'11','SAN ANDRES Y PROVIDENCIA':'88'})
    labels=['Educación','Niñez y Juventud','Trabajo','Salud','Vivienda'];rows=[];books=[]
    for last in [2024,2025]:
        path=ROOT/f'Fuente del IPM/anex-PMultidimensional-Departamental-{last}.xlsx'
        books.append({'archivo':str(path.relative_to(ROOT)),'sha256':sha(path)})
        w=openpyxl.load_workbook(path,read_only=True,data_only=True);sheet=w['Contribuciones IA_IPM'];dept=None;ys={}
        for row in sheet.iter_rows():
            vals=[c.value for c in row];first=vals[0]
            if isinstance(first,str) and 'Contribuciones a la Incidencia' in first:
                found=[names[norm(part)] for part in first.splitlines() if norm(part) in names]
                dept=found[0] if found else None
            if first=='Dimensión':
                ys={int(str(v)[:4]):i for i,v in enumerate(vals) if re.fullmatch(r'20\d\d\**',str(v))}
            if first in labels and dept:
                for year,i in ys.items():
                    if (last==2024 and year in YEARS[:-1]) or (last==2025 and year==2025):
                        rows.append(dict(codigo_departamento=dept,anio=year,dimension='contrib_'+norm(first).replace(' ','_').lower(),valor=float(vals[i]),archivo=str(path.relative_to(ROOT)),hoja=sheet.title,celda=row[i].coordinate))
        w.close()
    ledger=pd.DataFrame(rows);assert len(ledger)==231*5 and not ledger.duplicated(['codigo_departamento','anio','dimension']).any()
    pivot=ledger.pivot(index=['codigo_departamento','anio'],columns='dimension',values='valor').reset_index()
    dc=[c for c in pivot if c.startswith('contrib_')]
    assert len(dc)==5 and pivot[dc].ge(0).all().all() and pivot[dc].le(100).all().all()
    sums=pivot[dc].sum(axis=1);assert sums.sub(100).abs().max()<=.31,'contribuciones fuera de redondeo'
    ledger.to_csv(OUT/'contribuciones_celdas.csv',index=False)
    return pivot,books,{'suma_min':float(sums.min()),'suma_max':float(sums.max()),'unidad':'porcentaje de contribución a incidencia ajustada, no incidencia por dimensión'}
def run():
    OUT.mkdir(exist_ok=True);start=time.monotonic();agg=defaultdict(Counter);cat=Counter();controls=[];inputs={str(BASE.relative_to(ROOT)):sha(BASE)}
    paths=[p for p in sorted((ROOT/'raw_data').glob('*.txt')) if int(re.search(r'20\d{2}',p.name).group()) in YEARS]
    assert len(paths)==14
    for path in paths:
        per=re.search(r'20\d{3}',path.name).group();year=int(per[:4]);inputs[str(path.relative_to(ROOT))]=sha(path)
        with path.open(encoding='utf-8-sig') as f:line=f.readline()
        sep=max([';','\t',','],key=line.count);h=next(csv.reader([line],delimiter=sep));h=[v.strip().lower() for v in h]
        assert set(FIELDS)<=set(h),(path,set(FIELDS)-set(h))
        received=kept=bad_level=0
        for d in pd.read_csv(path,sep=sep,encoding='utf-8-sig',dtype=str,usecols=lambda c:c.strip().lower() in FIELDS,chunksize=100000,keep_default_na=False):
            if time.monotonic()-start>1800:raise TimeoutError('Preparación incompleta')
            d.columns=d.columns.str.strip().str.lower();received+=len(d)
            assert d.periodo.str.strip().eq(per).all(),'periodo distinto'
            nums={c:pd.to_numeric(d[c].str.replace(',','.',regex=False),errors='coerce') for c in SCORES}
            code=pd.to_numeric(d.cole_cod_depto_ubicacion,errors='coerce');grade=pd.to_numeric(d.estu_grado,errors='coerce')
            keep=d.estu_estudiante.str.strip().str.upper().eq('ESTUDIANTE')&~d.estu_privado_libertad.str.strip().str.upper().eq('S')&grade.eq(11)&code.notna()
            for x in nums.values():keep&=x.notna()&x.gt(0)
            q=d[keep].copy();q['code']=code[keep].astype(int).astype(str).str.zfill(2);q['global']=nums['punt_global'][keep]
            q['math']=nums['punt_matematicas'][keep];q['level']=pd.to_numeric(q.desemp_matematicas,errors='coerce')
            calc=np.searchsorted([35,50,70],q['math'],side='left')+1
            assert q.level.isin([1,2,3,4]).all(),'nivel faltante/no válido'
            bad_level+=int((q.level.to_numpy()!=calc).sum());q['success']=q.level.ge(3).astype(int)
            q['nature']=q.cole_naturaleza.str.strip().str.upper();q['area']=q.cole_area_ubicacion.str.strip().str.upper().replace({'URBANA':'URBANO'})
            for col,valid in [('nature',['OFICIAL','NO OFICIAL']),('area',['URBANO','RURAL'])]:
                for value,n in q[col].value_counts(dropna=False).items():cat[(col,value)]+=int(n)
                assert q[col].isin(valid).all(),f'categoría desconocida {col}: {q.loc[~q[col].isin(valid),col].value_counts().to_dict()}'
            kept+=len(q)
            for c,g in q.groupby('code'):
                a=agg[(c,year)];a['n']+=len(g);a['sum_global']+=float(g['global'].sum());a['official']+=int(g.nature.eq('OFICIAL').sum());a['urban']+=int(g.area.eq('URBANO').sum());a['math34']+=int(g.success.sum())
        assert bad_level==0,'nivel Matemáticas contradice límites auditados'
        controls.append(dict(archivo=str(path.relative_to(ROOT)),periodo=per,recibidos=received,elegibles=kept,niveles_discrepantes=bad_level))
        print(json.dumps(controls[-1],ensure_ascii=False),flush=True)
    base=pd.read_csv(BASE,dtype={'codigo_departamento':str},float_precision='round_trip')
    base['codigo_departamento']=base.codigo_departamento.str.zfill(2)
    assert not base.duplicated(['codigo_departamento','anio']).any()
    added=pd.DataFrame([dict(codigo_departamento=c,anio=y,**v) for (c,y),v in agg.items()])
    joined=base.merge(added,on=['codigo_departamento','anio'],validate='one_to_one');assert len(joined)==231
    assert np.array_equal(joined.n_punt_global,joined.n)
    deltas=joined.sum_global/joined.n-joined.prom_punt_global
    assert deltas.abs().max()<1e-9,'media global no conserva fuente'
    joined['prop_oficial']=joined.official/joined.n;joined['prop_urbana']=joined.urban/joined.n;joined['mat34']=100*joined.math34/joined.n
    joined['tiempo']=joined.anio-2018;joined['indicador2021']=joined.anio.eq(2021).astype(int)
    dims,books,checkdims=dimensions(base)
    joined=joined.merge(dims,on=['codigo_departamento','anio'],validate='one_to_one').sort_values(['anio','codigo_departamento'])
    joined.to_csv(OUT/'panel_enriquecido.csv',index=False,float_format='%.17g')
    pd.DataFrame(controls).to_csv(OUT/'controles_raw.csv',index=False)
    pd.DataFrame([dict(campo=k[0],categoria=k[1],n=v) for k,v in cat.items()]).to_csv(OUT/'categorias.csv',index=False)
    inputs.update({b['archivo']:b['sha256'] for b in books})
    result=dict(aprobado=True,fuentes_sha256=inputs,filas=231,media_delta_max=float(deltas.abs().max()),contribuciones=checkdims,seconds=time.monotonic()-start,python=sys.version,personales_guardados=False)
    (OUT/'CONTROL_PREPARACION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='fuentes_sha256'},ensure_ascii=False))
    return joined
if __name__=='__main__':run()
