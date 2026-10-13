"""Errata documental propia:10CSV, sin cambios analíticos. Preserva cierre anterior."""
from auditor import *
from cerrar_fase4 import verify, conservation, environment_readonly, notebook_readonly

def main():
 original=load(HERE/'MANIFIESTO_FASE4.json')
 for s,h in original['entregables_sha256'].items(): check(sha(HERE/s)==h,'original '+s)
 check(sha(BASE/'CONTINUIDAD_EXPERIMENTAL.md')==original['continuidad_actual_sha256'],'continuidad original')
 actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
 check(actual-set(original['entregables_sha256'])-set(original['exclusiones_autorreferencia'])=={'reparar_conteo.py'},'único nuevo archivo de reparación')
 conservation(); environment_readonly(); notebook_readonly()
 target=HERE/'antecedentes/cierre_preconteo'; check(not target.exists(),'errata ya aplicada'); target.mkdir()
 for p in [HERE/'README.md',HERE/'cerrar_fase4.py',HERE/'REGISTRO_HALLAZGOS.md',HERE/'MANIFIESTO_FASE4.json',HERE/'VERIFICACION_MANIFIESTO_FASE4.json',BASE/'CONTINUIDAD_EXPERIMENTAL.md']:
  (target/p.name).write_bytes(p.read_bytes())
 check(len(list((HERE/'tablas').glob('*.csv')))==10,'conteo real10CSV')
 for p in [HERE/'README.md',HERE/'cerrar_fase4.py',BASE/'CONTINUIDAD_EXPERIMENTAL.md']:
  p.write_text(p.read_text().replace('11CSV','10CSV'))
 p=HERE/'REGISTRO_HALLAZGOS.md'; p.write_text(p.read_text()+'\nErrata documental de cierre: README/continuidad indicaban11CSV; conteo final real10CSV. Se preservó íntegro el cierre previo en antecedentes/cierre_preconteo, se corrigió solo el conteo y se renovó manifiesto/verificación. Tablas, resultados, aceptación y ledger intactos. Sin ajuste ni modificación de criterios.\n')
 m=load(HERE/'MANIFIESTO_FASE4.json'); m['entregables_sha256']={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and p.relative_to(HERE).as_posix() not in m['exclusiones_autorreferencia']}; m['continuidad_actual_sha256']=sha(BASE/'CONTINUIDAD_EXPERIMENTAL.md'); m['errata_documental']='conteo10CSV; cierre anterior íntegro en antecedentes/cierre_preconteo'
 (HERE/'MANIFIESTO_FASE4.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 result=verify(); (HERE/'VERIFICACION_MANIFIESTO_FASE4.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__': main()
