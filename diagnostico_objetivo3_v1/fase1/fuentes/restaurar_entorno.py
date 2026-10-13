"""Recupera wheels exactos desde caché local sin alterar bytes ni fuentes analíticas.
Autorización expresa del usuario para reconstruir el entorno; no ejecuta diagnóstico.
El intérprete 3.12.14 procede del runtime local del escritorio, comprobado aparte.
"""
from pathlib import Path
import email
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'diagnostico_objetivo3_v1/fase1/resultados/restauracion_entorno'
WHEELS = Path('/tmp/icfes-diagnostico-wheels-exactos')
LOCK = ROOT / 'experimentos_objetivo3_v4/etapa1/requirements.lock.txt'


def main():
    wanted = {line.split('==')[0].lower().replace('_', '-'): line.split('==')[1]
              for line in LOCK.read_text().splitlines()}
    found = {}
    WHEELS.mkdir(exist_ok=False)
    for path in Path('/home/kelium/.cache/pip/http-v2').rglob('*.body'):
        try:
            with zipfile.ZipFile(path) as archive:
                metas = [n for n in archive.namelist() if n.endswith('.dist-info/METADATA')]
                if len(metas) != 1:
                    continue
                meta = email.message_from_bytes(archive.read(metas[0]))
                name = meta['Name'].lower().replace('_', '-')
                if wanted.get(name) != meta['Version']:
                    continue
                wheel = email.message_from_bytes(archive.read(metas[0].replace('METADATA', 'WHEEL')))
                tags = wheel.get_all('Tag')
                pieces = [tag.split('-') for tag in tags]
                tag = '-'.join('.'.join(dict.fromkeys(t[i] for t in pieces)) for i in range(3))
                fname = f"{name.replace('-', '_')}-{meta['Version']}-{tag}.whl"
                target = WHEELS / fname
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if name in found:
                    assert found[name]['sha256'] == digest, 'Wheels alternativos distintos requieren revisión'
                    continue
                shutil.copyfile(path, target)
                assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
                found[name] = dict(version=meta['Version'], origen=str(path), destino=str(target),
                                   sha256=digest, etiquetas_WHEEL=tags, bytes_iguales=True)
        except zipfile.BadZipFile:
            continue
    assert set(found) == set(wanted), f"Faltan {set(wanted) - set(found)}"
    assert not OUT.is_symlink() and OUT.resolve().is_relative_to(ROOT / 'diagnostico_objetivo3_v1')
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'wheels.json').write_text(json.dumps(dict(
        autorizacion='Usuario: si porfavor continua; reconstrucción exacta e instalaciones autorizadas',
        origen_python='/home/kelium/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
        lock_sha256=hashlib.sha256(LOCK.read_bytes()).hexdigest(), paquetes=found,
        descargas_red=0, fuentes_analiticas_nuevas=0), indent=2, ensure_ascii=False)+'\n')
    print('54 wheels exactos recuperados; bytes intactos; cero descargas de red.')


if __name__ == '__main__':
    main()
