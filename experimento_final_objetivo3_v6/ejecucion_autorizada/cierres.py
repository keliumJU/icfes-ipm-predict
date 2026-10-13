"""Aceptaciones propias; conserva cada continuidad anterior y cierres históricos."""
from comun import *
import time,shutil,nbformat

def notebook_verify(folder,name,source):
    p=folder/name;e=load(p.with_suffix('.ejecucion.json'));n=nbformat.read(p,as_version=4);nbformat.validate(n);cells=[c for c in n.cells if c.cell_type=='code']
    check(e['notebook_sha256']==sha(p) and e['source_sha256']==sha(HERE/source) and e['generator_sha256']==sha(HERE/'generar_notebook.py'),'notebook binding')
    check([c.execution_count for c in cells]==list(range(1,len(cells)+1)) and all(c.outputs and not any(o.output_type=='error' for o in c.outputs) for c in cells),'real executed cells')
    return e

def documental_mapping():
    m=load(OWNROOT/'MANIFIESTO_DOCUMENTAL.json')
    for s,h in m['entregables_sha256'].items():
        q=OWNROOT/'fase1/antecedentes/CONTINUIDAD_ANTERIOR.md' if s=='CONTINUIDAD_V6.md' else OWNROOT/s
        check(sha(q)==h,'documental preserved '+s)
    return dict(aprobado=True,continuidad_mapping='fase1/antecedentes/CONTINUIDAD_ANTERIOR.md',reason='verificador documental original no valida continuidad que avanzó; no modificar original',files=len(m['entregables_sha256']))

def preserve(phase):
    dest=HERE/f'fase{phase}/antecedentes/CONTINUIDAD_ANTERIOR.md';check(not dest.exists(),'preservación existente')
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HERE/'CONTINUIDAD_V6.md',dest);return sha(dest)

def manifest(phase):
    folder=HERE/f'fase{phase}';mapping={p.relative_to(HERE).as_posix():sha(p) for p in folder.rglob('*') if p.is_file() and p.name!='MANIFIESTO.json'}
    save(folder/'MANIFIESTO.json',dict(phase=phase,sha256=mapping,continuidad_sha=sha(HERE/'CONTINUIDAD_V6.md')))

def phase1():
    check(not (HERE/'fase1/CONGELACION.json').exists(),'freeze existente')
    save(HERE/'fase1/PREFLIGHT.json',preflight());save(HERE/'fase1/DOCUMENTAL_MAPPING.json',documental_mapping())
    from auditor import auditor_tests
    from referencias import historical_frames
    historical_frames();save(HERE/'fase1/REFERENCIAS.json',dict(aprobado=True,n=165,same_keys_observed_prediction=True,independent_evidence=False))
    save(HERE/'fase1/PRUEBAS_AUDITOR.json',auditor_tests())
    check(load(HERE/'fase1/PRUEBAS.json')['aprobado'] and load(HERE/'fase1/PRUEBAS_EJECUCION.json')['aprobado'],'synthetic tests')
    notebook_verify(HERE/'fase1','01_controles.ipynb','notebook_controles.py');previous=preserve(1)
    save(HERE/'fase1/LECTURAS.json',dict(protocol='completo',specification='completa;39 IDs/params/orden',continuity_previous=previous,AGENTS='completo',plan='comunes y fase1; salida accidental de plan completo en herramienta de lectura registrada, sin fases extra',PDF='tesis vigente páginas físicas25,56–57,113–114; pendiente58–60',original_attempt='preservado íntegro por mapping PARTIDA_PROPIA',authorization='sí lo autorizo: nueva ejecución del mismo diseño,7200s nuevos; texto último sin etiquetas de versión'))
    save(HERE/'fase1/ACEPTACION.json',dict(completa=True,real_fits=0,tests=True,notebook=True,independent_window_jobs=True,termination_wait=True,originals_preserved=True))
    files=['comun.py','motor.py','runner.py','pruebas.py','pruebas_ejecucion.py','notebook_controles.py','generar_notebook.py','ESPECIFICACION_V6.json','CANDIDATOS.csv','ENTORNO_DOCUMENTAL.json','PROTOCOLO_V6.md','PROTOCOLO_DE_EJECUCION.md','fase1/PREFLIGHT.json','fase1/PRUEBAS.json','fase1/PRUEBAS_EJECUCION.json','fase1/ACEPTACION.json','fase1/01_controles.ipynb','fase1/01_controles.ejecucion.json']
    save(HERE/'fase1/CONGELACION.json',dict(aprobado=True,before_real_fits=True,real_fits=0,seed=SEED,created_wall=time.time(),sha256={s:sha(HERE/s) for s in files},fuentes=load(HERE/'ESPECIFICACION_V6.json')['fuentes'],scientific_changes=[]))
    save(HERE/'CONTINUIDAD_V6.md',f'# Continuidad propia — fase1 completa y congelada\n\nAutorización humana para ejecutar el mismo diseño con ledger nuevo7200s. Intento anterior cerrado conservado íntegramente, sin reapertura ni saldo heredado. Continuidad de inicio preservada SHA{previous}. Controles inventados y notebook realmente ejecutados; cero fits reales.192 internos por ventana independientes,128 externos,hasta8 repetidos,104 constantes máximo.39 candidatos exactos, selección predefinida y primario global_v6, semilla20261010, entorno exacto y fuentes contractuales conservadas.\n\nPendiente autorizado: leer fase2 e iniciar piloto único nuevo, cerrar antes auditoría. Texto académico al final, estilo tesis vigente, sin versiones en cuerpo. Sin objetivo4/modelo final/proyecciones/fuentes/instalaciones/commit/push.\n')
    manifest(1);print('Fase1 aceptada y congelada; cero ajustes reales')

def phase2():
    l=load(HERE/'fase2/piloto/ledger.json');check(l['status']=='cerrado_completo' and l['pending'] is None,'piloto cerrado completo')
    previous=preserve(2);save(HERE/'fase2/CONSERVACION.json',conservation())
    save(HERE/'fase2/ACEPTACION.json',dict(completa=True,ledger_closed=True,reopen_allowed=False,fits=l['fits_started'],constants=l['statistical_estimates'],seconds=l['elapsed_seconds'],failures=l['failures'],retries=l['retries'],coverage=load(HERE/'fase2/piloto/COBERTURA.json'),independent_audit_pending=True))
    save(HERE/'CONTINUIDAD_V6.md',f'# Continuidad propia — fase2 piloto cerrado\n\nContinuidad fase1 preservada SHA{previous}. Freeze intacto, fuentes/originales/cierres históricos intactos. Piloto completo ledger nuevo7200s cerrado; fits{l["fits_started"]},constantes{l["statistical_estimates"]},segundos{l["elapsed_seconds"]}. Selecciones antes externas,12870 originales/5148 copias únicas/6600 externas/156 registros/linaje/cinco checks. Sin uso futuro de saldo.\n\nPendiente autorizado fase3: auditor independiente sin fits/modelos/imports operativos; notebook resultados/tablas/figuras desde celdas; texto académico último, estilo tesis vigente,sin versiones. Evaluación exploratoria,todos2021–2025 vistos,165 pares dependientes,fuente local no autenticada,IPM hogares vs alumnos/colegio residencia/ecología/pocos años/disponibilidad pendiente. Sin objetivo4 ni proyección.\n')
    manifest(2);print('Fase2 cerrada; auditoría pendiente')

if __name__=='__main__':
    {'1':phase1,'2':phase2}[sys.argv[1]]()

def phase3():
    previous=preserve(3);preflight();a=load(HERE/'fase3/AUDITORIA.json');ct=load(HERE/'fase3/CONTROL_TEXTO.json');check(a['aprobado'] and ct['aprobado'],'audit/text')
    notebook_verify(HERE/'fase3','02_resultados_objetivo3.ipynb','notebook_resultados.py');check(load(HERE/'fase3/REVISION_VISUAL.json')['aprobado'],'visual')
    save(HERE/'fase3/CONSERVACION.json',conservation());save(HERE/'fase3/LECTURAS.json',dict(plan='comunes y fase3 leídas al entrar',protocol='completo',historical='mappings originales; referencias persistencia/indicadores pobreza recalculadas desde CSV completos',PDF={'file':'Tesis Vigente/ACA2.pdf','physical_pages':[25,56,57,58,59,60,113,114],'other_pages':'no atribuir lectura actual'},web=0,raw=0))
    pending=['Autenticidad oficial y fechas de publicación/disponibilidad histórica del panel no demostradas','Todos los años de evaluación ya vistos: sin confirmación independiente','IPM hogares frente a estudiantes; geografía colegio frente a residencia; agregación ecológica','Pocos años y dependencia entre territorios/años; sin inferencia confirmatoria','El diseño autorizado no ejecuta íntegramente las especificaciones y reservas propuestas en tesis páginas58–59; no afirmar validación completaH3','Siguiente año condicional a fuentes comparables y disponibilidad; sin proyección ni objetivo4']
    save(HERE/'fase3/PENDIENTES.json',dict(technical_indispensable=[],scientific=pending,other_phases_authorized=False))
    save(HERE/'fase3/ACEPTACION.json',dict(completa=True,fits_auditor=0,models_loaded=0,pilot_closed=True,notebook_executed=True,text_control=True,visual_review=True,scientific_pending=pending,authenticity_confirmed=False,independent_confirmation=False,objective4=False))
    save(HERE/'CONTINUIDAD_V6.md',f'# Continuidad propia — fases1→2→3 completas; cierre\n\nAutorización humana explícita para repetir el mismo diseño con presupuesto nuevo7200s; no nueva versión científica ni criterios modificados. Intento anterior conservado íntegro según PARTIDA_PROPIA y antecedente continuidad, no reabierto ni saldo heredado. Fase2 preservada SHA{previous}; fase1 en fase2antecedentes; inicio en fase1antecedentes.\n\n39 candidatos exactos,192 ajustes internos independientes por ventana/128 externos, constantes históricas contadas, selección antes externas,2021fijo,2019solo historial,2020excluido,2021previo2019sinanualizar. Primario global_v6,165pares/igualpeso/meta5%,sin rescate por mejor política externa. Entorno exacto/54lock/semilla20261010/fuentes/Git/cierres históricos intactos. Piloto cerrado definitivamente, auditor independiente0fits/importsoperativos/modelos. Notebook02 fuente editable/generador, celdas reales y cifras/tablas/figuras desde funciones compartidas. Texto redactado después resultados/figuras, estilo tesis vigente,sin etiquetas de versión ni historia de iteraciones en cuerpo; evidencias asociadas.\n\nEntrega TEXTO_OBJETIVO3_TESIS.md,notebook02,tablas completas,figuras,INFORME_TECNICO,REGISTRO_HALLAZGOS,lecturas/aceptación/conservación/manifiesto/verificador lectura. Resultado primario en fase3/PRIMARIO.json; no confundir políticas descriptivas o antecedentes con primario. Pendientes científicos en fase3/PENDIENTES: autenticidad/disponibilidad/ecología/IPM/dependencia/pocos años/todos años vistos; contraste dinámico no prueba aporte incrementalIPM ni ejecución íntegra plan tesis páginas58–59. No cambiar tesis original,no objetivo4/proyección/modelofinal/nuevosdatos/red/instalaciones/commit/push/otra versión/otro experimento. No avance automático.\n')
    manifest(3)
    exclusions=['MANIFIESTO_FINAL.json','VERIFICACION_FINAL.json']
    files={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if (p.is_file() or p.is_symlink()) and p.relative_to(HERE).as_posix() not in exclusions}
    # Continuidad principal propia: original íntegra ya preservada antes de cambiar el puntero.
    previous_top=OWNROOT/'CONTINUIDAD_V6.md';check(sha(previous_top)==sha(HERE/'antecedentes/CONTINUIDAD_CIERRE_ANTERIOR.md'),'continuidad principal original preservada')
    pointer='# Continuidad principal — entrega vigente cerrada\n\nLa nueva ejecución del mismo diseño, autorizada expresamente por el usuario, completó fases1→2→3. Entrega vigente: ejecucion_autorizada/TEXTO_OBJETIVO3_TESIS.md y ejecucion_autorizada/fase3/02_resultados_objetivo3.ipynb. Continuidad detallada: ejecucion_autorizada/CONTINUIDAD_V6.md. Verificación solo lectura: ejecucion_autorizada/verificar_entrega.py.\n\nIntento previo cerrado incompleto se conserva íntegramente. Esta continuidad anterior está preservada exactamente en ejecucion_autorizada/antecedentes/CONTINUIDAD_CIERRE_ANTERIOR.md, con sus huellas originales en PARTIDA_PROPIA.json. Manifiestos, código, ledger y entregables previos no se modificaron. No confundir texto de cierre incompleto de carpeta superior con entrega actual.\n\nPiloto nuevo cerrado sin saldo reutilizable; auditoría independiente y notebook sin nuevosfits. Resultado primario y meta en ejecucion_autorizada/fase3/PRIMARIO.json; mejora insuficiente para5%. Texto final en lenguaje tesis vigente,sin versiones en cuerpo. Pendientes científicos documentados, sin afirmación H3 confirmada ni objetivo4/modelofinal/proyección/fuentesextra/instalaciones/commit/push/nueva versión/nuevo experimento automático.\n'
    tmp=previous_top.with_name('CONTINUIDAD_V6.md.tmp')
    with tmp.open('w') as handle:handle.write(pointer);handle.flush();os.fsync(handle.fileno())
    os.replace(tmp,previous_top)
    save(HERE/'MANIFIESTO_FINAL.json',dict(complete=True,sha256=files,exclusions=exclusions,original_attempt_manifest=load(HERE/'PARTIDA_PROPIA.json')['manifest_sha256'],continuidad_principal_sha=sha(previous_top)))
    print('Fase3 completa; sin avance automático')
