"""Controles de conservación; no carga estimadores ni ajusta modelos."""
import hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'fase5/resultados'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def guardar(nombre,obj):
    (OUT/nombre).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def inicio():
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert commit=='da48e1a4f85d206e8753fbad85b78ba2e3858b1a'
    base=sha(ROOT/'auditoria/base_analitica_departamento_anio.csv')
    assert base=='609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866'
    controles=[]
    for nombre in ['protocolo/evidencia/manifiesto_cierre.json','fase3/resultados/manifiesto_cierre.json','fase4/resultados/manifiesto_cierre.json']:
        m=json.loads((ROOT/nombre).read_text()); m=m.get('entregables_sha256',m)
        for ruta,huella in m.items():
            if ruta=='CONTINUIDAD_OBJETIVO_3.md' and not nombre.startswith('fase4'):
                controles.append({'manifiesto':nombre,'ruta':ruta,'estado':'version historica de continuidad; sustituida documentadamente por cierres posteriores'}); continue
            assert sha(ROOT/ruta)==huella,(nombre,ruta)
            controles.append({'manifiesto':nombre,'ruta':ruta,'sha256':huella,'estado':'coincide'})
    archivos=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    snapshot={p:sha(ROOT/p) for p in archivos if p and (ROOT/p).is_file()}
    guardar('integridad_inicial.json',{'commit_partida':commit,'base_sha256':base,'controles':controles,'snapshot_versionados':snapshot,'fecha_cliente':'2026-10-09','estado_git_inicial':'limpio (comprobado antes de crear fase5)'})
def cierre():
    m=json.loads((OUT/'integridad_inicial.json').read_text())
    intactos=[]
    for p,h in m['snapshot_versionados'].items():
        if p=='CONTINUIDAD_OBJETIVO_3.md': continue
        assert sha(ROOT/p)==h,p
        intactos.append(p)
    guardar('conservacion_final.json',{'archivos_previos_intactos':len(intactos),'rutas':intactos,'excepcion_intencional':['CONTINUIDAD_OBJETIVO_3.md'],'modelos_ajustados_fase5':0,'simulaciones_fase5':0})
if __name__=='__main__':
    import sys
    inicio() if '--inicio' in sys.argv else cierre()
