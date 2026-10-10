"""Congelar antes de ejecutar pruebas. No llama fit ni predict."""
import sys
sys.dont_write_bytecode=True
import platform,importlib.metadata as md,subprocess,json
from datetime import datetime,timezone
import configuracion as cfg
from comun import guardar,sha

def serial(value):
 if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
 if isinstance(value,(list,tuple)):return [serial(v) for v in value]
 if value is None or isinstance(value,(str,int,float,bool)):return value
 return repr(value)

def congelar():
 path=cfg.F2/'resultados/configuraciones_congeladas.json'
 candidates=cfg.candidatos()
 for c in candidates:
  model=cfg.construir(c)
  c['entradas']=[] if c['especificacion'] is None else cfg.ESPECIFICACIONES[c['especificacion']]
  c['orden']=candidates.index(c)
  c['parametros_completos']=serial(model.get_params(deep=True))
  assert not hasattr(model,'n_features_in_')
 ref=cfg.referencia_v1();ref['parametros_completos']=serial(cfg.construir(ref).get_params(deep=True))
 assert ref['parametros']==ref['parametros_completos']
 obj=dict(version='2.0.2',semilla=cfg.SEMILLA,panel_sha256=sha(cfg.BASE),
  especificaciones=cfg.ESPECIFICACIONES,ventanas=cfg.ventanas(),
  configuraciones=candidates,referencia_historica=ref,
  presupuesto_segundos=cfg.LIMITE_SEGUNDOS,tolerancias=dict(mae=cfg.TOL_MAE,rmse=cfg.TOL_RMSE),orden_familias=cfg.ORDEN)
 if path.exists() and '--enmienda-semilla' not in sys.argv:
  assert json.loads(path.read_text())==obj,'Congelación existente distinta; requiere enmienda'
 else:guardar(path,obj)
 packages={d.metadata['Name']:d.version for d in md.distributions()}
 guardar(cfg.F2/'resultados/entorno.json',dict(python=platform.python_version(),ejecutable=sys.executable,
  paquetes=packages,origen='Paquetes exactos v1 recuperados de caché local pip; entorno transitorio v1 ausente. Sin red.',
  pip_check=subprocess.check_output([sys.executable,'-m','pip','check']).decode().strip(),
  incidencia='Primer intento offline falló por nombres wheel multietiqueta abreviados; se preservaron todas las etiquetas WHEEL, sin cambiar bytes de paquetes. Ningún ajuste.',
  semilla=cfg.SEMILLA))
 (cfg.F2/'requirements.lock.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze']).decode())
 guardar(cfg.F2/'resultados/congelacion_previa.json',dict(momento_utc=datetime.now(timezone.utc).isoformat(),
  protocolo_sha256=sha(cfg.F2/'PROTOCOLO_V2.md'),configuraciones_sha256=sha(path),
  fuentes_sha256={str(p.relative_to(cfg.ROOT)):sha(p) for p in sorted((cfg.F2/'fuentes').glob('*.py'))},
  candidatos_construidos=100,candidatos_ajustados=0,predicciones_panel=0))
 print('100 configuraciones congeladas; cero ajustes.')
if __name__=='__main__':congelar()
