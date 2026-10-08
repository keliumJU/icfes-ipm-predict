"""Continuación fase 1: lectura completa de TXT nuevos, sin alterar fuentes.

Inspeccionado antes de ejecutar. El universo sigue 2018-2024 sin 2020.
Todos los TXT se inventarían; 2020/2025 solo se inspeccionan por encabezado.
Controles de filtros reproducen hipótesis explícitas de scripts suministrados.
Firmas SHA-256 de campos administrativos NO sustituyen identidad personal.
IDs y firmas únicamente en memoria; resultados agregados en carpeta fechada.
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, re, subprocess, sys, platform, io
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from comprobar_registros import KEYS, normal, digest

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'auditoria/evidencia/actualizacion_20261008'
OUT.mkdir(parents=True, exist_ok=True)
TARGET = {'20181','20182','20191','20192','20211','20212','20221','20222','20231','20232','20241','20242'}
SCORES = ['punt_global','punt_matematicas','punt_lectura_critica','punt_c_naturales','punt_sociales_ciudadanas','punt_ingles']
EXTRA = ['estu_consecutivo','cole_calendario','estu_estudiante','estu_privado_libertad',
         'cole_bilingue','cole_depto_ubicacion','estu_depto_reside','estu_depto_presentacion','estu_discapacidad']
NEEDED = list(dict.fromkeys(KEYS + EXTRA))
CHUNK = 100000


def csv_out(rows, name):
    pd.DataFrame(rows).to_csv(OUT / name, index=False)


def fmt(path):
    # Validate whole file encoding in inventory; header detection isn't full-file validation.
    for enc in ['utf-8-sig','latin-1']:
        try:
            with path.open(encoding=enc) as f: line=f.readline()
            sep=max([';','\t',','],key=line.count)
            header=next(csv.reader([line],delimiter=sep))
            return sep,enc,[c.strip().lower().lstrip('\ufeff') for c in header]
        except UnicodeDecodeError: pass
    raise ValueError(path)


def signatures(df):
    values=[]
    # Only representation adjustments previously documented; no score or population changes.
    for c in KEYS:
        values.append(df[c].fillna('').map(lambda v: normal(str(v),c)))
    return np.array([digest(row) for row in zip(*values)],dtype='S32')


def multiset_delta(a,b):
    ua,ca=np.unique(a,return_counts=True);ub,cb=np.unique(b,return_counts=True)
    if len(ub)==0:return int(len(a))
    pos=np.searchsorted(ub,ua);safe=np.minimum(pos,len(ub)-1)
    avail=np.where((pos<len(ub)) & (ub[safe]==ua),cb[safe],0)
    return int(np.maximum(ca-avail,0).sum())


def main():
    inventory=[];schemas=[];controls=[];calendars=[];formula=[];source_hash={};accepted_hash={};identified=[]
    previous=subprocess.check_output(['git','show','77c286f43a3c6d811fc68ba9399fd5ec99277528:auditoria/inventario_trazabilidad.csv'],cwd=ROOT).decode()
    old=pd.read_csv(io.StringIO(previous)).set_index('archivo')
    paths=sorted((ROOT/'raw_data').glob('*.txt'))+sorted((ROOT/'Datos anteriores a la unificacion').glob('*.csv'))
    paths+=[ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv']
    for path in paths:
        sha=hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda:f.read(8*1024*1024),b''):sha.update(block)
        rel=str(path.relative_to(ROOT)); previous=rel.replace('Datos anteriores a la unificacion/','Datos anteriores a la limpieza/')
        verified=previous in old.index and sha.hexdigest()==old.loc[previous,'sha256']
        inventory.append({'archivo':rel,'bytes':path.stat().st_size,'sha256':sha.hexdigest(),
                          'estado_git':'ignorado' if subprocess.run(['git','check-ignore','-q',rel],cwd=ROOT).returncode==0 else 'no ignorado',
                          'ruta_anterior':previous if previous in old.index else '',
                          'misma_huella_previa':verified if previous in old.index else '',
                          'origen':'aportado localmente por usuario; descarga no autenticada'})
    csv_out(inventory,'inventario_nuevos_y_renombrados.csv')
    for path in sorted((ROOT/'raw_data').glob('*.txt')):
        per=re.search(r'(\d{5})',path.name).group(1);sep,enc,header=fmt(path)
        schemas.extend({'archivo':path.name,'periodo_nombre':per,'columna':c,'posicion_1':i+1,
                        'separador':repr(sep),'encoding_detectado':enc,'en_universo':per in TARGET} for i,c in enumerate(header))
        if per not in TARGET:continue
        missing=set(NEEDED)-set(header)
        if missing:raise ValueError(f'{path.name}: faltan {missing}')
        count=Counter();calendar=Counter();ids=[];all_sigs=[];keep_sigs=[];idx=[header.index(c) for c in NEEDED]
        def process(block):
            df=pd.DataFrame(block,columns=NEEDED)
            # CSV/pandas default NA tokens used by supplied cleaning scripts.
            df=df.replace(['','NA','N/A','NULL','null','NaN','nan','None','<NA>'],np.nan)
            nums={c:pd.to_numeric(df[c].str.replace(',','.',regex=False),errors='coerce') for c in SCORES}
            est=df.estu_estudiante.fillna('').str.strip().str.upper().eq('ESTUDIANTE')
            lib=~df.estu_privado_libertad.fillna('N').str.strip().str.upper().eq('S')
            dept=df[['cole_depto_ubicacion','estu_depto_reside','estu_depto_presentacion']].bfill(axis=1).iloc[:,0]
            dept=~dept.fillna('').str.strip().str.upper().isin(['','NAN','NONE','NULL','DESCONOCIDO'])
            gp=nums['punt_global'].notna() & nums['punt_global'].gt(0)
            school=df.cole_cod_depto_ubicacion.notna()
            complete=pd.Series(True,index=df.index)
            for v in nums.values():complete &= v.notna() & v.gt(0)
            grade=pd.to_numeric(df.estu_grado,errors='coerce').eq(11)
            sequential={'01_recibido':pd.Series(True,index=df.index),'02_estudiante':est,
                        '03_sin_libertad':est&lib,'04_seis_puntajes':est&lib&complete,
                        '05_codigo_colegio':est&lib&complete&school,
                        '06_grado11':est&lib&complete&school&grade,
                        'script_FIX':gp&dept&est&lib,
                        'script_FIX_mas_final':gp&dept&est&lib&school&complete}
            for label,mask in sequential.items():
                count[label]+=int(mask.sum())
                for val,n in df.loc[mask,'cole_calendario'].fillna('(faltante)').value_counts().items():calendar[(label,val)]+=int(n)
            count['periodo_distinto_nombre']+=int(df.periodo.fillna('').str.replace(r'\.0$','',regex=True).ne(per).sum())
            count['bilingue_faltante_final']+=int((sequential['script_FIX_mas_final']&df.cole_bilingue.isna()).sum())
            count['id_faltante']+=int(df.estu_consecutivo.isna().sum())
            ids.extend(df.estu_consecutivo.fillna('').astype(str).tolist())
            sig=signatures(df);all_sigs.append(sig); keep_sigs.append(sig[sequential['script_FIX_mas_final'].to_numpy()])
            computed=np.floor((3*sum(nums[c] for c in SCORES[1:5])+nums['punt_ingles'])*5/13+0.5)
            bad=complete & nums['punt_global'].ne(computed)
            for label,mask in [('recibido',bad),('final_reconstruido',bad&sequential['script_FIX_mas_final']),('grado11_reconstruido',bad&sequential['06_grado11'])]:
                count['formula_discrepante_'+label]+=int(mask.sum())
            if per=='20222':
                tmp=pd.DataFrame({'delta':nums['punt_global']-computed,'grado':df.estu_grado,'discapacidad':df.estu_discapacidad.fillna('(faltante)')})
                for (delta,g,dis),n in tmp[bad].groupby(['delta','grado','discapacidad']).size().items():formula.append({'periodo':per,'delta':delta,'grado':g,'discapacidad':dis,'n':int(n)})
        widths=Counter();block=[]
        with path.open(encoding=enc,newline='') as f:
            reader=csv.reader(f,delimiter=sep);next(reader)
            for row in reader:
                widths[len(row)]+=1
                if len(row)!=len(header):continue
                block.append([row[i] for i in idx])
                if len(block)>=CHUNK:process(block);block=[]
            if block:process(block)
        a=np.array(ids,dtype=str);nonblank=a[a!=''];unique,freq=np.unique(nonblank,return_counts=True)
        count['id_repetidos_exceso']=int(np.maximum(freq-1,0).sum())
        count['grupos_id_repetido']=int((freq>1).sum())
        count['filas_ancho_incorrecto']=sum(n for w,n in widths.items() if w!=len(header))
        identified.extend(unique.tolist())
        source_hash[per]=np.concatenate(all_sigs);accepted_hash[per]=np.concatenate(keep_sigs)
        controls.extend({'archivo':path.name,'periodo':per,'control':k,'n':n} for k,n in count.items())
        calendars.extend({'periodo':per,'poblacion':p,'calendario':c,'n':n} for (p,c),n in calendar.items())
        print(json.dumps({'periodo':per,'filas':count['01_recibido'],'final_hipotesis':count['script_FIX_mas_final'],'grado11':count['06_grado11'],'id_repetidos':count['id_repetidos_exceso']},ensure_ascii=False),flush=True)
    csv_out(schemas,'esquemas_raw.csv');csv_out(controls,'filtros_raw.csv');csv_out(calendars,'calendarios_raw.csv')
    if formula:
        g=pd.DataFrame(formula).groupby(['periodo','delta','grado','discapacidad'],as_index=False).n.sum();g.to_csv(OUT/'formula20222_raw.csv',index=False)
    ids_all=np.array(identified,dtype=str);_,id_freq=np.unique(ids_all,return_counts=True)
    final={}
    path=ROOT/'Dataset individual Saber 11/Saber_11_Listo_2018_2024.csv'
    for df in pd.read_csv(path,usecols=lambda c:c.lower() in KEYS,dtype=str,chunksize=CHUNK):
        df.columns=df.columns.str.lower()
        for per,g in df.groupby('periodo'):
            final.setdefault(normal(per,'periodo'),[]).append(signatures(g))
    match=[]
    for per,parts in sorted(final.items()):
        sig=np.concatenate(parts);raw=accepted_hash[per]
        match.append({'periodo':per,'n_final':len(sig),'n_raw_filtrado':len(raw),
                      'final_sin_correspondencia_raw_filtrado':multiset_delta(sig,raw),
                      'raw_filtrado_sin_correspondencia_final':multiset_delta(raw,sig),
                      'ambiguedades_firma_raw_filtrado_exceso':len(raw)-len(np.unique(raw))})
    csv_out(match,'conservacion_raw_final.csv')
    periodic=[]
    for path in sorted((ROOT/'Datos anteriores a la unificacion').glob('*.csv')):
        per=re.search(r'(\d{5})',path.name).group(1);parts=[]
        for df in pd.read_csv(path,sep=';',usecols=lambda c:c.lower() in KEYS,dtype=str,chunksize=CHUNK):
            df.columns=df.columns.str.lower();parts.append(signatures(df))
        sig=np.concatenate(parts);raw=source_hash[per]
        periodic.append({'periodo':per,'n_periodico':len(sig),'n_raw':len(raw),'periodico_sin_correspondencia_raw':multiset_delta(sig,raw),'raw_sin_correspondencia_periodico':multiset_delta(raw,sig)})
    csv_out(periodic,'conservacion_raw_periodicos.csv')
    summary={'fecha_cliente':'2026-10-08','git_partida':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
             'python_actual':sys.version,'plataforma_actual':platform.platform(),'chunksize':CHUNK,
             'periodos_raw_auditados':len(accepted_hash),'filas_raw_universo':sum(len(a) for a in source_hash.values()),
             'filas_raw_hipotesis_final':sum(len(a) for a in accepted_hash.values()),
             'id_presentes_en_mas_de_un_periodo_exceso':int(np.maximum(id_freq-1,0).sum()),
             'identificador_no_interpretado_como_id_persona':True,
             'final_sin_raw_filtrado':sum(r['final_sin_correspondencia_raw_filtrado'] for r in match),
             'raw_filtrado_sin_final':sum(r['raw_filtrado_sin_correspondencia_final'] for r in match),
             'originales_no_modificados':True,'modelo_entrenado':False,
             'limite':'Conservación de 16 campos críticos, no igualdad de cada atributo; descarga histórica no autenticada'}
    (OUT/'resumen_raw.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
