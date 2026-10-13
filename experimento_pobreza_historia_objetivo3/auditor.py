"""Auditor independiente. Solo JSON/CSV y aritmética; nunca sklearn, fits o modelos.

No importa diseño, selector operativo, constructores ni ejecutores.
"""
from infra import HERE, ROOT, sha, load, save, check, START
import math, json, ast, numpy as np, pandas as pd
def measure(y,p):
    e=[float(p[i])-float(y[i]) for i in range(len(y))];n=len(e);check(n>0,'audit n')
    return {'n':n,'MAE':math.fsum(map(abs,e))/n,'RMSE':math.sqrt(math.fsum(v*v for v in e)/n),'sesgo':math.fsum(e)/n}
def choice(rows,ids,cs):
    a=[(c,rows[c['id']]) for c in cs if c['id'] in ids]
    cutoff=min(r['MAE'] for c,r in a)+.1
    b=[(c,r) for c,r in a if r['MAE']<=cutoff]
    cutoff2=min(r['RMSE'] for c,r in b)+.1
    return sorted((c for c,r in b if r['RMSE']<=cutoff2),key=lambda c:(len(c['inputs']),c['order']))[0]['id']
def exact(a,b,label):check(np.array_equal(np.asarray(a),np.asarray(b),equal_nan=True),'exact '+label)
def near(a,b,label,tol=1e-10):check(np.allclose(np.asarray(a),np.asarray(b),atol=tol,rtol=0),'near '+label)
def csv_exact(path,rows):
    a=pd.DataFrame(rows);b=pd.read_csv(path,float_precision='round_trip',dtype={'codigo_departamento':str})
    check(a.shape==b.shape and list(a.columns)==list(b.columns),'csv shape')
    for c in a:
        if pd.api.types.is_numeric_dtype(a[c]):exact(a[c].values,b[c].values,'CSV '+c)
        else:check(a[c].astype(str).tolist()==b[c].astype(str).tolist(),'CSV strings')
def predict(record,matrix):
    if record['family']=='persistencia':return matrix['test']['persistence']
    z=(np.array(matrix['test']['X'],dtype=float)-record['scaler']['mean'])/record['scaler']['scale']
    if record['family']=='Ridge':
        # una acumulación reproducible, tolerancia absoluta declarada
        return [math.fsum(float(x)*float(w) for x,w in zip(row,record['coef']))+record['intercept'] for row in z]
    t=record['tree'];out=[]
    for row in z.astype(np.float32):  # sklearn tree aplica float32 después de scaler
        node=0;visited=set()
        while t['children_left'][node]!=-1:
            check(node not in visited,'tree ciclo');visited.add(node)
            node=t['children_left'][node] if row[t['feature'][node]]<=t['threshold'][node] else t['children_right'][node]
        out.append(t['value'][node])
    return out
def validate_record(rec,mat,c):
    check(rec['id']==c['id'] and rec['params']==c['params'] and rec['inputs']==c['inputs'] and rec['family']==c['family'],'record spec')
    check(rec['matrix_sha256']==sha(HERE/rec['matrix_file']),'matrix binding')
    check(len(rec['prediction'])==len(mat['test']['keys'])==33,'33 prediction')
    if rec['family']!='persistencia':
        x=np.asarray(mat['train']['X']);check(len(x)>0,'train vacío')
        near(np.mean(x,axis=0),rec['scaler']['mean'],'scaler train mean')
        near(np.var(x,axis=0),rec['scaler']['var'],'scaler train var',1e-9)
        v=np.var(x,axis=0);scale=np.sqrt(v);scale[v==0]=1
        near(scale,rec['scaler']['scale'],'scaler train scale')
        check(rec['scaler']['n_samples_seen']==len(x) and rec['scaler']['params']==c['scaler'],'scaler params/n')
        check(rec['runtime_params']==c['params'] and rec['pipeline_params']=={'memory':None,'verbose':False,'transform_input':None},'defaults completos')
        if c['family']=='Ridge':check(len(rec['coef'])==len(c['inputs']),'coef len')
        else:
            t=rec['tree'];check(t['max_depth']<=2,'depth');check(all(n>=11 for n,left in zip(t['n_node_samples'],t['children_left']) if left==-1),'leaf>=11')
    near(predict(rec,mat),rec['prediction'],'reconstruction')
    check(not any(w['category'] in ['ConvergenceWarning','RuntimeWarning'] for w in rec['warnings']),'numerical warnings')
def independent_panel():
    spec=load(HERE/'ESPECIFICACION.json')
    for p,h in spec['source_hashes'].items():check(sha(ROOT/p)==h,'audit source')
    path=next(p for p in spec['source_hashes'] if 'base_analitica' in p)
    b=pd.read_csv(ROOT/path,float_precision='round_trip',dtype={'codigo_departamento':str})
    check(b.codigo_departamento.str.fullmatch(r'\d{1,2}').all(),'audit code format')
    b['codigo_departamento']=b.codigo_departamento.str.zfill(2)
    lookup={(str(r.codigo_departamento),int(r.anio)):r._asdict() for r in b.itertuples(index=False)}
    years=[2018,2019,2021,2022,2023,2024,2025];rows=[]
    for year in years[2:]:
        idx=years.index(year)
        for code in sorted(b.codigo_departamento.unique()):
            r=lookup[code,year].copy();prev=lookup[code,years[idx-1]];prev2=lookup[code,years[idx-2]]
            r.update(anio_previo=years[idx-1],anio_previo_previo=years[idx-2],puntaje_previo=prev['prom_punt_global'],puntaje_previo_previo=prev2['prom_punt_global'],cambio_previo=prev['prom_punt_global']-prev2['prom_punt_global'],cambio_observado=r['prom_punt_global']-prev['prom_punt_global'])
            rows.append(r)
    # nombres con espacios no se toman de namedtuple: reemplazar desde records fuente
    records=b.to_dict('records');lookup={(r['codigo_departamento'],r['anio']):r for r in records}
    for r in rows:
        original=lookup[r['codigo_departamento'],r['anio']]
        for key,val in original.items():r[key]=val
    return rows
def validate_matrix(mat,c,rows,evaluated):
    check(mat['evaluated_year']==evaluated,'evaluated')
    for part in ['train','test']:
        selected=[r for r in rows if (2021<=r['anio']<evaluated if part=='train' else r['anio']==evaluated)]
        actual=mat[part];check(actual['keys']==[{k:r[k] for k in ['codigo_departamento','anio']} for r in selected],'keys chronology')
        check(actual['years']==[r['anio'] for r in selected],'years')
        check(actual['inputs']==c['inputs'],'inputs')
        exact(actual['X'],[[r[k] for k in c['inputs']] for r in selected],'X')
        exact(actual['y'],[r['prom_punt_global'] for r in selected],'y')
        exact(actual['persistence'],[r['puntaje_previo'] for r in selected],'persistence')
        check(actual['history']==[{k:r[k] for k in ['anio_previo','anio_previo_previo','puntaje_previo','puntaje_previo_previo','cambio_previo']} for r in selected],'history exact')
        check(actual['units']==load(HERE/'ESPECIFICACION.json')['units'],'units')
def run(write=True):
    s=load(HERE/'ESPECIFICACION.json');cs=s['candidates'];by={c['id']:c for c in cs};rows=independent_panel()
    freeze=load(HERE/'CONGELACION.json')
    for p,h in freeze['sha256'].items():check(sha(HERE/p)==h,'freeze '+p)
    check(freeze['accepted_epoch']<load(HERE/'piloto/ledger.json')['started_epoch'],'accepted before fits')
    check(len(cs)==21 and [c['order'] for c in cs]==list(range(21)),'21 order')
    tree=ast.parse((ROOT/'protocolo/fuentes/configuracion.py').read_text())
    dim=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DIMENSIONES' for t in n.targets))
    independent_rates=[v for group in dim.values() for v in group]
    check(s['groups']['D']==independent_rates,'declared rate order independent')
    scaleparams={'copy':True,'with_mean':True,'with_std':True}
    ridgeparams={'alpha':1.,'copy_X':True,'fit_intercept':True,'max_iter':None,'positive':False,'random_state':20261010,'solver':'svd','tol':.0001}
    treeparams={'ccp_alpha':0.,'criterion':'absolute_error','max_depth':2,'max_features':None,'max_leaf_nodes':None,'min_impurity_decrease':0.,'min_samples_leaf':11,'min_samples_split':2,'min_weight_fraction_leaf':0.,'monotonic_cst':None,'random_state':20261010,'splitter':'best'}
    check(s['defaults']==dict(scaler=scaleparams,ridge=ridgeparams,tree=treeparams),'exact full defaults independent')
    wanted=['persistencia']+[f'Ridge_{g}_{a:g}' for g in ['H','I','D','HI','HD'] for a in [.1,1.,10.]]+['Arbol_'+g for g in ['H','I','D','HI','HD']]
    check([c['id'] for c in cs]==wanted,'order by group/alpha')
    for c in cs:
        if c['family']=='persistencia':check(c['inputs']==[] and c['params']=={} and c['scaler'] is None,'persistence spec')
        else:
            check(c['inputs']==s['groups'][c['group']] and c['scaler']==scaleparams,'candidate inputs/defaults')
            expected={**ridgeparams,'alpha':float(c['id'].split('_')[-1])} if c['family']=='Ridge' else treeparams
            check(c['params']==expected,'candidate exact params')
    wantedsets={'historico':['persistencia']+[f'Ridge_H_{a:g}' for a in [.1,1.,10.]],'ampliado':['persistencia']+[f'Ridge_{g}_{a:g}' for g in ['H','HI','HD'] for a in [.1,1.,10.]],'con_pobreza':[f'Ridge_{g}_{a:g}' for g in ['HI','HD'] for a in [.1,1.,10.]]}
    check(s['policies']==wantedsets,'policy candidates independent')
    expected_groups={'H':['puntaje_previo','cambio_previo'],'I':['ipm'],'D':s['groups']['D'],'HI':['puntaje_previo','cambio_previo','ipm'],'HD':['puntaje_previo','cambio_previo']+s['groups']['D']}
    check(s['groups']==expected_groups and len(s['groups']['D'])==15,'group closed')
    check(s['threshold_percent']==5 and s['primary']=='100*(MAE_historico-MAE_ampliado)/MAE_historico' and s['selector']=={'mae_tolerance':.1,'rmse_tolerance':.1,'complexity':'numero entradas','tie':'order'},'primary closed')
    led=load(HERE/'piloto/ledger.json');check(led['status']=='cerrado_completo' and led['pending'] is None,'pilot closed')
    check(led['start_epoch']==START and led['end_epoch']-START<=7200 and led['elapsed_seconds']==led['end_epoch']-START,'budget absolute')
    check(len(led['originals'])==200 and len(led['repetitions'])<=12 and len(set(led['originals']))==200 and len(set(led['repetitions']))==len(led['repetitions']),'fit counts')
    check(led['retries_used']<=1,'one retry')
    for attempt in led['attempts']:
        check(attempt['start_epoch']-START<5400 and attempt['end_epoch'] is not None and attempt['duration_seconds']>=0,'time/termination')
        check(attempt['process_terminated'] and attempt['status'] in ['complete','infrastructure_failed'],'process finished')
    check(len([a for a in led['attempts'] if a['status']=='complete'])==200+len(led['repetitions']),'attempts coverage')
    originals_expected={f'{ctx}__{c["id"]}' for ctx in ['i2023_2022','i2024_2022','i2024_2023','i2025_2022','i2025_2023','i2025_2024','e2022','e2023','e2024','e2025'] for c in cs[1:]}
    check(set(led['originals'])==originals_expected,'independent 200 contexts')
    all_predictions=[];records={};contexts=[f'i{outer}_{inner}' for outer in range(2022,2026) for inner in range(2021,outer)]+[f'e{year}' for year in range(2021,2026)]
    for context in contexts:
        year=int(context.split('_')[-1][1:] if context.startswith('e') else context.split('_')[-1])
        for c in cs:
            ident=f'{context}__{c["id"]}';rec=load(HERE/f'piloto/records/{ident}.json');mat=load(HERE/rec['matrix_file'])
            validate_matrix(mat,c,rows,year)
            effective={**c,'family':'persistencia','params':{}} if year==2021 else c
            validate_record(rec,mat,effective)
            records[ident]=rec
            for key,y,p in zip(mat['test']['keys'],mat['test']['y'],rec['prediction']):all_predictions.append(dict(context=context,id=c['id'],**key,observado=y,prediccion=p,error=p-y))
    csv_exact(HERE/'piloto/PREDICCIONES.csv',all_predictions)
    selections=load(HERE/'piloto/SELECCIONES.json');policies=[]
    for outer in range(2021,2026):
        if outer==2021: chosen={p:'persistencia' for p in s['policies']}
        else:
            scores={}
            for c in cs:
                actual=[];pred=[]
                for inner in range(2021,outer):
                    rec=records[f'i{outer}_{inner}__{c["id"]}'];mat=load(HERE/rec['matrix_file']);actual+=mat['test']['y'];pred+=rec['prediction']
                scores[c['id']]=measure(actual,pred)
            sel=selections[str(outer)];check(sel['scores']==scores,'selection scores')
            chosen={p:choice(scores,ids,cs) for p,ids in s['policies'].items()}
            check(sel['chosen']==chosen,'selection independent')
            ext=[a['start_epoch'] for a in led['attempts'] if a['identity'].startswith(f'e{outer}__')];check(sel['sealed_epoch']<min(ext),'selection sealed before external')
            check(sha(HERE/f'piloto/selecciones/{outer}.json')==sel['file_sha256'],'selection file hash')
        for policy,id in chosen.items():
            rec=records[f'e{outer}__{id}'];mat=load(HERE/rec['matrix_file'])
            copy=load(HERE/f'piloto/copias/{policy}_{outer}.json')
            check(copy['id']==id and copy['record_sha256']==sha(HERE/f'piloto/records/e{outer}__{id}.json') and copy['matrix_sha256']==rec['matrix_sha256'],'selected copy lineage')
            for key,y,p in zip(mat['test']['keys'],mat['test']['y'],rec['prediction']):policies.append(dict(policy=policy,id=id,**key,observado=y,prediccion=p,error=p-y))
    csv_exact(HERE/'piloto/POLITICAS.csv',policies)
    for ident in led['repetitions']:
        rec=load(HERE/f'piloto/repetitions/{ident}.json');mat=load(HERE/rec['matrix_file']);validate_record(rec,mat,by[rec['id']]);near(rec['prediction'],records[ident]['prediction'],'repeat prediction')
        check(ident.startswith('e') and rec['id'] in selections[ident[1:5]]['chosen'].values(),'repeat selected external')
    m={p:measure([r['observado'] for r in policies if r['policy']==p],[r['prediccion'] for r in policies if r['policy']==p]) for p in s['policies']}
    den=m['historico']['MAE'];check(math.isfinite(den) and den>0,'positive denominator')
    primary=100*(den-m['ampliado']['MAE'])/den
    result=dict(aprobado=True,fits_auditor=0,operational_imports=0,models_loaded=0,independent_selection=True,reconstructed_predictions=len(all_predictions),contexts=len(contexts),original_fits=200,repetitions=len(led['repetitions']),metrics=m,primary_percent=primary,meets_threshold=primary>=5,temporal_coverage=True,csv_exact=True,elapsed_pilot_seconds=led['elapsed_seconds'],scientific_confirmation=False)
    if write:save(HERE/'AUDITORIA.json',result)
    return result
def self_tests():
    import tempfile
    tests=[]
    def rejects(label,fn):
        try:fn()
        except AssertionError:tests.append(label);return
        raise AssertionError('auditor aceptó corrupción '+label)
    tests.append('metric_fsum');check(measure([1,2],[2,4])['MAE']==1.5,'metrics fixture')
    cs=[dict(id='a',inputs=['x'],order=0),dict(id='b',inputs=[],order=1),dict(id='c',inputs=['x'],order=2)]
    rows={'a':{'MAE':1.,'RMSE':2.},'b':{'MAE':1.1,'RMSE':2.1},'c':{'MAE':1.10001,'RMSE':1.}}
    check(choice(rows,['a','b','c'],cs)=='b','selector boundary');tests.append('selector boundary/complexity/order')
    rejects('CSV rechazo 1e-11',lambda:exact([0],[1e-11],'fixture'))
    exact([0],[0.],'int0 float0');tests.append('int0=float0')
    with tempfile.TemporaryDirectory(dir='/tmp') as d:
        p=__import__('pathlib').Path(d)/'test.csv';p.write_text('codigo_departamento,x\n05,0\n');csv_exact(p,[dict(codigo_departamento='05',x=0.)]);p.write_text('codigo_departamento,x\n05,1e-11\n');rejects('CSV corrupt real read',lambda:csv_exact(p,[dict(codigo_departamento='05',x=0.)]))
    mat={'test':{'X':[[1],[4]],'persistence':[2,3]}}
    r=dict(family='Ridge',scaler={'mean':[1],'scale':[1]},coef=[2],intercept=3)
    exact(predict(r,mat),[3,9],'ridge reconstruction');tests.append('Ridge params prediction')
    r=dict(family='Arbol',scaler={'mean':[1],'scale':[1]},tree={'children_left':[1,-1,-1],'children_right':[2,-1,-1],'feature':[0,-2,-2],'threshold':[1,-2,-2],'value':[0,2,4]})
    exact(predict(r,mat),[2,4],'tree');tests.append('tree float32 threshold')
    tests.append('no fits/imports operacional verified AST')
    source=ast.parse(__import__('pathlib').Path(__file__).read_text());check(not any(isinstance(n,(ast.Import,ast.ImportFrom)) and any(v in ast.unparse(n) for v in ['sklearn','diseno','piloto','worker']) for n in ast.walk(source)),'audit import restrictions')
    return dict(aprobado=True,tests=tests,fits=0)
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False))
