"""Fase4: diagnóstico condicionado a selección congelada; funciones compartidas."""
import sys, os
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'fase3/fuentes'))
import comun as m
import json, subprocess, importlib.metadata, platform, traceback, itertools
import numpy as np
import pandas as pd
OUT=ROOT/'fase4/resultados'
START='9a22b8adc406423fa6829b75e77d7473deffe710'
def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False,default=str)+'\n')
def csv(name,t): t.to_csv(OUT/name,index=False)
def load(name): return json.loads((OUT/name).read_text())
def readcsv(path): return pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip')
def prepare():
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==START
    for manifest in ('fase3/resultados/manifiesto_cierre.json',):
        for p,h in json.loads((ROOT/manifest).read_text()).items(): assert m.huella(ROOT/p)==h,p
    prep=m.read('preparacion.json')
    for p,h in prep['entradas_sha256'].items(): assert m.huella(ROOT/p)==h,p
    assert platform.python_version()==prep['python'] and sys.prefix!=sys.base_prefix
    versions={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
    assert versions==prep['paquetes'], 'Versiones distintas'
    subprocess.run([sys.executable,'-m','pip','check'],check=True)
    data=m.panel(); assert len(data)==198 and m.huella(ROOT/'auditoria/base_analitica_departamento_anio.csv')==m.cfg.BASE_SHA256
    names=subprocess.check_output(['git','ls-files','-z']).decode().split('\0')
    snapshot={p:m.huella(ROOT/p) for p in names if p}
    save('preparacion.json',{'commit_partida':START,'git_inicial':'limpio, comprobado antes de crear fase4','python':platform.python_version(),'paquetes':versions,'snapshot_previo':snapshot,'decisiones_previas_sha256':m.huella(ROOT/'fase4/decisiones_previas.md'),'huellas_verificadas':True,'semilla':m.cfg.SEMILLA})
    print('Huellas, panel198 y versiones exactas aprobados; ninguna evaluación nueva en preparación.')

def territorial():
    assert m.huella(ROOT/'fase4/decisiones_previas.md')==load('preparacion.json')['decisiones_previas_sha256']
    dev=m.panel().query('anio <= 2022').copy()
    frozen=m.read('congelacion.json'); candidates={c['id']:c for c in m.cfg.candidatos()}
    rows=[]; splits=[]; warnings=[]; failures=[]; support=[]
    for spec, ident in frozen['ganadores_especificacion'].items():
        c=candidates[ident]
        assert m.estimator(c).get_params(deep=True)==frozen['parametros_completos'][ident]
        for code in sorted(dev.codigo_departamento.unique()):
            train=dev[dev.codigo_departamento!=code]; test=dev[dev.codigo_departamento==code]
            assert len(train)==128 and len(test)==4 and train.codigo_departamento.nunique()==32
            assert set(test.anio)==set(m.cfg.DESARROLLO) and not set(train.codigo_departamento)&set(test.codigo_departamento)
            splits.append({'id':ident,'excluido':code,'n_entrenamiento':128,'n_evaluacion':4,'anios':list(m.cfg.DESARROLLO),'territorios_entrenamiento':sorted(train.codigo_departamento.unique()),'parametros':frozen['parametros_completos'][ident]})
            try:
                model,r,w=m.fit_predict(c,train,test,'territorio_'+code); warnings+=w
                if c['familia'] in ('ols','ridge'): np.testing.assert_allclose(model[0].mean_,m.x(train,c).mean(axis=0),atol=1e-12)
                r['especificacion']=spec; r['error_absoluto']=abs(r.error);r['error_cuadrado']=r.error**2;rows.append(r)
                for col in m.cfg.ESPECIFICACIONES[spec]:
                    for _,v in test.iterrows():
                        support.append({'id':ident,'codigo_departamento':code,'anio':v.anio,'variable':col,'valor':v[col],'min_entrenamiento':train[col].min(),'max_entrenamiento':train[col].max(),'fuera_rango':bool(v[col]<train[col].min() or v[col]>train[col].max())})
            except Exception:
                failures.append({'id':ident,'territorio':code,'traceback':traceback.format_exc(),'parametros':frozen['parametros_completos'][ident]})
    save('fallos.json',failures);save('advertencias.json',warnings);save('particiones.json',splits)
    if rows: csv('predicciones_territoriales.csv',pd.concat(rows))
    assert not failures, 'Fallos conservados; no cerrar métricas con cobertura incompleta'
    r=pd.concat(rows); assert len(r)==396
    scores=[]
    for keys,g in r.groupby(['id','especificacion']):
        scores.append({'id':keys[0],'especificacion':keys[1],'n':len(g),**m.metrics(g.observado,g.prediccion)})
    csv('metricas_agrupadas.csv',pd.DataFrame(scores))
    for name, cols in [('metricas_territorio.csv',['id','codigo_departamento','departamento']),('metricas_anio.csv',['id','anio'])]:
        csv(name,pd.DataFrame([{**dict(zip(cols,k)),'n':len(g),**m.metrics(g.observado,g.prediccion)} for k,g in r.groupby(cols)]))
    csv('soporte_territorial.csv',pd.DataFrame(support))
    print(pd.DataFrame(scores).to_string(index=False))
    print('99 ajustes, 396 predicciones; fallos:',len(failures),'advertencias:',len(warnings))

def bootstrap(table,pairs,context):
    # Filas alineadas por territorio/año, grupos con todos sus años.
    pivot=table.assign(abs_error=lambda t:abs(t.error)).pivot(index=['codigo_departamento','anio'],columns='id',values='abs_error')
    territory=pivot.groupby(level=0).mean(); assert len(territory)==33 and not territory.isna().any().any()
    rng=np.random.default_rng(m.cfg.SEMILLA);indices=rng.integers(0,33,size=(2000,33)); summaries=[];rep=[]
    for a,b in pairs:
        diff=(territory[a]-territory[b]).to_numpy(); samples=diff[indices].mean(axis=1)
        lo,hi=np.quantile(samples,[.025,.975]);summaries.append({'contexto':context,'a':a,'b':b,'delta_mae':float(diff.mean()),'percentil_2_5':float(lo),'percentil_97_5':float(hi),'replicas':2000})
        rep.extend({'contexto':context,'a':a,'b':b,'replica':i+1,'delta_mae':float(v)} for i,v in enumerate(samples))
    return summaries,rep

def robustez():
    dev=m.panel().query('anio <= 2022').copy(); r=readcsv(OUT/'predicciones_territoriales.csv'); frozen=m.read('congelacion.json')
    ids=list(frozen['ganadores_especificacion'].values()); summ,rep=bootstrap(r,list(itertools.combinations(ids,2)),'territorial_desarrollo')
    temporal=readcsv(ROOT/'fase3/resultados/predicciones_reevaluacion.csv')
    s,p=bootstrap(temporal,[(frozen['ganador_global'],b) for b in ['media','ols_ipm','ols_tasas','ols_ambas']],'temporal_cerrado_2023_2024');summ+=s;rep+=p
    csv('bootstrap_resumen.csv',pd.DataFrame(summ));csv('bootstrap_replicas.csv',pd.DataFrame(rep))
    assoc=[];cols=m.cfg.ESPECIFICACIONES['ambas'];y=m.cfg.RESULTADO
    means=dev.groupby('codigo_departamento')[[*cols,y]].mean()
    within=dev[[*cols,y]]-dev.groupby('codigo_departamento')[[*cols,y]].transform('mean')
    double=within-(dev.groupby('anio')[[*cols,y]].transform('mean')-dev[[*cols,y]].mean())
    for col in cols:
        assoc.append({'variable':col,'r_entre_territorios':means[col].corr(means[y]),'r_dentro_territorio':within[col].corr(within[y]),'r_doble_centrado':double[col].corr(double[y]),'n_territorios':33,'n_filas':132})
    csv('asociaciones_longitudinales.csv',pd.DataFrame(assoc))
    corr=dev[cols].corr();csv('correlaciones_predictores.csv',corr.rename_axis('variable').reset_index())
    conditioning=[];coeff=[]
    for spec,features in m.cfg.ESPECIFICACIONES.items():
        X=dev[features].to_numpy();z=(X-X.mean(axis=0))/X.std(axis=0);sv=np.linalg.svd(z,compute_uv=False)
        conditioning.append({'especificacion':spec,'numero_condicion':float(sv[0]/sv[-1]),'singular_min':float(sv[-1]),'rango':int(np.linalg.matrix_rank(z))})
        transform=frozen['transformaciones']['ols_'+spec]
        coeff.extend({'id':'ols_'+spec,'variable':col,'coef_por_sd_entrenamiento':coef,'sd_entrenamiento':scale,'coef_por_punto_porcentual':coef/scale} for col,coef,scale in zip(features,transform['coef'],transform['scale']))
    csv('colinealidad.csv',pd.DataFrame(conditioning));csv('coeficientes_ols_congelados.csv',pd.DataFrame(coeff))
    sizes=dev[['codigo_departamento','anio','n_estudiantes_saber']]
    merged=r.merge(sizes,on=['codigo_departamento','anio'],validate='many_to_one')
    diagnostics=[];influence=[];distribution=[]
    for ident,g in merged.groupby('id'):
        diagnostics.append({'id':ident,'r_abs_error_log_n':g.error_absoluto.corr(np.log(g.n_estudiantes_saber)),'min_n':int(g.n_estudiantes_saber.min()),'max_n':int(g.n_estudiantes_saber.max())})
        for code in sorted(g.codigo_departamento.unique()):
            h=g[g.codigo_departamento!=code];influence.append({'id':ident,'codigo_omitido_evaluacion':code,'n':len(h),**m.metrics(h.observado,h.prediccion)})
        for q,v in g.error_absoluto.quantile([0,.25,.5,.75,.9,.95,1]).items():distribution.append({'id':ident,'cuantil':q,'error_absoluto':v})
    csv('diagnostico_tamanos.csv',pd.DataFrame(diagnostics));csv('influencia_grupos_errores.csv',pd.DataFrame(influence));csv('distribucion_errores.csv',pd.DataFrame(distribution))
    print(pd.DataFrame(summ).to_string(index=False));print(pd.DataFrame(assoc).head().to_string(index=False));print(pd.DataFrame(conditioning).to_string(index=False))
