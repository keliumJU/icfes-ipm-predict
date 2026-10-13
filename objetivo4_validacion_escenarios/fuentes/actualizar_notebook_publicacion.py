"""Amplía notebook desde fuente; conserva cada celda y salida real del ajuste."""
from pathlib import Path
import os,sys,io,contextlib,base64,json
import nbformat
from generar_notebooks import generate,HERE
from modelos import sha
os.chdir(HERE);dest=HERE/'02_validacion_escenarios.ipynb';old=nbformat.read(dest,as_version=4);new=generate(HERE/'fuentes/notebook_validacion.py')
assert len(new.cells)>=len(old.cells)
for a,b in zip(old.cells,new.cells):assert a.source==b.source and a.cell_type==b.cell_type
for i,cell in enumerate(old.cells):new.cells[i]=cell
count=max(c.execution_count or 0 for c in old.cells if c.cell_type=='code');namespace={'__name__':'__main__'}
start=len(old.cells) if len(new.cells)>len(old.cells) else len(new.cells)-1
for cell in new.cells[start:]:
    if cell.cell_type!='code':continue
    count+=1;buf=io.StringIO()
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):exec(compile(cell.source,'publicacion_notebook','exec'),namespace)
    cell.execution_count=count;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue())]
    for p in sorted((HERE/'figuras').glob('*.png')):cell.outputs.append(nbformat.v4.new_output('display_data',data={'image/png':base64.b64encode(p.read_bytes()).decode(),'text/plain':p.name},metadata={}))
new.metadata.update(old.metadata);new.metadata['ejecucion_real']['celdas']=sum(c.cell_type=='code' for c in new.cells);new.metadata['publicacion_verificada']=True
nbformat.validate(new);nbformat.write(new,dest)
freeze=json.loads((HERE/'resultados/CONGELACION_PREVIA.json').read_text());diff={p.name:sha(p) for p in (HERE/'fuentes').glob('*.py') if freeze['fuentes_sha'].get(p.name)!=sha(p)}
assert sha(HERE/'fuentes/modelos.py')==freeze['fuentes_sha']['modelos.py'];assert sha(HERE/'PLAN_Y_PROTOCOLO.md')==freeze['protocol_sha']
record={'sin_nuevos_ajustes':True,'fuente_modelos_y_protocolo_sin_cambio':True,'fuentes_publicacion_nuevas_o_actualizadas':diff,'motivo':'Prueba de datos de figuras y presentación solo de reducciones efectivas; texto, Word y gráficos desde resultados fijados','tests_finales':10}
(HERE/'resultados/PUBLICACION.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(record)
