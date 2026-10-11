"""Auditoría independiente desde artefactos guardados: no ajusta ni selecciona externos."""
from piloto import *
import math,re

def etiqueta_interna(label):return re.fullmatch(r'e202[2-5]_i202[1-4]_.+',label) is not None

def independent(y,pred):
    y=list(map(float,y));pred=list(map(float,pred));assert len(y)==len(pred) and y
    assert all(math.isfinite(v) for v in y+pred)
    n=len(y);e=[p-o for p,o in zip(pred,y)];mean=math.fsum(y)/n
    sse=math.fsum(v*v for v in e);den=math.fsum((v-mean)**2 for v in y)
    return dict(n=n,mae=math.fsum(abs(v) for v in e)/n,rmse=math.sqrt(sse/n),sesgo=math.fsum(e)/n,r2=None if den==0 else 1-sse/den)

def referencias_lectura(panel):
    refinfo=read(E1/'resultados/referencias_guardadas.json')
    check_hashes(refinfo['archivos_sha256']);check_hashes(refinfo['selecciones_sha256'])
    sources=[('v3',ROOT/'experimentos_objetivo3_v3/etapa2/resultados',{'v3':'procedimiento_v3'}),
             ('v2',ROOT/'experimentos_objetivo3_v2/fase3/resultados',dict(v2='procedimiento_v2',v1='referencia_v1',media='media',ols_ipm='ols_ipm_00',ols_tasas='ols_tasas_00',ols_ambas='ols_ambas_00'))]
    sources.append(('v4',ROOT/'experimentos_objetivo3_v4/etapa2/resultados',{'v4':'procedimiento_v4'}))
    result={};expected=panel[panel.anio>=2021].sort_values(LLAVES)
    for version,base,roles in sources:
        frame=compartido.normalizar_codigos(loadcsv(base/'predicciones_externas.csv'))
        for year in range(2021,2026):
            sp=base/'piloto'/f'seleccion_{year}.json';d=read(sp);q=frame[frame.anio==year]
            assert d['externo']==year and q.seleccion_sha256.eq(sha(sp)).all()
            assert q[q.procedimiento=='procedimiento_'+version].id.eq(d['global_id']).all()
            for group,ident in d['especificaciones'].items():assert q[q.procedimiento=='procedimiento_'+group].id.eq(ident).all()
        for name,role in roles.items():
            q=frame[frame.procedimiento==role].sort_values(LLAVES).reset_index(drop=True)
            assert len(q)==165 and not q.duplicated(LLAVES).any()
            assert q[LLAVES].values.tolist()==expected[LLAVES].values.tolist()
            np.testing.assert_array_equal(q.observado,expected[anterior.RESULTADO])
            assert np.isfinite(q.prediccion).all()
            if name not in ('v2','v3','v4'):assert q.id.eq(role).all()
            result[name]=q
    np.testing.assert_array_equal(result['v3'].prediccion,expected.puntaje_previo)
    assert result['v3'].id.eq('persistencia').all()
    return result

def auditar_artefactos(out,panel):
    assert read(out/'estado.json')['completo']
    lookup=panel.set_index(LLAVES)
    auditor=Runner.__new__(Runner);auditor.out=out;auditor.budget=type('B',(),{'data':read(out/'ledger.json')})();auditor.verify_checkpoint()
    cs=candidatos();byid={c['id']:c for c in cs}
    orden=auditar_orden(out,cs)
    ledger=read(out/'ledger.json');assert ledger['limite']==read(out/'contexto.json')['limite'] and not ledger['pendiente']
    assert len({r['etiqueta'] for r in ledger['ajustes']})==len(ledger['ajustes'])
    total=math.fsum(r['segundos'] for r in ledger['ajustes']);assert math.isclose(total,ledger['consumido'],abs_tol=1e-9,rel_tol=0) and total<=7200
    if read(out/'contexto.json')['origen']=='real':
        assert datetime.fromisoformat(read(OUT/'congelacion_operativa.json')['instante'])<datetime.fromtimestamp((out/'ledger.json').stat().st_mtime,timezone.utc)
    internal=[];failures=[];warns=[];fits={};allframes={}
    # Controles contra matrices y parámetros exactos sin cargar/ajustar modelos.
    for meta in sorted((out/'ajustes').glob('*/ajuste.json')):
        info=read(meta);label=meta.parent.name;c=byid[info['id']]
        match=re.fullmatch(r'e(202[1-5])_(?:i(202[1-4])|externo|repeticion)_(.+)',label);assert match,label
        external=int(match[1]);testyear=int(match[2]) if match[2] else external
        assert external!=2021
        years=[a for a in anterior.ANIOS if 2018<a<testyear]
        assert info['entrenamiento']==years
        tr,te=dividir(panel,years,testyear);X,y=matrices_entrenamiento(tr,c)
        assert info['llaves_entrenamiento']==tr[LLAVES].values.tolist() and info['n']==len(tr)
        assert info['entradas']==c['entradas'] and info['parametros_completos']==c['parametros_completos']
        assert info['datos_X_sha256']==__import__('hashlib').sha256(X.tobytes()).hexdigest()
        assert info['datos_y_sha256']==__import__('hashlib').sha256(y.tobytes()).hexdigest()
        assert info['panel_sha256']==sha(PANEL) and info['entorno_sha256']==sha(OUT/'entorno.json')
        if info['origen']=='real':assert info['congelacion_sha256']==sha(OUT/'congelacion_operativa.json')
        fits[label]=info
        if info['estado']=='ok':
            assert sha(meta.parent/'modelo.joblib')==info['modelo_sha256']
            if c['familia'] in ('mediana',):
                s=info['transformacion_ajustada'];assert s['n_samples_seen']==len(tr)
                np.testing.assert_allclose(s['mean'],X.mean(axis=0),rtol=1e-12,atol=1e-12)
                np.testing.assert_allclose(s['var'],X.var(axis=0),rtol=1e-12,atol=1e-12)
            else:
                assert not info['transformacion_ajustada']
                assert info['mediana_train'] is None
            assert sha(meta.parent/'entradas_entrenamiento.csv')==info['entradas_entrenamiento_sha256']
            igualdad_exacta(loadcsv(meta.parent/'entradas_entrenamiento.csv'),tr[[*LLAVES,*c['entradas'],'cambio_observado']].reset_index(drop=True))
            assert info['tiempo'] in ledger['ajustes'] and info['tiempo']['estado']=='ok'
            warns.extend(dict(etiqueta=label,**w) for w in info['advertencias'])
        for failure in meta.parent.glob('fallo_*.json'):failures.append(read(failure))
    for kind in ('ajustes','persistencia'):
        for path in sorted((out/kind).glob('*/predicciones.csv')):
            info=read(path.parent/('ajuste.json' if kind=='ajustes' else 'calculo.json'));assert sha(path)==info['predicciones_sha256']
            assert sha(path.parent/'entradas_prediccion.csv')==info['entradas_prediccion_sha256']
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
            igualdad_exacta(loadcsv(path.parent/'entradas_prediccion.csv'),expected[[*LLAVES,*byid[info['id']]['entradas']]].reset_index(drop=True))
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
                score=dict(id=c['id'],estado='completo' if valid==expected else 'inelegible',ventanas=valid,mae=None,rmse=None,razon=None if valid==expected else 'numérico/convergencia persistente; internas incompletas')
                if valid==expected:
                    j=pd.concat(parts);m=independent(j.observado,j.prediccion);score.update(mae=m['mae'],rmse=m['rmse'])
                scores.append(score);score_rows.append(dict(externo=year,**score))
            saved=d['metricas_internas'];assert len(saved)==36
            for a,b in zip(scores,saved):
                assert a['id']==b['id'] and a['estado']==b['estado'] and a['ventanas']==b['ventanas']
                if a['estado']=='completo':
                    for k in ('mae','rmse'):assert math.isclose(a[k],b[k],rel_tol=0,abs_tol=1e-12)
            # La selección original es determinista usando sus métricas guardadas; auditoría fsum cotejada arriba.
            again=seleccionar(saved,expected,year)
            assert again['global_id']==d['global_id'] and again['especificaciones']==d['especificaciones']
        roles={'global':d['global_id'],**{s:v for s,v in d['especificaciones'].items()},'persistencia':'persistencia'}
        ext=loadcsv(out/f'externas_{year}.csv');assert len(ext)==231
        for role,ident in roles.items():
            q=ext[ext.procedimiento==role];assert len(q)==33 and q.id.eq(ident).all() and q.seleccion_sha256.eq(sha(selection)).all()
            label=f'e{year}_externo_{ident}';igualdad_exacta(q[allframes[label].columns].reset_index(drop=True),allframes[label].reset_index(drop=True))
            winners.append(dict(externo=year,procedimiento=role,id=ident))
            if ident!='persistencia':assert datetime.fromisoformat(d['instante_antes_externo'])<datetime.fromisoformat(fits[label]['instante_inicio'])
        externals.append(ext)
    assert len(expected_fits)==350
    actual_internals=[label for label in fits if etiqueta_interna(label)]
    assert set(expected_fits)==set(actual_internals)
    if not failures:assert len(fits)<=378
    expected_externals={f"e{w['externo']}_externo_{ident}" for w in ventanas() for ident in ids_externos(read(out/f"seleccion_{w['externo']}.json")) if ident!='persistencia'}
    expected_repeats={f"e{w['externo']}_repeticion_{read(out/f"seleccion_{w['externo']}.json")['global_id']}" for w in ventanas() if read(out/f"seleccion_{w['externo']}.json")['global_id']!='persistencia'}
    assert set(fits)==set(expected_fits)|expected_externals|expected_repeats
    assert len(ledger['ajustes'])==sum(info['intento'] for info in fits.values())
    repeats=read(out/'reproducibilidad.json');assert repeats['aprobado'] and len(repeats['repeticiones'])==5
    for year,r in zip(range(2021,2026),repeats['repeticiones']):
        d=read(out/f'seleccion_{year}.json');ident=d['global_id'];assert r['externo']==year and r['id']==ident
        a=allframes[f'e{year}_repeticion_{ident}'];b=allframes[f'e{year}_externo_{ident}']
        np.testing.assert_allclose(a.prediccion,b.prediccion,atol=1e-10,rtol=0)
    cobertura(pd.concat(externals,ignore_index=True),panel.codigo_departamento.unique())
    return dict(orden=orden,ledger=ledger,internal=internal,failures=failures,warns=warns,fits=fits,score_rows=score_rows,winners=winners,externals=externals,actual_internals=actual_internals)

def verificar():
    verify_freeze();out=OUT/'piloto';panel=loadcsv(PANEL)
    data=auditar_artefactos(out,panel)
    orden=data['orden'];ledger=data['ledger'];internal=data['internal'];failures=data['failures'];warns=data['warns'];fits=data['fits'];score_rows=data['score_rows'];winners=data['winners'];externals=data['externals'];actual_internals=data['actual_internals']
    refs_map=referencias_lectura(panel)
    external=pd.concat(externals,ignore_index=True)
    refs=pd.concat([r.assign(procedimiento='referencia_'+name) for name,r in refs_map.items()],ignore_index=True)
    ref_roles=refs.procedimiento.unique().tolist()
    for role,q in external.groupby('procedimiento'):
        expected=panel[panel.anio>=2021].sort_values(LLAVES)
        q=q.sort_values(LLAVES)
        assert len(q)==165 and not q.duplicated(LLAVES).any()
        assert q[LLAVES].values.tolist()==expected[LLAVES].values.tolist()
        np.testing.assert_array_equal(q.observado,expected[anterior.RESULTADO])
    np.testing.assert_array_equal(external[external.procedimiento=='persistencia'].sort_values(LLAVES).prediccion,refs_map['v3'].prediccion)
    csv(OUT/'predicciones_externas.csv',external)
    csv(OUT/'predicciones_internas.csv',pd.concat(internal,ignore_index=True))
    csv(OUT/'metricas_internas.csv',pd.DataFrame(score_rows));csv(OUT/'ganadores.csv',pd.DataFrame(winners))
    metrics=[]
    all_eval=pd.concat([external,refs[refs.procedimiento.isin(ref_roles)]],ignore_index=True)
    for role,q in all_eval.groupby('procedimiento',sort=False):
        assert len(q)==165
        for period,sub in [('2021–2025',q),*[(str(y),g) for y,g in q.groupby('anio')]]:
            metrics.append(dict(procedimiento=role,periodo=period,**independent(sub.observado,sub.prediccion)))
    for role,q in all_eval.groupby('procedimiento',sort=False):
        for code,sub in q.groupby('codigo_departamento'):
            metrics.append(dict(procedimiento=role,periodo='territorio_'+code,**independent(sub.observado,sub.prediccion)))
    csv(OUT/'metricas.csv',pd.DataFrame(metrics))
    a=external[external.procedimiento=='global'].sort_values(LLAVES).reset_index(drop=True)
    b=refs_map['v3'].sort_values(LLAVES).reset_index(drop=True)
    dif=a[LLAVES+['observado','prediccion']].copy();dif['prediccion_referencia']=b.prediccion
    dif['delta_error_absoluto']=abs(a.error)-abs(b.prediccion-b.observado)
    dif['delta_error_cuadratico']=a.error**2-(b.prediccion-b.observado)**2
    csv(OUT/'diferencias_emparejadas.csv',dif);csv(OUT/'deterioros.csv',dif[dif.delta_error_absoluto>0])
    global_=external[external.procedimiento=='global'];v2=refs[refs.procedimiento=='referencia_v3']
    mae=independent(global_.observado,global_.prediccion)['mae'];den=independent(v2.observado,v2.prediccion)['mae']
    assert math.isfinite(den) and den>0
    assert den==3.429267191379531
    goal=compartido.condicion_personal(den,mae,True)
    guardar(OUT/'meta.json',dict(completo=True,n=165,mae_v5=mae,mae_referencia=den,mejora_porcentual_exacta=goal['mejora'],meta_satisfecha=goal['entregar'],umbral=5,notebook_personal_entregado=False,exploratorio=True))
    guardar(OUT/'fallos_advertencias.json',dict(fallos=failures,advertencias=warns,fuera_0_500=[dict(etiqueta=p.parent.name,n=read(p).get('fuera_0_500',0)) for p in (out/'ajustes').glob('*/ajuste.json') if read(p).get('fuera_0_500',0)]))
    persistence_seconds=math.fsum(read(p)['segundos_calculo'] for p in (out/'persistencia').glob('*/calculo.json'))
    guardar(OUT/'verificacion.json',dict(aprobado=True,completo=True,internos_requeridos=350,internos_documentados=len(actual_internals),predicciones_internas=len(pd.concat(internal)),ajustes_documentados=len(fits),intentos_ledger=len(ledger['ajustes']),segundos_ajustes=ledger['consumido'],orden_ledger=orden,externas_por_procedimiento={r:165 for r in external.procedimiento.unique()},segundos_persistencia=persistence_seconds,cinco_repeticiones=True,referencias_guardadas_verificadas=True,metricas_independientes='math.fsum desde CSV de precisión round_trip',regex_E3_01='fullmatch temporal completa; no subcadena _i',E3_02_antecedente_v2=1555,cota_v5_sin_fallos=378,fallos=len(failures),advertencias=len(warns),sin_ajustes_nuevos=True))
    print('Auditoría completa aprobada:',read(OUT/'meta.json'),flush=True)
if __name__=='__main__':verificar()
