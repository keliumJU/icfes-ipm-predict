"""Verificación documental; no ejecuta modelos ni importa runners históricos.
Uso: PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python .../verificar_documental.py
Escrituras limitadas al directorio de diseño. No sigue enlaces del inventario.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load(p):
    return json.loads((ROOT / p).read_text())

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def info(p):
    p = ROOT / p
    if p.is_symlink():
        target = os.readlink(p)
        return {'tipo': 'symlink', 'destino': target, 'sha256': sha(target.encode())}
    return {'tipo': 'archivo', 'sha256': sha(p.read_bytes())}

def equal(a, b):
    # La clase de fixture rechazado es un enlace, no un archivo regular.
    return a.get('sha256', a.get('sha256_texto_enlace')) == b.get('sha256', b.get('sha256_texto_enlace')) and ('symlink' in a.get('tipo', 'archivo')) == ('symlink' in b.get('tipo', 'archivo')) and (not ('symlink' in a.get('tipo', 'archivo')) or a.get('destino', a.get('target', a.get('enlace'))) == b.get('destino', b.get('target', b.get('enlace'))))

def write(name, d):
    (OUT / name).write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')

def main():
    prep = load('diseno_memoria_comun_objetivo3_v1/REGISTRO_PREPARACION.json')
    bad = []
    for p, expected in prep['inventario_protegido'].items():
        try:
            if not equal(expected, info(p)): bad.append(p)
        except (FileNotFoundError, OSError): bad.append(p)
    head = git('rev-parse', 'HEAD').decode().strip()
    base = '75c3a25182af363f47b0d743820f99084e18fed5'
    ancestor = subprocess.run(['git','merge-base','--is-ancestor',base,head],cwd=ROOT).returncode == 0
    tracked = git('ls-files','-z').decode().split('\0')[:-1]
    new_outside = [p for p in git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1] if not p.startswith(OUT.name+'/') and p not in prep['inventario_protegido']]
    part = load('experimentos_temporales_objetivo3_v1/etapa2/resultados/partida.json')
    preserved = part['continuidad_inicial'].encode()
    assert sha(preserved) == part['continuidad_sha256'] == 'fd3b963135e9e8233470ef36116d82e67ca4a88aae67b7c785d0a9185ba0b8bb'
    hist_commit = '109797407d75d2097e5b71f8bcef3fc266bc61d2'
    manifests = {}
    for mp in prep['verificaciones_antecedentes']:
        d = load(mp)
        mapping = next(d[k] for k in ['entregables_sha256','entregables','artefactos_sha256','archivos_sha256'] if k in d)
        errors = []; historical = []
        for p, exp in mapping.items():
            exp = {'tipo':'archivo','sha256':exp} if isinstance(exp,str) else exp
            if p == 'experimentos_objetivo3_v5/CONTINUIDAD_V5.md' and '/etapa1/' in mp:
                actual = {'tipo':'archivo','sha256':sha(git('show',hist_commit+':'+p))}
                historical.append({'archivo':p,'commit':hist_commit,'sha256':actual['sha256']})
            elif p == 'experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md' and '/etapa1/' in mp:
                actual = {'tipo':'archivo','sha256':sha(preserved)}
                historical.append({'archivo':p,'ubicacion':'etapa2/resultados/partida.json:continuidad_inicial','sha256':actual['sha256']})
            else:
                q = 'experimentos_objetivo3_v5/etapa2/resultados/piloto/'+p if mp.endswith('piloto/indice_integridad.json') else p
                actual = info(q)
            if not equal(exp, actual): errors.append(p)
        manifests[mp]={'huellas':len(mapping),'aprobado':not errors,'diferencias':errors,'versiones_historicas':historical}
    own_prep = {p: sha((OUT/p).read_bytes()) == h for p,h in prep['huellas_propias'].items()}
    sources = {p:{'esperado':h,'actual':info(p)['sha256'],'aprobado':info(p)['sha256']==h} for p,h in prep['fuentes_sha256'].items()}
    git_record={'head':head,'asunto':git('log','-1','--format=%s').decode().strip(),'rama':git('branch','--show-current').decode().strip(),'base':base,'ascendencia':ancestor,'trabajo_posterior':git('log','--format=%H %s',base+'..HEAD').decode().splitlines(),'versionados':len(tracked),'lista_versionados_igual':tracked==prep['versionados'],'diff_versionados':git('diff','--name-only','HEAD').decode().splitlines(),'status':git('status','--short').decode().splitlines(),'ajenos_nuevos':new_outside}
    ok=not bad and not new_outside and ancestor and tracked==prep['versionados'] and not git_record['diff_versionados'] and all(x['aprobado'] for x in manifests.values()) and all(x['aprobado'] for x in sources.values())
    write('PREFLIGHT_FASE1.json',{'aprobado':ok,'git':git_record,'inventario_protegido':{'entradas':len(prep['inventario_protegido']),'diferencias':bad,'base':'REGISTRO_PREPARACION.json:inventario_protegido','raw':'ignorado sin lectura/censo/escritura'},'manifiestos':manifests,'fuentes':sources,'huellas_preparacion':own_prep,'nota_huellas_propias':'En primera corrida, las cuatro huellas deben coincidir. El cierre actual sustituye solo continuidad propia; original preservado por separado.'})
    print(json.dumps({'aprobado':ok,'protegidos':len(prep['inventario_protegido']),'manifiestos':{p:{'n':v['huellas'],'aprobado':v['aprobado'],'errores':v['diferencias'][:3]} for p,v in manifests.items()},'diferencias':bad[:3],'ajenos_nuevos':new_outside[:3],'huellas_preparacion':own_prep},ensure_ascii=False))

if __name__ == '__main__':
    main()
