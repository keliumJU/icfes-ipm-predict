"""Conservación y manifiesto exclusivo etapa2; no invoca cierres v2/etapa1."""
from piloto import *

def cerrar():
    partida=read(OUT/'partida.json');protected={p:h for p,h in partida['snapshot_versionados'].items() if p!='experimentos_objetivo3_v3/CONTINUIDAD_V3.md'}
    check_hashes(protected)
    assert read(OUT/'verificacion.json')['aprobado'] and read(OUT/'verificacion.json')['completo']
    changes=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).decode().splitlines()
    assert all(p.startswith('experimentos_objetivo3_v3/') for p in changes)
    guardar(OUT/'conservacion_final.json',dict(aprobado=True,protegidos_sha256=protected,unica_modificacion_previa='CONTINUIDAD_V3.md, antecedente íntegro conservado',pdf_leidos=[],push=False))
    paths=[p for p in E2.rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']+[V3/'CONTINUIDAD_V3.md',V3/'PROMPT_ETAPA3_NUEVA_SESION.md']
    assert not any('__pycache__' in p.parts for p in paths)
    guardar(OUT/'manifiesto_cierre.json',dict(etapa='v3/etapa2',completo=True,commit_partida=partida['commit_partida'],entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},pendientes_indispensables=[],push=False))
    verificar()
def verificar():
    check_hashes(read(OUT/'conservacion_final.json')['protegidos_sha256'])
    check_hashes(read(OUT/'manifiesto_cierre.json')['entregables_sha256'])
    verify_freeze();print('Cierre etapa2 y conservación verificados en lectura.')
if __name__=='__main__':
    if '--verificar' in sys.argv:verificar()
    else:cerrar()
