"""Auditoría de fase 1. Solo lectura de insumos; no entrena ni imputa puntajes.

Ejecutar desde la raíz con Python que tenga pandas, numpy y openpyxl.
Los controles recorren todas las filas, en bloques de 100.000 y columnas necesarias.
Los paneles escritos son evidencia de reproducción, NO bases analíticas validadas.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv, hashlib, json, subprocess, sys, platform, importlib.metadata as metadata
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'auditoria/evidencia'
OUT.mkdir(parents=True, exist_ok=True)
CHUNK = 100_000
SCORES = ['punt_global','punt_matematicas','punt_lectura_critica','punt_c_naturales','punt_sociales_ciudadanas','punt_ingles']
AVERAGES = SCORES + ['percentil_global','estu_inse_individual']
NEEDED = ['periodo','anio','cole_cod_depto_ubicacion','cole_depto_ubicacion','estu_cod_reside_depto','estu_cod_depto_presentacion','estu_depto_reside','estu_depto_presentacion','estu_estudiante','estu_privado_libertad','estu_grado','cole_calendario','estu_consecutivo','cole_bilingue','depto_analisis'] + AVERAGES
OFFICIAL = {5,8,11,13,15,17,18,19,20,23,25,27,41,44,47,50,52,54,63,66,68,70,73,76,81,85,86,88,91,94,95,97,99}

def write(df, name):
    df.to_csv(OUT/name,index=False,encoding='utf-8')

def inventory():
    rows=[]
    folders=['Tesis Vigente','Dataset individual Saber 11','Datos anteriores a la limpieza','Fuente del IPM','Scripts de preparacion','Scripts de análisis y modelos','Resultados Guardados','Entorno de ejecución']
    paths=[ROOT/x for x in ['AGENTS.md','PLAN_OBJETIVO_3.md','prom.pdf','nueva ivestigacion .pdf','panel_departamento_anio_unido.csv','.gitignore']]
    for folder in folders:
        files=sorted((ROOT/folder).rglob('*'))
        paths += [p for p in files if p.is_file()]
        if not files:
            rows.append({'archivo':folder+'/', 'tipo':'directorio vacío','bytes':0,'sha256':'','estado_git':'sin archivos','observacion':'Inspección local; no hay resultados ni versiones históricas aquí'})
    tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))
    for p in paths:
        digest=hashlib.sha256()
        with p.open('rb') as f:
            while block:=f.read(8*1024*1024): digest.update(block)
        rel=str(p.relative_to(ROOT))
        ignored=subprocess.run(['git','check-ignore','-q',rel],cwd=ROOT).returncode==0
        rows.append({'archivo':rel,'tipo':p.suffix,'bytes':p.stat().st_size,'sha256':digest.hexdigest(),'estado_git':'versionado' if rel in tracked else ('ignorado' if ignored else 'no versionado'),'observacion':'Insumo local conservado; nombre no acredita origen ni historial'})
    pd.DataFrame(rows).to_csv(ROOT/'auditoria/inventario_trazabilidad.csv',index=False)
    versions={}
    for p in ['pandas','numpy','openpyxl','pypdf','pdfplumber','scikit-learn','xgboost','matplotlib','seaborn']:
        try: versions[p]=metadata.version(p)
        except metadata.PackageNotFoundError: versions[p]='no instalado en este intérprete'
    (OUT/'entorno_actual.json').write_text(json.dumps({'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'packages':versions,'chunksize':CHUNK,'historico':'Estas versiones son actuales, no históricas verificadas','git_partida':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'fecha_cliente':'2026-10-07'},indent=2,ensure_ascii=False))

def scan(path,sep,tag):
    header=list(pd.read_csv(path,sep=sep,nrows=0,encoding='utf-8-sig').columns)
    cmap={c.strip().lower():c for c in header}
    cols=[cmap[c] for c in NEEDED if c in cmap]
    counts=Counter(); categories=Counter(); stats=Counter(); groups={}; schemas=[]
    for c in NEEDED:
        schemas.append({'archivo':str(path.relative_to(ROOT)),'columna':c,'presente':c in cmap})
    for df in pd.read_csv(path,sep=sep,usecols=cols,dtype=str,encoding='utf-8-sig',chunksize=CHUNK,keep_default_na=False):
        df.columns=[c.strip().lower() for c in df.columns]
        period=df['periodo'].str.strip().str.replace(r'\.0$','',regex=True)
        year=pd.to_numeric(period.str[:4],errors='coerce')
        code=pd.to_numeric(df['cole_cod_depto_ubicacion'],errors='coerce')
        grade=pd.to_numeric(df['estu_grado'],errors='coerce') if 'estu_grado' in df else pd.Series(np.nan,index=df.index)
        numeric={c:pd.to_numeric(df[c].str.strip().str.replace(',','.',regex=False),errors='coerce') for c in AVERAGES if c in df}
        # Missing flags remain unknown for source files lacking columns; never treat this as verified membership.
        est=df['estu_estudiante'].str.strip().str.upper().eq('ESTUDIANTE') if 'estu_estudiante' in df else pd.Series(True,index=df.index)
        lib=~df['estu_privado_libertad'].str.strip().str.upper().eq('S') if 'estu_privado_libertad' in df else pd.Series(True,index=df.index)
        complete=pd.Series(True,index=df.index)
        for c in SCORES: complete &= numeric[c].notna() & numeric[c].gt(0)
        codvalid=code.isin(OFFICIAL)
        globalvalid=numeric['punt_global'].notna() & numeric['punt_global'].gt(0)
        flags={'filas':pd.Series(True,index=df.index),'estudiantes_si_disponible':est,'sin_libertad_secuencial_si_disponible':est&lib,'puntajes_completos_secuencial_si_disponible':est&lib&complete,'grado11_secuencial_si_disponible':est&lib&complete&grade.eq(11),'codigo_no_nulo':code.notna(),'codigo_oficial':codvalid,'global_valido':globalvalid,'todos_puntajes_validos':complete,'grado11':grade.eq(11),'grado26':grade.eq(26),'anio_discrepante':pd.to_numeric(df['anio'],errors='coerce').ne(year) if 'anio' in df else pd.Series(False,index=df.index)}
        for c,x in numeric.items():
            flags['nulo_'+c]=x.isna(); flags['fuera_rango_'+c]=x.notna() & (~x.between(0,500 if c=='punt_global' else (100 if c!='estu_inse_individual' else 100)))
        for per,idx in period.groupby(period).groups.items():
            for f,mask in flags.items(): counts[(per,f)]+=int(mask.loc[idx].sum())
        for c in ['estu_grado','estu_estudiante','estu_privado_libertad','cole_bilingue','cole_cod_depto_ubicacion','cole_depto_ubicacion']:
            if c in df:
                for (per,val),n in df.groupby([period,df[c]],dropna=False).size().items(): categories[(c,per,val)]+=int(n)
        if 'estu_cod_reside_depto' in df:
            stats['colegio_distinto_residencia']+=int((code.notna()&pd.to_numeric(df['estu_cod_reside_depto'],errors='coerce').notna()&code.ne(pd.to_numeric(df['estu_cod_reside_depto'],errors='coerce'))).sum())
        if 'estu_cod_depto_presentacion' in df:
            stats['colegio_distinto_presentacion']+=int((code.notna()&pd.to_numeric(df['estu_cod_depto_presentacion'],errors='coerce').notna()&code.ne(pd.to_numeric(df['estu_cod_depto_presentacion'],errors='coerce'))).sum())
        # As-received aggregation and explicitly labeled grade-11 sensitivity; no source is overwritten.
        for subset,mask in [('recibido',code.notna()&year.notna()),('grado11_control',codvalid&year.notna()&est&lib&complete&grade.eq(11))]:
            temp=pd.DataFrame({'codigo_departamento':code[mask],'anio':year[mask]})
            for c,x in numeric.items(): temp[c]=x[mask]
            for key,g in temp.groupby(['codigo_departamento','anio']):
                k=(subset,int(key[0]),int(key[1])); acc=groups.setdefault(k,Counter()); acc['n_estudiantes_saber']+=len(g)
                for c in numeric:
                    acc['sum_'+c]+=float(g[c].sum()); acc['n_'+c]+=int(g[c].count())
    report=pd.DataFrame([{'archivo':tag,'periodo':p,'control':f,'n':n} for (p,f),n in counts.items()])
    write(report,f'controles_{tag}.csv')
    write(pd.DataFrame([{'archivo':tag,'columna':c,'periodo':p,'valor':v,'n':n} for (c,p,v),n in categories.items()]),f'categorias_{tag}.csv')
    write(pd.DataFrame(schemas),f'esquema_{tag}.csv')
    rows=[]
    for (subset,code,year),a in groups.items():
        r={'archivo':tag,'subconjunto':subset,'codigo_departamento':code,'anio':year,'n_estudiantes_saber':a['n_estudiantes_saber']}
        for c in AVERAGES:
            if c in cmap:
                r['n_'+c]=a['n_'+c]; r['sum_'+c]=a['sum_'+c]; r['prom_'+c]=round(a['sum_'+c]/a['n_'+c],2) if a['n_'+c] else np.nan
        rows.append(r)
    write(pd.DataFrame(rows),f'agregados_{tag}.csv')
    print(tag, 'filas',int(report.loc[report.control.eq('filas'),'n'].sum()),'columnas',len(header),flush=True)
    return report,pd.DataFrame(rows),stats

def main():
    inventory()
    files=sorted((ROOT/'Datos anteriores a la limpieza').glob('*.csv'))
    reports=[]; panels=[]; geographic=[]
    for f in files+ [ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv']:
        tag=f.stem
        r,p,s=scan(f,',' if f.parent.name=='Dataset individual Saber 11' else ';',tag)
        reports.append(r); panels.append(p); geographic.append({'archivo':tag,**s})
    write(pd.concat(reports,ignore_index=True),'controles_todos.csv')
    write(pd.DataFrame(geographic),'discrepancias_geograficas.csv')
    ag=pd.concat(panels,ignore_index=True)
    final=ag[ag.archivo.eq('Saber_11_Listo_2018_2024') & ag.subconjunto.eq('recibido')].copy()
    historical=pd.read_csv(ROOT/'panel_departamento_anio_unido.csv',sep=';',encoding='utf-8-sig')
    comp=historical.merge(final,on=['codigo_departamento','anio'],how='outer',suffixes=('_historico','_actual'),indicator='comparacion_llaves',validate='one_to_one')
    cols=['codigo_departamento','anio','comparacion_llaves']
    for c in ['n_estudiantes_saber']+['n_'+c for c in AVERAGES]+['prom_'+c for c in AVERAGES]:
        if c+'_historico' in comp and c+'_actual' in comp:
            comp['delta_'+c]=comp[c+'_actual']-comp[c+'_historico']; cols += [c+'_historico',c+'_actual','delta_'+c]
    write(comp[cols],'comparacion_panel_recibido.csv')
    summaries=[]
    for y,g in historical.groupby('anio'):
        summaries.append({'anio':y,'filas':len(g),'both':g._merge.eq('both').sum(),'n':g.n_estudiantes_saber.sum(),'media_departamental':g.prom_punt_global.mean(),'media_ponderada_redondeada':(g.prom_punt_global*g.n_punt_global).sum()/g.n_punt_global.sum(),'min_n':g.n_estudiantes_saber.min(),'max_n':g.n_estudiantes_saber.max(),'positivos_ge250':g.prom_punt_global.ge(250).sum()})
    write(pd.DataFrame(summaries),'resumen_panel_historico.csv')
    matched=historical[historical._merge.eq('both')]
    summary={'filas_panel':len(historical),'llaves_duplicadas':int(historical.duplicated(['codigo_departamento','anio']).sum()),'cruces':historical._merge.value_counts().to_dict(),'conteo_total_panel':int(historical.n_estudiantes_saber.sum()),'diferencia_vs_tesis':int(2984199-historical.n_estudiantes_saber.sum()),'train':len(matched[matched.anio.isin([2018,2019,2021,2022])]),'positivos_train':int(matched[matched.anio.isin([2018,2019,2021,2022])].prom_punt_global.ge(250).sum()),'test':len(matched[matched.anio.isin([2023,2024])]),'positivos_test':int(matched[matched.anio.isin([2023,2024])].prom_punt_global.ge(250).sum())}
    (OUT/'resumen_recomprobacion.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__': main()
