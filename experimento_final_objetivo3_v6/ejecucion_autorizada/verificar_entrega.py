"""Solo lectura: integridad de cierres, evidencias y notebooks; nunca fits."""
from comun import *
from cierres import notebook_verify,documental_mapping
import pandas as pd

def verify():
    pf=preflight();documental_mapping();m=load(HERE/'MANIFIESTO_FINAL.json')
    check(sha(OWNROOT/'CONTINUIDAD_V6.md')==m['continuidad_principal_sha'],'own main continuity pointer')
    for s,h in m['sha256'].items():check(sha(HERE/s)==h,'manifest '+s)
    paths={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
    check(paths-set(m['exclusions'])==set(m['sha256']),'manifest inventory')
    for phase,nextphase in [(1,2),(2,3)]:
        pm=load(HERE/f'fase{phase}/MANIFIESTO.json')
        for s,h in pm['sha256'].items():check(sha(HERE/s)==h,'phase '+s)
        check(sha(HERE/f'fase{nextphase}/antecedentes/CONTINUIDAD_ANTERIOR.md')==pm['continuidad_sha'],'preserved continuity')
    for s,h in load(HERE/'fase1/CONGELACION.json')['sha256'].items():check(sha(HERE/s)==h,'freeze '+s)
    notebook_verify(HERE/'fase1','01_controles.ipynb','notebook_controles.py');notebook_verify(HERE/'fase3','02_resultados_objetivo3.ipynb','notebook_resultados.py')
    l=load(HERE/'fase2/piloto/ledger.json');a=load(HERE/'fase3/AUDITORIA.json');accept=load(HERE/'fase3/ACEPTACION.json');ct=load(HERE/'fase3/CONTROL_TEXTO.json')
    check(l['status']=='cerrado_completo' and l['pending'] is None and l['elapsed_seconds']<=7200,'closed budget')
    check(a['aprobado'] and accept['completa'] and accept['fits_auditor']==0,'audit accepted')
    check(ct['aprobado'] and ct['text_sha']==sha(HERE/'TEXTO_OBJETIVO3_TESIS.md') and ct['evidence_sha']==sha(HERE/'EVIDENCIAS_TEXTO.csv'),'text binding')
    ev=pd.read_csv(HERE/'EVIDENCIAS_TEXTO.csv',dtype=str)
    for _,r in ev.iterrows():check(sha(HERE/r.file)==r.sha256,'evidence hash')
    text=(HERE/'TEXTO_OBJETIVO3_TESIS.md').read_text();check(not any(word in text.lower() for word in ['v6','v5','v3','v2','global_v6','especificacion_','runner','ledger']),'academic no engineering versions')
    visual=load(HERE/'fase3/REVISION_VISUAL.json');check(visual['aprobado'],'visual review')
    for name,h in visual['files'].items():check(sha(HERE/'fase3/figuras'/name)==h,'reviewed figure unchanged')
    return dict(aprobado=True,files=len(m['sha256']),originals=pf['conservacion'],historical=pf['historia']['mappings'],experiment_complete=True,new_fits=0,models_loaded=0,read_only=True,technical_acceptance_is_not_authenticity_or_confirmation=True)
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
