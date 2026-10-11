"""Generar, validar nbformat y ejecutar únicamente celdas de controles inventados."""
from comun_v5 import *
import nbformat,io,contextlib,os

def generar():
    source=E1/'fuentes/01_controles.py';target=destino(E1/'notebooks/01_controles.ipynb')
    parts=[p.strip() for p in source.read_text().split('# %%') if p.strip()]
    nb=nbformat.v4.new_notebook()
    nb.metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3.12.14'),icfes=dict(version='5.0.0',semilla=SEMILLA,origen='datos inventados/dobles',ajustes_panel=0))
    nb.cells=[nbformat.v4.new_markdown_cell('# Controles de etapa1 v5\n\nOrden: contrato/grilla y ventanas; historial inventado; suite sintética y procesos hijos. Entradas: fuentes editables propias y grupos v4 en lectura. Salidas: directorio único bajo etapa1/resultados/sinteticos/notebook. Python3.12.14, lock de54 paquetes y sklearn1.9.1, semilla20261010. Ejecutar desde raíz tras comprobar entorno exacto, con PYTHONDONTWRITEBYTECODE=1. Sin fits del panel real, presupuesto real ni meta. No es orquestación de etapa2; esta se implementará, probará y congelará con nueva autorización. Predicciones no son efectos causales. Casos completos, enlace ecológico y pocos años limitan la interpretación. Reejecutar crea evidencia sintética separada y exige cierre explícito nuevo; abrir es lectura.')]
    namespace={'__name__':'notebook_controles_v5'};executed=[]
    os.chdir(ROOT)
    for i,code in enumerate(parts,1):
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf):exec(compile(code,str(source),'exec'),namespace)
        cell=nbformat.v4.new_code_cell(code,execution_count=i)
        if buf.getvalue():cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue())]
        nb.cells.append(cell);executed.append(i)
    nbformat.validate(nb);nbformat.write(nb,target);nbformat.validate(nbformat.read(target,as_version=4))
    guardar(OUT/'verificacion_notebook.json',dict(aprobado=True,celdas_ejecutadas=executed,metodo='Python exec en orden; no kernel Jupyter',fuente_sha256=sha(source),notebook_sha256=sha(target),fuentes_sha256=namespace['resultado']['fuentes_sha256'],resultado_sintetico=namespace['resultado'],ajustes_panel=0,salidas_realmente_ejecutadas=True))
    print('Notebook generado, validado y sus tres celdas ejecutadas con inventados.')
if __name__=='__main__':generar()
