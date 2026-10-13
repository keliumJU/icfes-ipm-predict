"""Conservar estado previo y verificar entrega documental; sin ajustes ni datos personales."""
from pathlib import Path
import os,hashlib,json,sys,datetime
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parent
OLD=ROOT/'experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/resolucion_procedencia_versiones_historicas/investigacion'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def inventory():
    exclusions=json.loads((OLD/'PARTIDA.json').read_text())['exclusiones_directorios']
    found={}
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in exclusions and not (Path(base)/d).is_symlink() and Path(base)/d!=HERE]
        for name in names:
            p=Path(base)/name
            if p.is_file() and not p.is_symlink():found[p.relative_to(ROOT).as_posix()]=sha(p)
    return exclusions,found
if __name__=='__main__':
    if sys.argv[1]=='inicio':
        assert not (HERE/'PARTIDA.json').exists()
        ex,files=inventory()
        (HERE/'PARTIDA.json').write_text(json.dumps(dict(fecha_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=files,exclusiones_directorios=ex,exclusion_nueva=str(HERE.relative_to(ROOT)),limite='Archivos regulares; no certifica enlaces ni directorios excluidos. Verificador previo aprobado antes de ampliar inventario.'),ensure_ascii=False,indent=2)+'\n')
        print('Archivos previos registrados:',len(files))
    else:
        partida=json.loads((HERE/'PARTIDA.json').read_text())
        _,current=inventory()
        assert current==partida['sha256'],'Cambio fuera de nueva entrega'
        previous=json.loads((OLD/'MANIFIESTO.json').read_text())['sha256']
        assert all(sha(OLD/name)==value for name,value in previous.items())
        files={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and p.name not in ['MANIFIESTO.json','VERIFICACION.json']}
        if sys.argv[1]=='cierre':
            assert not (HERE/'MANIFIESTO.json').exists()
            (HERE/'MANIFIESTO.json').write_text(json.dumps(dict(sha256=files),ensure_ascii=False,indent=2)+'\n')
            result=dict(conservacion_aprobada=True,archivos_previos=len(current),archivos_entrega=len(files),rama_historica_preservada=True,modelos_nuevos=0,escenarios_nuevos=0,tesis_modificada=False,preferencias_objetivo3='Pendientes de respuesta humana; no inferidas por silencio')
            (HERE/'VERIFICACION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps(result,ensure_ascii=False))
        else:
            assert files==json.loads((HERE/'MANIFIESTO.json').read_text())['sha256']
            print('Conservación e integridad aprobadas; sin escrituras.')
