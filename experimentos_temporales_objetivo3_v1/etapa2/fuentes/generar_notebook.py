"""Fuente editable→nbformat; ejecución real sin kernel ni fits, resultados guardados."""
import sys,io,contextlib,json,base64
from pathlib import Path
import nbformat
from seguridad import ROOT,E1,OUT,guardar,sha

def main():
    source=E1/'fuentes/01_resultados.py';cells=source.read_text().split('# %%')[1:]
    nb=nbformat.v4.new_notebook();nb.cells=[nbformat.v4.new_markdown_cell('''# Piloto exploratorio recencia_h2: resultados auditados

Orden: preflight→piloto→auditar→resultados→generar_notebook. Este notebook solo lee
resultados completos; no ajusta modelos. Entorno Python3.12.14/sklearn1.9.1, lock54,
semilla20261010 del piloto. Todos2021–2025 vistos; sin confirmación independiente ni
causalidad. Entradas: resultados/meta.json, auditoría, tablas y gráficos propios.
Fuente editable: fuentes/01_resultados.py. Celdas realmente ejecutadas mediante exec.
''')];namespace={}
    for count,text in enumerate(cells,1):
        text=text.strip();buffer=io.StringIO();images=[]
        def display(value):
            data=getattr(value,'data',None)
            if isinstance(data,bytes):images.append(nbformat.v4.new_output('display_data',data={'image/png':base64.b64encode(data).decode()},metadata={}))
        if 'from IPython.display import display,Image' in text:
            executable=text.replace('from IPython.display import display,Image','from IPython.display import Image')
            namespace['display']=display
        else:executable=text
        with contextlib.redirect_stdout(buffer):exec(compile(executable,str(source),'exec'),namespace)
        cell=nbformat.v4.new_code_cell(text,execution_count=count,outputs=([nbformat.v4.new_output('stream',name='stdout',text=buffer.getvalue())] if buffer.getvalue() else [])+images);nb.cells.append(cell)
    nb.metadata=dict(kernelspec=dict(display_name='Python 3.12.14 (entorno contratado)',language='python',name='python3'),language_info=dict(name='python',version='3.12.14'))
    path=E1/'notebooks/01_resultados_recencia.ipynb';nbformat.validate(nb)
    with path.open('x') as f:nbformat.write(nb,f)
    nbformat.validate(nbformat.read(path,as_version=4))
    guardar(OUT/'notebook.json',dict(aprobado=True,celdas_codigo_ejecutadas=len(cells),ejecucion='exec real con outputs capturados; sin kernel',fuente_sha256=sha(source),notebook_sha256=sha(path),fits=0,solo_resultados=True))
    print('Notebook ejecutado y validado:',len(cells),'celdas')
if __name__=='__main__':main()
