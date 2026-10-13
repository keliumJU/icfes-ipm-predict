"""Prueba del runner real con tareas inventadas, sin ningún sklearn.fit."""
from comun import *
import contextlib,io,signal,time,threading
import numpy as np
def flow_tests():
    from motor import build_panel
    source=(HERE/'runner.py').read_text();spec=load(HERE/'ESPECIFICACION_V6.json');codes=[f'{i:02d}' for i in range(33)]
    p=build_panel({y:np.full(33,200.) for y in spec['years']},codes);summaries=[]
    def scenario(force=None,reuse=False):
        ns={'__name__':'ensayo_flujo','__file__':str(HERE/'runner.py')};exec(compile(source,str(HERE/'runner.py'),'exec'),ns)
        tasks=[];writes={};cache={}
        class FakeLedger:
            def __init__(self,*a,**kw):self.state=dict(fits_started=0,statistical_estimates=0,elapsed_seconds=0,events=[])
            def task(self,name,req):
                cand=req['candidate'];ctx=req['context'];key=(ctx['year'],cand['id'])
                if reuse and name.startswith('interno') and key in cache:return cache[key]
                check(name not in [t[0] for t in tasks],'identificador duplicado')
                eligible=bool(ctx['eligible_years']);f=len(cand['components']) if eligible else 0;s=int(eligible and cand['family'] in ['nivel_territorial','nivel_comun'])
                out=dict(context=ctx,prediction=ctx['previous_score'].copy(),predicted_delta=[0.]*33,fits=f,statistical_estimates=s,metadata={},job_id=name)
                self.state['fits_started']+=f;self.state['statistical_estimates']+=s;self.state['events'].append(dict(name=name));tasks.append((name,req,out));cache[key]=out;return out
            def close(self,*a):pass
        original_load=ns['load']
        ns.update(Ledger=FakeLedger,panel=lambda:p,environment=lambda:None,conservation=lambda:None,defaults=lambda:None,save=lambda q,v:writes.update({str(q):v}),writecsv=lambda q,v:writes.update({str(q):v}))
        # Freeze y aceptación ficticios son entradas explícitas del ensayo, nunca escribirlos.
        ns['load']=lambda q: {'sha256':{}} if str(q).endswith('CONGELACION.json') else {'completa':True} if str(q).endswith('ACEPTACION.json') else original_load(q)
        if force:
            old=ns['select']
            def selected(records):r=old(records);r['winner']=force;return r
            ns['select']=selected
        with contextlib.redirect_stdout(io.StringIO()):ns['run']()
        inf=sum(t[2]['fits'] for t in tasks if t[0].startswith('interno_'));exf=sum(t[2]['fits'] for t in tasks if t[0].startswith('externo_'));rep=sum(t[2]['fits'] for t in tasks if t[0].startswith('check_'))
        inc=sum(t[2]['statistical_estimates'] for t in tasks if t[0].startswith('interno_'));exc=sum(t[2]['statistical_estimates'] for t in tasks if t[0].startswith('externo_'));rc=sum(t[2]['statistical_estimates'] for t in tasks if t[0].startswith('check_'))
        check((inf,exf,inc,exc)==(192,128,60,40),'192/128/60/40')
        expected={'internas_originales.csv':12870,'internas_unicas.csv':5148,'externas.csv':6600,'selecciones.csv':156,'linaje.csv':12870}
        for name,count in expected.items():check(len(writes[str(HERE/'fase2/piloto'/name)])==count,'cobertura '+name)
        for name,req,out in tasks:
            if name.startswith('interno'):check(req['validation']<req['external'] and out['job_id']==name,'ventana/identidad propia')
        return dict(internal_fits=inf,external_fits=exf,repeat_fits=rep,internal_constants=inc,external_constants=exc,repeat_constants=rc,internal_jobs=sum(t[0].startswith('interno') for t in tasks),coverage=expected)
    summaries.append(scenario())
    z=scenario('comun_correccion_qr_a0p0_all');check(z['repeat_fits']==8,'cota repetición8');summaries.append(z)
    z=scenario('nivel_median_all');check(z['repeat_constants']==4,'cota constante104');summaries.append(z)
    try:scenario(reuse=True)
    except AssertionError as e:check('ajustes independientes' in str(e),'rechazo por reuso específico')
    else:raise AssertionError('runner aceptó reuso prohibido')
    return dict(aprobado=True,scenarios=summaries,negative_reuse_rejected=True,real_fits=0,synthetic_sklearn_fits=0)
def termination_test():
    from runner import Ledger
    l=Ledger(HERE/'fase1/fixtures/ledger_signal',20)
    killer=threading.Timer(.15,lambda:os.kill(os.getpid(),signal.SIGINT));killer.start()
    try:l.task('cancelado',dict(test_sleep=10))
    except KeyboardInterrupt:pass
    else:raise AssertionError('señal no interrumpió')
    finally:killer.join()
    check(l.state['pending'] is None and l.state['events'][0]['terminated'] and l.state['events'][0]['wait_completed'] and l.state['events'][0]['interrupted'],'terminación durable')
    check(l.state['retries']==0,'cancelación no es retry');l.close(False,'interrupción inventada medida')
    return dict(aprobado=True,worker_pid=l.state['events'][0]['pid'],wait_completed=True,pending=None,elapsed_seconds=l.state['elapsed_seconds'],retry=0)
def execute_tests():
    result=dict(aprobado=True,flow=flow_tests(),termination=termination_test());save(HERE/'fase1/PRUEBAS_EJECUCION.json',result);return result
