"""Revalidación sin fits, antes del piloto autorizado por prompt humano."""
import sys,subprocess,platform,importlib.metadata as md,os
from pathlib import Path
from seguridad import ROOT,OUT,OWN,guardar,leer,sha
from comun import reconstruir,referencias,comprobar_defaults,CONF,SPEC
CLOSE='75c3a25182af363f47b0d743820f99084e18fed5'
HIST='109797407d75d2097e5b71f8bcef3fc266bc61d2'
def git(*args,binary=False):return subprocess.check_output(['git',*args],cwd=ROOT,text=not binary)
def entorno():
    wanted=dict(x.split('==') for x in (ROOT/'experimentos_objetivo3_v4/etapa1/requirements.lock.txt').read_text().splitlines())
    actual={d.metadata['Name']:d.version for d in md.distributions() if d.metadata['Name'].lower()!='pip'}
    norm=lambda d:{k.lower().replace('_','-'):v for k,v in d.items()}
    assert sys.executable=='/tmp/icfes-v2-fase2-venv/bin/python' and platform.python_version()=='3.12.14'
    assert len(actual)==54 and norm(actual)==norm(wanted) and md.version('scikit-learn')=='1.9.1'
    assert os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'
    p=subprocess.run([sys.executable,'-m','pip','--disable-pip-version-check','check'],text=True,capture_output=True,check=True)
    return dict(python=platform.python_version(),sklearn=md.version('scikit-learn'),paquetes=actual,pip_check=p.stdout,pip_advertencias=p.stderr,lock_sha256=sha(ROOT/'experimentos_objetivo3_v4/etapa1/requirements.lock.txt'),semilla=20261010,bytecode=False)
def entries(paths):
    import hashlib
    return {str(p.relative_to(ROOT)):dict(tipo='symlink',enlace=p.readlink().as_posix()) if p.is_symlink() else dict(tipo='archivo',sha256=sha(p)) for p in sorted(paths) if p.is_file() or p.is_symlink()}
def check_entries(mapping):
    import hashlib
    for n,state in mapping.items():
        p=ROOT/n
        if state['tipo']=='archivo':assert not p.is_symlink() and sha(p)==state['sha256'],n
        else:
            assert p.is_symlink() and p.readlink().as_posix()==state.get('destino',state.get('enlace')),n
            if 'sha256_texto_enlace' in state:assert hashlib.sha256(state['destino'].encode()).hexdigest()==state['sha256_texto_enlace'],n
def verificar(mapping,historical=False,prefix=''):
    import hashlib
    for n,h in mapping.items():
        name=str(Path(prefix)/n)
        if sha(ROOT/name)!=h:
            assert historical and name=='experimentos_objetivo3_v5/CONTINUIDAD_V5.md'
            assert hashlib.sha256(git('show',HIST+':'+name,binary=True)).hexdigest()==h
    return len(mapping)
def main():
    env=entorno()
    e1=OWN/'etapa1/resultados'
    assert leer(e1/'aceptacion_etapa1.json')['aprobado'] and not leer(e1/'aceptacion_etapa1.json')['pendientes_indispensables']
    assert leer(e1/'verificacion_cierre.json')['aprobado']
    check_entries(leer(e1/'manifiesto_cierre.json')['entregables'])
    check_entries(leer(e1/'congelacion_operativa.json')['artefactos'])
    assert git('rev-parse','HEAD').strip()==CLOSE
    assert git('branch','--show-current').strip()=='codex/objetivo3-v5-mae'
    assert git('show','-s','--format=%s','HEAD').strip()=='etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora'
    assert not git('log','--oneline',CLOSE+'..HEAD').strip()
    subprocess.run(['git','merge-base','--is-ancestor',CLOSE,'HEAD'],cwd=ROOT,check=True)
    refs=[('diseno_temporal_objetivo3_v1/resultados/manifiesto_diseno.json','entregables_sha256',False,''),('diagnostico_objetivo3_v1/fase1/resultados/manifiesto_cierre.json','entregables_sha256',False,''),('experimentos_objetivo3_v5/etapa1/resultados/manifiesto_cierre.json','entregables_sha256',True,''),('experimentos_objetivo3_v5/etapa2/resultados/manifiesto_cierre.json','entregables_sha256',False,''),('experimentos_objetivo3_v5/etapa1/resultados/congelacion_previa.json','artefactos_sha256',False,''),('experimentos_objetivo3_v5/etapa2/resultados/congelacion_operativa.json','artefactos_sha256',False,''),('experimentos_objetivo3_v5/etapa2/resultados/piloto/indice_integridad.json','archivos_sha256',False,'experimentos_objetivo3_v5/etapa2/resultados/piloto')]
    evidence={n:verificar(leer(ROOT/n)[k],h,p) for n,k,h,p in refs}
    snapshot=leer(e1/'inventario_partida.json')
    for n,state in snapshot['archivos'].items():assert sha(ROOT/n)==state['sha256'],n
    assert git('ls-files','-z').split('\0')[:-1]==snapshot['versionados']
    p,q=reconstruir();r=referencias(p);comprobar_defaults()
    assert leer(e1/'configuracion_operativa.json')['configuraciones']==CONF['configuraciones']
    assert SPEC['heredado']['ventanas']==CONF['ventanas']
    paths=[ROOT/n for n in snapshot['archivos']]
    paths.extend((OWN/'etapa1').rglob('*'))
    protected=entries(set(paths))
    guardar(OUT/'entorno.json',env)
    guardar(OUT/'partida.json',dict(protegidos=protected,continuidad_inicial=(OWN/'CONTINUIDAD_EXPERIMENTAL.md').read_text(),continuidad_sha256=sha(OWN/'CONTINUIDAD_EXPERIMENTAL.md'),git=dict(head=CLOSE,rama=git('branch','--show-current').strip(),asunto=git('show','-s','--format=%s','HEAD').strip(),ascendencia=True,posterior=[],versionados=snapshot['versionados'])))
    guardar(OUT/'preflight.json',dict(aprobado=True,fase1_completa_congelada=True,manifiestos=evidence,filas=len(p),territorios=p.codigo_departamento.nunique(),cambios=len(q),referencias=r,defaults36=True,pruebas17=True,notebook6=True,fuente_sha256=SPEC['heredado']['fuente_sha256'],derivado_sha256=SPEC['heredado']['derivado_sha256'],fase2_autorizada='Prompt humano enviado expresamente el 2026-10-11',plan_fase2_previo='No existe plan experimental con sección fase2; contrato vigente protocolo1.0.0 §§3–8 y prompt enviado; plan propio documentado antes de fits',fits=0))
    print('Preflight etapa2 APROBADO; sin fits')
if __name__=='__main__':main()
