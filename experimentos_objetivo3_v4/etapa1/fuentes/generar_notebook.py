"""Genera/valida .ipynb desde fuente editable; ejecuta celdas mediante Python exec."""
from comun_v4 import *
import nbformat,io,contextlib
def generar():
    source=(E1/'fuentes/01_diagnostico_controles.py').read_text()
    blocks=[b.strip() for b in source.split('# %%') if b.strip()]
    nb=nbformat.v4.new_notebook()
    nb.metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3.12.14'))
    nb.cells=[nbformat.v4.new_markdown_cell('## Etapa1 v4: diagnóstico histórico y controles\nEjecutar desde raíz con PYTHONDONTWRITEBYTECODE=1. Entradas: CSV históricos verificados y evidencias etapa1. Salida: notebook_sinteticos dentro v4. Orden: integridad, diagnóstico, controles. Python3.12.14, lock exacto, semilla20261010. Sin fits del panel, sin ledger operativo, sin modelos/personal/simulación. Celdas ejecutadas mediante Python exec, no kernel Jupyter.')]
    scope={'__name__':'notebook_v4'}
    for n,block in enumerate(blocks,1):
        cell=nbformat.v4.new_code_cell(block);buf=io.StringIO()
        with contextlib.redirect_stdout(buf):exec(compile(block,f'celda_{n}','exec'),scope)
        cell.execution_count=n;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue())]
        nb.cells.append(cell)
    nbformat.validate(nb)
    path=destino(E1/'notebooks/01_diagnostico_controles.ipynb');nbformat.write(nb,path)
    nbformat.validate(nbformat.read(path,as_version=4))
    guardar(OUT/'verificacion_notebook.json',dict(aprobado=True,celdas_ejecutadas=len(blocks),modo='Python exec sin kernel',fuente_sha256=sha(E1/'fuentes/01_diagnostico_controles.py'),notebook_sha256=sha(path),ajustes_panel=0))
    print('Notebook generado, validado y tres celdas ejecutadas realmente.')
if __name__=='__main__':generar()
