"""Controles de cobertura e integridad etapa2; no ejecuta fits."""
from comun import *
import numpy as np

def validate_outputs(data,levels,ledger):
    internal=data['internal']; external=data['external']; records=data['records']
    exact_coverage([(r['external'],r['validation'],r['candidate'],r['code']) for r in internal],expected_internal_keys())
    exact_coverage([(r['external'],r['policy'],r['code']) for r in external],expected_external_keys())
    assert len(records)==16 and len(data['global_checks'])==5 and all(c['approved'] for c in data['global_checks'])
    for e in YEARS[3:]:
        selected=next(s['candidate'] for s in data['selections'] if s['external']==e)
        recs=[r for r in records if r['external']==e]
        assert select_internal(e,recs)['candidate']==selected
        for rec in recs:
            pool=[r for r in internal if r['external']==e and r['candidate']==rec['candidate']]
            assert rec['eligible'] and rec['n']==len(pool)
            assert metrics([r['observed'] for r in pool],[r['predicted'] for r in pool])=={k:rec[k] for k in ('MAE','RMSE','n')}
        g=[r for r in external if r['external']==e and r['policy']=='global']
        src=[r for r in external if r['external']==e and r['policy']==selected]
        for a,b in zip(g,src): assert all(a[k]==b[k] for k in a if k!='policy')
    for r in internal+external:
        evaluated=r['validation']; previous=max(y for y in YEARS if y<evaluated)
        assert r['observed']==levels[evaluated][r['code']]
        assert r['previous_score']==levels[previous][r['code']] and r['previous_year']==previous
        assert r['predicted']==r['previous_score']+r['delta']
        if evaluated==2021: assert r['delta']==0 and r['interval']==2
    unique,links=lineage(internal); assert unique==data['unique'] and links==data['lineage'] and len(unique)==528
    rolecounts={'interna':0,'externa':0,'repeticion':0}; warnings=[]; started=0
    for attempt in ledger.state['attempts']:
        assert attempt['state']=='success' and digest(safe_path(HERE,attempt['output']))==attempt['output_sha256']
        res=load(safe_path(HERE,attempt['output'])); candidate=res['candidate']; evaluated=res['evaluated']
        p=prepare(levels,evaluated,res['role'])
        assert res['context']==prepared_context(p,candidate)
        # JSON se compara con representación canonizada para tuplas/int claves.
        expected=json.loads(json.dumps(serial_prepared(p,candidate)))
        assert all(res[k]==v for k,v in expected.items())
        if 'request' in attempt:
            req=load(safe_path(HERE,attempt['request']))
            assert digest(safe_path(HERE,attempt['request']))==attempt['request_sha256']
            assert all(int(y)<evaluated for y in req['levels'])
            assert attempt['process_terminated']
        components=COMPONENTS[candidate_index(candidate)] if p.supervised_years and candidate!='persistencia' else ()
        assert res['fits']==len(components)==attempt['pipeline_fits_started']
        started+=res['fits']; delta=np.zeros(33)
        for component in components:
            evidence=res['pipelines'][component]; X,y=p.matrices[component]
            assert len(X)==len(p.supervised_years)*(1 if component=='comun' else 33)
            scaler=evidence['scaler']; reg=evidence['regressor']
            assert scaler['params']==SCALER and reg['params']==REGRESSOR
            np.testing.assert_allclose(scaler['mean'],np.mean(X,axis=0),atol=1e-12,rtol=0)
            np.testing.assert_allclose(scaler['var'],np.var(X,axis=0),atol=1e-12,rtol=0)
            assert scaler['n_samples_seen']==len(X)
            prediction=((p.prediction_inputs[component]-np.array(scaler['mean']))/np.array(scaler['scale']))@np.array(reg['coef'])+reg['intercept']
            delta+=prediction[0] if component=='comun' else prediction
        np.testing.assert_allclose(delta,res['delta'],atol=1e-10,rtol=0)
        key='repeticion' if attempt['job'].startswith('rep_') else res['role']
        rolecounts[key]+=res['fits']; warnings.extend(res['warnings'])
    assert rolecounts['interna']==24 and rolecounts['externa']==16 and rolecounts['repeticion']<=6 and started<=46
    assert started==data['pipeline_fits_started']
    return {'aprobado':True,'internas':1320,'internas_unicas':528,'linaje':1320,'registros_seleccion':16,'externas':825,
            'global_checks':5,'fits':rolecounts,'fits_total':started,'warnings':warnings,
            'controles':'Coberturas exactas, contextos/matrices/llaves/fechas/defaults/semilla/objetivos anteriores, scaler aritmético, reconstrucción predicción, selección solo internas, copias/linaje/reuso/global, huellas y procesos terminados',
            'alcance':'Controles indispensables del piloto fase3. No reemplaza auditoría interpretativa fase4.'}
