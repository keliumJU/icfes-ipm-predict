"""Ledger propio persistente. Pipeline entero, arranque y comunicación presupuestados."""
import json,time,multiprocessing as mp,os
from pathlib import Path
from worker import ejecutar
E2=Path(__file__).resolve().parents[1]

def guardar(path,data):
    path=Path(path).resolve()
    if not path.is_relative_to(E2):raise ValueError('ledger fuera de etapa2')
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n');os.replace(temp,path)

class Presupuesto:
    def __init__(self,path,limit=7200):
        self.path=Path(path).resolve();self.limit=limit;self.checkpoint=lambda:None;self.recovered=False
        if not self.path.is_relative_to(E2):raise ValueError('ledger fuera etapa2')
        if self.path.exists():
            self.data=json.loads(self.path.read_text());assert self.data['limite']==limit,'no ampliar/reiniciar'
        else:self.data=dict(limite=limit,consumido=0.,pendiente=False,ajustes=[]);guardar(self.path,self.data)
        if self.data['pendiente']:
            pending=self.data['pendiente'];self.data['ajustes'].append(dict(etiqueta=pending['etiqueta'],estado='interrupcion_no_medida',segundos=limit-self.data['consumido']))
            self.data.update(consumido=limit,pendiente=False);guardar(self.path,self.data);self.recovered=True
    def ajustar(self,label,estimator,X,y,executor=None):
        if self.data['consumido']>=self.limit:raise TimeoutError('sin saldo; no intento ficticio')
        assert not self.data['pendiente'] and label not in [r['etiqueta'] for r in self.data['ajustes']]
        remaining=self.limit-self.data['consumido'];start=time.monotonic();proc=None;parent=None
        self.data['pendiente']=dict(etiqueta=label,instante=time.time(),saldo=remaining)
        guardar(self.path,self.data);self.checkpoint();state='error';duration=None
        try:
            if executor:
                result,duration=executor(estimator,X,y,remaining)
                notes=[]
            else:
                ctx=mp.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
                proc=ctx.Process(target=ejecutar,args=(child,estimator,X,y));proc.start();child.close()
                available=remaining-(time.monotonic()-start)
                if available<=0 or not parent.poll(available):raise TimeoutError('límite serial')
                response=parent.recv();proc.join(timeout=max(0.,remaining-(time.monotonic()-start)))
                if proc.is_alive():raise TimeoutError('worker no terminó en saldo')
                if response[0]=='error':
                    cls,message,tb=response[1:]
                    if cls in ('ValueError','FloatingPointError','OverflowError','LinAlgError'):raise ValueError(cls+': '+message+'\n'+tb)
                    if cls in ('OSError','EOFError','BrokenPipeError','ConnectionError'):raise OSError(cls+': '+message)
                    raise RuntimeError(cls+': '+message+'\n'+tb)
                result,notes=response[1:]
            if duration is None:duration=time.monotonic()-start
            if duration>=remaining:raise TimeoutError('límite inclusivo')
            state='ok';return result,notes
        except TimeoutError:state='limite';duration=remaining;raise
        finally:
            if proc is not None and proc.is_alive():
                proc.terminate();proc.join(timeout=1)
                if proc.is_alive():proc.kill();proc.join(timeout=1)
                assert not proc.is_alive(),'proceso restante'
            if parent is not None:parent.close()
            if duration is None:duration=time.monotonic()-start
            duration=min(remaining,max(0.,duration))
            self.data['ajustes'].append(dict(etiqueta=label,estado=state,segundos=duration))
            self.data['consumido']=min(self.limit,self.data['consumido']+duration);self.data['pendiente']=False
            guardar(self.path,self.data);self.checkpoint()
