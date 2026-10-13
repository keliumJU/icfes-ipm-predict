from pathlib import Path
import hashlib, json, os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def sha(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()

def verify():
    baseline = json.loads((HERE/'PARTIDA_PLAN.json').read_text())
    manifest = json.loads((HERE/'MANIFIESTO_PLAN.json').read_text())
    for name, expected in baseline['sha256'].items():
        assert sha(ROOT/name) == expected, f'Original alterado: {name}'
    for name, expected in manifest['sha256'].items():
        assert sha(HERE/name) == expected, f'Entrega alterada: {name}'
    actual = set()
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in baseline['exclusiones_directorios'] and not (Path(base)/d).is_symlink()]
        for name in names:
            p = Path(base)/name
            if p.is_file() and not p.is_symlink(): actual.add(p.relative_to(ROOT).as_posix())
    prefix = HERE.relative_to(ROOT).as_posix()+'/'
    own = {prefix+n for n in manifest['sha256']} | {prefix+n for n in manifest['exclusiones']}
    assert actual == set(baseline['sha256']) | own, 'Inventario cerrado cambió; requiere nueva partida, no modificar este verificador'
    return dict(conservacion_aprobada=True, archivos_previos=len(baseline['sha256']), archivos_paquete=len(manifest['sha256']), investigacion_ejecutada=False, modelos_ejecutados=False, disponibilidad_historica_certificada=False, avance_automatico=False)

if __name__ == '__main__': print(json.dumps(verify(), ensure_ascii=False))
