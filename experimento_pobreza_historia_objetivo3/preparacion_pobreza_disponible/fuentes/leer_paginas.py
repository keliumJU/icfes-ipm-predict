"""Extrae únicamente páginas seleccionadas de documentos en /tmp con Poppler.

Uso: python -B fuentes/leer_paginas.py /tmp/documento.pdf 1 2 3
Salidas temporales /tmp; no declara lectura automática ni guarda microdatos.
"""
import subprocess, sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
assert source.is_relative_to('/tmp') and source.suffix == '.pdf'
for page in map(int, sys.argv[2:]):
    assert page > 0
    output = Path('/tmp') / f'{source.stem}_p{page}.txt'
    subprocess.run(['pdftotext', '-layout', '-f', str(page), '-l', str(page), str(source), str(output)], check=True)
    print(f'\n{source.name} página PDF {page}\n{output.read_text()}')
