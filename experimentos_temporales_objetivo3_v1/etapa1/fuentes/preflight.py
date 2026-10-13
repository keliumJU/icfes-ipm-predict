"""Inventario, hashes y entorno; solo lectura de antecedentes y escritura propia."""
import importlib.metadata as md
import platform
import subprocess
import sys
from seguridad import ROOT, OUT, OWN, sha, leer, guardar

CLOSE = '75c3a25182af363f47b0d743820f99084e18fed5'
HIST = '109797407d75d2097e5b71f8bcef3fc266bc61d2'


def git(*args, binary=False):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=not binary)


def inventario():
    tracked = git('ls-files', '-z').split('\0')[:-1]
    names = set(tracked)
    for folder in ('diagnostico_objetivo3_v1', 'diseno_temporal_objetivo3_v1'):
        names.update(str(p.relative_to(ROOT)) for p in (ROOT / folder).rglob('*') if p.is_file())
    return {n: dict(sha256=sha(ROOT/n), symlink=(ROOT/n).readlink().as_posix()
                   if (ROOT/n).is_symlink() else None) for n in sorted(names)}, tracked


def verificar(mapping, historical=False, prefix=''):
    rows = []
    for n, h in mapping.items():
        name = str(__import__('pathlib').Path(prefix) / n)
        actual = sha(ROOT/name)
        hist = None
        if actual != h and historical and name == 'experimentos_objetivo3_v5/CONTINUIDAD_V5.md':
            import hashlib
            hist = hashlib.sha256(git('show', HIST + ':' + name, binary=True)).hexdigest()
        if actual != h and hist != h:
            raise ValueError('Huella no resuelta: ' + name)
        rows.append(dict(archivo=name, esperado=h, actual=actual, commit=HIST if hist else None,
                         historico=hist))
    return rows


def entorno():
    wanted = dict(line.split('==') for line in (ROOT/'experimentos_objetivo3_v4/etapa1/requirements.lock.txt').read_text().splitlines())
    actual = {d.metadata['Name']: d.version for d in md.distributions() if d.metadata['Name'].lower() != 'pip'}
    norm = lambda d: {k.lower().replace('_', '-'): v for k,v in d.items()}
    if (sys.executable != '/tmp/icfes-v2-fase2-venv/bin/python' or platform.python_version() != '3.12.14'
            or len(actual) != 54 or norm(actual) != norm(wanted) or md.version('scikit-learn') != '1.9.1'):
        raise RuntimeError('Entorno distinto: consultar; sin sustituciones')
    check = subprocess.run([sys.executable, '-m', 'pip', '--disable-pip-version-check', 'check'],
                           capture_output=True, text=True, check=True)
    return dict(aprobado=True, python=platform.python_version(), ejecutable=sys.executable,
                paquetes=actual, sklearn=md.version('scikit-learn'), pip=md.version('pip'),
                pip_check=check.stdout.strip(), pip_advertencias=check.stderr.strip(),
                lock_sha256=sha(ROOT/'experimentos_objetivo3_v4/etapa1/requirements.lock.txt'),
                PYTHONDONTWRITEBYTECODE=__import__('os').environ.get('PYTHONDONTWRITEBYTECODE'), semilla=20261010)


def main():
    env = entorno()
    head = git('rev-parse', 'HEAD').strip()
    subject = git('show', '-s', '--format=%s', 'HEAD').strip()
    branch = git('branch', '--show-current').strip()
    posterior = git('log', '--format=%H %s', CLOSE+'..HEAD').splitlines()
    ancestor = subprocess.run(['git','merge-base','--is-ancestor',CLOSE,'HEAD'],cwd=ROOT).returncode == 0
    assert head == CLOSE and ancestor and not posterior
    assert subject == 'etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora'
    assert branch == 'codex/objetivo3-v5-mae'
    snapshot, tracked = inventario()
    refs = [
        ('diseno_temporal_objetivo3_v1/resultados/manifiesto_diseno.json','entregables_sha256',False,''),
        ('diagnostico_objetivo3_v1/fase1/resultados/manifiesto_cierre.json','entregables_sha256',False,''),
        ('experimentos_objetivo3_v5/etapa1/resultados/manifiesto_cierre.json','entregables_sha256',True,''),
        ('experimentos_objetivo3_v5/etapa2/resultados/manifiesto_cierre.json','entregables_sha256',False,''),
        ('experimentos_objetivo3_v5/etapa1/resultados/congelacion_previa.json','artefactos_sha256',False,''),
        ('experimentos_objetivo3_v5/etapa2/resultados/congelacion_operativa.json','artefactos_sha256',False,''),
        ('experimentos_objetivo3_v5/etapa2/resultados/piloto/indice_integridad.json','archivos_sha256',False,
         'experimentos_objetivo3_v5/etapa2/resultados/piloto'),
    ]
    evidence = {}
    for name,key,hist,prefix in refs:
        evidence[name] = verificar(leer(ROOT/name)[key],hist,prefix)
    index = leer(ROOT/refs[-1][0])['archivos_sha256']
    base = ROOT / refs[-1][-1]
    assert set(index) == {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and p.name != 'indice_integridad.json'}
    conf = leer(ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json')
    spec = leer(ROOT/'diseno_temporal_objetivo3_v1/ESPECIFICACION_PROPUESTA.json')
    for k,old in [('candidatos','configuraciones'),('grupos','grupos'),('ventanas','ventanas')]:
        assert spec['heredado'][k] == conf[old]
    assert sha(ROOT/spec['heredado']['configuracion_archivo']) == spec['heredado']['configuracion_sha256']
    guardar(OUT/'entorno.json',env)
    guardar(OUT/'inventario_partida.json',dict(archivos=snapshot, versionados=tracked,
            git=dict(head=head,asunto=subject,rama=branch,ascendencia=ancestor,posterior=posterior,
                     status=git('status','--short','--untracked-files=all').splitlines()),
            raw='Sin lectura ni censo; ninguna escritura', continuidad_experimental_previa=False))
    guardar(OUT/'huellas_antecedentes.json',evidence)
    guardar(OUT/'preflight.json',dict(aprobado=True,protegidos=len(snapshot),versionados=len(tracked),
            entorno=True,diseno_documental_intacto=True,herencia_exacta=True,
            fits_panel_real=0,modelos_historicos_cargados=0))
    print('Preflight aprobado:',len(tracked),'versionados y',len(snapshot)-len(tracked),'archivos de diagnóstico/diseño protegidos')


if __name__ == '__main__':
    main()
