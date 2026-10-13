"""Worker propio spawn: solo matrices inventadas entregadas por el padre."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import traceback
from comun import ajustar_autorizado


def ejecutar(conn,c,train,contexto):
    try:
        result = ajustar_autorizado(c,train,contexto)
        conn.send(('ok',result))
    except BaseException as exc:
        conn.send(('error',type(exc).__name__,str(exc),traceback.format_exc()))
    finally:
        conn.close()

