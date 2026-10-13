"""Generador nbformat + ejecución real nbclient en entorno exacto, sin fits.

Orden: preview (celdas1-3), revisión visual, final (cinco celdas).
"""
from infra import *
import sys, nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec
from notebook_resultados import CELLS
def run(preview=False):
    deadline();check(load(HERE/'AUDITORIA.json')['aprobado'],'audit')
    cells=CELLS[:3] if preview else CELLS
    nb=nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell('# Resultados: pobreza e historia del puntaje\n\nEntradas: predicciones/params/ledger cerrados y auditoría. Salidas: tablas, JSON, figuras y texto. Python3.12.14/sklearn1.9.1, semilla20261010, un hilo. No nuevos fits; pobreza contemporánea, exploratorio y sin interpretación causal. Ejecutar primero preview, revisar figuras y después final. Fuentes editables: notebook_resultados.py y analisis.py. Los modelos se ajustaron exclusivamente en el piloto ya cerrado.'),*[nbformat.v4.new_code_cell(c) for c in cells]],metadata={'kernelspec':{'display_name':'Python exacto local','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12.14'}})
    # Se suministra el comando explícito; no instala kernelspec ni toca runtime compartido.
    km=KernelManager(kernel_name='python3',connection_file=str(HERE/'resultados/kernel_connection.json'))
    km._kernel_spec=KernelSpec(argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],display_name='Python exacto local',language='python')
    client=NotebookClient(nb,km=km,timeout=min(600,max(1,int(7200-elapsed()))),resources={'metadata':{'path':str(HERE)}})
    (HERE/'resultados').mkdir(parents=True,exist_ok=True)
    try:client.execute()
    finally:
        if km.has_kernel:km.shutdown_kernel(now=True)
        km.cleanup_resources()
    nbformat.validate(nb)
    for i,c in enumerate([c for c in nb.cells if c.cell_type=='code'],1):check(c.execution_count==i and c.outputs and not any(o.output_type=='error' for o in c.outputs),'real outputs')
    name='PREVIEW.ipynb' if preview else 'RESULTADOS.ipynb';save(HERE/name,nbformat.writes(nb))
    e=dict(aprobado=True,notebook_sha256=sha(HERE/name),source_sha256=sha(HERE/'notebook_resultados.py'),shared_functions_sha256=sha(HERE/'analisis.py'),generator_sha256=sha(HERE/'generar_notebook.py'),cells=len(cells),executed=True,new_fits=0,python=sys.executable)
    save(HERE/(name+'.ejecucion.json'),e);print(json.dumps(e))
if __name__=='__main__':run('--preview' in sys.argv)
