"""Genera desde fuentes # %%, valida y ejecuta en kernel del entorno aislado."""
import sys,os,re,hashlib,json
sys.dont_write_bytecode=True
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'fase4/resultados'
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['MPLCONFIGDIR']='/tmp/icfes-fase4-mpl'
os.environ['IPYTHONDIR']='/tmp/icfes-fase4-ipython'
os.environ['JUPYTER_RUNTIME_DIR']='/tmp/icfes-fase4-jupyter'
results=[]
for stage in ('05_contraste_territorial','06_robustez_explicaciones'):
    source=ROOT/'fase4/fuentes'/f'{stage}.py'
    chunks=re.split(r'^# %%([^\n]*)\n',source.read_text(),flags=re.M)
    cells=[]
    for flag,body in zip(chunks[1::2],chunks[2::2]):
        cell=nbformat.v4.new_markdown_cell(body.strip()) if '[markdown]' in flag else nbformat.v4.new_code_cell(body.strip())
        cell.id=hashlib.sha256((stage+str(len(cells))).encode()).hexdigest()[:12]
        if cell.cell_type=='code':compile(cell.source,str(source),'exec')
        cells.append(cell)
    nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python (entorno fase 4)','language':'python','name':'python3'}})
    nbformat.validate(nb)
    # Kernel explícito del venv; no se instala ni sustituye kernel global.
    km=KernelManager(kernel_name='python3')
    km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
    client=NotebookClient(nb,km=km,timeout=600,resources={'metadata':{'path':str(ROOT)}},allow_errors=False)
    if '--reusar-salidas' in sys.argv:
        previous=nbformat.read(ROOT/'notebooks'/f'{stage}.ipynb',as_version=4)
        old=[c for c in previous.cells if c.cell_type=='code']
        new=[c for c in nb.cells if c.cell_type=='code']
        assert len(old)==len(new)
        for a,b in zip(old,new):
            assert a.source==b.source, 'Cambió código: requiere nueva ejecución explícita'
            b.outputs=a.outputs; b.execution_count=a.execution_count
        nb.metadata=previous.metadata
    else:
        client.execute()
    nbformat.validate(nb)
    target=ROOT/'notebooks'/f'{stage}.ipynb'
    nbformat.write(nb,target);nbformat.validate(nbformat.read(target,as_version=4))
    results.append({'notebook':str(target.relative_to(ROOT)),'fuente_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'notebook_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'celdas_codigo_ejecutadas':sum(c.cell_type=='code' and c.execution_count is not None for c in nb.cells),'kernel_python':sys.executable,'validacion_nbformat':True,'salidas_preservadas_codigo_identico':'--reusar-salidas' in sys.argv})
    print(stage,'ejecutado y validado',flush=True)
(OUT/'verificacion_notebooks.json').write_text(json.dumps(results,indent=2)+'\n')
