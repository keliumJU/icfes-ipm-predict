"""Aceptación, conservación y cierre SOLO diagnóstico. --verificar es solo lectura.
No ajustes/deserialización/runners/cierres históricos/commit/push.
"""
from comun_diagnostico import *
from preflight_documental import verify as verify_hashes, git
import ast


def validate_artifacts():
    env = environment()
    audit = read_json(OUT / 'auditoria_diagnostico.json')
    tests = read_json(OUT / 'pruebas_inventadas/pruebas.json')
    nb = read_json(OUT / 'verificacion_notebook_diagnostico.json')
    assert audit['aprobado'] and tests['aprobado'] and nb['aprobado']
    assert audit['internos_originales'] == 11880 and audit['internos_unicos'] == 4752
    assert audit['externas'] == 1155 and audit['candidatos'] == 36 and audit['metricas_internas'] == 144
    assert len(list(TABLES.glob('*.csv'))) == 25 and len(list(FIGS.glob('*.png'))) == 5
    assert len(nb['celdas']) == 6 and all(c['ejecutada'] and not c['error'] for c in nb['celdas'])
    assert nb['notebook_sha256'] == sha(F1 / 'notebooks/01_diagnostico.ipynb')
    assert nb['fuente_sha256'] == sha(F1 / 'fuentes/01_diagnostico.py')
    assert nb['generador_sha256'] == sha(F1 / 'fuentes/generar_notebook.py')
    for record in tests['fuentes']:
        assert sha(ROOT / record['archivo']) == record['sha256']
    for p in (F1 / 'fuentes').glob('*.py'):
        tree = ast.parse(p.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {'fit', 'fit_transform', 'partial_fit', 'fit_predict'}
            if isinstance(node, ast.Import):
                assert not any(n.name.split('.')[0] in {'joblib', 'pickle', 'cloudpickle'} for n in node.names)
            if isinstance(node, ast.ImportFrom):
                assert (node.module or '').split('.')[0] not in {'joblib', 'pickle', 'cloudpickle', 'piloto', 'worker', 'motor'}
    archived = read_json(OUT / 'antecedentes_entorno_ausente/index.json')
    for name, r in archived['archivos'].items():
        assert sha(ROOT / r['copia']) == r['sha256']
    old_manifest = read_json(ROOT / archived['archivos']['diagnostico_objetivo3_v1/fase1/resultados/manifiesto_incompleto.json']['copia'])
    for name, digest in old_manifest['artefactos_sha256'].items():
        assert archived['archivos'][name]['sha256'] == digest
    # Cotejo de métricas externas históricas SOLO sobre los siete procedimientos existentes.
    saved = csv(E2 / 'resultados/metricas.csv')
    current = csv(TABLES / 'metricas_externas.csv')
    external_checks = []
    for r in current.itertuples():
        if r.periodo in ['2021_2024', '2025']:
            continue
        period = '2021–2025' if r.periodo == 'total' else r.periodo.removeprefix('anio_')
        old = saved[(saved.procedimiento == r.procedimiento) & (saved.periodo == period)]
        assert len(old) == 1 and old.n.iloc[0] == r.n
        diffs = {k: abs(getattr(r, k)-float(old.iloc[0][k])) for k in ['mae', 'rmse', 'sesgo']}
        assert max(diffs.values()) <= 1e-12
        external_checks.append(dict(procedimiento=r.procedimiento, periodo=period, n=int(r.n), **diffs))
    assert len(external_checks) == 273
    global_now = current[(current.procedimiento == 'global') & (current.periodo == 'total')].iloc[0]
    meta = read_json(E2 / 'resultados/meta.json')
    assert global_now.mae == meta['mae_v5'] == 3.429267191379531
    assert meta['meta_satisfecha'] is False and meta['mejora_porcentual_exacta'] == 0
    hypotheses = csv(TABLES / 'matriz_hipotesis.csv')
    assert len(hypotheses) == 7 and not hypotheses[['ubicacion', 'n', 'favor', 'contra', 'impacto', 'alternativa', 'resolucion', 'pendiente']].isna().any().any()
    assert set(hypotheses.estado) == {'apoyada descriptivamente', 'contradicha', 'insuficientemente evaluada'}
    return dict(aprobado=True, controles_inventados=tests['n_grupos'], notebook_celdas_reales=6,
                graficos=5, tablas=25, cotejos_externos_historicos=len(external_checks),
                max_diferencia_externas=max(max(r[k] for k in ['mae', 'rmse', 'sesgo']) for r in external_checks),
                entorno=env['python'], paquetes=54, hipotesis=7, alternativas=4,
                fits=0, modelos_cargados=0, meta_v5_intacta=True, pendientes_indispensables=[])


def close():
    assert not (OUT / 'manifiesto_cierre.json').exists()
    accepted = validate_artifacts()
    prep = read_json(OWN / 'REGISTRO_PREPARACION.json')
    old_cont = (OWN / 'CONTINUIDAD_DIAGNOSTICO.md').read_text()
    index = read_json(OUT / 'antecedentes_entorno_ausente/index.json')
    old_copy = ROOT / index['archivos']['diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md']['copia']
    assert old_copy.read_text() == old_cont
    text = f"""# Continuidad diagnóstico objetivo3 v1 — fase1 descriptiva cerrada

Fecha cliente2026-10-11,America/Bogota. Autorización:prompt diagnóstico enviado
expresamente por usuario;posteriormente `si porfavor continua` autorizó reconstruir
el entorno exacto con instalaciones/descargas necesarias y seguir sin nuevosfits.
Se ejecutaron A–E sobre guardados;aceptaciónplan§4 aprobada. No etapa3v5/excepción
metaNOsatisfecha,noexperimento nuevo/notebookpersonal/simulación/objetivo4/ajustefinal.

## Partida, entorno y conservación

HEAD75c3a25182af363f47b0d743820f99084e18fed5,asunto `etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora`,
rama codex/objetivo3-v5-mae/ascendencia/trabajoposterior comprobados;sinreset/checkout.
Cuatrodocumentospreparación no versionados;3huellas documentales válidas alinicio.
29640versionados protegidos intactos antes análisis y al cierre;fuentes/selecciones/
manifiestos/índice2174/congelaciones/hashmodelos íntegros,sin regenerar ni deserializar.
Continuidadhistóricav5etapa1 enGit109797407d75d2097e5b71f8bcef3fc266bc61d2;
no excepciónparaotrasrutas. Solo propiosfase1/continuidad yentornoautorizado/tmp.

Entorno inicial ausente fue bloqueo real,ahora RESUELTO;primer cierre incompleto
con23copias exactas en fase1/resultados/antecedentes_entorno_ausente/index.json,
manifestaciónhistoricapropia verificada contra esas copias. Antecedenteíntegroabajo.
Runtime localPython3.12.14;54wheelslock recuperados decachélocalpip,bytesintactos,
instalaciónoffline autorizada,sinred/descargafuentedatos. Sklearn1.9.1/54paquetes
exactos/pipcheckaprobados. Pip herramientas excluido del lock igual que contrato.
Entornoautorizado=/tmp/icfes-v2-fase2-venv;PYTHONDONTWRITEBYTECODE=1,semilla20261010
reservada,no aleatoriedad aplicada. Evidenciarestauracion_entorno yentorno_diagnostico.

## Acuerdos y ejecución actual

Usuario:intactos ESTUDIANTE/no libertadS/grado11/seispuntajespositivospresentes/
sincalendario/mediarecibida/geografíacolegio/pesoigualterritorio-año/conteostrazabilidad;
2020excluido/2018historial/2021previo2019/sinanualizar/objetivooriginal/GRUPOSv5exactos.
Unión18entradasprimeraaparición;añocódigointervalo solo descripción/llaves.
Fuenteúnicav2 SHA{SOURCE_SHA},derivadov5 SHA{PANEL_SHA},
reconstruidos en memoria mismos campos/orden/llaves/valores:231filas/33territorios/
198cambios,sin raw/fuentesextra/no reescritura. Criterios/meta/selecciones/ledgersintactos.

Nuevas implementaciones:fuentespropiascomunes/reconstrucción/auditorCSVmetadata/
estadísticadescriptiva/matrizE/notebooklector/generador/cierre;sinimportsoperativos.
Cuantileslineales/ddof1/Pearson/Spearmanrangosmedios/nexplícito/no p-valores/importancias/
selecciónautomática. MAEfsum/RMSE/sesgo/deltasdirección/magnitud porcandidato/familia/
grupo/ventana/año/territorio;sin poolingdeconfiguracionescomoobservacionesindependientes.
Copias11880originales exactas y firmasdeentrenamiento/params/semilla/versiones:
4752únicas comprobadas=36×4×33,representantemenorexterno,linaje11880. Cuatrovalidaciones
únicas2021–2024,no10añosindependientes;análisisoriginalporventanaconservado.
144registrosinternosrecalculados,máxdiferencia2.6645352591003757e−15≤1e−12rtol0;
CSVvalores exactos,intfloat0aceptado,sin tolerancia. 187resúmenesporracionalesFraction,
273métricasexternashistóricas cotejadas.1155externas=7×165intactas;35ajustadossin
externasno fabricadas.360artefactos/350metas ajustadasauditadas,modelossolobyteshash.

## Hallazgos descriptivos e impacto

Ubicaciones/llaves/n/favor/contra/alternativas/resoluciones completas en matriz_hipotesis.csv
(7filas),alternativas_y_pruebas_futuras.csv(4),registro_hallazgos e informe.
2019:33cambiosnegativos,2021:23negativos,2022–2024:31positivoscadaaño,2025:27positivos;
23/33cambiansigno2021→2022;2021intervalo2preservado. Distribucionesvarían(H1apoyada
descriptivamente),sin causa/rupturadefinitiva. Contrastestrain/validn33–132/33 completos.
0entradasconstantes/0paresidénticos,no finitos0;18entradas/anualn33/globaln198.
Spearmancambio_ipm-objetivo2019−0.0254/2023−0.3326/2025+0.3891;previo–IPMagregado−0.7650.
Signouniforme/constantesduplicadascontradichos(H2/H3);redundanciacomocausa no probada(H4).
Correlaciónno demuestra capacidadpredictiva/inutilidadintrínseca;sinvariableseliminadas.

Internasúnicas132pares/candidato:MAEpersistencia3.7249352319645874;35ajustados
4.758036518…a5.761295…;todospeoresenconjunto. Por año0/35superioresen2021/2022/2023,
33/35en2024:patrónretrospectivo,nuevo ganador no autorizado. Sesgosajustados−5.2850a−4.1561,
dirección34.09%–53.03%;direcciónpersistencia0bajosignoexacto,pero menorMAE. H5errores
descriptivamenteapoyada,no causadefinitiva. Eficaciarecencia/máshistoria insuficientemente
evaluada(H6);H7conservarreferenciapersistenciaapoyada para guardados,noóptimouniversal.
ExternasMAE3.429267191379531/RMSE4.314920647368904/sesgo−2.0960105973100562,
sietepersistencias/deltaMAE0;metaNOsatisfechav5intacta. Resultadosactuales son recálculos
de guardados,no reproduccionesfits. Ningún punto de partida mejor demostrado.

Alternativasexpresas:recencia/máshistoria justificadas comohipótesispara estudiar,
no eficacia; simplificación no remediosuficiente;conservarpersistenciareferencia.
Futuroprotocolo prospectivo separado debe discriminar historia/memoria/aporteincremental
con referencias/evaluaciónacordadas y evidencia temporal independiente. Sin grilla/
hiperparámetros,nuevoexperimento,efectoscausales ni promesa5%.

## Entregables, pruebas y pendientes

25CSVcompletos/5PNGdescriptivosrevisadosvisualmente;README/protocolo/informe/registro;
preflight/entorno/pruebas9gruposinventados/auditoría/lecturas/notebookaceptación/
conservación/manifiesto propio. Notebook01_diagnostico.ipynb desde fuentePythoneditable
y generadornbformat,6celdas realmenteejecutadasexecPython/5PNGguardados,sin kernel/fit.
Todo deterministicoynorecopiarresultadosinexistentes/datos personales.

Incidenciaspropiasresueltas:baseíndicerelativopiloto/ (registropreliminarconservado),
pd.NAcomparación por máscarasexactas antesestadísticas (ensayoarchivo),paréntesis
inicialantescálculos,lecturasconjuntas truncadascorregidas porseccionesacotadas.
Revisión final corrigióconteodocumental25tablas yprecisótrain2019/2021vsvalid2022
enH1 antescerrar,sin modificar datos/métricas/criterios.Registrodocumentalcompleto.
PDF0páginas,referenciashistóricasdistinguidas. Antecedentes históricos archivados no
reabiertos sin nueva conexión;no inventarcriterios ni cerrarcontrolirresuelto.

Sin pendientesindispensables de integridad/aceptaciónfase1. Pendientescientíficos:
eficaciaalternativas/capacidadpredictivafutura/causas,confirmaciónindependiente y
disponibilidadoperacional. Necesitan protocolo/autorizaciónseparados,noautoavance.
Guainía238vs404/21.012106puntos(evidenciahistóricav2/fase1/resultados/diagnostico_medias_disponibles.csv),
procedencialocalnoautenticada,IPMhogares/alumnos,colegio/residencia/enlaceecológico,
dependencia temporal-territorial/pocosañospreservados.2021–2025vistos:exploratorio,
sinconfirmaciónindependiente/causalidad/pronósticoanticipadodemostrado.
Nuevosfits0/modeloscargados0/commits0/push0/simulación0/objetivo4no iniciado.

---

## Antecedente íntegro de estado incompleto y preparación — ya superado

"""
    # Evitar cifras aproximadas mal transcritas: resumen exacto obtenido de tablas.
    metrics = csv(TABLES / 'metricas_internas_unicas.csv')
    q = metrics[(metrics.periodo == 'total') & (metrics.id != 'persistencia')]
    text = text.replace('4.758036518…a5.761295…', f'{q.mae.min():.15g}a{q.mae.max():.15g}')
    (OWN / 'CONTINUIDAD_DIAGNOSTICO.md').write_text(text + old_cont)
    assert (OWN / 'CONTINUIDAD_DIAGNOSTICO.md').read_text().endswith(old_cont)
    readings = read_json(OUT / 'lecturas.json')
    write_json(OUT / 'lecturas_finales.json', dict(antecedente_lecturas_iniciales=readings,
        nuevas_lecturas=['v5etapa1/preparar.py:reconstrucción/entorno en lectura',
                        'v3comun_v3.py:historial/ventanas leído sin importar',
                        'v4comun_v4.py:1–105,GRUPOS/historial en lectura',
                        'v5etapa2/verificar.py:1–190,piloto.py:105–185 lectura de contrato sin ejecutar',
                        'configuraciones36/defaults/grupos/ventanas completosJSON',
                        '350ajuste.json y10calculo.json internos completos;entradas/predicciones360CSV',
                        '5selecciones/meta/contexto/entorno/273métricas históricas seleccionadas'],
        pdf_paginas_actuales=0, planes_consultados='Solo planpropio1–5;no planes entrenamiento posteriores',
        semantica_actual='Datos/predicciones/parametrización/linaje auditados por fuentespropias',
        lecturas_historicas='AdvertenciasGuainía/local/IPM heredadas;sin lectura PDF nueva ni nuevo cálculo casos',
        pendientes_lectura='NingúnPDFnecesario para este alcance;no autenticaciónfuentesoriginales'))
    write_json(OUT / 'revision_visual.json', dict(aprobado=True, graficos=[
        dict(archivo=str(p.relative_to(ROOT)), sha256=sha(p), revisado=True, observacion='Etiquetas/unidades/n legibles;figura completa')
        for p in sorted(FIGS.glob('*.png'))], metodo='view_image:inspección visual de cinco PNG reales'))
    write_json(OUT / 'incidencias_finales.json', dict(incidencias=[
        'Sintaxisparéntesis inicial:resuelta antes cualquierescrituraestadística',
        'Nullablepd.NA:ensayoentorno archivado,comparaciónmáscarasexactas/pruebas aprobadas',
        'Baseíndicerelativa:preflightpreliminarconservado/revisiónfinalexacta',
        'Documento conteo25tablas=22A–D+3E/resumen yH1train2019/2021vsvalid2022 corregidos antescierre'],
        impacto='Sin cambios a datos,criterios,métricasguardadas o fits;sin incidencias abiertas'))
    write_json(OUT / 'aceptacion_final.json', dict(**accepted, fase_completa=True,
        conservacion_a_verificar='conservacion_final.json', estado='Diagnóstico descriptivo completo,ningún punto de partida mejor validado',
        permisos_excepcion='Usuario autorizó reconstruir entorno;instalaciónoffline/caché,ninguna descarga analítica',
        pendiente_cientifico=['eficaciarecencia/simplificación/máshistoria', 'causas', 'confirmaciónindependiente'],
        nuevo_experimento=False, notebook_personal=False, etapa3v5=False, commits=0, push=False))
    protected = verify_hashes(prep['inventario_protegido']['sha256_versionados'])
    assert protected['aprobado']
    tracked = set(git('ls-files', '-z').split('\0')) - {''}
    assert tracked == set(prep['inventario_protegido']['sha256_versionados'])
    assert git('rev-parse', 'HEAD').strip() == prep['commit_partida']
    status = git('status', '--porcelain', '--untracked-files=all').splitlines()
    assert all(line[3:].startswith('diagnostico_objetivo3_v1/') for line in status)
    # La conservación inicial está archivada; este archivo pasa a ser cierre vigente propio.
    conservation = dict(aprobado=True, versionados_intactos=protected['n'], inventario_git_identico=True,
        head=prep['commit_partida'], rama=git('branch', '--show-current').strip(),
        cambios_git_fuera_diagnostico=[], continuidad_propia_antecedente_integro=True,
        sha_antecedente_continuidad=sha(old_copy), snapshot_incompleto_copias=23,
        fuentes_panel_derivado_selecciones_modelos_ledgers_atributos_intactos=True,
        raw_ignorado='No censo binario;ninguna escritura', fits=0, modelos_deserializados=0,
        entorno_y_wheels_tmp='Única excepción de escritura fuera de diagnóstico autorizada por usuario',
        descargas_red=0, commits=0, push=False)
    destination(OUT / 'conservacion_final.json').write_text(json.dumps(conservation, ensure_ascii=False, indent=2)+'\n')
    excluded = {OUT / 'manifiesto_cierre.json', OUT / 'verificacion_cierre.json'}
    artifacts = {str(p.relative_to(ROOT)): sha(p) for p in sorted(OWN.rglob('*'))
                 if p.is_file() and p not in excluded and not p.is_symlink()}
    write_json(OUT / 'manifiesto_cierre.json', dict(version='1.0', fase='diagnostico_objetivo3_v1/fase1',
        completa=True, aceptacion_plan4=True, commit_partida=prep['commit_partida'],
        entregables_sha256=artifacts, exclusiones_autorreferencia=['manifiesto_cierre.json','verificacion_cierre.json'],
        artefactos_temporales='Entorno/wheels registrados por versión/SHA enrestauracion_entorno;sin garantizar permanencia/tmp',
        fits=0, modelos_cargados=0, pendientes_indispensables=[], pendientes_cientificos=accepted.get('pendientes_cientificos', ['eficaciaalternativas/causas/confirmación']),
        nuevo_experimento=False, commits=0, push=False))
    result = verify_close()
    write_json(OUT / 'verificacion_cierre.json', result)
    print(json.dumps(result, ensure_ascii=False))


def verify_close():
    manifest = read_json(OUT / 'manifiesto_cierre.json')
    result = verify_hashes(manifest['entregables_sha256'])
    assert result['aprobado']
    prep = read_json(OWN / 'REGISTRO_PREPARACION.json')
    current = verify_hashes(prep['inventario_protegido']['sha256_versionados'])
    assert current['aprobado'] and git('rev-parse', 'HEAD').strip() == prep['commit_partida']
    assert sha(SOURCE) == SOURCE_SHA and sha(PANEL) == PANEL_SHA
    assert read_json(OUT / 'aceptacion_final.json')['fase_completa']
    return dict(aprobado=True, entregables_verificados=result['n'], protegidos_verificados=current['n'],
                manifiesto_sha256=sha(OUT / 'manifiesto_cierre.json'), modo='Solo lectura;sin análisis/fits/controles nuevos',
                fase_descriptiva_completa=True, nuevo_punto_partida_mejor_demostrado=False,
                fits=0, modelos_cargados=0, commits=0, push=False)


if __name__ == '__main__':
    if '--verificar' in sys.argv:
        print(json.dumps(verify_close(), ensure_ascii=False))
    else:
        close()
