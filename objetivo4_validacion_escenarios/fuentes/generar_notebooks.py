"""Generador y ejecutor Python secuencial real; no kernel ni salidas simuladas."""
from pathlib import Path
import sys,io,contextlib,traceback,json,os
import nbformat
HERE=Path(__file__).resolve().parents[1]
def generate(source):
    cells=[];kind='code';lines=[]
    def flush():
        if lines:
            content='\n'.join(lines).strip()
            if content:cells.append(nbformat.v4.new_markdown_cell(content) if kind=='markdown' else nbformat.v4.new_code_cell(content))
    for line in source.read_text().splitlines():
        if line.startswith('# %%'):
            flush();lines=[];kind='markdown' if '[markdown]' in line else 'code'
        else:lines.append(line[2:] if kind=='markdown' and line.startswith('# ') else line)
    flush();nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python','version':sys.version.split()[0]}});nbformat.validate(nb);return nb

def main(execute=False):
    os.chdir(HERE)
    for source,name in [('notebook_preparacion.py','01_preparacion.ipynb'),('notebook_validacion.py','02_validacion_escenarios.ipynb')]:
        nb=generate(HERE/'fuentes'/source);dest=HERE/name;nbformat.write(nb,dest)
        if execute:
            namespace={'__name__':'__main__'};count=0
            for cell in nb.cells:
                if cell.cell_type!='code':continue
                count+=1;buf=io.StringIO();cell.execution_count=count
                try:
                    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):exec(compile(cell.source,f'{name}:celda{count}','exec'),namespace)
                except BaseException as e:
                    cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue()),nbformat.v4.new_output('error',ename=type(e).__name__,evalue=str(e),traceback=traceback.format_exc().splitlines())];nbformat.write(nb,dest);raise
                cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue())];nbformat.write(nb,dest)
                print(name,'celda',count,'ejecutada',flush=True)
            nb.metadata['ejecucion_real']={'modo':'Python secuencial con exec y captura real stdout/stderr; no kernel','python':sys.version,'celdas':count}
        nbformat.validate(nb);nbformat.write(nb,dest)
        print(dest,flush=True)
if __name__=='__main__':main('--ejecutar' in sys.argv)
