"""Runner serial terminable; modelos exclusivamente propios, ledger persistente."""
import math,time,multiprocessing as mp,traceback
import joblib
from seguridad import OUT,destino,checkpoint,leer,sha
from worker import ejecutar
class FalloNumerico(ValueError):pass
class FalloControl(RuntimeError):pass

def proceso(c,train,context,saldo):
    start=time.monotonic();ctx=mp.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
    proc=ctx.Process(target=ejecutar,args=(child,c,train,context))
    try:
        proc.start();child.close()
        if not parent.poll(max(0.,saldo-(time.monotonic()-start))):raise TimeoutError('Worker agotó saldo')
        response=parent.recv();proc.join(timeout=max(0.,saldo-(time.monotonic()-start)))
        if proc.is_alive() or time.monotonic()-start>=saldo:raise TimeoutError('Comunicación/terminación fuera de saldo')
        if response[0]=='error':
            cls,message,tb=response[1:]
            if cls in ('OSError','EOFError','BrokenPipeError','ConnectionError'):raise OSError(message)
            if cls in ('ValueError','FloatingPointError','OverflowError','LinAlgError'):raise FalloNumerico(message+'\n'+tb)
            raise FalloControl(cls+': '+message+'\n'+tb)
        return response[1]
    finally:
        if proc.pid is not None:
            if proc.is_alive():proc.terminate();proc.join(timeout=1.)
            if proc.is_alive():proc.kill();proc.join(timeout=1.)
            if proc.is_alive():raise FalloControl('Hijo restante')
        child.close();parent.close()
class Presupuesto:
    def __init__(self,contexto):
        self.path=destino(OUT/'ledger.json');self.limit=7200.;self.context=contexto
        if self.path.exists():self.data=leer(self.path)
        else:
            self.data=dict(origen='recencia_h2',contexto=contexto,limite=7200.,consumido=0.,pendiente=False,ajustes=[])
            checkpoint(self.path,self.data)
        d=self.data
        if d.get('contexto')!=contexto or d.get('limite')!=7200. or not isinstance(d.get('ajustes'),list) or not math.isfinite(d['consumido']) or not 0<=d['consumido']<=7200.:raise FalloControl('Ledger/contexto corrupto')
        for r in d['ajustes']:
            if r['estado']=='ok':
                for n,h in r['artefactos'].items():
                    if sha(destino(n))!=h:raise FalloControl('Artefacto cambiado')
        if d['pendiente']:
            d['ajustes'].append(dict(etiqueta=d['pendiente']['etiqueta'],estado='interrupcion_no_medida',clase_fallo='infraestructura',segundos=7200.-d['consumido']))
            d.update(consumido=7200.,pendiente=False);checkpoint(self.path,d)
            raise TimeoutError('Interrupción sin medición agotó presupuesto conservadoramente')
    def ajustar(self,label,c,train,context):
        attempts=[r for r in self.data['ajustes'] if r['etiqueta'].startswith(label+'#')]
        for r in attempts:
            if r.get('contexto')!=context:raise FalloControl('Contexto de ajuste cambiado')
            if r['estado']=='ok':
                model=destino(OUT/'modelos'/f'{label}.joblib');meta=destino(OUT/'metadatos'/f'{label}.json')
                return joblib.load(model),leer(meta)
            if r['clase_fallo']=='numerico_convergencia':raise FalloNumerico(r['razon'])
        if len(attempts)>=2:raise OSError('Segundo fallo infraestructura; detener')
        for attempt in range(len(attempts)+1,3):
            saldo=self.limit-self.data['consumido']
            if saldo<=0:raise TimeoutError('Sin presupuesto')
            tag=label+'#'+str(attempt);start=time.monotonic()
            self.data['pendiente']=dict(etiqueta=tag,contexto=context,saldo=saldo);checkpoint(self.path,self.data)
            state,kind,reason,art='error',None,None,{}
            try:
                result=proceso(c,train,context,saldo);model,meta=result
                p=destino(OUT/'modelos'/f'{label}.joblib');p.parent.mkdir(parents=True,exist_ok=True)
                if p.exists():raise FalloControl('Artefacto huérfano; sin sobrescribir')
                joblib.dump(model,p)
                m=destino(OUT/'metadatos'/f'{label}.json');checkpoint(m,meta)
                art={str(p):sha(p),str(m):sha(m)}
                if time.monotonic()-start>=saldo:raise TimeoutError('Límite inclusivo')
                state='ok';return result
            except TimeoutError as e:state,kind,reason='limite','limite',str(e);raise
            except (OSError,EOFError,ConnectionError) as e:
                kind,reason='infraestructura',str(e)
                if attempt==2:raise
            except FalloNumerico as e:kind,reason='numerico_convergencia',str(e);raise
            except BaseException as e:kind,reason='control_indispensable',str(e);raise
            finally:
                elapsed=time.monotonic()-start
                duration=saldo if state=='limite' else min(saldo,max(0.,elapsed))
                self.data['ajustes'].append(dict(etiqueta=tag,estado=state,clase_fallo=kind,razon=reason,segundos=duration,contexto=context,artefactos=art))
                self.data.update(consumido=min(7200.,self.data['consumido']+duration),pendiente=False)
                checkpoint(self.path,self.data)
                print(f'{label} {state}: {duration:.3f}s; total {self.data["consumido"]:.3f}/7200s',flush=True)
