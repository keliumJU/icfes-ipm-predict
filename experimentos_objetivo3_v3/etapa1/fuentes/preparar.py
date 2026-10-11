"""Estructura real, conservación, grilla y entorno. Nunca calcula predicciones ni errores."""
from comun_v3 import *
import subprocess, platform, importlib.metadata as md, hashlib
from datetime import datetime, timezone

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def preparar():
    out=E1/'resultados'
    snapshot_path=out/'partida.json'
    if not snapshot_path.exists():
        files=git('ls-files').splitlines()
        guardar(snapshot_path,dict(commit_partida=git('rev-parse','HEAD'),rama=git('branch','--show-current'),
              estado_git=git('status','--porcelain'),cierre_v2='cc21529532668a966d500e435dca65ef11db09a3',
              diferencia_documental=git('diff','--name-only','cc21529532668a966d500e435dca65ef11db09a3','HEAD').splitlines(),
              snapshot_versionados={p:sha(ROOT/p) for p in files if (ROOT/p).is_file()},pdf_leidos=[]))
    versions={}
    for line in (anterior.F2/'requirements.lock.txt').read_text().splitlines():
        name,version=line.split('==');versions[name]=md.version(name);assert versions[name]==version
    assert platform.python_version()=='3.12.14' and versions['scikit-learn']=='1.9.1'
    lock=destino(E1/'requirements.lock.txt');lock.write_bytes((anterior.F2/'requirements.lock.txt').read_bytes())
    guardar(out/'entorno.json',dict(python=platform.python_version(),ejecutable=sys.executable,paquetes=versions,
        pip_check=subprocess.check_output([sys.executable,'-m','pip','check']).decode().strip(),semilla=SEMILLA,
        origen='Entorno existente comprobado; ninguna instalación/red.',lock_sha256=sha(lock)))
    count=0;historical=[]
    commits={2:'0664ac21100982006d1a20670c7e987879444dc6',3:'b37a2f338f0708958a412f5a0efa09f33861322b',4:'cc21529532668a966d500e435dca65ef11db09a3'}
    for phase,commit in commits.items():
        manifest=read(ROOT/f'experimentos_objetivo3_v2/fase{phase}/resultados/manifiesto_cierre.json')
        for path,h in manifest['entregables_sha256'].items():
            if path=='experimentos_objetivo3_v2/CONTINUIDAD_V2.md':
                assert hashlib.sha256(subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=ROOT)).hexdigest()==h
                historical.append(dict(archivo=path,commit=commit,sha256=h))
            else: assert sha(ROOT/path)==h,path
            count+=1
    frozen=read(anterior.F2/'resultados/congelacion_previa.json')
    for path,h in frozen['fuentes_sha256'].items():assert sha(ROOT/path)==h
    assert sha(anterior.F2/'resultados/configuraciones_congeladas.json')==frozen['configuraciones_sha256']
    assert sha(anterior.F2/'PROTOCOLO_V2.md')==frozen['protocolo_sha256']
    operative=read(ROOT/'experimentos_objetivo3_v2/fase3/resultados/congelacion_operativa.json')
    for path,h in operative['codigo'].items():assert sha(ROOT/path)==h
    sources=read(ROOT/'experimentos_objetivo3_v2/fase3/resultados/conservacion_fuentes.json')['fuentes_sha256']
    for path,h in sources.items():assert sha(ROOT/path)==h
    # Solo se consulta el estado histórico; no se consume ni se modifica su saldo.
    ledger=read(ROOT/'experimentos_objetivo3_v2/fase3/resultados/piloto/ledger.json')
    repeat=read(ROOT/'experimentos_objetivo3_v2/fase3/resultados/piloto/reproducibilidad.json')
    verification=read(ROOT/'experimentos_objetivo3_v2/fase4/resultados/verificacion.json')
    conservation=read(ROOT/'experimentos_objetivo3_v2/fase3/resultados/conservacion_final.json')
    assert ledger['limite']==7200 and not ledger['pendiente'] and len(repeat['repeticiones'])==10
    panel=compartido.cargar_panel();p=historial(panel)
    assert len(p)==231 and p.cambio_observado.notna().sum()==198
    assert p.loc[p.anio==2018,['anio_previo','puntaje_previo','cambio_observado']].isna().all().all()
    assert p.loc[p.anio==2021,'anio_previo'].eq(2019).all()
    assert len(p[p.anio>=2021])==165
    for w in ventanas():
        tr,te=dividir(p,w['entrenamiento'],w['externo'])
        assert len(te)==33
        for i in w['internas']:dividir(p,i['entrenamiento'],i['validacion'])
    # Columnas originales sin cambio de valor; llave normalizada únicamente en derivado.
    pd.testing.assert_frame_equal(p[panel.columns].sort_values(LLAVES).reset_index(drop=True),panel.sort_values(LLAVES).reset_index(drop=True))
    p['fuente_sha256']=anterior.BASE_SHA
    path=destino(E1/'reconstrucciones/panel_historial.csv')
    p.to_csv(path,index=False,float_format='%.17g')
    q=pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip')
    np.testing.assert_array_equal(q[anterior.RESULTADO],p[anterior.RESULTADO])
    # Coteja previo contra fila fuente y conserva identificadores de procedencia.
    lookup=panel.set_index(LLAVES)[anterior.RESULTADO]
    for row in p[p.anio_previo.notna()].itertuples():
        assert row.puntaje_previo==lookup.loc[(row.codigo_departamento,int(row.anio_previo))]
        assert row.cambio_observado==row.prom_punt_global-row.puntaje_previo
    refs=pd.read_csv(ROOT/'experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    roles=['procedimiento_v2','referencia_v1','media',*[f'ols_{s}_00' for s in ESPECIFICACIONES]]
    keys=set(map(tuple,p.loc[p.anio>=2021,LLAVES].to_numpy()))
    references={}
    for role in roles:
        r=refs[refs.procedimiento==role]
        assert len(r)==165 and not r.duplicated(LLAVES).any() and set(map(tuple,r[LLAVES].to_numpy()))==keys
        for row in r.itertuples():assert row.observado==lookup.loc[(row.codigo_departamento,row.anio)]
        references[role]=dict(filas=165,llaves_identicas=True,observados_identicos=True)
    selections={str(y):sha(ROOT/f'experimentos_objetivo3_v2/fase3/resultados/piloto/seleccion_{y}.json') for y in range(2021,2026)}
    for y in range(2021,2026):
        assert refs.loc[refs.anio==y,'seleccion_sha256'].eq(selections[str(y)]).all()
        selection=read(ROOT/f'experimentos_objetivo3_v2/fase3/resultados/piloto/seleccion_{y}.json')
        assert selection['externo']==y
        assert refs.loc[(refs.anio==y)&(refs.procedimiento=='procedimiento_v2'),'id'].eq(selection['global_id']).all()
        for spec,ident in selection['especificaciones'].items():
            assert refs.loc[(refs.anio==y)&(refs.procedimiento==f'procedimiento_{spec}'),'id'].eq(ident).all()
    guardar(out/'referencias_guardadas.json',dict(roles=references,selecciones_sha256=selections,
        archivo='experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv',
        sha256=sha(ROOT/'experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv'),
        errores_o_metricas_recalculados=False,modelos_cargados=False))
    cs=candidatos()
    assert {s:len(v) for s,v in ESPECIFICACIONES.items()}==dict(ipm=2,tasas=16,ambas=17)
    count_internal=sum(len(w['internas'])*99 for w in ventanas())
    bound=count_internal+4*4+4
    assert count_internal==990 and bound==1010
    conf=dict(version='3.0.0',semilla=SEMILLA,configuraciones=cs,especificaciones=ESPECIFICACIONES,
        ventanas=ventanas(),panel_fuente_sha256=anterior.BASE_SHA,panel_derivado_sha256=sha(path),
        tolerancias=dict(mae=0.1,rmse=0.1,atol_repeticion=1e-10,rtol_repeticion=0),
        orden_familias=ORDEN,presupuesto_segundos=7200,
        cota_sin_fallos=dict(internos=990,externos=16,repeticiones_ajustadas=4,total=1010,
            comprobaciones_repeticion=5,persistencia_2021_ajustes=0,comparadores_guardados_ajustes=0))
    dest=out/'configuraciones_congeladas.json'
    if dest.exists():assert read(dest)==conf,'Grilla existente distinta'
    else:guardar(dest,conf)
    guardar(out/'estructura_real.json',dict(aprobado=True,registros_fuente=231,cambios=198,externas=165,
        territorios=33,anio_previo_2021=2019,objetivos_2018=0,anio_2020=False,
        igualdad_columnas_fuente=True,trazabilidad_previo=True,ajustes=0,predicciones=0,metricas=0,
        panel_derivado_sha256=sha(path)))
    guardar(out/'integridad_antecedentes.json',dict(aprobado=True,cotejos_manifiestos=count,
        continuidades_en_commits=historical,fuentes_sha256=sources,ledger_v2_sha256=sha(ROOT/'experimentos_objetivo3_v2/fase3/resultados/piloto/ledger.json'),
        consumo_v2_historico=ledger['consumido'],repeticiones_v2_historicas=10,conservacion_v2_consultada=True,
        verificacion_fase4_consultada=True,pdf_leidos=[]))
    print('Estructura real: 231 registros, 198 cambios, 165 externas; 100 configuraciones; cota 1010. Sin predicciones.')
if __name__=='__main__':preparar()
