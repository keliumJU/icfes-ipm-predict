"""Entrega final de la rama incompleta autorizada; no ajustes ni nuevo experimento."""
from comun import *
from cerrar import preserve,readings,notebook_check,manifest
def main():
    check(not (HERE/'MANIFIESTO_FINAL.json').exists(),'cierre existente; solo lectura')
    preflight();notebook_check(HERE/'fase3','02_resultados_objetivo3.ipynb');previous=preserve(3);readings(3)
    a=load(HERE/'fase3/AUDITORIA_INCOMPLETA.json');check(not a['complete'] and not a['performance_synthesis'],'incompleto')
    save(HERE/'fase3/CONSERVACION.json',conservation())
    save(HERE/'fase3/REVISION_VISUAL.json',dict(aprobado=True,method='view_image: etiquetas/ejes/unidad/counts/alcance incompleto legibles sin recortes; figura técnica, no desempeño',file='fase3/figuras/01_control_ajustes_internos.png',sha256=sha(HERE/'fase3/figuras/01_control_ajustes_internos.png')))
    pending=['ajustes internos independientes por ventana no ejecutados como contrato','cobertura completa/selección/linaje/CSV final del piloto no verificables','medición y registro individual de terminación del último pendiente no consolidado']
    save(HERE/'fase3/PENDIENTES.json',dict(indispensables=pending,scientific=['autenticidad de fuente local','fecha histórica de disponibilidad del panel','confirmación independiente temporal','interpretación ecológica/IPM hogares vs estudiantes/colegio vs residencia','dependencia entre territorios-años y pocos años'],closure='no nueva versión/experimento/reapertura/objetivo4/modelofinal/fuente/instalación/commit/push; ningún avance automático',resolution='fallo de ejecución no autoriza sintetizar métricas/meta v6; evidencia disponible y antecedentes recalculados entregados'))
    save(HERE/'fase3/ACEPTACION.json',dict(experimento_completo=False,entrega_incompleta_verificable=True,notebook_ejecutado=True,available_audit_contexts=a['verified_available_contexts'],no_new_fits=True,no_v6_performance_synthesis=True,historical_values_verified=True,text_evidence_checked=True,pendientes_indispensables=pending,phase1_acceptance_superseded=True))
    save(HERE/'REGISTRO_HALLAZGOS.md','''# Registro de hallazgos v6

## Falla activa de implementación y cierre

Evidencia: runner.py/run/unique[(año,ID)], ESPECIFICACION_V6.json/windows/budget y fase3/AUDITORIA_INCOMPLETA.json. Ajustes internos por ventana requeridos192 frente96consolidados. El código reutilizó fits entre externas; deduplicar copias después de ajustes no autoriza ese reuso. Error propio del asistente. Impacto: aceptación de fase1 insuficiente e invalidada, piloto incompleto, ninguna meta/síntesis dependiente admisible. Alternativa lógica/verificable dentro del contrato: detener, conservar, auditar lo disponible y cerrar incompleto. Resuelto como cierre; NO resolver científico/técnico mediante nuevos fits u otro experimento. No cambiar criterios ni denominar96como192.

Evidencia: fase2/DETENCION_CONTROLADA.json y antecedente ledger_interrumpido.json. Búsqueda de PID desde otra invocación no vio runner por namespace aislado; sin señales enviadas. Sesión44244 se interrumpió por write_stdin Ctrl-C y terminó130. Último pendiente sin medición/terminación individual consolidada. Impacto: control de terminación no aprobado y consumo conservador7200s, no tiempo medido. Alternativa aplicada: cerrar caída sin saldo reutilizable; original/snapshots preservados. No reabrir ledger.

## Incidencias resueltas sin impacto en datos originales

Fase1 ensayos001/002: orden de índices y código5/8frente05/08. Evidencia: fase1/antecedentes y histórico motor etapa1 memoria/levels_from_rowszfill2. Impacto: cotejo inicial no pasó; alternativa: ordenar/reiniciar índices y normalización textual histórica en memoria. Resuelto antes freeze; no cambiar población/valores/criterios. Refuerzo propio traversal/códigos únicos probado y notebook01reejecutado antesfitreal. Cada corrida inventada registra32fits; cuatrocorridas=128inventados, separadas de ledger real, todas con entorno exacto. No efectos predictivos de datos inventados.

Fase3 ensayoauditor001: respaldo sinfit no genera events_0.json y ledgerevents_shaNone. Impacto: lector falló, sin resultados inventados. Alternativa: aceptar ausencia solo sihashNone/eventoscero; resuelto lector independiente, sin modificar piloto. Auditor final coteja258contextos consolidados sin discrepancias. Notebook02primeroejecutado luego repetido solo por refuerzo llave/valor/SHA del texto (0fits); primera ejecución preservada. Análisis completo preparado en resultados.py y notebook planificado no ejecutado se distinguen de salidas reales incompletas.

Lecturas iniciales extensas truncadas y aparición incidental del plan entero en texto del creador se registran en lecturas; no ejecución por leerplan/prompt. Contrato releído íntegro separado; datos/JSONcompletos mediante código, resúmenes pequeños. PDF0páginas/web0/fuentesnuevas0. Sin reabrir históricos archivados ni alterar cierres para aceptar v6.

## Antecedentes verificables y límites activos

Notebook02/antecedents recalcula v2/v3/v5/recencia/memoria yGuainía desde fuentesguardadas; tablas/evidenciasSHA. No son nuevas evidencias independientes ni resultadosv6. Impacto: pueden incorporarse al texto solo atribuidos como históricos recálculosactuales. Alternativa aplicada: tabla histórica separada y ausencia explícita de métricas/meta v6.

DISPONIBILIDAD.json comprueba último año local2025/siguiente2026condicional. Fuente localnoautenticada/fechasdepublicación del panel no acreditadas; fuente local de consulta anterior no demuestra disponibilidad histórica. Impacto: no pronósticoanticipadodemostrado. Alternativa aplicada: documentar límite/siguientecondicional sin proyectar/objetivo4.

Guainía/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años/2021–2025vistos permanecen activos. Aceptación de entregaincompleta no acredita autenticidad/confirmación/causalidad ni resuelve fallo piloto. No siguientes acciones automáticas.
''')
    save(HERE/'LEEME_ENTREGA.md','''# Entrega v6 — INCOMPLETA

El experimento no es técnicamente aceptable: se reutilizaron ajustes internos entre ventanas externas. No hay métrica/meta/conclusión v6 admisible. Ledger cerrado conservadoramente, sin nuevo experimento ni reapertura. Fase1/aceptación/freeze se preservan, con aceptación supersedida por control incumplido.

Entregables: TEXTO_OBJETIVO3_TESIS.md (texto de cierre incompleto para incorporar con ese alcance), fase3/02_resultados_objetivo3.ipynb (6celdas reales,nbformat), EVIDENCIAS_TEXTO.csv (valores ligados a fuentes/llaves/SHA), INFORME_TECNICO.md, fase3/tablas/ (antecedentes históricos completos/Guainía/conteos/controles/258trabajosverificados/inventario), figura diagnóstica revisada, auditoría/sintéticos/lecturas/conservación/aceptación/pendientes/manifiestos/continuidad. No tablas/gráficos de desempeño v6 ni outputs fabricados. Código editable/generador y drafts no ejecutados preservados.

Notebooks:01controles→02cierre. No repetir generador tras cierre; resultados.py/analyse/figures/thesis son fuentes preparadas NO ejecutadas, no outputs. Notebook02usa exclusivamente audit_incomplete/antecedents/control_tables/diagnostic_figure/document. Entorno exacto/tmp/icfes-v2-fase2-venv Python3.12.14/sklearn1.9.1/54lock/semilla20261010/PYTHONDONTWRITEBYTECODE1. Sin datos personales ni archivos ajenos modificados.

Verificación solo lectura:
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python experimento_final_objetivo3_v6/verificar_cierre.py

El verificador documental inicial queda intacto y conserva sus supuestos de fase0; no usarlo sobre el inventario ejecutado. verificar_cierre coteja su mapping original y continuidad fase0 preservada. No modificar verificador/cierres anteriores para admitir nuevas carpetas. La aprobación del cierre verifica integridad de entrega incompleta, no ejecución científica completa. No commits/push/fuentes/instalaciones/objetivo4/modelofinal/otra versión/otroexperimento/avance automático.
''')
    save(HERE/'CONTINUIDAD_V6.md',f'''# Continuidad v6 — CIERRE FINAL INCOMPLETO, entrega verificable

2026-10-11 America/Bogota. Usuario envió expresamente fases1→2→3 del último experimento y exigió incompleto si falla indispensable. Se siguió rama incompleta después de detectar falla propia; no otra versión/experimento/modelofinal/objetivo4/proyección2026/simulación/notebookpersonal/fuentes/instalaciones/commit/push. Originales/cierres previos/.git intactos. Continuidad fase2 preservada fase3/antecedentes/CONTINUIDAD_ANTERIOR.md SHA{previous}; fase1enfase2antecedentes/fase0enfase1antecedentes.

Fase1: documental inicial lectura aprobado antes escrituras; mappinghistórico diseño28/implementación234/piloto1018/auditoría54, continuidades históricas reales/preservadas y fase2 íntegra, GitHEAD75c3a25182af363f47b0d743820f99084e18fed5/asunto/rama/ascendencia/sin posteriores, v5commitreal109797407d75d2097e5b71f8bcef3fc266bc61d2/temporal solo texto huella partida. EntornoPython3.12.14/sklearn1.9.1/54lockexactos/pipcheck/PYTHONDONTWRITEBYTECODE1/semilla20261010/fuentesSHAcontractuales revalidados, no sustitución. Fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3/derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc.

Contrato intacto: población ESTUDIANTE/no libertadS/grado11/seispuntajes/sincalendario/mediarecibida/geografíacolegio/igualpeso/2018nivel/2019historialnorepuesta/2020excluido/2021previo2019sinanualizar/165pares/meta5%/39IDs completos. Nivel/media/mediana/rezago/regularización/historyQR/Ridge/árbol/comúncorrección fijados antesfit; Pipelines/defaults/selectorbandas0.1MAE/RMSE→entradas→orden/persistenciaprimero/global_v6 fijo. No nuevos criterios o entradas. Notebook01controles3celdas ejecutadas/fuente/generador/sintéticos/freeze: aceptación inicial conservada pero INVALIDADA por prueba de no compartir fits entre ventanas insuficiente.

Falla ACTIVA: runner.py/run utilizaunique[(año,ID)] para emitir originales entre externas, compartiendo ajustes; requeridos192internos32×6, ejecutados96internos32×3. No resolver mediante redefinición de ventana/deduplicación. Piloto interrumpido sesiones44244/Ctrl-C/exit130;175fits terminados/58constantes en registro durable/último pending sin medición consolidada; no confundir con totalfitspotencialpendiente. Ledger abierto original preservado/snapshots intactos, caída consumida conservadoramente7200s/estado cerrado_incompleto/pending_unmeasured. Último wait/poll individual no consolidado, indispensable pendiente. No reopen/continuaciónfits/retry posterior. Congelación código operativo intacta, ninguna modificación retrospectiva para rescatar.

Fase3 en modo incompleto: auditor independiente sinimportsoperativos/deserialización/fits:258contextos disponibles cotejados,0discrepancias; no aceptación completa de cobertura/selección/linaje/CSV final/terminación. Pruebas inventadas auditor0fits/CSV0intfloatequivalente/rechazo1e-11/matrizalterada/selector/scaler/coef/fecha. Notebook02seisceldas realmente ejecutadas/nbformat/fuenteeditable/generador (segundaejecuciónjustificada controlvalor/llave/SHA,0fits); salidas/texto/figura de conteos todos desde celdasfunciones. Auditoría y artefactos insuficientes para métricasv6/meta/síntesis dependiente: NO CALCULADAS. Tablas completas disponibles solo antecedentes/controles/trabajos/inventario, nofabricar faltantes.

Antecedentes recalculados actual notebook desde guardados: v3MAE3.429267191379531 vs v2MAE4.879557188161031/mejora29.721754266970148%; memoria global1.7979745286559843%/políticamemoria12.392390281511053%históricos exploratorios, nuncaconclusionesv6. v3persistencia/v5global/recenciaglobal mismas165llaves/observados/predicciones, noevidenciaindependiente. Guainía238vs404/diferencia21.012105832431985puntos histórico v2archivo filas57/90recalculado. Próximo2026soloCONDICIONAL porúltimo2025local; DISPONIBILIDAD registra ausencia fecha publicación/disponibilidad histórica autenticada. Fuente localnoautenticada/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocosaños/todos2021–2025vistos exploratorio/sinconfirmación/causalidad/pronósticoanticipadodemostrado permanecen.

Entregables TEXTO_OBJETIVO3_TESIS.md como texto de cierre incompleto/INFORME_TECNICO/02notebook/tablas/figura diagnósticaQA/EVIDENCIAS_TEXTO/REGISTRO_HALLAZGOS/lecturas/aceptaciónincompleta/conservación/manifiesto/verificaciónlectura. LEEME_ENTREGA orienta ejecución y distingue drafts noejecutados. Pendientes técnicos{pending}; científicos en fase3/PENDIENTES. No cierre falso de indispensables/no cambio original/no fase automática. verificar_cierre.pysololectura valida integridad entregaINCOMPLETA y mappingdocfase0concontinuidadpreservada; no usar ni alterar cierres históricos para aceptar carpeta nueva.
''')
    manifest(3)
    exclusions=['MANIFIESTO_FINAL.json','VERIFICACION_FINAL.json']
    files={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if (p.is_file() or p.is_symlink()) and p.relative_to(HERE).as_posix() not in exclusions}
    save(HERE/'MANIFIESTO_FINAL.json',dict(status='cierre final incompleto; entrega verificable',experimento_completo=False,sha256=files,exclusions=exclusions,indispensables=pending))
    from verificar_cierre import verify
    result=verify();save(HERE/'VERIFICACION_FINAL.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
