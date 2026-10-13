"""Verificador solo lectura. No red, escritura, modelos ni lectura de registros.
Opcional --cotejo: reconstruir evidencias en memoria con runtime documental.
"""
from pathlib import Path
import sys,json,csv,hashlib,os,collections
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(p):
    assert p.is_file() and not p.is_symlink(),str(p)
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def rows(n): return list(csv.DictReader((HERE/n).open()))
def verify(recompute=False):
    partida=json.loads((HERE/'PARTIDA.json').read_text());manifest=json.loads((HERE/'MANIFIESTO.json').read_text())
    for name,h in partida['sha256'].items():assert sha(ROOT/name)==h,'Original alterado: '+name
    actual=set()
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in partida['exclusiones_directorios'] and not (Path(base)/d).is_symlink() and Path(base)/d!=HERE]
        for n in names:
            p=Path(base)/n
            if p.is_file() and not p.is_symlink():actual.add(p.relative_to(ROOT).as_posix())
    assert actual==set(partida['sha256']),'Inventario fuera de investigación cambió'
    own=set()
    for p in HERE.rglob('*'):
        assert not p.is_symlink(),'Enlace propio no permitido'
        if p.is_file():own.add(p.relative_to(HERE).as_posix())
    assert own==set(manifest['sha256'])|set(manifest['exclusiones']),'Inventario propio cambió'
    for name,h in manifest['sha256'].items():assert sha(HERE/name)==h,'Entrega alterada: '+name
    acquisitions=[json.loads(l) for l in (HERE/'ADQUISICIONES.jsonl').read_text().splitlines()]
    assert len({r['archivo'] for r in acquisitions})==len(acquisitions)
    for r in acquisitions:
        assert sha(HERE/r['archivo'])==r['sha256']
        assert r['url_solicitada'].startswith(('https://www.dane.gov.co/','https://www.icfes.gov.co/'))
        assert r['url_final'].startswith(('https://www.dane.gov.co/','https://www.icfes.gov.co/'))
        assert not any(t in r['archivo'].lower() for t in ['.txt','microdatos'])
    txt=json.loads((HERE/'PROCEDENCIA_TXT.json').read_text())
    assert len(txt)==14
    for r in txt:assert partida['sha256'][r['archivo']]==r['sha256']
    cells=rows('COTEJO_CELDAS.csv');diff=rows('DIFERENCIAS.csv');summary=rows('RESUMEN_COTEJO.csv');calendar=rows('CALENDARIO_EDICIONES.csv')
    assert len(cells)==31152 and len(diff)==984 and len(calendar)==494
    assert all(int(r['celdas'])==528 for r in summary)
    assert sum(int(r['diferentes']) for r in summary)==len(diff)
    assert len({tuple(r[k] for k in ['oficial','local','anio','territorio','variable']) for r in cells})==len(cells)
    assert all(r['anio']!='2020' for r in cells)
    assert sum(r['igual_exacto']=='True' for r in cells)==30168
    assert all('original_2018' in r['oficial'] for r in diff)
    assert len(rows('CORTES_REVISADOS.csv'))==15
    for r in rows('CORTES_REVISADOS.csv'):assert r['decision_uso'].startswith('PENDIENTE')
    for r in json.loads((HERE/'REFERENCIAS.json').read_text()):
        path=HERE/r['archivo']
        if not path.exists():path=ROOT/r['archivo']
        assert sha(path)==r['sha256'],r['id']
    ctrl=json.loads((HERE/'CONTROL_DOCUMENTAL.json').read_text())
    assert ctrl['fecha_uso'] is None and ctrl['cobertura_nominal']==165 and ctrl['cobertura_certificada']==0
    assert all(ctrl[k]==0 for k in ['fits','repeticiones','escenarios','datasets_analiticos_nuevos','bases_icfes_descargadas','registros_personales_leidos'])
    assert ctrl['avance_automatico'] is False
    if recompute:
        sys.path.insert(0,str(HERE/'fuentes'))
        from cotejar import calculate
        e,s,d,st=calculate()
        def comparable(items):return [{k:str(v) for k,v in r.items()} for r in items]
        assert comparable(e)==cells and comparable(s)==summary and comparable(d)==diff,'Cotejo no reproducido'
        assert st==json.loads((HERE/'ESTRUCTURA_Y_NOTAS.json').read_text()),'Estructura no reproducida'
    return dict(conservacion_aprobada=True,archivos_previos=len(actual),archivos_entrega=len(manifest['sha256']),adquisiciones=len(acquisitions),trazabilidad_aprobada=True,comparaciones_celdas=len(cells),diferencias=len(diff),reproduccion_cotejo=recompute,disponibilidad_historica_certificada=False,identidad_txt_icfes_certificada=False,cierre_cientifico='DOCUMENTAL INCOMPLETO',fecha_uso=None,modelos_ejecutados=False,avance_automatico=False,limite='Conservación no autentica disponibilidad histórica; exclusiones y destinos de enlaces no certificados.')
if __name__=='__main__': print(json.dumps(verify('--cotejo' in sys.argv),ensure_ascii=False))
