"""Validar datos, reglas y matrices; aceptación y congelación antes de todo fit."""
from infra import *
from diseno import validate_sources,specification,contexts
import pruebas
def run():
    check(load(HERE/'preflight/ENTORNO.json')['aprobado'],'exact environment checked')
    deadline();p,t=validate_sources();s=specification(t);pruebas.run()
    ctx=[(f'i{o}_{i}',i) for o in range(2022,2026) for i in range(2021,o)]+[(f'e{y}',y) for y in range(2021,2026)]
    for context,year in ctx:
        for c in s['candidates']:save(HERE/f'preflight/matrices/{context}__{c["id"]}.json',contexts(p,c,year))
    files=['infra.py','preflight.py','diseno.py','auditor.py','worker.py','piloto.py','pruebas.py','preparar_ejecucion.py','analisis.py','notebook_resultados.py','generar_notebook.py','ESPECIFICACION.json','CANDIDATOS.csv','PLAN.md','AUTORIZACION_SESION.md','preflight/ENTORNO.json','preflight/CONSERVACION.json','preflight/POBLACION.json','preflight/PANEL.csv','preflight/FUENTES.json','preflight/PRUEBAS.json','preflight/PRUEBAS_AUDITOR.json']
    files += [p.relative_to(HERE).as_posix() for p in sorted((HERE/'preflight/matrices').glob('*.json'))]
    check(len(ctx)==15 and len(list((HERE/'preflight/matrices').glob('*.json')))==315,'matrix coverage')
    acceptance=dict(aprobado=True,real_fits=0,synthetic_fits=0,matrix_files=315,operational_acceptance=True,scientific_confirmation=False,epoch=time.time(),pendientes=['autenticidad fuente local','disponibilidad contemporánea','dependencia y todos años vistos'])
    save(HERE/'preflight/ACEPTACION.json',acceptance)
    files+=['preflight/ACEPTACION.json','preflight/NORMALIZACION_CODIGOS.csv','preflight/HALLAZGO_CODIGOS.json','verificar_entrega.py','cerrar.py','PROTOCOLO.md']
    previous=None
    if (HERE/'CONGELACION.json').exists():
        check(not (HERE/'piloto/ledger.json').exists(),'no cambiar congelación después piloto')
        previous=sha(HERE/'CONGELACION.json');save(HERE/f'preflight/CONGELACION_SIN_FITS_{previous[:12]}.json',load(HERE/'CONGELACION.json'))
    save(HERE/'CONGELACION.json',dict(accepted=True,accepted_epoch=time.time(),sha256={f:sha(HERE/f) for f in files},source_hashes=s['source_hashes'],seed=SEED,previous_prefit_freeze_sha=previous,changes_before_any_fit='robustecer pruebas inventadas y comando kernel exacto; cero métricas/candidatos alterados' if previous else None))
    print(json.dumps(acceptance,ensure_ascii=False))
if __name__=='__main__':run()
