"""Verificación propia en lectura; no verifica un piloto ni hace ajustes."""
from pathlib import Path
import hashlib, json, os, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def sha(path):
    if path.is_symlink():
        return hashlib.sha256(os.readlink(path).encode()).hexdigest()
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def load(path):
    return json.loads(path.read_text())

def verify():
    baseline = load(HERE/'preparacion/PARTIDA.json')
    for name, digest in baseline['protegidos'].items():
        assert sha(ROOT/name) == digest, 'Original modificado: '+name
    git = lambda *a: subprocess.check_output(['git', *a], cwd=ROOT).decode().strip()
    assert git('rev-parse', 'HEAD') == baseline['head']
    assert git('branch', '--show-current') == baseline['rama']
    assert git('log', '-1', '--format=%s') == baseline['asunto']
    assert git('diff', '--name-only', 'HEAD') == baseline['tracked_diff']
    paths = git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split('\0')
    foreign = [s for s in paths if s and s not in baseline['protegidos'] and not s.startswith(HERE.name+'/')]
    assert not foreign, 'Rutas nuevas fuera del alcance: '+str(foreign)
    manifest = load(HERE/'MANIFIESTO_PREPARACION.json')
    for name, digest in manifest['sha256'].items():
        assert sha(HERE/name) == digest, 'Preparación modificada: '+name
    inventory = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
    assert inventory-{ 'MANIFIESTO_PREPARACION.json' } == set(manifest['sha256'])
    closure = load(HERE/'preparacion/CIERRE_PREPARACION.json')
    assert closure['real_fits'] == closure['synthetic_fits'] == 0 and not closure['pilot_started']
    assert load(HERE/'preparacion/VERIFICACION_ANTERIOR.json')['aprobado']
    return dict(aprobado=True,modo='solo lectura; preparación, no piloto',originales=len(baseline['protegidos']),archivos_preparacion=len(manifest['sha256']),fits=0,ejecucion_pendiente=True)

if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))
