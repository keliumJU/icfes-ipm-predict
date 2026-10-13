"""Archiva documentos consultados y registro explícito de lectura (sin declarar páginas no leídas).

Entradas: documentos oficiales descargados en /tmp y REFERENCIAS.json.
Salida: evidencia_oficial/*, LECTURAS.json, EXTRACTOS_DOCUMENTALES.md.
No realiza descargas; no lee datos analíticos. No hay aleatoriedad ni semillas.
"""
from pathlib import Path
import json, shutil, hashlib, platform

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    refs=json.loads((HERE/'REFERENCIAS.json').read_text())
    pages={'dane2018.pdf':([1],6),'dane_nota2019.pdf':([1,2,3],12),
           'dane2025.pdf':([1,2,3,12],26),'icfes_gestion2021.pdf':([146],215),
           'icfes_rendicion2024.pdf':([111,112],None)}
    records=[]
    for r in refs:
        if not r['copia_documental']: continue
        dest=HERE/r['copia_documental'];src=Path('/tmp')/dest.name
        assert src.exists()
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():assert sha(dest)==sha(src)
        else:shutil.copy2(src,dest)
        read,total=pages.get(dest.name,('imagen completa',1))
        if dest.name=='icfes_rendicion2024.pdf':
            import subprocess,re
            info=subprocess.check_output(['pdfinfo',str(src)],text=True)
            total=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        records.append(dict(archivo=dest.relative_to(HERE).as_posix(),url=r['url'],consulta='2026-10-12',sha256=sha(dest),
            bytes=dest.stat().st_size,paginas_revisadas=read,paginas_totales=total,
            paginas_pendientes=[p for p in range(1,total+1) if p not in read] if isinstance(read,list) else [],
            modo='lectura textual de páginas completas; imágenes visualizadas' if dest.suffix=='.pdf' else 'imagen completa inspeccionada visualmente',
            revision_visual_paginas=[1] if dest.name=='dane_nota2019.pdf' else [3] if dest.name=='dane2025.pdf' else [],
            advertencia='Descarga documental actual, no adquisición de datos históricos. Índice textual completo para localizar p112 de rendición no equivale a lectura completa.'))
    local=[('AGENTS.md','completo'),('experimento_pobreza_historia_objetivo3/CONTINUIDAD.md','completo'),
        ('experimento_pobreza_historia_objetivo3/revision_alcance_objetivo4/CONTINUIDAD.md','completo'),
        ('experimento_pobreza_historia_objetivo3/revision_alcance_objetivo4/DECISION_Y_PROTOCOLO.md','completo'),
        ('experimento_pobreza_historia_objetivo3/revision_alcance_objetivo4/REVISION_EVIDENCIA_LOCAL.md','completo'),
        ('experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/antecedentes_prompt_guardado/CONTINUIDAD.md','completo, leído antes de preservación'),
        ('experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/DECISION_GUARDADA.md','completo'),
        ('experimento_pobreza_historia_objetivo3/PROTOCOLO.md','completo; reglas anteriores no adoptadas como nuevo protocolo'),
        ('experimento_pobreza_historia_objetivo3/PLAN.md','Entrega pertinente; el comando mostró incidentalmente todo el archivo, sin activar ejecución ni presupuesto'),
        ('experimento_pobreza_historia_objetivo3/resultados/FECHA_LOCAL.json','completo'),
        ('experimentos_objetivo3_v2/fase1/INFORME_AUDITORIA.md','completo como antecedente necesario; no repetición de cálculos'),
        ('experimentos_objetivo3_v2/fase1/resultados/notas_ipm_2025.csv','completo, notas sin valores analíticos'),
        ('experimentos_objetivo3_v2/fase1/resultados/encabezados_ipm_2025.csv','completo'),
        ('experimentos_objetivo3_v2/fase1/resultados/integridad_inicial.json','claves y fuentes, no inventario histórico completo'),
        ('protocolo/fuentes/configuracion.py','mostrado completo; únicamente DIMENSIONES usado por AST'),
        ('Fuente del IPM/archivo-IPM-descargado.png','imagen completa, sin URL/fecha adquisición'),
        ('experimento_pobreza_historia_objetivo3/preflight.py','antecedente de fuentes y método de tasas; no ejecutado'),
        ('experimento_pobreza_historia_objetivo3/infra.py','mostrado, no ejecutado ni importado'),
        ('experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/verificar_preparacion.py','leído y ejecutado una vez ANTES de ampliación; aprobación histórica preservada')]
    obj=dict(fecha='2026-10-12',python=platform.python_version(),oficiales_archivados=records,
        locales=[dict(archivo=n,ubicacion=s,sha256=sha(ROOT/n)) for n,s in local],
        webs=[dict(id=r['id'],url=r['url'],ubicacion=r['ubicacion'],estado='sección pertinente revisada; resto pendiente') for r in refs if not r['copia_documental']],
        otras_consultas=[dict(url='https://www.icfes.gov.co/wp-content/uploads/2026/06/saber-al-detalle-no-21.pdf',
            ubicacion='fragmentos localizados por búsqueda, pp12–14; no páginas completas',estado='parcial; no usado como prueba en calendario'),
            dict(url='https://www.icfes.gov.co/',ubicacion='calendario mostrado por buscador 2026',estado='parcial; no fecha efectiva de bases')],
        fallos_acceso=['Ruta DANE históricos supuesta no accesible; sustitución por enlaces oficiales por año.',
                      'Imágenes DataIcfes sin texto en navegador; leídas desde descarga documental oficial en /tmp.',
                      'PDF rendición ICFES no accesible mediante web; obtenido por descarga directa oficial.',
                      'Primer curl de calendario falló DNS en aislamiento; repetido con permiso de red.'],
        datos_personales_registros_leidos=False,raw='únicamente SHA256/tamaño/mtime de originales preservados; sin censo ni extracción',
        tesis='No PDF de tesis releído en esta fase; antecedentes necesarios por protocolos y revisión cerrada. No se afirma lectura nueva de sus páginas.',
        limites='No se censó documentación completa del repositorio ni historia de publicaciones completas. Coincidencia nominal no autentica valores.')
    (HERE/'LECTURAS.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    text=['# Extractos documentales pertinentes','',
          'Consulta: 12/10/2026. Extractos breves literales y paráfrasis; sin cifras incorporadas al análisis. Originales documentales archivados cuando se descargaron. Ubicaciones web por encabezado/fila, no números de línea inestables.','']
    for r in refs:
        text += [f"## {r['id']}",'',f"Fuente: [{r['id']}]({r['url']}). Consulta: {r['consulta']}. Ubicación: {r['ubicacion']}.",'',
                 '> '+r['extracto_breve'],'',r['interpretacion'],'','Límite: '+r['limitacion'],'']
    (HERE/'EXTRACTOS_DOCUMENTALES.md').write_text('\n'.join(text))
    print(json.dumps({'documentos_archivados':len(records),'lecturas_locales':len(local)}))

if __name__=='__main__':main()
