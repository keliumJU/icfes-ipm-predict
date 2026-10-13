"""E: evidencia, hipótesis y alternativas; documentación sin entrenamiento nuevo."""
from comun_diagnostico import *
import shutil


def archive_incomplete():
    manifest_path = OUT / 'manifiesto_incompleto.json'
    manifest = read_json(manifest_path)
    archive = destination(OUT / 'antecedentes_entorno_ausente/index.json').parent
    assert not (archive / 'index.json').exists()
    copies = {}
    names = [*manifest['artefactos_sha256'], str(manifest_path.relative_to(ROOT)),
             str((OUT / 'verificacion_manifiesto.json').relative_to(ROOT))]
    for name in names:
        source = ROOT / name
        if name in manifest['artefactos_sha256']:
            assert sha(source) == manifest['artefactos_sha256'][name]
        target = destination(archive / name)
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copies[name] = dict(copia=str(target.relative_to(ROOT)), sha256=sha(target))
    write_json(archive / 'index.json', dict(motivo='Entorno ausente resuelto con autorización expresa del usuario; conservar cierre incompleto y continuidad íntegros',
                                           archivos=copies, n=len(copies), evidencia='Sin alterar antecedentes históricos v1–v5'))


def doc(name, body):
    destination(F1 / name).write_text(body)


def main():
    environment()
    assert read_json(OUT / 'auditoria_diagnostico.json')['aprobado']
    assert read_json(OUT / 'pruebas_inventadas/pruebas.json')['aprobado']
    archive_incomplete()
    annual = csv(TABLES / 'estabilidad_anual.csv')
    unique = csv(TABLES / 'metricas_internas_unicas.csv')
    ext = csv(TABLES / 'metricas_externas.csv')
    association = csv(TABLES / 'asociaciones_objetivo.csv')
    variation = csv(TABLES / 'variacion_entradas.csv')
    target_rows = unique[(unique.periodo == 'total') & (unique.id != 'persistencia')]
    persist = unique[(unique.periodo == 'total') & (unique.id == 'persistencia')].iloc[0]
    glob = ext[(ext.procedimiento == 'global') & (ext.periodo == 'total')].iloc[0]
    per_year = unique[(unique.periodo.str.startswith('anio_')) & (unique.id != 'persistencia')]
    counts = per_year.groupby('periodo').delta_mae_pareado.apply(lambda a: int((a < 0).sum()))
    cov_summary = pd.DataFrame([dict(periodo=y, n_configuraciones=35, n_por_configuracion=33, superiores_persistencia=int(counts[y])) for y in counts.index])
    write_csv('conteos_ventaja_interna_por_anio.csv', cov_summary)
    hypotheses = [
        dict(id='H1', hipotesis='La distribución del cambio varía entre años', estado='apoyada descriptivamente',
             ubicacion='estabilidad_anual.csv:periodo=2019/2021/2022/2023/2024/2025; contrastes_particiones_originales.csv:variable=cambio_observado',
             n='198 cambios;33por año;6años;4validaciones únicas',
             favor='2019:33negativos;2021:23negativos;2022–2024:31positivos/año;2025:27positivos;train2019/2021 mediana=-4.0945 vs valid2022=4.5786',
             contra='6años y dependencia;2021 intervalo2;variación no acredita ruptura estructural ni causa del error',
             impacto='Una señal aprendida con distribución anterior puede no describir posteriores; eficacia de recencia no probada',
             alternativa='Estudiar recencia frente historia acumulada con protocolo separado y control de mayor historia',
             resolucion='Desplazamientos y trayectorias completos conservados;sin eliminar años/anualizar',
             pendiente='Prueba futura discriminante con evaluación temporal independiente;sin fijar grilla'),
        dict(id='H2', hipotesis='Las asociaciones anuales observadas conservan signo uniforme', estado='contradicha',
             ubicacion='asociaciones_objetivo.csv:entrada=cambio_ipm/ipm/puntaje_previo,metodo=spearman,periodo=año',
             n='18entradas×6años×33territorios;asociaciones no independientes',
             favor='Algunos años comparten signos y magnitudes cercanas',
             contra='cambio_ipm:rho2019=-0.0254,2023=-0.3326,2025=0.3891;ipm:2021=-0.1295,2023=0.3782',
             impacto='No resumir asociación agregada como relación estable o utilidad predictiva',
             alternativa='Separar niveles/cambios/asociación anual y exigir futuro aporte fuera de muestra',
             resolucion='Pearson/Spearman globales y anuales completos;sin p-valores ni selección de variables',
             pendiente='Estabilidad de relación subyacente/capacidadpredictiva insuficientemente evaluadas'),
        dict(id='H3', hipotesis='Entradas constantes o duplicadas exactamente explican los errores', estado='contradicha',
             ubicacion='variacion_entradas.csv:constante_exacta;redundancia_exacta.csv:iguales_exactamente',
             n='126resúmenes=18×7periodos;1071pares=153×7periodos',
             favor='Cuantiles/rangos difieren por entrada y año', contra='0constantes exactas;0pares idénticos;mínimo23valoresúnicos anuales',
             impacto='No justificar descartar covariables por falta total de variación',
             alternativa='Mantener entradas y valorar simplificación por aporte incremental en futuro protocolo',
             resolucion='Todas entradas completas/no finitos0;sin filtrar variables', pendiente='Variación no demuestra capacidad predictiva'),
        dict(id='H4', hipotesis='La redundancia parcial causa el fracaso de la grilla', estado='insuficientemente evaluada',
             ubicacion='asociaciones_entre_entradas.csv:periodo=global,metodo=spearman,entrada_x=puntaje_previo,entrada_y=ipm;metricas_internas_unicas.csv:periodo=total',
             n='198pares para asociación;132pares por candidato;35configuraciones',
             favor='rho(puntaje_previo,ipm)=-0.7650 agregado;otras asociaciones parciales',
             contra='Sin duplicados exactos;grupos simples también empeoran;correlación no prueba contribución al error',
             impacto='Simplificar podría estudiarse;no es explicación causal ni selección automática',
             alternativa='Comparación futura de aporte incremental de grupos con evaluación temporal separada',
             resolucion='Pares globales/anuales completos y resultados de todos grupos disponibles', pendiente='Prueba incremental requiere autorización;sin escoger variables ahora'),
        dict(id='H5', hipotesis='Los cambios predichos históricos presentan errores de dirección y sesgo', estado='apoyada descriptivamente',
             ubicacion='metricas_internas_unicas.csv:periodo=total,id!=persistencia;errores_internas_unicas.csv',
             n='35configuraciones×132pares;4años únicos;dependencia entre candidatos',
             favor=f"Direcciónacertada {target_rows.direccion_acertada.min():.6f}–{target_rows.direccion_acertada.max():.6f};sesgo {target_rows.sesgo.min():.6f}–{target_rows.sesgo.max():.6f};todasdeltaMAE>0",
             contra='33configuraciones mejoran MAE en2024;dirección/magnitud no sustituyen MAE;0de persistencia es definición de signo exacto',
             impacto='Errores descriptivos ayudan a formular pruebas;no identifican causa única ni inutilidad intrínseca',
             alternativa='Examinar estabilidad de error por año y conservar persistencia como referencia',
             resolucion='Errores/deltas/dirección/magnitud completos y versiones únicas/originales', pendiente='Causa y efecto de recencia no identificados'),
        dict(id='H6', hipotesis='Recencia o mayor historia mejoraría las predicciones', estado='insuficientemente evaluada',
             ubicacion='contrastes_particiones_originales.csv;conteos_ventaja_interna_por_anio.csv;linaje_copias.csv',
             n='10particiones repetidas;4validaciones únicas;33territorios',
             favor='Desplazamientos de mediana;ventaja ajustados concentrada en2024;solo pocos años de historia',
             contra='Sin entrenamiento alternativo ni años inéditos;33ventajas en1año no demuestra mejora de procedimiento completo',
             impacto='Motiva comparar memoria temporal y escasez de historia, sin prometer5%',
             alternativa='Nuevo protocolo prospectivo que discrimine historia/recencia, conservando referencia y evaluación acordadas',
             resolucion='No se fija grilla/hiperparámetros ni inicia experimento', pendiente='Autorización/materialización de protocolo separado y evidencia temporal nueva'),
        dict(id='H7', hipotesis='Conservar persistencia como referencia está respaldado por resultados guardados', estado='apoyada descriptivamente',
             ubicacion='metricas_internas_unicas.csv:periodo=total;metricas_externas.csv:procedimiento=global,periodo=total;v5selecciones',
             n='132internos únicos por candidato;165externos por procedimiento;7procedimientos',
             favor=f"MAEinternopersistencia={persist.mae:.15g};todos35ajustadosmayores;MAEexterno={glob.mae:.15g};sieteprocedimientosidénticos",
             contra='Persistencia mantiene error/sesgo;dirección0 exacta;no prueba optimalidad universal ni inutilidad de entradas',
             impacto='No hay justificación para sustituirla con un nuevo ganador retrospectivo',
             alternativa='Mantener comparador mientras se estudian hipótesis temporales con protocolo independiente',
             resolucion='Selecciones v5intactas;externasfaltantes35no fabricadas', pendiente='Ningún punto de partida mejor demostrado'),
    ]
    write_csv('matriz_hipotesis.csv', pd.DataFrame(hypotheses))
    alternatives = [
        dict(alternativa='Recencia', fundamento='H1/H5/H6;distribuciones y errores cambian entre años',
             conclusion='Justificada como hipótesis para estudiar;NO eficacia demostrada ni nuevo punto de partida validado',
             incertidumbre='Solo4validaciones únicas,2021intervalo2,dependencia,2024no confirma por sí solo',
             prueba_futura='Contrastar esquema temporal acumulado con alternativa de memoria, antes de resultados, en validación temporal separada;conservar persistencia',
             autorizacion='Protocolo y autorización separados;sin fijar grilla/hiperparámetros'),
        dict(alternativa='Simplificación', fundamento='H3/H4;variación presente,dependencia parcial de niveles,grupos simples ya evaluados',
             conclusion='No justificada como remedio suficiente;puede estudiarse aporte incremental sin seleccionar variables por correlación',
             incertidumbre='Asociación no equivale a redundancia predictiva/causa',
             prueba_futura='Comparación prospectiva de aporte de grupos bajo mismo esquema temporal y referencia',
             autorizacion='Nueva decisión de entradas exige protocolo y autorización separados'),
        dict(alternativa='Más historia', fundamento='H1/H6;6cambios anuales disponibles y4validaciones únicas',
             conclusion='Justifica reconocer insuficiencia temporal;no demuestra mejora al añadir años',
             incertidumbre='Más años podrían incorporar cambios de medición/distribución',
             prueba_futura='Verificar comparabilidad/disponibilidad temporal de historia adicional y evaluar en años independientes',
             autorizacion='Fuentes/población/historia adicionales exigen autorización separada;no se obtuvieron'),
        dict(alternativa='Conservar persistencia', fundamento='H7;ningúnajustadomejora conjuntointerno;seleccionesexternasidénticas',
             conclusion='Referencia respaldada para estos guardados;ninguna alternativa mejor validada',
             incertidumbre='MAE/sesgo persisten,no óptimo universal',
             prueba_futura='Mantenerla como comparador de cualquier futuro procedimiento definido antes de evaluar',
             autorizacion='Conservar referencia actual no cambia criterios;experimento nuevo requiere autorización'),
    ]
    write_csv('alternativas_y_pruebas_futuras.csv', pd.DataFrame(alternatives))
    write_json(OUT / 'hipotesis_verificadas.json', dict(n_hipotesis=7, n_alternativas=4,
        estados=pd.Series([h['estado'] for h in hypotheses]).value_counts().to_dict(),
        resultado='Ningún punto de partida predictivo mejor demostrado;recencia/más historia como hipótesis, no experimento diseñado',
        nuevo_experimento_iniciado=False))
    summary = '\n'.join(f"|{r.periodo}|{int(r.n)}|{r.media:.6f}|{r.mediana:.6f}|{r.iqr:.6f}|{int(r.n_negativos)}|{int(r.n_ceros)}|{int(r.n_positivos)}|" for r in annual[annual.n == 33].itertuples())
    doc('INFORME_DIAGNOSTICO.md', f"""# Diagnóstico objetivo3 v1 — resultados descriptivos, sin nuevos fits

Fecha cliente2026-10-11,America/Bogota. A–E ejecutados exclusivamente sobre guardados.
La distribución del cambio y las asociaciones anuales observadas varían. Estos
resultados justifican estudiar estabilidad temporal y escasez de historia; no
identifican una causa definitiva del fracaso ni demuestran eficacia de recencia.
Ningún nuevo punto de partida predictivo mejor queda validado. Persistencia sigue
siendo referencia respaldada por estos guardados; v5metaNOsatisfecha permanece intacta.

## Integridad, conservación y entorno

Fuenteúnicav2 SHA{SOURCE_SHA};derivadov5 SHA{PANEL_SHA}. Reconstrucción actual enmemoria
exacta en todos campos/llaves/orden/valores:231filas/33territorios/198cambios.
Evidencia resultados/preflight_actual.json; procedimiento comun_diagnostico.load_panel.
Fuente/derivado no reescritos.298? No: inventario protegido exacto de29640versionados,
comprobado antes de análisis y de nuevo al cierre (conservacion/manifiesto final).

El entorno temporal ausente se restauró con autorización expresa del usuario:
Python3.12.14 del runtime local;54wheels exactos de caché local,bytes conservados,
sin red. sklearn1.9.1/54paqueteslock/pip check aprobados. Pip es herramienta de
instalación excluida del lock igual que contrato histórico. Evidencia:
resultados/restauracion_entorno/wheels.json,entorno_verificado.json y entorno_diagnostico.json.
Excepción autorizada exclusivamente reconstrucción/instalación del entorno;sin fits.

## Cambios observados y particiones originales

Tabla completa estabilidad_anual.csv, llaves periodo=año. Cuantiles lineales,
desviaciónddof1,IQR,rango ysignos exactos;33territorios cada año,198cambios completos.

|Año|n|Media puntos|Mediana puntos|IQR puntos|Negativos|Ceros|Positivos|
|---|---:|---:|---:|---:|---:|---:|---:|
{summary}

2019 fue negativo en33/33;2021 en23/33;2022–2024 positivos31/33cadaaño;2025positivos27/33.
2021 compara2019:intervalo2,sin anualizar;resto intervalos1. No eliminar2019 ni salto.
Transiciones en transiciones_signo.csv y transiciones_resumen.csv:10/33cambian signo
2019→2021,23/33en2021→2022,4/33en2022→2023,4/33en2023→2024,6/33en2024→2025.
Trayectorias completas33 y resúmenes territoriales conservados. No años/territorios
independientes ni diagnóstico de ruptura causal.

Contrastes_particiones_originales.csv conserva10particiones originales para objetivo
y18entradas,n_train33/66/99/132,n_valid33. Para valid2022,train2019/2021 mediana−4.094537
frentevalid4.578600 (delta8.673137puntos);se repite por diseño en externas2023/2024/2025.
Impacto: historia previa puede describir otra distribución. Alternativa: estudiar
memoria temporal con protocolo separado; resolución actual mantener todos años y
comparaciones completas. No se prueba que recencia reduzca error.

## Variación y asociaciones

Unión exacta18entradas GRUPOSv5 (ordenprimeraaparición);variacion_entradas.csv contiene
126resúmenes,0constantes exactas/no finitos0,mínimo23valoresúnicos entre resúmenes
anuales. Redundancia_exacta.csv:1071pares,0idénticos;asociaciones_objetivo.csv:252registros,
asociaciones_entre_entradas.csv:2142registros. Pearson/Spearman,rangosmedios,globaln198/
anualn33;en estos datos0correlaciones indefinidas. Controles inventados verifican
salida vacía con razón/n ante constante/insuficiencia/no finitos, nunca correlación0.

Spearman cambio_ipm–objetivo agregado−0.063199;2019−0.025407,2023−0.332553,2025+0.389102.
IPM–objetivo2019−0.034094,2023+0.378238. Spearman agregado previo–IPM−0.765016
(tabla entreentradas,periodo=global). Variación de signo observado no demuestra
inestabilidad de una relación subyacente;agregación mezcla tiempo y territorio.
Impacto: no concluir capacidad predictiva/inutilidad intrínseca por correlación.
Alternativa: comparar aporte incremental prospectivo; resolución tablas completas,
sin p-valores,importancias,selecciónautomática ni umbrales para futurasgrillas.

## Errores guardados y ausencia de pseudo-repetición

Auditoría exacta de360artefactos internos/350metas de ajustes históricos,entradastrain/
test,parámetros completos,semilla/versiones/huellas/llaves/observados/previos/predicciones.
Solo hash de modelos;no carga ni reproducción de sus fits. Copias coinciden exactamente:
11880originales→4752únicas=36×4×33,representante menor externo. Linaje11880filas en
linaje_copias.csv;firmas/meta en auditoria_metadatos_copias.csv. Diezparticiones
acumuladas contienen cuatrovalidaciones únicas2021–2024;no10años independientes.
Análisis por ventana original conserva11880filas,sin deduplicarlo ni cambiar métricas.

144registros guardados cotejados por math.fsum;máximadiferencia2.6645352591003757e−15,
atol1e−12/rtol0soloacumuladores. CSVllaves/valores exactos,sin tolerancia,int/float0válido.
Resultados/cotejo_144_metricas_guardadas.csv (en tablas),auditoria_aritmetica_independiente.csv:
187resúmenes contrastados mediante sumasracionalesFraction sobreerroresIEEEexactos.

Internas únicas,n132porcandidato:MAEpersistencia={persist.mae:.15g};35ajustados
MAEentre{target_rows.mae.min():.15g}y{target_rows.mae.max():.15g};todosdeltaMAE>0.
Por año,n33/configuración:0de35mejoranen2021,2022,2023;33de35en2024.
Evidencia metricas_internas_unicas.csv,conteos_ventaja_interna_por_anio.csv y
minimos_internos_retrospectivos.csv (descripción,NO nuevosganadores).
Sesgosajustados {target_rows.sesgo.min():.6f}a{target_rows.sesgo.max():.6f}puntos;
direcciónacertada{target_rows.direccion_acertada.min():.6f}a{target_rows.direccion_acertada.max():.6f}.
Impacto:errores de dirección/sesgo son descriptivamente observables;alternativa
examinar patrones temporales;resolución errores completos,ninguna causa única.
Magnitudes/errores de cambio/deltasabsolutos/cuadráticos completos en errores_*.csv.
Direcciónexacta distingue−/0/+;persistencia acierta0porqueobservados no son0,
pero conserva menorMAE;acierto direccional no reemplaza métrica global.

Externas1155=7×165,33territorios×5años,todosprocedimientosigualespersistencia:
MAEglobal={glob.mae:.15g},RMSE={glob.rmse:.15g},sesgo={glob.sesgo:.15g},deltaMAE0.
Esto reproduce aritmética actual de resultados históricos, no fits. Errores por
procedimiento/año/territorio/2021–2024/2025 completos;las35configuraciones no seleccionadas
no tienen externas y no se fabrican. Ventaja de algún candidato en2024 no crea
ganador externo ni autoriza alterar selecciones/meta. Error ysesgo de persistencia permanecen.

## Hipótesis, alternativas e incertidumbre

Matriz_hipotesis.csv registra7hipótesis con evidenciafavor/contra,n,ubicación/llave,
impacto,alternativa,resolución/pendiente. H1/H5/H7 apoyadas descriptivamente;
H2signouniforme/H3constantesduplicadascontradichas;H4causaredundancia/H6eficaciarecencia
insuficientemente evaluadas. Alternativas_y_pruebas_futuras.csv desarrolla4alternativas:
recencia,simplificación,máshistoria,conservarpersistencia. Recencia/máshistoria
merecen estudio,ninguna acredita un punto de partida mejor. Simplificación no queda
justificada como remedio suficiente;no todo error procede de muchas variables.

Prueba futura discriminante: protocolo separado antes de resultados que contraste
memoria temporal y disponibilidad de más historia, conserve referencia/evaluación
acordadas y procure años independientes. Para simplificación,comparación de aporte
incremental con tiempo controlado. No fijar grilla/hiperparámetros ni iniciar experimento.
No promesa de5%,selecciónfinal ni efecto causal.2021–2025vistos:exploratorio.

## Advertencias, entregables y pendientes

Conservar Guainía238vs404/21.012106puntos: evidenciahistóricav2/fase1/resultados/
diagnostico_medias_disponibles.csv,no recálculo actual de casos. Procedencia local
no autenticada,IPMhogares frentealumnos,colegiofrenteresidencia/enlaceecológico,
dependenciatemporal-territorial,pocosaños. No pronósticoanticipadodemostrado ni
confirmaciónindependiente. Antecedentes59/esquema82/causa20212/fórmuladesconocida/
E2-01/E3-01/E3-02conservados,no nueva conexión que justifique reabrirlos.
PDFactual0páginas;lecturas históricas no presentadas como actuales.

Pruebas9grupos inventados aprobadas;22tablasA–D+3tablasE/resumen;5PNGdescriptivos
revisados visualmente. Notebook/fuente/generador/verificaciónreal y cierre final
en README/resultados/continuidad. Conservación/manifiesto se sellan después de
notebook/documentación;consultar aceptación_final.json para aceptación definitiva.
Sin pendientes de integridad conocidos;eficaciaalternativas e historia/confirmación
independiente son pendientes científicos,requieren otra autorización.
Sin commit/push/ajustes/simulación/objetivo4/notebookpersonal/entrenamientofinal.
""".replace('298? No: inventario', 'Inventario'))
    doc('registro_hallazgos.md', """# Hallazgos, impacto, alternativas y resolución

Fecha cliente2026-10-11. Resultados actuales separados de resultados históricos.
Registro completo de hipótesis estadísticas: tablas/matriz_hipotesis.csv (7filas)
y alternativas_y_pruebas_futuras.csv (4filas), con archivo/llave/n/procedimiento.

|ID/ubicación|Impacto|Alternativa/resolución|Estado|
|---|---|---|---|
|D-01 entorno ausente;restauracion_entorno/wheels.json y entorno_verificado.json|Bloqueaba controles|Usuario autorizó reconstrucción;runtimePython3.12.14+54wheelscache;bytes intactos,pipcheckexacto,sinred|Resuelto;estado incompleto archivado íntegro|
|D-02 preflight_actual.json/conservacion_final.json;29640protegidos|Partida debe ser real|HEAD/asunto/rama/ascendencia esperados y huellasidénticas;sin reset ni Gitlimpio artificial|Resuelto|
|D-03 primer índice propio;piloto.py:74–97|Baseincorrecta generó falso rechazo|Cotejo corregido con basepiloto/,2174huellas/coberturaexacta;registropreliminarconservado|Antecedente propio sin impactoestadístico;no reabrirv5|
|D-04 ensayos_implementacion/fallo_comparacion_nullable|pd.NA bloqueó igualdadexacta en2018historial|Máscaras exactas yvalorespresentes exactos;pruebasnullable/intfloat0/1e−11;originalesintactos|Resuelto antes de estadísticas|
|D-05 ejecutar_diagnostico.py;error sintaxis inicial|No podía ejecutar|Paréntesis corregido antes de cualquier escritura/estadística;ejecuciónfinalaprobada|Resuelto,sinimpactohistórico|
|D-06 lecturas.json|Salidaconjuntatruncada no acredita lectura completa|Relecturasacotadas/plan1–5/continuidadesvigentes/documentosv5;PDF0|Resuelto;antecedentes no atribuidos como nuevaslecturas|
|H1–H7 matriz_hipotesis.csv|Distribución/asociación/error diferentes no acreditan causalidad|7hipótesis clasificadas confavor/contra/n;conservar todos años/territorios|Resuelto descriptivamente;eficaciaalternativaspendiente|
|D-07 linaje_copias.csv/auditoria_metadatos_copias.csv|11880copias no son evidenciaindependiente|Identidadexactapredicciones+entrenamiento/config/semilla/versiones;4752únicas conrepresentantemenorexterno;análisisoriginalconservado|Resuelto|
|D-08 errores_externas.csv/v5selecciones|35ajustados sinexternas no puedenrescatarse|Conservar7×165procedimientosoriginales,no fabricar ni ajustar externas|Resuelto;ningúnnuevo ganador|

Guainía238vs404/21.012106puntos,procedencialocal,comparabilidadIPM/ecología/dependencia/
pocosaños siguen advertencias activas;ubicación/evidencia en protocolo/informe.
Antecedentes archivados sin nueva conexión siguen archivados;no se inventaron
criterios históricos ni saldos. Confirmaciónindependiente/capacidadpredictivafutura
no resueltas por correlaciones. No hipótesis convertida en causa definitiva.
""")
    doc('PROTOCOLO_DIAGNOSTICO.md', """# Protocolo diagnóstico1.0 — decisiones intactas, solo guardados

Fecha cliente2026-10-11,America/Bogota. Contrato completo PLAN_DIAGNOSTICO.md §§1–5,
SHA4c33307f11ec2da96ea108faf12a1eb44ba52eb805e7fd7ed9ad445eae6e7fe2.
Usuario envió prompt diagnóstico y posteriormente autorizó reconstruir entorno
con instalaciones/descargas necesarias;excepción solo entorno,sin nuevosfits.
Se usó runtimePython3.12.14 ycache54wheelslocal,sin red. Entorno/pipcheckexactos.

Decisionesdelusuario:intactas poblaciónESTUDIANTE/no libertadS/grado11/seispuntajes
positivospresentes/sincalendario;mediarecibida/geografíacolegio/pesoigualterritorio-año;
2020excluido/2018historial/2021previo2019/sinanualizar/objetivooriginal.
Fuenteúnicav2/derivadov5/GRUPOS exactos en plan§2;18entradas unión primeraaparición.
Año/código/intervalo no son entradas. Selecciones/meta/criterios/ledgersv5 no cambian.

Procedimientos íntegros plan§3: distribución198global/anual/territorial/particiones,
cuantileslineales/ddof1/signoexacto−/0/+;variación/no finitos/constantes exactas,
Pearson/Spearmanrangosmediosglobaln198/anualn33/sinp-valores/importancias;
errorpred−obs/MAEfsum/RMSEsqrtfsum/sesgo/deltapareadoconpersistencia/dirección/
magnitud;144guardadosatol1e−12rtol0soloacumuladores,CSVvaloresllavesexactosintfloat0;
linaje11880copias/4752únicas comprobadasexactamente,menorexternorepresentante;
matriz7hipótesis3estados y4alternativas sin nueva grilla/ganador/experimento.
Estadísticasentreconfiguraciones retrospectivas,no observacionesindependientes.

Decisiones nuevas de implementación: módulos propios stdlib/numpy/pandas/matplotlib
sin importar módulos experimentales;reconstrucción exacta enmemoria;guardiasfase1/
symlinks;controles9grupos;auditoríaracionalFraction187grupos;5PNGestándar;notebook
sololector desde fuentePython/generador/nbformat/exec real,no kernel ni ajuste.
Todo determinista,semilla20261010reservada,sin aleatoriedad aplicada.
Nombre/función de todas tablas y orden de ejecución en README y manifiesto.
No datos personales,fuentesextra,raw ni modelos deserializados.

Originales/v1–v5/continuidadesajenas/protocolos/atributos/.gitignore/ledgers intactos
por29640huellas. Escriturasartefactos solo diagnósticofase1/continuidadpropia;
entorno/54wheels en/tmp por nuevaautorización. Cierre incompleto anterior archivado
con23copias exactas y su índice;antecedentecontinuidad íntegro también al final.

2021–2025vistos:exploratorio,sinconfirmaciónindependiente/causalidad/pronóstico
anticipadodemostrado. CasoscompletosGuainía238vs404/21.012106puntos(evidenciahistóricav2/
fase1/resultados/diagnostico_medias_disponibles.csv),procedencialocalnoautenticada,
IPMhogares/alumnos,colegio/residencia/enlaceecológico,pocosaños/dependencia.
Antecedentesarchivados sin nueva conexión no se reabren. Etapa3v5no autorizada;
metaNOsatisfecha intacta;ningúnfit/cargamodelo/commit/push/experimento posterior.
Aceptación definitiva: resultados/aceptacion_final.json/manifiesto_cierre.json.
""")
    table_descriptions = {
        'estabilidad_anual.csv':'Distribuciones global y seis años, n/intervalo/cuantiles/signos',
        'trayectorias_33.csv':'198cambios,33territorios,previos/intervalos',
        'transiciones_signo.csv':'165transiciones territoriales', 'transiciones_resumen.csv':'Conteos exactos de transiciones por años/signos',
        'estabilidad_territorial.csv':'33distribuciones completas', 'contrastes_particiones_originales.csv':'10particiones×19variables (objetivo+18entradas), n explícitos',
        'variacion_entradas.csv':'126resúmenes de variación', 'asociaciones_objetivo.csv':'252Pearson/Spearman con objetivo',
        'asociaciones_entre_entradas.csv':'2142asociaciones entre entradas', 'redundancia_exacta.csv':'1071pares exactos',
        'auditoria_metadatos_copias.csv':'360firmas/entrenamiento/rutasmetadata', 'linaje_copias.csv':'11880copias y representante',
        'cotejo_144_metricas_guardadas.csv':'144registros históricos recalculados sin selección',
        'errores_internas_originales.csv':'11880errores/deltas/dirección/magnitud originales',
        'errores_internas_unicas.csv':'4752errores únicos,4años por candidato', 'errores_externas.csv':'1155externas originales completas',
        'metricas_internas_originales.csv':'Candidato/familia/grupo/ventana/año/territorio, copias conservadas',
        'metricas_internas_unicas.csv':'Candidato/familia/grupo/4años/territorio sin repetir',
        'metricas_externas.csv':'7procedimientos/5años/territorio/cortes132+33',
        'errores_anuales_candidato_familia_grupo.csv':'Resúmenes anuales en tres conjuntos, sin pooling candidatos',
        'minimos_internos_retrospectivos.csv':'Familia/grupo/ventana, mínimos descriptivos;NO nueva selección',
        'auditoria_aritmetica_independiente.csv':'187comparaciones con sumas racionales de erroresIEEE',
        'conteos_ventaja_interna_por_anio.csv':'0/0/0/33configuraciones superiores,35/año',
        'matriz_hipotesis.csv':'7hipótesis:n/evidencia/impacto/alternativas/resolución',
        'alternativas_y_pruebas_futuras.csv':'4alternativas,incertidumbre/prueba/autorización'}
    assert set(table_descriptions) == {p.name for p in TABLES.glob('*.csv')}
    table_list = '\n'.join(f'- `tablas/{n}`: {d}.' for n,d in table_descriptions.items())
    doc('README.md', f"""# Diagnóstico objetivo3 v1 — fase1 descriptiva

Fecha cliente2026-10-11,America/Bogota. Solo guardados,cero nuevosfits/modeloscargados.
Informe/7hipótesis/4alternativas;ningúnnuevo punto de partida mejorvalidado.
Recencia/máshistoria se proponen como hipótesis;persistencia sigue referencia.
Este trabajo no es etapa3v5;metaNOsatisfecha intacta. Estado definitivo en
resultados/aceptacion_final.json;conservación/manifiesto verificables.

Entorno reconstruido con autorización expresa:Python3.12.14 runtime local,
sklearn1.9.1,54paquetesexactoslockv4/pipcheck;wheelscache,sin descarga de red.
PYTHONDONTWRITEBYTECODE=1;semilla20261010reservada,sin aleatoriedad.

Orden realmente realizado, desde raíz con `/tmp/icfes-v2-fase2-venv/bin/python`:

1. Verificación documental inicial stdlib;bloqueoentorno y consulta alusuario.
2. `fuentes/restaurar_entorno.py`,venv con runtimelocal,instalaciónoffline y verificaciónexacta.
3. `fuentes/ejecutar_diagnostico.py`:reconstrucción/cotejo/metas/CSV/linaje,A–D/aritmética/gráficos.
4. `fuentes/pruebas_diagnostico.py`:9gruposinventados sin ajuste;salidasreales.
5. `fuentes/documentar_resultados.py`:archivo estadoincompleto,matrizE/informe/protocolo/README.
6. `fuentes/generar_notebook.py`:notebook desde `01_diagnostico.py`,validaciónnbformat/celdasexec reales.
7. `fuentes/cerrar_diagnostico.py`:aceptación/conservación/manifiesto/continuidadpropia;
   `--verificar`sololectura,no volver a ejecutar análisis ni controles.

No sobrescribir salidas existentes al reejecutar;los scripts analíticos rechazan
destinos ya usados. Notebook solo lee guardados;no crea nuevas métricas ni ajustes.
Los ensayos previos/salidaspreliminares se conservan,pero no acreditan aprobaciónfinal.
Antecedentes_entorno_ausente/index.json conserva23archivos del primer estado incompleto
con rutasoriginales/huellas/copias;su manifiesto se verifica contra esas copias.

Fuentes únicas y decisiones poblacionales:PROTOCOLO_DIAGNOSTICO.md/plan§§1–5.
Documentos:INFORME_DIAGNOSTICO.md,registro_hallazgos.md;resultadospreflightactual,
entorno,pruebas/auditoría/lecturas/notebook/aceptación/conservación/manifiesto.
Notebook: `notebooks/01_diagnostico.ipynb` (solo diagnóstico,no personal).
Cinco PNG en graficos/:distribuciones,trayectorias,contrastes,asociaciones,deltasinternos.

Tablas completas (sin redondeoCSV ni datos personales):

{table_list}

Métricas con puntos y puntos²;correlación sin unidades;IPM/tasas conservan unidades
recibidas porcentuales,cambios en puntosporcentuales.33territorios/198cambios;
11880internasoriginales,4752únicas,144registros,36IDs,1155externas=7×165.
Solo4añosvalidación únicos,dependenciastemporales/territoriales,2021intervalo2sinanualizar.
2021–2025vistos:exploratorio,no confirmación independiente/causalidad/pronóstico
anticipadodemostrado. AdvertenciasGuainía/IPM/local/ecología preservadas.

Pendiente científico:eficaciarecencia/simplificación/máshistoria ycausas no establecidas.
Nuevoexperimento requiere protocolo/autorizaciónseparados;sin grilla nueva niavanceauto.
Sin commit/push/objetivo4/simulación/notebookpersonal/entrenamientofinal.
""")
    print('Matriz7hipótesis,4alternativas,informe/protocolo/README generados;antecedenteincompleto preservado.')


if __name__ == '__main__':
    main()
