"""Generación nbformat y ejecución real Python exec del modo verificar."""
import sys
sys.dont_write_bytecode=True
from revision import *
import nbformat,contextlib,io,base64

def generar():
 assert read(F4/'resultados/verificacion.json')['condicion']['entregar'], 'Condición de entrega no satisfecha'
 source=F4/'fuentes/01_notebook_personal.py';cells=[];kind=None;lines=[]
 def add():
  if not lines:return
  value='\n'.join(lines).strip()
  if kind=='markdown':cells.append(nbformat.v4.new_markdown_cell('\n'.join(s[2:] if s.startswith('# ') else s[1:] if s.startswith('#') else s for s in value.splitlines())))
  else:cells.append(nbformat.v4.new_code_cell(value))
 for line in source.read_text().splitlines():
  if line.startswith('# %%'):add();lines=[];kind='markdown' if '[markdown]' in line else 'code'
  else:lines.append(line)
 add();nb=nbformat.v4.new_notebook(cells=cells,metadata=dict(kernelspec=dict(name='python3',display_name='Python 3.12.14',language='python'),language_info=dict(name='python',version='3.12.14'),execution_mode='Python exec real, modo verificar; sin kernel Jupyter ni reentrenamiento'))
 namespace={'__name__':'__notebook__'};count=0
 for cell in nb.cells:
  if cell.cell_type=='code':
   count+=1;stream=io.StringIO()
   with contextlib.redirect_stdout(stream):exec(compile(cell.source,str(source),'exec'),namespace)
   cell.execution_count=count;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=stream.getvalue())]
   if 'GRAPH_PATHS = ' in cell.source:
    for p in namespace['GRAPH_PATHS']:cell.outputs.append(nbformat.v4.new_output('display_data',data={'image/png':base64.b64encode(p.read_bytes()).decode()},metadata={}))
 assert namespace['MODO']=='verificar';nbformat.validate(nb);path=F4/'notebooks/01_notebook_personal.ipynb';nbformat.write(nb,path);nbformat.validate(nbformat.read(path,as_version=4))
 guardar(F4/'resultados/verificacion_notebook.json',dict(aprobado=True,celdas_codigo_ejecutadas=count,modo='Python exec real de verificar; sin kernel Jupyter',ajustes_nuevos=0,reejecucion_completa_realizada=False,fuente_sha256=sha(source),notebook_sha256=sha(path),graficos_incrustados=3,validacion='nbformat antes y después de guardar'))
 print('Notebook personal generado, ejecutado en verificar y validado.')
if __name__=='__main__':generar()
