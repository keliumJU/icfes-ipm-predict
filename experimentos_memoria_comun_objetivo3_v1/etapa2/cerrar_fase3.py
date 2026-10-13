"""Cierre fase3 incluso incompleto; --verificar solo lectura y cero fits."""
from comun import *
from congelar import verify_freeze
from panel import validated_panel
from runner import Ledger
from verificar import validate_outputs

def verify():
    manifest=load(HERE/'MANIFIESTO_FASE3.json'); errors=[]
    for p,h in manifest['entregables_sha256'].items():
        if digest(safe_path(HERE,p))!=h: errors.append(p)
    current={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
    assert current-set(manifest['exclusiones_autorreferencia'])==set(manifest['entregables_sha256'])
    assert digest(HERE.parent/'CONTINUIDAD_EXPERIMENTAL.md')==manifest['continuidad_actual_sha256']
    preserved=HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md'
    prior=load(E1/'MANIFIESTO_FASE2.json')['entregables']['CONTINUIDAD_EXPERIMENTAL.md']
    assert digest(preserved)==prior['sha256']
    assert not errors and conservation()['aprobado'] and environment()['aprobado']
    acceptance=load(HERE/'ACEPTACION_FASE3.json')
    if acceptance['completa']:
        verify_freeze(); assert all(acceptance['controles'].values())
        assert load(HERE/'resultados/piloto/ledger.json')['closed']
    result={'aprobado':True,'completa':acceptance['completa'],'huellas':len(manifest['entregables_sha256']),
            'diferencias':errors,'conservacion':conservation(),'modo':'lectura; sin fits/escrituras'}
    print(json.dumps(result)); return result

def main():
    if (HERE/'MANIFIESTO_FASE3.json').exists(): raise IntegrityError('Cierre existente; usar --verificar')
    env=environment(); fresh('ENTORNO_CIERRE_FASE3.json',env)
    cons=conservation(); fresh('CONSERVACION_FASE3.json',cons)
    controls={'entorno_exacto':env['aprobado'],'conservacion_integra':cons['aprobado']}
    failed=(HERE/'resultados/INCOMPLETO.json').exists()
    if not failed and (HERE/'resultados/VALIDACION_PILOTO.json').exists():
        freeze=verify_freeze(); levels,proof=validated_panel()
        state=load(HERE/'resultados/piloto/ledger.json')
        ledger=Ledger('resultados/piloto',state['context'])
        data=load(HERE/'resultados/piloto/salidas.json')
        validation=validate_outputs(data,levels,ledger)
        fresh('VALIDACION_CIERRE_FASE3.json',validation)
        # Cotejo exacto independiente de CSV guardado frente filas de salidas verificadas.
        for key,name in [('internal','predicciones_internas_originales'),('external','predicciones_externas'),('records','registros_seleccion'),('unique','predicciones_internas_unicas')]:
            rel='resultados/control_csv/'+name+'.csv'; csv_write(rel,data[key])
            numerics=tuple(k for k,v in data[key][0].items() if type(v) in (int,float))
            exact_csv(HERE/rel,HERE/('resultados/'+name+'.csv'),numeric=numerics)
        note=load(HERE/'ACEPTACION_NOTEBOOK.json')
        import nbformat
        nb=nbformat.read(HERE/'01_resultados_piloto.ipynb',as_version=4); nbformat.validate(nb)
        notebook=(note['aprobado'] and digest(HERE/'01_resultados_piloto.ipynb')==note['notebook_sha256']
            and [c.execution_count for c in nb.cells if c.cell_type=='code']==[1,2] and all(c.outputs for c in nb.cells if c.cell_type=='code'))
        controls.update(congelacion_probada_antes_de_fits=True,panel_referencias_exactas=proof['aprobado'],
            cobertura_contextos_scales_seleccion_linaje=validation['aprobado'],CSV_exactos=True,global_cinco_comprobaciones=True,
            notebook_lector_validado=notebook,presupuesto_valido=state['used']<7200 and not state['exhausted'] and state['retries']<=1)
    else:
        controls['piloto_integro']=False; ledger=None; data=None; validation=None
    complete=all(controls.values())
    pending=[k for k,v in controls.items() if not v]
    status='COMPLETA' if complete else 'INCOMPLETA'
    meta=load(HERE/'resultados/meta.json') if complete else None
    text=f'''# Fase3 — piloto exploratorio {status}

2026-10-11 America/Bogota. Autorización humana exclusiva fase3; fase1 aprobada/fase2 congelada revalidadas. Orden/criterios/entradas/salidas/entorno/semilla en PROTOCOLO_ETAPA2.md. Cierre con controles indispensables {controls}; pendientes {pending}. Resultado real: {meta}. No se cambia primario por mejor política externa.

Evidencia: resultados/piloto/ledger.json y jobs por candidato/ventana; solicitudes solo historia anterior, X/y/llaves/d/c/r/defaults/fechas/unidades/semilla/versiones/scaler/coef/advertencias/tiempos/estados/huellas. Tablas1320internas/16registros/825externas/528únicas condicionadas, linaje y cinco comprobaciones globales únicamente si cobertura íntegra. VALIDACION_CIERRE_FASE3.json y control_csv cotejan guardados sin fits; aceptación/manifiesto/conservación independientes. Notebook lector de resultados desde fuentes Python, cero fits adicionales. Nunca se importaron runners ni cargaron modelos históricos.

Conservación: {cons['protegidos']} archivos protegidos, GitHEAD75c3a25182af363f47b0d743820f99084e18fed5/rama codex/objetivo3-v5-mae intactos; originales/etapa1/diseño intactos. Continuidadfase2 previa íntegra en antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md; referencias históricas se mantienen en su commit/copia reales. Incidencia preflight001 preservada y corregida antesfit, sin cambio de entorno/criterios. Verificar en lectura: PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python experimentos_memoria_comun_objetivo3_v1/etapa2/cerrar_fase3.py --verificar.

Todos2021–2025vistos: exploratorio sin confirmación independiente ni causalidad; procedencia local no autenticada, Guainía238vs404/21.012105832431985puntos histórica v2 filas57y90, IPMhogares-alumnos, colegio-residencia, ecología, dependencia/pocos años y común1fila preservados. Fase4 requiere autorización separada; confirmación/disponibilidad requieren evidencia nueva fuera alcance. Sin nuevas fuentes/instalación/commit/push/modelo final/notebook personal/simulación/objetivo4/avance automático.
'''
    (HERE/'README.md').write_text(text)
    continuity=f'''# Continuidad experimental memoria/común — fase3 {status}

2026-10-11 America/Bogota. Envío humano autorizó exclusivamente fase3 y fits predefinidos. Diseño aprobado en fase2; lectura inicial continuidad/AGENTS, plan únicamente decisiones comunes líneas1–15 y fase3 líneas85–105, protocolo/documental fase1 completo y protocolo implementaciónetapa1 completos. Antecedentes vigentes diagnóstico líneas1–106, temporal vigente y v5 líneas1–98, histórico real y copia temporal registrados. Fase2 anterior íntegra en etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md, SHA en etapa2/resultados/partida.json, coincide manifiesto original. No modificar etapa1/diseño.

Preflight anterior234huellas/31010protegidos válido en lectura antes etapa2; nueva conservación{cons['protegidos']}protegidos/29640versionados. GitHEAD75c3a25182af363f47b0d743820f99084e18fed5/asunto etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora/rama codex/objetivo3-v5-mae/ascendencia/sin posteriores comprobados. Nueve manifiestos históricos; v5etapa1 en commit109797407d75d2097e5b71f8bcef3fc266bc61d2; temporal solo texto/huella preservados partida etapa2. Fuentesv2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3/derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc intactos; panel completo por bloques y tres referencias165pares cotejados exactos. Python3.12.14/sklearn1.9.1/54lock/pipcheck/PYTHONDONTWRITEBYTECODE=1/semilla20261010 exactos, sin instalar.

Decisiones usuario/documentales intactas: población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario/media recibida/geografía colegio/2020excluido/2018historial/dsin anualizar/2021externafija/165pares/meta5%/igualpeso.2019historial sin respuesta con lag inexistente. Cuatro candidatos0/1/1/2entradas, Pipeline defaults congelados, común1fila/territoriales33por año, un año permitefit/cero respalda, máximo previo anterior sin inventar2020. Selección únicamente internas/bandas0.1/entradas/orden; primario global predefinido, políticas individuales diagnósticas sin rescate.

Orquestación propia probada con niveles inventados y congelada antesfit; reutiliza motor/integridadetapa1, sin runners/modelos históricos. Runner serial terminable/ledger persistente/7200nuevo/cota46/un retry máximo infraestructura/numérico inelegible/caída pendiente agota, sin reinicio/ampliación. X/y/llaves/d/c/r/fechas/unidades/scaler/defaults/semilla/versiones/advertencias/huellas/tiempos/estados/predicciones/selecciones auditables. Pruebas y resultados sintéticos separados de fits reales. Incidencia propia preflight001 por nombres defaults archivada/resuelta antesfit, no diferencia real de entorno ni cambio decriterios.

Resultados REALES de esta fase: {meta}. Validación indispensable: {validation}. Controles cierre {controls}; pendientes {pending}. Resultados históricos se conservan y no cuentan como fits actuales. Originales1320/selecciones16/externas825/únicas528/linaje y cinco global checks solo se aceptan con cobertura íntegra. Repeticionesatol1e-10/rtol0; CSVexactos/0intfloat/rechazo1e-11. Notebooklector dos celdas ejecutadas desde fuente/generadorPython y nbformat, sinfit/personales; ningún modelo final.

Impacto: piloto verifica las hipótesis con criterios fijos; no ajusta reglas para mejorar métricas. Alternativa verificable dentrofase3 fue ejecutar cuatro contrastes completos y comprobar global; evidencia en VALIDACION_CIERRE_FASE3/meta/tablas/ledger. Auditoría interpretativa fase4 PENDIENTE, no automática. Todos2021–2025vistos: exploratorio sin confirmación independiente/causalidad/pronóstico anticipado demostrado. Procedencia local no autenticada/Guainía238vs404 y21.012105832431985puntos histórica v2filas57y90/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años/común1fila activos. No reabrir incidencias históricas archivadas sin evidencia nueva.

Cierre aceptación/manifiesto/conservación/README/notebook/continuidad verificables en etapa2; verificar con cerrar_fase3.py --verificar, lectura y cerofits. Falta/diferencia entorno futura exige consultar sin sustituir/instalar. Sin nuevasfuentes/instalación/commit/push/modelofinal/notebookpersonal/simulación/objetivo4/fase4/avanceauto. Saldo no reutilizable ni ampliable; ledger cerrado propio.
'''
    (HERE.parent/'CONTINUIDAD_EXPERIMENTAL.md').write_text(continuity)
    if ledger:
        ledger.close(); state=ledger.state
        controls['presupuesto_valido']=state['used']<7200 and not state['exhausted']
        complete=all(controls.values()); pending=[k for k,v in controls.items() if not v]
    else: state=load(HERE/'resultados/piloto/ledger.json') if (HERE/'resultados/piloto/ledger.json').exists() else None
    fresh('ACEPTACION_FASE3.json',{'completa':complete,'controles':controls,'pendientes_indispensables':pending,
        'fits_reales':validation['fits_total'] if validation else sum(a.get('pipeline_fits_started',0) for a in (state or {}).get('attempts',[])),
        'presupuesto':state,'meta':meta if complete else None,'fase4_autorizada':False,'congelacion_sha256':digest(HERE/'CONGELACION_FASE3.json') if (HERE/'CONGELACION_FASE3.json').exists() else None})
    fresh('LECTURAS_FASE3.json',{'AGENTS':'completo','continuidad_propia':'fase2 completa alinicio; anterior preservada',
        'plan':'únicamente líneas1–15 y85–105','protocolo_fase1':'§§1–7','especificacion_documental':'completa','protocolo_implementacion_etapa1':'completo',
        'vigentes':'diagnóstico1–106; temporal vigente completo; v5 1–98; diseño propio completo',
        'historico':'v5 en commitreal; temporal solo texto/huella de partidaetapa2','PDF_paginas':0,'web':0,
        'pendiente':'Fase4 auditoría interpretativa/confirmación independiente/disponibilidad; no autorizadas'})
    excluded=['MANIFIESTO_FASE3.json','VERIFICACION_MANIFIESTO_FASE3.json']
    mapping={p.relative_to(HERE).as_posix():digest(p) for p in HERE.rglob('*') if p.is_file() and p.name not in excluded}
    fresh('MANIFIESTO_FASE3.json',{'completa':complete,'entregables_sha256':mapping,'exclusiones_autorreferencia':excluded,
        'continuidad_actual_sha256':digest(HERE.parent/'CONTINUIDAD_EXPERIMENTAL.md'),
        'continuidad_fase2_preservada_sha256':digest(HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md')})
    result=verify(); fresh('VERIFICACION_MANIFIESTO_FASE3.json',result)

if __name__=='__main__':
    if sys.argv[1:]==['--verificar']: verify()
    elif not sys.argv[1:]: main()
    else: raise ValueError('Uso: cerrar_fase3.py [--verificar]')
