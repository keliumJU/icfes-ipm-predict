"""Entrega fechada: solo se habilita base si pasan controles completos de raw.

Conserva evidencia de 2026-10-07. No ejecuta scripts originales ni modelos.
Actualiza inventario y matriz actuales con estado previo explícito.
La base es departamento-año, nunca contiene identificadores individuales.
"""
from pathlib import Path
import json, hashlib, csv, io, subprocess, sys
sys.dont_write_bytecode = True
import pandas as pd
from collections import Counter
from auditar_raw_20261008 import fmt, TARGET

ROOT=Path(__file__).resolve().parents[2];AUD=ROOT/'auditoria';EV=AUD/'evidencia';NEW=EV/'actualizacion_20261008'
SCORES=['punt_global','punt_matematicas','punt_lectura_critica','punt_c_naturales','punt_sociales_ciudadanas','punt_ingles']

def main():
    summary=json.loads((NEW/'resumen_raw.json').read_text())
    filters=pd.read_csv(NEW/'filtros_raw.csv',dtype={'periodo':str})
    totals=filters.groupby('control').n.sum().to_dict()
    conservation=pd.read_csv(NEW/'conservacion_raw_final.csv')
    conditions={
        'doce_periodos':summary['periodos_raw_auditados']==12,
        'total_inicial':summary['filas_raw_universo']==4039755,
        'estudiantes':totals['02_estudiante']==3433542,
        'sin_libertad':totals['03_sin_libertad']==3432366,
        'puntajes':totals['04_seis_puntajes']==3401100,
        'codigo_colegio':totals['05_codigo_colegio']==3401100,
        'grado11':totals['06_grado11']==2984199,
        'final_igual_raw_filtrado':summary['final_sin_raw_filtrado']==summary['raw_filtrado_sin_final']==0,
        'ancho_y_periodo_correctos':totals['filas_ancho_incorrecto']==totals['periodo_distinto_nombre']==0,
        'identificadores_registro_completos_unicos':totals['id_faltante']==totals['id_repetidos_exceso']==0,
        'firmas_criticas_no_ambiguas':int(conservation.ambiguedades_firma_raw_filtrado_exceso.sum())==0,
    }
    validation={'fecha':'2026-10-08','condiciones':conditions,'reconstruccion_validada':all(conditions.values()),
                'alcance':'población, geografía codificada, seis puntajes y agregación reproducidos desde TXT locales; no autenticación de descarga ni igualdad de todos los atributos',
                'causa_historica_20212':'recuerdo del usuario y comentario del script; no se exige recrear fallo del panel sustituido',
                'criterios_no_cambiados':True,'modelo_entrenado':False}
    (NEW/'validacion_reconstruccion.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False)+'\n')
    # Preserve the previous release; do not rewrite old result tables or its environment.
    previous_commit='77c286f43a3c6d811fc68ba9399fd5ec99277528'
    def previous_csv(name):
        content=subprocess.check_output(['git','show',f'{previous_commit}:auditoria/{name}'],cwd=ROOT).decode()
        return pd.read_csv(io.StringIO(content),keep_default_na=False)
    old=previous_csv('inventario_trazabilidad.csv')
    incoming=pd.read_csv(NEW/'inventario_nuevos_y_renombrados.csv',keep_default_na=False).set_index('archivo')
    inv=[]
    for row in old.to_dict('records'):
        rel=row['archivo'].replace('Datos anteriores a la limpieza/','Datos anteriores a la unificacion/')
        row['ruta_entrega_20261007']=row['archivo'];row['archivo']=rel;row['fecha_verificacion']='2026-10-08'
        path=ROOT/rel
        if row['tipo']=='directorio vacío':
            assert path.is_dir() and not any(path.iterdir())
        elif rel in incoming.index:
            assert row['sha256']==incoming.loc[rel,'sha256'];row['observacion']='Mismo contenido que entrega previa; ruta local actualizada si corresponde'
        else:
            sha=hashlib.sha256(path.read_bytes()).hexdigest()
            if rel!='.gitignore':assert sha==row['sha256'],rel
            else:row['observacion']='Cambio del usuario presente al iniciar sesión; no se modifica ni incorpora al commit de auditoría'
            row['sha256']=sha;row['bytes']=path.stat().st_size
        inv.append(row)
    for rel,r in incoming.iterrows():
        if rel.startswith('raw_data/'):
            inv.append({'archivo':rel,'tipo':'.txt','bytes':r['bytes'],'sha256':r['sha256'],
                        'estado_git':r['estado_git'],'observacion':r['origen'],'ruta_entrega_20261007':'','fecha_verificacion':'2026-10-08'})
    pd.DataFrame(inv).to_csv(AUD/'inventario_trazabilidad.csv',index=False)
    if not validation['reconstruccion_validada']:
        print(json.dumps(validation,ensure_ascii=False));return
    ag=pd.read_csv(EV/'agregados_Saber_11_Listo_2018_2024.csv')
    grade=ag[ag.subconjunto.eq('grado11_control')].copy()
    # Independent sums directly from all relevant TXT blocks, not rounded intermediate means.
    acc={}
    columns=SCORES+['periodo','estu_estudiante','estu_privado_libertad','estu_grado','cole_cod_depto_ubicacion']
    for path in sorted((ROOT/'raw_data').glob('*.txt')):
        if not any(path.stem.endswith(p) for p in TARGET):continue
        sep,enc,header=fmt(path)
        for df in pd.read_csv(path,sep=sep,encoding=enc,usecols=columns,dtype=str,chunksize=100000):
            num={c:pd.to_numeric(df[c].str.replace(',','.',regex=False),errors='coerce') for c in SCORES}
            code=pd.to_numeric(df.cole_cod_depto_ubicacion,errors='coerce')
            mask=df.estu_estudiante.fillna('').str.strip().str.upper().eq('ESTUDIANTE')
            mask &= ~df.estu_privado_libertad.fillna('N').str.strip().str.upper().eq('S')
            mask &= code.notna() & pd.to_numeric(df.estu_grado,errors='coerce').eq(11)
            for c,v in num.items():mask &= v.notna() & v.gt(0)
            temp=pd.DataFrame({'codigo_departamento':code[mask], 'anio':df.loc[mask,'periodo'].str[:4].astype(int)})
            for c,v in num.items():temp[c]=v[mask]
            for (d,y),g in temp.groupby(['codigo_departamento','anio']):
                a=acc.setdefault((int(d),int(y)),Counter());a['n_estudiantes_saber']+=len(g)
                for c in SCORES:a['sum_'+c]+=float(g[c].sum());a['n_'+c]+=int(g[c].count())
    raw_ag=pd.DataFrame([{'codigo_departamento':d,'anio':y,**a} for (d,y),a in acc.items()])
    raw_ag.to_csv(NEW/'agregados_grado11_raw.csv',index=False)
    comparison=raw_ag.merge(grade,on=['codigo_departamento','anio'],suffixes=('_raw','_final'),validate='one_to_one')
    assert len(comparison)==198
    ledger=[]
    for c in ['n_estudiantes_saber']+['sum_'+c for c in SCORES]+['n_'+c for c in SCORES]:
        delta=comparison[c+'_raw']-comparison[c+'_final']
        assert delta.eq(0).all(),c
        for (d,y,v) in zip(comparison.codigo_departamento,comparison.anio,delta):
            ledger.append({'codigo_departamento':d,'anio':y,'variable':c,'delta_raw_menos_final':v})
    pd.DataFrame(ledger).to_csv(NEW/'cotejo_agregacion_raw_final.csv',index=False)
    grade=raw_ag
    data=grade[['codigo_departamento','anio','n_estudiantes_saber']].copy()
    for c in SCORES:
        assert grade['n_'+c].equals(grade.n_estudiantes_saber)
        data['n_'+c]=grade['n_'+c]
        data['prom_'+c]=grade['sum_'+c]/grade['n_'+c]
    ipm=pd.read_csv(ROOT/'Fuente del IPM/ipm_departamental_limpio_sin_2020.csv',sep=';')
    data=data.merge(ipm,on=['codigo_departamento','anio'],how='outer',indicator=True,validate='one_to_one')
    assert len(data)==198 and data._merge.eq('both').all() and data.n_estudiantes_saber.sum()==2984199
    assert not data.drop(columns='_merge').isna().any().any()
    assert data.groupby('anio').size().eq(33).all()
    for year,n in filters[filters.control.eq('06_grado11')].assign(anio=lambda d:d.periodo.str[:4].astype(int)).groupby('anio').n.sum().items():
        assert data.loc[data.anio.eq(year),'n_estudiantes_saber'].sum()==n
    data=data.drop(columns='_merge').sort_values(['anio','codigo_departamento'])
    data['codigo_departamento']=data.codigo_departamento.astype(int).astype(str).str.zfill(2)
    data.to_csv(AUD/'base_analitica_departamento_anio.csv',index=False)
    dictionary=[]
    for c in data.columns:
        if c=='codigo_departamento':definition='Código DIVIPOLA departamento del colegio, dos dígitos';unit='código';source='COLE_COD_DEPTO_UBICACION raw, conservado en final'
        elif c=='departamento':definition='Nombre departamental homologado del anexo IPM';unit='texto';source='CSV IPM cotejado por celda contra XLSX'
        elif c=='anio':definition='Primeros cuatro dígitos de PERIODO; 2018,2019,2021,2022,2023,2024';unit='año';source='PERIODO raw/final'
        elif c.startswith('n_'):definition='Conteo de registros elegibles en la celda; denominador propio del puntaje si aplica';unit='registros, no personas únicas';source='consolidado verificado contra raw filtrado'
        elif c.startswith('prom_'):definition='Suma de puntajes recibidos / conteo propio, sin redondeo intermedio';unit='puntos, 0–500 global; 0–100 pruebas';source='puntajes de TXT locales conservados, incluidos 414 globales con diferencia de fórmula'
        elif c=='ipm':definition='Incidencia departamental total de pobreza multidimensional';unit='% personas';source='XLSX IPM_Departamentos, celda exacta en cotejo_ipm_celdas.csv'
        else:definition='Tasa departamental total de privación marginal: '+c;unit='% hogares, según rótulo de fuente';source='XLSX IPM_Variables_Departamento, celda exacta en cotejo_ipm_celdas.csv'
        dictionary.append({'variable':c,'definicion':definition,'unidad':unit,'fuente_procedimiento':source,
                           'advertencia':'Universo grado11; no2020/2025; no causalidad; IPM con notas de comparabilidad; sin imputación de puntajes'})
    pd.DataFrame(dictionary).to_csv(AUD/'diccionario_base_analitica.csv',index=False)
    # Descriptive replacement of the added table, with explicit N and no variable selection.
    measures=[c for c in ipm.columns if c not in ['codigo_departamento','departamento','anio']]
    between=data.groupby('codigo_departamento')[['prom_punt_global']+measures].mean()
    table=[{'variable':c,'r_198_celdas':data[c].corr(data.prom_punt_global),
            'r_33_medias_territoriales':between[c].corr(between.prom_punt_global),
            'n_celdas':198,'n_territorios':33,'geografia':'departamento del colegio',
            'anios':'2018,2019,2021,2022,2023,2024','poblacion':'grado11'} for c in measures]
    pd.DataFrame(table).to_csv(NEW/'tabla12_propuesta_198.csv',index=False)
    # Editorial update preserves what was known in the previous session per claim.
    matrix=previous_csv('auditoria_afirmaciones.csv')
    for c in ['dictamen','evidencia_verificable','pendiente']:
        matrix[c+'_20261007']=matrix[c]
    matrix['fecha_actualizacion']='2026-10-08'
    for i,r in matrix.iterrows():
        loc=r.afirmacion
        if loc=='2.984.199 estudiantes de grado 11':
            matrix.loc[i,['dictamen','evidencia_verificable','correccion_o_alcance','pendiente']]=['respaldada','actualizacion_20261008/filtros_raw.csv; conservacion_raw_final.csv: doce periodos, 2.984.199 grado11','Registros elegibles reconstruidos desde TXT locales; no personas únicas ni descarga autenticada','']
        elif loc.startswith('4.039.755 filas originales'):
            matrix.loc[i,['dictamen','evidencia_verificable','correccion_o_alcance','pendiente']]=['respaldada','actualizacion_20261008/filtros_raw.csv y validacion_reconstruccion.json: etapas secuenciales reproducidas','Conteos actuales de los TXT locales; filtros concurrentes no deben sumarse como mermas disjuntas','']
        elif loc.startswith('608.458 bilingüismos'):
            matrix.loc[i,['dictamen','evidencia_verificable','correccion_o_alcance','pendiente']]=['respaldada','actualizacion_20261008/filtros_raw.csv: 608.458 bilingue_faltante_final, 20.485 de20241 todos; categorias del final; código fillna N','Recuento actual de faltantes coincide. No autentica fecha de ejecución histórica; auditoría no imputa ni usa bilingüismo','']
        elif loc.startswith('No hay duplicados'):
            matrix.loc[i,['evidencia_verificable','correccion_o_alcance','pendiente']]=['actualizacion_20261008/filtros_raw.csv: ID nulos y repetidos; resumen_raw.json: repetición entre periodos','Se verifican IDs de registro; no identidad de personas que puedan presentar varias aplicaciones','']
        elif loc.startswith('Los _limpio son originales'):
            matrix.loc[i,['evidencia_verificable','correccion_o_alcance','pendiente']]=['actualizacion_20261008/esquemas_raw.csv y conservacion_raw_periodicos.csv; columna59 distinta de esquema77','Derivados de 59 campos. Se comprueba su conservación proyectada; no se conoce criterio histórico de columnas. Reconstrucción nueva usa raw directamente','Criterio histórico59 no recuperado; no requerido por reconstrucción explícita nueva']
        elif loc.startswith('Fórmula estándar global'):
            matrix.loc[i,['evidencia_verificable','correccion_o_alcance','pendiente']]=['actualizacion_20261008/formula20222_raw.csv; filtros_raw.csv y conservacion_raw_final.csv','Discrepancias ya presentes en TXT y conservadas; no error de lectura demostrado ni corrección de puntajes','Regla o versión ICFES que explique aritmética; advertencia de fuente, no filtro']
        elif loc.startswith('198 observaciones disponibles') or loc.startswith('198 celdas y 33'):
            matrix.loc[i,['dictamen','evidencia_verificable','correccion_o_alcance','pendiente']]=['respaldada','base_analitica_departamento_anio.csv; actualizacion_20261008/validacion_reconstruccion.json','198 celdas de población explícita reconstruida; no utilizar panel raíz incompleto','']
        elif loc.startswith('12 periodos, esquema 82'):
            matrix.loc[i,['evidencia_verificable','pendiente']]=['actualizacion_20261008/esquemas_raw.csv: identificador/calendario en TXT; final79 y periódicos59 los omiten','Historial exacto del esquema82 no autenticado; reconstrucción nueva no depende de él']
        elif loc.startswith('Saber local no tiene cohorte'):
            matrix.loc[i,['evidencia_verificable','correccion_o_alcance','pendiente']]=['actualizacion_20261008/conservacion_raw_final.csv: 20211 y20212 completos bajo filtros; IPM Bogotá completo','Afirmación descartada para reconstrucción actual; conservar2021 yBogotá','']
        elif loc.startswith('Panel 160, 32 territorios'):
            matrix.loc[i,['correccion_o_alcance','pendiente']]=['Propuesta formal de sustitución en propuesta_correccion_tesis.md y tabla12_propuesta_198.csv; otra construcción histórica preservada','Edición por el grupo pendiente; no bloquea cotejo de la propuesta ni autentica artefactos históricos']
        elif loc.startswith('Residuo tabulado fue causa'):
            matrix.loc[i,['correccion_o_alcance','pendiente']]=['Usuario recuerda error de lectura20212; TXT actual tiene separador válido y final conserva sus filas filtradas. No recrear ni atribuir causa específica sin log','Causa histórica archivada como no verificable; panel reemplazado para reconstrucción']
        elif loc.startswith('Todas las cifras publicadas'):
            matrix.loc[i,'pendiente']='Convención de redondeo histórica desconocida; diferencias registradas, sin adaptar criterios'
    matrix.to_csv(AUD/'auditoria_afirmaciones.csv',index=False)
    validation['base_entregada']='auditoria/base_analitica_departamento_anio.csv'
    validation['cotejos_agregacion_independiente']=len(ledger)
    validation['filas_base']=len(data);validation['suma_registros_base']=int(data.n_estudiantes_saber.sum())
    (NEW/'validacion_reconstruccion.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(validation,ensure_ascii=False))

if __name__=='__main__':main()
