"""Informe técnico y hallazgos desde resultados verificados, sin ajustes."""
from comun import *
from resultados import OUT,TABLES,readcsv

def technical():
    a=load(OUT/'AUDITORIA.json');p=load(OUT/'PRIMARIO.json');e=load(OUT/'CONTROL_TEXTO.json');l=load(HERE/'fase2/piloto/ledger.json');pf=preflight()
    check(a['aprobado'] and e['aprobado'] and l['status']=='cerrado_completo','reporte solo verificables')
    hist=readcsv(TABLES/'antecedentes_recalculados.csv');contr=readcsv(TABLES/'contrastes_predefinidos_completos.csv')
    report=f'''# Informe técnico — cierre del objetivo3

## Autoridad y alcance

Respuesta humana «sí lo autorizo» habilitó corrección y nueva ejecución del mismo contrato con7200s nuevos, preservando el intento anterior incompleto. No reapertura/ampliación/herencia de saldo ni nuevo diseño. Solo fases1→2→3. No raw/red/nuevasfuentes/instalaciones/commit/push/modelofinal/notebookpersonal/objetivo4/proyección. Escribir solo carpeta propia. Texto académico final sin etiquetasdeversión, estilo impersonal tesis vigente.

## Contrato y conservación

39 IDs/orden/parametrización íntegros ESPECIFICACION/CANDIDATOS. Ventanas originales; primario técnico global_v6, referencia persistencia/v3 y meta5%. Bandas internas inclusivas0.1MAE y0.1RMSE dentropool→entradas0/1/2→orden. Constantes0entradas/persistencia primero;2021externa fija sin fit/score/selection;2019solo historial,2018nivel,2020excluido y salto2021previo2019sinanualizar.165pares/33territorios/igualpeso/mediarecibida/geografíacolegio/población original. Todos ajustes propios por ventana, sin modelos históricos.

Entorno Python3.12.14/sklearn1.9.1,54lockexactos/pipcheck,semilla20261010/PYTHONDONTWRITEBYTECODE1. Fuentes SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc. GitHEAD/asunto/rama/ascendencia y originales revalidados: {json.dumps(pf['conservacion'],ensure_ascii=False)}. Mappingshistóricos {pf['historia']['mappings']}; v5 etapa1 commitreal109797407d75d2097e5b71f8bcef3fc266bc61d2; temporal solo texto/huella partida. Cierres históricos sin modificación. Cierre documental inicial cotejado por continuidadfase0 preservada, sin reescribir verificador documental original que esperaba continuidad antigua. Registro fase1/DOCUMENTAL_MAPPING.json.

Intento previo preservado por PARTIDA_PROPIA.json/manifest1935huellas y continuidad anterior propia. Su fallo de compartir fits internos queda archivado como antecedente resuelto en esta ejecución mediante192internos independientes. No reinterpretar como ejecución previa completa ni ocultar su ledger cerrado incompleto. Nuevos tests de flujo máximos328fits/104constantes y negativo reuso.32componentes sintéticos terminados y un intento fallido numérico de prueba separados del piloto; fixtures procesos ficticios separados.

## Ejecución y auditoría

Ledger nuevo7200s cerrado definitivamente en {l['elapsed_seconds']}s;{l['fits_started']} componentes iniciados/{l['fits_completed']}terminados,{l['statistical_estimates']} constantes,{l['failures']}fallos/{l['retries']}retries.192internos+128externos más repeticiones incluidas;60constantesinternas+40externas más recomputación. Serial: eventosstart/endmonotónicos, wait_completed/returncode/terminación durables; no procesos pendientes. Tiempo incluye arranque/comunicación/escritura/constantes/repeticiones/pausas. Saldo no reutilizable.

{a['jobs']} trabajos reconstruidos por auditor independiente sin motor/runner/selector operativo ni fit/carga/deserialización. Matrices X/y/llaves/fechas/d/c/r/unidades/defaults/semilla/versiones/coef/intercept/scales/advertencias/origen/hash cotejados. Scaler arithmetic atol1e-12/rtol0; CSV y matrices/predicciones serializadas exactos,intfloat0equivalente,1e-11rechazado; cinco checks globales previoexacto/constante recomputada/fitrepetidoatol1e-10rtol0. Repeticiones contadas en ledger, no nuevas duranteauditoría.

12870internasoriginales/5148únicas,156registrosselección,6600externas,12870linajes,cobertura39políticas+global. Todas internas repetidas vienen de ajustes propios identificados, contexto/predicción exacta antesdeduplicación,mismoID/año y representante menor externo. Decisiones fechadas antesprimerexternoincluidopersistencia. Primario copia delmismoID/ventana consource_id, no mejorpolíticaexterna.

## Resultado verificado

PRIMARIO.json (celda4,resultados.analyse): {json.dumps(p,ensure_ascii=False)}. Meta calculada sin redondeo con denominador positivo; no rescate por política externa.39candidatos completos,40procedimientos con primario; contrastes {len(contr)} descriptivos predefinidos por dimensiones del contrato. Tablas poraño/territorio,erroresfirmados/absolutos/sesgo/dirección/coeficientes y equivalencias. Copias y165pares dependientes; no p-valores confirmatorios.

Antecedentes recalculados notebookcelda3:{hist[['label','MAE','improvement_vs_reference']].to_dict('records')}. V3/v5global/recencia165 mismasllaves/observados/predicciones; no evidencia independiente. Memoriaglobal1.7979745286559843% ymemoria12.392390281511053% son antecedentes, no resultado primario actual. Guainía diagnóstico filas57/90,238vs404/diferencia21.012105832431985 histórica; no cambiómedia.

## Notebook y texto

Notebook01cuatroceldascontroles inventados; notebook02fuentePython/generador,nbformatvalidado,releído,execsecuencialreal constdoutcapturado. Celdas1preflight,2auditoría,3antecedentes,4análisis,5figuras,6tablascomplementarias,7redacciónúltima. Compartidas sin lógica duplicada por modelo. Texto interpolado desde salidas; {e['claims']} registros de evidencia con celda/función/archivo/tabla/llave/n/unidad/SHA y valoresexactoscontrolados. Figuras generadas notebookcell5 y revisadas visualmente. Sin outputsmanuales,dato personal ni fits nuevos. Regeneraciones para añadir redacción al final y normalizar decimales/mostrar figuras en notebook: ejecuciones previas y fuentes preservadas en fase3/antecedentes; todas sin fits. Reejecución auditoría/cálculos no usa saldo piloto.

## Alcance académico y pendientes

PDF tesis vigente ACA2,páginasfísicas25,56–60,113–114 leídas; demás no atribuir lectura. Objetivo3 y diseño páginas58–59 proponen IPM/especificacionescomposición/reserva2023–24,robustezMatemáticas/excluir2021 y validaciónterritorial. El contrato ejecutado es diferente: resultados históricos de indicadorespobreza más evaluación dinámica; extensión2025exploratoria. No afirmar ejecución íntegra de eseplan o validaciónH3. Texto lo explicita sin modificartesisoriginal. No se creó modelo final ni escenarios.

Fuente local no autenticada; huellas conservación no oficialidad/publicación. Registro local consulta2026-10-07 y publicaciónIPM2024registrada22/04/2025 no demuestra disponibilidad anticipada panel2025. Últimoaño local2025/siguiente2026soloCONDICIONAL sinpredicción. Hogaresvsalumnos/colegiovsresidencia/ecología/pocos años/dependencia/todos2021–2025vistos permanecen. Aceptación técnica no soluciona estos límites.

Entregables completos, pendientes científicos y no avance automático. Sololectura verificar_entrega.py coteja manifiestos/notebooks/freeze/cierres/continuidades/evidencias/conservación sin fits/modelos/escrituras.
'''
    save(HERE/'INFORME_TECNICO.md',report)
    findings=[
    dict(id='ajustes_por_ventana',state='resuelto; antecedente propio archivado',impact='previo compartía ajustes y no cumplía192internos',alternative='Pipeline y proceso propios por componente/candidato/ventana antes deduplicación',resolution='freeze,tests negativos y auditoría independiente;192internos/128externos',evidence='fase1/PRUEBAS_EJECUCION.json;fase3/AUDITORIA.json;fase2/piloto/ledger.json'),
    dict(id='cierre_documental',state='resuelto por mapping histórico existente',impact='verificadorfase0 espera continuidad previa y falló al usar continuidad avanzada',alternative='cotejar SHA contra archivo fase0 ya preservado, sin alterarverificador/manifiesto',resolution='fase1/DOCUMENTAL_MAPPING.json; originales intactos',evidence='fase1/DOCUMENTAL_MAPPING.json;antecedentes/CONTINUIDAD_CIERRE_ANTERIOR.md'),
    dict(id='primario',state='resultado completo',impact='meta5%'+('alcanzada' if p['target_met'] else 'no alcanzada'),alternative='reportar primario predefinido y todos contrastes sin rescate por ganador externo',resolution='PRIMARIO/tablas/notebook/texto',evidence='fase3/PRIMARIO.json;fase3/tablas/metricas_40_procedimientos.csv'),
    dict(id='objetivo_IPM',state='límite académico activo',impact='predicción dinámica no demuestra utilidad incremental de pobreza ni ejecutaplanoriginal completo',alternative='integrar recálculos IPM válidos y comparación con persistencia; explicitaralcance',resolution='texto sin versiones; no afirmación H3 validada',evidence='Tesis Vigente/ACA2.pdf físicas25,58–59;fase3/tablas/procedimientos_indicadores_pobreza_recalculados.csv'),
    dict(id='origen_fechas',state='pendiente científico activo',impact='aceptación técnica no autentica ni prueba anticipación',alternative='conservar huellas/localfecha y decir límite; nofuentesnuevas',resolution='DISPONIBILIDAD y texto',evidence='fase3/DISPONIBILIDAD.json;auditoria/fuentes_verificadas.md líneas3/7'),
    dict(id='Guainia',state='antecedente numérico preservado, sin cambio actual',impact='población completa vs globaldisponible difieren',alternative='recalcular guardados notebook y mantener población/media fijadas',resolution='guainia_historico.csv; advertencia sin reabrirraw',evidence='fase3/tablas/guainia_historico.csv;diagnóstico histórico líneas57/90'),
    dict(id='dependencia',state='pendiente científico activo',impact='165pares y copias no replicacionesindependientes; pocos años',alternative='tablas descriptivas completas sinp-valores',resolution='erroraño/territorio/sesgo/dirección; sin causalidad',evidence='fase3/tablas/errores_completos_6600.csv;TEXTO_OBJETIVO3_TESIS.md')]
    save(OUT/'REGISTRO_HALLAZGOS.json',findings);print({'informe_guardado':True,'hallazgos':len(findings),'nuevos_fits':0})
