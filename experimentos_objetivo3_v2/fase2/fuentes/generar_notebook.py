"""Generar desde celdas fuente con nbformat; ejecutar solo modo de verificación."""
import sys,os,re,hashlib
sys.dont_write_bytecode=True
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
import configuracion as cfg
from comun import sha,guardar
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
os.environ['IPYTHONDIR']='/tmp/icfes-v2-fase2-ipython'
os.environ['JUPYTER_RUNTIME_DIR']='/tmp/icfes-v2-fase2-jupyter'

def generar(execute=True):
 source=cfg.F2/'fuentes/01_protocolo_verificacion.py'
 chunks=re.split(r'^# %%([^\n]*)\n',source.read_text(),flags=re.M)
 cells=[]
 for flag,body in zip(chunks[1::2],chunks[2::2]):
  cell=nbformat.v4.new_markdown_cell(body.strip()) if '[markdown]' in flag else nbformat.v4.new_code_cell(body.strip())
  cell.id=hashlib.sha256(('v2_verificacion_'+str(len(cells))).encode()).hexdigest()[:12]
  if cell.cell_type=='code':compile(cell.source,str(source),'exec')
  cells.append(cell)
 nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python — verificación fase 2 v2','name':'python3','language':'python'}})
 nbformat.validate(nb)
 dest=cfg.F2/'notebooks/01_protocolo_verificacion.ipynb';nbformat.write(nb,dest)
 if execute:
  # Fallar de inmediato si el aislamiento no permite sockets locales Jupyter.
  import socket
  probe=socket.socket();probe.close()
  km=KernelManager(kernel_name='python3');km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
  NotebookClient(nb,km=km,timeout=60,allow_errors=False,resources={'metadata':{'path':str(dest.parent)}}).execute()
  nbformat.validate(nb);nbformat.write(nb,dest);nbformat.validate(nbformat.read(dest,as_version=4))
  codes=[c for c in nb.cells if c.cell_type=='code'];assert all(c.execution_count is not None for c in codes)
  guardar(cfg.F2/'resultados/verificacion_notebook.json',dict(aprobado=True,nbformat=True,ejecucion_real_kernel=True,
   kernel_python=sys.executable,modo='verificacion',celdas_codigo_ejecutadas=len(codes),fuente_sha256=sha(source),notebook_sha256=sha(dest),
   controles_notebook_sha256=sha(cfg.F2/'resultados/controles_notebook.json'),ajustes_panel=0,predicciones_panel=0))
 print('Notebook válido'+(' y ejecutado en kernel real.' if execute else '; ejecución pendiente.'))
if __name__=='__main__':generar('--solo-generar' not in sys.argv)
