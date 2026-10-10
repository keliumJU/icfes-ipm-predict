"""Cierre restringido: solo fase4 y continuidad ya actualizada."""
from revision import *

def cerrar():
 initial=read(F4/'resultados/partida.json');exception='experimentos_objetivo3_v2/CONTINUIDAD_V2.md';verified=0
 for p,h in initial['snapshot_versionados'].items():
  if p!=exception:assert sha(ROOT/p)==h,p;verified+=1
 source_hashes=read(F3/'resultados/conservacion_fuentes.json')['fuentes_sha256']
 for p,h in source_hashes.items():assert sha(ROOT/p)==h,p
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==initial['commit_partida']
 for p in (F4/'fuentes').glob('*.py'):compile(p.read_text(),str(p),'exec')
 nb=read(F4/'resultados/verificacion_notebook.json');assert sha(F4/'notebooks/01_notebook_personal.ipynb')==nb['notebook_sha256'] and sha(F4/'fuentes/01_notebook_personal.py')==nb['fuente_sha256']
 guardar(F4/'resultados/conservacion_final.json',dict(aprobado=True,commit_partida=initial['commit_partida'],versionados_previos_intactos=verified,fuentes_originales_intactas=len(source_hashes),fuentes_sha256=source_hashes,excepcion_autorizada=dict(archivo=exception,antes=initial['snapshot_versionados'][exception],despues=sha(ROOT/exception)),fases1_3_intactas=True,continuidad_historica_y_gitignore_intactos=True,pdf_leidos=[],push=False))
 paths=[p for p in F4.rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']+[ROOT/exception]
 result=read(F4/'resultados/verificacion.json')
 guardar(F4/'resultados/manifiesto_cierre.json',dict(fase='v2/fase4',fecha_cliente='2026-10-10',commit_partida=initial['commit_partida'],entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},revision_completa=True,notebook_personal_entregado=True,mejora_porcentaje=result['condicion']['mejora'],ajustes_nuevos=0,reejecucion_completa_realizada=False,pendientes_indispensables=[],push=False))
 print('Conservación y manifiesto aprobados:',verified,'versionados previos y',len(source_hashes),'fuentes intactos.')
if __name__=='__main__':cerrar()
