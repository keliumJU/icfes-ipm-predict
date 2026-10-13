"""Un candidato y contexto por proceso; Pipeline propio por componente."""
from comun import *
import warnings, platform, traceback
import numpy as np, sklearn

def main():
    relative=sys.argv[1]; req=load(safe_path(HERE,relative))
    output=req['output']; progress=req['progress']
    # Solo inyecciones sintéticas de infraestructura/terminación, nunca panel real.
    if req.get('synthetic') and req.get('mode') in ('infrastructure','wait'):
        if req['mode']=='wait': time.sleep(10)
        sys.exit(3)
    levels={int(y):a for y,a in req['levels'].items()}
    p=prepare(levels,req['evaluated'],req['role']); candidate=req['candidate']
    assert prepared_context(p,candidate)==req['context']
    np.random.seed(SEED)
    evidence=serial_prepared(p,candidate)
    fits=[]; warns=[]
    def factory():
        pipe=new_pipeline(); old=pipe.fit
        comp=COMPONENTS[candidate_index(candidate)][len(fits)]
        def fit(X,y,**kwargs):
            assert not kwargs
            rec={'component':comp,'state':'started','X':X.tolist(),'y':y.tolist(),'start_monotonic':time.monotonic()}
            fits.append(rec); write(progress,{'fits':fits})
            if req.get('synthetic') and req.get('mode')=='numerical': raise NumericalFailure('fallo numérico inventado')
            result=old(X,y)
            rec.update(state='complete',seconds=time.monotonic()-rec['start_monotonic'])
            write(progress,{'fits':fits}); return result
        pipe.fit=fit
        return pipe
    start=time.monotonic()
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            res=fit_predict(p,candidate,factory)
        warns=[{'category':w.category.__name__,'message':str(w.message)} for w in caught]
        if not np.isfinite(res['score']).all(): raise NumericalFailure('Puntaje no finito')
        evidence.update(state='success',score=res['score'].tolist(),delta=res['delta'].tolist(),reason=res['reason'],fits=res['fits'],
            pipelines={k:{'scaler':{'params':obj.named_steps['scaler'].get_params(),
                'mean':obj.named_steps['scaler'].mean_.tolist(),'var':obj.named_steps['scaler'].var_.tolist(),
                'scale':obj.named_steps['scaler'].scale_.tolist(),'n_samples_seen':int(obj.named_steps['scaler'].n_samples_seen_)},
                'regressor':{'params':obj.named_steps['regressor'].get_params(),'coef':obj.named_steps['regressor'].coef_.tolist(),
                'intercept':float(obj.named_steps['regressor'].intercept_),'n_iter':int(obj.named_steps['regressor'].n_iter_)}}
                for k,obj in res['pipelines'].items()})
        code=0
    except NumericalFailure as exc:
        evidence.update(state='numerical',reason=str(exc),fits_started=len(fits)); code=2
    except IntegrityError as exc:
        evidence.update(state='integrity',reason=str(exc),fits_started=len(fits)); code=4
    except Exception as exc:
        evidence.update(state='infrastructure',reason=repr(exc),traceback=traceback.format_exc(),fits_started=len(fits)); code=3
    evidence.update(warnings=warns,seconds_worker=time.monotonic()-start,python=platform.python_version(),sklearn=sklearn.__version__,fit_progress=fits,synthetic=req.get('synthetic',False))
    write(output,evidence); sys.exit(code)
if __name__=='__main__': main()
