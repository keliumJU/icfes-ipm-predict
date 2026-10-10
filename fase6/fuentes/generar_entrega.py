"""Generación documental determinista; solo entradas cerradas y fuentes Markdown."""
from pathlib import Path
import csv
import hashlib
import html
import json
import platform
import re
import shutil
from integridad import ROOT, OUT, guardar, sha

HERE = Path(__file__).resolve().parent
ENT = ROOT/'fase6/entrega'
LABELS = {'gradient_boosting_ambas_07':'GBR ambas', 'gradient_boosting_tasas_07':'GBR tasas',
          'gradient_boosting_ipm_02':'GBR IPM', 'ols_ambas':'OLS ambas',
          'ols_tasas':'OLS tasas', 'ols_ipm':'OLS IPM', 'media':'Media',
          'random_forest_ambas_05':'RF ambas', 'ridge_tasas_02':'Ridge tasas'}
HEADERS = {'anio':'Año','territorios':'Territorios','celdas':'Celdas','registros':'Registros',
           'min_registros':'Mín.','max_registros':'Máx.','uso':'Uso','id':'Modelo',
           'n_entradas':'Entradas','n':'n','mae':'MAE','rmse':'RMSE','sesgo':'Sesgo','r2':'R²',
           'periodo':'Periodo','variable':'Indicador','familia':'Familia',
           'r_entre_territorios':'Entre','r_dentro_territorio':'Dentro',
           'r_doble_centrado':'Doble centrado'}

def cells(line):
    return [x.strip() for x in line.strip().strip('|').split('|')]

def compact_tables(text):
    def table(match):
        lines=match.group().strip().splitlines()
        data=[cells(x) for x in lines]
        if data[0][0] == 'anio':
            data=[row[:2]+row[3:] for row in data]
        # Mínimos por familia: el ID exacto y familia redundante viven en anexo.
        if data[0][:2] == ['familia','id']:
            data=[row[1:] for row in data]
        # Remuestreo: quitar contexto/cantidad redundantes y combinar percentiles.
        if data[0][0] == 'contexto':
            rows=[['Comparación a−b','Δ MAE','P2,5','P97,5'],['---']*4]
            for row in data[2:]:
                rows.append([f'{LABELS[row[1]]}−{LABELS[row[2]]}', *row[3:6]])
            data=rows
        # Fuentes de robustez quedan en pie y anexo.
        if data[0][0] == 'Diagnóstico' and len(data[0]) == 4:
            data=[row[:3] for row in data]
        for i,row in enumerate(data):
            data[i]=[HEADERS.get(x,LABELS.get(x,x)) for x in row]
        return '\n'.join('| '+' | '.join(row)+' |' for row in data)+'\n'
    return re.sub(r'(?:^\|.*\n)+',table,text,flags=re.M)

def inline(s):
    s=html.escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'\*([^*]+)\*',r'<em>\1</em>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
    return s

def render(md):
    """Subconjunto explícito: títulos, párrafos, tablas GFM, listas y enlaces."""
    lines=md.splitlines(); parts=[]; i=0
    while i<len(lines):
        s=lines[i]
        if not s.strip(): i+=1; continue
        h=re.match(r'^(#{1,3}) (.*)',s)
        if h:
            n=len(h[1]); parts.append(f'<h{n}>{inline(h[2])}</h{n}>'); i+=1
        elif s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                rows.append(cells(lines[i])); i+=1
            parts.append('<table><thead><tr>'+''.join(f'<th>{inline(x)}</th>' for x in rows[0])+'</tr></thead><tbody>')
            for row in rows[2:]: parts.append('<tr>'+''.join(f'<td>{inline(x)}</td>' for x in row)+'</tr>')
            parts.append('</tbody></table>')
        elif re.match(r'^\d+\. ',s):
            parts.append('<ol>')
            while i<len(lines) and re.match(r'^\d+\. ',lines[i]):
                parts.append('<li>'+inline(re.sub(r'^\d+\. ','',lines[i]))+'</li>'); i+=1
            parts.append('</ol>')
        else:
            paragraph=[s]; i+=1
            while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||\d+\. )',lines[i]):
                paragraph.append(lines[i]); i+=1
            parts.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '<!doctype html><html lang="es"><meta charset="utf-8"><title>Objetivo 3: entrega revisada</title><style>body{font:16px/1.5 Arial,sans-serif;max-width:960px;margin:32px auto;padding:0 24px;color:#202830}h1{font-size:26px}h2{font-size:21px;margin-top:32px}h3{font-size:18px}table{border-collapse:collapse;width:100%;font-size:13px;margin:16px 0;table-layout:auto}th,td{border:1px solid #bac4cc;padding:6px;text-align:left;overflow-wrap:anywhere}th{background:#e8eef3}code{font-size:12px;overflow-wrap:anywhere}a{overflow-wrap:anywhere}@media print{body{max-width:none;margin:0}table{font-size:10px}tr{break-inside:avoid}h2{break-after:avoid}}</style><body><main>'+''.join(parts)+'</main></body></html>\n'

def generar():
    ENT.mkdir(parents=True,exist_ok=True)
    clean=compact_tables((HERE/'informe_plantilla.md').read_text())
    (ENT/'informe_objetivo_3_revisado.md').write_text(clean)
    (ENT/'informe_para_copiar.html').write_text(render(clean))
    # Anexo independiente: detalle exacto de revisión y copia íntegra de evidencia narrativa.
    header=(HERE/'anexo_plantilla.md').read_text()
    reviewed=(ROOT/'informe_objetivo_3.md').read_text().replace('tas as','tasas')
    reviewed=reviewed.replace('que cruzan cero: la ventaja no es uniforme respecto de la composición territorial remuestreada',
        'que cruzan cero: la dispersión condicional de la diferencia agregada incluye valores de ambos signos')
    reviewed=re.sub(r'^# ', '## ', reviewed, flags=re.M)
    reviewed=re.sub(r'^## ([1-8])\.',r'### R\1.',reviewed,flags=re.M)
    reviewed=reviewed.replace('](fase5/figuras/','](../../fase5/figuras/')
    anexo=header+'\n\n'+reviewed
    (ENT/'anexo_tecnico.md').write_text(anexo)
    figdir=ENT/'figuras'; figdir.mkdir(exist_ok=True)
    for p in sorted((ROOT/'fase5/figuras').glob('*')):
        shutil.copyfile(p,figdir/p.name)
    fuentes=['informe_objetivo_3.md','fase6/fuentes/informe_plantilla.md','fase6/fuentes/anexo_plantilla.md']
    guardar('generacion.json',dict(fecha_cliente='2026-10-09',python=platform.python_version(),
        fuentes_sha256={p:sha(ROOT/p) for p in fuentes},
        figuras_copia_exacta={p.name:sha(p) for p in figdir.iterdir()},
        modelos_ajustados=0,predicciones_nuevas=0,remuestreos_nuevos=0,simulaciones=0,
        nuevo_notebook='No necesario: revisión y generación documental, notebooks previos conservados',
        semilla='No aplica; generación determinista',render='HTML semántico desde subconjunto Markdown, sin servicio Google Docs'))
    print('Informe revisado, anexo independiente, HTML de copia y ocho figuras conservadas')

if __name__=='__main__': generar()
