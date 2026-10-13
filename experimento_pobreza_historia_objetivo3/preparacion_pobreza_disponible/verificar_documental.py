"""Verificador actual de SOLO LECTURA; Python estándar, no red, no modelos.

Comprueba conservación del inventario inicial y copia de continuidad propia,
manifiesto ampliado y coherencia documental. No autentica fuentes oficiales.
Ejecución: python -B verificar_documental.py (no necesita /tmp).
"""
from pathlib import Path
import hashlib, json, csv, os, ast

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PREFIX=HERE.relative_to(ROOT).as_posix()+'/'

def sha(p):
    assert p.is_file() and not p.is_symlink(), f'Archivo ausente/symlink: {p}'
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def load(name):return json.loads((HERE/name).read_text())

def verify():
    initial=load('PARTIDA_DOCUMENTAL.json')
    old=initial['archivos_previos_sha256']
    # Exactly one permitted changed previous file, mapped to its exact preserved bytes.
    continuity=PREFIX+'CONTINUIDAD.md'
    for name,expected in old.items():
        p=HERE/'antecedentes_prompt_guardado/CONTINUIDAD.md' if name==continuity else ROOT/name
        assert sha(p)==expected, f'Original alterado: {name}'
    for name,expected in initial['carpeta_previa_sha256'].items():
        assert sha(HERE/'antecedentes_prompt_guardado'/name)==expected, f'Copia inicial alterada: {name}'
    manifest=load('MANIFIESTO_DOCUMENTAL.json')
    for name,expected in manifest['sha256'].items():
        assert sha(HERE/name)==expected, f'Entrega alterada: {name}'
    assert manifest['exclusiones']==['MANIFIESTO_DOCUMENTAL.json','VERIFICACION_DOCUMENTAL.json']
    actual=set()
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in initial['excluidos_inventario']]
        for n in names:
            p=Path(base)/n
            if p.is_file():
                if p.is_symlink():
                    assert not p.is_relative_to(HERE), f'Symlink en entrega nueva: {p}'
                    # Initial snapshot explicitly selected regular, non-symlink files.
                    # Do not invent a historical link-target baseline now.
                    continue
                actual.add(p.relative_to(ROOT).as_posix())
    own={PREFIX+n for n in manifest['sha256']}|{PREFIX+n for n in manifest['exclusiones']}
    assert actual==set(old)|own, 'Inventario ampliado incorrecto o escritura ajena'
    refs=load('REFERENCIAS.json');ids={r['id'] for r in refs}
    assert len(refs)==len(ids)==20
    for r in refs:
        from urllib.parse import urlparse
        host=urlparse(r['url']).hostname
        assert host.endswith('.dane.gov.co') or host.endswith('.icfes.gov.co')
        assert r['consulta']=='2026-10-12' and r['ubicacion'] and r['limitacion']
        assert len(r['extracto_breve'].split())<=25
        if r['copia_documental']:assert r['copia_documental'] in manifest['sha256']
    rows=list(csv.DictReader((HERE/'CALENDARIO.csv').open()))
    assert len(rows)==134
    required=['fuente','anio_observado','edicion','fecha_publicacion','evidencia',
              'correspondencia_archivo_local','estado_comprobacion','limitacion','fecha_adquisicion']
    for r in rows:
        assert all(r[k] for k in required)
        assert set(r['evidencia'].split(';'))<=ids
        assert r['fecha_adquisicion']=='NO DEMOSTRADA'
        assert 'DEMOSTRADA' in r['correspondencia_archivo_local'] or 'NO ES' in r['correspondencia_archivo_local'] or 'NO CORRESPONDENCIA' in r['correspondencia_archivo_local']
    summary=load('RESUMEN_CALENDARIO.json')
    for year in summary['anios']:
        for variable in ['IPM',*summary['tasas']]:
            selected=[r for r in rows if int(r['anio_observado'])==year and r['fuente']==variable]
            assert len(selected)==(2 if variable=='IPM' and year==2018 else 1)
        assert len([r for r in rows if int(r['anio_observado'])==year and r['fuente']=='Saber 11 puntajes'])==2
        assert len([r for r in rows if int(r['anio_observado'])==year and r['fuente']=='Saber 11 media anual local'])==1
    cuts=list(csv.DictReader((HERE/'CORTES_PROPUESTOS.csv').open()))
    january=[r for r in cuts if '-01-01T' in r['corte_propuesto']]
    assert len(cuts)==15 and [int(r['pobreza_ultimo_anio_documentado']) for r in january]==[2019,2019,2021,2022,2023]
    for r in cuts:
        assert r['fecha_producto']<r['corte_propuesto'][:10]
        assert r['evidencia'] in ids and '0 pares certificados' in r['cobertura_certificada']
    readings=load('LECTURAS.json')
    for r in readings['oficiales_archivados']:
        assert sha(HERE/r['archivo'])==r['sha256']
        if isinstance(r['paginas_revisadas'],list):
            assert set(r['paginas_revisadas']).isdisjoint(r['paginas_pendientes'])
            assert set(r['paginas_revisadas'])|set(r['paginas_pendientes'])==set(range(1,r['paginas_totales']+1))
    for r in readings['locales']:assert sha(ROOT/r['archivo'])==r['sha256']
    assert summary['pares_objetivo_historico']==165 and summary['pares_certificados_historicos']==0
    closure=load('CIERRE_DOCUMENTAL_DISPONIBILIDAD.json')
    assert closure['estado']=='incompleto_documental_procedencia_disponibilidad'
    assert closure['ajustes']==closure['nuevos_datasets_analiticos']==0
    assert not closure['objetivo4_ejecutado'] and not closure['avance_automatico']
    # Own executable sources must use standard documentary tooling only.
    allowed={'pathlib','hashlib','json','datetime','zipfile','xml.etree.ElementTree','subprocess','sys','csv','ast','platform','shutil','re','os','urllib.parse'}
    sources=list((HERE/'fuentes').glob('*.py'))+[HERE/'verificar_documental.py']
    for p in sources:
        tree=ast.parse(p.read_text())
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):assert all(a.name in allowed for a in n.names)
            if isinstance(n,ast.ImportFrom):assert n.module in allowed
    for phrase in ['1 de enero','pendiente','No se heredan','Persistencia','Historia sola','sin anualizar','2020 excluido']:
        assert phrase in (HERE/'PROPUESTA_PROTOCOLO.md').read_text(), phrase
    return dict(aprobado_integridad_documental=True,solo_lectura=True,archivos_previos_comprobados=len(old),
        archivos_entrega_comprobados=len(manifest['sha256']),copias_prompt_comprobadas=7,calendario_filas=134,cortes=15,
        fuentes_autenticadas=False,disponibilidad_valores_locales_certificada=False,pares_certificados=0,
        cierre_incompleto=True,ajustes=0,nuevos_datasets_analiticos=0,objetivo4_ejecutado=False,avance_automatico=False,
        limite='Inventario inicial de archivos regulares, sin symlinks; Git/runtime/cache excluidos. Sin certificación retrospectiva de destinos de enlaces ni autenticidad oficial.')

if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
