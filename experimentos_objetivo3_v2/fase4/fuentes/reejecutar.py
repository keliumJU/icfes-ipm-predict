"""Reejecución VOLUNTARIA completa: solo nuevos artefactos en fase4/reproducciones."""
from revision import *
import piloto as motor
from datetime import datetime,timezone
from presentar import presentar

def reejecutar(nombre=None):
 integrity=integridad()
 name=nombre or datetime.now(timezone.utc).strftime('piloto_%Y%m%dT%H%M%S%fZ')
 if not re.fullmatch(r'[A-Za-z0-9_-]+',name):raise ValueError('Nombre de reproducción no válido')
 target=(F4/'reproducciones'/name).resolve();assert target.is_relative_to((F4/'reproducciones').resolve())
 if target.exists():raise FileExistsError('Destino existente: no se reutiliza ni se borra un ledger')
 target.mkdir(parents=True);source=target/'resultados';source.mkdir()
 guardar(source/'entorno.json',dict(python=integrity['python'],paquetes=integrity['paquetes'],ejecutable=sys.executable,semilla=20261010))
 freeze=read(F3/'resultados/congelacion_operativa.json');freeze['entorno_sha256']=sha(source/'entorno.json');freeze['tipo']='Reproducción voluntaria nueva; congelados fase2/fase3 intactos';guardar(source/'congelacion_operativa.json',freeze)
 guardar(target/'entrada.json',dict(configuraciones_sha256=sha(CONFIG),panel_sha256=sha(cfg.BASE),motor_sha256=sha(F3/'fuentes/piloto.py'),semilla=20261010,limite_segundos=7200,nota='Ledger propio del piloto completo nuevo, sin reutilizar ni alterar saldo o artefactos fase3.'))
 motor.F3=target
 runner=motor.Runner(source/'piloto',cargar_panel(),read(CONFIG),limit=7200)
 try:
  runner.run();m,c,p,r=revisar(source,source/'revision');presentar(m,c,p,source/'revision');guardar(target/'cierre.json',dict(completo=True,verificacion=r))
 except BaseException:
  import traceback
  guardar(target/'cierre.json',dict(completo=False,error=traceback.format_exc(),ledger_preservado=True));raise
 return target
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--nombre');args=parser.parse_args();print(reejecutar(args.nombre))
