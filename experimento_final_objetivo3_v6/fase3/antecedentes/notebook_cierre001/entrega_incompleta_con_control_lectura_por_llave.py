"""Entrega verificable de cierre incompleto, llamada únicamente por notebook02."""
from comun import *
from resultados import csvsave,readcsv,OUT,TABLES
import math
import pandas as pd
def control_tables():
    a=load(OUT/'AUDITORIA_INCOMPLETA.json');spec=load(HERE/'ESPECIFICACION_V6.json');jobs=readcsv(TABLES/'trabajos_consolidados_verificados.csv')
    totals=[]
    for role,expected in [('interno',spec['budget']['internal_component_fits']),('externo',spec['budget']['external_component_fits']),('check',spec['budget']['global_repeat_component_fits_max'])]:
        g=jobs[jobs.role==role];totals.append(dict(role=role,component_fits_durable=int(g.component_fits_completed.sum()),contract_count_or_max=expected,meaning='máximo' if role=='check' else 'cantidad requerida',jobs=len(g),constant_estimates=int(g.statistical_estimates.sum())))
    csvsave('conteos_operativos_incompletos',totals)
    contracts=dict(candidates=len(spec['candidates']),components_per_context=sum(len(c['components']) for c in spec['candidates']),internal_trainable_window_contexts=sum(i['validacion']>=2022 for w in spec['windows'] for i in w['internas']),observed_unique_internal_trainable_years=3,external_windows=len(spec['windows']),external_years=[w['externo'] for w in spec['windows']],internal_windows=sum(len(w['internas']) for w in spec['windows']),target_percent=spec['target_percent'],population_territories=33,evaluation_pairs=165,excluded_year=2020,first_level=2018,history_only_response_excluded=2019,MAE_band=spec['selection']['MAE_band'],RMSE_band=spec['selection']['RMSE_band'],budget_seconds=spec['budget']['seconds'],seed=SEED,full_internal_original_rows=spec['coverage']['internal_original'],full_external_rows=spec['coverage']['external'],full_unique_internal_rows=spec['coverage']['internal_unique_conditional'],full_selection_rows=spec['coverage']['selection_records'],notebook_fits=0,status='cantidades contractuales, no cobertura lograda')
    save(OUT/'CONTRATO_COTEJADO.json',contracts)
    csvsave('controles_y_pendientes',[dict(control=k,passed=v,impact='verificable localmente' if v else 'impide aceptación completa o síntesis dependiente') for k,v in a['controls'].items()])
    inventory=[]
    for f in sorted((HERE/'fase2/piloto').rglob('*')):
        if f.is_file():inventory.append(dict(file=f.relative_to(HERE).as_posix(),bytes=f.stat().st_size,sha256=sha(f),status='guardado parcial; no resultado primario admisible'))
    csvsave('inventario_guardados_parciales',inventory)
    print(pd.DataFrame(totals).to_string(index=False));print(contracts);return contracts
def diagnostic_figure():
    os.environ['MPLCONFIGDIR']=str(OUT/'cache_matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    a=load(OUT/'AUDITORIA_INCOMPLETA.json');c=load(OUT/'CONTRATO_COTEJADO.json');fig,ax=plt.subplots(figsize=(7.5,4.4),layout='constrained')
    values=[a['internal_fits_contract'],a['internal_fits_durable']];labels=['Contrato: ajustes por ventana','Ejecución: ajustes por año único'];bars=ax.bar(labels,values,color=['#147a89','#b55a45'],width=.55)
    ax.bar_label(bars,padding=3);ax.set(ylabel='Componentes ajustados (conteo)',ylim=(0,max(values)*1.2),title='Control interno incumplido — v6 incompleto')
    ax.text(.5,.95,f"{c['components_per_context']} componentes por contexto • {c['internal_trainable_window_contexts']} contextos requeridos\nLa deduplicación posterior no autoriza compartir ajustes",transform=ax.transAxes,ha='center',va='top',fontsize=9)
    ax.grid(axis='y',alpha=.2);folder=OUT/'figuras';folder.mkdir(parents=True,exist_ok=True);p=folder/'01_control_ajustes_internos.png';fig.savefig(p,dpi=180);plt.close(fig)
    save(OUT/'FIGURAS_ORIGEN.json',dict(cell=5,function='entrega_incompleta.diagnostic_figure',files={p.name:sha(p)},input=sha(OUT/'AUDITORIA_INCOMPLETA.json'),unit='componentes ajustados; control técnico, no desempeño',performance_figure=False));print(str(p));return p
def document():
    a=load(OUT/'AUDITORIA_INCOMPLETA.json');c=load(OUT/'CONTRATO_COTEJADO.json');hist=readcsv(TABLES/'antecedentes_recalculados.csv');gu=readcsv(TABLES/'guainia_historico.csv');av=load(OUT/'DISPONIBILIDAD.json');evidence=[]
    def ev(claim,value,path,key,cell,function,n,unit):
        evidence.append(dict(claim=claim,value=str(value),cell=cell,function=function,file=str(path.relative_to(HERE)),table=path.stem,key=key,n=n,unit=unit,sha256=sha(path)));return value
    def avalue(key):return ev('control_'+key,a[key],OUT/'AUDITORIA_INCOMPLETA.json',key,2,'auditor.audit_incomplete',a['available_consolidated_jobs'],'conteo o segundos según llave')
    for k,v in c.items():
        if isinstance(v,(int,float,list)):ev('contrato_'+k,v,OUT/'CONTRATO_COTEJADO.json',k,4,'entrega_incompleta.control_tables',165,'cantidad contractual; no cobertura ejecutada')
    for idx,row in hist.iterrows():
        for col in hist.columns:ev('hist_'+str(idx)+'_'+col,row[col],TABLES/'antecedentes_recalculados.csv',f'row={idx};column={col}',3,'resultados.antecedents',165,'puntos MAE/RMSE/sesgo;porcentaje mejora;n conteo')
    for idx,row in gu.iterrows():
        for col in gu.columns:ev('guainia_'+str(idx)+'_'+col,row[col],TABLES/'guainia_historico.csv',f'row={idx};column={col}',3,'resultados.antecedents',row.n_complete,'registros/diferencia en puntos/ubicación histórica')
    for key in ['last_usable_year','next_year_conditional']:ev(key,av[key],OUT/'DISPONIBILIDAD.json',key,3,'resultados.antecedents',231,'año local/condicional')
    # Tablas históricas completas con unidades separadas de los porcentajes y sus bases.
    lines=['| Antecedente | MAE (puntos) | RMSE (puntos) | Mejora (%) | Base de mejora |','|---|---:|---:|---:|---|']
    for _,row in hist.iterrows():
        base='v2 global' if row.label=='v3_persistencia' else 'v3 persistencia' if row.label.startswith('memoria_') else 'referencia idéntica o base propia'
        lines.append(f'| {row.label} | {row.MAE:.6f} | {row.RMSE:.6f} | {row.improvement_vs_reference:.6f} | {base} |')
    table='\n'.join(lines);reference=hist[hist.label=='v3_persistencia'].iloc[0];v2=hist[hist.label=='v2_global'].iloc[0]
    text=f'''# Objetivo 3. Evaluación predictiva territorial y cierre del experimento exploratorio v6

## Objetivo, datos y alcance

El objetivo fue evaluar si un procedimiento predefinido podía mejorar la predicción del puntaje global promedio territorial respecto a persistencia. Se mantuvo la población de estudiantes de grado once, sin privación de libertad reportada, con seis puntajes presentes y positivos y sin filtro por calendario. La ubicación fue la del colegio y se conservó la media global recibida, sin sustituirla por un promedio de subpruebas. La evaluación acordada asignó igual peso a {c['evaluation_pairs']} pares de {c['population_territories']} territorios entre {min(c['external_years'])} y {max(c['external_years'])}; estas cantidades describen el diseño, no una cobertura v6 validada.

El panel local conserva niveles desde {c['first_level']}, excluye {c['excluded_year']} y define cada cambio respecto al máximo año previo disponible del mismo territorio, sin anualizar. Para el primer año externo, el previo fue {c['history_only_response_excluded']}. Este último año sirvió como historial, pero no como respuesta supervisada, porque no existe el cambio previo requerido. Los años externos ya habían sido examinados durante el desarrollo; cualquier resultado admisible de este proceso sería exploratorio, sin confirmación independiente ni pronóstico anticipado demostrado.

## Antecedentes verificados

Los resultados anteriores se recalcularon actualmente desde predicciones guardadas, sobre llaves y observados cotejados. La persistencia v3 obtuvo MAE {reference.MAE:.6f} puntos frente a {v2.MAE:.6f} puntos del procedimiento v2, con mejora de {reference.improvement_vs_reference:.6f} %. El ganador fue persistencia; esta comparación no demuestra aprendizaje del IPM. Las referencias globales v5 y recencia coincidieron exactamente con persistencia en llaves, observados y predicciones, por lo que no representan evidencia independiente.

Tabla 1. Recálculos actuales de resultados históricos. Los porcentajes usan las bases indicadas y no se suman entre sí. Los resultados de memoria son exploratorios y no son conclusiones v6.

{table}

## Contrato del último experimento

La grilla cerrada v6 contenía {c['candidates']} candidatos: persistencia, nivel histórico por media o mediana, memoria del cambio, regularización, historia completa o últimos años, Ridge, árboles pequeños, componente común y componente común con corrección territorial. Se conservaron el objetivo, la población, las variables y las ventanas. Año, código, intervalos, conteos, IPM y tasas de privación no entraron como predictores. Los niveles constantes debían contabilizarse como estimaciones históricas, aun sin llamar a sklearn.fit.

Cada componente ajustado debía utilizar un Pipeline nuevo por candidato y ventana, con StandardScaler estimado solo en entrenamiento. La selección se fijó exclusivamente mediante ventanas internas: banda MAE de {c['MAE_band']:.1f} puntos, luego banda RMSE de {c['RMSE_band']:.1f} puntos dentro del grupo, menor número de entradas predictoras y orden establecido. Las constantes contaron como cero entradas y persistencia tuvo prioridad en el orden. La ventana externa inicial quedó fijada en persistencia, sin ajuste, puntuación ni selección. El primario fue global_v6 y la meta pactada fue una mejora adicional de {c['target_percent']} % frente a persistencia. No se autorizó reemplazarlo por la mejor política externa.

## Incidencia de implementación y decisión de cierre

Durante el piloto se identificó que el runner construía un ajuste interno por candidato y año de validación y lo reutilizaba entre ventanas externas. Esto incumplió el requisito de ajustes nuevos por componente, candidato y ventana. La deduplicación de copias estaba permitida únicamente después de ejecutar los ajustes y comprobar identidad de contexto y salida; no permitía compartir el ajuste para producir esas copias.

El contrato requería {avalue('internal_fits_contract')} componentes ajustados internos, mientras el registro durable contiene {avalue('internal_fits_durable')} componentes internos. Esta diferencia es un error de implementación propio, no una razón para modificar los criterios de evaluación. Los tests de la fase de implementación habían pasado, pero no verificaron adecuadamente que el runner preservara la identidad de las ventanas durante la ejecución. La aceptación inicial se conserva como antecedente documental y queda invalidada por este control indispensable.

El piloto se interrumpió. Antes del último trabajo pendiente, el registro consolidó {avalue('consolidated_fits_durable')} componentes terminados y {avalue('constant_estimates_durable')} estimaciones constantes. Estos son conteos operativos durables, no una afirmación sobre la totalidad de ajustes que pudo iniciar el último proceso. El último snapshot consolidado registraba {avalue('last_measured_snapshot_seconds'):.3f} segundos; al no contar con medición consolidada del pendiente, se consumieron conservadoramente los {avalue('budget_consumed_conservative_seconds')} segundos del presupuesto conforme a la regla de caída. El ledger se cerró sin reapertura ni reinicio.

La ejecución principal terminó por interrupción, pero no quedó consolidado el registro individual de terminación del último trabajador. Este control se mantiene incompleto y no se sustituye por una afirmación de aprobación. La auditoría independiente cotejó {avalue('verified_available_contexts')} contextos disponibles frente a fuentes, matrices, fechas, defaults, unidades, escalas, coeficientes o estructura de árbol y predicciones guardadas. Estos cotejos locales no corrigen el incumplimiento de ejecución por ventana ni la cobertura incompleta.

![Diagnóstico de ajustes internos](fase3/figuras/01_control_ajustes_internos.png)

La figura presenta un control técnico de conteos y no una comparación de desempeño. El impacto del hallazgo es impedir una evaluación válida del procedimiento v6. La alternativa verificable fue conservar los artefactos, registrar la incidencia, auditar únicamente lo disponible y cerrar incompleto. Se adoptó esta alternativa sin repetir ajustes, ampliar el presupuesto, crear otro experimento o reinterpretar el mejor resultado parcial.

## Resultado admisible y limitaciones

**V6 no produjo un resultado primario técnicamente válido. No se calculó ni se declara una mejora v6, éxito o fracaso de la meta, ni una conclusión sobre nivel frente a rezago, regularización, historia o corrección a partir de este piloto.** Las predicciones parciales se conservan como evidencia de ejecución, pero no se sintetizan como resultados de la tesis. El cierre distingue el fallo de implementación de los antecedentes históricos que sí pudieron recalcularse.

La conservación por huellas no autentica la fuente local ni acredita la disponibilidad temporal de los datos. El antecedente de Guainía conserva {int(gu.iloc[0].n_complete)} registros completos frente a {int(gu.iloc[0].n_global)} con puntaje global disponible y una diferencia de {gu.iloc[0].difference:.6f} puntos, en diagnóstico_medias_disponibles.csv de v2, filas de archivo {int(gu.iloc[0].file_line)} y {int(gu.iloc[1].file_line)}. Se mantuvo la media recibida; no se corrigió la población para mejorar el error. El IPM describe hogares y Saber 11 describe estudiantes; la ubicación del colegio no equivale a residencia. La agregación territorial, dependencia entre años y territorios y escasez de años limitan las interpretaciones ecológicas. No se atribuyen efectos causales ni se reportan p-valores confirmatorios.

## Conclusión y siguiente horizonte condicional

Los antecedentes verificables muestran el valor de una referencia simple de persistencia y la necesidad de separar resultados exploratorios de evidencia independiente. La ejecución final v6 se cierra incompleta por un control indispensable, sin rescatar una política externa ni atribuir eficacia al procedimiento incompleto. La auditoría de lo disponible y el notebook documentan qué pudo verificarse y qué permanece pendiente; no constituyen aceptación técnica completa del experimento.

El último año utilizable comprobado en el panel local fue {av['last_usable_year']}. El siguiente año sería {av['next_year_conditional']} solo condicionalmente a datos comparables y disponibilidad verificable, con autorización separada. El registro local de consulta en auditoria/fuentes_verificadas.md no acredita una fecha histórica de publicación o disponibilidad del panel. No se emitieron proyecciones, no se ejecutó el objetivo siguiente y no se seleccionó ni entrenó un modelo final.

## Ubicaciones verificables

Notebook ejecutado: fase3/02_resultados_objetivo3.ipynb, desde notebook_resultados.py y generar_notebook.py. Auditoría: fase3/AUDITORIA_INCOMPLETA.json; fase3/tablas/trabajos_consolidados_verificados.csv. Incidencia y cierre: fase2/DETENCION_CONTROLADA.json, fase2/ACEPTACION.json y fase2/piloto/ledger.json; estado abierto anterior preservado en fase2/antecedentes/ledger_interrumpido.json. Contrato: PROTOCOLO_V6.md §§2–7 y ESPECIFICACION_V6.json/budget/windows. Antecedentes recalculados y Guainía: fase3/tablas/antecedentes_recalculados.csv y guainia_historico.csv; fuentes originales en sus columnas source/file. Disponibilidad: fase3/DISPONIBILIDAD.json y registro local auditoria/fuentes_verificadas.md líneas3–7. EVIDENCIAS_TEXTO.csv liga cada cifra a celda, función, archivo, tabla, llave, tamaño, unidad y huella. No se añadieron citas bibliográficas ni resultados inexistentes.
'''
    save(HERE/'TEXTO_OBJETIVO3_TESIS.md',text)
    ev('figura_control_interno',sha(OUT/'figuras/01_control_ajustes_internos.png'),OUT/'FIGURAS_ORIGEN.json','files/01_control_ajustes_internos.png',5,'entrega_incompleta.diagnostic_figure',c['internal_trainable_window_contexts'],'SHA256; conteos192/96 ligados a auditoría')
    csvsave('evidencias_texto',evidence);(HERE/'EVIDENCIAS_TEXTO.csv').write_bytes((TABLES/'evidencias_texto.csv').read_bytes())
    for row in evidence:
        check(sha(HERE/row['file'])==row['sha256'],'evidence source unchanged')
        fp=HERE/row['file'];key=row['key']
        if fp.suffix=='.json':
            actual=load(fp)
            # La llave de figura contiene slash en el nombre; estructura files/nombre.
            if key.startswith('files/'):actual=actual['files'][key[6:]]
            else:actual=actual[key]
        else:
            ri,co=key.split(';');actual=readcsv(fp).iloc[int(ri.split('=')[1])][co.split('=')[1]]
        try:same=float(actual)==float(row['value'])
        except (ValueError,TypeError):same=str(actual)==row['value']
        check(same,'evidence key/value '+row['claim'])
    save(OUT/'CONTROL_TEXTO.json',dict(aprobado=True,status='texto de cierre incompleto; sin síntesis v6 dependiente',text_sha=sha(HERE/'TEXTO_OBJETIVO3_TESIS.md'),evidence_sha=sha(HERE/'EVIDENCIAS_TEXTO.csv'),claims=len(evidence),method='interpolación desde salidas de celdas2/3/4/5; cada cifra ligada por llave/SHA; antecedentes cotejados antes de citar',new_v6_performance_numbers=0))
    technical=f'''# Informe técnico v6 — INCOMPLETO

Alcance autorizado: fases1→2→3; salida incompleta exigida por control indispensable. No aceptación completa ni eficacia v6. Código operativo/freeze/artefactos del piloto se preservan sin corregir retrospectivamente. No reinicio/otro experimento/fits de auditoría/modelos cargados/instalaciones/red/commit/push/objetivo4.

Falla: runner.py/run crea unique[(año,ID)] antes de ventanas externas y reutiliza ajustes para emitir originales. Contrato exige192componentes internos=32×6contextos por ventana; durable96=32×3años únicos. La prueba linaje/copia no probó que cada ventana tuviera ajuste propio. Fase1/ACEPTACION.json pasó los controles ejecutados; fase2/ACEPTACION.json la deja supersedida por falla, conservando freeze y documentos originales. No cambiar definición de ventana ni cerrar192 con96.

Registro durable antes pendiente: {a['consolidated_fits_durable']}fits/{a['constant_estimates_durable']}constantes; último snapshot{a['last_measured_snapshot_seconds']}s. No equiparar estos conteos con total iniciado por pendiente. Interrupción sesión44244 salida130; PID namespace aislado impidió señal desde otra invocación. Último proceso no tiene wait/poll individual consolidado; terminación indispensable incompleta. Ledger anterior íntegro preservado; saldo conservador7200consumido, estado cerrado_incompleto/pending_unmeasured=True. Snapshots previos no modificados, sin reabrir.

Auditor independiente de{a['available_consolidated_jobs']}trabajos consolidados, {a['verified_available_contexts']}contextos verificados y errores{len(a['available_check_errors'])}; sin imports motor/selector/runner, deserialización o fit. Reconstrucción por fuentes/bytes/metadatos; scale aritmético atol1e-12/rtol0, coef/árbol/componentes/reconstrucción exacta. Pruebas inventadas del auditor sinfit:CSV0intfloat equivalente,1e-11rechazado, selector inclusivo, matrices/coef/scaler/fechas y mutación rechazada. No auditoría completa de selección/cobertura/linaje/repeticiones/CSV final inexistente; pendientes activos, no cerrar con guardados parciales.

Notebook02 ejecuta únicamente entorno/conservación, audit_incomplete, antecedentes, tablas de controles, figura diagnóstica, texto/evidencias. Antecedentesv2/v3/memoria/v5/recencia recalculados exactos; sin métricasv6. Todas cifras nuevas de texto salen de funciones invocadas en celdas realmente ejecutadas; no outputs manuales. No datos personales; agregados territoriales únicamente. Python3.12.14/sklearn1.9.1/54lock exactos/pipcheck/PYTHONDONTWRITEBYTECODE1/semilla20261010. Panel231niveles/198cambios, códigoszfill2 histórico, fuentes contractualesSHA intactas.

Fuente local no autenticada/disponibilidad temporal no acreditada. Último año local{av['last_usable_year']}, siguiente{av['next_year_conditional']}condicional, cero proyecciones. Guainía/IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años/2021–2025vistos permanecen advertencias. Los recálculos históricos no confirman científicamente v6. Pendientes técnicos de piloto no se subsanan con otra ejecución en esta sesión; no avance automático.

Orden: verificador documental lectura→preflightmappings→implementación/tests/notebook01→freeze→pilotoúnico→interrupción/cierre conservador→cierre fase2incompleto→notebook02auditor independiente/antecedentes/controles/figura/texto→QAvisual→cierre/manifiesto/verificaciónlectura. Fuentes Python editables; generador nbformat con exec secuencial explícito y capturas reales. resultados.py contiene análisis completo preparado NO ejecutado; fuente notebook planificado NO ejecutado preservada en fase3/antecedentes, no usar para inferir resultados.
'''
    save(HERE/'INFORME_TECNICO.md',technical)
    print({'text':str(HERE/'TEXTO_OBJETIVO3_TESIS.md'),'evidence_claims':len(evidence),'status':'incompleto; sin métricas/meta v6'});return len(evidence)
