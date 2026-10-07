"""Localiza páginas completas y conserva mapa y hashes, sin versionar textos PDF completos.

El estado de lectura humana es explícito; extraer una página no equivale a revisarla.
Las imágenes para inspección se guardan fuera del repositorio y no cambian los PDF.
"""
from pathlib import Path
import csv, hashlib, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'auditoria/evidencia'
REVIEWED={10,11,25,*range(30,34),*range(50,61),*range(63,75),*range(85,89),*range(95,119)}
VISUAL={66,68,73,88,96,97,98,99,100,101,102,103,105,107,109,111,115,116,117}
def main():
    rows=[]
    for name in ['Tesis Vigente/ACA2.pdf','prom.pdf','nueva ivestigacion .pdf']:
        with tempfile.TemporaryDirectory(prefix='audit_pdf_') as tmp:
            dest=Path(tmp)/'texto.txt'
            subprocess.run(['pdftotext','-layout',str(ROOT/name),str(dest)],check=True)
            pages=dest.read_text().split('\f')
            if not pages[-1].strip():pages.pop()
            for i,t in enumerate(pages,1):
                if name.endswith('ACA2.pdf'):
                    reviewed=i in REVIEWED;visual=i in VISUAL
                else: reviewed=True;visual=name=='prom.pdf' and i==24
                lines=[s.strip() for s in t.splitlines() if s.strip()]
                heading=next((s for s in lines if s!=str(i)),'página gráfica o vacía')
                rows.append({'archivo':name,'pagina_pdf':i,'pagina_impresa':i if name.endswith('ACA2.pdf') else '', 'estado':'texto completo revisado' if reviewed else 'extraída; pendiente de lectura','revision_visual':'revisada' if visual else 'no registrada / no necesaria para cifra citada','titulo_o_inicio':heading[:180],'sha256_texto_extraido':hashlib.sha256(t.encode()).hexdigest()})
    with (OUT/'mapa_paginas.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    print('Páginas indexadas:',len(rows),'ACA2 revisadas:',len(REVIEWED))
if __name__=='__main__':main()
