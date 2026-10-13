"""Cierre documental después de notebook/texto; ninguna operación de ajuste."""
from infra import *
from preflight import conservation
import pandas as pd
def close():
    deadline();r=load(HERE/'resultados/PRIMARIO.json');a=load(HERE/'AUDITORIA.json');l=load(HERE/'piloto/ledger.json')
    check(a['aprobado'] and l['status']=='cerrado_completo','complete pilot and audit')
    c=conservation();save(HERE/'resultados/CONSERVACION_FINAL.json',c)
    save(HERE/'ACEPTACION_FINAL.json',dict(completa=True,operativa=True,tecnica=True,fits_auditor=0,authenticity_resolved=False,temporal_availability_resolved=False,independent_confirmation=False,notebook_executed=True,visual_review=True,text_verified=load(HERE/'CONTROL_TEXTO.json')['aprobado'],epoch=time.time()))
    pending='''# Pendientes científicos y límites

- Autenticar la fuente local y documentar la disponibilidad de cada medición antes de una evaluación prospectiva. La integridad técnica no acredita procedencia oficial.
- Todos los años ya fueron vistos; diseñar una evaluación posterior independiente requeriría otra autorización y datos comparables.
- Documentar mejor la relación hogares/personas/estudiantes y colegio/residencia; el enlace es ecológico. Pocos años y dependencia territorial.
- El contraste autorizado no ejecuta todo el diseño de las páginas58-59: no entradas de composición/año, contribuciones dimensionales, lasso/elastic net, respuesta de niveles de Matemáticas, exclusión de2021 ni validación territorial. No se inventan esas variables o se declara su ejecución.
- Último año local utilizable2025. Siguiente año exclusivamente condicional a información auténtica, comparable y temporalmente disponible; cero proyecciones.
- Objetivo4, escenarios, simulación, modelo final y avance automático no autorizados. Piloto cerrado, sin saldo reutilizable.
'''
    save(HERE/'PENDIENTES.md',pending)
    findings=[dict(hallazgo='Representación05/08 versus5/8',impacto='llaves literales fragmentarían historia',alternativa='canonicalizar dos dígitos y cotejar nombres antes de ajuste',resolucion='preflight/NORMALIZACION_CODIGOS.csv; fuente intacta; cero fits al decidir'),dict(hallazgo='Verificador histórico controla rutas ajenas',impacto='no puede aprobar carpeta nueva',alternativa='cotejo propio huellas/mappings, sin modificar original',resolucion='preflight/CONSERVACION.json y resultados/CONSERVACION_FINAL.json; aprobación histórica separada'),dict(hallazgo='Pobreza contemporánea y publicación local2026',impacto='no disponibilidad anticipada demostrada',alternativa='interpretación condicional con fecha local explícita',resolucion='resultados/FECHA_LOCAL.json; no forecast/causalidad'),dict(hallazgo='Resultado primario',impacto='determina alcance de aporte incremental',alternativa='respetar meta5% y políticas cerradas; diagnósticos secundarios',resolucion='resultados/PRIMARIO.json y TEXTO_OBJETIVO3_TESIS.md; sin rescate primario'),dict(hallazgo='Años ya vistos/dependencia',impacto='sin confirmación independiente',alternativa='describir contraste exploratorio y pendientes prospectivos',resolucion='PENDIENTES.md; cero escenarios')]
    save(HERE/'REGISTRO_HALLAZGOS.json',findings)
    technical=f'''# Informe técnico

Ejecución única autorizada por envío expreso. Preparación anterior preservada en antecedentes/CONTINUIDAD_PREPARACION.md y MANIFIESTO_PREPARACION.json. Inicio absoluto INICIO.json. No saldo previo, no ajustes repetidos de piloto anterior: no existía uno.

Preflight: entorno exacto de54distribuciones+pip25.0.1,Python3.12.14/sklearn1.9.1,pip check y un hilo. Conservación propia aprobada de{c['protegidos']}originales/mappings/cierres. HEAD/rama/asunto/ascendencia/trabajo posterior en preflight/CONSERVACION.json. Verificador anterior aprobado antes de carpeta nueva, conservado sin reejecutarlo parcialmente. Temporal etapa1 únicamente texto/huella de partida original.

Fuentes completas round_trip y códigos string. Normalización de representación geográfica antes de resultados, trazable porfila.231filas/33territorios/siete años;165pares externos. Media recibida, geografía colegio, conteos fuera deX, igualpeso. Cotejo exacto de historia/cambios y porcentajes. IPM%personas/tasas%hogares; quince en orden declarado, sin agregados inventados.

21candidatos,200fits originales seriales,{len(l['repetitions'])}repeticiones deduplicadas, {l['retries_used']}retries. Ledger cerrado a{l['elapsed_seconds']:.3f}s desde primera acción; ningún nuevofit después5400s. Procesos terminados, matrices y estadosdurables. Preservadas315matrices/315records, predicciones de21candidatos por15contextos. Modelos JSON: params/scaler/coefs/intercept/árbol/advertencias/huellas; no pickle/deserialización. Selecciones selladas antes de externas. Copias seleccionadas solo por referencia de huella, no comparten fits internos/externos.

Auditor independiente sin sklearn/diseño/selector operativo/runner/modelos/fits. Selección/métricas propias y reconstrucción desde parámetros guardados; matrices/fechas/cobertura/defaults/scaler/CSV/linaje/budget/terminación verificados. Exactitud CSV tras round_trip, 0entero=0float y rechazo1e-11. Predicciones/repeticiones tolerancia absoluta1e-10,rtol0. Pruebas inventadas antes de fits en preflight/PRUEBAS*.json. Revisiones de congelación anteriores fueron exclusivamente prefit; cadena en CONGELACION.json. Errores iniciales de forma de código/lectura CSV corregidos antes de toda métrica/fit, sin criterio científico cambiado.

Resultado nuevo exploratorio: MAE histórico {r['MAE_historico']:.17g}; ampliado {r['MAE_ampliado']:.17g}; reducción primaria {r['mejora_primaria_percent']:.17g}%; meta>=5%: {r['meta_cumplida']}. Procedimiento:analisis.tables, celda2 del notebook; confirmación independiente=False. No comparar el porcentaje primario directamente con denominadores de experimentos históricos. No se usaron métricas históricas como observaciones independientes ni se rescata primario con I/D/árboles/con_pobreza.

Notebook fuente/generador editables; preview para revisión visual y notebook final de5celdas realmente ejecutadas, ambas sinfits. Tablas/figuras/JSON/texto/evidencias provienen de funciones compartidas llamadas por celdas. Texto generado al final, después de gráficos y revisiónvisual. Fuentes/semilla/env congelados antes de ajustes; las validaciones finales no modifican reglas.

Leer RESULTADOS.ipynb y resultados/tablas completos. Comparaciones a mismoalpha, diagnósticos deárbol, grupos descriptivos por terciles de rangoIPM2018 (11territorios cadauno, desempate código; sin uso para selección), coeficientes estandarizados/originales, erroresfirmados/absolutos/sesgo/dirección/rangos disponibles. No criterios de confirmación estadística ni efectos causales. Los antecedentes históricos sin impacto se conservan archivados por huella; no se reabren.

La coherencia de la entrega no autentica fuentes. Las limitaciones y validaciones adicionales de la tesis no ejecutadas figuran en PENDIENTES.md y LECTURAS.json. Último año2025; nota local14abril2026 (no autenticación web). No nuevas fuentes/raw/red, no tesis original/experimentosajenos/.git/commit/push, no objetivo4/proyecciones/modelofinal. No avance automático.
'''
    save(HERE/'INFORME_TECNICO.md',technical)
    # preserve current own continuity before replacing it (original already saved)
    check(sha(HERE/'CONTINUIDAD.md')==sha(HERE/'antecedentes/CONTINUIDAD_PREPARACION.md'),'continuidad anterior conservada')
    save(HERE/'CONTINUIDAD.md',f'''# Continuidad propia: ejecución única completa y cerrada

Autorización: envío expreso del prompt actual; máximo7200s desde2026-10-12 18:07:59UTC. Preparación anterior cero fits/cero piloto preservada exactamente en antecedentes/CONTINUIDAD_PREPARACION.md. No saldo heredado ni piloto previo descubierto.

Preflight/conservación/entorno exacto/controlsinventados aprobados antes de fits; CONGELACION.json mantiene fuentes/defaults/candidatos/reglas/código/notebook/semilla20261010. Decisión nueva previa a resultados: normalización solo de representación05/08 vs5/8, por nombres estables y33territorios cada año; originales intactos. No cambio de población, media recibida, geografía colegio, igualpeso, entradas o criterios. Códigos strings y floatsround_trip. H dos variables dehistoria; I IPM%personas; D quince%hogares en ordenDIMENSIONES/TASAS; HI/HD; sin otras entradas.2018nivel,2019solo historia,2020excluido,previo2021=2019sinanualizar. Respuestas2021+,165pares2021-2025. Protocolo en PROTOCOLO.md y ESPECIFICACION.json.

21candidatos; {len(l['originals'])}fitsoriginales, {len(l['repetitions'])}repeticiones, {l['retries_used']}retry. Piloto cerrado_completo antes de análisis, sin pendiente ni saldo reutilizable. Auditor independiente aprobado,0fits/importsoperativos/modelos. Notebook5celdas reales sin nuevosfits, texto académico generado último, evidencias y revisiónvisual. Primario usa denominador MAEhistórico nuevo aprobado antes deresultados; valor/meta exclusivamente resultados/PRIMARIO.json. Sin rescate por diagnósticos/ganador externo.

Históricos: verificador vigente anterior aprobado antes de carpeta nueva (preparacion/VERIFICACION_ANTERIOR.json); cotejo actual propio de37744 originales/manifiestos/mappings/cierres. Commit109797407d75d2097e5b71f8bcef3fc266bc61d2 ytrabajoposterior verificados. Temporal etapa1 solo texto/huella de partida original. No original/.git modificado.

Entregas: TEXTO_OBJETIVO3_TESIS.md, RESULTADOS.ipynb, tablas/figuras completas, INFORME_TECNICO.md, REGISTRO_HALLAZGOS.json, LECTURAS.json, EVIDENCIAS_TEXTO.csv, aceptaciones/conservación/manifest/verificar_entrega.py. Pendientes científicos en PENDIENTES.md: fuente local noautenticada, disponibilidadsinverificar/ecología/pocosaños/dependencia/todosañosvistos/sinconfirmaciónindependiente. Último añoutilizable2025 ynotafechalocal14abril2026; siguienteañocondicional. No causalidad/objetivo4/escenarios/proyecciones/modelofinal/nuevasfuentes/red/commit/push/nuevaejecuciónautomática.
''')
    save(HERE/'CIERRE_SESION.json',dict(estado='completo',start_epoch=START,end_epoch=time.time(),elapsed_seconds=0,saldo_reutilizable=False,no_auto_advance=True))
    closure=load(HERE/'CIERRE_SESION.json');closure['elapsed_seconds']=closure['end_epoch']-START;save(HERE/'CIERRE_SESION.json',closure)
    from verificar_entrega import verify
    preliminary=verify(require_manifest=False);save(HERE/'VERIFICACION_PREMANIFIESTO.json',preliminary)
    paths={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
    exclusions=['MANIFIESTO_FINAL.json','VERIFICACION_FINAL.json'];paths={n:h for n,h in paths.items() if n not in exclusions}
    save(HERE/'MANIFIESTO_FINAL.json',dict(sha256=paths,exclusions=exclusions,closure_sha256=sha(HERE/'CIERRE_SESION.json'),scope=HERE.name))
    final=verify();save(HERE/'VERIFICACION_FINAL.json',final)
    # El tiempo de verificaciones y cierre también cuenta; manifiesto se actualiza al cierre real.
    closure['end_epoch']=time.time();closure['elapsed_seconds']=closure['end_epoch']-START;check(closure['elapsed_seconds']<=7200,'global time');save(HERE/'CIERRE_SESION.json',closure)
    m=load(HERE/'MANIFIESTO_FINAL.json');m['sha256']['CIERRE_SESION.json']=sha(HERE/'CIERRE_SESION.json');m['closure_sha256']=sha(HERE/'CIERRE_SESION.json');save(HERE/'MANIFIESTO_FINAL.json',m)
    print(json.dumps(dict(aprobado=final['aprobado'],elapsed_total_seconds=closure['elapsed_seconds'],files=len(m['sha256'])),ensure_ascii=False))
if __name__=='__main__':close()
