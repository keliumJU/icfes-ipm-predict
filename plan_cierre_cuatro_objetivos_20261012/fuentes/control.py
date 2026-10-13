"""Inventario previo y cierre del paquete documental; no ejecuta análisis."""
from pathlib import Path
import os,hashlib,json,sys,datetime
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parent
PREVIOUS=ROOT/'revision_cumplimiento_objetivos_20261012'
HISTORY=ROOT/'experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/resolucion_procedencia_versiones_historicas/investigacion'
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def inventory():
    exclusions=json.loads((PREVIOUS/'PARTIDA.json').read_text())['exclusiones_directorios']
    files={}
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in exclusions and not (Path(base)/d).is_symlink() and Path(base)/d!=HERE]
        for name in names:
            path=Path(base)/name
            if path.is_file() and not path.is_symlink():files[path.relative_to(ROOT).as_posix()]=sha(path)
    return exclusions,files
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='inicio':
        assert not (HERE/'PARTIDA.json').exists(),'No sobrescribir partida'
        ex,files=inventory()
        (HERE/'PARTIDA.json').write_text(json.dumps(dict(fecha_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,exclusiones_directorios=ex,exclusion_nueva=str(HERE.relative_to(ROOT)),sha256=files,limite='Archivos regulares; no certifica enlaces ni directorios excluidos. Revisión previa verificada antes de ampliar.'),ensure_ascii=False,indent=2)+'\n')
        print('Archivos previos registrados:',len(files))
    else:
        _,files=inventory()
        assert files==json.loads((HERE/'PARTIDA.json').read_text())['sha256'],'Estado externo cambió'
        for prior in [PREVIOUS,HISTORY]:
            manifest=json.loads((prior/'MANIFIESTO.json').read_text())['sha256']
            assert all(sha(prior/name)==value for name,value in manifest.items()),'Entrega anterior cambió'
        own={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and p.name not in ['MANIFIESTO.json','VERIFICACION.json']}
        if mode=='cierre':
            assert not (HERE/'MANIFIESTO.json').exists(),'No sobrescribir cierre'
            for name in ['PLAN_POR_OBJETIVOS.md','PROMPT_NUEVA_SESION.md','CONTINUIDAD.md','README.md']:
                assert (HERE/name).is_file()
            (HERE/'MANIFIESTO.json').write_text(json.dumps(dict(sha256=own),ensure_ascii=False,indent=2)+'\n')
            result=dict(conservacion_aprobada=True,archivos_previos=len(files),archivos_paquete=len(own),revision_previa_preservada=True,investigacion_historica_preservada=True,modelos_nuevos=0,escenarios_nuevos=0,tesis_modificada=False,estado='Plan y prompt preparados; decisiones por objetivo pendientes en nueva sesión')
            (HERE/'VERIFICACION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps(result,ensure_ascii=False))
        elif mode=='verificar':
            assert own==json.loads((HERE/'MANIFIESTO.json').read_text())['sha256'],'Paquete cambió'
            expected=set(own)|{'MANIFIESTO.json','VERIFICACION.json'}
            actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
            assert actual==expected,'Inventario del paquete cambió'
            print('Conservación e integridad aprobadas; verificación de solo lectura.')
        else:raise ValueError(mode)
