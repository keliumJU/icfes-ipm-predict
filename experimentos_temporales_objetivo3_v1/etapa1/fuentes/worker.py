"""Worker propio spawn: solo matrices inventadas entregadas por el padre."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import traceback
from comun import ajustar_inventado


def ejecutar(conn,c,train,contexto):
    try:
        result = ajustar_inventado(c,train,contexto)
        conn.send(('ok',result))
    except BaseException as exc:
        conn.send(('error',type(exc).__name__,str(exc),traceback.format_exc()))
    finally:
        conn.close()


def prueba_hijo(conn,mode):
    """Doble propio para verificar imports/terminación; no modelos ni datos reales."""
    try:
        if mode == 'bloqueo':
            __import__('time').sleep(30)
        elif mode == 'caida':
            os._exit(7)
        else:
            bad = [n for n,m in sys.modules.items() if getattr(m,'__file__',None)
                   and any(x in m.__file__ for x in ('experimentos_objetivo3_v','diagnostico_objetivo3_v1/fase1/fuentes'))]
            conn.send(('ok',dict(imports_ajenos=bad,routing=__import__('sklearn').get_config()['enable_metadata_routing'],
                                 bytecode=sys.dont_write_bytecode,semilla=20261010)))
    finally:
        conn.close()
