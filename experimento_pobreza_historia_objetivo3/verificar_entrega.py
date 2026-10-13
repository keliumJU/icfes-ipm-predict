"""Verificador de entrega propia SOLO lectura; no inicia/reabre fits ni escribe."""
from infra import *
import json, pandas as pd, nbformat
from preflight import conservation,environment
import auditor
def evidence_check():
    e=pd.read_csv(HERE/'EVIDENCIAS_TEXTO.csv',dtype=str,keep_default_na=False)
    for _,r in e.iterrows():
        check(sha(HERE/r.archivo)==r.sha256,'evidence hash')
        if r.archivo.endswith('PRIMARIO.json'):
            check(str(load(HERE/r.archivo)[r.llave])==r.valor or json.dumps(load(HERE/r.archivo)[r.llave])==r.valor,'primary evidence value')
        elif r.archivo.endswith('ESPECIFICACION.json'):
            value=load(HERE/r.archivo)
            for field in r.llave.split('.'):value=value[field]
            check(value==json.loads(r.valor),'spec evidence value')
        elif r.archivo.endswith('.csv'):
            df=pd.read_csv(HERE/r.archivo,float_precision='round_trip',dtype={'codigo_departamento':str})
            filters=r.llave.split(';');col=None
            for item in filters:
                key,value=item.split('=',1)
                if key=='col':col=value
                else:df=df[df[key].astype(str)==value]
            check(len(df)==1,'evidence unique key')
            column=col or ('id' if r.tabla=='selecciones' else None)
            check(column is not None,'evidence column')
            v=df[column].iloc[0]
            check(float(v)==float(r.valor) if col else str(v)==r.valor,'table evidence value')
        elif r.archivo.endswith('.png'):check(sha(HERE/r.archivo)==r.valor,'figure evidence')
        elif r.archivo.endswith('FECHA_LOCAL.json'):check(load(HERE/r.archivo)['fecha_local']==r.valor,'date evidence')
    return len(e)
def verify(require_manifest=True):
    environment();c=conservation();a=auditor.run(write=False)
    if require_manifest:
        m=load(HERE/'MANIFIESTO_FINAL.json')
        for n,h in m['sha256'].items():check(sha(HERE/n)==h,'manifest '+n)
        paths={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
        check(paths-set(m['exclusions'])==set(m['sha256']),'manifest inventory')
    nb=nbformat.read(HERE/'RESULTADOS.ipynb',as_version=4);nbformat.validate(nb);codes=[c for c in nb.cells if c.cell_type=='code']
    e=load(HERE/'RESULTADOS.ipynb.ejecucion.json')
    check(e['executed'] and e['new_fits']==0 and len(codes)==5 and [c.execution_count for c in codes]==[1,2,3,4,5] and all(c.outputs and not any(o.output_type=='error' for o in c.outputs) for c in codes),'notebook real')
    for k,p in [('notebook_sha256','RESULTADOS.ipynb'),('source_sha256','notebook_resultados.py'),('shared_functions_sha256','analisis.py'),('generator_sha256','generar_notebook.py')]:check(e[k]==sha(HERE/p),'notebook lineage '+k)
    ct=load(HERE/'CONTROL_TEXTO.json');check(ct['aprobado'] and ct['text_sha256']==sha(HERE/'TEXTO_OBJETIVO3_TESIS.md') and ct['evidence_sha256']==sha(HERE/'EVIDENCIAS_TEXTO.csv'),'text binding')
    n=evidence_check()
    visual=load(HERE/'resultados/REVISION_VISUAL.json');check(visual['aprobado'],'visual')
    for name,h in visual['files'].items():check(sha(HERE/'resultados/figuras'/name)==h,'visual hash')
    r=load(HERE/'resultados/PRIMARIO.json');check(r['mejora_primaria_percent']==a['primary_percent'] and r['meta_cumplida']==a['meets_threshold'],'primary audit')
    acceptance=load(HERE/'ACEPTACION_FINAL.json');check(acceptance['completa'] and acceptance['fits_auditor']==0,'complete acceptance')
    closure=load(HERE/'CIERRE_SESION.json');check(closure['elapsed_seconds']<=7200 and closure['elapsed_seconds']==closure['end_epoch']-START and closure['no_auto_advance'] and not closure['saldo_reutilizable'],'global closure')
    return dict(aprobado=True,solo_lectura=True,fits_nuevos=0,originales=c['protegidos'],auditoria_independiente=True,notebook_celdas=5,evidencias_texto=n,piloto_cerrado=True,confirmacion_cientifica=False)
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
