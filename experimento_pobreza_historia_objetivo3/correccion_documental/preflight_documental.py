"""Preserva todos los bytes del cierre antes de completar, sin importar runners."""
from infra_correccion import *
from preflight import conservation,environment
import auditor
AUTH='''Autorizo corregir el arranque del notebook y completar la entrega pendiente de experimento_pobreza_historia_objetivo3, con un presupuesto nuevo máximo de 7200 segundos desde la primera acción.
Preservar el cierre incompleto y el código congelado; guardar la corrección por separado. Revalidar conservación y entorno, probar primero el notebook con datos inventados y reutilizar exclusivamente las matrices, parámetros, selecciones y predicciones del piloto cerrado y auditado.
Cero nuevos ajustes, repeticiones de modelos o cambios científicos. Completar notebook ejecutado, tablas, figuras revisadas, texto académico último, evidencias, informes, manifiesto, verificación y continuidad. Mantener todas las restricciones anteriores y no avanzar automáticamente.
'''
def run():
    deadline();check(not (HERE/'PARTIDA_CORRECCION.json').exists(),'corrección ya iniciada')
    env=environment();cons=conservation();audit=auditor.run(write=False)
    old=load(MAIN/'MANIFIESTO_INCOMPLETO.json')
    for p,h in old['sha256'].items():check(sha(MAIN/p)==h,'cierre previo '+p)
    original={p.relative_to(MAIN).as_posix():sha(p) for p in MAIN.rglob('*') if (p.is_file() or p.is_symlink()) and not p.is_relative_to(HERE)}
    save(HERE/'antecedentes/CONTINUIDAD_INCOMPLETA.md',(MAIN/'CONTINUIDAD.md').read_text())
    save(HERE/'AUTORIZACION.md',AUTH)
    save(HERE/'PARTIDA_CORRECCION.json',dict(original_sha256=original,continuity_mapping='correccion_documental/antecedentes/CONTINUIDAD_INCOMPLETA.md',start_epoch=START,start_utc='2026-10-12T18:37:59Z',max_total_seconds=7200,pilot_reopened=False,new_fits_authorized=0,seed=20261010,closed_previous_verification=load(MAIN/'VERIFICACION_CIERRE_INCOMPLETO.json'),environment=env,conservation=cons,pilot_audit=audit,pilot_ledger_sha256=sha(MAIN/'piloto/ledger.json'),authorization_sha256=sha(HERE/'AUTORIZACION.md')))
    save(HERE/'PREFLIGHT.json',dict(aprobado=True,environment=env,conservation=cons,pilot_audit=audit,previous_files=len(original),start_epoch=START,elapsed_seconds=elapsed(),new_fits=0))
    print(json.dumps(dict(aprobado=True,previous_files=len(original),originals=cons['protegidos'],environment='exacto',new_fits=0,elapsed_seconds=elapsed())))
if __name__=='__main__':run()
