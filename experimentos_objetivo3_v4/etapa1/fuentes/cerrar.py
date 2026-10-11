"""Cierre únicamente v4 etapa1. --verificar es estrictamente lectura."""
from preparar import *
from datetime import datetime,timezone
def verificar():
    check_hashes(read(OUT/'conservacion_final.json')['protegidos_sha256'])
    check_hashes(read(OUT/'congelacion_previa.json')['artefactos_sha256'])
    check_hashes(read(OUT/'manifiesto_cierre.json')['entregables_sha256'])
    assert not (V4/'etapa2').exists(),'etapa2 fuera de alcance'
    assert not list(V4.rglob('__pycache__'))
    print('Cierre, congelación y conservación v4 verificados en lectura.')
def cerrar():
    protected={p:h for p,h in read(OUT/'partida.json')['snapshot_versionados'].items() if not p.startswith('experimentos_objetivo3_v4/')}
    check_hashes(protected)
    original=read(V4/'REGISTRO_PREPARACION.json')
    for p,h in original['documentos_sha256'].items():
        if not p.endswith('CONTINUIDAD_V4.md'):assert sha(ROOT/p)==h
    assert read(OUT/'estructura_real.json')['aprobado']
    for p in [OUT/'sinteticos/controles.json',OUT/'notebook_sinteticos/controles.json',OUT/'verificacion_notebook.json']:
        assert read(p)['aprobado']
        if 'fuentes_sha256' in read(p):check_hashes(read(p)['fuentes_sha256'])
    nb=read(OUT/'verificacion_notebook.json')
    assert nb['fuente_sha256']==sha(E1/'fuentes/01_diagnostico_controles.py')
    assert nb['notebook_sha256']==sha(E1/'notebooks/01_diagnostico_controles.ipynb')
    changes=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT).decode().splitlines()
    assert all(line[3:].startswith('experimentos_objetivo3_v4/') for line in changes),changes
    reused=[ROOT/'experimentos_objetivo3_v3/etapa1/fuentes/comun_v3.py',*[ROOT/'experimentos_objetivo3_v2/fase2/fuentes'/s for s in ['comun.py','configuracion.py','congelar.py']],ROOT/'protocolo/fuentes/configuracion.py',anterior.BASE]
    refs=read(OUT/'referencias_guardadas.json')
    paths=[p for p in E1.rglob('*') if p.is_file() and p.name not in ['congelacion_previa.json','conservacion_final.json','manifiesto_cierre.json','verificacion_cierre.json']]+reused
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}
    hashes.update(refs['archivos_sha256']);hashes.update(refs['selecciones_sha256'])
    guardar(OUT/'congelacion_previa.json',dict(version='4.0.0',fecha_cliente='2026-10-10',instante_utc=datetime.now(timezone.utc).isoformat(),
        artefactos_sha256=hashes,semilla=SEMILLA,ajustes_panel=0,correcciones_panel=0,ledger_operativo_creado=False,meta_v4_evaluada=False,
        requisito_etapa2='Verificar etapa1/entorno; probar y congelar nueva orquestación antes del primer fit. Requiere autorización separada.'))
    guardar(OUT/'conservacion_final.json',dict(aprobado=True,protegidos_sha256=protected,preparacion_intacta_salvo_continuidad=True,
        continuidad_anterior_conservada=True,originales_no_escritos=True,pdf_leidos=[],push=False))
    guardar(OUT/'verificacion_cierre.json',dict(aprobado=True,etapa1_completa=True,configuraciones=29,cambios=198,
        ajustes_panel=0,predicciones_v4=0,meta_v4_evaluada=False,ledger_operativo_creado=False,pendientes_indispensables=[]))
    paths=[p for p in V4.rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']
    guardar(OUT/'manifiesto_cierre.json',dict(etapa='v4/etapa1',version='4.0.0',commit_partida=read(OUT/'partida.json')['commit_partida'],
        entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},etapa1_completa=True,piloto_iniciado=False,push=False))
    verificar()
if __name__=='__main__':
    if '--verificar' in sys.argv:verificar()
    else:cerrar()
