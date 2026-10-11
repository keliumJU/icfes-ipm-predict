"""Worker propio importable por spawn; solo recibe matrices del intento autorizado."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import warnings,traceback
import numpy as np
from sklearn.exceptions import ConvergenceWarning

def ejecutar(conn,estimator,X,y):
    np.random.seed(20261010)
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            estimator.fit(X,y)
        notes=[dict(categoria=w.category.__name__,mensaje=str(w.message)) for w in caught]
        if any(issubclass(w.category,(ConvergenceWarning,RuntimeWarning)) for w in caught):
            raise ValueError('numerico/convergencia: '+str(notes))
        conn.send(('ok',estimator,notes))
    except BaseException as exc:
        conn.send(('error',type(exc).__name__,str(exc),traceback.format_exc()))
    finally:conn.close()
