"""Genera, valida y ejecuta realmente celdas con exec; sin kernel Jupyter."""
from comun_v3 import *
import nbformat, io, contextlib, traceback

def generar():
    source=E1/'fuentes/01_controles.py'
    cells=[]
    for block in source.read_text().split('# %%')[1:]:
        if block.startswith(' [markdown]'):
            text='\n'.join(line.removeprefix('# ').removeprefix('#') for line in block.splitlines()[1:]).strip()
            cells.append(nbformat.v4.new_markdown_cell(text))
        else:cells.append(nbformat.v4.new_code_cell(block.strip()))
    nb=nbformat.v4.new_notebook(cells=cells,metadata=dict(kernelspec=dict(name='python3',display_name='Python 3 (entorno exacto v3)',language='python')))
    namespace={'__name__':'notebook_controles'};executed=0
    for cell in nb.cells:
        if cell.cell_type!='code':continue
        output=io.StringIO()
        with contextlib.redirect_stdout(output):exec(compile(cell.source,str(source),'exec'),namespace)
        executed+=1;cell.execution_count=executed
        if output.getvalue():cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=output.getvalue())]
    nbformat.validate(nb)
    path=destino(E1/'notebooks/01_controles.ipynb');nbformat.write(nb,path)
    nbformat.validate(nbformat.read(path,as_version=4))
    guardar(E1/'resultados/verificacion_notebook.json',dict(aprobado=True,celdas_codigo_ejecutadas=executed,
        modo='Python exec de cada celda, realmente ejecutado; sin kernel Jupyter',
        fuente_sha256=sha(source),generador_sha256=sha(Path(__file__)),notebook_sha256=sha(path),
        ajustes_reales=0,predicciones_reales=0,semilla=SEMILLA))
    print('Notebook generado, validado y ejecutado:',executed,'celdas de código.')
if __name__=='__main__':generar()
