"""Calendarios y referencias documentales sin valores analíticos ni modelos.
Depende de cotejo ejecutado y adquisiciones conservadas. Semilla: no aplica.
"""
from iniciar import HERE,ROOT,sha
from cotejar import write_csv,YEARS
from pypdf import PdfReader
import json,csv,collections,sys,platform
DATES={2018:'2019-07-12',2019:'2020-12-21',2020:'2021-09-02',2021:'2022-04-28',2022:'2023-05-23',2023:'2024-04-19',2024:'2025-04-22',2025:'2026-04-14'}
REVIEWS={'icfes_2018.pdf':[146,147],'icfes_2019.pdf':[70,94],'icfes_2020.pdf':[40,41,42],'icfes_cuatrienio.pdf':[87,89],'icfes_2023.pdf':[89,90,91,92],'icfes_2024.pdf':[26,27],'icfes_2025.pdf':[35,36,38,42,44,45,46,47,49],'icfes_paac2022_2.pdf':[9],'icfes_paac2022_3.pdf':[9]}
def save(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    acquisitions=[json.loads(l) for l in (HERE/'ADQUISICIONES.jsonl').read_text().splitlines()]
    acquired={r['archivo']:r for r in acquisitions}
    structures=json.loads((HERE/'ESTRUCTURA_Y_NOTAS.json').read_text())
    comparisons=list(csv.DictReader((HERE/'RESUMEN_COTEJO.csv').open()))
    cellrows=list(csv.DictReader((HERE/'COTEJO_CELDAS.csv').open()))
    calendar=[];references=[]
    for st in structures:
        if '/evidencia/' not in st['archivo']:continue
        filename=st['archivo'].split('/')[-1];edition=2018 if 'original' in filename else int(filename[5:9])
        ar=acquired['evidencia/'+filename]; groups=collections.defaultdict(list)
        for r in cellrows:
            if r['oficial']=='evidencia/'+filename and r['local'].endswith('2025.xlsx'):groups[(int(r['anio']),r['variable'])].append(r)
        for (y,var),rows in groups.items():
            assert len(rows)==33
            n=sum(r['igual_exacto']=='True' for r in rows)
            calendar.append(dict(fuente='DANE ECV',anio_observado=y,producto=var,edicion=filename,publicacion_producto=DATES[edition],primera_publicacion_valores_locales='NO CERTIFICADA',revision='CNPV 2018' if edition!=2018 else 'Original anterior a recalibración',url=ar['url_final'],evidencia='ESTRUCTURA_Y_NOTAS.json; '+filename+'; hoja/celda en COTEJO_CELDAS.csv',correspondencia_local=f'{n}/33 igualdad exacta frente a libro local 2025',identidad_archivo_local=edition in [2024,2025],disponibilidad_historica='CONDICIONADA: fecha declarada y contenido adquirido hoy; bytes históricos sin sello',poblacion='Personas residentes' if var=='IPM' else 'Hogares residentes',geografia='32 departamentos y Bogotá; Total',estado='Igualdad numérica demostrada' if n==33 else 'Edición original incompatible con vector local',limitacion='No autentica el evento histórico de adquisición ni ausencia de revisiones intermedias',adquisicion_actual_utc=ar['adquisicion_utc']))
        references.append(dict(id='D'+str(edition),url=ar['url_final'],consulta='2026-10-12',archivo='evidencia/'+filename,sha256=ar['sha256'],ubicacion='ESTRUCTURA_Y_NOTAS.json: títulos, columnas Total, notas y celdas; COTEJO_CELDAS.csv',hecho=f'Edición agregada departamental adquirida hoy, fecha declarada {DATES[edition]}',limite='No sello histórico de bytes; fecha de publicación del producto separada de disponibilidad local.'))
    meta=json.loads((HERE.parent.parent/'METADATOS_LOCALES.json').read_text())
    for y in sorted(YEARS):
        for period in [1,2]:
            local=next(r for r in meta if r['archivo']==f'raw_data/Examen_Saber_11_{y}{period}.txt')
            lower=upper='NO DEMOSTRADO';evidence='Inventario general hasta 2024, reedición 2025; sin enlace a TXT local';edition='NO IDENTIFICADA'
            if y==2021 and period==2:
                lower='2021-09-01';upper='2021-12-31';evidence='evidencia_oficial/icfes_gestion2021.pdf página PDF/impresa 146; carga 2021 A; informe de otra entrega, huella en REFERENCIAS.json'
            if y==2023:
                lower='2024-01-01';upper='2024-03-31';evidence='evidencia_oficial/icfes_rendicion2024.pdf páginas PDF 111–112; revisión y publicación 2023 A+B'
            if y==2024: evidence='evidencia/icfes_2025.pdf página PDF 46; repositorio hasta 2024 en 2025, sin día/aplicación/edición específica'
            calendar.append(dict(fuente='ICFES',anio_observado=y,producto=f'Saber 11 aplicación {period}',edicion=edition,publicacion_producto=f'{lower} / {upper}',primera_publicacion_valores_locales='NO CERTIFICADA',revision='Diccionarios actualizados 2024; ampliación/estandarización 2025, correspondencia individual pendiente',url='https://www.icfes.gov.co/investigaciones/data-icfes/',evidencia=evidence,correspondencia_local=local['archivo']+' SHA256 '+local['sha256'],identidad_archivo_local=False,disponibilidad_historica='NO DEMOSTRADA para TXT local',poblacion='Local filtrada según protocolo; universo edición oficial por identificar',geografia='Colegio; agregación anual requiere ambas aplicaciones',estado='Compatibilidad nominal; edición local no autenticada',limitacion='Intervalo de evento institucional no es disponibilidad de valores locales; mtime no es adquisición',adquisicion_actual_utc='No se adquirió base ICFES'))
    for row in calendar:
        if row['fuente']=='DANE ECV':
            row['identidad_archivo_local']=('Identidad completa con libro local '+row['edicion'][5:9]+'; frente a otro libro solo igualdad numérica' if row['edicion'] in ['dane_2024.xlsx','dane_2025.xlsx'] else 'No identidad de archivo; cotejo de celdas')
    write_csv('CALENDARIO_EDICIONES.csv',calendar)
    # Catorce TXT: solo metadatos antecedentes y revalidación por baseline, ningún registro.
    save('PROCEDENCIA_TXT.json',[dict(**r,correspondencia_edicion='NO DEMOSTRADA',fecha_uso='PENDIENTE',revision_actual='Huellas revalidadas por conservación, registros no leídos') for r in meta if r['archivo'].startswith('raw_data/')])
    readings=[]
    for name,pages in REVIEWS.items():
        b=PdfReader(HERE/'evidencia'/name)
        readings.append(dict(archivo='evidencia/'+name,total_paginas=len(b.pages),revisadas=pages,pendientes=[i for i in range(1,len(b.pages)+1) if i not in pages],ubicacion='Numeración PDF 1-based; folio puede diferir',metodo='Localización automática de palabras y lectura explícita de páginas; no lectura íntegra',revision_visual=[9] if 'paac2022_2' in name else ([46] if name=='icfes_2025.pdf' else [])))
    oldrefs=json.loads((HERE.parent.parent/'REFERENCIAS.json').read_text())
    for id in ['DRECALIBRACION','I2021CARGA','I2023CARGA','IINVENTARIO','INUEVAS','ICALENDARIO']:
        r=next(r for r in oldrefs if r['id']==id);p=HERE.parent.parent/r['copia_documental']
        references.append(dict(id=id,url=r['url'],consulta='2026-10-12',archivo=str(p.relative_to(ROOT)),sha256=sha(p),ubicacion=r['ubicacion'],hecho=r['interpretacion'],limite=r['limitacion'],revision_actual='Páginas 1–3, 146 y 111–112 releídas según documento; imágenes conservadas como antecedente salvo inventario visual actual'))
    for name,pages in REVIEWS.items():
        ar=acquired['evidencia/'+name]
        references.append(dict(id=name.removesuffix('.pdf').upper(),url=ar['url_final'],consulta='2026-10-12',archivo=ar['archivo'],sha256=ar['sha256'],ubicacion='Páginas PDF '+','.join(map(str,pages)),hecho='Gestión/publicación y repositorio: ver REGISTRO_PROCEDENCIA_REVISIONES.md',limite='No enlaza huellas de TXT locales ni certifica fecha de sus valores'))
    for ar in acquisitions:
        if ar['archivo'].endswith('.html'):references.append(dict(id=ar['archivo'].split('/')[-1],url=ar['url_final'],consulta='2026-10-12',archivo=ar['archivo'],sha256=ar['sha256'],ubicacion='Sección de producto: Anexo departamental / DataIcfes / Saber 11 / Informes de gestión según título',hecho='Página oficial conservada con enlaces y fechas declaradas',limite='Página actual, no captura histórica autenticada'))
    save('REFERENCIAS.json',references);save('LECTURAS.json',readings+[
        dict(archivo='../../evidencia_oficial/dane_nota2019.pdf',revisadas=[1,2,3],pendientes='Páginas posteriores no revisadas en esta sesión'),
        dict(archivo='../../evidencia_oficial/icfes_gestion2021.pdf',revisadas=[146],pendientes='Resto no revisado en esta sesión'),
        dict(archivo='../../evidencia_oficial/icfes_rendicion2024.pdf',revisadas=[111,112],pendientes='Resto no revisado en esta sesión')])
    cuts=list(csv.DictReader((HERE.parent.parent/'CORTES_PROPUESTOS.csv').open()))
    for r in cuts:
        r['decision_uso']='PENDIENTE; ninguna fecha adoptada'
        r['nuevo_cotejo']='Igualdad de las 528 celdas del año con edición DANE enlazada actualmente; sellado histórico pendiente'
        r['historia_puntaje']='Ediciones de ambas aplicaciones no vinculadas a TXT locales; no certificar persistencia ni historia'
        r['respuestas_entrenamiento']='Disponibilidad de edición local y de cada etiqueta anterior al corte sin certificar'
        r['cobertura_certificada']='0/33 por corte; 0/165 conjunta; no inexistencia de datos'
    write_csv('CORTES_REVISADOS.csv',cuts)
    dif=list(csv.DictReader((HERE/'DIFERENCIAS.csv').open()))
    c=collections.Counter(r['variable'] for r in dif if r['local'].endswith('2025.xlsx'))
    save('CONTROL_DOCUMENTAL.json',dict(fecha_cliente='2026-10-12 America/Bogota',version='1.0',python=sys.version,plataforma=platform.platform(),openpyxl=__import__('openpyxl').__version__,xlrd=__import__('xlrd').__version__,pypdf=__import__('pypdf').__version__,xlrd_origen='/tmp/icfes_vintage_deps, 2.0.2; runtime compartido sin cambios',semilla=None,comprobaciones_celdas=len(cellrows),diferencias_original2018_por_variable=dict(c),archivos_dane_identicos=['2024','2025'],fits=0,repeticiones=0,escenarios=0,datasets_analiticos_nuevos=0,bases_icfes_descargadas=0,registros_personales_leidos=0,fecha_uso=None,cobertura_nominal=165,cobertura_certificada=0,cobertura_maxima_condicionada=165,disponibilidad_historica_certificada=False,avance_automatico=False))
    print(json.dumps(dict(filas_calendario=len(calendar),referencias=len(references),cortes=len(cuts),cotejos=len(cellrows))))
if __name__=='__main__': main()
