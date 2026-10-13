"""Ejecución serial única. Ledger durable antes/después de cada proceso."""
from infra import *
from diseno import metrics,select
import subprocess, sys, signal, pandas as pd
LEDGER=HERE/'piloto/ledger.json'
def new_identity(identity,seen):check(identity not in seen,'reuso ID/contexto')
def retry_allowed(classification,used):
    check(classification=='infrastructure' and used==0,'retry no autorizado')
class Pilot:
    def __init__(self):
        check(not LEDGER.exists(),'piloto ya iniciado o cerrado')
        self.l=dict(status='abierto',start_epoch=START,started_epoch=time.time(),pending=None,originals=[],repetitions=[],attempts=[],retries_used=0,stop_new_fits_seconds=5400,max_total_seconds=7200)
        self.process=None;self.flush()
    def flush(self):save(LEDGER,self.l)
    def close(self,status,reason=None):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
        self.l.update(status=status,end_epoch=time.time(),reason=reason,saldo_reutilizable=False)
        self.l['elapsed_seconds']=self.l['end_epoch']-START
        # pendiente se conserva si no hay medición terminal comprobable
        self.flush()
    def fit(self,identity,c,repeat=False):
        kind='repetitions' if repeat else 'originals'
        new_identity(identity,self.l[kind]);check(not repeat or len(self.l[kind])<12,'max12')
        matrix=f'preflight/matrices/{identity}.json'
        output=f'piloto/{"repetitions" if repeat else "records"}/{identity}.json'
        request=f'piloto/requests/{identity}{"_repeat" if repeat else ""}.json'
        save(HERE/request,dict(candidate=c,matrix_file=matrix,output_file=output))
        for trial in range(2):
            deadline(True);start=time.time();mono=time.monotonic()
            attempt=dict(identity=identity,repeat=repeat,trial=trial,start_epoch=start,end_epoch=None,duration_seconds=None,status='pending',process_terminated=False)
            self.l['attempts'].append(attempt);self.l['pending']=dict(identity=identity,repeat=repeat,start_epoch=start);self.flush()
            # outputs logging preserved; process deadline absolute, no fits after stop
            log=HERE/f'piloto/logs/{identity}{"_repeat" if repeat else ""}_{trial}.txt';safe(log);log.parent.mkdir(parents=True,exist_ok=True)
            with log.open('w') as f:
                self.process=subprocess.Popen([sys.executable,str(HERE/'worker.py'),request],stdout=f,stderr=subprocess.STDOUT,env=os.environ.copy(),start_new_session=True)
                attempt['pid']=self.process.pid;self.flush()
                try:rc=self.process.wait(timeout=max(.01,5400-elapsed()))
                except subprocess.TimeoutExpired:
                    self.process.terminate()
                    try:self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
                    attempt.update(end_epoch=time.time(),duration_seconds=time.monotonic()-mono,status='timeout',process_terminated=True);self.l['pending']=None;self.flush();raise TimeoutError('fit detenido al límite absoluto')
            attempt.update(end_epoch=time.time(),duration_seconds=time.monotonic()-mono,returncode=rc,process_terminated=True)
            self.l['pending']=None
            if rc==0 and (HERE/output).exists():
                r=load(HERE/output);check(not r.get('failed'),'worker failed')
                attempt.update(status='complete',output_file=output,output_sha256=sha(HERE/output),matrix_sha256=sha(HERE/matrix));self.l[kind].append(identity);self.flush();self.process=None;return r
            if (HERE/output).exists() and load(HERE/output).get('failed'):
                attempt['status']='numeric_or_implementation_failed';self.flush();raise RuntimeError('Sin retry numérico/implementación: '+str(load(HERE/output)))
            attempt['status']='infrastructure_failed';self.flush()
            retry_allowed('infrastructure',self.l['retries_used']);self.l['retries_used']+=1;self.flush()
        raise RuntimeError('infraestructura no resuelta')
def run():
    deadline();s=load(HERE/'ESPECIFICACION.json');cs=s['candidates'];f=load(HERE/'CONGELACION.json')
    check(f['accepted'] and load(HERE/'preflight/ACEPTACION.json')['aprobado'],'preflight acceptance')
    for p,h in f['sha256'].items():check(sha(HERE/p)==h,'frozen '+p)
    pilot=Pilot();records={};selections={};allrows=[];policyrows=[]
    def stop(sig,frame):raise InterruptedError('señal '+str(sig))
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    def context(ctx,year):
        for c in cs:
            identity=f'{ctx}__{c["id"]}';mfile=f'preflight/matrices/{identity}.json';m=load(HERE/mfile)
            if c['family']=='persistencia' or year==2021:
                r=dict(id=c['id'],family='persistencia',params={},inputs=c['inputs'],matrix_file=mfile,matrix_sha256=sha(HERE/mfile),prediction=m['test']['persistence'],warnings=[],reason='2021 fijo sin fit' if year==2021 else 'persistencia sin fit')
                save(HERE/f'piloto/records/{identity}.json',r)
            else:r=pilot.fit(identity,c)
            records[identity]=r
            for k,y,p in zip(m['test']['keys'],m['test']['y'],r['prediction']):allrows.append(dict(context=ctx,id=c['id'],**k,observado=y,prediccion=p,error=p-y))
    try:
        context('e2021',2021)
        for policy in s['policies']:
            id='persistencia';r=records['e2021__'+id];m=load(HERE/r['matrix_file'])
            save(HERE/f'piloto/copias/{policy}_2021.json',dict(id=id,record_sha256=sha(HERE/'piloto/records/e2021__persistencia.json'),matrix_sha256=r['matrix_sha256']))
            for k,y,p in zip(m['test']['keys'],m['test']['y'],r['prediction']):policyrows.append(dict(policy=policy,id=id,**k,observado=y,prediccion=p,error=p-y))
        for outer in range(2022,2026):
            for inner in range(2021,outer):context(f'i{outer}_{inner}',inner)
            scores={}
            for c in cs:
                y=[];p=[]
                for inner in range(2021,outer):
                    r=records[f'i{outer}_{inner}__{c["id"]}'];m=load(HERE/r['matrix_file']);y+=m['test']['y'];p+=r['prediction']
                scores[c['id']]=metrics(y,p)
            chosen={policy:select(scores,cs,ids) for policy,ids in s['policies'].items()}
            sel=dict(scores=scores,chosen=chosen,sealed_epoch=time.time(),inner_years=list(range(2021,outer)))
            save(HERE/f'piloto/selecciones/{outer}.json',sel);selections[str(outer)]={**sel,'file_sha256':sha(HERE/f'piloto/selecciones/{outer}.json')};save(HERE/'piloto/SELECCIONES.json',selections)
            context(f'e{outer}',outer)
            for id in sorted(set(chosen.values()),key=lambda id:next(c['order'] for c in cs if c['id']==id)):
                c=next(c for c in cs if c['id']==id)
                if c['family']=='persistencia':continue
                identity=f'e{outer}__{id}';rep=pilot.fit(identity,c,True)
                import numpy as np
                check(np.allclose(rep['prediction'],records[identity]['prediction'],atol=1e-10,rtol=0),'repetición discordante')
            for policy,id in chosen.items():
                identity=f'e{outer}__{id}';r=records[identity];m=load(HERE/r['matrix_file'])
                save(HERE/f'piloto/copias/{policy}_{outer}.json',dict(id=id,record_sha256=sha(HERE/f'piloto/records/{identity}.json'),matrix_sha256=r['matrix_sha256']))
                for k,y,p in zip(m['test']['keys'],m['test']['y'],r['prediction']):policyrows.append(dict(policy=policy,id=id,**k,observado=y,prediccion=p,error=p-y))
            print(json.dumps(dict(externo=outer,fits=len(pilot.l['originals']),repeticiones=len(pilot.l['repetitions']),elapsed_seconds=elapsed())),flush=True)
        # orden de CSV verificable independiente, internas primero y externas después
        allrows.sort(key=lambda r:([f'i{o}_{i}' for o in range(2022,2026) for i in range(2021,o)]+[f'e{y}' for y in range(2021,2026)]).index(r['context'])*21+next(c['order'] for c in cs if c['id']==r['id']))
        csv_save(HERE/'piloto/PREDICCIONES.csv',pd.DataFrame(allrows));csv_save(HERE/'piloto/POLITICAS.csv',pd.DataFrame(policyrows))
        check(len(pilot.l['originals'])==200 and len(allrows)==10395 and len(policyrows)==495,'cobertura terminal')
        pilot.close('cerrado_completo')
    except BaseException as e:
        pilot.close('cerrado_incompleto',str(e));raise
if __name__=='__main__':run()
