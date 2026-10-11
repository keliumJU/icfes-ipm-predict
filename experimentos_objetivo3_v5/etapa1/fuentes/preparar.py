"""Reconstrucción y evidencia documental; nunca ajustar ni generar predicciones v5."""
from comun_v5 import *
import subprocess, platform, importlib.metadata as md, hashlib
DOC='fa2b5ab1852f427549a9fd5e9a119a3ab4fdeb77'
SOURCE=ROOT/'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
DERIVADO=ROOT/'experimentos_objetivo3_v4/etapa1/reconstrucciones/panel_cambios.csv'
SOURCE_SHA='6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3'
DERIVADO_SHA='aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def csv(path):return pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip')

def entorno():
    lock=ROOT/'experimentos_objetivo3_v4/etapa1/requirements.lock.txt'
    expected={n.lower().replace('_','-'):v for n,v in (line.split('==') for line in lock.read_text().splitlines())}
    actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions() if d.metadata['Name'].lower()!='pip'}
    assert platform.python_version()=='3.12.14' and len(expected)==54 and actual==expected
    pip=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True,check=True)
    return dict(python=platform.python_version(),ejecutable=sys.executable,paquetes=actual,sklearn=md.version('scikit-learn'),pip_check=pip.stdout.strip(),advertencias=pip.stderr.strip(),semilla=SEMILLA,instalaciones=False,lock_sha256=sha(lock))

def antecedentes():
    r=read(V5/'REGISTRO_PREPARACION.json')
    check_hashes(r['inventario_previo']['sha256_versionados'])
    for p,h in r['sha256_documentos'].items():
        assert hashlib.sha256(subprocess.check_output(['git','show',f'{DOC}:{p}'],cwd=ROOT)).hexdigest()==h
        assert sha(ROOT/p)==h
    rp='experimentos_objetivo3_v5/REGISTRO_PREPARACION.json'
    assert (ROOT/rp).read_bytes()==subprocess.check_output(['git','show',f'{DOC}:{rp}'],cwd=ROOT)
    files=git('diff-tree','--no-commit-id','--name-only','-r',DOC).splitlines()
    assert set(files)==set(r['archivos_creados']) and len(files)==4
    assert git('rev-parse',DOC+'^')=='0f159164e31e671e47a432afb9f2974724dec5c2'
    assert git('log','-1','--format=%s',DOC)=='documentar plan v5 y prompt de diseno MAE sin piloto'
    command=[sys.executable,str(ROOT/'experimentos_objetivo3_v4/etapa2/fuentes/cerrar.py'),'--verificar']
    result=subprocess.run(command,capture_output=True,text=True,check=True)
    # Leer íntegramente las estructuras y verificar huellas pertinentes sin escribir v4.
    inspected=[];comparisons=0
    for stage,commit in [('etapa1','7f25ad066386965a75058e96b4716cdd8a9adb52'),('etapa2','0f159164e31e671e47a432afb9f2974724dec5c2')]:
        folder=ROOT/'experimentos_objetivo3_v4'/stage/'resultados'
        names=['configuraciones_congeladas.json','controles.json','congelacion_previa.json','congelacion_operativa.json','congelacion_extension_auditoria.json','conservacion_final.json','manifiesto_cierre.json']
        for name in names:
            path=folder/name
            if not path.exists():continue
            data=read(path);inspected.append(dict(archivo=str(path.relative_to(ROOT)),sha256=sha(path),campos=list(data)))
            for field in ('entregables_sha256','artefactos_sha256','protegidos_sha256'):
                for p,h in data.get(field,{}).items():
                    if sha(ROOT/p)!=h:
                        assert p=='experimentos_objetivo3_v4/CONTINUIDAD_V4.md'
                        assert hashlib.sha256(subprocess.check_output(['git','show',f'{commit}:{p}'],cwd=ROOT)).hexdigest()==h
                    comparisons+=1
    return dict(aprobado=True,commit_documental=DOC,cuatro_archivos=files,snapshot_preparacion_cotejado=len(r['inventario_previo']['sha256_versionados']),cierre_v4_lectura=result.stdout.strip(),manifiestos_leidos=inspected,cotejos=comparisons,registro_sha256=sha(V5/'REGISTRO_PREPARACION.json'),pdf_paginas=0)

def panel():
    assert sha(SOURCE)==SOURCE_SHA and sha(DERIVADO)==DERIVADO_SHA
    source=previo.compartido.normalizar_codigos(csv(SOURCE))
    previo.compartido.validar_panel(source)
    p=historial(source);p['fuente_sha256']=SOURCE_SHA
    old=csv(DERIVADO)
    # Cotejo íntegro en memoria antes de guardar copia propia: mismas llaves/campos/orden/valores.
    igualdad_exacta(p.reset_index(drop=True),old.reset_index(drop=True))
    igualdad_exacta(p[source.columns].reset_index(drop=True),source.sort_values(LLAVES).reset_index(drop=True))
    changes=p[p.anio>2018];assert len(p)==231 and len(changes)==198 and p.codigo_departamento.nunique()==33
    assert np.isfinite(changes[['cambio_observado',*['cambio_'+s for s in COV]]].to_numpy(float)).all()
    lookup=source.set_index(LLAVES);trace=[]
    for row in changes.to_dict('records'):
        code=row['codigo_departamento'];year=row['anio'];past=int(row['anio_previo'])
        assert past==max(source[(source.codigo_departamento==code)&(source.anio<year)].anio)
        prev=lookup.loc[(code,past)]
        assert row['puntaje_previo']==prev['prom_punt_global']
        assert row['cambio_observado']==row['prom_punt_global']-prev['prom_punt_global']
        for s in COV:
            assert row['previo_'+s]==prev[s] and row['cambio_'+s]==row[s]-prev[s]
        trace.append({k:row[k] for k in [*LLAVES,'anio_previo','intervalo','puntaje_previo',*['previo_'+s for s in COV],*['cambio_'+s for s in COV]]})
    assert p[p.anio==2021].anio_previo.eq(2019).all()
    target=destino(E1/'reconstrucciones/panel_cambios.csv')
    if target.exists():igualdad_exacta(p.reset_index(drop=True),csv(target))
    else:p.to_csv(target,index=False,float_format='%.17g')
    igualdad_exacta(p.reset_index(drop=True),csv(target))
    assert sha(target)==DERIVADO_SHA
    pd.DataFrame(trace).to_csv(destino(OUT/'trazabilidad_198.csv'),index=False,float_format='%.17g')
    return p

def referencias(p):
    sources=[('v3',ROOT/'experimentos_objetivo3_v3/etapa2/resultados',{'v3':'procedimiento_v3'}),('v4',ROOT/'experimentos_objetivo3_v4/etapa2/resultados',{'v4':'procedimiento_v4'}),('v2',ROOT/'experimentos_objetivo3_v2/fase3/resultados',dict(v2='procedimiento_v2',v1='referencia_v1',media='media',ols_ipm='ols_ipm_00',ols_tasas='ols_tasas_00',ols_ambas='ols_ambas_00'))]
    expected=p[p.anio>=2021].sort_values(LLAVES).reset_index(drop=True)
    hashes={};selection_hashes={};roles={};v3=None
    for version,base,mapping in sources:
        path=base/'predicciones_externas.csv';hashes[str(path.relative_to(ROOT))]=sha(path)
        f=previo.compartido.normalizar_codigos(csv(path))
        for year in range(2021,2026):
            sp=base/'piloto'/f'seleccion_{year}.json';h=sha(sp);sel=read(sp);selection_hashes[str(sp.relative_to(ROOT))]=h
            assert sel['externo']==year
            q=f[f.anio==year];assert q.seleccion_sha256.eq(h).all()
            assert q[q.procedimiento=='procedimiento_'+version].id.eq(sel['global_id']).all()
            for g,ident in sel['especificaciones'].items():assert q[q.procedimiento=='procedimiento_'+g].id.eq(ident).all()
        for name,role in mapping.items():
            q=f[f.procedimiento==role].sort_values(LLAVES).reset_index(drop=True)
            assert len(q)==165 and not q.duplicated(LLAVES).any()
            igualdad_exacta(q[LLAVES],expected[LLAVES])
            np.testing.assert_array_equal(q.observado,expected.prom_punt_global)
            assert np.isfinite(q.prediccion).all()
            if name not in ('v2','v3','v4'):assert q.id.eq(role).all()
            roles[name]=dict(filas=165,llaves_observados_identicos=True)
            if name=='v3':v3=q
    np.testing.assert_array_equal(v3.prediccion,expected.puntaje_previo)
    np.testing.assert_array_equal(v3.puntaje_previo,expected.puntaje_previo)
    np.testing.assert_array_equal(v3.anio_previo,expected.anio_previo.astype(int))
    assert v3.id.eq('persistencia').all()
    mae=math.fsum(abs(float(a)-float(b)) for a,b in zip(v3.prediccion,v3.observado))/165
    assert mae>0 and math.isfinite(mae) and mae==3.429267191379531
    return dict(aprobado=True,origen='CSV históricos guardados; recálculo actual del denominador, cero nuevos fits',archivos_sha256=hashes,selecciones_sha256=selection_hashes,roles=roles,mae_persistencia_v3=mae,persistencia_independiente=True,modelos_cargados=False,meta_v5_evaluada=False)

def preparar():
    assert git('branch','--show-current')=='codex/objetivo3-v5-mae'
    if (OUT/'partida.json').exists():raise ValueError('no sobrescribir preflight')
    files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT).decode()
    assert all(line[3:].startswith('experimentos_objetivo3_v5/') for line in status.splitlines())
    guardar(OUT/'partida.json',dict(commit_partida=git('rev-parse','HEAD'),rama=git('branch','--show-current'),commit_documental=DOC,git_inicial_limpio=True,diferencias_posteriores=git('diff','--name-only',DOC,'HEAD').splitlines(),snapshot_versionados={p:sha(ROOT/p) for p in files},autorizacion='exclusivamente etapa1; cero fits panel',creacion_rama='git switch -c; escalado por .git solo lectura'))
    guardar(OUT/'entorno.json',entorno());destino(E1/'requirements.lock.txt').write_bytes((ROOT/'experimentos_objetivo3_v4/etapa1/requirements.lock.txt').read_bytes())
    guardar(OUT/'integridad_antecedentes.json',antecedentes())
    p=panel()
    guardar(OUT/'estructura_real.json',dict(aprobado=True,filas=231,territorios=33,cambios_completos=198,cotejo_integral_exacto=True,trazabilidad_misma_llave=True,fuente_sha256=SOURCE_SHA,derivado_sha256=DERIVADO_SHA,ajustes_panel=0,estadisticas_aprendidas=0,predicciones_nuevas=0))
    guardar(OUT/'referencias_guardadas.json',referencias(p))
    guardar(OUT/'configuraciones_congeladas.json',dict(version='5.0.0',configuraciones=candidatos(),grupos=GRUPOS,ventanas=ventanas(),orden_familias=ORDEN,semilla=SEMILLA,tolerancias=dict(mae=.1,rmse=.1,atol=1e-10,rtol=0),limite_futuro=7200,cota_sin_fallos=dict(internos=350,externos=24,repeticiones=4,total=378),panel_fuente_sha256=SOURCE_SHA,panel_derivado_sha256=DERIVADO_SHA))
    print('Panel cotejado íntegramente:231 filas/198 cambios; grilla36; cero fits reales.')
if __name__=='__main__':preparar()
