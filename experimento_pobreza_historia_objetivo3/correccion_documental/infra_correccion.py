"""Infraestructura documental nueva: reloj separado y prohibición de fits.

No cambia START del piloto ni ninguna función científica del código congelado.
"""
from pathlib import Path
import time, sys, json
MAIN=Path(__file__).resolve().parent.parent
HERE=MAIN/'correccion_documental'
ROOT=MAIN.parent
START=1791830279.0  # primera acción de corrección:2026-10-12 18:37:59UTC
sys.path.insert(0,str(MAIN))
from infra import save,load,sha,check
def elapsed():return time.time()-START
def deadline(fits=False):
    check(not fits,'ningún fit autorizado en corrección')
    check(elapsed()<7200,'presupuesto documental absoluto agotado')
FIT_CALLS=[]
def no_fit_guard(frame,event,arg):
    if event=='call' and frame.f_globals.get('__name__','').startswith('sklearn.') and frame.f_code.co_name in ['fit','partial_fit','fit_transform','fit_predict']:
        FIT_CALLS.append(dict(module=frame.f_globals.get('__name__'),function=frame.f_code.co_name))
        raise RuntimeError('Fit prohibido en corrección documental')
def activate(analysis=None):
    deadline()
    if analysis is not None:analysis.deadline=deadline  # solo adaptador de reloj, sin cambios aritméticos
    sys.setprofile(no_fit_guard)
    return dict(budget_start=START,model_fits=len(FIT_CALLS),clock='corrección documental',scientific_functions_unchanged=True)
def guard_status():
    check(not FIT_CALLS,'fit detectado')
    return dict(model_fits=len(FIT_CALLS),no_fit_guard_active=sys.getprofile() is no_fit_guard)
