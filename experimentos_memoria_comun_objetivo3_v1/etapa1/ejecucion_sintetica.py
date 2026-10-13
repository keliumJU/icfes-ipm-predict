"""Controles de ejecución SOLO sintéticos. No ledger operativo iniciado.

Protocolo de estados destinado a ensayarse antes de un futuro runner real.
El runner aquí solo admite un worker inventado fijo; no carga panel/modelos.
"""
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
import time
from integridad import safe_path,digest
from motor import IntegrityError

BASE=Path(__file__).resolve().parent/'resultados'/'sinteticos'

class BudgetError(RuntimeError): pass
class InfrastructureFailure(RuntimeError): pass

def atomic_json(path,data):
    path=Path(path); tmp=path.with_name(path.name+'.tmp')
    safe_path(path.parent,tmp.name)
    with tmp.open('w') as f:
        json.dump(data,f,ensure_ascii=False,indent=2,allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

class SyntheticLedger:
    def __init__(self, relative, limit, context):
        self.path=safe_path(BASE,relative)
        if not isinstance(limit,(int,float)) or limit<=0: raise IntegrityError('Límite inválido')
        self.path.parent.mkdir(parents=True,exist_ok=True)
        if self.path.exists():
            self.state=json.loads(self.path.read_text())
            if self.state['context']!=context or self.state['limit']!=limit or self.state['synthetic'] is not True:
                raise IntegrityError('Contexto/límite de reanudación diferente')
            self.validate()
        else:
            self.state={'synthetic':True,'context':context,'limit':limit,'used':0.0,'attempts':[]}
            self.save()

    def save(self):
        # Preservar estados anteriores; nunca reiniciar saldo.
        history=safe_path(self.path.parent,'historia')
        history.mkdir(exist_ok=True)
        n=len(list(history.glob('*.json')))
        snapshot=safe_path(history,f'{n:04d}.json')
        if snapshot.exists(): raise IntegrityError('Snapshot existente')
        atomic_json(snapshot,self.state); atomic_json(self.path,self.state)

    def validate(self):
        a=self.state['attempts']
        if self.state['used']<0 or self.state['used']>self.state['limit']:
            raise IntegrityError('Consumo inválido')
        if self.state['used']!=sum(r.get('seconds',0) for r in a):
            raise IntegrityError('Consumo no coincide con intentos')
        for rec in a:
            if rec['status']=='success':
                p=safe_path(self.path.parent,rec['artifact'])
                if not p.exists() or digest(p)!=rec['sha256']: raise IntegrityError('Artefacto reanudado corrupto')
            if rec['status']=='pending':
                # Caída sin tiempo: agotar TODO saldo conservadoramente.
                rec['status']='unknown_crash'; rec['seconds']=self.state['limit']-self.state['used']
                self.state['used']=self.state['limit']; self.save()
                raise BudgetError('Caída pendiente sin tiempo: saldo agotado')

    def prior(self,job):
        return [r for r in self.state['attempts'] if r['job']==job]

    def begin(self,job):
        if any(r['status']=='pending' for r in self.state['attempts']): raise IntegrityError('Solo serial')
        prior=self.prior(job)
        if any(r['status']=='success' for r in prior): return False
        if any(r['status']=='numerical' for r in prior): raise IntegrityError('Numérico inelegible; no retry')
        if len(prior)>=2: raise InfrastructureFailure('Máximo un retry')
        if self.state['used']>=self.state['limit']: raise BudgetError('Sin saldo')
        self.state['attempts'].append({'job':job,'status':'pending','attempt':len(prior)+1})
        self.save(); return True

    def finish(self,job,status,seconds,artifact=None):
        if status not in ('success','infrastructure','numerical','timeout'): raise IntegrityError('Estado inválido')
        rec=self.state['attempts'][-1]
        if rec['job']!=job or rec['status']!='pending': raise IntegrityError('No pendiente')
        if not isinstance(seconds,(int,float)) or not 0<=seconds<float('inf'): raise IntegrityError('Tiempo inválido')
        charged=min(seconds,self.state['limit']-self.state['used'])
        rec.update(status=status,seconds=charged,elapsed_measured=seconds)
        if seconds>=self.state['limit']-self.state['used']: rec['status']='timeout'
        if rec['status']=='success':
            p=safe_path(self.path.parent,artifact)
            if not p.is_file(): raise IntegrityError('Artefacto obligatorio')
            rec.update(artifact=artifact,sha256=digest(p))
        self.state['used']+=charged; self.save()

def run_invented(ledger,job,mode='success',timeout=1.0):
    if mode not in ('success','infrastructure','numerical','wait'): raise IntegrityError('Worker solo inventado')
    if not ledger.begin(job): return 'resumed'
    # Incluye arranque/proceso/comunicación. POSIX grupo termina descendientes.
    start=time.monotonic()
    available=ledger.state['limit']-ledger.state['used']
    worker=Path(__file__).resolve().parent/'worker_inventado.py'
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    proc=subprocess.Popen([sys.executable,str(worker),mode],stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          env=env,start_new_session=True)
    status='infrastructure'; output=''
    try:
        out,err=proc.communicate(timeout=min(timeout,available))
        output=out.decode()
        status={0:'success',2:'numerical'}.get(proc.returncode,'infrastructure')
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGTERM)
        try: proc.communicate(timeout=0.2)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL); proc.communicate()
        status='timeout'
    elapsed=time.monotonic()-start
    artifact=None
    if status=='success':
        artifact=f'{job}_{len(ledger.state["attempts"])}.txt'
        p=safe_path(ledger.path.parent,artifact); p.write_text(output)
    ledger.finish(job,status,elapsed,artifact)
    if proc.poll() is None: raise IntegrityError('Proceso sobreviviente')
    return status
