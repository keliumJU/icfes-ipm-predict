"""Verificación SOLO LECTURA; el auditor del piloto permanece independiente e intacto."""
from infra_correccion import *
import nbformat, pandas as pd
from preflight import conservation,environment
from verificar_entrega import evidence_check
import auditor
def preserved():
    p=load(HERE/'PARTIDA_CORRECCION.json')
    for name,h in p['original_sha256'].items():
        target=HERE/'antecedentes/CONTINUIDAD_INCOMPLETA.md' if name=='CONTINUIDAD.md' else MAIN/name
        check(sha(target)==h,'cierre incompleto preservado '+name)
    for name,h in load(MAIN/'CONGELACION.json')['sha256'].items():check(sha(MAIN/name)==h,'científico congelado '+name)
    check(sha(MAIN/'piloto/ledger.json')==p['pilot_ledger_sha256'],'piloto intacto')
    return len(p['original_sha256'])
def notebook_verify(path):
    nb=nbformat.read(path,as_version=4);nbformat.validate(nb);e=load(path.with_name(path.name+'.ejecucion.json'))
    expected=3 if path.name=='NOTEBOOK_INVENTADO.ipynb' else 5
    c=[c for c in nb.cells if c.cell_type=='code']
    check(e['executed'] and e['new_fits']==0 and e['manager']=='AsyncKernelManager' and len(c)==expected and [x.execution_count for x in c]==list(range(1,expected+1)),'notebook real')
    check(all(x.outputs and not any(o.output_type=='error' for o in x.outputs) for x in c),'no outputs manuales/errores')
    for key,p in [('notebook_sha256',path),('source_sha256',HERE/'notebook_corregido.py'),('original_cells_sha256',MAIN/'notebook_resultados.py'),('shared_functions_sha256',MAIN/'analisis.py'),('generator_sha256',HERE/'generar_notebook_corregido.py'),('clock_sha256',HERE/'infra_correccion.py')]:check(e[key]==sha(p),'notebook huella '+key)
    text='\n'.join(o.get('text','') for cell in c for o in cell.outputs)
    check('"model_fits": 0' in text and '"no_fit_guard_active": true' in text,'guardia real cero fits')
    if expected==5:
        import notebook_resultados
        for original,actual in zip(notebook_resultados.CELLS,c):check(actual.source.startswith(original),'celdas científicas preservadas')
    return e
def verify(manifest=True):
    environment();cons=conservation();n=preserved();a=auditor.run(write=False)
    for name,h in load(HERE/'CONGELACION_DOCUMENTAL.json')['sha256'].items():check(sha(MAIN/name)==h,'documental congelado '+name)
    notebook_verify(HERE/'NOTEBOOK_INVENTADO.ipynb');notebook_verify(MAIN/'RESULTADOS.ipynb')
    count=evidence_check();ct=load(MAIN/'CONTROL_TEXTO.json')
    check(ct['aprobado'] and ct['text_sha256']==sha(MAIN/'TEXTO_OBJETIVO3_TESIS.md') and ct['evidence_sha256']==sha(MAIN/'EVIDENCIAS_TEXTO.csv'),'text verified')
    visual=load(MAIN/'resultados/REVISION_VISUAL.json');check(visual['aprobado'],'visual review')
    for name,h in visual['files'].items():check(sha(MAIN/'resultados/figuras'/name)==h,'visual unchanged')
    primary=load(MAIN/'resultados/PRIMARIO.json');check(primary['mejora_primaria_percent']==a['primary_percent'] and primary['meta_cumplida']==a['meets_threshold'],'primary independent')
    ledger=load(HERE/'LEDGER_DOCUMENTAL.json');check(ledger['status']=='cerrado_completo' and ledger['start_epoch']==START and ledger['new_fits']==0,'documental cerrado')
    complete=[r for r in ledger['attempts'] if r['status']=='complete']
    check([r['mode'] for r in complete]==['inventado','preview','final'],'orden inventado/resultados/revisión/texto')
    check(len(complete[-1]['cells'])==5 and complete[-1]['cells'][3]['start_epoch']>visual['review_epoch'],'texto último tras revisión')
    for r in ledger['attempts']:check(r['status'] in ['failed','complete'] and r['end_epoch'] is not None,'no pendiente documental')
    check(len([r for r in ledger['attempts'] if r['status']=='failed'])<=1,'único bloqueo/reintento local')
    end=load(HERE/'CIERRE_DOCUMENTAL.json');check(end['estado']=='completo' and end['start_epoch']==START and end['elapsed_seconds']==end['end_epoch']-START and end['elapsed_seconds']<=7200 and not end['saldo_reutilizable'],'budget nuevo independiente')
    acceptance=load(MAIN/'ACEPTACION_FINAL.json');check(acceptance['completa'] and acceptance['new_fits']==0 and acceptance['independent_confirmation']==False,'technical acceptance')
    if manifest:
        m=load(MAIN/'MANIFIESTO_FINAL.json')
        for name,h in m['sha256'].items():check(sha(MAIN/name)==h,'manifest final '+name)
        paths={p.relative_to(MAIN).as_posix() for p in MAIN.rglob('*') if p.is_file() or p.is_symlink()}
        check(paths-set(m['exclusions'])==set(m['sha256']),'manifest inventory')
    return dict(aprobado=True,solo_lectura=True,new_fits=0,piloto_reabierto=False,original_fits_conservados=200,repeticiones_conservadas=4,archivos_cierre_incompleto_preservados=n,originales=cons['protegidos'],auditoria_piloto_aprobada=True,notebook_celdas_reales=5,evidencias_texto=count,entrega_completa=True,meta_cumplida=primary['meta_cumplida'],mejora_primaria_percent=primary['mejora_primaria_percent'],confirmacion_cientifica=False)
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
