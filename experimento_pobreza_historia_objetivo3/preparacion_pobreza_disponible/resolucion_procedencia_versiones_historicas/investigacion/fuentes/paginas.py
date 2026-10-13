"""Leer páginas explícitas; textos/renders temporales en /tmp. No marca revisión."""
from iniciar import HERE
from pathlib import Path
from pypdf import PdfReader
import sys,subprocess
if __name__=='__main__':
    arg=sys.argv[1]
    p=HERE/arg
    if not p.exists(): p=HERE.parent.parent/arg
    assert p.suffix=='.pdf' and p.exists()
    b=PdfReader(p)
    for i in map(int,sys.argv[2:]):
        assert 1<=i<=len(b.pages)
        t=b.pages[i-1].extract_text() or ''
        print(f'{p.name} página PDF {i}\n{t}\n')
        Path(f'/tmp/icfes_vintage_paginas/{p.stem}_p{i}.txt').write_text(t)
