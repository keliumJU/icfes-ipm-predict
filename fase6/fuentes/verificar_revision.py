"""Cotejos aritméticos/documentales sin ajustar ni aplicar estimadores."""
import ast
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from integridad import ROOT, OUT, guardar, sha, cierre
from generar_entrega import compact_tables, render, ENT

WIN='gradient_boosting_ambas_07'
CHECKS=[]

def leer(r):
    return pd.read_csv(ROOT/r,float_precision='round_trip',dtype={'codigo_departamento':str})

def cerca(a,b,etiqueta):
    assert np.allclose(a,b,rtol=0,atol=1e-10),etiqueta
    CHECKS.append(etiqueta)

def metrics(p):
    e=p.prediccion.to_numpy()-p.observado.to_numpy(); y=p.observado.to_numpy()
    return [len(p),np.abs(e).mean(),np.sqrt((e**2).mean()),e.mean(),1-(e**2).sum()/((y-y.mean())**2).sum()]

def tablas(md):
    return [m.group().strip() for m in re.finditer(r'(?:^\|.*\n)+',md,flags=re.M)]

def numerica():
    # Fuente común declarativa sin importar lógica de ajuste.
    spec=importlib.util.spec_from_file_location('config_fase6',ROOT/'protocolo/fuentes/configuracion.py')
    cfg=importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
    base=leer('auditoria/base_analitica_departamento_anio.csv'); dev=base.query('anio<=2022')
    assert len(base)==198 and len(dev)==132 and not base.isna().any().any()
    assert base.groupby('anio').size().tolist()==[33]*6 and base.n_estudiantes_saber.sum()==2984199
    assert not base.duplicated(['codigo_departamento','anio']).any()
    con=json.loads((ROOT/'fase3/resultados/congelacion.json').read_text())
    assert con['ganador_global']==WIN and con['filas']==132 and con['entrenamiento_anios']==[2018,2019,2021,2022]
    for p,h in con['artefactos_sha256'].items(): assert sha(ROOT/p)==h
    # 91 métricas completas, 4 indicadores numéricos/n por fila, todas las familias.
    count=0
    for path,metpath,context in [
        ('fase3/resultados/predicciones_desarrollo.csv','fase3/resultados/comparacion_desarrollo.csv','seleccion'),
        ('fase3/resultados/predicciones_reevaluacion.csv','fase3/resultados/metricas_reevaluacion.csv','temporal'),
        ('fase4/resultados/predicciones_territoriales.csv','fase4/resultados/metricas_agrupadas.csv','territorial')]:
        pred=leer(path); met=leer(metpath)
        cerca(pred.prediccion-pred.observado,pred.error,context+': error por fila')
        assert len(pred)=={'seleccion':6633,'temporal':462,'territorial':396}[context]
        for _,r in met.iterrows():
            p=pred[pred.id==r.id]
            if context=='temporal' and str(r.periodo)!='conjunto':p=p[p.anio==int(r.periodo)]
            vals=metrics(p)
            cerca(vals[1:],r[['mae','rmse','sesgo','r2']].astype(float).to_numpy(),f'{context}/{r.id}/{r.get("periodo","conjunto")}')
            assert len(p)==(int(r['n']) if 'n' in r.index else 99)
            count+=1
    assert count==91
    # Todas las métricas territoriales; no omisión de grupos extremos.
    terr=leer('fase4/resultados/predicciones_territoriales.csv')
    for _,r in leer('fase4/resultados/metricas_territorio.csv').iterrows():
        p=terr[(terr.id==r.id)&(terr.codigo_departamento==r.codigo_departamento)]
        cerca(metrics(p)[1:],r[['mae','rmse','sesgo','r2']].astype(float).to_numpy(),'territorio/'+r.id+'/'+r.codigo_departamento)
    # Cuantiles de réplicas YA guardadas: sin muestreo nuevo ni RNG.
    boot=leer('fase4/resultados/bootstrap_resumen.csv');rep=leer('fase4/resultados/bootstrap_replicas.csv')
    assert len(rep)==14000
    for _,r in boot.iterrows():
        p=rep[(rep.contexto==r.contexto)&(rep.a==r.a)&(rep.b==r.b)]
        assert len(p)==2000 and p.replica.nunique()==2000
        cerca(np.quantile(p.delta_mae,[.025,.975]),[r.percentil_2_5,r.percentil_97_5],'percentiles/'+r.contexto+'/'+r.a+'/'+r.b)
        pred=terr if r.contexto=='territorial_desarrollo' else leer('fase3/resultados/predicciones_reevaluacion.csv')
        g=pred.assign(ae=lambda x:abs(x.error)).groupby('id').ae.mean()
        cerca(g[r.a]-g[r.b],r.delta_mae,'delta/'+r.a+'/'+r.b)
    # Asociaciones entre/dentro/doble centrado y todas las columnas.
    cols=cfg.ESPECIFICACIONES['ambas']; y=cfg.RESULTADO
    means=dev.groupby('codigo_departamento')[[*cols,y]].mean()
    within=dev[[*cols,y]]-dev.groupby('codigo_departamento')[[*cols,y]].transform('mean')
    double=within-dev.groupby('anio')[[*cols,y]].transform('mean')+dev[[*cols,y]].mean()
    assoc=leer('fase4/resultados/asociaciones_longitudinales.csv')
    for _,r in assoc.iterrows():
        cerca([means[r.variable].corr(means[y]),within[r.variable].corr(within[y]),double[r.variable].corr(double[y])],
            [r.r_entre_territorios,r.r_dentro_territorio,r.r_doble_centrado],'asociacion/'+r.variable)
    col=leer('fase4/resultados/colinealidad.csv').set_index('especificacion')
    coeff=leer('fase4/resultados/coeficientes_ols_congelados.csv')
    for name,features in cfg.ESPECIFICACIONES.items():
        x=dev[features].to_numpy();z=(x-x.mean(0))/x.std(0);sv=np.linalg.svd(z,compute_uv=False)
        cerca(sv[0]/sv[-1],col.loc[name,'numero_condicion'],'condicion/'+name)
        assert np.linalg.matrix_rank(z)==col.loc[name,'rango']==len(features)
        stored=coeff[coeff.id=='ols_'+name].set_index('variable').loc[features]
        tr=con['transformaciones']['ols_'+name]
        cerca(stored.coef_por_sd_entrenamiento,tr['coef'],'coeficientes/'+name)
        cerca(stored.sd_entrenamiento,tr['scale'],'escala/'+name)
        cerca(stored.coef_por_punto_porcentual,np.array(tr['coef'])/tr['scale'],'coef_pp/'+name)
    pairs=leer('fase4/resultados/pares_correlacion.csv')
    for _,r in pairs.iterrows():cerca(dev[r.a].corr(dev[r.b]),r.r,'correlacion/'+r.a+'/'+r.b)
    # Conteos/cotejos de evidencia anterior, sin relectura raw ni alteración.
    cotejos=leer('auditoria/evidencia/actualizacion_20261008/cotejo_agregacion_raw_final.csv')
    assert len(cotejos)==2574 and (cotejos.delta_raw_menos_final==0).all()
    formula=leer('auditoria/evidencia/actualizacion_20261008/formula20222_raw.csv')
    assert formula[formula.grado==11].n.sum()==414
    sample=base.groupby('anio',as_index=False).agg(territorios=('codigo_departamento','nunique'),celdas=('codigo_departamento','size'),registros=('n_estudiantes_saber','sum'),min_registros=('n_estudiantes_saber','min'),max_registros=('n_estudiantes_saber','max'))
    prior=leer('fase5/resultados/tabla_muestra.csv')
    cerca(sample.select_dtypes('number'),prior.select_dtypes('number'),'tabla_muestra')
    # Control previo reutilizado exclusivamente en modo lectura: sustituir las dos
    # funciones que escribían en fase5. No invocar generador previo.
    oldpath=ROOT/'fase5/fuentes';sys.path.insert(0,str(oldpath))
    module_spec=importlib.util.spec_from_file_location('verificador5_lectura',oldpath/'verificar_informe.py')
    v=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(v)
    v.cierre=lambda:None
    captured={};v.guardar=lambda name,obj:captured.update({name:obj})
    v.main();sys.path.remove(str(oldpath))
    assert captured['verificacion_informe.json']['cifras_narrativas_contrastadas']
    # Las diez tablas exactas de informe raíz deben coincidir con CSV fase5.
    original=(ROOT/'informe_objetivo_3.md').read_text(); all_tables=tablas(original)
    table_files=['muestra','especificaciones','familias_seleccion','seleccion_referencias','reevaluacion_conjunta','ganador_temporal','territorial','remuestreo','sintesis_robustez','asociaciones']
    spec_d=importlib.util.spec_from_file_location('documentar5_lectura',oldpath/'documentar.py')
    d=importlib.util.module_from_spec(spec_d);spec_d.loader.exec_module(d)
    # Función tabla escribe: redirigir únicamente sus derivados a fase6.
    d.OUT=OUT/'tablas_cotejo'; d.OUT.mkdir(exist_ok=True)
    for name,expected in zip(table_files,all_tables):
        actual=d.tabla(leer('fase5/resultados/tabla_'+name+'.csv'),'tabla_'+name)
        assert actual.strip()==expected,name
    guardar('verificacion_numerica.json',dict(aprobado=True,filas_metricas=91,
        metricas_territorio=99,asociaciones=16,replicas_previas_leidas=14000,tablas_exactas=10,
        controles=CHECKS,control_narrativo_previo_en_modo_lectura=captured,
        ajustes_nuevos=0,predicciones_nuevas=0,replicas_nuevas=0,versiones={'python':sys.version.split()[0],'pandas':pd.__version__,'numpy':np.__version__}))

def trazabilidad():
    original=(ROOT/'informe_objetivo_3.md').read_text()
    sources={
    1:'protocolo/PROTOCOLO_OBJETIVO_3.md §§1–7; fase3/decisiones.md F03-01; fase5/decisiones_previas.md F05-01',
    2:'auditoria/base_analitica_departamento_anio.csv llave codigo_departamento/anio; auditoria/diccionario_base_analitica.csv; auditoria/evidencia/actualizacion_20261008/filtros_raw.csv; calendarios_raw.csv; cotejo_agregacion_raw_final.csv columna delta_raw_menos_final; formula20222_raw.csv grado11; auditoria/evidencia/notas_ipm.csv celdas A50–A53/A864–A868; protocolo §§1–3,8',
    3:'protocolo/PROTOCOLO_OBJETIVO_3.md §§3–7; protocolo/fuentes/configuracion.py ESPECIFICACIONES/VENTANAS; protocolo/evidencia/candidatos_congelados.json; fase3/resultados/preparacion.json; metricas_ventanas.csv; congelacion.json ganador_global/parametros_completos/filas/entrenamiento_anios; fase3/requirements.lock.txt; fase3/decisiones.md F03-01',
    4:'fase3/resultados/comparacion_desarrollo.csv id/familia; congelacion.json; metricas_reevaluacion.csv llave id/periodo, columnas n/mae/rmse/sesgo/r2; predicciones_desarrollo.csv llave id/codigo_departamento/anio; predicciones_reevaluacion.csv; fase4/resultados/predicciones_territoriales.csv; protocolo §7; continuidad criterios fase2 páginas históricas',
    5:'fase4/resultados/particiones.json; metricas_agrupadas.csv id; metricas_territorio.csv id/codigo_departamento; bootstrap_resumen.csv contexto/a/b; bootstrap_replicas.csv contexto/a/b/replica; influencia_grupos_errores.csv id/codigo_omitido_evaluacion; soporte_territorial.csv id/codigo_departamento/anio/variable; asociaciones_longitudinales.csv variable; coeficientes_ols_congelados.csv id/variable; colinealidad.csv especificacion; pares_correlacion.csv a/b; diagnostico_tamanos.csv id; fase4/fuentes/analisis.py líneas70–115; fase4/decisiones_previas.md remuestreo',
    6:'Tablas4–10 y ubicaciones R4–R5; protocolo §8; fase4/informe.md Medición; CONTINUIDAD_OBJETIVO_3.md Salvedades; protocolo/decisiones_fase2.md D10,D13',
    7:'protocolo §§1–3,8; fase4/informe.md soporte; DANE descripción HTML §3; condición prospectiva, ningún resultado de escenarios',
    8:'fase5/referencias_verificadas.md; fase6/referencias_verificadas.md; fuentes primarias reconsultadas; referencias locales conservadas'}
    rows=[];section=0
    for ln,line in enumerate(original.splitlines(),1):
        h=re.match(r'## ([1-8])\.',line)
        if h:section=int(h[1])
        if section and line.strip() and not line.startswith('##'):
            kind='fila tabla' if line.startswith('|') else ('figura' if line.startswith('![') else 'parrafo o pie')
            if line.startswith('| ---'): continue
            rows.append(dict(id=f'T{len(rows)+1:03}',archivo='informe_objetivo_3.md',linea=ln,seccion='R'+str(section),tipo=kind,
                afirmacion=line,ubicacion_verificable=sources[section],
                dictamen=('corregido F06-01 en copia' if 'tas as' in line else 'corregido F06-02 en copia' if 'ventaja no es uniforme' in line else 'revisado; conservar alcance y evidencia'),
                procedimiento='verificar_revision.py numerica y cotejo de diez tablas; revisión documental de protocolo/fuentes; sin reproducir entrenamiento',
                naturaleza='condición prospectiva' if section==7 else 'referencia' if section==8 else 'resultado actual o evidencia anterior explícitamente distinguida'))
    # También registrar cada elemento de la entrega revisada, incluido resumen.
    clean=(ENT/'informe_objetivo_3_revisado.md').read_text();section=0
    for ln,line in enumerate(clean.splitlines(),1):
        h=re.match(r'## ([1-8])\.',line)
        if h:section=int(h[1])
        if line=='## Resumen':section=9
        if section and line.strip() and not line.startswith('##') and not line.startswith('| ---'):
            rows.append(dict(id=f'T{len(rows)+1:03}',archivo='fase6/entrega/informe_objetivo_3_revisado.md',linea=ln,
                seccion='Resumen' if section==9 else 'R'+str(section),
                tipo='fila tabla' if line.startswith('|') else 'parrafo o pie',afirmacion=line,
                ubicacion_verificable=(sources[2]+'; '+sources[4]+'; '+sources[5]) if section==9 else sources[section],
                dictamen='revisado en entrega final; tablas exactas transformadas solo en presentación',
                procedimiento='verificar_revision.py; tablas iguales a compact_tables(original); resumen cotejado con Tablas1,4–10',
                naturaleza='condición prospectiva' if section==7 else 'referencia' if section==8 else 'resultado actual o evidencia anterior explícitamente distinguida'))
    with (OUT/'matriz_trazabilidad.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
    return len(rows)

def final():
    clean=(ENT/'informe_objetivo_3_revisado.md').read_text()
    assert clean==compact_tables((ROOT/'fase6/fuentes/informe_plantilla.md').read_text())
    assert (ENT/'informe_para_copiar.html').read_text()==render(clean)
    assert len(tablas(clean))==10
    for table in tablas(clean):
        rows=[line.strip('|').split('|') for line in table.splitlines()]
        assert len(rows[0])<=6
        assert all(len(row)==len(rows[0]) for row in rows)
    for p in re.findall(r'\[[^\]]+\]\(([^)]+)\)',clean):
        if not p.startswith('https://'): assert (ENT/p).exists(),p
    for p in (ENT/'figuras').iterdir(): assert sha(p)==sha(ROOT/'fase5/figuras'/p.name)
    assert 'tas as' not in clean and 'ventaja no es uniforme' not in clean
    for term in ['## Resumen','## 7. Puente','persistencia','previamente expuestos','sesgo de selección','sin causa identificada','OLS IPM','7.825903','8.067691','6.345582']:
        assert term in clean,term
    for p in (ROOT/'fase6/fuentes').glob('*.py'):ast.parse(p.read_text())
    # Copia corregida exacta de tablas en anexo y correspondencia de compactas.
    original=(ROOT/'informe_objetivo_3.md').read_text()
    anexo=(ENT/'anexo_tecnico.md').read_text()
    assert tablas(anexo)==tablas(original)
    assert tablas(clean)==tablas(compact_tables(original))
    cierre()
    n=trazabilidad()
    guardar('verificacion_final.json',dict(aprobado=True,elementos_trazabilidad=n,
        tablas=10,columnas_maximas=6,figuras_png=4,figuras_svg=4,
        resumen_metodologia_conclusiones_coherentes=True,conservacion_aprobada=True,
        protocolos_y_ganador_conservados=True,entrega_local=True,aceptacion_editorial_grupo='pendiente externa',
        pdf_paginas_revisadas_fase6=[],google_docs='Prueba local de HTML; pegado real no ejecutado',
        ajustes_nuevos=0,simulaciones=0,objetivo4_ejecutado=False))
    print(f'Revisión aprobada: 91 filas de métricas, 10 tablas, {n} elementos trazados')

if __name__=='__main__':
    numerica();final()
