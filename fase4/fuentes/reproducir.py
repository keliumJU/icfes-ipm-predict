"""Reproduce en copia nueva conservando cierre fuente. No ejecutado en el cierre."""
import sys, subprocess, shutil, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
START='9a22b8adc406423fa6829b75e77d7473deffe710'
if len(sys.argv)!=2: raise SystemExit('Uso: python reproducir.py /tmp/ruta-inexistente')
target=Path(sys.argv[1]).resolve()
assert not target.exists(), 'La copia debe ser nueva'
subprocess.run(['git','clone','--no-hardlinks','--quiet',str(ROOT),str(target)],check=True)
subprocess.run(['git','checkout','--quiet',START],cwd=target,check=True)
(target/'fase4/resultados').mkdir(parents=True)
shutil.copytree(ROOT/'fase4/fuentes',target/'fase4/fuentes')
shutil.copy2(ROOT/'fase4/decisiones_previas.md',target/'fase4/decisiones_previas.md')
# Reutilizar entorno fijado; la preparación comprueba TODAS sus versiones.
python=Path('/tmp/icfes-fase3-venv/bin/python');assert python.exists()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
commands=[['-c',"import sys;sys.path.insert(0,'fase4/fuentes');import analisis;analisis.prepare()"],['fase4/fuentes/generar_notebooks.py'],['fase4/fuentes/documentar.py'],['fase4/fuentes/generar_notebooks.py','--reusar-salidas'],['fase4/fuentes/verificar_cierre.py']]
for args in commands:subprocess.run([str(python),*args],cwd=target,env=env,check=True)
print('Copia ejecutada:',target,'; fuente conservada; commit base:',START)
