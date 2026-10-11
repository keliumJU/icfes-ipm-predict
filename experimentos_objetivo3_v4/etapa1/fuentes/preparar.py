"""Preflight, estructura y diagnóstico de CSV históricos. Cero fits del panel."""
from comun_v4 import *
import subprocess,platform,importlib.metadata as md,hashlib

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def check_hashes(mapping):
    for p,h in mapping.items():assert sha(ROOT/p)==h,p

def antecedentes():
    count=0;historical=[]
    for stage,commit in [('etapa1','45fa051ffadc0fc25a326605069dd2f93920898f'),('etapa2','15dcf122897d16bfde0e50da316d8f6c6dffdfd4')]:
        base=ROOT/'experimentos_objetivo3_v3'/stage/'resultados'
        for name,field in [('manifiesto_cierre.json','entregables_sha256'),('congelacion_previa.json','artefactos_sha256'),('congelacion_operativa.json','artefactos_sha256'),('conservacion_final.json','protegidos_sha256')]:
            path=base/name
            if not path.exists():continue
            for p,h in read(path)[field].items():
                if sha(ROOT/p)!=h:
                    assert p=='experimentos_objetivo3_v3/CONTINUIDAD_V3.md',p
                    assert hashlib.sha256(subprocess.check_output(['git','show',f'{commit}:{p}'],cwd=ROOT)).hexdigest()==h
                    historical.append(dict(archivo=p,commit=commit,sha256=h))
                count+=1
    guardar(OUT/'integridad_antecedentes.json',dict(aprobado=True,cotejos=count,continuidad_historica=historical,modelos_cargados=False,pdf_leidos=[]))

def referencias(panel):
    lookup=panel.set_index(LLAVES)[anterior.RESULTADO]
    target=panel[panel.anio>=2021].sort_values(LLAVES)[LLAVES+[anterior.RESULTADO]]
    allrefs={};hashes={};selection_hashes={}
    sources=[('v3',ROOT/'experimentos_objetivo3_v3/etapa2/resultados',{'v3':'procedimiento_v3'}),
             ('v2',ROOT/'experimentos_objetivo3_v2/fase3/resultados',dict(v2='procedimiento_v2',v1='referencia_v1',media='media',ols_ipm='ols_ipm_00',ols_tasas='ols_tasas_00',ols_ambas='ols_ambas_00'))]
    for version,base,roles in sources:
        path=base/'predicciones_externas.csv';hashes[str(path.relative_to(ROOT))]=sha(path)
        frame=compartido.normalizar_codigos(pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip'))
        for year in range(2021,2026):
            sp=base/'piloto'/f'seleccion_{year}.json';h=sha(sp);sel=read(sp)
            selection_hashes[str(sp.relative_to(ROOT))]=h
            assert sel['externo']==year
            f=frame[frame.anio==year]
            assert f.seleccion_sha256.eq(h).all()
            main='procedimiento_'+version
            assert f[f.procedimiento==main].id.eq(sel['global_id']).all()
            for group,ident in sel['especificaciones'].items():
                assert f[f.procedimiento=='procedimiento_'+group].id.eq(ident).all()
        for name,role in roles.items():
            r=frame[frame.procedimiento==role].sort_values(LLAVES).reset_index(drop=True)
            assert len(r)==165 and not r.duplicated(LLAVES).any()
            pd.testing.assert_frame_equal(r[LLAVES],target[LLAVES].reset_index(drop=True))
            np.testing.assert_array_equal(r.observado,target[anterior.RESULTADO])
            assert np.isfinite(r.prediccion).all()
            if name not in ('v2','v3'):assert r.id.eq(role).all()
            allrefs[name]=r
    v=allrefs['v3'];hist=v3.historial(panel);pv=hist[hist.anio>=2021].sort_values(LLAVES)
    np.testing.assert_array_equal(v.prediccion,pv.puntaje_previo)
    np.testing.assert_array_equal(v.puntaje_previo,pv.puntaje_previo)
    np.testing.assert_array_equal(v.anio_previo,pv.anio_previo.astype(int))
    assert v.id.eq('persistencia').all()
    guardar(OUT/'referencias_guardadas.json',dict(aprobado=True,archivos_sha256=hashes,selecciones_sha256=selection_hashes,
        roles={n:dict(filas=165,llaves_observados_identicos=True) for n in allrefs},persistencia_independiente=True,ajustes_nuevos=0,modelos_cargados=False))
    return allrefs

def independientes(y,pred):
    y=list(map(float,y));pred=list(map(float,pred));n=len(y);errors=[p-o for p,o in zip(pred,y)]
    mean=math.fsum(y)/n;den=math.fsum((v-mean)**2 for v in y)
    return dict(n=n,mae=math.fsum(abs(e) for e in errors)/n,rmse=math.sqrt(math.fsum(e*e for e in errors)/n),
                sesgo=math.fsum(errors)/n,r2=None if den==0 else 1-math.fsum(e*e for e in errors)/den)

def diagnostico(refs):
    rows=[];diffs=[];aggregate=[]
    scopes=[('conjunto','2021–2025',lambda r:r),('corte','2021–2024',lambda r:r[r.anio<=2024]),('corte','2025',lambda r:r[r.anio==2025])]
    scopes += [('anio',str(y),lambda r,y=y:r[r.anio==y]) for y in range(2021,2026)]
    scopes += [('territorio',c,lambda r,c=c:r[r.codigo_departamento==c]) for c in refs['v3'].codigo_departamento.unique()]
    scopes += [('territorio_corte',c+'_'+period,lambda r,c=c,lo=lo,hi=hi:r[(r.codigo_departamento==c)&r.anio.between(lo,hi)])
               for c in refs['v3'].codigo_departamento.unique() for period,lo,hi in [('2021–2024',2021,2024),('2025',2025,2025)]]
    for name,r in refs.items():
        for scope,period,filter_fn in scopes:
            q=filter_fn(r);m=independientes(q.observado,q.prediccion)
            current=metricas(q.observado,q.prediccion)
            for k in ('mae','rmse','sesgo'):assert math.isclose(m[k],current[k],rel_tol=0,abs_tol=1e-12)
            rows.append(dict(referencia=name,ambito=scope,periodo=period,**m))
    metrics=pd.DataFrame(rows)
    for name,r in refs.items():
        if name=='v3':continue
        v=refs['v3'];e=v.prediccion.to_numpy()-v.observado.to_numpy();other=r.prediccion.to_numpy()-r.observado.to_numpy()
        d=v[LLAVES].copy();d['referencia']=name;d['observado']=v.observado
        d['prediccion_v3']=v.prediccion;d['prediccion_referencia']=r.prediccion
        d['error_v3']=e;d['error_referencia']=other
        d['delta_firmado_puntos']=e-other;d['delta_absoluto_puntos']=abs(e)-abs(other);d['delta_cuadratico_puntos2']=e**2-other**2
        diffs.append(d)
        for scope,period,_ in scopes:
            a=metrics[(metrics.referencia=='v3')&(metrics.ambito==scope)&(metrics.periodo==period)].iloc[0]
            b=metrics[(metrics.referencia==name)&(metrics.ambito==scope)&(metrics.periodo==period)].iloc[0]
            aggregate.append(dict(referencia=name,ambito=scope,periodo=period,n=int(a.n),delta_mae_puntos=a.mae-b.mae,delta_rmse_puntos=a.rmse-b.rmse,delta_sesgo_puntos=a.sesgo-b.sesgo))
    d=pd.concat(diffs,ignore_index=True);a=pd.DataFrame(aggregate)
    for name,frame in [('metricas_historicas.csv',metrics),('diferencias_emparejadas.csv',d),('comparaciones_agregadas.csv',a),
                       ('deterioros_pares.csv',d[d.delta_absoluto_puntos>0]),('deterioros_agregados.csv',a[(a.delta_mae_puntos>0)|(a.delta_rmse_puntos>0)])]:
        frame.to_csv(destino(OUT/name),index=False,float_format='%.17g')
    m=independientes(refs['v3'].observado,refs['v3'].prediccion)
    assert m['mae']>0 and math.isfinite(m['mae'])
    assert abs(m['mae']-read(ROOT/'experimentos_objetivo3_v3/etapa2/resultados/meta.json')['mae_v3'])<=1e-12
    guardar(OUT/'diagnostico_historico.json',dict(origen='recálculo actual de CSV históricos; no resultados v4',v3=m,
        deterioros_pares_vs_v2=int(((d.referencia=='v2')&(d.delta_absoluto_puntos>0)).sum()),
        criterios_modificados=False,meta_v4_evaluada=False,ajustes_panel=0))

def preparar():
    if not (OUT/'partida.json').exists():
        files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')
        guardar(OUT/'partida.json',dict(commit_partida=git('rev-parse','HEAD'),rama=git('branch','--show-current'),
            snapshot_versionados={p:sha(ROOT/p) for p in files},git_inicial_limpio=True,
            commit_documental='46193a5a97962abaef39c2c30e599a347731e45f',diferencias_desde_partida_documental=git('diff','--name-only','15dcf122897d16bfde0e50da316d8f6c6dffdfd4','HEAD').splitlines()))
    versions={}
    lock=ROOT/'experimentos_objetivo3_v3/etapa1/requirements.lock.txt'
    for line in lock.read_text().splitlines():
        n,v=line.split('==');versions[n]=md.version(n);assert versions[n]==v
    assert platform.python_version()=='3.12.14'
    pip=subprocess.check_output([sys.executable,'-m','pip','check']).decode().strip()
    destino(E1/'requirements.lock.txt').write_bytes(lock.read_bytes())
    guardar(OUT/'entorno.json',dict(python=platform.python_version(),ejecutable=sys.executable,paquetes=versions,pip_check=pip,semilla=SEMILLA,instalaciones=False,lock_sha256=sha(lock)))
    reg=read(V4/'REGISTRO_PREPARACION.json');check_hashes(reg['snapshot_versionados_sha256'])
    docs=reg['documentos_sha256']
    # Continuidad se coteja en el commit documental tras actualizarla en cierre.
    for p,h in docs.items():assert hashlib.sha256(subprocess.check_output(['git','show',f'46193a5:{p}'],cwd=ROOT)).hexdigest()==h
    rp=str((V4/'REGISTRO_PREPARACION.json').relative_to(ROOT));assert (ROOT/rp).read_bytes()==subprocess.check_output(['git','show',f'46193a5:{rp}'])
    antecedentes()
    assert sha(anterior.BASE)==anterior.BASE_SHA
    panel=compartido.normalizar_codigos(pd.read_csv(anterior.BASE,dtype={'codigo_departamento':str},float_precision='round_trip'))
    compartido.validar_panel(panel);p=historial(panel)
    pd.testing.assert_frame_equal(p[panel.columns].reset_index(drop=True),panel.sort_values(LLAVES).reset_index(drop=True))
    old=pd.read_csv(ROOT/'experimentos_objetivo3_v3/etapa1/reconstrucciones/panel_historial.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    for c in ['puntaje_previo','cambio_observado']:
        np.testing.assert_array_equal(p[c].to_numpy(),old.sort_values(LLAVES)[c].to_numpy())
    available=p[p.anio>2018];assert len(available)==198
    assert np.isfinite(available[['cambio_'+s for s in COV]].to_numpy()).all()
    lookup=panel.set_index(LLAVES)
    trace=[]
    for row in available.to_dict('records'):
        prev=lookup.loc[(row['codigo_departamento'],int(row['anio_previo']))]
        for s in COV:
            assert row['previo_'+s]==prev[s]
            assert row['cambio_'+s]==row[s]-prev[s]
        trace.append({k:row[k] for k in [*LLAVES,'anio_previo','intervalo','puntaje_previo',*['previo_'+s for s in COV],*['cambio_'+s for s in COV]]})
    assert p[p.anio==2021].anio_previo.eq(2019).all()
    p['fuente_sha256']=anterior.BASE_SHA
    p.to_csv(destino(E1/'reconstrucciones/panel_cambios.csv'),index=False,float_format='%.17g')
    roundtrip=pd.read_csv(E1/'reconstrucciones/panel_cambios.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    for col in [anterior.RESULTADO,'puntaje_previo','cambio_observado',*['cambio_'+s for s in COV]]:
        np.testing.assert_array_equal(roundtrip[col].to_numpy(),p[col].to_numpy())
    pd.DataFrame(trace).to_csv(destino(OUT/'trazabilidad_198.csv'),index=False,float_format='%.17g')
    for w in ventanas():
        dividir(p,w['entrenamiento'],w['externo'])
        for i in w['internas']:dividir(p,i['entrenamiento'],i['validacion'])
    conf=dict(version='4.0.0',semilla=SEMILLA,configuraciones=candidatos(),grupos=GRUPOS,ventanas=ventanas(),orden_familias=ORDEN,
        tolerancias=dict(mae=.1,rmse=.1,atol=1e-10,rtol=0),limite_futuro=7200,cota_sin_fallos=dict(internos=280,externos=24,repeticiones=4,total=308),
        panel_fuente_sha256=anterior.BASE_SHA,panel_derivado_sha256=sha(E1/'reconstrucciones/panel_cambios.csv'))
    if (OUT/'configuraciones_congeladas.json').exists():assert read(OUT/'configuraciones_congeladas.json')==conf
    else:guardar(OUT/'configuraciones_congeladas.json',conf)
    guardar(OUT/'estructura_real.json',dict(aprobado=True,filas=231,cambios_completos=198,externas=165,territorios=33,matrices=[len(v) for v in GRUPOS.values()],trazabilidad_covariables=True,ajustes_panel=0,correcciones_reales_estimadas=0))
    refs=referencias(panel);diagnostico(refs)
    print('Preflight aprobado: 198 cambios completos, 29 candidatos; diagnóstico histórico guardado, cero fits reales.')
if __name__=='__main__':preparar()
