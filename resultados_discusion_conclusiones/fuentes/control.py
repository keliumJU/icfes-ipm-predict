"""Control propio de ampliación documental; no procesa datos analíticos."""
from pathlib import Path
import datetime, hashlib, json, os, sys
ROOT = Path('/home/kelium/Documents/espcarlos/icfes-predict-improved')
HERE = ROOT / 'resultados_discusion_conclusiones'
EX = json.loads((ROOT/'plan_cierre_cuatro_objetivos_20261012/PARTIDA.json').read_text())['exclusiones_directorios']
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()
def inventory():
    result = {}
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EX and not (Path(base)/d).is_symlink() and Path(base)/d != HERE]
        for name in names:
            p = Path(base)/name
            if p.is_file() and not p.is_symlink(): result[p.relative_to(ROOT).as_posix()] = sha(p)
    return result
def own():
    return {p.relative_to(HERE).as_posix(): sha(p) for p in HERE.rglob('*') if p.is_file() and p.name not in ('MANIFIESTO.json', 'VERIFICACION.json')}
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'inicio':
        assert not HERE.exists(), 'Leer continuidad existente; no sobrescribir'
        files = inventory()
        # La partida se registra fuera de la entrega antes de escribir en ella.
        temp = Path('/tmp/partida_resultados_discusion_conclusiones.json')
        temp.write_text(json.dumps(dict(fecha_local='2026-10-12', fecha_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=sys.version, sha256=files, exclusiones_directorios=EX, exclusion_nueva=HERE.name, limite='Archivos regulares; no certifica enlaces ni directorios excluidos. No incluye ni modifica .git o runtime excluido.', verificacion_previa='python3 -B objetivo4_validacion_escenarios/fuentes/control.py verificar: exit 0; conservación externa e integridad aprobadas antes de ampliación.'), ensure_ascii=False, indent=2)+'\n')
        (HERE/'fuentes').mkdir(parents=True)
        (HERE/'PARTIDA.json').write_bytes(temp.read_bytes())
        (HERE/'fuentes/control.py').write_bytes(Path(__file__).read_bytes())
        print(json.dumps({'partida_archivos':len(files), 'control_nuevo':True}))
    elif mode in ('cierre', 'verificar'):
        files = inventory()
        assert files == json.loads((HERE/'PARTIDA.json').read_text())['sha256'], 'Estado externo cambió'
        current = own()
        if mode == 'cierre':
            assert not (HERE/'MANIFIESTO.json').exists(), 'No sobrescribir cierre'
            (HERE/'MANIFIESTO.json').write_text(json.dumps({'sha256':current}, ensure_ascii=False, indent=2)+'\n')
            result = dict(conservacion_aprobada=True, archivos_previos=len(files), archivos_entrega=len(current), alcance='Síntesis editorial de resultados, discusión y conclusiones; sin ajustes nuevos', ejecucion_nueva=False, tesis_modificada=False)
            (HERE/'VERIFICACION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
            print(json.dumps(result, ensure_ascii=False))
        else:
            assert current == json.loads((HERE/'MANIFIESTO.json').read_text())['sha256'], 'Entrega cambió'
            print('Conservación externa e integridad documental aprobadas')
    else: raise ValueError(mode)
