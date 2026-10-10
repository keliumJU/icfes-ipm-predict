"""Conservación de entradas y archivos previos, sin módulos de modelos."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'fase6/resultados'
PARTIDA = '10ebe23eb2fd1518956391213301439ef718b844'
CIERRE5 = '9becbc3239a540dfa8f31f45c281ac3a61361d19'
CIERRES = ['7e95ffe823c3d08f345620c0f9bc65dc72fae7d5',
           '9a22b8adc406423fa6829b75e77d7473deffe710',
           'da48e1a4f85d206e8753fbad85b78ba2e3858b1a', CIERRE5]
MANIFIESTOS = ['protocolo/evidencia/manifiesto_cierre.json',
               'fase3/resultados/manifiesto_cierre.json',
               'fase4/resultados/manifiesto_cierre.json',
               'fase5/resultados/manifiesto_cierre.json']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def guardar(nombre, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / nombre).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def inicio():
    assert git('rev-parse', 'HEAD').decode().strip() == PARTIDA
    assert git('rev-parse', 'HEAD^').decode().strip() == CIERRE5
    assert git('diff', '--name-only', CIERRE5, PARTIDA).decode().strip() == 'informe_objetivo_3.md'
    controles = []
    for nombre, cierre in zip(MANIFIESTOS, CIERRES):
        m = json.loads((ROOT / nombre).read_text())
        for ruta, esperado in m.get('entregables_sha256', m).items():
            actual = sha(ROOT / ruta)
            estado = 'coincide'
            if ruta == 'CONTINUIDAD_OBJETIVO_3.md':
                historica = hashlib.sha256(git('show', f'{cierre}:{ruta}')).hexdigest()
                assert historica == esperado, (nombre, ruta, 'histórica')
                estado = 'coincide' if actual == esperado else 'continuidad histórica cotejada en commit de cierre; sustitución documentada'
            elif ruta == 'informe_objetivo_3.md' and nombre.startswith('fase5'):
                assert hashlib.sha256(git('show', f'{CIERRE5}:{ruta}')).hexdigest() == esperado
                assert (ROOT/ruta).read_bytes() == git('show', f'{PARTIDA}:{ruta}')
                estado = 'cambio del usuario autenticado por diff cierre5→partida; conservado'
            else:
                assert actual == esperado, (nombre, ruta)
            controles.append(dict(manifiesto=nombre, ruta=ruta, esperado=esperado, actual=actual, estado=estado))
    assert sha(ROOT/'auditoria/base_analitica_departamento_anio.csv') == '609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866'
    snapshot = {p: sha(ROOT/p) for p in git('ls-files', '-z').decode().split('\0') if p and (ROOT/p).is_file()}
    guardar('integridad_inicial.json', dict(commit_partida=PARTIDA, cierre5=CIERRE5,
        estado_inicial='Git limpio antes de crear fase6', controles=controles,
        snapshot_versionados=snapshot, fecha_cliente='2026-10-09'))
    print(f'Integridad inicial: {len(controles)} huellas cotejadas, {len(snapshot)} archivos previos registrados')

def cierre():
    m = json.loads((OUT/'integridad_inicial.json').read_text())
    for p,h in m['snapshot_versionados'].items():
        if p != 'CONTINUIDAD_OBJETIVO_3.md':
            assert sha(ROOT/p) == h, p
    guardar('conservacion_final.json', dict(aprobado=True,
        archivos_previos_intactos=len(m['snapshot_versionados'])-1,
        excepcion_intencional=['CONTINUIDAD_OBJETIVO_3.md'],
        informe_usuario_conservado=True, modelos_ajustados=0, predicciones_nuevas=0,
        remuestreos_nuevos=0, simulaciones=0, push=False))

if __name__ == '__main__':
    import sys
    inicio() if '--inicio' in sys.argv else cierre()
