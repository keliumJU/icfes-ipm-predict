"""Verificador de lectura: conservación previa e inventario ampliado propio."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
MAIN = HERE.parent

def sha(path):
    assert not path.is_symlink(), f'Symlink no autorizado: {path}'
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
    partida = json.loads((HERE / 'PARTIDA.json').read_text())
    old = partida['archivos_previos_sha256']
    for name, expected in old.items():
        assert sha(MAIN / name) == expected, f'Archivo previo alterado: {name}'
    manifest = json.loads((HERE / 'MANIFIESTO.json').read_text())
    for name, expected in manifest['sha256'].items():
        assert sha(HERE / name) == expected, f'Entrega nueva alterada: {name}'
    assert not any(p.is_symlink() for p in MAIN.rglob('*')), 'Symlinks'
    actual = {p.relative_to(MAIN).as_posix() for p in MAIN.rglob('*') if p.is_file()}
    added = {f'{HERE.name}/{name}' for name in manifest['sha256']}
    exclusions = {f'{HERE.name}/{name}' for name in manifest['exclusiones']}
    assert actual - exclusions == set(old) | added, 'Inventario ampliado incorrecto'
    for folder, filename in [('', 'MANIFIESTO_FINAL.json'), ('revision_alcance_objetivo4', 'MANIFIESTO.json')]:
        base = MAIN / folder
        prior = json.loads((base / filename).read_text())
        for name, expected in prior['sha256'].items():
            assert sha(base / name) == expected, f'Manifiesto anterior: {name}'
    prompt = (HERE / 'PROMPT_NUEVA_SESION.md').read_text()
    requirements = [
        'exclusivamente la preparación documental',
        'sitios oficiales del DANE y del ICFES',
        'No descargar microdatos, raw ni nuevos paneles',
        'No autoriza ajustes, nuevos datasets analíticos, escenarios ni ejecución del objetivo 4',
        'No heredes presupuestos anteriores',
        'No supongas que un rezago anual garantiza disponibilidad',
        'fuentes `.py`',
        'nunca crees notebooks directamente',
        'Ningún avance automático',
    ]
    for text in requirements:
        assert text in prompt, f'Requisito ausente: {text}'
    return {
        'aprobado': True,
        'solo_lectura': True,
        'archivos_previos_intactos': len(old),
        'manifiestos_anteriores_intactos': True,
        'inventario_ampliado_control_propio': True,
        'restricciones_prompt_comprobadas': len(requirements),
        'preparacion_documental_futura_ejecutada': False,
        'ajustes_nuevos': 0,
        'consultas_externas_realizadas': 0,
        'objetivo4_ejecutado': False,
        'nueva_auditoria_modelos_o_entorno': False,
        'avance_automatico': False,
    }

if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))
