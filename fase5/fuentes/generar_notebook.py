"""Genera, valida y ejecuta el notebook documental mediante Python secuencial."""
from pathlib import Path
import contextlib,io,json,hashlib
import nbformat
ROOT=Path(__file__).resolve().parents[2]
def main():
    import os
    os.chdir(ROOT)
    src=ROOT/'fase5/fuentes/07_informe_tesis.py'
    cells=[]; buf=[]; markdown=False
    def flush():
        if not buf:return
        s='\n'.join(buf).strip()
        if markdown:
            s='\n'.join(line[2:] if line.startswith('# ') else line[1:] if line.startswith('#') else line for line in s.splitlines())
        cell=nbformat.v4.new_markdown_cell(s) if markdown else nbformat.v4.new_code_cell(s)
        cell.id=hashlib.sha256((str(len(cells))+s).encode()).hexdigest()[:12]
        cells.append(cell)
    for line in src.read_text().splitlines():
        if line.startswith('# %%'):
            flush();buf=[];markdown='[markdown]' in line
        else:buf.append(line)
    flush(); nb=nbformat.v4.new_notebook(cells=cells,metadata={'language_info':{'name':'python'},'ejecucion':'Python secuencial compile/exec; no kernel Jupyter'})
    nbformat.validate(nb)
    ns={'__name__':'__main__'}; count=0
    for cell in cells:
        if cell.cell_type!='code':continue
        count+=1; stream=io.StringIO()
        with contextlib.redirect_stdout(stream):exec(compile(cell.source,str(src),'exec'),ns)
        cell.execution_count=count
        cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=stream.getvalue())] if stream.getvalue() else []
    path=ROOT/'fase5/notebooks/07_informe_tesis.ipynb';path.parent.mkdir(exist_ok=True)
    nbformat.write(nb,path);nbformat.validate(nbformat.read(path,as_version=4))
    (ROOT/'fase5/resultados/verificacion_notebook.json').write_text(json.dumps({'fuente':str(src.relative_to(ROOT)),'sha256_fuente':hashlib.sha256(src.read_bytes()).hexdigest(),'notebook':str(path.relative_to(ROOT)),'validado_nbformat':True,'celdas_codigo_ejecutadas':count,'modo':'Python secuencial compile/exec; sin kernel Jupyter','salidas_reales':True},ensure_ascii=False,indent=2)+'\n')
    print('Notebook documental generado, validado y ejecutado:',count,'celdas de código')
if __name__=='__main__':main()
