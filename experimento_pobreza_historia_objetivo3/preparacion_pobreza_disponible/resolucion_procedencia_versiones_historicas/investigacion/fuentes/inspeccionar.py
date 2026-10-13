"""Inspección de estructura agregada y localización automática en documentación.
Índice de coincidencias PDF no equivale a páginas revisadas por el investigador.
"""
from iniciar import HERE, ROOT
import sys, json
sys.path.insert(0,'/tmp/icfes_vintage_deps')
import xlrd, openpyxl
from pypdf import PdfReader
def sheets(p):
    if p.suffix=='.xls':
        b=xlrd.open_workbook(p)
        return [(s.name,[[s.cell_value(r,c) for c in range(s.ncols)] for r in range(s.nrows)]) for s in b.sheets()]
    b=openpyxl.load_workbook(p,read_only=True,data_only=True)
    result=[(s.title,[list(r) for r in s.iter_rows(values_only=True)]) for s in b];b.close();return result
if __name__=='__main__':
    if sys.argv[1]=='books':
        for p in sorted((HERE/'evidencia').glob('*.xls*'))+sorted((ROOT/'Fuente del IPM').glob('*.xlsx')):
            print(p.name)
            for n,rows in sheets(p):
                if 'Depart' in n or 'depart' in n:
                    print(n,len(rows),max(map(len,rows)))
                    for i,r in enumerate(rows[:20]):
                        print(i+1,[(j+1,v) for j,v in enumerate(r) if v is not None and v!=''])
    elif sys.argv[1]=='pdf':
        index=[]
        for p in sorted((HERE/'evidencia').glob('icfes*.pdf')):
            b=PdfReader(p); hits=[]
            for i,page in enumerate(b.pages):
                t=page.extract_text() or ''
                if any(w in t.lower() for w in ['dataicfes','data icfes','ftp','carga anonimizada']):
                    hits.append(i+1)
                    Path=__import__('pathlib').Path
                    dest=Path('/tmp/icfes_vintage_paginas');dest.mkdir(exist_ok=True)
                    (dest/f'{p.stem}_p{i+1}.txt').write_text(t)
            index.append(dict(archivo=str(p.relative_to(HERE)),paginas=len(b.pages),localizadas_automaticamente=hits,revisadas=[],pendientes='Todas salvo lectura explícita posterior'))
        (HERE/'INDICE_PDF.json').write_text(json.dumps(index,indent=2)+'\n');print(json.dumps(index))
