"""Genera con nbformat; ejecuta únicamente lectura de artefactos en Python, sin kernel ni fits."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import contextlib,io,json
import nbformat
from piloto import F3,sha,guardar,ROOT

def generate():
 source=F3/'fuentes/01_resultados_piloto.py';cells=[];kind=None;lines=[]
 def add():
  if not lines:return
  text='\n'.join(lines).strip()
  if kind=='markdown':text='\n'.join(s[2:] if s.startswith('# ') else s[1:] if s.startswith('#') else s for s in text.splitlines());cells.append(nbformat.v4.new_markdown_cell(text))
  else:cells.append(nbformat.v4.new_code_cell(text))
 for line in source.read_text().splitlines():
  if line.startswith('# %%'):add();lines=[];kind='markdown' if '[markdown]' in line else 'code'
  else:lines.append(line)
 add();notebook=nbformat.v4.new_notebook(cells=cells,metadata=dict(kernelspec=dict(name='python3',display_name='Python 3',language='python'),language_info=dict(name='python',version='3.12.14'),execution_mode='Python exec: lectura real de artefactos, sin kernel Jupyter, sin entrenamiento'))
 namespace={'__name__':'__notebook__'};count=0
 for cell in notebook.cells:
  if cell.cell_type=='code':
   count+=1;stream=io.StringIO()
   with contextlib.redirect_stdout(stream):exec(compile(cell.source,str(source),'exec'),namespace)
   cell.execution_count=count;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=stream.getvalue())]
 nbformat.validate(notebook);path=F3/'notebooks/01_resultados_piloto.ipynb';nbformat.write(notebook,path);nbformat.validate(nbformat.read(path,as_version=4))
 guardar(F3/'resultados/verificacion_notebook.json',dict(aprobado=True,nbformat=True,ejecucion_real='Python exec de lectura; sin kernel; no entrenamiento',celdas_codigo_ejecutadas=count,fuente_sha256=sha(source),notebook_sha256=sha(path),resultados_sha256=sha(F3/'resultados/verificacion_resultados.json'),ajustes_adicionales=0));print('Notebook generado, ejecutado y validado; sin ajustes adicionales.')
if __name__=='__main__':generate()
