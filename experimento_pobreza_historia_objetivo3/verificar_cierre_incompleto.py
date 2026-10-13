"""SOLO LECTURA: verifica conservación y cierre incompleto, nunca aprobación de entrega."""
from infra import *
from preflight import conservation,environment
import auditor
def verify():
    c=conservation();environment();a=auditor.run(write=False)
    m=load(HERE/'MANIFIESTO_INCOMPLETO.json')
    for p,h in m['sha256'].items():check(sha(HERE/p)==h,'manifest incompleto '+p)
    paths={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
    check(paths-set(m['exclusions'])==set(m['sha256']),'inventory incompleto')
    end=load(HERE/'CIERRE_SESION.json');check(end['estado']=='incompleto' and end['end_epoch']-START==end['elapsed_seconds'] and end['elapsed_seconds']<=7200 and not end['saldo_reutilizable'] and end['no_auto_advance'],'incomplete closure')
    i=load(HERE/'INCIDENCIA_NOTEBOOK.json');check(i['estado']=='cerrado_fallido' and i['retry_total_sesion']==1 and i['process_terminated'] and i['notebook_cells_executed']==0,'notebook failure documented')
    check(not (HERE/'RESULTADOS.ipynb').exists() and not (HERE/'PREVIEW.ipynb').exists() and not (HERE/'TEXTO_OBJETIVO3_TESIS.md').exists() and not (HERE/'ACEPTACION_FINAL.json').exists(),'no deliverables simulated')
    check(sha(HERE/'antecedentes/CONTINUIDAD_PREPARACION.md')==load(HERE/'MANIFIESTO_PREPARACION.json')['sha256']['CONTINUIDAD.md'],'continuity preparation conserved')
    return dict(conservacion_cierre_incompleto_verificados=True,entrega_completa=False,meta_certificada=False,solo_lectura=True,new_fits=0,originales=c['protegidos'],piloto_cerrado=True,original_fits=a['original_fits'],repeticiones=a['repetitions'],auditoria_piloto_aprobada=True,notebook_ejecutado=False,texto_academico_generado=False,retry_total_sesion=1,pendientes=['notebook ejecutado','tablas/figuras de notebook y revisión visual','texto último y evidencias','aceptación completa'],avance_automatico=False)
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
