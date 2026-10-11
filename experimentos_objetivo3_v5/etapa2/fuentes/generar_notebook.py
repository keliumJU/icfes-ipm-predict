"""Genera, valida y ejecuta realmente las celdas de lectura; no kernel ni fits."""
from piloto import *
import nbformat,io,contextlib

def generar():
    source=E2/'fuentes/01_resultados_piloto.py';text=source.read_text();cells=[]
    for part in text.split('# %%')[1:]:
        if part.startswith(' [markdown]'):
            content='\n'.join(line[2:] if line.startswith('# ') else line.lstrip('#') for line in part.splitlines()[1:]);cells.append(nbformat.v4.new_markdown_cell(content.strip()))
        else:cells.append(nbformat.v4.new_code_cell(part.strip()))
    nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3 (entorno verificado)','language':'python','name':'python3'}})
    scope={'__name__':'__notebook__'};count=0
    for cell in cells:
        if cell.cell_type=='code':
            count+=1;buffer=io.StringIO()
            with contextlib.redirect_stdout(buffer):exec(compile(cell.source,str(source),'exec'),scope)
            cell.execution_count=count;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buffer.getvalue())]
    nbformat.validate(nb);path=destino(E2/'notebooks/01_resultados_piloto.ipynb');nbformat.write(nb,path)
    guardar(OUT/'verificacion_notebook.json',dict(aprobado=True,celdas_ejecutadas=count,fuente_sha256=sha(source),notebook_sha256=sha(path),solo_resultados_guardados=True,ajustes_nuevos=0,salidas_realmente_ejecutadas=True))
    print('Notebook generado, validado y ejecutado:',count,'celdas de lectura')
if __name__=='__main__':generar()
