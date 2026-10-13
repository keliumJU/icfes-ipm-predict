"""Genera/ejecuta lector desde Python; nbformat validado, sin fits."""
from comun import *
import nbformat, io, contextlib
from notebook_resultados import CELLS

def main():
    path=HERE/'01_resultados_piloto.ipynb'
    if path.exists(): raise IntegrityError('Notebook existente')
    assert load(HERE/'resultados/VALIDACION_PILOTO.json')['aprobado']
    nb=nbformat.v4.new_notebook(metadata={'language_info':{'name':'python','version':'3.12.14'},
        'ejecucion':'exec secuencial fuente Python; solo guardados; semilla20261010; cero nuevosfits'})
    nb.cells=[nbformat.v4.new_markdown_cell('# Fase3 — piloto exploratorio\n\nEntradas: VALIDACION_PILOTO.json y meta.json. Ejecutar después de piloto.py, con entorno exacto. Salidas: registros guardados; no reentrena. Criterios y advertencias: PROTOCOLO_ETAPA2.md. Sin datos personales. Auditoría interpretativa fase4 pendiente.')]
    scope={'__file__':str(HERE/'notebook_resultados.py')}
    for i,source in enumerate(CELLS,1):
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf): exec(compile(source,str(HERE/'notebook_resultados.py'),'exec'),scope)
        cell=nbformat.v4.new_code_cell(source,execution_count=i,outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue())])
        nb.cells.append(cell)
    nbformat.validate(nb); nbformat.write(nb,path); nbformat.validate(nbformat.read(path,as_version=4))
    fresh('ACEPTACION_NOTEBOOK.json',{'aprobado':True,'celdas_realmente_ejecutadas':2,'fits':0,'fuente_sha256':digest(HERE/'notebook_resultados.py'),
          'generador_sha256':digest(HERE/'generar_notebook.py'),'notebook_sha256':digest(path),'sin_datos_personales':True})
    print(json.dumps({'notebook_valido':True,'celdas_ejecutadas':2,'fits':0}))
if __name__=='__main__': main()
