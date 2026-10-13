"""Activación explícita etapa2; no modifica fuentes/congelación etapa1."""
from pathlib import Path
ROOT=Path(__file__).absolute().parents[3]
E1=ROOT/'experimentos_temporales_objetivo3_v1/etapa1/fuentes'
E2=Path(__file__).parent

def escribir(name,text):
    p=E2/name
    with p.open('x') as f:f.write(text)

s=(E1/'seguridad.py').read_text().replace("E1 = OWN / 'etapa1'","E1 = OWN / 'etapa2'")
s=s.replace("base=E1):","base=E1):").replace("p = destino(path, TEST)","p = destino(path, E1)").replace("tmp = destino(p.with_suffix(p.suffix + '.tmp'), TEST)","tmp = destino(p.with_suffix(p.suffix + '.tmp'), E1)").replace("destino(p, TEST)","destino(p, E1)")
escribir('seguridad.py',s)
s=(E1/'comun.py').read_text().replace('ajustar_inventado','ajustar_autorizado')
s=s.replace("contexto.get('origen') != 'inventado' or train.attrs.get('origen') != 'inventado'", "contexto.get('origen') != 'recencia_h2' or train.attrs.get('origen') != 'recencia_h2'")
s=s.replace("Etapa1 permite exclusivamente ajustes inventados","Etapa2 exige autorización recencia_h2")
s=s.replace("dict(origen='inventado',contexto=contexto,pesos=meta,id=c['id'],","dict(origen='recencia_h2',contexto=contexto,pesos=meta,id=c['id'],X=X.tolist(),y=y.tolist(),")
escribir('comun.py',s)
s=(E1/'worker.py').read_text().split('\ndef prueba_hijo')[0].replace('ajustar_inventado','ajustar_autorizado')
escribir('worker.py',s)
s=(E1/'orquestacion.py').read_text().split('\ndef ventana_inventada')[0]
s=s.replace("'inventado'","'recencia_h2'")
escribir('particiones.py',s)
