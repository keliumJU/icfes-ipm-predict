"""Cierre y verificación propia: nunca invoca cierres ni congelaciones v2."""
from comun_v3 import *
from preparar import git
from datetime import datetime, timezone

def verificar():
    manifest=read(E1/'resultados/manifiesto_cierre.json')
    for path,h in manifest['entregables_sha256'].items():assert sha(ROOT/path)==h,path
    conservation=read(E1/'resultados/conservacion_final.json')
    for path,h in conservation['protegidos_sha256'].items():assert sha(ROOT/path)==h,path
    freeze=read(E1/'resultados/congelacion_previa.json')
    for path,h in freeze['artefactos_sha256'].items():assert sha(ROOT/path)==h,path
    print('Cierre v3 y conservación verificados en lectura; piloto no iniciado.')

def cerrar():
    snapshot=read(E1/'resultados/partida.json')['snapshot_versionados']
    protected={p:h for p,h in snapshot.items() if not p.startswith('experimentos_objetivo3_v3/')}
    for path,h in protected.items():assert sha(ROOT/path)==h,path
    original_docs={p:h for p,h in snapshot.items() if p.startswith('experimentos_objetivo3_v3/') and not p.endswith('CONTINUIDAD_V3.md')}
    for path,h in original_docs.items():assert sha(ROOT/path)==h,path
    assert all(p.startswith('experimentos_objetivo3_v3/') for p in git('diff','--name-only').splitlines())
    assert read(E1/'resultados/estructura_real.json')['aprobado']
    assert read(E1/'resultados/sinteticos/controles.json')['aprobado']
    assert read(E1/'resultados/notebook_sinteticos/controles.json')['aprobado']
    nb=read(E1/'resultados/verificacion_notebook.json')
    assert sha(E1/'notebooks/01_controles.ipynb')==nb['notebook_sha256']
    assert sha(E1/'fuentes/01_controles.py')==nb['fuente_sha256']
    sources=read(E1/'resultados/integridad_antecedentes.json')['fuentes_sha256']
    for path,h in sources.items():assert sha(ROOT/path)==h,path
    artifacts=[*sorted((E1/'fuentes').glob('*.py')),E1/'PROTOCOLO_V3.md',E1/'requirements.lock.txt',
               E1/'resultados/configuraciones_congeladas.json',E1/'resultados/entorno.json',
               E1/'reconstrucciones/panel_historial.csv',E1/'resultados/referencias_guardadas.json']
    # Dependencias compartidas también quedan fijadas por huella, siempre en lectura.
    artifacts += [ROOT/'experimentos_objetivo3_v2/fase2/fuentes'/name for name in ('configuracion.py','comun.py','congelar.py')]
    artifacts += [ROOT/'protocolo/fuentes/configuracion.py']
    guardar(E1/'resultados/congelacion_previa.json',dict(version='3.0.0',fecha_cliente='2026-10-10',
        momento_utc=datetime.now(timezone.utc).isoformat(),artefactos_sha256={str(p.relative_to(ROOT)):sha(p) for p in artifacts},
        congelacion_v2_sha256=sha(anterior.F2/'resultados/configuraciones_congeladas.json'),
        panel_fuente_sha256=anterior.BASE_SHA,semilla=SEMILLA,ajustes_reales=0,predicciones_reales=0,
        piloto_iniciado=False,ledger_operativo_creado=False,
        requisito_futuro='Verificar estas huellas y congelar orquestación etapa2 antes del primer ajuste real.'))
    guardar(E1/'resultados/conservacion_final.json',dict(aprobado=True,protegidos_sha256=protected,
        documentos_preparacion_intactos=original_docs,fuentes_originales_sha256=sources,
        modificaciones='exclusivamente v3; continuidad propia actualizada',pdf_leidos=[],push=False))
    paths=[p for p in V3.rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']
    assert not any('__pycache__' in p.parts for p in paths)
    guardar(E1/'resultados/manifiesto_cierre.json',dict(etapa='v3/etapa1',fecha_cliente='2026-10-10',
        commit_partida=read(E1/'resultados/partida.json')['commit_partida'],
        entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},
        etapa1_completa=True,ajustes_reales=0,predicciones_reales=0,piloto_iniciado=False,
        pendientes_indispensables=[],push=False))
    verificar()
if __name__=='__main__':
    if '--verificar' in sys.argv:verificar()
    else:cerrar()
