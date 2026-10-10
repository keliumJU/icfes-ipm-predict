"""Snapshot y manifiestos: nuevas escrituras exclusivamente en v2."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / 'experimentos_objetivo3_v2'
OUT = V2 / 'fase1/resultados'
PARTIDA = '742c66577abaeade216d0498e4ecfd12d4c7abfb'
CIERRE_V1 = 'fc8dc23de8a85cffcc1c87d47ac740650b27ace5'
CIERRES = {
    'protocolo/evidencia/manifiesto_cierre.json': '7e95ffe823c3d08f345620c0f9bc65dc72fae7d5',
    'fase3/resultados/manifiesto_cierre.json': '9a22b8adc406423fa6829b75e77d7473deffe710',
    'fase4/resultados/manifiesto_cierre.json': 'da48e1a4f85d206e8753fbad85b78ba2e3858b1a',
    'fase5/resultados/manifiesto_cierre.json': '9becbc3239a540dfa8f31f45c281ac3a61361d19',
    'fase6/resultados/manifiesto_cierre.json': CIERRE_V1,
}
INPUTS = [
    'auditoria/base_analitica_departamento_anio.csv',
    'raw_data/Examen_Saber_11_20251.txt', 'raw_data/Examen_Saber_11_20252.txt',
    'Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx',
    'Fuente del IPM/anex-PMultidimensional-Departamental-2024.xlsx',
    'panel_departamento_anio_unido_2025.csv', 'panel_departamento_anio_unido.csv',
]

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')

def inicio():
    dest = OUT / 'integridad_inicial.json'
    if dest.exists():
        raise RuntimeError('Snapshot existente: no sustituir partida histórica.')
    assert git('rev-parse', 'HEAD').decode().strip() == PARTIDA
    controles = []
    for nombre, cierre in CIERRES.items():
        m = json.loads((ROOT / nombre).read_text())
        for ruta, esperado in m.get('entregables_sha256', m).items():
            actual = sha(ROOT / ruta)
            estado = 'coincide'
            if actual != esperado:
                assert ruta == 'CONTINUIDAD_OBJETIVO_3.md' or (
                    ruta == 'informe_objetivo_3.md' and nombre.startswith('fase5'))
                historica = hashlib.sha256(git('show', f'{cierre}:{ruta}')).hexdigest()
                assert historica == esperado, (nombre, ruta)
                estado = 'histórico cotejado en su commit; versión vigente conservada'
            controles.append(dict(manifiesto=nombre, ruta=ruta, esperado=esperado, actual=actual, estado=estado))
    tracked = {p: sha(ROOT / p) for p in git('ls-files', '-z').decode().split('\0') if p and (ROOT / p).is_file()}
    sources = {p: dict(sha256=sha(ROOT / p), bytes=(ROOT / p).stat().st_size) for p in INPUTS}
    assert sources[INPUTS[0]]['sha256'] == '609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866'
    save(dest, dict(fecha_cliente='2026-10-10', commit_partida=PARTIDA, cierre_v1=CIERRE_V1,
        cambios_usuario=git('diff', '--name-status', CIERRE_V1, PARTIDA).decode(),
        rama=git('branch', '--show-current').decode().strip(),
        git_status_inicial=git('status', '--short').decode(),
        snapshot_versionados=tracked, fuentes=sources, controles=controles))
    print(json.dumps(dict(huellas=len(controles), archivos_previos=len(tracked), fuentes=len(sources))))

def verificar_conservacion():
    m = json.loads((OUT / 'integridad_inicial.json').read_text())
    for p, h in m['snapshot_versionados'].items():
        assert sha(ROOT / p) == h, p
    for p, spec in m['fuentes'].items():
        assert sha(ROOT / p) == spec['sha256'], p
    return m

def cierre():
    m = verificar_conservacion()
    save(OUT / 'conservacion_final.json', dict(aprobado=True,
        archivos_previos_intactos=len(m['snapshot_versionados']), fuentes_intactas=len(m['fuentes']),
        excepciones=[], modelos_ajustados=0, predicciones_nuevas=0, simulaciones=0,
        notebooks_modelos_generados=0, push=False))
    files = {str(p.relative_to(ROOT)): sha(p) for p in sorted(V2.rglob('*'))
             if p.is_file() and p.name != 'manifiesto_cierre.json' and '__pycache__' not in p.parts}
    save(OUT / 'manifiesto_cierre.json', dict(fecha_cliente='2026-10-10', commit_partida=PARTIDA,
        fase='v2/fase1', entregables_sha256=files, entrenamiento=False, push=False))
    print(json.dumps(dict(conservacion=True, entregables=len(files))))

if __name__ == '__main__':
    inicio() if '--inicio' in sys.argv else cierre()
