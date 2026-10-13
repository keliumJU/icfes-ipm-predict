"""Motor serial inventado. Contrato futuro 7200s/378, sin ledger operativo real."""
import math
import multiprocessing as mp
import time
from seguridad import TEST, destino, checkpoint, leer, sha
from worker import ejecutar


def proceso(target,args,saldo):
    start = time.monotonic()
    ctx = mp.get_context('spawn')
    parent,child = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=target,args=(child,*args))
    try:
        proc.start()
        child.close()
        available = saldo-(time.monotonic()-start)
        if available <= 0 or not parent.poll(available):
            raise TimeoutError('Worker agotó saldo inclusivo')
        response = parent.recv()
        proc.join(timeout=max(0.,saldo-(time.monotonic()-start)))
        if proc.is_alive() or time.monotonic()-start >= saldo:
            raise TimeoutError('Comunicación/terminación fuera de saldo')
        if response[0] == 'error':
            cls,message,tb = response[1:]
            if cls in ('OSError','EOFError','BrokenPipeError','ConnectionError'):
                raise OSError(cls+': '+message)
            if cls in ('ValueError','FloatingPointError','OverflowError','LinAlgError'):
                raise ValueError(cls+': '+message+'\n'+tb)
            raise RuntimeError(cls+': '+message+'\n'+tb)
        return response[1]
    finally:
        if proc.pid is not None:
            if proc.is_alive():
                proc.terminate()
                proc.join(timeout=1.)
            if proc.is_alive():
                proc.kill()
                proc.join(timeout=1.)
            if proc.is_alive():
                raise RuntimeError('Hijo restante: control indispensable')
        child.close()
        parent.close()


class PresupuestoInventado:
    def __init__(self,path,contexto,limit):
        self.path = destino(path,TEST)
        if not math.isfinite(limit) or limit <= 0 or contexto.get('origen') != 'inventado':
            raise ValueError('Solo presupuesto/contexto inventado positivo')
        self.limit = limit
        if self.path.exists():
            self.data = leer(self.path)
            if self.data['limite'] != limit or self.data['contexto'] != contexto:
                raise ValueError('No reiniciar/ampliar; contexto diferente')
        else:
            self.data = dict(origen='inventado',contexto=contexto,limite=limit,consumido=0.,pendiente=False,ajustes=[])
            checkpoint(self.path,self.data)
        if (self.data.get('origen') != 'inventado' or not isinstance(self.data.get('ajustes'),list)
                or not isinstance(self.data.get('consumido'),(int,float))
                or not math.isfinite(self.data['consumido']) or not 0 <= self.data['consumido'] <= limit):
            raise ValueError('Estado inventado corrupto; detener sin rescate')
        if self.data['pendiente']:
            pending = self.data['pendiente']
            self.data['ajustes'].append(dict(etiqueta=pending['etiqueta'],estado='interrupcion_no_medida',
                clase_fallo='infraestructura',segundos=limit-self.data['consumido']))
            self.data.update(consumido=limit,pendiente=False)
            checkpoint(self.path,self.data)

    def ajustar(self,label,c,train,contexto,executor=None):
        if train.attrs.get('origen') != 'inventado' or contexto.get('origen') != 'inventado':
            raise ValueError('Panel real prohibido en etapa1')
        attempts = [r for r in self.data['ajustes'] if r['etiqueta'].startswith(label+'#')]
        if any(r['estado'] == 'ok' for r in attempts):
            raise ValueError('Completo: comprobar contexto/artefactos antes de reutilizar')
        if any(r['clase_fallo'] == 'numerico_convergencia' for r in attempts):
            raise ValueError('Inelegible persistente, sin retry')
        if len(attempts) >= 2:
            raise OSError('Segundo fallo de infraestructura: detener')
        for attempt in range(len(attempts)+1,3):
            if self.data['consumido'] >= self.limit:
                raise TimeoutError('Sin saldo; no fabricar intento')
            remaining = self.limit-self.data['consumido']
            tag = label+'#'+str(attempt)
            start = time.monotonic()
            self.data['pendiente'] = dict(etiqueta=tag,saldo=remaining)
            checkpoint(self.path,self.data)
            state,kind,duration = 'error',None,None
            try:
                if executor is None:
                    result = proceso(ejecutar,(c,train,contexto),remaining)
                    duration = time.monotonic()-start
                else:
                    result,declared = executor(c,train,contexto,remaining)
                    if not math.isfinite(declared) or declared < 0:
                        raise ValueError('Tiempo inventado inválido')
                    duration = max(declared,time.monotonic()-start)
                if duration >= remaining:
                    raise TimeoutError('Límite inclusivo')
                state = 'ok'
                return result
            except TimeoutError:
                state,kind,duration = 'limite','limite',remaining
                raise
            except (OSError,EOFError,ConnectionError):
                kind = 'infraestructura'
                if attempt == 2:
                    raise
            except Exception:
                kind = 'numerico_convergencia'
                raise
            finally:
                if duration is None:
                    duration = time.monotonic()-start
                duration = min(remaining,max(0.,duration))
                self.data['ajustes'].append(dict(etiqueta=tag,estado=state,clase_fallo=kind,segundos=duration))
                self.data['consumido'] = min(self.limit,self.data['consumido']+duration)
                self.data['pendiente'] = False
                checkpoint(self.path,self.data)

    def reanudar_completo(self,label,contexto,artefactos):
        if contexto != self.data['contexto'] or not artefactos:
            raise ValueError('Contexto/artefactos incompletos')
        attempts = [r for r in self.data['ajustes'] if r['etiqueta'].startswith(label+'#')]
        if len(attempts)>2 or not any(r['estado']=='ok' for r in attempts):
            raise ValueError('Sin ajuste completo verificable')
        for path,h in artefactos.items():
            p = destino(path,TEST)
            if sha(p) != h:
                raise ValueError('Artefacto cambiado')
        return True
