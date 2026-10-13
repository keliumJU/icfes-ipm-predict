"""Cierre verificable propio; no ejecuta tests/modelos ni modifica antecedentes."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import nbformat
from seguridad import ROOT,OWN,E1,OUT,TEST,sha,leer,guardar,destino
from preflight import git,entorno,verificar as verificar_antecedentes
from comun import CS,GROUPS,INPUTS,CONF,SPEC,SEED,comprobar_defaults


def entry(p):
    if p.is_symlink():
        link = p.readlink().as_posix()
        return dict(tipo='symlink_fixture_rechazado',destino=link,
                    sha256_texto_enlace=hashlib.sha256(link.encode()).hexdigest())
    return dict(tipo='archivo',sha256=sha(p))


def mapping(exclude=()):
    result = {}
    for p in sorted(OWN.rglob('*')):
        name = str(p.relative_to(ROOT))
        if name in exclude:
            continue
        if p.is_symlink() or p.is_file():
            if p.is_symlink() and not p.is_relative_to(TEST):
                raise ValueError('Symlink fuera de fixture')
            result[name] = entry(p)
    return result


def conservar():
    snapshot = leer(OUT/'inventario_partida.json')
    tracked = git('ls-files','-z').split('\0')[:-1]
    assert tracked == snapshot['versionados']
    assert git('rev-parse','HEAD').strip() == snapshot['git']['head']
    assert git('branch','--show-current').strip() == snapshot['git']['rama']
    for n,state in snapshot['archivos'].items():
        p = ROOT/n
        assert sha(p) == state['sha256'],n
        assert (p.readlink().as_posix() if p.is_symlink() else None) == state['symlink'],n
    prep = leer(ROOT/'diagnostico_objetivo3_v1/REGISTRO_PREPARACION.json')
    verificar_antecedentes(prep['inventario_protegido']['sha256_versionados'])
    extra = {}
    for suffix,key in [('etapa1/resultados/controles.json','fuentes_sha256'),
                       ('etapa2/resultados/controles.json','fuentes_sha256'),
                       ('etapa2/resultados/piloto/contexto.json','fuentes_sha256')]:
        n = 'experimentos_objetivo3_v5/'+suffix
        extra[n] = verificar_antecedentes(leer(ROOT/n)[key])
    allowed = ('diagnostico_objetivo3_v1/','diseno_temporal_objetivo3_v1/',
               'experimentos_temporales_objetivo3_v1/')
    status = git('status','--short','--untracked-files=all').splitlines()
    assert all(r.startswith('?? ') and r[3:].startswith(allowed) for r in status)
    return dict(aprobado=True,versionados_intactos=len(tracked),
        diagnostico_diseno_intactos=len(snapshot['archivos'])-len(tracked),
        inventario_git_identico=True,head=snapshot['git']['head'],rama=snapshot['git']['rama'],
        otras_huellas_v5=extra,preparacion_diagnostico_versionados_cotejados=True,
        raw='Sin lectura/censo/escritura',cambios_ajenos=[],fits_panel_real=0,commit=0,push=0)


def verificar_cierre():
    name = str((OUT/'manifiesto_cierre.json').relative_to(ROOT))
    excluded = [name,str((OUT/'verificacion_cierre.json').relative_to(ROOT))]
    manifest = leer(OUT/'manifiesto_cierre.json')
    actual = mapping(excluded)
    assert actual == manifest['entregables'], 'Cobertura/huellas de cierre distintas'
    freeze = leer(OUT/'congelacion_operativa.json')
    for n,h in freeze['artefactos'].items():
        assert entry(ROOT/n) == h,n
    conservar()
    return dict(aprobado=True,entregables=len(actual),congelacion_completa=True,
        conservacion_completa=True,manifest_sha256=sha(OUT/'manifiesto_cierre.json'),
        fits_panel_real=0,piloto_autorizado=False,pendientes_indispensables_etapa1=[])


def main():
    if '--verificar' in sys.argv:
        print(json.dumps(verificar_cierre(),ensure_ascii=False))
        return
    assert leer(OUT/'preflight.json')['aprobado']
    assert leer(OUT/'reconstruccion_referencias.json')['referencias']['aprobado']
    tests = leer(OUT/'pruebas_cierre.json')
    assert tests['aprobado'] and tests['grupos_ejecutados']==17 and tests['ajustes_estimadores_inventados']==106
    notebook = leer(OUT/'notebook.json')
    assert notebook['aprobado'] and notebook['celdas_codigo_ejecutadas']==6
    assert sha(E1/'fuentes/01_controles.py')==notebook['fuente_sha256']
    assert sha(E1/'notebooks/01_controles_recencia.ipynb')==notebook['notebook_sha256']
    nbformat.validate(nbformat.read(E1/'notebooks/01_controles_recencia.ipynb',as_version=4))
    comprobar_defaults()
    for p in (E1/'fuentes').glob('*.py'):
        tree = ast.parse(p.read_text(),str(p))
        for node in ast.walk(tree):
            names = [n.name for n in node.names] if isinstance(node,ast.Import) else [node.module or ''] if isinstance(node,ast.ImportFrom) else []
            assert not any(n.startswith(('comun_v','piloto','configuracion')) for n in names),str(p)
    metadata = leer(Path(tests['directorio_inventados'])/'metadatos_modelos_inventados.json')
    assert len(metadata['ajustes_ponderados_y_uniformes'])==70
    assert all(m['origen']=='inventado' for m in metadata['ajustes_ponderados_y_uniformes'])
    assert not list(OWN.rglob('*.pkl')) and not list(OWN.rglob('*.joblib')) and not list(OWN.rglob('__pycache__'))
    guardar(OUT/'entorno_final.json',entorno())
    guardar(OUT/'configuracion_operativa.json',dict(version='1.0.0',estado='Fase1 aprobada por prompt; sin piloto',
        configuraciones=CS,grupos=GROUPS,entradas=INPUTS,ventanas=CONF['ventanas'],
        orden_familias=CONF['orden_familias'],semilla=SEED,bandas=dict(mae=.1,rmse=.1),
        recencia=SPEC['recencia'],procedimiento_primario=SPEC['procedimiento_primario'],
        entrenamiento_ponderado=True,evaluacion_seleccion='Igual peso territorio-año',
        esquema_unico='recencia_h2',routing=False,persistencia_sin_fit=True,
        limite_futuro=dict(segundos=7200,total_sin_fallos=378,disponible_ahora=False),
        fuentes_heredadas={k:SPEC['heredado'][k] for k in ('fuente_archivo','fuente_sha256','derivado_archivo','derivado_sha256','configuracion_archivo','configuracion_sha256')},
        modelos_reales=0,pesos_reales_calculados=0,piloto_autorizado=False))
    readings = [
        ('AGENTS.md','Completo'),
        ('diseno_temporal_objetivo3_v1/CONTINUIDAD_DISENO.md','Completa'),
        ('diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md','Completa; estado vigente separado de antecedentes archivados'),
        ('diseno_temporal_objetivo3_v1/PLAN_DISENO.md','Solo fase documental actual registrada; no planes operativos posteriores'),
        ('experimentos_temporales_objetivo3_v1/etapa1/PLAN_ETAPA1.md','Solo fase1 actual'),
        ('diseno_temporal_objetivo3_v1/PROTOCOLO_TEMPORAL.md','Completo, releído sin truncar'),
        ('diseno_temporal_objetivo3_v1/ESPECIFICACION_PROPUESTA.json','JSON completo procesado; herencia exacta comparada'),
        ('diseno_temporal_objetivo3_v1/EVIDENCIA_Y_DECISIONES.md','Completo'),
        ('diseno_temporal_objetivo3_v1/HISTORIA_Y_EVALUACION.md','Completo'),
        ('diseno_temporal_objetivo3_v1/PROMPT_FASE1_IMPLEMENTACION.md','1–60; además prompt completo recibido del usuario'),
        ('diagnostico_objetivo3_v1/fase1/fuentes/comun_diagnostico.py','Completo, solo lectura, nunca importado'),
        ('diagnostico_objetivo3_v1/fase1/fuentes/preflight_documental.py','Completo, solo lectura, nunca ejecutado/importado'),
        ('diagnostico_objetivo3_v1/fase1/fuentes/ejecutar_diagnostico.py','170–225; búsqueda acotada de referencias'),
        ('experimentos_objetivo3_v5/etapa1/fuentes/comun_v5.py','Completo, solo lectura'),
        ('experimentos_objetivo3_v5/etapa2/fuentes/motor.py','Completo, solo lectura'),
        ('experimentos_objetivo3_v5/etapa2/fuentes/worker.py','Completo, solo lectura'),
        ('experimentos_objetivo3_v2/fase2/fuentes/comun.py','85–120; selección heredada'),
        ('experimentos_objetivo3_v2/fase2/fuentes/congelar.py','Completo, serialización/defaults; solo lectura'),
        ('experimentos_objetivo3_v5/etapa2/fuentes/verificar.py','Búsqueda acotada referencias/v3/persistencia, no completo'),
    ]
    guardar(OUT/'lecturas.json',dict(archivos=[dict(archivo=n,alcance=a,sha256=sha(ROOT/n)) for n,a in readings],
        datasets='Única fuente/derivado y dos CSV de referencia completos mediante código; solo integridad, sin raw',
        manifiestos='Mapas completos en huellas_antecedentes y conservación; única excepción continuidad v5 etapa1 en su commit real',
        pdf_paginas=0,web=0,pendiente='Lecturas operativas fase2 solo bajo otra autorización'))
    guardar(OUT/'registro_hallazgos.json',dict(fecha_cliente='2026-10-11',timezone='America/Bogota',
        autorizacion='Prompt humano enviado expresamente: semivida2 y fase1, no piloto',
        hallazgos=[
            dict(id='E1',evidencia='preflight.json/entorno.json',impacto='Permite controles en el entorno contratado',
                 alternativa='Revalidar versiones/54paquetes/pipcheck sin sustituir',resolucion='Aprobado antes uso y al cierre'),
            dict(id='E2',evidencia='reconstruccion_referencias.json',impacto='Evita cambios silenciosos de datos/territorios/objetivo',
                 alternativa='Reconstrucción exacta en memoria con regla heredada',resolucion='231/33/198 exactos, intervalo2 sin anualizar'),
            dict(id='E3',evidencia='reconstruccion_referencias.json:referencias',impacto='Referencias idénticas no duplican evidencia',
                 alternativa='Cotejo independiente contra previo, sin volver a ajustar',resolucion='165 pares exactos'),
            dict(id='E4',evidencia='pruebas.json:test_17',impacto='Excepción EOF de caída impedía cerrar suite',
                 alternativa='Incluir excepción esperada en comprobación; conservar fallo',resolucion='pruebas_finales.json y pruebas_cierre.json aprobados'),
            dict(id='E5',evidencia='pruebas_cierre.json y fixtures finales',impacto='Compatibilidad ponderada/serial validada solo en inventados',
                 alternativa='Pruebas completas/scaler independiente/dobles/metadata',resolucion='17 grupos, defaults36, 5comprobacionesglobales, sin evidencia de eficacia'),
        ],
        incidencias_lectura=['Salida inicial protocolo/JSON truncada: protocolo releído completo y JSON íntegro procesado',
                            'Clave informativa candidatos inexistente en v5: usar configuraciones, sin alterar archivos',
                            'Ruta informativa predicciones_externas bajo piloto inexistente: fuente real está en resultados/'],
        antecedentes_archivados='No reabiertos sin conexión nueva; no criterios históricos inventados',
        hipotesis='Eficacia de recencia pendiente; ninguna evaluación sobre el panel real',
        resultados_historicos='V5 meta no satisfecha intacta; Guainía238vs404/21.012106puntos conserva advertencia',
        fits_panel_real=0,ajustes_estimadores_inventados_totales=sum(leer(OUT/n)['ajustes_estimadores_inventados'] for n in
            ('pruebas.json','pruebas_finales.json','pruebas_cierre.json'))+notebook['ajustes_inventados'],
        modelos_historicos_cargados=0,modelos_guardados=0,ledger_real=0,instalaciones=0,descargas=0,commit=0,push=0))
    guardar(OUT/'conservacion_final.json',conservar())
    guardar(OUT/'aceptacion_etapa1.json',dict(aprobado=True,estado='COMPLETA SIN FITS REALES',
        pruebas_finales=17,notebook_celdas_ejecutadas=6,pendientes_indispensables=[],
        pendientes=['Enviar prompt separado fase2','Revalidar entorno/integridad y activar ámbito propio autorizado etapa2',
                    'Evaluar exploratoriamente recencia; eficacia todavía desconocida',
                    'Confirmación independiente y disponibilidad operacional requieren otra autorización/fuentes'],
        etapa2_autorizada=False,etapa3_v5=False,fit_panel_real=0))
    guardar(OUT/'congelacion_operativa.json',dict(version='1.0.0',antes_de_todo_fit_real=True,
        alcance='Código/defaults/entradas/pesos/entorno/tests íntegros etapa1; no autorización de piloto',
        artefactos=mapping(),diseno_sha256=sha(ROOT/'diseno_temporal_objetivo3_v1/ESPECIFICACION_PROPUESTA.json'),
        fits_panel_real=0,piloto_autorizado=False,regla_cambios='Revalidar y recongelar cualquier cambio antes de fit real autorizado'))
    excluded = [str((OUT/n).relative_to(ROOT)) for n in ('manifiesto_cierre.json','verificacion_cierre.json')]
    guardar(OUT/'manifiesto_cierre.json',dict(version='1.0.0',etapa1_completa=True,piloto_autorizado=False,
        entregables=mapping(excluded),exclusiones_autorreferencia=excluded,
        fits_panel_real=0,pendientes_indispensables=[]))
    result = verificar_cierre()
    guardar(OUT/'verificacion_cierre.json',result)
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
