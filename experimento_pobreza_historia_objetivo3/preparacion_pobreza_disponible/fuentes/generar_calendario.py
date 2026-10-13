"""Calendario DOCUMENTAL v1, Python estándar, sin datos de evaluación.

Entradas: constantes documentales abajo; configuración leída por AST (sin importarla),
METADATOS_LOCALES.json y encabezados históricos ya auditados.
Salidas: REFERENCIAS.json, CALENDARIO.csv, CORTES_PROPUESTOS.csv, RESUMEN_CALENDARIO.json.
Orden: documental.py -> generar_calendario.py -> cierre y verificador.
Sin red, modelos, paneles numéricos, aleatoriedad, semilla ni notebook necesario.
Las fechas son fechas del PRODUCTO documentado; no certifican los valores locales.
"""
from pathlib import Path
import ast, csv, json, datetime, platform

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
CONSULTA = '2026-10-12'
DANE = 'https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-multidimensional'
ICFES = 'https://www.icfes.gov.co/'
YEARS = [2018, 2019, 2021, 2022, 2023, 2024, 2025]

def save_json(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def save_csv(name, rows):
    with (HERE/name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    refs=[]
    def ref(id, url, location, quote, conclusion, limit, local=''):
        assert len(quote.split()) <= 25
        refs.append(dict(id=id,url=url,consulta=CONSULTA,ubicacion=location,
                         extracto_breve=quote,interpretacion=conclusion,limitacion=limit,
                         copia_documental=local))
    ref('D2025',DANE,'Información 2025; filas Boletín/Anexo departamental y nota Comunicado',
        'Información publicada el 14 de abril de 2026',
        'El anexo departamental está fechado 2026-04-14; el comunicado fue reemplazado 2026-04-20 para precisar redacción sobre personas.',
        'No hay prueba de revisión de cifras del anexo por esa corrección del comunicado; tampoco de ausencia de otras revisiones.')
    for year,date,display in [(2024,'2025-04-22','22 de abril de 2025'),(2023,'2024-04-19','19 de abril de 2024'),(2022,'2023-05-23','23 de mayo de 2023'),(2021,'2022-04-28','28 de abril de 2022')]:
        loc='Información por departamentos; fila Anexo departamental'
        if year in [2023,2024]:loc='Información '+str(year)+'; fila Anexo departamental'
        ref(f'D{year}',DANE+f'/pobreza-multidimensional-{year}',loc,
            f'Anexo departamental {date}', 'Fecha del producto departamental documentada.',
            'Primera disponibilidad de cada cifra/indicador de la edición local no demostrada; no se descargó anexo externo.')
    ref('D2019',DANE+'/pobreza-multidimensional-2019',
        'Información nacional y por departamentos; fila Anexo departamental',
        'Información actualizada el 21 de diciembre de 2020',
        'Publicación nacional 2020-07-14; edición departamental fechada 2020-12-21.',
        'Actualizada no identifica la primera publicación departamental. No trasladar fecha nacional a quince tasas departamentales.')
    ref('D2018ORIGINAL','https://www.dane.gov.co/files/investigaciones/condiciones_vida/pobreza/2018/cp_pobreza_multidimensional_18_departamento.pdf',
        'Página PDF/impresa 1, encabezado',
        '12 de julio de 2019',
        'Comunicado departamental 2018 en edición anterior a la recalibración CNPV 2018.',
        'Fecha del comunicado no demuestra fecha de las quince tasas ni identidad con la serie local revisada.',
        'evidencia_oficial/dane2018.pdf')
    ref('DRECALIBRACION','https://www.dane.gov.co/files/investigaciones/condiciones_vida/pobreza/2019/nota_met__pobreza_multidimensional_19.pdf',
        'Páginas PDF/impresas 1–3, Introducción y estandarización',
        'Asimismo, junto con los resultados de 2019 se publicaron los de 2018 actualizados',
        '2018 fue recalibrado con CNPV 2018 y divulgado con 2019 el 2020-07-14; la nota declara no comparabilidad con la serie de proyecciones Censo 2005.',
        'No demuestra primera publicación de todas las celdas departamentales revisadas.',
        'evidencia_oficial/dane_nota2019.pdf')
    ref('DMETODO2025','https://www.dane.gov.co/files/operaciones/PM/bol-PMultidimensional-2025.pdf',
        'Páginas PDF/impresas 1–3 y 12, Introducción, sección 1 y Tabla 5',
        'A partir de 2018 tiene representatividad estadística',
        'DANE calcula/divulga IPM desde ECV; cinco dimensiones/quince indicadores; incidencia de personas; cobertura 32 departamentos y Bogotá. Tabla 5 usa ECV y proyecciones CNPV 2018.',
        'No autentica libros locales. Las tasas por hogar se identifican en rótulos locales, no se importan cifras del PDF.',
        'evidencia_oficial/dane2025.pdf')
    ref('D2023CORRECCION',DANE+'/pobreza-multidimensional-2023',
        'Fila Boletín técnico, nota aclaratoria',
        'Se realiza una corrección tipográfica',
        'Boletín reemplazado 2024-05-07 para corregir año de referencia en página 3.',
        'No prueba revisión de valores del anexo departamental.')
    ref('DPDET',DANE+'/pobreza-multidimensional-2022',
        'Sección IPM-PDET, nota informativa y Nota aclaratoria 2023-12-22',
        'La serie del Índice de Pobreza Multidimensional de los Programas de Desarrollo con Enfoque Territorial',
        'Se documenta ajuste de factores PDET, un producto diferente del total departamental.',
        'Antecedente sin vínculo demostrado con las celdas locales; no trasladar su revisión al IPM departamental.')
    ref('IDATA',ICFES+'investigaciones/data-icfes/',
        'Consulta más información y Preguntas frecuentes, formato de archivos',
        'Los archivos de DataIcfes se encuentran en formato .txt',
        'Repositorio de bases anonimizadas y documentación; página actualizada 2025-06-26 enlaza inventario, nuevas bases y calendario.',
        'Actualización de página no es publicación histórica de cada archivo.')
    ref('IINVENTARIO',ICFES+'wp-content/uploads/2025/03/inventario_img.jpg',
        'Imagen completa, primera fila de tabla: Examen Saber 11',
        '1996 - 2024',
        'El inventario enlazado declara Saber 11, nivel estudiante, hasta 2024.',
        'Sin fecha interna de primera publicación; ruta de carga no prueba evento histórico. Omisión de 2025 no demuestra inexistencia.',
        'evidencia_oficial/inventario_img.jpg')
    ref('INUEVAS',ICFES+'wp-content/uploads/2025/03/nuevasbases_img.jpg',
        'Imagen completa, bloques Saber 11 y desagregación',
        'Desde 1996 hasta 2024',
        'Anuncia nuevas bases y desagregación étnica/discapacidad desde 2016; contexto de reedición del repositorio.',
        'No identifica cambios de puntajes ni fecha de entrega de los TXT locales.',
        'evidencia_oficial/nuevasbases_img.jpg')
    ref('ICALENDARIO',ICFES+'wp-content/uploads/2025/06/calendario_dataicfes.jpg',
        'Imagen completa, Fase II y lista de exámenes',
        '7 de julio',
        'Lista Saber Pro 2024, TyT 2024 y Pre Saber 2022–2024; aviso de aplazamiento de 30 de junio a 7 de julio.',
        'No incluye Saber 11 y no muestra año de lanzamiento dentro de la imagen: no certifica fechas históricas Saber 11.',
        'evidencia_oficial/calendario_dataicfes.jpg')
    ref('I2021CARGA',ICFES+'wp-content/uploads/2024/12/Informe-de-Gestion-2021-1.pdf',
        'Página PDF/impresa 146, sección 4.8',
        'En el tercer cuatrimestre del año, se realizó la carga anonimizada',
        'Informe de gestión 2021 reporta carga anonimizada de Saber 11-2021 calendario A durante septiembre–diciembre de 2021.',
        'Intervalo, sin día ni edición; no prueba la disponibilidad conjunta de ambos periodos ni los valores locales.',
        'evidencia_oficial/icfes_gestion2021.pdf')
    ref('I2023CARGA',ICFES+'wp-content/uploads/2025/04/Informe-de-rendicio%CC%81n-de-cuentas-Vf.pdf',
        'Páginas PDF 111–112 (sin folio impreso), gestión OGPI 2024',
        'Durante el primer trimestre de 2024',
        'Registra revisión/publicación de bases Saber 11 2023 A y B durante enero–marzo de 2024 y actualización de diccionarios; prepara transformación del repositorio.',
        'No fecha exacta, no primera edición identificada, no identidad con TXT locales. Lo previsto para segundo semestre no es evento efectivo.',
        'evidencia_oficial/icfes_rendicion2024.pdf')
    ref('IAGREGADOS',ICFES+'evaluaciones-icfes/saber-11/otros-resultados-examen-saber-11/',
        'Sábanas 2011–2025, tablas 2018, 2019, 2021, 2022-1, 2024 y 2025',
        'Sábanas de resultados agregados desde el 2011 al 2025',
        'Tablas actuales fechan 2018/2019/2021/2022-1 en 2025-02-26, 2024 en 2025-02-13 y 2025 en 2026-01-22.',
        'Fechas mostradas para agregados, no primeras publicaciones de bases anonimizadas. 2018-1 y 2018-2 repiten enlace rotulado 20181; no resolver por inferencia.')
    ref('IESTADISTICAS',ICFES+'estadisticas-oficiales/',
        'Alcance; Examen Saber 11, nota metodológica; Cuadros de salida',
        'Estudiantes no repitentes',
        'Agregados actuales excluyen según discapacidad, repetición y estado publicado; desagregación territorial disponible. Cuadros 2021/2022/2024 actualizados 2026-04-06 y 2023 en 2026-10-08.',
        'Producto/población distintos de la media local. No aplicar regla actual retroactivamente ni confundir Updated con primera publicación.')
    ref('I2026',ICFES+'analisis-de-datos/',
        'Informes nacionales Saber 11, 2026 y 2025',
        'Resumen preliminar de resultados del examen Saber 11° – 2026 Calendario B',
        'Se enlaza producto preliminar B 2026, mientras el conjunto local termina en 2025.',
        'No demuestra un año anual A+B comparable ni bases para conservar población; no se accedió a los resultados enlazados.')
    save_json('REFERENCIAS.json',refs)
    tree=ast.parse((ROOT/'protocolo/fuentes/configuracion.py').read_text())
    dims=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DIMENSIONES' for t in n.targets))
    tasas=[v for group in dims.values() for v in group]
    assert len(tasas)==15
    headers=list(csv.DictReader((ROOT/'experimentos_objetivo3_v2/fase1/resultados/encabezados_ipm_2025.csv').open()))
    dates={2018:None,2019:'2020-12-21',2021:'2022-04-28',2022:'2023-05-23',2023:'2024-04-19',2024:'2025-04-22',2025:'2026-04-14'}
    rows=[]
    for year in YEARS:
        for var in ['IPM',*tasas]:
            h=next(x for x in headers if int(x['anio'])==year and (x['hoja']=='IPM_Departamentos')==(var=='IPM'))
            evid='DRECALIBRACION;D2019' if year==2018 else f'D{year}'
            rows.append(dict(fuente=var,organismo='DANE',producto='Anexo departamental de pobreza multidimensional ECV',
                anio_observado=year,periodo_observado=f'ECV {year}; anual, no fecha de publicación',
                poblacion='personas residentes en hogares' if var=='IPM' else 'hogares residentes; tasa de privación',
                geografia='32 departamentos y Bogotá; dominio Total',edicion='Producto histórico CNPV 2018; edición exacta local no autenticada',
                fecha_publicacion=dates[year] or 'NO DEMOSTRADA departamental revisada 2018',
                primera_publicacion='NO DEMOSTRADA del archivo/celdas exactos',
                edicion_revisada='Recalibración 2018 divulgada 2020-07-14; nacional no basta para todas las celdas' if year==2018 else 'Revisiones exhaustivas NO DEMOSTRADAS',
                edicion_local='Anexo local 2025; nota 2026-04-14; histórico local 2024 sin diferencias según auditoría previa',
                evidencia=evid,ubicacion_local=f"Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx :: {h['hoja']} {h['celda']} año/fila13 Total; fila variable según cifras_xlsx.csv",
                correspondencia_archivo_local='Compatible en organismo/producto/año/base censal; NO DEMOSTRADA identidad de valores con edición publicada',
                estado_comprobacion='fecha de producto documentada, vintage local pendiente' if year!=2018 else 'revisión nacional demostrada; fecha primera departamental revisada pendiente',
                fecha_adquisicion='NO DEMOSTRADA',modificacion_local='METADATOS_LOCALES.json; no prueba publicación',
                limitacion='No se descargó ni cotejó anexo remoto; fecha producto no certifica cada tasa local.',fecha_consulta=CONSULTA))
    # Historical original is separate; never used to backdate revised local observations.
    rows.append(dict(rows[0],edicion='Comunicado departamental original, Censo 2005 según archivo histórico DANE',
        fecha_publicacion='2019-07-12',primera_publicacion='Comunicado fechado; primera publicación absoluta no demostrada',
        edicion_revisada='2018 recalibrado posteriormente',evidencia='D2018ORIGINAL;DRECALIBRACION',
        correspondencia_archivo_local='NO CORRESPONDENCIA acreditada: edición previa distinta',
        estado_comprobacion='antecedente de edición, excluido de certificación local',
        limitacion='No demuestra disponibilidad de tasas ni valores revisados locales en 2019.'))
    for year in YEARS:
        for period in [1,2]:
            date='NO DEMOSTRADA'
            evid='IDATA;IINVENTARIO;INUEVAS'
            lim='Inventario actual prueba cobertura nominal hasta 2024, no primera publicación/edición.'
            if year==2021 and period==2:
                date='intervalo reportado 2021-09-01/2021-12-31, calendario A';evid+=';I2021CARGA';lim='Calendario A del informe; equivalencia con periodo local/edición sin autenticar.'
            if year==2023:
                date='intervalo reportado 2024-01-01/2024-03-31, A y B';evid+=';I2023CARGA';lim='Publicación durante trimestre; no día, primera edición ni igualdad de valores.'
            if year==2025:
                evid='IDATA;IAGREGADOS';lim='Inventario enlazado no lista 2025; agregados públicos 2026-01-22 son otro producto. TXT local conocido desde auditoría 2026-10-10.'
            rows.append(dict(fuente='Saber 11 puntajes',organismo='ICFES',producto='Base anonimizada por aplicación, producto local declarado',
                anio_observado=year,periodo_observado=f'{year}{period}; no equiparar periodo y calendario individual sin documentación',
                poblacion='Base: evaluados; local: estudiante/no libertad S/grado11/seis puntajes positivos/código colegio, sin filtro calendario',
                geografia='departamento del colegio; agregado anual por registros, 33 territorios',edicion='TXT local sin identificador oficial de versión',
                fecha_publicacion=date,primera_publicacion='NO DEMOSTRADA archivo exacto',edicion_revisada='Historial de revisiones del TXT NO DEMOSTRADO; renovación repositorio documentada',
                edicion_local=f'raw_data/Examen_Saber_11_{year}{period}.txt; SHA en METADATOS_LOCALES.json',evidencia=evid,
                ubicacion_local='PROTOCOLO.md superior, población y agregación; auditoría v2 Resultado y población; METADATOS_LOCALES.json',
                correspondencia_archivo_local='Formato/producto compatibles; igualdad con edición oficial NO DEMOSTRADA',
                estado_comprobacion='publicación en intervalo, vintage pendiente' if date!='NO DEMOSTRADA' else 'fecha efectiva y vintage pendientes',
                fecha_adquisicion='NO DEMOSTRADA',modificacion_local='METADATOS_LOCALES.json; no adquisición',limitacion=lim,fecha_consulta=CONSULTA))
        rows.append(dict(rows[-1],fuente='Saber 11 media anual local',producto='prom_punt_global, reconstrucción local',
                         periodo_observado=f'{year} ambos periodos locales',edicion='Base analítica v2, recibida y congelada',
                         fecha_publicacion='NO DEMOSTRADA disponibilidad de ambas bases y transformación en corte histórico',
                         evidencia='IDATA;IAGREGADOS;IESTADISTICAS'+(';I2023CARGA' if year==2023 else ''),
                         edicion_local='experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv',
                         estado_comprobacion='agregado local trazado por auditoría previa; calendario efectivo pendiente',
                         correspondencia_archivo_local='NO ES un agregado oficial; preservar estimando local',
                         limitacion='Requiere las dos bases elegibles y cálculo reproducible disponible al corte; publicación individual/institucional insuficiente.'))
    save_csv('CALENDARIO.csv',rows)
    # Documentary calculation only; no target values read and no choice based on errors.
    # 2018 has unresolved revised departmental date; 2019 is the earliest proven dated departmental edition retained.
    releases={year:datetime.date.fromisoformat(date) for year,date in dates.items() if date}
    cuts=[]
    for target in range(2021,2026):
        for month,day,mode in [(1,1,'opción recomendada, pendiente decisión de uso'),(7,1,'alternativa; anticipación anual íntegra NO demostrada')]:
            cut=datetime.date(target,month,day)
            eligible=[y for y,date in releases.items() if date<cut]
            latest=max(eligible) if eligible else None
            cuts.append(dict(anio_respuesta=target,corte_propuesto=cut.isoformat()+'T00:00:00-05:00',tipo=mode,
                pobreza_ultimo_anio_documentado=latest,fecha_producto=releases[latest].isoformat() if latest else 'NO DEMOSTRADA',
                edad_anual_nominal=target-latest if latest else '',
                entradas_pobreza=f'IPM o quince tasas {latest}, solo SI edición y contenido históricos se autentican',
                historia_puntaje='Dos últimas medias elegibles excluyendo 2020 SOLO si ambas bases/ediciones estaban disponibles; años exactos pendientes',
                cobertura_nominal_objetivo='33 territorios; no panel exportado',cobertura_certificada='0 pares certificados por procedencia/edición pendiente; no ausencia de datos',
                evidencia=f'D{latest}' if latest else 'DRECALIBRACION',limitacion='Fechas documentan producto, no bytes ni quince celdas locales en ese corte.'))
    for observed in [2021,2022,2023,2024,2025]:
        date=releases[observed]+datetime.timedelta(days=1)
        cuts.append(dict(anio_respuesta=observed,corte_propuesto=date.isoformat()+'T00:00:00-05:00',tipo='corte documental posterior a pobreza del propio año: estimación contemporánea/reconstrucción',
            pobreza_ultimo_anio_documentado=observed,fecha_producto=releases[observed].isoformat(),edad_anual_nominal=0,
            entradas_pobreza=f'IPM o quince tasas {observed}, identidad de edición pendiente',historia_puntaje='Disponibilidad de versiones de historia y respuesta pendientes',
            cobertura_nominal_objetivo='33 territorios',cobertura_certificada='0 pares certificados; procede solo calendario documental',
            evidencia=f'D{observed}',limitacion='Corte no anticipa la respuesta académica anual ya observada; hora pública desconocida, se usa día siguiente.'))
    save_csv('CORTES_PROPUESTOS.csv',cuts)
    save_json('RESUMEN_CALENDARIO.json',dict(version='1.0',python=platform.python_version(),filas=len(rows),referencias=len(refs),
        anios=YEARS,tasas=tasas,pares_objetivo_historico=33*5,pares_certificados_historicos=0,
        significado_cero='No se certifican retrospectivamente, no significa datos inexistentes.',
        cortes=len(cuts),metodo='Fechas de productos anteriores estrictamente al corte, años 2020 excluidos; edición/celdas pendientes.',
        no_datos_externos_analiticos=True,ajustes=0,objetivo4_ejecutado=False))
    print(json.dumps({'filas':len(rows),'referencias':len(refs),'cortes':len(cuts)}))

if __name__=='__main__':
    main()
