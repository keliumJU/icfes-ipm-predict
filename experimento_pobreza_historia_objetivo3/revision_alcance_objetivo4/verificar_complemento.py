"""Lectura: conserva el cierre previo y verifica el inventario ampliado explícito."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
MAIN = HERE.parent

def digest(path):
    assert not path.is_symlink(), f"symlink: {path}"
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
    partida = json.loads((HERE / 'PARTIDA.json').read_text())
    for name, expected in partida['archivos_entrega_previa'].items():
        assert digest(MAIN / name) == expected, f"entrega previa alterada: {name}"
    manifest = json.loads((HERE / 'MANIFIESTO.json').read_text())
    for name, expected in manifest['sha256'].items():
        assert digest(HERE / name) == expected, f"complemento alterado: {name}"
    assert not any(p.is_symlink() for p in MAIN.rglob('*')), 'symlinks'
    paths = {p.relative_to(MAIN).as_posix() for p in MAIN.rglob('*') if p.is_file()}
    added = {f'{HERE.name}/{name}' for name in manifest['sha256']}
    exclusions = {f'{HERE.name}/{name}' for name in manifest['exclusiones']}
    assert paths - exclusions == set(partida['archivos_entrega_previa']) | added, 'inventario ampliado'
    # No modificar ni afirmar aprobación actual del control histórico de inventario.
    # Se ejecutan sus controles sustantivos intactos; el inventario ampliado se comprueba arriba.
    sys.path.insert(0, str(MAIN))
    sys.path.insert(0, str(MAIN / 'correccion_documental'))
    from verificar_entrega_corregida import verify as verify_closed
    closed = verify_closed(manifest=False)
    assert closed['aprobado'] and closed['new_fits'] == 0
    return {
        'aprobado': True,
        'solo_lectura': True,
        'archivos_previos_intactos': len(partida['archivos_entrega_previa']),
        'complemento_documental': True,
        'inventario_ampliado_control_propio': True,
        'verificador_historico_inventario_modificado': False,
        'controles_sustantivos_entrega': closed,
        'nuevos_ajustes': 0,
        'objetivo4_ejecutado': False,
        'autenticidad_resuelta': False,
        'disponibilidad_anticipada_resuelta': False,
        'avance_automatico': False,
    }

if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))
