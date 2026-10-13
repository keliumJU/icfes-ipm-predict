"""AsyncKernelManager compatible con nbclient; ejecución real y ledger documental.

Orden CLI: --inventado, --preview, después revisión visual y ejecución final.
"""
import os, sys
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['GIT_OPTIONAL_LOCKS']='0'
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[key]='1'
os.environ['IPYTHONDIR']='/tmp/icfes-pobreza-doc-ipython'
os.environ['JUPYTER_RUNTIME_DIR']='/tmp/icfes-pobreza-doc-jupyter'
os.environ['MPLCONFIGDIR']='/tmp/icfes-pobreza-doc-matplotlib'
from infra_correccion import *
import asyncio, inspect, traceback, nbformat
from nbclient import NotebookClient
from jupyter_client import AsyncKernelManager
from jupyter_client.kernelspec import KernelSpec
from notebook_corregido import CELLS,SYNTHETIC
LEDGER=HERE/'LEDGER_DOCUMENTAL.json'
def run(mode='final'):
    deadline();check(load(HERE/'PREFLIGHT.json')['aprobado'],'preflight documental')
    if mode!='inventado':check(load(HERE/'PRUEBA_NOTEBOOK_INVENTADO.json')['aprobado'],'inventado primero');check(load(HERE/'CONGELACION_DOCUMENTAL.json')['aprobado'],'infraestructura documental congelada')
    if mode=='final':check(load(MAIN/'resultados/REVISION_VISUAL.json')['aprobado'],'visual antes del texto')
    l=load(LEDGER) if LEDGER.exists() else dict(start_epoch=START,new_fits=0,attempts=[],status='abierto')
    check(l['status']=='abierto' and not any(a['status']=='running' for a in l['attempts']),'documental no pendiente')
    count=len(l['attempts']);attempt=dict(mode=mode,start_epoch=time.time(),end_epoch=None,status='running',cells=[]);l['attempts'].append(attempt);save(LEDGER,l)
    cells=SYNTHETIC if mode=='inventado' else (CELLS[:3] if mode=='preview' else CELLS)
    name='NOTEBOOK_INVENTADO.ipynb' if mode=='inventado' else ('PREVIEW.ipynb' if mode=='preview' else 'RESULTADOS.ipynb')
    target=HERE/name if mode=='inventado' else MAIN/name
    nb=nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell('# '+('Prueba inventada del arranque' if mode=='inventado' else 'Resultados: pobreza e historia del puntaje')+'\n\nCorrección documental autorizada, cero nuevosfits. Python3.12.14/sklearn1.9.1, semilla20261010, un hilo. Fuentes científicas originales congeladas; se corrige exclusivamente arranque asíncrono y reloj separado. Orden: inventado → preview → revisión visual → final. Entradas reales: matrices, parámetros, selecciones y predicciones del piloto cerrado; salidas: tablas, figuras, texto y evidencias. Los escenarios no se ejecutan.'),*[nbformat.v4.new_code_cell(c) for c in cells]],metadata={'kernelspec':{'display_name':'Python exacto local','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12.14'}})
    km=AsyncKernelManager(kernel_name='python3',connection_file=str(HERE/f'connection_{count}.json'))
    km._kernel_spec=KernelSpec(argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],display_name='Python exacto local',language='python')
    def before(cell,cell_index,**kw):
        deadline();attempt['cells'].append(dict(index=cell_index,status='running',start_epoch=time.time()));save(LEDGER,l)
    def after(cell,cell_index,**kw):
        if cell.cell_type=='code':
            rec=attempt['cells'][-1];rec.update(status='complete',end_epoch=time.time(),execution_count=cell.execution_count);save(LEDGER,l)
    client=NotebookClient(nb,km=km,timeout=min(600,max(1,int(7200-elapsed()))),startup_timeout=45,resources={'metadata':{'path':str(MAIN)}},on_cell_execute=before,on_cell_executed=after)
    try:
        client.execute(cleanup_kc=True)
        nbformat.validate(nb)
        code=[c for c in nb.cells if c.cell_type=='code']
        for i,c in enumerate(code,1):check(c.execution_count==i and c.outputs and not any(o.output_type=='error' for o in c.outputs),'celdas realmente ejecutadas')
        save(target,nbformat.writes(nb))
        e=dict(aprobado=True,notebook_file=target.relative_to(MAIN).as_posix(),notebook_sha256=sha(target),source_file='correccion_documental/notebook_corregido.py',source_sha256=sha(HERE/'notebook_corregido.py'),original_cells_sha256=sha(MAIN/'notebook_resultados.py'),shared_functions_sha256=sha(MAIN/'analisis.py'),generator_file='correccion_documental/generar_notebook_corregido.py',generator_sha256=sha(HERE/'generar_notebook_corregido.py'),clock_file='correccion_documental/infra_correccion.py',clock_sha256=sha(HERE/'infra_correccion.py'),cells=len(code),executed=True,new_fits=0,python=sys.executable,manager='AsyncKernelManager',mode=mode)
        save(target.with_name(target.name+'.ejecucion.json'),e)
        if mode=='inventado':save(HERE/'PRUEBA_NOTEBOOK_INVENTADO.json',e)
        attempt.update(status='complete',end_epoch=time.time(),notebook_sha256=sha(target),kernel_terminated=True);save(LEDGER,l)
        print(json.dumps(e,ensure_ascii=False))
    except BaseException as ex:
        attempt.update(status='failed',end_epoch=time.time(),exception=type(ex).__name__,message=str(ex));save(LEDGER,l);save(HERE/f'ERROR_NOTEBOOK_{count}.txt',traceback.format_exc());raise
    finally:
        async def cleanup():
            if km.has_kernel:await km.shutdown_kernel(now=True)
            r=km.cleanup_resources()
            if inspect.isawaitable(r):await r
        asyncio.run(cleanup())
if __name__=='__main__':run('inventado' if '--inventado' in sys.argv else ('preview' if '--preview' in sys.argv else 'final'))
