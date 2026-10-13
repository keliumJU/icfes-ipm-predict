"""Controles inventados; ningún fit con panel real."""
from motor import *
from runner import Ledger,reject_crashed
import tempfile,time
def tests():
    start=time.monotonic();spec=load(HERE/'ESPECIFICACION_V6.json');cands=spec['candidates'];done=[];synthetic_fits=0
    def test(n,fn):fn();done.append(n)
    codes=[f'{i:02d}' for i in range(33)];levels={y:np.asarray([200+i+(y-2018)*(i%4+1) for i in range(33)],float) for y in spec['years']};p=build_panel(levels,codes)
    def temporal():
        check(p['previous'][2021]==2019 and np.array_equal(p['d'][2021],levels[2021]-levels[2019]),'sin anualizar')
        for cand in cands:
            for y in [2021,2022,2023,2024,2025]:
                ctx=context(p,cand,y);check(2019 not in ctx['eligible_years'] and all(q<y for q in ctx['eligible_years']),'respuestas elegibles')
                if y==2021:check(not ctx['eligible_years'],'cero historial')
                if y==2022:check(ctx['eligible_years']==[2021],'un año')
        cand=next(c for c in cands if c['id']=='memoria_qr_a0p0_last2');ctx=context(p,cand,2025)
        check(ctx['eligible_years']==[2023,2024] and ctx['components']['memoria']['previous_years']==[2022,2023],'lastk después elegibles')
        check(2018 in p['levels'] and 2020 not in p['levels'],'historial')
    test('temporalidad/lastk/no2019/2020/2018/salto2021',temporal)
    def anti():
        changed=dict(levels);changed[2025]=levels[2025]+100000;changed[2024]=levels[2024]-5000;other=build_panel(changed,codes)
        for c in cands:check(context(p,c,2024)==context(other,c,2024),'anti-fuga futuros')
    test('anti-fuga por mutación de futuros',anti)
    test('defaults completos invariantes',lambda:defaults())
    def fits():
        nonlocal synthetic_fits
        for c in cands:
            z=estimate(c,context(p,c,2021));check(z['fits']==0 and z['statistical_estimates']==0 and z['prediction']==levels[2019].tolist(),'cero respaldo sinfit')
            ctx=context(p,c,2022);z=estimate(c,ctx);synthetic_fits+=z['fits']
            check(z['fits']==len(c['components']) if c['family']!='persistencia' else z['fits']==0,'un fit por componente')
            for comp,data in ctx['components'].items():
                check(len(data['y'])==(1 if comp=='comun' else 33),'33 vs1')
                x=np.asarray(data['X']);m=z['metadata'][comp]
                check(np.allclose(m['scaler_mean'],x.mean(axis=0),rtol=0,atol=1e-12),'scaler train')
                check(np.allclose(m['scaler_var'],x.var(axis=0),rtol=0,atol=1e-12),'scaler var train')
            check(np.array_equal(np.asarray(z['prediction']),np.asarray(ctx['previous_score'])+z['predicted_delta']),'reconstrucción')
            if c['components']:
                a=pipeline(c);b=pipeline(c);check(a is not b and a.named_steps['scaler'] is not b.named_steps['scaler'] and a.named_steps['regressor'] is not b.named_steps['regressor'],'pipelines independientes')
        c=next(c for c in cands if c['id']=='nivel_median_all');ctx=context(p,c,2022);ctx['statistic_values']=[0,2,4,8];z=estimate(c,ctx);check(z['metadata']['statistic_value']==3,'mediana par central')
        c=next(c for c in cands if c['id']=='nivel_mean_all');ctx['statistic_values']=[1e16,1,-1e16];z=estimate(c,ctx);check(z['metadata']['statistic_value']==1/3,'mean fsum')
    test('39 candidatos/cero-un año/Pipelines/scaler/reconstrucción/constantes',fits)
    def selector():
        rr=[dict(id='persistencia',MAE=1.1,RMSE=2.1,inputs=0,order=0),dict(id='rezago',MAE=1,RMSE=2,inputs=1,order=1),dict(id='constante',MAE=1.1,RMSE=2.1,inputs=0,order=2)]
        z=select(rr);check(z['winner']=='persistencia' and len(z['pool_rmse'])==3,'bandas inclusivas entradas0 orden')
        rr[0]['RMSE']=2.10000001;check(select(rr)['winner']=='constante','RMSE mínimo del pool')
        rr[2]['MAE']=1.10000001;check(select(rr)['winner']=='rezago','MAE pool')
    test('selector pools inclusivos/constants0/persistencia primero',selector)
    def csvtest():
        a=pd.DataFrame(dict(code=['a'],year=[1],prediction=[0]));b=a.copy();b.prediction=b.prediction.astype(float);exact_csv(a,b,['code','year'])
        b.loc[0,'prediction']=1e-11
        try:exact_csv(a,b,['code','year'])
        except AssertionError:pass
        else:raise AssertionError('1e-11 debe rechazarse')
    test('CSV intfloat0 exacto/rechazo1e-11',csvtest)
    def routes():
        try:safe(HERE/'../no_autorizado.json')
        except AssertionError:pass
        else:raise AssertionError('traversal')
        try:safe(ROOT/'no_autorizado.json')
        except AssertionError:pass
        else:raise AssertionError('ruta externa')
        link=HERE/'fase1/fixtures/link';link.parent.mkdir(parents=True,exist_ok=True);link.symlink_to('/tmp')
        try:safe(link/'archivo')
        except AssertionError:pass
        else:raise AssertionError('symlink')
    test('rutas/symlinks',routes)
    def integrity():
        for badcodes,badlevels in [(codes[:-1]+[codes[0]],levels),(codes,{**levels,2020:levels[2019]}),(codes,{**levels,2023:levels[2023][:-1]})]:
            try:build_panel(badlevels,badcodes)
            except AssertionError:pass
            else:raise AssertionError('integridad no rechazada')
    test('rechazo duplicados/incompletos/2020',integrity)
    def lineage():
        original=[(ex,y,c['id'],j) for ex in range(2022,2026) for y in range(2021,ex) for c in cands for j in codes]
        representative={(y,c,j):min(ex for ex,iy,ic,ij in original if (iy,ic,ij)==(y,c,j)) for y,c,j in set((y,c,j) for ex,y,c,j in original)}
        check(len(original)==12870 and len(representative)==5148 and all(ex==y+1 for (y,c,j),ex in representative.items()),'linaje exacto menor externo')
        a=context(p,cands[9],2023);b=context(p,cands[9],2023);check(a==b,'copias mismo id ventana')
        check(a!=context(p,cands[10],2023),'no caché entre candidatos')
    test('linaje12870/5148/contextos exactos/reuso mismoIDventana',lineage)
    def durable():
        folder=HERE/'fase1/fixtures/ledger_ok';l=Ledger(folder,20);out=l.task('sleep',dict(test_sleep=.01));check(out['ok'],'worker inventado');l.close(True)
        check(all(x['terminated'] for x in l.state['events']),'terminación serial')
        try:Ledger(folder)
        except AssertionError:pass
        else:raise AssertionError('reapertura')
        l=Ledger(HERE/'fase1/fixtures/ledger_timeout',.05)
        try:l.task('timeout',dict(test_sleep=5))
        except RuntimeError:pass
        else:raise AssertionError('timeout')
        l.close(False);check(l.state['events'][0]['terminated'] and l.state['events'][0]['timeout'],'timeout terminable')
        l=Ledger(HERE/'fase1/fixtures/ledger_retry',20)
        try:l.task('failure',dict(test_fail=True))
        except RuntimeError:pass
        else:raise AssertionError('infraestructura')
        l.close(False);check(l.state['retries']==1 and l.state['failures']==2,'retry máximo1')
        l=Ledger(HERE/'fase1/fixtures/ledger_numeric',20);c=cands[9];ctx=context(p,c,2022);ctx['components']['memoria']['y']=[]
        try:l.task('numeric',dict(candidate=c,context=ctx))
        except RuntimeError:pass
        else:raise AssertionError('numérico')
        l.close(False);check(l.state['retries']==0,'numérico sinretry')
        l=Ledger(HERE/'fase1/fixtures/ledger_crash',20);l.state['pending']={'sin_medicion':True};l.persist();z=reject_crashed(l.path);check(z['elapsed_seconds']==20 and z['pending_unmeasured'],'caída agota saldo')
    test('serial durable terminación/timeout/retry/numérico/caída/presupuesto/no reabrir',durable)
    result=dict(aprobado=True,tests=done,synthetic_component_fits=synthetic_fits,real_fits=0,seconds=time.monotonic()-start)
    save(HERE/'fase1/PRUEBAS.json',result);return result
