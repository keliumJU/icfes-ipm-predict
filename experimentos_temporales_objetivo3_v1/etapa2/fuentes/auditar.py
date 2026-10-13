"""Auditoría independiente: no importa selector/fit/métricas del piloto ni modelos."""
import json,math,hashlib
from pathlib import Path
from fractions import Fraction
import numpy as np,pandas as pd
ROOT=Path(__file__).absolute().parents[3];E2=ROOT/'experimentos_temporales_objetivo3_v1/etapa2';OUT=E2/'resultados'
K=['codigo_departamento','anio']
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def csv(p):return pd.read_csv(p,dtype={'codigo_departamento':str},float_precision='round_trip')
def same(a,b):
    assert a.shape==b.shape and a.columns.tolist()==b.columns.tolist() and a.index.equals(b.index)
    for col in a:
        x,y=a[col],b[col];assert np.array_equal(x.isna(),y.isna())
        assert np.array_equal(x[~x.isna()].to_numpy(),y[~y.isna()].to_numpy()),col
    return True
def metrics(q):
    errors=[float(x)-float(y) for x,y in zip(q.prediccion,q.observado)]
    assert errors and all(math.isfinite(e) for e in errors)
    return dict(n=len(errors),mae=math.fsum(map(abs,errors))/len(errors),rmse=math.sqrt(math.fsum(e*e for e in errors)/len(errors)),sesgo=math.fsum(errors)/len(errors))
def select(rows,conf,group=None):
    candidates=conf['configuraciones'];pool=[]
    for r,c in zip(rows,candidates):
        if r['estado']=='completo' and (group is None or c['especificacion'] in (None,group)):
            pool.append((r,c))
    m=min(r['mae'] for r,c in pool);pool=[(r,c) for r,c in pool if r['mae']<=m+.1]
    m=min(r['rmse'] for r,c in pool);pool=[(r,c) for r,c in pool if r['rmse']<=m+.1]
    return min(pool,key=lambda z:(z[1]['n_ajustadas'],conf['orden_familias'].index(z[1]['familia']),z[1]['orden']))[1]['id']
def guardar(name,obj):
    with (OUT/name).open('x') as f:json.dump(obj,f,indent=2,ensure_ascii=False,allow_nan=False)
def main():
    conf=read(ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json');spec=read(ROOT/'diseno_temporal_objetivo3_v1/ESPECIFICACION_PROPUESTA.json')
    inherited=spec['heredado'];s=csv(ROOT/inherited['fuente_archivo']);s.codigo_departamento=s.codigo_departamento.str.zfill(2)
    assert sha(ROOT/inherited['fuente_archivo'])==inherited['fuente_sha256'] and sha(ROOT/inherited['derivado_archivo'])==inherited['derivado_sha256']
    p=s.sort_values(K).reset_index(drop=True);g=p.groupby('codigo_departamento',sort=False)
    p['anio_previo']=g.anio.shift(1).astype('Int64');p['puntaje_previo']=g.prom_punt_global.shift(1);p['cambio_observado']=p.prom_punt_global-p.puntaje_previo
    for col in [v.removeprefix('cambio_') for v in conf['grupos']['cambio_ambas'][1:]]:
        p['previo_'+col]=g[col].shift(1);p['cambio_'+col]=p[col]-p['previo_'+col]
    p['intervalo']=p.anio-p.anio_previo;p['fuente_sha256']=inherited['fuente_sha256'];same(p,csv(ROOT/inherited['derivado_archivo']))
    assert len(p)==231 and p.codigo_departamento.nunique()==33 and len(p[p.anio>2018])==198
    internal,external=csv(OUT/'predicciones_internas.csv'),csv(OUT/'predicciones_externas.csv')
    recs=read(OUT/'registros_internos.json');signatures=read(OUT/'firmas_internas.json');ledger=read(OUT/'ledger.json')
    assert len(internal)==11880 and len(external)==1155 and len(recs)==144 and len(signatures)==360
    ids=[c['id'] for c in conf['configuraciones']];cmap={c['id']:c for c in conf['configuraciones']}
    assert set(internal.id)==set(ids) and not internal.duplicated(['externo','id',*K]).any()
    roles=['global',*conf['grupos'],'persistencia'];assert set(external.procedimiento)==set(roles)
    assert not external.duplicated(['procedimiento',*K]).any()
    for frame in (internal,external):
        assert np.isfinite(frame[['observado','prediccion','cambio_predicho','error']].to_numpy(float)).all()
        assert frame.origen.eq('recencia_h2').all()
        for _,part in frame.groupby('ajuste',sort=False):
            test=p[p.anio.eq(int(part.anio.iloc[0]))].reset_index(drop=True);part=part.drop_duplicates(K).reset_index(drop=True)
            same(part[K+['observado']].rename(columns={'observado':'prom_punt_global'}),test[K+['prom_punt_global']])
            same(part[K+['puntaje_previo']],test[K+['puntaje_previo']])
            assert np.array_equal(part.prediccion,(part.puntaje_previo+part.cambio_predicho))
            assert np.array_equal(part.error,(part.prediccion-part.observado))
            if part.id.iloc[0]=='persistencia':assert part.cambio_predicho.eq(0).all()
    for w in conf['ventanas']:
        ext=w['externo'];decision=read(OUT/f'seleccion_{ext}.json');assert decision['antes_externo']
        rows=[r for r in recs if r['externo']==ext]
        if ext==2021:assert not rows and decision['decision']['global_id']=='persistencia' and all(v=='persistencia' for v in decision['decision']['especificaciones'].values())
        else:
            assert [r['id'] for r in rows]==ids
            for r in rows:
                assert r['estado']=='completo' and r['ventanas']==[i['validacion'] for i in w['internas']]
                part=internal[(internal.externo==ext)&(internal.id==r['id'])]
                assert len(part)==33*len(w['internas']);m=metrics(part)
                assert abs(r['mae']-m['mae'])<=1e-12 and abs(r['rmse']-m['rmse'])<=1e-12
                rational=sum((abs(Fraction.from_float(float(a))-Fraction.from_float(float(b))) for a,b in zip(part.prediccion,part.observado)),Fraction(0))/len(part)
                assert abs(float(rational)-r['mae'])<=1e-12
            assert select(rows,conf)==decision['decision']['global_id']
            assert all(select(rows,conf,group)==ident for group,ident in decision['decision']['especificaciones'].items())
        for role,ident in {'global':decision['decision']['global_id'],**decision['decision']['especificaciones'],'persistencia':'persistencia'}.items():
            part=external[(external.externo==ext)&(external.procedimiento==role)];assert len(part)==33 and part.id.eq(ident).all()
        rep=csv(OUT/'repeticiones'/f'{ext}.csv');primary=external[(external.externo==ext)&(external.procedimiento=='global')].reset_index(drop=True)
        same(rep[K+['observado']],primary[K+['observado']]);np.testing.assert_allclose(rep.prediccion,primary.prediccion,atol=1e-10,rtol=0)
    # Matrices/objetivos/pesos y scaler de cada ajuste real, independientemente del fit.
    meta_count=0
    for file in sorted((OUT/'metadatos').glob('*.json')):
        meta=read(file);c=cmap[meta['id']];wm=meta['pesos'];train=p[p.anio.isin(wm['anios_train'])].sort_values(K).reset_index(drop=True)
        assert max(train.anio)==wm['ancla_train'];assert train[K].values.tolist()==wm['llaves']
        raw=[2**(-(int(train.anio.max())-int(a))/2) for a in train.anio];total=math.fsum(raw)
        weights=[1.]*len(raw) if len(set(raw))==1 else [len(raw)*v/total for v in raw]
        assert wm['pesos_brutos']==raw and wm['pesos']==weights and wm['suma_brutos']==total
        assert all(v>0 and math.isfinite(v) for v in weights) and abs(math.fsum(weights)-len(train))<=1e-12
        X=train[c['entradas']].to_numpy(float);y=train.cambio_observado.to_numpy(float)
        assert np.array_equal(np.array(meta['X']),X) and np.array_equal(np.array(meta['y']),y)
        assert meta['entradas']==c['entradas'] and meta['parametros']==c['parametros_completos'] and meta['semilla']==20261010 and meta['routing']==False
        assert meta['python']=='3.12.14' and meta['sklearn']=='1.9.1'
        expected=[] if len(set(raw))==1 else ['escalado__sample_weight','modelo__sample_weight'] if c['familia']=='mediana' else ['sample_weight']
        assert meta['ruta_fit']==expected
        assert not any(n['categoria'] in ('RuntimeWarning','ConvergenceWarning') for n in meta['advertencias'])
        if c['familia']=='mediana':
            means=[math.fsum(w*x for w,x in zip(weights,X[:,j]))/math.fsum(weights) for j in range(X.shape[1])]
            variances=[math.fsum(w*(x-means[j])**2 for w,x in zip(weights,X[:,j]))/math.fsum(weights) for j in range(X.shape[1])]
            np.testing.assert_allclose(meta['transformaciones']['media'],means,atol=1e-12,rtol=0)
            np.testing.assert_allclose(meta['transformaciones']['varianza'],variances,atol=1e-12,rtol=0)
        meta_count+=1
    assert not ledger['pendiente'] and ledger['limite']==7200. and ledger['consumido']<7200.
    assert abs(math.fsum(r['segundos'] for r in ledger['ajustes'])-ledger['consumido'])<1e-9
    assert len(ledger['ajustes'])<=378 and all(r['estado']=='ok' for r in ledger['ajustes'])
    assert sum('_i20' in r['etiqueta'] for r in ledger['ajustes'])==350
    assert sum('_externo_' in r['etiqueta'] for r in ledger['ajustes'])<=24 and sum('_repeticion_' in r['etiqueta'] for r in ledger['ajustes'])<=4
    assert meta_count==len(ledger['ajustes'])
    for r in ledger['ajustes']:
        assert r['segundos']>0
        for path,h in r['artefactos'].items():assert sha(path)==h
        if '_externo_' in r['etiqueta']:assert r['contexto']['seleccion_sha256']==sha(OUT/f'seleccion_{r["contexto"]["externo"]}.json')
    # Copias exactas, train/contexto idénticos, representante menor externo.
    sig={(r['externo'],r['id'],r['validacion']):r['firma'] for r in signatures}
    for (ident,year),part in internal.groupby(['id','anio'],sort=False):
        copies=[];contexts=[]
        for ext,copy in part.groupby('externo',sort=True):
            copies.append(copy.drop(columns=['externo','ajuste']).reset_index(drop=True));contexts.append(sig[(int(ext),ident,int(year))])
        assert all(x==contexts[0] for x in contexts)
        for copy in copies[1:]:same(copy,copies[0])
    unique=internal.sort_values(['externo','id',*K]).drop_duplicates(['id',*K],keep='first').reset_index(drop=True);assert len(unique)==4752
    reps=unique.set_index(['id',*K]).externo;lineage=internal[['externo','id',*K,'ajuste']].copy()
    lineage['externo_representante']=[int(reps.loc[tuple(row)]) for row in lineage[['id',*K]].itertuples(index=False,name=None)]
    unique.to_csv(OUT/'internas_unicas.csv',index=False);lineage.to_csv(OUT/'linaje_internas.csv',index=False)
    same(unique,csv(OUT/'internas_unicas.csv'));same(lineage,csv(OUT/'linaje_internas.csv'))
    # Referencias independientes del piloto: archivo guardado versus previo reconstruido.
    expected=p[p.anio.between(2021,2025)].sort_values(K).reset_index(drop=True)[K+['prom_punt_global','puntaje_previo']].rename(columns={'prom_punt_global':'observado','puntaje_previo':'prediccion'})
    v5=csv(ROOT/'experimentos_objetivo3_v5/etapa2/resultados/predicciones_externas.csv');v3=csv(ROOT/'experimentos_objetivo3_v3/etapa2/resultados/predicciones_externas.csv')
    v5=v5[v5.procedimiento=='global'].sort_values(K).reset_index(drop=True);v3=v3[v3.procedimiento=='procedimiento_v3'].sort_values(K).reset_index(drop=True)
    same(expected,v5[expected.columns]);same(expected,v3[expected.columns])
    primary=external[external.procedimiento=='global'].sort_values(K).reset_index(drop=True)
    same(primary[K+['observado']],expected[K+['observado']]);assert len(primary)==165
    base=metrics(expected);globalm=metrics(primary);assert math.isfinite(base['mae']) and base['mae']>0
    improvement=100*(base['mae']-globalm['mae'])/base['mae']
    guardar('meta.json',dict(primario='recencia_h2/global',n=165,mae_persistencia=base['mae'],mae_recencia_global=globalm['mae'],mejora_porcentaje=improvement,umbral_original=5,cumple=improvement>=5,delta_mae_v5=globalm['mae']-metrics(v5)['mae'],exploratorio=True,confirmacion_independiente=False,causalidad=False))
    # Rechazos semánticos controlados: 1e-11, llaves, orden, nofinito; intfloat0 equivalente.
    a=pd.DataFrame({'x':[0,1]});same(a,pd.DataFrame({'x':[0.,1.]}));tests={}
    for name,b in [('1e-11',pd.DataFrame({'x':[1e-11,1.]})),('orden',pd.DataFrame({'x':[1.,0.]})),('campos',pd.DataFrame({'y':[0,1]})),('no_finito',pd.DataFrame({'x':[np.inf,1.]}))]:
        try:same(a,b)
        except AssertionError:tests[name]=True
        else:raise AssertionError('Control no rechazó '+name)
    keys_a=pd.DataFrame({'codigo_departamento':['01','02'],'anio':[2021,2021]});keys_b=keys_a.copy();keys_b.loc[0,'codigo_departamento']='99'
    try:same(keys_a,keys_b)
    except AssertionError:tests['llaves']=True
    else:raise AssertionError('Llave distinta aceptada')
    guardar('auditoria_independiente.json',dict(aprobado=True,procedimiento='Fuente reconstruida; igualdad exacta round_trip; MAE/RMSE/sesgo fsum y selector independientes; sin importar piloto ni cargar modelos',internas=11880,unicas=4752,linaje=11880,externas=1155,registros=144,firmas=360,metadata_modelos=meta_count,repeticiones=5,referencias=165,tests=tests,intfloat0_equivalente=True,segundos=ledger['consumido'],intentos=len(ledger['ajustes']),fits_historicos=0,modelos_historicos_cargados=0))
    print(json.dumps(read(OUT/'meta.json'),ensure_ascii=False))
if __name__=='__main__':main()
