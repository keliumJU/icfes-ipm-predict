"""Conservación de antecedentes y cierre propio; ningún fit/commit/push."""
import sys,json,hashlib,subprocess,ast
from pathlib import Path
import nbformat
from seguridad import ROOT,OWN,E1,OUT,guardar,leer,sha,destino
from preflight import entorno,check_entries,entries,git

def manifest_mapping(exclusions):
    files=[]
    for p in E1.rglob('*'):
        assert not p.is_symlink(),'Symlink propio prohibido'
        if p.is_file() and str(p.relative_to(ROOT)) not in exclusions:files.append(p)
    files.append(OWN/'CONTINUIDAD_EXPERIMENTAL.md')
    return entries(files)
def verify():
    manifest=leer(OUT/'manifiesto_cierre.json');actual=manifest_mapping(manifest['exclusiones'])
    assert actual==manifest['entregables'],'Cobertura/huellas propias cambiadas'
    check_entries(leer(OUT/'partida.json')['protegidos']);check_entries(leer(OUT/'congelacion_operativa_v2.json')['fuentes'])
    assert git('rev-parse','HEAD').strip()==leer(OUT/'partida.json')['git']['head']
    return dict(aprobado=True,entregables=len(actual),manifiesto_sha256=sha(OUT/'manifiesto_cierre.json'),antecedentes_intactos=True,completa=True,fits_historicos=0,commit=0,push=0)
def main():
    if '--verificar' in sys.argv:print(json.dumps(verify(),ensure_ascii=False));return
    assert leer(OUT/'ejecucion.json')['completa'] and leer(OUT/'auditoria_independiente.json')['aprobado']
    assert leer(OUT/'notebook.json')['aprobado'] and leer(OUT/'notebook.json')['celdas_codigo_ejecutadas']==6
    check_entries(leer(OUT/'partida.json')['protegidos']);check_entries(leer(OUT/'congelacion_operativa_v2.json')['fuentes'])
    snapshot=leer(OUT/'partida.json');assert git('ls-files','-z').split('\0')[:-1]==snapshot['git']['versionados']
    assert git('branch','--show-current').strip()==snapshot['git']['rama'] and git('rev-parse','HEAD').strip()==snapshot['git']['head']
    assert sha(OWN/'CONTINUIDAD_EXPERIMENTAL.md')==snapshot['continuidad_sha256']
    for p in (E1/'fuentes').glob('*.py'):ast.parse(p.read_text(),str(p))
    nbformat.validate(nbformat.read(E1/'notebooks/01_resultados_recencia.ipynb',as_version=4))
    ledger=leer(OUT/'ledger.json');meta=leer(OUT/'meta.json');audit=leer(OUT/'auditoria_independiente.json')
    guardar(OUT/'entorno_final.json',entorno())
    guardar(OUT/'conservacion_final.json',dict(aprobado=True,protegidos=len(snapshot['protegidos']),etapa1_intacta=True,versionados_intactos=len(snapshot['git']['versionados']),diagnostico_diseno_intactos=True,continuidad_etapa1_previa_preservada_en='resultados/partida.json:continuidad_inicial',continuidad_sha256_antes=snapshot['continuidad_sha256'],git=snapshot['git'],no_reset=True,commit=0,push=0,raw='Sin lectura/censo/escritura',antecedentes_archivados='No reabiertos'))
    guardar(OUT/'lecturas.json',dict(archivos=[dict(archivo=n,alcance=a,sha256=sha(ROOT/n)) for n,a in [('AGENTS.md','Completo'),('experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md','Completa, estado inicial conservado antes de actualizar'),('diseno_temporal_objetivo3_v1/CONTINUIDAD_DISENO.md','Completa'),('diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md','Completa, vigente y antecedentes diferenciados'),('diseno_temporal_objetivo3_v1/PROTOCOLO_TEMPORAL.md','Completo1.0.0'),('experimentos_temporales_objetivo3_v1/etapa1/PROTOCOLO_IMPLEMENTACION.md','Completo'),('diseno_temporal_objetivo3_v1/ESPECIFICACION_PROPUESTA.json','JSON íntegro procesado, herencia exacta; salida informativa truncada no usada como prueba'),('experimentos_temporales_objetivo3_v1/etapa2/PLAN_ETAPA2.md','Solo fase2 propia autorizada')]],fuentes_etapa1='comun/seguridad/preflight/cerrar/orquestacion/motor/worker completos; pruebas1–180 y reportes finales íntegros',datasets='Única fuente v2 y derivado v5 completos mediante código; 2CSVreferencia completos; todas predicciones propias completas',manifiestos='Mapas enteros verificados por preflight; continuidadv5etapa1 solo commitreal109797407d75d2097e5b71f8bcef3fc266bc61d2',pdf_paginas=0,web=0,fuentes_extra=0,pendiente='Ninguna lectura indispensable para este piloto; disponibilidad/confirmación futuras requieren otra autorización'))
    guardar(OUT/'registro_hallazgos.json',dict(fecha='2026-10-11',timezone='America/Bogota',autorizacion='Prompt humano fase2 expresamente enviado, condicionado a etapa1 revalidada',hallazgos=[dict(id='R1',ubicacion='preflight.json/entorno.json',impacto='Permite ejecutar contrato sin cambiar datos/defaults/entorno',alternativa='Revalidación integral independiente de afirmaciones históricas',resolucion='APROBADO antes fit'),dict(id='R2',ubicacion='salida_piloto.log/incompleto.json/congelacion_operativa_v2.json',impacto='Lectura de esquema symlink detuvo antes primerfit; no afecta análisis científico',alternativa='Aceptar ambos esquemas de conservación sin cambiar hashes',resolucion='Corregido/revalidado/recongelado antes fit; original archivado, fits0'),dict(id='R3',ubicacion='auditoria_independiente.json/linaje_internas.csv',impacto='Evita pseudo-repetición de años/candidatos',alternativa='Igualdad exacta y train/X/y/weights/metadata idénticos',resolucion='11880→4752 condicionado aprobado, menor externo, sin promediar'),dict(id='R4',ubicacion='meta.json/tablas/metricas_externas.csv',impacto='Meta primario '+('SATISFECHA' if meta['cumple'] else 'NO SATISFECHA'),alternativa='Conservar referencia y todas salidas descriptivas, sin rescatar con grupos/control/cortes',resolucion='Informe completo; investigación exploratoria cerrada, no avance automático')],antecedentes_propios_archivados=[dict(archivo='resultados/incompleto.json',motivo='Intento inicial antes fits0, bloqueo helper resuelto; no estado actual',evidencia='salida_piloto.log y congelacion_operativa_v2.json')],incidencias_lectura=['JSON propuesta salida informativa truncada, procesado completo en preflight/auditoría'],modelos_historicos_cargados=0,fuentes_extra=0,instalaciones=0,commit=0,push=0,criterios_cambiados=False))
    readme='''# Etapa2 — piloto exploratorio recencia_h2 cerrado

Entradas únicas y decisiones: PLAN_ETAPA2.md; protocolo temporal1.0.0 y contratos
fase1 aprobados intactos. Resultado y meta exacta: INFORME.md/resultados/meta.json.
Validación: resultados/auditoria_independiente.json, conservación/manifiesto.
Orden ejecutado: fuentes/preflight.py→piloto.py→auditar.py→resultados.py→
generar_notebook.py→cerrar.py. Fuentes editables Python; notebook útil solo resultados
notebooks/01_resultados_recencia.ipynb con6celdas realmente ejecutadas. Python3.12.14,
sklearn1.9.1/54lock/pipcheck antes uso/al cierre; semilla20261010, sin instalaciones.

Ledger nuevo7200s persistente, serial spawn terminable, modelos propios guardados por
ajuste; sin comparadores históricos cargados. Reanudación no amplía saldo y exige
contexto/huellas/artefactos/intentos idénticos; pendiente no medido agota presupuesto.
2021fijo persistencia sinfit/selección. 350internos,≤24externos,≤4repeticiones,cota378.
Pesos/metadatos/matrices/objetivos/routing/scaler/defaults/warnings en metadatos/;
selecciones antesexterno; predicciones porajuste/ventana/originales/únicas/linaje.

Tablas completas y3gráficos con unidades/n en resultados/. MAE/RMSE/sesgo/deltas/
dirección/magnitud/años/territorios/cortes; grupos secundarios sin rescate/meta parcial.
ControlCSVv5global yv3persistencia idénticos,no evidenciaindependiente. Todos2021–2025
vistos: exploratorio,sinconfirmaciónindependiente/causalidad/pronósticoanticipado.
Guainía238vs404/21.012106puntos histórico;localnoautenticada/IPMhogares-alumnos/
colegio-residencia/ecología/dependencia/pocosaños. No etapa3v5/modelofinal/simulación/
notebookpersonal/objetivo4/commit/push/fuentesextra/avanceautomático.

Archivo incompleto.json ysalida_piloto.log conservan el primerintento sinfits,
resuelto por recongelaciónv2; no describen el cierre actual. Continuidad inicial
preservada textualmente/hash en partida.json. Etapa1 no modificada; su manifiesto
histórico incluye la continuidad anterior, que se consulta allí para validar ese
estado previo, sin atribuirle el cierre etapa2. No modificar el manifiesto etapa1.
'''
    (E1/'README.md').write_text(readme)
    guardar(OUT/'aceptacion_etapa2.json',dict(completa=True,aprobado=True,meta_satisfecha=meta['cumple'],auditoria=True,notebook6=True,conservacion=True,pendientes_indispensables=[],pendientes_cientificos=['Confirmación independiente/disponibilidad operacional requieren fuentes comparables/fechas y autorización separadas'],avance_auto=False,primario='recencia_h2/global'))
    intern=sum('_i20' in r['etiqueta'] for r in ledger['ajustes']);ext=sum('_externo_' in r['etiqueta'] for r in ledger['ajustes']);rep=sum('_repeticion_' in r['etiqueta'] for r in ledger['ajustes'])
    text=f'''# Continuidad experimental temporal — etapa2 exploratoria completa

2026-10-11 America/Bogota. Usuario envió expresamente promptfase2, condicionado a
fase1 experimental completa/congelada. Revalidación pasó antes todo fitreal:77
entregables/freeze/defaults/17grupos pruebas/notebook6 yconservación antecedentes.
Etapa1 permanece intacta; continuidadinicial íntegra en etapa2/resultados/partida.json
con SHA{snapshot['continuidad_sha256']}. Manifiesto histórico etapa1 incluye esa
continuidad anterior: cotejar esa versión preservada para su estado, no alterar
etapa1 ni presentar su declaración sinpiloto como estadoactual. Diseño/diagnóstico
cerrados intactos. No existía planexperimental secciónfase2; contrato aprobado
concretado antesfit en etapa2/PLAN_ETAPA2.md sin cambiar objetivos/criterios.

GitHEAD{snapshot['git']['head']},asunto `{snapshot['git']['asunto']}`,
rama{snapshot['git']['rama']},ascendencia ysintrabajoposterior confirmados;noreset/
checkout/commit/push. Conservación{len(snapshot['protegidos'])}antecedentes, incluidos
29640versionados ydiagnóstico/diseño/etapa1. Continuidadhistóricav5etapa1 cotejada en
commitreal109797407d75d2097e5b71f8bcef3fc266bc61d2, ningunaotraexcepción. Raw sinlectura/censo.

Entornoexacto /tmp/icfes-v2-fase2-venv/bin/python,Python3.12.14/sklearn1.9.1/54lock/
pipcheck antesuso yal cierre,PYTHONDONTWRITEBYTECODE=1,semilla20261010;sininstalación.
Fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;
derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc,
231/33/198 reconstruidos exactos campos/llaves/valores/orden;GRUPOS/18entradas/36IDs/
defaults iguales;2021previo2019/intervalo2sinanualizar. Referencias165paresoriginales
v5global/v3persistencia idénticos numéricamente, no evidenciasindependientes.

Decisionesusuario conservadas población/mediarecibida/geografíacolegio/objetivo/
2020excluido/2018historial/evaluaciónigualpeso/meta5%/bandas0.1. Único cambio aprobado
pesostrainrecencia_h2 semivida2,n*bruto/fsum,anclamaxtrain,todospositivos y toda historia.
Scaler/regresor ponderados,boostingpesoexplícito;uniformevector1rutaoriginal. No añadir
anio/código a X/nuevafamilia/variable/lambda/búsqueda/mezcla/imputación/clipping/fuente.
2021 fijo persistencia sinfit/puntuación/selección;desde2022selecciónantesexterno,
globalindependientegrupos,dedupsoloIDigual,no reutilizarinternosentreventanas.

Ejecuciónactual propia:{intern}internos/{ext}externos/{rep}repeticiones ajustadas,
{len(ledger['ajustes'])}intentos/{ledger['consumido']!r}segundos/7200nuevo;ledger persistente
arranque/Pipeline/comunicación, sinfallos/retries. Persistenciasinfit tiempoaparte.
Cinco controlesglobales aprobados, repeticiónatol1e−10rtol0 o previoexacto. Sin nuevos
fits uniformes reales ni cargasmodeloshistóricos. Modelos propios porajuste guardados,
no modelofinal. X/y/llaves/weights/normalización/anios/scaler/defaults/semilla/versiones/
advertencias/tiempos/huellas/predicciones/selecciones/repeticiones completos.

Auditoría independienteaprobada:11880internasoriginales/36IDs/144registros/1155externas
7×165/33territorios×5años.4752únicas tras copias ycontexto idénticos,linaje11880 ymenor
externorepresentante; originalesporventana preservados. CSVexactos/intfloat0 equivalente,
rechazos1e−11/campos/orden/nofinitos. Referencias/weights/scaler/presupuesto/cobertura
resueltos. Primario recencia/global fijo;MAE{meta['mae_recencia_global']!r},persistencia
{meta['mae_persistencia']!r},mejoraexacta{meta['mejora_porcentaje']!r}%,meta5%
{'SATISFECHA' if meta['cumple'] else 'NO SATISFECHA'}. DeltaMAErecencia−v5global{meta['delta_mae_v5']!r}
descriptivo,sinnuevoumbral;165llaves/observadosidénticos/denominadorpositivofinito.
Grupos/cortes/control no reemplazan primario;sinrescate/metaparcial.

Incidencia propia antesprimerfit: helperdestino/enlace de symlink;fallooriginal
incompleto.json/salida_piloto.log conservados,corregido/revalidado/recongeladov2 antes
fitreal. Archivado con evidencia/motivo,no problemaactivo ni antecedente científico.
Entregables README/informe/plan/fuentes/tablas/3PNG/notebooksoloresultados6celdasexec/
registro/lecturas/auditoría/entorno/conservación/manifiesto/verificación/cierre propios.
Notebook desdefuentePythoneditable/generadornbformat;noejecucionesfabricadas.
No pendientesindispensablesfase2. Confirmación/disponibilidad/máshistoria pendientes
requieren fuentescomparables/fechas yautorizaciónseparadas; nofuentesextraobtenidas.

Todos2021–2025vistos:EXPLORATORIO,sinconfirmaciónindependiente/causalidad/pronóstico
anticipadodemostrado. Guainía238vs404/21.012106puntos histórico v2/fase1/resultados/
diagnostico_medias_disponibles.csv; localnoautenticada/IPMhogares-alumnos/colegio-
residencia/ecología/dependencia/pocosaños preservados. Antecedentesarchivados no reabiertos.
V5metaNOsatisfechaintacta;NOetapa3v5/excepción/notebookpersonal/simulación/objetivo4/
entrenamientofinal/commit/push/avanceauto. Toda escritura etapa2 ycontinuidadpropia.
'''
    path=destino(OWN/'CONTINUIDAD_EXPERIMENTAL.md',OWN);path.write_text(text)
    exclusions=[str((OUT/n).relative_to(ROOT)) for n in ('manifiesto_cierre.json','verificacion_cierre.json')]
    guardar(OUT/'manifiesto_cierre.json',dict(version='1.0.0',fase2_completa=True,entregables=manifest_mapping(exclusions),exclusiones=exclusions,meta_satisfecha=meta['cumple']))
    result=verify();guardar(OUT/'verificacion_cierre.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
