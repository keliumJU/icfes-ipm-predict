"""Registrar partida antes de adquisiciones/procesamiento; solo archivos regulares.
La única escritura es dentro de investigacion. No lee registros TXT: los hashea.
"""
from pathlib import Path
import os, hashlib, json, datetime
HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()
def inventory():
    exclusions=json.loads((HERE.parent/'PARTIDA_PLAN.json').read_text())['exclusiones_directorios']
    found={}
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in exclusions and not (Path(base)/d).is_symlink() and Path(base)/d != HERE]
        for n in names:
            p=Path(base)/n
            if p.is_file() and not p.is_symlink(): found[p.relative_to(ROOT).as_posix()]=sha(p)
    return exclusions,found
if __name__=='__main__':
    target=HERE/'PARTIDA.json'
    assert not target.exists(), 'No sobrescribir partida'
    ex,files=inventory()
    target.write_text(json.dumps(dict(fecha_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exclusiones_directorios=ex,exclusion_nueva=str(HERE.relative_to(ROOT)),sha256=files,arranque=dict(conservacion_aprobada=True,archivos_previos=39001,archivos_paquete=7),limite='No certifica destinos de enlaces ni Git/runtime/cache excluidos.'),indent=2)+'\n')
    print(json.dumps({'archivos_preservados':len(files)}))
