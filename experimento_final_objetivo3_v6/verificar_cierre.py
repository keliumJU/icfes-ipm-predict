"""Verificación FINAL solo lectura: cierre incompleto verificable, no eficacia."""
from comun import *
import nbformat,pandas as pd
def verify():
    environment();cons=conservation();hist=historical();m=load(HERE/'MANIFIESTO_FINAL.json')
    for s,h in m['sha256'].items():check(sha(HERE/s)==h,'manifiesto final '+s)
    files={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
    check(files-set(m['exclusions'])==set(m['sha256']),'inventario final exacto')
    # El manifiesto DOCUMENTAL inicial se comprueba contra continuidad fase0 preservada.
    d=load(HERE/'MANIFIESTO_DOCUMENTAL.json')
    for s,h in d['entregables_sha256'].items():
        p=HERE/'fase1/antecedentes/CONTINUIDAD_ANTERIOR.md' if s=='CONTINUIDAD_V6.md' else HERE/s
        check(sha(p)==h,'documental inicial conservado '+s)
    for phase,nextphase in [(1,2),(2,3)]:
        pm=load(HERE/f'fase{phase}/MANIFIESTO.json')
        for s,h in pm['sha256'].items():check(sha(HERE/s)==h,'cierre propio fase '+str(phase)+' '+s)
        check(sha(HERE/f'fase{nextphase}/antecedentes/CONTINUIDAD_ANTERIOR.md')==pm['continuidad_sha'],'continuidad preservada '+str(phase))
    f=load(HERE/'fase1/CONGELACION.json')
    for s,h in f['sha256'].items():check(sha(HERE/s)==h,'freeze operativo conservado '+s)
    for folder,name,source in [('fase1','01_controles.ipynb','notebook_controles.py'),('fase3','02_resultados_objetivo3.ipynb','notebook_resultados.py')]:
        p=HERE/folder/name;e=load(p.with_suffix('.ejecucion.json'));n=nbformat.read(p,as_version=4);nbformat.validate(n);cc=[c for c in n.cells if c.cell_type=='code']
        check(e['notebook_sha256']==sha(p) and e['source_sha256']==sha(HERE/source) and e['generator_sha256']==sha(HERE/'generar_notebook.py'),'notebook sources/hashes')
        check([c.execution_count for c in cc]==list(range(1,len(cc)+1)) and all(c.outputs and not any(o.output_type=='error' for o in c.outputs) for c in cc),'real executed cells')
    ledger=load(HERE/'fase2/piloto/ledger.json');a=load(HERE/'fase3/AUDITORIA_INCOMPLETA.json');accept=load(HERE/'fase3/ACEPTACION.json');ct=load(HERE/'fase3/CONTROL_TEXTO.json')
    check(ledger['status']=='cerrado_incompleto' and ledger['elapsed_seconds']==7200 and ledger['pending_unmeasured'],'ledger conservador cerrado')
    check(not accept['experimento_completo'] and accept['entrega_incompleta_verificable'] and not a['primary_evaluation_valid'] and not a['performance_synthesis'],'incompleto no eficacia')
    check(ct['text_sha']==sha(HERE/'TEXTO_OBJETIVO3_TESIS.md') and ct['evidence_sha']==sha(HERE/'EVIDENCIAS_TEXTO.csv') and ct['new_v6_performance_numbers']==0,'text/evidence/no synthesis')
    ev=pd.read_csv(HERE/'EVIDENCIAS_TEXTO.csv',dtype=str)
    for _,r in ev.iterrows():check(sha(HERE/r.file)==r.sha256,'evidence file hash')
    check(load(HERE/'fase3/REVISION_VISUAL.json')['aprobado'],'visual review')
    return dict(verificacion_cierre_aprobada=True,experimento_completo=False,meta_v6_evaluada=False,ledger='cerrado_incompleto; saldo agotado conservadoramente',huellas=len(m['sha256']),originales_intactos=cons['aprobado'],historicos_mappings=hist['mappings'],fits_verificador=0,modelos_cargados=0,modo='solo lectura sin escritura/fit',pendientes_indispensables=accept['pendientes_indispensables'])
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
