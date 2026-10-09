"""Control documental/huellas final; no nuevos ajustes."""
import analisis as a
import nbformat, re, ast
from pathlib import Path
prep=a.load('preparacion.json')
for p,h in prep['snapshot_previo'].items():
    if p!='CONTINUIDAD_OBJETIVO_3.md': assert a.m.huella(a.ROOT/p)==h,p
for source in (a.ROOT/'fase4/fuentes').glob('*.py'):
    if not source.name[:2].isdigit(): ast.parse(source.read_text())
for stage in ('05_contraste_territorial','06_robustez_explicaciones'):
    source=a.ROOT/'fase4/fuentes'/f'{stage}.py'
    chunks=re.split(r'^# %%([^\n]*)\n',source.read_text(),flags=re.M)
    expected=[(flag,body.strip()) for flag,body in zip(chunks[1::2],chunks[2::2])]
    nb=nbformat.read(a.ROOT/'notebooks'/f'{stage}.ipynb',as_version=4);nbformat.validate(nb)
    assert len(nb.cells)==len(expected)
    for cell,(flag,body) in zip(nb.cells,expected):
        assert cell.source==body
        assert cell.cell_type==('markdown' if '[markdown]' in flag else 'code')
        if cell.cell_type=='code':
            compile(body,str(source),'exec'); assert cell.execution_count is not None
    check=next(v for v in a.load('verificacion_notebooks.json') if v['notebook']==str((a.ROOT/'notebooks'/f'{stage}.ipynb').relative_to(a.ROOT)))
    assert check['fuente_sha256']==a.m.huella(source) and check['notebook_sha256']==a.m.huella(a.ROOT/check['notebook'])
a.save('registro_ejecuciones.json',{'ajustes_territoriales':99,'controles_focales_realizados':2,'ajustes_por_control':3,'ajustes_focales_totales':6,'predicciones_comprobadas_por_control':12,'bootstrap_replicas_guardadas':14000,'reproduccion_completa_en_copia_ejecutada':False,'kernel_inicial_interrumpido_sin_resultados':True,'celdas_ejecutadas_kernel':4,'documentacion_regenerada_sin_reajuste':True})
a.save('verificacion_documental.json',{'fuentes_sintaxis_validas':True,'fuentes_notebooks_identicas':True,'notebooks_validados_con_ejecuciones_reales':True,'snapshot_previo_conservado_excepto_continuidad':True})
paths=list((a.ROOT/'fase4').rglob('*'))+[a.ROOT/'CONTINUIDAD_OBJETIVO_3.md']+[a.ROOT/'notebooks'/f'{stage}.ipynb' for stage in ('05_contraste_territorial','06_robustez_explicaciones')]
a.save('manifiesto_cierre.json',{str(p.relative_to(a.ROOT)):a.m.huella(p) for p in sorted(paths) if p.is_file() and p.name!='manifiesto_cierre.json' and '__pycache__' not in p.parts})
print('Conservación final, correspondencia fuentes/notebooks y manifiesto aprobados; sin nuevos ajustes.')
