"""Un proceso, un Pipeline nuevo, un fit; resultado solo parámetros JSON."""
from infra import *
import sys, warnings, traceback, numpy as np
def work(request):
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import Ridge
    from sklearn.tree import DecisionTreeRegressor
    from threadpoolctl import threadpool_info
    c=request['candidate'];m=load(HERE/request['matrix_file']);deadline(True)
    estimator=Ridge(**c['params']) if c['family']=='Ridge' else DecisionTreeRegressor(**c['params'])
    pipeline=Pipeline([('scaler',StandardScaler(**c['scaler'])),('model',estimator)])
    pp=pipeline.get_params(deep=False);pp={k:v for k,v in pp.items() if k!='steps'}
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        start=time.time();mono=time.monotonic()
        pipeline.fit(np.array(m['train']['X']),np.array(m['train']['y']))
        pred=pipeline.predict(np.array(m['test']['X']));duration=time.monotonic()-mono;end=time.time()
    warn=[dict(category=w.category.__name__,message=str(w.message)) for w in ws]
    check(np.isfinite(pred).all() and not any(w['category'] in ['ConvergenceWarning','RuntimeWarning'] for w in warn),'fallo numérico/convergencia')
    scaler=pipeline.named_steps['scaler'];model=pipeline.named_steps['model']
    result=dict(id=c['id'],family=c['family'],params=c['params'],inputs=c['inputs'],matrix_file=request['matrix_file'],matrix_sha256=sha(HERE/request['matrix_file']),prediction=pred.tolist(),warnings=warn,runtime_params=model.get_params(),pipeline_params=pp,scaler=dict(params=scaler.get_params(),mean=scaler.mean_.tolist(),var=scaler.var_.tolist(),scale=scaler.scale_.tolist(),n_samples_seen=int(scaler.n_samples_seen_)),fit_start_epoch=start,fit_end_epoch=end,fit_duration_seconds=duration,threadpools=threadpool_info(),seed=SEED)
    check(all(t['num_threads']==1 for t in result['threadpools']),'hilos worker')
    if c['family']=='Ridge':result.update(coef=model.coef_.tolist(),intercept=float(model.intercept_),n_features_in=int(model.n_features_in_))
    else:
        t=model.tree_;result['tree']=dict(children_left=t.children_left.tolist(),children_right=t.children_right.tolist(),feature=t.feature.tolist(),threshold=t.threshold.tolist(),value=t.value[:,0,0].tolist(),impurity=t.impurity.tolist(),n_node_samples=t.n_node_samples.tolist(),weighted_n_node_samples=t.weighted_n_node_samples.tolist(),max_depth=int(t.max_depth),node_count=int(t.node_count))
    return result
if __name__=='__main__':
    req=load(HERE/sys.argv[1])
    try:save(HERE/req['output_file'],work(req))
    except BaseException as e:
        save(HERE/req['output_file'],dict(failed=True,classification='numerical_or_implementation',exception=type(e).__name__,message=str(e),traceback=traceback.format_exc()));sys.exit(2)
