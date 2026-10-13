"""Generación nbformat + ejecución Python real de celdas editables en orden."""
from pathlib import Path
import contextlib
import io
import json
import sys
import nbformat
from preflight import environment
from integridad import digest

HERE=Path(__file__).resolve().parent

def main():
    environment()
    source=HERE/'notebook_controles.py'
    blocks=[b.strip() for b in source.read_text().split('# %%') if b.strip()]
    cells=[nbformat.v4.new_markdown_cell('# Controles fase2\n\nSolo datos y ajustes inventados. No resultados del panel, modelo final ni simulación. Ejecución secuencial Python; no kernel Jupyter.')]
    namespace={'__name__':'notebook_controles','__file__':str(source)}
    for n,block in enumerate(blocks,1):
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured),contextlib.redirect_stderr(captured):
            exec(compile(block,str(source),'exec'),namespace)
        cell=nbformat.v4.new_code_cell(block,execution_count=n,
            outputs=[nbformat.v4.new_output('stream',name='stdout',text=captured.getvalue())])
        cells.append(cell)
    notebook=nbformat.v4.new_notebook(cells=cells,metadata={
        'language_info':{'name':'python','version':'3.12.14'},
        'ejecucion':{'metodo':'exec Python secuencial; stdout real','fuente_sha256':digest(source),
                     'fits_reales':0,'semilla':20261010}})
    nbformat.validate(notebook)
    target=HERE/'01_controles.ipynb'
    if target.exists(): raise RuntimeError('Notebook existente: preservar antes de regenerar')
    nbformat.write(notebook,target)
    reread=nbformat.read(target,as_version=4); nbformat.validate(reread)
    assert [c.execution_count for c in reread.cells if c.cell_type=='code']==list(range(1,len(blocks)+1))
    proof={'aprobado':True,'nbformat_validado':True,'celdas_ejecutadas':len(blocks),'metodo':'exec Python secuencial, salidas capturadas reales',
           'fuente':source.name,'fuente_sha256':digest(source),'generador_sha256':digest(Path(__file__)),
           'notebook_sha256':digest(target),'controles':str(namespace['report_path'].relative_to(HERE)),
           'fits_inventados':namespace['report']['fits_inventados'],'fits_panel_real':0}
    (HERE/'ACEPTACION_NOTEBOOK.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(proof,ensure_ascii=False))

if __name__=='__main__': main()
