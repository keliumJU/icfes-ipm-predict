"""Reproducción completa en copia nueva; preserva cierre y repositorio fuente."""
import sys,os,subprocess,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if len(sys.argv)!=2:raise SystemExit('Uso: Python3.12.14 reproducir.py /ruta/inexistente')
if sys.version_info[:3]!=(3,12,14):raise SystemExit('Se requiere Python3.12.14, versión del estudio')
dest=Path(sys.argv[1]).resolve()
venv=dest.parent/(dest.name+'-venv')
if dest.exists() or venv.exists():raise SystemExit('Rutas de copia y entorno deben ser inexistentes')
subprocess.run(['git','clone','--local','--no-hardlinks',str(ROOT),str(dest)],check=True)
archive=dest/'fase3/archivo_cierre';archive.mkdir()
shutil.move(str(dest/'fase3/resultados'),archive/'resultados')
for stage in ('02_preparacion_desarrollo','03_modelos_validacion','04_reevaluacion_temporal'):
    shutil.move(str(dest/'notebooks'/f'{stage}.ipynb'),archive/f'{stage}.ipynb')
subprocess.run([sys.executable,'-m','venv',str(venv)],check=True)
python=str(venv/'bin/python')
subprocess.run([python,'-m','pip','install','pip==25.0.1'],check=True)
subprocess.run([python,'-m','pip','install','-r',str(dest/'fase3/requirements.lock.txt')],check=True)
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
for args in ([python,'-c',"import sys; sys.path.insert(0,'fase3/fuentes'); from comun import prepare; prepare()"],
             [python,'fase3/fuentes/generar_notebooks.py'],[python,'fase3/fuentes/verificar_cierre.py']):
    subprocess.run(args,cwd=dest,env=env,check=True)
import csv,math
for filename in ('comparacion_desarrollo.csv','predicciones_desarrollo.csv','predicciones_reevaluacion.csv'):
    with (archive/'resultados'/filename).open() as a,(dest/'fase3/resultados'/filename).open() as b:
        old=list(csv.DictReader(a));new=list(csv.DictReader(b));assert len(old)==len(new)
        for r,s in zip(old,new):
            for k in r:
                try:assert math.isclose(float(r[k]),float(s[k]),rel_tol=1e-12,abs_tol=1e-12)
                except ValueError:assert r[k]==s[k]
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=dest,text=True).strip()
(dest/'fase3/resultados/reproduccion_copia.json').write_text(json.dumps({'commit_reproduccion':commit,'comparacion_con_cierre':True,'fuente_preservada':str(ROOT)},indent=2)+'\n')
print('Reproducción comparada en:',dest)
