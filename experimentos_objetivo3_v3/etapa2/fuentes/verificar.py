"""Auditoría independiente desde artefactos guardados: no ajusta ni selecciona externos."""
from piloto import *
import math,re

def independent(y,pred):
    y=list(map(float,y));pred=list(map(float,pred));assert len(y)==len(pred) and y
    assert all(math.isfinite(v) for v in y+pred)
    n=len(y);e=[p-o for p,o in zip(pred,y)];mean=math.fsum(y)/n
    sse=math.fsum(v*v for v in e);den=math.fsum((v-mean)**2 for v in y)
    return dict(n=n,mae=math.fsum(abs(v) for v in e)/n,rmse=math.sqrt(sse/n),sesgo=math.fsum(e)/n,r2=None if den==0 else 1-sse/den)

def verificar():
    verify_freeze();out=OUT/'piloto';assert read(out/'estado.json')['completo']
    panel=loadcsv(PANEL);lookup=panel.set_index(LLAVES)
    cs=candidatos();byid={c['id']:c for c in cs}
    ledger=read(out/'ledger.json');assert ledger['limite']==7200 and not ledger['pendiente']
    assert len({r['etiqueta'] for r in ledger['ajustes']})==len(ledger['ajustes'])
    total=math.fsum(r['segundos'] for r in ledger['ajustes']);assert math.isclose(total,ledger['consumido'],abs_tol=1e-9,rel_tol=0) and total<=7200
    internal=[];failures=[];warns=[];fits={};allframes={}
    # Controles contra matrices y parámetros exactos sin cargar/ajustar modelos.
    for meta in sorted((out/'ajustes').glob('*/ajuste.json')):
        info=read(meta);label=meta.parent.name;c=byid[info['id']]
        match=re.fullmatch(r'e(202[1-5])_(?:i(202[1-4])|externo|repeticion)_(delta_.+)',label);assert match,label
        external=int(match[1]);testyear=int(match[2]) if match[2] else external
        assert external!=2021
        years=[a for a in ANIOS if 2018<a<testyear]
        assert info['entrenamiento']==years
        tr,te=dividir(panel,years,testyear);X,y=matrices_entrenamiento(tr,c)
        assert info['llaves_entrenamiento']==tr[LLAVES].values.tolist() and info['n']==len(tr)
        assert info['entradas']==c['entradas'] and info['parametros_completos']==c['parametros_completos']
        assert info['datos_X_sha256']==__import__('hashlib').sha256(X.tobytes()).hexdigest()
        assert info['datos_y_sha256']==__import__('hashlib').sha256(y.tobytes()).hexdigest()
        assert info['panel_sha256']==sha(PANEL) and info['congelacion_sha256']==sha(OUT/'congelacion_operativa.json') and info['entorno_sha256']==sha(OUT/'entorno.json')
        fits[label]=info
        if info['estado']=='ok':
            assert sha(meta.parent/'modelo.joblib')==info['modelo_sha256']
            if c['familia'] in ('ols','ridge','elastic_net','svr'):
                s=info['transformacion_ajustada'];assert s['n_samples_seen']==len(tr)
                np.testing.assert_allclose(s['mean'],X.mean(axis=0),rtol=1e-12,atol=1e-12)
                np.testing.assert_allclose(s['var'],X.var(axis=0),rtol=1e-12,atol=1e-12)
            else:assert not info['transformacion_ajustada']
            warns.extend(dict(etiqueta=label,**w) for w in info['advertencias'])
        for failure in meta.parent.glob('fallo_*.json'):failures.append(read(failure))
    for kind in ('ajustes','persistencia'):
        for path in sorted((out/kind).glob('*/predicciones.csv')):
            info=read(path.parent/('ajuste.json' if kind=='ajustes' else 'calculo.json'));assert sha(path)==info['predicciones_sha256']
            p=loadcsv(path);assert len(p)==33 and not p.duplicated(LLAVES).any()
            label=path.parent.name;assert p.ajuste.eq(label).all() and p.id.eq(info['id']).all()
            testyear=int(p.anio.iloc[0]);assert p.anio.eq(testyear).all()
            expected=panel[panel.anio==testyear].sort_values(LLAVES)
            assert p[LLAVES].values.tolist()==expected[LLAVES].values.tolist()
            np.testing.assert_array_equal(p.observado,expected[anterior.RESULTADO])
            np.testing.assert_array_equal(p.puntaje_previo,expected.puntaje_previo)
            np.testing.assert_array_equal(p.anio_previo,expected.anio_previo)
            np.testing.assert_array_equal(p.prediccion,p.puntaje_previo+p.cambio_predicho)
            np.testing.assert_array_equal(p.error,p.prediccion-p.observado)
            if kind=='persistencia':np.testing.assert_array_equal(p.prediccion,p.puntaje_previo);assert info['ajustes']==0
            allframes[label]=p
            if etiqueta_interna(label):internal.append(p.assign(externo=int(label[1:5])))
    # Una meta por cada interno ajustado requerido, también si fue inelegible.
    expected_fits=[];score_rows=[];winners=[];externals=[]
    for w in ventanas():
        year=w['externo'];selection=out/f'seleccion_{year}.json';d=read(selection);expected=[i['validacion'] for i in w['internas']]
        scores=[]
        if year==2021:
            assert d['metricas_internas']==[] and d['global_id']=='persistencia' and set(d['especificaciones'].values())=={'persistencia'}
        else:
            for c in cs:
                parts=[];valid=[]
                for i in w['internas']:
                    label=f"e{year}_i{i['validacion']}_{c['id']}"
                    if c['id']!='persistencia':expected_fits.append(label);assert label in fits
                    if label in allframes:parts.append(allframes[label]);valid.append(i['validacion'])
                    else:assert fits[label]['estado']=='numerico' or (out/'ajustes'/label/'prediccion_no_finita.json').exists()
                score=dict(id=c['id'],estado='completo' if valid==expected else 'inelegible',ventanas=valid)
                if valid==expected:
                    j=pd.concat(parts);m=independent(j.observado,j.prediccion);score.update(mae=m['mae'],rmse=m['rmse'])
                scores.append(score);score_rows.append(dict(externo=year,**score))
            saved=d['metricas_internas'];assert len(saved)==100
            for a,b in zip(scores,saved):
                assert a['id']==b['id'] and a['estado']==b['estado'] and a['ventanas']==b['ventanas']
                if a['estado']=='completo':
                    for k in ('mae','rmse'):assert math.isclose(a[k],b[k],rel_tol=0,abs_tol=1e-12)
            # La selección original es determinista usando sus métricas guardadas; auditoría fsum cotejada arriba.
            again=seleccionar(saved,expected,year)
            assert again['global_id']==d['global_id'] and again['especificaciones']==d['especificaciones']
        roles={'procedimiento_v3':d['global_id'],**{f'procedimiento_{s}':v for s,v in d['especificaciones'].items()},'persistencia':'persistencia'}
        ext=loadcsv(out/f'externas_{year}.csv');assert len(ext)==165
        for role,ident in roles.items():
            q=ext[ext.procedimiento==role];assert len(q)==33 and q.id.eq(ident).all() and q.seleccion_sha256.eq(sha(selection)).all()
            label=f'e{year}_externo_{ident}';pd.testing.assert_frame_equal(q[allframes[label].columns].reset_index(drop=True),allframes[label].reset_index(drop=True))
            winners.append(dict(externo=year,procedimiento=role,id=ident))
            if ident!='persistencia':assert datetime.fromisoformat(d['instante_antes_externo'])<datetime.fromtimestamp((out/'ajustes'/label/'modelo.joblib').stat().st_mtime,timezone.utc)
        externals.append(ext)
    assert len(expected_fits)==990
    actual_internals=[label for label in fits if etiqueta_interna(label)]
    assert set(expected_fits)==set(actual_internals)
    assert len(fits)<=1010
    repeats=read(out/'reproducibilidad.json');assert repeats['aprobado'] and len(repeats['repeticiones'])==5
    for year,r in zip(range(2021,2026),repeats['repeticiones']):
        d=read(out/f'seleccion_{year}.json');ident=d['global_id'];assert r['externo']==year and r['id']==ident
        a=allframes[f'e{year}_repeticion_{ident}'];b=allframes[f'e{year}_externo_{ident}']
        np.testing.assert_allclose(a.prediccion,b.prediccion,atol=1e-10,rtol=0)
    refinfo=read(E1/'resultados/referencias_guardadas.json');assert sha(ROOT/refinfo['archivo'])==refinfo['sha256']
    refs=loadcsv(ROOT/refinfo['archivo']);external=pd.concat(externals,ignore_index=True)
    for role in refinfo['roles']:
        q=refs[refs.procedimiento==role].sort_values(LLAVES);expected=panel[panel.anio>=2021].sort_values(LLAVES)
        assert len(q)==165 and q[LLAVES].values.tolist()==expected[LLAVES].values.tolist()
        np.testing.assert_array_equal(q.observado,expected[anterior.RESULTADO])
        for year,h in refinfo['selecciones_sha256'].items():assert q[q.anio==int(year)].seleccion_sha256.eq(h).all()
    csv(OUT/'predicciones_externas.csv',external)
    csv(OUT/'predicciones_internas.csv',pd.concat(internal,ignore_index=True))
    csv(OUT/'metricas_internas.csv',pd.DataFrame(score_rows));csv(OUT/'ganadores.csv',pd.DataFrame(winners))
    metrics=[]
    all_eval=pd.concat([external,refs[refs.procedimiento.isin(refinfo['roles'])]],ignore_index=True)
    for role,q in all_eval.groupby('procedimiento',sort=False):
        assert len(q)==165
        for period,sub in [('2021–2025',q),*[(str(y),g) for y,g in q.groupby('anio')]]:
            metrics.append(dict(procedimiento=role,periodo=period,**independent(sub.observado,sub.prediccion)))
    csv(OUT/'metricas.csv',pd.DataFrame(metrics))
    global_=external[external.procedimiento=='procedimiento_v3'];v2=refs[refs.procedimiento=='procedimiento_v2']
    mae=independent(global_.observado,global_.prediccion)['mae'];den=independent(v2.observado,v2.prediccion)['mae']
    assert math.isfinite(den) and den>0
    goal=condicion_personal(den,mae,True)
    guardar(OUT/'meta.json',dict(completo=True,n=165,mae_v3=mae,mae_v2=den,mejora_porcentual_exacta=goal['mejora'],meta_satisfecha=goal['entregar'],umbral=5,notebook_personal_entregado=False,exploratorio=True))
    guardar(OUT/'fallos_advertencias.json',dict(fallos=failures,advertencias=warns,fuera_0_500=[dict(etiqueta=p.parent.name,n=read(p).get('fuera_0_500',0)) for p in (out/'ajustes').glob('*/ajuste.json') if read(p).get('fuera_0_500',0)]))
    persistence_seconds=math.fsum(read(p)['segundos_calculo'] for p in (out/'persistencia').glob('*/calculo.json'))
    guardar(OUT/'verificacion.json',dict(aprobado=True,completo=True,internos_requeridos=990,internos_documentados=len(actual_internals),predicciones_internas=len(pd.concat(internal)),ajustes_documentados=len(fits),intentos_ledger=len(ledger['ajustes']),segundos_ajustes=ledger['consumido'],segundos_persistencia=persistence_seconds,cinco_repeticiones=True,referencias_guardadas_verificadas=True,metricas_independientes='math.fsum desde CSV de precisión round_trip',regex_E3_01='fullmatch temporal completa; no subcadena _i',E3_02_antecedente_v2=1555,cota_v3_sin_fallos=1010,fallos=len(failures),advertencias=len(warns),sin_ajustes_nuevos=True))
    print('Auditoría completa aprobada:',read(OUT/'meta.json'),flush=True)
if __name__=='__main__':verificar()
