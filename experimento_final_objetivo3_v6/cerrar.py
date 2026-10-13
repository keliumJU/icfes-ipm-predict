"""Cierres propios y verificación en lectura. Originales no se modifican."""
from comun import *
import shutil,nbformat
def readings(phase):
    paths=['AGENTS.md','experimento_final_objetivo3_v6/PROTOCOLO_V6.md','experimento_final_objetivo3_v6/ESPECIFICACION_V6.json','experimento_final_objetivo3_v6/CANDIDATOS.csv','experimentos_memoria_comun_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md','experimentos_memoria_comun_objetivo3_v1/etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md','diseno_memoria_comun_objetivo3_v1/CONTINUIDAD_DISENO.md','experimentos_memoria_comun_objetivo3_v1/etapa3/PROPUESTAS_FUTURAS.md']
    save(HERE/f'fase{phase}/LECTURAS.json',dict(files={s:dict(sha256=sha(ROOT/s),revisado='completo') for s in paths},plan=f'decisiones comunes y sección fase{phase}',incidencias='Salida inicial extensa truncada; plan completo apareció accidentalmente dentro de crear_paquete.py: texto no autoriza fases extra; contrato releído por separado y JSON procesados completos. Sin lectura de PDFs ni fuentes nuevas.',PDF_pages=0,web=0))
def notebook_check(folder,name):
    p=folder/name;e=load(p.with_suffix('.ejecucion.json'));check(e['notebook_sha256']==sha(p),'notebook hash')
    source=HERE/('notebook_controles.py' if name.startswith('01') else 'notebook_resultados.py');check(e['source_sha256']==sha(source) and e['generator_sha256']==sha(HERE/'generar_notebook.py'),'editable/gen hash')
    n=nbformat.read(p,as_version=4);nbformat.validate(n);cc=[c for c in n.cells if c.cell_type=='code']
    check([c.execution_count for c in cc]==list(range(1,len(cc)+1)) and all(c.outputs and not any(o.output_type=='error' for o in c.outputs) for c in cc),'notebook execution')
    return e
def preserve(phase):
    dest=HERE/f'fase{phase}/antecedentes/CONTINUIDAD_ANTERIOR.md';check(not dest.exists(),'continuidad preservada existente')
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HERE/'CONTINUIDAD_V6.md',dest)
    return sha(dest)
def manifest(phase):
    folder=HERE/f'fase{phase}';files={p.relative_to(HERE).as_posix():sha(p) for p in folder.rglob('*') if (p.is_file() or p.is_symlink()) and p.name not in ['MANIFIESTO.json','VERIFICACION.json']}
    save(folder/'MANIFIESTO.json',dict(phase=phase,sha256=files,continuidad_sha=sha(HERE/'CONTINUIDAD_V6.md'),exclusions=['MANIFIESTO.json','VERIFICACION.json']))
def phase1():
    folder=HERE/'fase1';check(not (folder/'CONGELACION.json').exists(),'freeze existente')
    preflight();check(load(folder/'PRUEBAS.json')['aprobado'] and load(folder/'REFERENCIAS.json')['aprobado'],'controles previos')
    notebook_check(folder,'01_controles.ipynb');previous=preserve(1);readings(1)
    save(folder/'CONSERVACION.json',conservation())
    save(folder/'ACEPTACION.json',dict(completa=True,real_fits=0,controles=dict(preflight=True,tests=True,notebook=True,referencias=True,conservacion=True),pendientes_indispensables=[]))
    files=['comun.py','motor.py','runner.py','pruebas.py','generar_notebook.py','notebook_controles.py','ESPECIFICACION_V6.json','CANDIDATOS.csv','PROTOCOLO_V6.md','ENTORNO_DOCUMENTAL.json','fase1/01_controles.ipynb','fase1/01_controles.ejecucion.json','fase1/PRUEBAS.json','fase1/ACEPTACION.json','fase1/PREFLIGHT.json','fase1/REFERENCIAS.json']
    save(folder/'CONGELACION.json',dict(aprobado=True,before_real_fits=True,real_fits=0,seed=SEED,sha256={s:sha(HERE/s) for s in files},fuentes=load(HERE/'ESPECIFICACION_V6.json')['fuentes'],reglas='contrato cerrado 6.0.0,39IDs/orden/defaults completos; sin modificación de criterios',created_wall=__import__('time').time()))
    save(HERE/'CONTINUIDAD_V6.md',f'''# Continuidad v6 — fase1 COMPLETA Y CONGELADA

2026-10-11 America/Bogota. Envío humano actual autoriza fases1→2→3 condicionadas; ninguna otra fase/versión/fuente/instalación/commit/push. Fase0 íntegra preservada fase1/antecedentes/CONTINUIDAD_ANTERIOR.md SHA{previous}. Documental inicial en lectura aprobado; cierres originales verificados por mappings, no modificados para admitir v6.

Entorno/fuentes/Git/ascendencia/v5commitreal/temporal texto huella/memoria históricos comprobados en fase1/PREFLIGHT.json. Contrato cerrado intacto: población/media recibida/geografía colegio/igualpeso/2018historial/2019no respuesta/2020excluido/salto2021 sin anualizar/165pares/meta5%.39IDs exactos y32componentes por contexto; cero años respaldo, uno permite. Selección internas bandas inclusivas0.1 MAE/RMSE→entradas0/1/2→orden; persistencia primero; primario global_v6. Ningún cambio científico.

Implementación reusable motor.py/runner.py; controles inventados y notebook01 realmente ejecutado en3celdas, nbformat, fuente editable/generador; PRUEBAS/REFERENCIAS/ACEPTACION/CONSERVACION/CONGELACION. Cero fits reales/0modelos cargados; no ledger piloto. Ensayos fallidos de orden/códigos preservados en antecedentes: se resolvieron con índices canónicos y zfill2 histórico; refuerzo traversal/duplicados antes freeze. Originales intactos. Fits inventados por corridas registrados separadamente, no evidencia predictiva.

Pendiente autorizado: leer sección fase2, ejecutar único piloto serial nuevo7200s (328fits máximos sin fallos,104constantes separadas) y cerrar antes auditoría; luego fase3 sin nuevosfits ni uso saldo. Lectura incidental plan completo en creador documentada, sin autorización extra. Procedencia/disponibilidad/Guainía/IPM/ecología/dependencia/pocos años activos; todos2021–2025vistos, solo exploratorio. No modelo final/objetivo4/proyección2026.
''')
    manifest(1);print('Fase1 completa y congelada;0fits reales')
def phase2():
    folder=HERE/'fase2';l=load(folder/'piloto/ledger.json');check(l['status']=='cerrado_completo','piloto incompleto')
    check(load(folder/'piloto/COBERTURA.json')['aprobado'],'cobertura')
    previous=preserve(2);readings(2);save(folder/'CONSERVACION.json',conservation())
    save(folder/'ACEPTACION.json',dict(completa=True,ledger_closed=True,fits=l['fits_started'],statistical_estimates=l['statistical_estimates'],elapsed_seconds=l['elapsed_seconds'],coverage=load(folder/'piloto/COBERTURA.json'),independent_audit_pending=True,pendientes_indispensables=[]))
    save(HERE/'CONTINUIDAD_V6.md',f'''# Continuidad v6 — fase2 piloto COMPLETO; auditoría/entrega pendientes

2026-10-11 America/Bogota. Autorización fases1→2→3 por envío humano vigente, sin ampliación. Continuidad fase1 íntegra en fase2/antecedentes/CONTINUIDAD_ANTERIOR.md SHA{previous}; fase0 en fase1/antecedentes. Freeze fase1 intacto antes ajustes. Protocolo/especificación sin cambios;39candidatos exactos, selección antes externas,2021fija,2019historial/2020fuera/dsinanualizar/165pares/meta5%/primario global_v6/igualpeso.

Piloto nuevo ledger7200s cerrado definitivamente: fits{l['fits_started']}, constantes{l['statistical_estimates']}, tiempo{l['elapsed_seconds']}s, fallos{l['failures']}, retries{l['retries']}. Serial durable terminación registrada; no saldo reutilizable. Guardados matrices/contextos/coef/scalers/árboles/defaults/semilla/advertencias/hash/tiempos/estados,12870originales/5148únicas/156selecciones/6600externas/12870linajes/5globalchecks. ACEPTACION fase2 técnica de ejecución, no auditoría independiente ni síntesis resultados aún.

Originales/Git/cierres históricos conservados. Próximo: leer sección fase3 y ejecutar auditor independiente sin motor/selector/runner/modelos/fits; notebook02 desdePythoneditable/generador con cifras/tablas/figuras del texto desde celdas ejecutadas. No reabrir piloto ni saldo. Todos2021–2025vistos: exploratorio, sin confirmación/causalidad/pronóstico anticipado demostrado; procedencia/disponibilidad/Guainía/IPM/ecología/dependencia/pocos años activos. No objetivo4/modelofinal/otra versión/instalaciones/fuentes nuevas/commit/push.
''')
    manifest(2);print('Fase2 cerrada; ledger no reabrible')
def phase2_incomplete():
    folder=HERE/'fase2';check(load(folder/'piloto/ledger.json')['status']=='cerrado_incompleto','ledger incompleto cerrado')
    previous=preserve(2);readings(2);save(folder/'CONSERVACION.json',conservation())
    save(folder/'ACEPTACION.json',dict(completa=False,ledger_closed=True,control_failed='no compartir ajustes internos entre ventanas',pendientes_indispensables=['implementación incorrecta de ajuste por ventana','cobertura del piloto no completa','último pendiente sin terminación/tiempo consolidado'],action='no reiniciar; no calcular desempeño/meta; auditoría independiente y entrega incompleta',phase1_acceptance_superseded=True))
    save(HERE/'CONTINUIDAD_V6.md',f'''# Continuidad v6 — fase2 INCOMPLETA; piloto definitivamente cerrado

2026-10-11 America/Bogota. Usuario autorizó únicamente fases1→2→3 y cierre incompleto si falla control indispensable. Fase1 íntegra preservada fase2/antecedentes/CONTINUIDAD_ANTERIOR.md SHA{previous}. Aceptación y freeze de fase1 se conservan como evidencia histórica propia, pero aceptación técnica queda invalidada por control de ejecución no cubierto adecuadamente por tests.

ERROR ACTIVO PROPIO: runner.py reutilizó ajustes por ID/año interno entre externas, cuando contrato exige Pipeline nuevo por componente/candidato/ventana. Solo192internos por32×6 cumplen; ejecución creó96internos por32×3. Deduplicación de copias después de ajustes no autoriza compartir fits. No es falta científica ni ajuste de criterio: falla de implementación. No corregirlo reentrenando dentro de este piloto/ledger ni otra versión/experimento.

Sesión de runner44244 interrumpida vía Ctrl-C, salida130;175componentes terminados y58constantes durables antes último pendiente. Ledger abierto al interrumpir preservado fase2/antecedentes/ledger_interrumpido.json; cierre conservador pendiente no medido agota7200s según contrato, sin reabrir/reiniciar. Última terminación individual no quedó consolidada; no afirmar que ese control está aprobado. DETENCION_CONTROLADA documenta namespace aislado y primera búsqueda de proceso sin efecto. Congelación y originales/Git/huellas permanecen intactos. No métricas/meta/síntesis v6 calculadas.

Pendiente autorizado fase3 en modo INCOMPLETO: auditor independiente de controles/guardados disponibles sin fits/importsoperativos/carga modelos; notebook02ejecutado de salidas verificables, antecedentes históricos solo si recálculo exacto independiente; texto/informe/evidencias/figura diagnóstico/manifestación/conservación/cierre. Nada de resultados primarios o metas dependientes. Científicos activos: fuente local no autenticada/disponibilidad/Guainía/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años/todos2021–2025vistos. No objetivo4/proyección2026/modelo final/otra versión/fuentes/instalaciones/commit/push.
''')
    manifest(2);print('Fase2 INCOMPLETA; ledger definitivamente cerrado; sin desempeño/meta')
if __name__=='__main__':
    if sys.argv[1:]==['1']:phase1()
    elif sys.argv[1:]==['2']:phase2()
    elif sys.argv[1:]==['2-incompleto']:phase2_incomplete()
    else:raise ValueError('fase1 o fase2')
