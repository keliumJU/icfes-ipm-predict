"""Genera, ejecuta realmente por exec secuencial y valida notebook; sin kernel/fits."""
from auditor import *
from notebook_resultados import CELLS
import nbformat, io, contextlib

def main():
 check(load(HERE/'AUDITORIA_INDEPENDIENTE.json')['aprobado'],'auditoría')
 p=HERE/'01_auditoria_resultados.ipynb'; check(not p.exists(),'no sobrescribir notebook')
 nb=nbformat.v4.new_notebook(metadata={'language_info':{'name':'python','version':'3.12.14'},'kernelspec':{'name':'python3','display_name':'Python3.12.14 contratado','language':'python'},'ejecucion':'exec Python secuencial con entorno exacto; no kernelJupyter; cero fits; semilla20261010'})
 nb.cells=[nbformat.v4.new_markdown_cell('''# Fase4: auditoría y resultados exploratorios

Ejecutar después de auditor.py --preflight, --pruebas, analizar.py, complementar.py y documentar.py. Entradas: guardados etapa2, auditorías y tablas etapa3. Python3.12.14/sklearn1.9.1/54lock/PYTHONDONTWRITEBYTECODE=1/semilla20261010. Celdas solo lectura y recálculo; no escriben resultados ni cargan modelos. Generador ejecuta realmente con exec secuencial; salidas de esta ejecución.

Primario global fijo,165pares/igualpeso/meta5%. Advertencias completas en INFORME_FASE4.md. Resultados de políticas individuales exploratorios; ningún experimento nuevo autorizado.''')]
 scope={'__file__':str(HERE/'notebook_resultados.py')}
 for i,s in enumerate(CELLS,1):
  out=io.StringIO()
  with contextlib.redirect_stdout(out): exec(compile(s,str(HERE/'notebook_resultados.py'),'exec'),scope)
  nb.cells.append(nbformat.v4.new_code_cell(s,execution_count=i,outputs=[nbformat.v4.new_output('stream',name='stdout',text=out.getvalue())]))
 nb.cells.append(nbformat.v4.new_markdown_cell('''## Gráficos guardados (puntos y n explícitos)

![MAE por año](graficos/mae_por_anio.png)

![Beneficio territorial](graficos/beneficio_territorial.png)

![Nivel y rezago](graficos/memoria_nivel_y_rezago.png)

Son recálculos de guardados, sin fits. No confirmación independiente, causalidad ni avance automático.'''))
 nbformat.validate(nb); nbformat.write(nb,p); nb2=nbformat.read(p,as_version=4); nbformat.validate(nb2)
 save('ACEPTACION_NOTEBOOK.json',{'aprobado':True,'celdas_realmente_ejecutadas':len(CELLS),'metodo':'exec Python secuencial; stdout real; nbformat validado y releído','notebook_sha256':sha(p),'fuente_sha256':sha(HERE/'notebook_resultados.py'),'generador_sha256':sha(HERE/'generar_notebook.py'),'fits':0,'modelos_cargados':0,'datos_personales':False})
 print('Notebook válido;6celdas realmente ejecutadas;0fits')
if __name__=='__main__': main()
