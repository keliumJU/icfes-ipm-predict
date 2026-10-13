"""Pruebas de contrato exclusivamente inventadas. No lee el panel real.

Ejecutar con el entorno exacto después de preflight. Cada corrida preserva
artefactos sintéticos en un directorio nuevo; no consume presupuesto futuro.
"""
from pathlib import Path
import copy
import csv
import json
import math
import time
import traceback
import warnings
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from motor import (YEARS,CODES,CANDIDATES,COMPONENTS,INPUTS,SCALER,REGRESSOR,SEED,
                   FUTURE_CONTRACT,IntegrityError,NumericalFailure,new_pipeline,
                   window,prepare,fit_predict,metrics,select_internal,exact_coverage,
                   expected_internal_keys,expected_external_keys,lineage,reuse_global)
from integridad import safe_path,digest,context_hash,exact_csv
from ejecucion_sintetica import (BASE,SyntheticLedger,BudgetError,InfrastructureFailure,run_invented)

HERE=Path(__file__).resolve().parent
DESIGN=HERE.parents[1]/'diseno_memoria_comun_objetivo3_v1'

def reject(call,exc=IntegrityError):
    try: call()
    except exc: return
    raise AssertionError(f'No rechazó {exc.__name__}')

def invented():
    rng=np.random.default_rng(SEED)
    # Niveles totalmente inventados; diferencias con signos y mediana conocida.
    scores=100+np.arange(33,dtype=float)
    result={2018:dict(zip(CODES,scores.tolist()))}
    for i,y in enumerate(YEARS[1:]):
        scores=scores+(np.arange(33)-16)*(i+1)/8+(i-2)+rng.integers(-2,3,size=33)
        result[y]=dict(zip(CODES,scores.tolist()))
    return result

class Suite:
    def __init__(self,folder):
        self.folder=folder
        self.synthetic_fits=0
        self.negative_checks=0

    def factory(self):
        outer=self
        pipeline=new_pipeline()
        original=pipeline.fit
        def counted(X,y,**kwargs):
            assert not kwargs, 'No sample_weight/recencia'
            assert X.shape[1]==1
            outer.synthetic_fits+=1
            return original(X,y)
        pipeline.fit=counted
        return pipeline

    def no(self,call,exc=IntegrityError):
        reject(call,exc); self.negative_checks+=1

    def dates_and_history(self):
        panel=invented()
        for evaluated in YEARS[2:]:
            p=prepare(panel,evaluated)
            prior=max(y for y in YEARS if y<evaluated)
            assert p.previous_year==prior
            assert p.supervised_years==tuple(y for y in YEARS[2:] if y<evaluated)
            assert 2019 not in p.supervised_years and 2020 not in p.history_years
            for component,keys in p.keys.items():
                for key in keys:
                    response,lag=key[-2:]
                    assert lag==max(y for y in YEARS if y<response)
                    assert lag<response<evaluated
        p=prepare(panel,2021)
        assert p.previous_year==2019 and 2021-p.previous_year==2
        np.testing.assert_array_equal(p.d[2019],np.array([panel[2019][c]-panel[2018][c] for c in CODES]))
        contaminated=copy.deepcopy(panel); contaminated[2020]={c:1e7 for c in CODES}
        q=prepare(contaminated,2021)
        np.testing.assert_array_equal(q.previous_score,p.previous_score)
        self.no(lambda:prepare(panel,2019))
        self.no(lambda:prepare(panel,2020))
        self.no(lambda:prepare(panel,2022,'otro'))

    def geography_and_units(self):
        sem=json.loads((DESIGN/'SEMANTICA_FASE1.json').read_text())
        assert tuple(sem['territorios'])==CODES and len(CODES)==33
        panel=invented(); p=prepare(panel,2025)
        for y in p.d:
            raw=[panel[y][c]-panel[max(t for t in YEARS if t<y)][c] for c in CODES]
            assert p.c[y]==sorted(raw)[16]
            np.testing.assert_array_equal(p.r[y],np.array(raw)-sorted(raw)[16])
        for k,n in [('memoria',132),('comun',4),('correccion',132)]:
            X,y=p.matrices[k]; assert X.shape==(n,1) and y.shape==(n,)
        # Independencia del orden de los códigos y respuesta/rezago manual.
        shuffled={y:dict(reversed(list(a.items()))) for y,a in panel.items()}
        q=prepare(shuffled,2025)
        for k in p.matrices:
            for a,b in zip(p.matrices[k],q.matrices[k]): np.testing.assert_array_equal(a,b)
        X,y=p.matrices['memoria']
        assert X[0,0]==panel[2019]['05']-panel[2018]['05']
        assert y[0]==panel[2021]['05']-panel[2019]['05']
        bad=copy.deepcopy(panel); bad[2021]['00']=bad[2021].pop('05')
        self.no(lambda:prepare(bad,2022))
        bad=copy.deepcopy(panel); del bad[2019]['94']
        self.no(lambda:prepare(bad,2021))
        bad=copy.deepcopy(panel); del bad[2021]
        self.no(lambda:prepare(bad,2023))
        bad=copy.deepcopy(panel); bad[2019]['05']=float('nan')
        self.no(lambda:prepare(bad,2021))

    def documentary_defaults(self):
        spec=json.loads((DESIGN/'ESPECIFICACION_DOCUMENTAL.json').read_text())
        assert [window(y) for y in YEARS[2:]]==spec['ventanas']
        assert list(CANDIDATES)==[c['id'] for c in spec['candidatos']]
        assert list(INPUTS)==[c['n_entradas_derivadas'] for c in spec['candidatos']]
        assert new_pipeline().named_steps['scaler'].get_params()==SCALER==spec['pipeline_componentes']['defaults_completos']['StandardScaler']
        assert new_pipeline().named_steps['regressor'].get_params()==REGRESSOR==spec['pipeline_componentes']['defaults_completos']['QuantileRegressor']
        assert tuple(tuple(k['nombre'] for k in c['componentes']) for c in spec['candidatos'])==COMPONENTS
        assert SEED==spec['semilla'] and spec['pipeline_componentes']['recencia'] is False
        assert FUTURE_CONTRACT['cota_sin_fallos']==24+16+6==46
        assert FUTURE_CONTRACT['presupuesto_segundos']==7200 and FUTURE_CONTRACT['saldo_heredado'] is None
        with (DESIGN/'TRAZABILIDAD_TEMPORAL.csv').open() as f:
            rows=list(csv.DictReader(f))
        assert len(rows)==15
        for row in rows:
            p=prepare(invented(),int(row['evaluado']),row['tipo'])
            assert len(p.supervised_years)==int(row['anios_pares_completos'])
            assert len(p.matrices['comun'][1])==int(row['filas_comun'])
            assert len(p.matrices['memoria'][1])==int(row['filas_memoria_correccion'])

    def zero_one_and_fixed_2021(self):
        panel=invented()
        def forbidden(): raise AssertionError('Cero pares no debe crear scaler ni fit')
        for role in ('interna','externa'):
            p=prepare(panel,2021,role)
            for candidate in CANDIDATES:
                out=fit_predict(p,candidate,forbidden)
                assert out['fits']==0 and not out['pipelines']
                np.testing.assert_array_equal(out['score'],p.previous_score)
        self.no(lambda:select_internal(2021,[]))
        records=[{'external':2022,'role':'interna','candidate':c,'eligible':True,'n':33,**metrics(np.ones(33),np.zeros(33))} for c in CANDIDATES]
        assert select_internal(2022,records)['candidate']=='persistencia'
        p=prepare(panel,2022)
        assert p.supervised_years==(2021,)
        outputs={c:fit_predict(p,c,self.factory) for c in CANDIDATES}
        assert [outputs[c]['fits'] for c in CANDIDATES]==[0,1,1,2]
        common=outputs['comun']['pipelines']['comun']
        correction_common=outputs['comun_correccion']['pipelines']['comun']
        assert common is not correction_common
        assert common.named_steps['scaler'].n_samples_seen_==1
        np.testing.assert_array_equal(common.named_steps['scaler'].transform(p.matrices['comun'][0]),np.zeros((1,1)))
        np.testing.assert_allclose(outputs['comun']['delta'],np.repeat(p.c[2021],33),atol=1e-10,rtol=0)

    def training_scaler_and_invariance(self):
        panel=invented(); changed=copy.deepcopy(panel)
        for y in (2023,2024,2025): changed[y]={c:float('nan') for c in CODES}
        # Valores evaluados/futuros no se acceden; ni siquiera no-finitos alteran train.
        p=prepare(panel,2023); q=prepare(changed,2023)
        assert p.c==q.c and p.keys==q.keys
        for k in p.matrices:
            for a,b in zip(p.matrices[k],q.matrices[k]): np.testing.assert_array_equal(a,b)
            np.testing.assert_array_equal(p.prediction_inputs[k],q.prediction_inputs[k])
        for candidate in CANDIDATES:
            a=fit_predict(p,candidate,self.factory); b=fit_predict(q,candidate,self.factory)
            np.testing.assert_allclose(a['score'],b['score'],atol=1e-10,rtol=0)
            np.testing.assert_array_equal(a['score'],p.previous_score+a['delta'])
            for component,pipe in a['pipelines'].items():
                scaler=pipe.named_steps['scaler']; X=p.matrices[component][0]
                assert scaler.n_samples_seen_==len(X)
                np.testing.assert_allclose(scaler.mean_,X.mean(axis=0),atol=1e-12,rtol=0)
                np.testing.assert_allclose(scaler.var_,X.var(axis=0),atol=1e-12,rtol=0)
                np.testing.assert_array_equal(scaler.mean_,b['pipelines'][component].named_steps['scaler'].mean_)
                assert pipe.named_steps['regressor'].n_features_in_==1
        # Copias nuevas por llamada, sin compartir fits aun idéntico contexto.
        a=fit_predict(p,'comun',self.factory); b=fit_predict(p,'comun',self.factory)
        assert a['pipelines']['comun'] is not b['pipelines']['comun']
        # Territorial: entradas iguales producen predicciones iguales, sin código.
        p.prediction_inputs['correccion'][:]=7
        a=fit_predict(p,'comun_correccion',self.factory)
        assert len(set(a['delta']))==1
        self.no(lambda:reuse_global(a,'comun_correccion',2023,'comun',2023))
        self.no(lambda:reuse_global(a,'comun_correccion',2023,'comun_correccion',2024))
        np.testing.assert_array_equal(reuse_global(a,'comun_correccion',2023,'comun_correccion',2023),a['score'])

    def numerical_failures(self):
        p=prepare(invented(),2022)
        class Fake:
            def __init__(self,mode): self.mode=mode
            def fit(self,X,y):
                if self.mode=='value': raise ValueError('HiGHS inventado falla')
                if self.mode=='warning': warnings.warn('Convergencia inventada',ConvergenceWarning)
                return self
            def predict(self,X): return np.repeat(np.nan if self.mode=='nan' else 0,len(X))
        for mode in ('value','warning','nan'):
            self.no(lambda:fit_predict(p,'memoria',lambda:Fake(mode)),NumericalFailure)
        shared=Fake('ok')
        self.no(lambda:fit_predict(p,'comun_correccion',lambda:shared))

    def selection_bands_and_ties(self):
        def records(mae,rmse):
            return [{'external':2023,'role':'interna','candidate':c,'eligible':True,'n':66,'MAE':a,'RMSE':b} for c,a,b in zip(CANDIDATES,mae,rmse)]
        assert select_internal(2023,records([1]*4,[2]*4))['candidate']=='persistencia'
        assert select_internal(2023,records([2,1,1,1],[2]*4))['candidate']=='memoria'
        assert select_internal(2023,records([2,2,1,1],[2]*4))['candidate']=='comun'
        assert select_internal(2023,records([2,2,2,1],[2]*4))['candidate']=='comun_correccion'
        # Límites inclusivos y siguiente representable fuera de banda.
        band=1.0+0.1
        r=records([band,1,3,3],[2]*4)
        assert select_internal(2023,r)['candidate']=='persistencia'
        r[0]['MAE']=math.nextafter(band,math.inf)
        assert select_internal(2023,r)['candidate']=='memoria'
        r=records([1]*4,[band,1,3,3])
        assert select_internal(2023,r)['candidate']=='persistencia'
        r[0]['RMSE']=math.nextafter(band,math.inf)
        assert select_internal(2023,r)['candidate']=='memoria'
        r=records([1,2,1,1],[4,0,3,3])
        assert select_internal(2023,r)['candidate']=='comun' # RMSE mínimo solo pool MAE
        bad=records([1]*4,[2]*4); bad[0].update(eligible=False,reason='numérico')
        self.no(lambda:select_internal(2023,bad))
        bad=records([1]*4,[2]*4); bad[1].update(eligible=False,reason='numérico')
        assert select_internal(2023,bad)['candidate']=='persistencia'
        bad[1].pop('reason'); self.no(lambda:select_internal(2023,bad))
        bad=records([1]*4,[2]*4); bad[0]['n']=65
        self.no(lambda:select_internal(2023,bad))
        bad=records([1]*4,[2]*4); bad[0]['MAE']=float('nan')
        self.no(lambda:select_internal(2023,bad))
        bad=records([1]*4,[2]*4); bad[0]['role']='externa'
        self.no(lambda:select_internal(2023,bad))
        bad=records([1]*4,[2]*4); bad[0]['candidate']='memoria'
        self.no(lambda:select_internal(2023,bad))
        assert metrics([0,0,0],[1,2,3])['MAE']==2
        assert metrics([0,0],[1,3])['RMSE']==math.sqrt(5)

    def coverage_and_csv(self):
        a=expected_internal_keys(); b=expected_external_keys()
        assert len(a)==1320 and len(b)==825 and len(set(b))==825
        assert 4*len(YEARS[3:])==16
        assert exact_coverage(a,a)
        self.no(lambda:exact_coverage(a[:-1],a))
        self.no(lambda:exact_coverage(a+[a[0]],a))
        left=self.folder/'csv_original.csv'; right=self.folder/'csv_equivalente.csv'
        left.write_text('codigo,anio,delta\n05,2021,0\n08,2021,2.5\n')
        right.write_text('codigo,anio,delta\n05,2021,0.0\n08,2021,2.5\n')
        assert exact_csv(left,right,numeric=('delta',),keys=('codigo','anio'))
        self.no(lambda:exact_csv(left,right,numeric=('delta',),keys=('faltante',)))
        for name,text in [('1e-11','codigo,anio,delta\n05,2021,0.00000000001\n08,2021,2.5\n'),
                          ('orden','codigo,anio,delta\n08,2021,2.5\n05,2021,0\n'),
                          ('columnas','anio,codigo,delta\n2021,05,0\n2021,08,2.5\n'),
                          ('codigo','codigo,anio,delta\n5,2021,0\n08,2021,2.5\n'),
                          ('nofinito','codigo,anio,delta\n05,2021,nan\n08,2021,2.5\n'),
                          ('duplicado','codigo,anio,delta\n05,2021,0\n05,2021,2.5\n')]:
            p=self.folder/f'csv_rechazado_{name}.csv'; p.write_text(text)
            self.no(lambda:exact_csv(left,p,numeric=('delta',),keys=('codigo','anio')))

    def copies_lineage_context(self):
        rows=[{'external':e,'validation':v,'candidate':c,'code':code,'observed':float(v),'predicted':0.0,
               'context':context_hash({'candidate':c,'validation':v,'history':[y for y in YEARS if y<v],
                                       'defaults':[SCALER,REGRESSOR],'seed':SEED,'matrices':'inventadas constantes'})} for e,v,c,code in expected_internal_keys()]
        frozen=copy.deepcopy(rows)
        unique,links=lineage(rows)
        assert len(unique)==528 and len(links)==1320 and rows==frozen
        for r in unique: assert r['external']==r['validation']+1
        bad=copy.deepcopy(rows); bad[-1]['predicted']+=1e-11
        self.no(lambda:lineage(bad))
        bad=copy.deepcopy(rows); bad[-1]['context']='matriz alterada'
        self.no(lambda:lineage(bad))
        bad=copy.deepcopy(rows); bad[-1]['observed']+=1
        self.no(lambda:lineage(bad))
        assert context_hash({'a':1,'b':2})==context_hash({'b':2,'a':1})
        assert context_hash({'seed':1})!=context_hash({'seed':SEED})
        (self.folder/'linaje_inventado.json').write_text(json.dumps({'unique':len(unique),'original':len(rows),'representatives':sorted(set(r['external'] for r in unique))}))

    def paths_symlinks_and_conservation(self):
        for bad in ('../escape','/tmp/escape','x/../../escape'):
            self.no(lambda:safe_path(self.folder,bad))
        original=self.folder/'original.txt'; original.write_text('conservar')
        before=digest(original)
        alias=self.folder/'alias'; alias.symlink_to(original.name)
        self.no(lambda:safe_path(self.folder,'alias'))
        self.no(lambda:digest(alias))
        folder_alias=self.folder/'alias_dir'; folder_alias.symlink_to(self.folder,target_is_directory=True)
        self.no(lambda:safe_path(self.folder,'alias_dir/nuevo'))
        self.no(lambda:safe_path(folder_alias,'nuevo'))
        self.no(lambda:safe_path(self.folder/'sub'/'..'/'alias_dir','nuevo'))
        assert digest(original)==before
        assert original.read_text()=='conservar'

    def budget_retry_resume(self):
        rel=self.folder.relative_to(BASE)
        ledger=SyntheticLedger(rel/'ledger_estados.json',10,'contexto-inventado')
        assert ledger.state['used']==0 and ledger.state['limit']==10
        assert ledger.begin('a') is True
        self.no(lambda:ledger.begin('b')) # serial
        ledger.finish('a','infrastructure',2)
        assert ledger.begin('a') is True
        artifact=safe_path(ledger.path.parent,'inventado.txt'); artifact.write_text('inventado')
        ledger.finish('a','success',3,'inventado.txt')
        assert ledger.state['used']==5 and ledger.begin('a') is False
        resumed=SyntheticLedger(rel/'ledger_estados.json',10,'contexto-inventado')
        assert resumed.state['used']==5 and resumed.begin('a') is False
        self.no(lambda:SyntheticLedger(rel/'ledger_estados.json',11,'contexto-inventado'))
        self.no(lambda:SyntheticLedger(rel/'ledger_estados.json',10,'cambiado'))
        artifact.write_text('corrupto')
        self.no(lambda:SyntheticLedger(rel/'ledger_estados.json',10,'contexto-inventado'))
        numerical=SyntheticLedger(rel/'numerico'/'ledger.json',10,'inventado')
        numerical.begin('x'); numerical.finish('x','numerical',1)
        self.no(lambda:numerical.begin('x'))
        retry=SyntheticLedger(rel/'retry'/'ledger.json',10,'inventado')
        for i in range(2): retry.begin('x'); retry.finish('x','infrastructure',1)
        self.no(lambda:retry.begin('x'),InfrastructureFailure)
        crash=SyntheticLedger(rel/'caida'/'ledger.json',10,'inventado')
        crash.begin('x')
        self.no(lambda:SyntheticLedger(rel/'caida'/'ledger.json',10,'inventado'),BudgetError)
        state=json.loads(crash.path.read_text()); assert state['used']==10 and state['attempts'][0]['status']=='unknown_crash'
        exhausted=SyntheticLedger(rel/'caida'/'ledger.json',10,'inventado')
        self.no(lambda:exhausted.begin('nuevo'),BudgetError)
        limit=SyntheticLedger(rel/'limite'/'ledger.json',1,'inventado')
        limit.begin('x'); limit.finish('x','infrastructure',2)
        assert limit.state['used']==1 and limit.state['attempts'][0]['status']=='timeout'
        self.no(lambda:limit.begin('y'),BudgetError)
        self.no(lambda:SyntheticLedger(Path('/tmp')/'ledger_prohibido.json',10,'inventado'))
        self.no(lambda:SyntheticLedger('../ledger_prohibido.json',10,'inventado'))

    def real_process_termination_invented_worker(self):
        rel=self.folder.relative_to(BASE)
        l=SyntheticLedger(rel/'procesos'/'ledger.json',10,'inventado-procesos')
        assert run_invented(l,'ok')=='success'
        assert run_invented(l,'ok')=='resumed'
        assert run_invented(l,'infra','infrastructure')=='infrastructure'
        assert run_invented(l,'infra','success')=='success'
        assert run_invented(l,'numerico','numerical')=='numerical'
        self.no(lambda:run_invented(l,'numerico','success'))
        start=time.monotonic()
        assert run_invented(l,'terminacion','wait',timeout=0.1)=='timeout'
        assert time.monotonic()-start<2
        assert l.state['used']>0 and not any(r['status']=='pending' for r in l.state['attempts'])
        self.no(lambda:run_invented(l,'x','real'))

def run_suite(label='cli'):
    # Verificar entorno de nuevo antes de cada corrida y antes de cualquier fit.
    from preflight import environment
    environment()
    BASE.mkdir(parents=True,exist_ok=True)
    i=1
    while (BASE/f'{label}_{i:03d}').exists(): i+=1
    folder=safe_path(BASE,f'{label}_{i:03d}'); folder.mkdir()
    suite=Suite(folder)
    names=[name for name in Suite.__dict__ if name not in ('__init__','factory','no') and not name.startswith('_')]
    results=[]
    for name in names:
        started=time.monotonic()
        try:
            getattr(suite,name)(); status='aprobado'; error=None
        except Exception:
            status='fallo'; error=traceback.format_exc()
        results.append({'control':name,'estado':status,'seconds':time.monotonic()-started,'error':error})
    report={'aprobado':all(r['estado']=='aprobado' for r in results),'grupos':len(results),
            'pruebas':results,'fits_inventados':suite.synthetic_fits,'fits_panel_real':0,
            'controles_negativos':suite.negative_checks,'modelos_cargados':0,'seed':SEED,
            'presupuesto_real_iniciado':False,'artefactos':str(folder.relative_to(HERE)),
            'huellas_fuentes':{p.name:digest(p) for p in HERE.glob('*.py')}}
    report_path=HERE/'resultados'/f'CONTROLES_{label}_{i:03d}.json'
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('aprobado','grupos','fits_inventados','fits_panel_real','controles_negativos','artefactos')},ensure_ascii=False))
    if not report['aprobado']:
        for r in results:
            if r['estado']=='fallo': print(r['control'],r['error'])
        raise RuntimeError(f'Controles fallidos; evidencia preservada {report_path}')
    return report,report_path

if __name__=='__main__':
    run_suite()
