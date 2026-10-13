"""Generar/ejecutar celdas Python con exec y validar nbformat; sin kernel ni panel real."""
import contextlib
import io
import json
import sys
import nbformat
from seguridad import E1,OUT,destino,texto_nuevo,guardar,sha


def main():
    source = E1/'fuentes/01_controles.py'
    parts = []
    current,markdown = [],False
    for line in source.read_text().splitlines():
        if line.startswith('# %%'):
            if current:
                parts.append((markdown,'\n'.join(current)+'\n'))
            current=[]
            markdown='[markdown]' in line
        else:
            current.append(line)
    if current:
        parts.append((markdown,'\n'.join(current)+'\n'))
    cells,namespace,count = [],{'__name__':'controles_notebook'},0
    for md,body in parts:
        if md:
            cells.append(nbformat.v4.new_markdown_cell('\n'.join(line.removeprefix('# ').removeprefix('#') for line in body.splitlines())))
        else:
            count += 1
            cell = nbformat.v4.new_code_cell(body,execution_count=count)
            output = io.StringIO()
            with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
                exec(compile(body,str(source)+f':celda{count}','exec'),namespace)
            cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=output.getvalue())]
            cells.append(cell)
    nb = nbformat.v4.new_notebook(cells=cells,metadata=dict(
        kernelspec=dict(name='python3',display_name='Python 3.12.14 (entorno exacto)',language='python'),
        language_info=dict(name='python',version='3.12.14'),
        ejecucion=dict(metodo='exec Python por celda; sin kernel',origen='inventado',fits_panel_real=0)))
    nbformat.validate(nb)
    path = destino(E1/'notebooks/01_controles_recencia.ipynb')
    texto_nuevo(path,nbformat.writes(nb))
    loaded = nbformat.read(path,as_version=4)
    nbformat.validate(loaded)
    assert [c.execution_count for c in loaded.cells if c.cell_type=='code'] == list(range(1,count+1))
    assert all(c.outputs and all(o.output_type != 'error' for o in c.outputs) for c in loaded.cells if c.cell_type=='code')
    guardar(OUT/'notebook.json',dict(aprobado=True,celdas_codigo_ejecutadas=count,
        metodo='exec Python por celda, stdout capturado, sin kernel',fuente_sha256=sha(source),
        notebook_sha256=sha(path),ajustes_inventados=1,fits_panel_real=0,nbformat=nbformat.__version__,
        metadata_ajuste_inventado=namespace['meta_nb']))
    print('Notebook validado:',count,'celdas ejecutadas, solo inventados')


if __name__ == '__main__':
    main()
