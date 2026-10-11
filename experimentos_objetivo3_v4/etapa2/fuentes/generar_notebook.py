"""Generador/validador y ejecución real de tres celdas de lectura, sin fit."""
from piloto import *
import nbformat,io,contextlib

def generar():
    assert read(OUT/'verificacion.json')['aprobado']
    source=E2/'fuentes/01_resultados_piloto.py'
    nb=nbformat.v4.new_notebook()
    nb.cells=[nbformat.v4.new_markdown_cell('# Piloto exploratorio v4 — resultados guardados\n\nSolo lectura; protocolo4.0.0, semilla20261010. Orden: comprobar entorno y huellas, controles, congelación, piloto, verificación y este resumen. No notebook personal ni ajuste final. Ejecución desde raíz del repositorio. Dependencias exactas en etapa1/requirements.lock.txt. Entradas/salidas documentadas en README de etapa2.')]
    scope={'__name__':'__notebook__'};executed=[]
    for i,code in enumerate(source.read_text().split('# %%')[1:],1):
        code=code.strip();cell=nbformat.v4.new_code_cell(code);stream=io.StringIO()
        with contextlib.redirect_stdout(stream):exec(compile(code,str(source),'exec'),scope)
        cell.execution_count=i;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=stream.getvalue())]
        nb.cells.append(cell);executed.append(i)
    nb.metadata.kernelspec=dict(name='python3',display_name='Python3.12.14 (lock v4)',language='python')
    nbformat.validate(nb);path=destino(E2/'notebooks/01_resultados_piloto.ipynb');nbformat.write(nb,path)
    nbformat.validate(nbformat.read(path,as_version=4))
    guardar(OUT/'verificacion_notebook.json',dict(aprobado=True,celdas_ejecutadas=executed,metodo='Python exec de celdas reales de lectura; no kernel Jupyter',fuente_sha256=sha(source),notebook_sha256=sha(path),ajustes_adicionales=0,notebook_personal=False))
    print('Notebook de resumen generado, validado y tres celdas ejecutadas sin ajustes.')
if __name__=='__main__':generar()
