"""Utilidades documentales; no importa código científico ni lee registros individuales.

Python estándar, sin instalación ni semilla (no hay aleatoriedad).
Huellas y metadatos locales: python -B fuentes/documental.py
PDF: extraer páginas explícitas con pdftotext en /tmp; registrar lectura aparte.
No descarga datos, no genera paneles, no ajusta modelos.
"""
from pathlib import Path
import hashlib, json, datetime, zipfile, xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def write_json(name, obj):
    path = HERE / name
    assert path.resolve().is_relative_to(HERE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def metadata():
    partida = json.loads((HERE / 'PARTIDA_DOCUMENTAL.json').read_text())
    names = ['Fuente del IPM/anex-PMultidimensional-Departamental-2024.xlsx',
             'Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx',
             'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv']
    names += [f'raw_data/Examen_Saber_11_{year}{period}.txt'
              for year in [2018, 2019, 2021, 2022, 2023, 2024, 2025] for period in [1, 2]]
    rows = []
    for name in names:
        p = ROOT / name
        assert sha(p) == partida['archivos_previos_sha256'][name]
        st = p.stat()
        row = dict(archivo=name, sha256=sha(p), bytes=st.st_size,
                   modificacion_local_utc=datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).isoformat(),
                   adquisicion='NO DEMOSTRADA', primera_publicacion_del_archivo_exacto='NO DEMOSTRADA',
                   limitacion='mtime no acredita adquisición ni publicación. TXT solo huella, sin lectura de registros.')
        if p.suffix == '.xlsx':
            with zipfile.ZipFile(p) as z:
                core = ET.fromstring(z.read('docProps/core.xml'))
                row['propiedades_ooxml'] = {s.tag.split('}')[-1]: s.text for s in core
                                            if s.tag.split('}')[-1] in ['created', 'modified', 'revision']}
                w = ET.fromstring(z.read('xl/workbook.xml'))
                row['hojas'] = [s.attrib['name'] for s in w.findall('.//{*}sheet')]
                texts = [''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('{*}si')]
                row['rotulos_privaciones'] = [s for s in texts if 'Privaciones por hogar según variable\nDepartamentos' in s]
            row['limitacion'] += ' Propiedades del libro son metadatos editables; no prueban origen.'
        rows.append(row)
    write_json('METADATOS_LOCALES.json', rows)
    print(json.dumps({'archivos': len(rows), 'solo_huellas_y_metadatos': True}))

if __name__ == '__main__':
    metadata()
