"""Cerrar exclusivamente etapa1; --verificar lee, no reconstruye ni ejecuta pruebas/fits."""
from comun_v5 import *
from preparar import DOC, entorno
import subprocess,hashlib,nbformat
from datetime import datetime,timezone

def evidencia():
    assert not (V5/'etapa2').exists(),'etapa2 no autorizada'
    assert not (OUT/'piloto').exists() and not (OUT/'ledger.json').exists() and not (OUT/'meta.json').exists()
    assert not any(p.suffix in ('.joblib','.pkl') for p in E1.rglob('*'))
    for name in ('controles.json','verificacion_notebook.json'):
        data=read(OUT/name);assert data['aprobado'] and data['ajustes_panel']==0
        check_hashes(data['fuentes_sha256'])
    nb=read(OUT/'verificacion_notebook.json')
    assert nb['fuente_sha256']==sha(E1/'fuentes/01_controles.py')
    assert nb['notebook_sha256']==sha(E1/'notebooks/01_controles.ipynb')
    assert nb['celdas_ejecutadas']==[1,2,3] and nb['salidas_realmente_ejecutadas']
    notebook=nbformat.read(E1/'notebooks/01_controles.ipynb',as_version=4);nbformat.validate(notebook)
    code=[c for c in notebook.cells if c.cell_type=='code']
    assert [c.execution_count for c in code]==[1,2,3] and all(c.outputs for c in code)
    conf=read(OUT/'configuraciones_congeladas.json')
    assert conf['configuraciones']==candidatos() and conf['grupos']==GRUPOS and conf['ventanas']==ventanas()
    assert conf['cota_sin_fallos']==dict(internos=350,externos=24,repeticiones=4,total=378)
    assert read(OUT/'estructura_real.json')['cotejo_integral_exacto']
    refs=read(OUT/'referencias_guardadas.json');assert refs['aprobado'] and not refs['meta_v5_evaluada'] and not refs['modelos_cargados']
    check_hashes(refs['archivos_sha256']);check_hashes(refs['selecciones_sha256'])
    part=read(OUT/'partida.json')
    protected={p:h for p,h in part['snapshot_versionados'].items() if p!='experimentos_objetivo3_v5/CONTINUIDAD_V5.md'}
    check_hashes(protected)
    old=subprocess.check_output(['git','show',DOC+':experimentos_objetivo3_v5/CONTINUIDAD_V5.md'],cwd=ROOT).decode()
    assert (V5/'CONTINUIDAD_V5.md').read_text().endswith(old)
    return protected

def cerrar():
    if (OUT/'manifiesto_cierre.json').exists():raise ValueError('cierre ya existe; no sobrescribir congelación')
    protected=evidencia()
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT).decode()
    assert all(line[3:].startswith('experimentos_objetivo3_v5/') for line in status.splitlines())
    guardar(OUT/'conservacion_final.json',dict(aprobado=True,protegidos_sha256=protected,continuidad_previa_conservada=True,unica_modificacion_previa='v5/CONTINUIDAD_V5.md, antecedente íntegro al final',pdf_paginas=0,push=False))
    files=[p for p in (E1/'fuentes').glob('*.py')]+[E1/'PROTOCOLO_V5.md',E1/'requirements.lock.txt',E1/'reconstrucciones/panel_cambios.csv']
    files += [OUT/name for name in ['configuraciones_congeladas.json','entorno.json','estructura_real.json','referencias_guardadas.json','controles.json','verificacion_notebook.json']]
    modules=[]
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path:
            p=Path(path).resolve()
            if p.is_relative_to(ROOT) and p.suffix=='.py':modules.append(p)
    refs=read(OUT/'referencias_guardadas.json')
    mapping={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(files+modules))}
    mapping.update(refs['archivos_sha256']);mapping.update(refs['selecciones_sha256'])
    mapping[str(previo.anterior.BASE.relative_to(ROOT))]=sha(previo.anterior.BASE)
    mapping['experimentos_objetivo3_v4/etapa1/reconstrucciones/panel_cambios.csv']=sha(ROOT/'experimentos_objetivo3_v4/etapa1/reconstrucciones/panel_cambios.csv')
    guardar(OUT/'congelacion_previa.json',dict(version='5.0.0',fecha_cliente='2026-10-10',instante_utc=datetime.now(timezone.utc).isoformat(),artefactos_sha256=mapping,fuentes_reutilizadas_lectura=[str(p.relative_to(ROOT)) for p in sorted(set(modules)) if not p.is_relative_to(V5)],ajustes_panel=0,ledger_operativo_creado=False,presupuesto_real_iniciado=False,meta_v5_evaluada=False,requisito_etapa2='Otra autorización; nueva orquestación propia probada y congelada antes del primer fit real'))
    paths=[p for p in E1.rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']+[V5/'CONTINUIDAD_V5.md',V5/'PROMPT_ETAPA2_NUEVA_SESION.md',V5/'PLAN_INVESTIGACION_V5.md',V5/'REGISTRO_PREPARACION.json',V5/'PROMPT_ETAPA1_NUEVA_SESION.md']
    assert not any('__pycache__' in p.parts for p in paths)
    guardar(OUT/'manifiesto_cierre.json',dict(etapa='v5/etapa1',version='5.0.0',commit_partida=read(OUT/'partida.json')['commit_partida'],etapa1_completa=True,entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},ajustes_panel=0,presupuesto_real_iniciado=False,meta_v5_evaluada=False,pendientes_indispensables=[],pendientes_autorizacion=['etapa2','etapa3 condicionada a meta'],push=False))
    verificar()

def verificar():
    check_hashes(read(OUT/'conservacion_final.json')['protegidos_sha256'])
    check_hashes(read(OUT/'manifiesto_cierre.json')['entregables_sha256'])
    check_hashes(read(OUT/'congelacion_previa.json')['artefactos_sha256'])
    actual=entorno();expected=read(OUT/'entorno.json')
    assert all(actual[k]==expected[k] for k in ('python','paquetes','sklearn','lock_sha256','semilla','pip_check'))
    evidencia()
    print('Cierre etapa1 v5 verificado en lectura: cero fits panel; presupuesto real no iniciado; meta no evaluada.')
if __name__=='__main__':
    if sys.argv[1:]==['--verificar']:verificar()
    elif not sys.argv[1:]:cerrar()
    else:raise ValueError('argumentos no autorizados')
