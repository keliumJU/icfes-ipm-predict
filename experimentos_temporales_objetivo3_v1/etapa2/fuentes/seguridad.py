"""Destinos propios; ninguna importación de runners históricos."""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).absolute().parents[3]
OWN = ROOT / 'experimentos_temporales_objetivo3_v1'
E1 = OWN / 'etapa2'
OUT = E1 / 'resultados'
TEST = OUT / 'inventados'


def destino(path, base=E1):
    p = Path(path).absolute()
    base = Path(base).absolute()
    if base not in (E1, TEST, OWN):
        raise ValueError('Base no autorizada')
    if not p.is_relative_to(base) or '..' in p.parts:
        raise ValueError('Fuera del destino autorizado')
    # Verificar también el propio root/base, antes de resolver o crear directorios.
    for part in [p, *p.parents]:
        if part.is_symlink():
            raise ValueError('Symlink en destino')
        if part == ROOT:
            break
    if not p.resolve().is_relative_to(base.resolve()):
        raise ValueError('Destino resuelto fuera de base')
    if base == OWN and p != OWN / 'CONTINUIDAD_EXPERIMENTAL.md':
        raise ValueError('Solo continuidad propia fuera de etapa1')
    return p


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def leer(path):
    return json.loads(Path(path).read_text())


def texto_nuevo(path, value, base=E1):
    p = destino(path, base)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        f.write(value)


def guardar(path, value, base=E1):
    texto_nuevo(path, json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', base)


def checkpoint(path, value):
    """Actualización atómica SOLO estado inventado propio, nunca archivos ajenos."""
    p = destino(path, E1)
    tmp = destino(p.with_suffix(p.suffix + '.tmp'), E1)
    p.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.flush()
        os.fsync(f.fileno())
    destino(p, E1)
    os.replace(tmp, p)
