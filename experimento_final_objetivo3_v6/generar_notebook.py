"""Fuente por celdas; ejecución secuencial explícita real, captura stdout y nbformat."""
from comun import *
import nbformat,io,contextlib,time
def generate(source,target):
    source=safe(source);target=safe(target);check(not target.exists(),'notebook existente; preservar')
    chunks=source.read_text().split('# %%');cells=[];ns={'__name__':'__notebook__'};count=0;start=time.monotonic()
    for chunk in chunks:
        if not chunk.strip():continue
        if chunk.startswith(' markdown'):
            text='\n'.join(s[2:] if s.startswith('# ') else s for s in chunk.splitlines()[1:]);cells.append(nbformat.v4.new_markdown_cell(text));continue
        code=chunk.strip();count+=1;output=io.StringIO()
        with contextlib.redirect_stdout(output):exec(compile(code,str(source),'exec'),ns)
        cell=nbformat.v4.new_code_cell(code,execution_count=count,outputs=[nbformat.v4.new_output('stream',name='stdout',text=output.getvalue())]);cells.append(cell)
    nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python v6 exacto','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12.14'},'execution':{'method':'exec secuencial explícito; captura real stdout','source_sha256':sha(source),'semilla':SEED}})
    nbformat.validate(nb);target.parent.mkdir(parents=True,exist_ok=True);nbformat.write(nb,target);nbformat.validate(nbformat.read(target,as_version=4))
    result=dict(aprobado=True,cells_executed=count,source_sha256=sha(source),notebook_sha256=sha(target),generator_sha256=sha(__file__),seconds=time.monotonic()-start)
    save(target.with_suffix('.ejecucion.json'),result);print(result)
if __name__=='__main__':generate(HERE/sys.argv[1],HERE/sys.argv[2])
