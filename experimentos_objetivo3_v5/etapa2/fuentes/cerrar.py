"""Conservación y cierre exclusivo etapa2; nunca entrena ni reescribe etapa1."""
from piloto import *
import nbformat,hashlib
CLOSE='109797407d75d2097e5b71f8bcef3fc266bc61d2'
def conservacion():
    snapshot=read(OUT/'partida.json')['snapshot_versionados'];historical='experimentos_objetivo3_v5/CONTINUIDAD_V5.md'
    for p,h in snapshot.items():
        if p==historical:
            old=subprocess.check_output(['git','show',CLOSE+':'+p],cwd=ROOT)
            assert hashlib.sha256(old).hexdigest()==h
            assert (ROOT/p).read_bytes().endswith(old)
        else:assert sha(ROOT/p)==h,p
    return snapshot

def verificar():
    verify_freeze();conservacion()
    check_hashes(read(OUT/'manifiesto_cierre.json')['entregables_sha256'])
    nb=read(OUT/'verificacion_notebook.json');assert nb['aprobado'] and nb['celdas_ejecutadas']==3 and nb['salidas_realmente_ejecutadas']
    assert sha(E2/'fuentes/01_resultados_piloto.py')==nb['fuente_sha256'] and sha(E2/'notebooks/01_resultados_piloto.ipynb')==nb['notebook_sha256']
    nbformat.validate(nbformat.read(E2/'notebooks/01_resultados_piloto.ipynb',as_version=4))
    assert read(OUT/'verificacion.json')['aprobado'] and read(OUT/'meta.json')['completo']
    print('Cierre etapa2 v5 verificado en lectura, conservación íntegra.')

def cerrar():
    assert not (OUT/'manifiesto_cierre.json').exists(),'no sobrescribir cierre'
    verify_freeze();snapshot=conservacion()
    assert read(OUT/'verificacion.json')['aprobado']
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT).decode()
    assert all(line[3:].startswith('experimentos_objetivo3_v5/') for line in status.splitlines())
    guardar(OUT/'conservacion_final.json',dict(aprobado=True,protegidos_sha256=snapshot,continuidad_historica_commit=CLOSE,unica_actualizacion='CONTINUIDAD_V5.md con antecedente íntegro',pdf_paginas=0,push=False))
    paths=[p for p in E2.rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']+[V5/'CONTINUIDAD_V5.md',E2/'PROMPT_ETAPA3_NUEVA_SESION.md']
    assert not any('__pycache__' in p.parts for p in paths)
    guardar(OUT/'manifiesto_cierre.json',dict(etapa='v5/etapa2',version='5.0.0',commit_partida=CLOSE,completa=True,entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))},meta=read(OUT/'meta.json'),pendientes_indispensables=[],pendientes=['otra autorización etapa3 y meta global satisfecha; no avance automático'],push=False))
    verificar()
if __name__=='__main__':
    if sys.argv[1:]==['--verificar']:verificar()
    elif not sys.argv[1:]:cerrar()
    else:raise ValueError('argumento desconocido')
