"""Generar/validar desde fuentes Python; ejecutar solo el cuaderno de resultados."""
from pathlib import Path
import re,json,sys
import nbformat
from nbclient import NotebookClient
HERE=Path(__file__).resolve().parents[1]
def generate(name):
    text=(HERE/'fuentes'/f'{name}.py').read_text();parts=re.split(r'^# %%([^\n]*)\n',text,flags=re.M)
    cells=[]
    for kind,body in zip(parts[1::2],parts[2::2]):
        if 'markdown' in kind:
            lines=[line[2:] if line.startswith('# ') else line[1:] if line.startswith('#') else line for line in body.strip().splitlines()]
            cells.append(nbformat.v4.new_markdown_cell('\n'.join(lines)))
        else:cells.append(nbformat.v4.new_code_cell(body.strip()))
    nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'}})
    nbformat.validate(nb);path=HERE/f'{name}.ipynb';nbformat.write(nb,path);nbformat.validate(nbformat.read(path,as_version=4))
    return path,nb
if __name__=='__main__':
    generate('01_diseno_y_reproduccion')
    path,nb=generate('02_resultados_y_graficas')
    client=NotebookClient(nb,timeout=120,resources={'metadata':{'path':str(HERE)}})
    client.execute();nbformat.validate(nb);nbformat.write(nb,path)
    assert all(c.execution_count is not None for c in nb.cells if c.cell_type=='code')
    assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
    (HERE/'EJECUCION_NOTEBOOKS.json').write_text(json.dumps({'generador':'fuentes/generar_notebooks.py','nbformat_validado':True,'01_diseno':'generado sin ejecución; rutas manuales desactivadas','02_resultados':'ejecutado realmente con kernel','ejecutable_generador':sys.executable,'fits_nuevos':0},indent=2,ensure_ascii=False)+'\n')
    print('Dos notebooks validados; resultados y figuras ejecutados, entrenamiento no ejecutado.')
