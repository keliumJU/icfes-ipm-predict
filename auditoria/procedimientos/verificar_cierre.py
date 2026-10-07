"""Control de conservación y coherencia de la entrega; no valida el origen ausente.

Leer antes de ejecutar. Solo lee insumos y escribe evidencia agregada de cierre.
El inventario de referencia no se modifica.
"""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
AUD = ROOT / 'auditoria'
EV = AUD / 'evidencia'


def rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    inventory = rows(AUD / 'inventario_trazabilidad.csv')
    checked = []
    for item in inventory:
        path = ROOT / item['archivo']
        if item['tipo'] == 'directorio vacío':
            assert path.is_dir() and not any(path.iterdir()), item['archivo']
            continue
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                digest.update(block)
        assert path.stat().st_size == int(item['bytes']), item['archivo']
        assert digest.hexdigest() == item['sha256'], item['archivo']
        checked.append(item['archivo'])

    required = ['diagnostico_calidad.md', 'auditoria_afirmaciones.csv',
                'inventario_trazabilidad.csv', 'mapa_tesis.md',
                'procedimientos/README.md']
    assert all((AUD / name).is_file() for name in required)
    assert (ROOT / 'CONTINUIDAD_OBJETIVO_3.md').is_file()
    claims = rows(AUD / 'auditoria_afirmaciones.csv')
    assert len(claims) == 59
    assert len({r['id'] for r in claims}) == len(claims)
    assert all(r['ubicacion'] and r['evidencia_verificable'] for r in claims)
    structure = rows(EV / 'estructura_duplicados.csv')
    assert len(structure) == 12
    for r in structure:
        assert all(int(r[k]) == 0 for k in [
            'filas_ancho_incorrecto', 'filas_con_tab_en_campos',
            'filas_repetidas_exactas_exceso'])
    conservation = rows(EV / 'conservacion_registros.csv')
    assert len(conservation) == 12
    assert all(float(r['no_en_fuente_exceso_multiconjunto']) == 0
               for r in conservation if r['periodo'] != '20181')
    levels = rows(EV / 'niveles_desempeno.csv')
    assert sum(int(r['n']) for r in levels if r['control'] == 'comparaciones') == 13604400
    assert sum(int(r['n']) for r in levels if r['control'] == 'discrepancias') == 0
    ipm = json.loads((EV / 'resumen_ipm.json').read_text())
    assert ipm['celdas_cotejadas'] == 3168 and ipm['diferencias_numericas'] == 0
    sec115 = json.loads((EV / 'resumen_seccion115.json').read_text())
    assert sec115['coincidencias_entre'] == sec115['coincidencias_celdas'] == 16
    poppler = {}
    for command in ['pdftotext', 'pdftoppm']:
        p = subprocess.run([command, '-v'], capture_output=True, text=True, check=True)
        poppler[command] = (p.stdout + p.stderr).splitlines()[0]
    result = {
        'fecha_sesion': '2026-10-07',
        'insumos_archivo_sha256_y_tamano_inalterados': len(checked),
        'directorios_vacios_conservados': len(inventory) - len(checked),
        'insumos_ignorados_inventariados': sum(r['estado_git'] == 'ignorado' for r in inventory),
        'afirmaciones': len(claims), 'dictamenes': dict(Counter(r['dictamen'] for r in claims)),
        'filas_estructura_comprobadas': sum(int(r['filas']) for r in structure),
        'periodos_conservacion_proyeccion_verificada': 11,
        'periodo_sin_fuente_para_conservacion': '20181',
        'versiones_actuales_poppler': poppler,
        'controles_cierre': 'satisfactorios para conservación y coherencia interna',
        'auditoria_completa': False,
        'limitacion': 'No valida origen ausente ni filtros históricos; ver pendientes en continuidad',
    }
    (EV / 'verificacion_cierre.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
