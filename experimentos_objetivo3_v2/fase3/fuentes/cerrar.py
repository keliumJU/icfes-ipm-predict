"""Informe, conservación y manifiesto de fase3, sin entrenamiento."""
from piloto import *

def close():
 out=F3/'resultados';r=read(out/'verificacion_resultados.json');initial=read(out/'integridad_inicial.json');run=out/'piloto';continuity='experimentos_objetivo3_v2/CONTINUIDAD_V2.md'
 conserved=[]
 for p,h in initial['snapshot_versionados'].items():
  if p==continuity:continue
  assert sha(ROOT/p)==h,p;conserved.append(p)
 # Siete fuentes originales, incluso si no estuvieran versionadas: huellas fase2.
 sources=read(cfg.F2/'resultados/integridad_inicial.json')['fuentes']
 for p,h in sources.items():assert sha(ROOT/p)==h,p
 for p,h in read(cfg.F2/'resultados/manifiesto_cierre.json')['entregables_sha256'].items():
  if p!=continuity:assert sha(ROOT/p)==h,p
 frozen=read(out/'congelacion_operativa.json')
 for p,h in frozen['codigo'].items():assert sha(ROOT/p)==h,p
 assert sha(CONFIG)==frozen['configuraciones_sha256'] and sha(cfg.BASE)==frozen['panel_sha256']
 assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==initial['commit_partida']
 assert subprocess.check_output(['git','branch','--show-current']).decode().strip()==initial['rama']
 changes=subprocess.check_output(['git','diff','--name-only']).decode().splitlines();assert set(changes)<={continuity}
 nb=read(out/'verificacion_notebook.json');assert nb['aprobado'] and nb['notebook_sha256']==sha(F3/'notebooks/01_resultados_piloto.ipynb')
 metrics=pd.read_csv(out/'metricas.csv');winners=pd.read_csv(out/'ganadores.csv');deter=pd.read_csv(out/'deterioros.csv');fail=read(out/'fallos.json')
 def table(frame):
  rows=['| '+' | '.join(frame.columns)+' |','|'+'|'.join(['---']*len(frame.columns))+'|']
  for row in frame.itertuples(index=False,name=None):rows.append('| '+' | '.join(f'{v:.8f}' if isinstance(v,float) else str(v) for v in row)+' |')
  return '\n'.join(rows)
 joint=metrics[metrics.ambito=='conjunto'][['procedimiento','n','mae','rmse','sesgo','r2']]
 yearly=metrics[(metrics.ambito=='anual') & metrics.procedimiento.isin(['procedimiento_v2','referencia_v1'])][['procedimiento','grupo','n','mae','rmse','sesgo','r2']]
 own=deter[deter.procedimiento.eq('procedimiento_v2')];annual=own[own.ambito.eq('anual')];territ=own[own.ambito.eq('territorial')]
 territorial_table=metrics[(metrics.ambito=='territorial') & metrics.procedimiento.isin(['procedimiento_v2','referencia_v1'])][['procedimiento','grupo','n','mae','rmse','sesgo','r2']]
 improvement='No calculable: procedimiento incompleto o denominador no positivo.' if r['mejora_porcentaje'] is None else f"{r['mejora_porcentaje']:.12f}% (valor sin redondeo adicional en verificacion_resultados.json: {r['mejora_porcentaje']!r}). Umbral futuro ≥5%: {r['umbral_futuro_satisfecho']}."
 text=f'''# Informe del piloto temporal — fase 3 v2

Fecha del cliente: 2026-10-10, America/Bogota. **Procedimiento {'completo' if r['completo'] else 'incompleto'}**.
Partida real `{initial['commit_partida']}` coincide exactamente con cierre conocido fase2;
rama `{initial['rama']}` reutilizada, sin cambios previos ajenos. Solo fase3 autorizada.
PDF efectivamente leídos: ninguno, cero páginas. Los PDFs citados en antecedentes no se releen.

## Resultado principal y condición futura

{improvement}
Cálculo: 100×(MAE v1 reentrenada−MAE procedimiento v2)/MAE v1 reentrenada.
Se usan idénticas 165 llaves externas y ponderación igual por territorio-año; el RMSE
conjunto procede de los errores concatenados, no del promedio de raíces anuales.
El umbral es práctico, no significancia estadística; no se exige mejora en tres años.
Se entrega informe completo con todos los deterioros. **No se entrega notebook personal**:
su revisión/entrega pertenece a fase4 y no está autorizada en esta solicitud.

{table(joint)}

Fuente verificable: resultados/metricas.csv, ámbito conjunto; recálculo independiente
con math.fsum en fuentes/verificar_resultados.py, independent. Los CSV se guardan con
17 cifras significativas, sin redondeo para selección/condición. Tabla solo redondeada
para lectura; valores íntegros en CSV/JSON. No se usan métricas históricas como denominador.
La especificación ambas tiene menor MAE externo que el procedimiento global en esta
ejecución; es comparación descriptiva, no autorización para sustituir retrospectivamente
el procedimiento principal. La condición futura usa exclusivamente procedimiento_v2.

## Ganadores y evaluación anual

{table(winners)}

Fuente: resultados/ganadores.csv y piloto/seleccion_AAAA.json. Cada selección incluye
las 100 métricas internas, huella e instante anteriores a evaluar el externo; la media
es elegible en las tres especificaciones. El resultado principal corresponde al
procedimiento que selecciona por año, sin ganador único escogido retrospectivamente.

{table(yearly)}

Fuente: resultados/metricas.csv, ámbito anual. Se incluyen media, tres OLS, referencia v1
y los procedimientos IPM/tasas/ambas completos en ese mismo archivo. La referencia fija
v1 gradient_boosting_ambas_07 se reentrena por ventana con estructura/defaults congelados
y semilla prospectiva20261010; 20261008 queda solo como antecedente, sin cargar joblib v1.

## Deterioros y resultados territoriales

{table(annual[['grupo','delta_mae','delta_rmse','deteriora_mae']])}

Delta positivo implica mayor error v2 frente a referencia v1. Fuente:
resultados/deterioros.csv, procedimiento_v2. Deteriora MAE en
{int(annual.deteriora_mae.sum())} de cinco años y {int(territ.deteriora_mae.sum())} de33
territorios. Todos los MAE/RMSE/sesgo/R² territoriales, incluidos deterioros, se entregan
en metricas.csv (cinco observaciones por territorio y procedimiento); no se ocultan territorios.
R² territorial usa variación de los cinco observados de ese territorio, sin atribución causal.

{table(territorial_table)}

## Ejecución, presupuesto y fallos

{r['ajustes']} ajustes contabilizados, {r['segundos_consumidos']:.6f} segundos de7200;
saldo {r['saldo']:.6f}. Tiempo observado incluido arranque/comunicación de procesos:
{r['segundos_observados']:.6f}s. Ledger persistente resultados/piloto/ledger.json;
ajustes_resumen.csv y registros por ajuste. Ejecución serial spawn, BLAS/OMP un hilo,
Extra Trees n_jobs1; cada trabajador recibe solo entrenamiento, interrumpible al agotar
saldo. No se reinicia presupuesto al reanudar ni se reutilizan internas entre externos.
La cota descriptiva8 externos/1550 totales de protocolo §7 tiene un error aritmético:
pueden existir9 IDs externos distintos (global, tres especificaciones, media, tres OLS,
v1). Enmienda E3-02 en ENMIENDAS_TECNICAS.md/conteo_enmienda.json corrige solo cota
a≤1555 sin fallos, conservando todos los roles, orden,100 configuraciones y7200s.
No se cambia selección ni se repite entrenamiento; se deduplican solo IDs iguales.

Ajustes fallidos: {r['fallos']}; registros con advertencias o predicciones fuera0–500:
{len(fail['advertencias'])}. Evidencia íntegra en resultados/fallos.json y cada ajuste.json.
Todas las advertencias capturadas se conservan; sin clipping, nuevas semillas/grillas ni
transformaciones. Diez repeticiones al final (cinco ganadores globales y cinco v1), mismo
saldo y tolerancia absoluta1e−10/rtol0: piloto/reproducibilidad.json y recálculo de sus CSV.
No se ajusta modelo final sobre todos los años; no llamadas a modelos de lenguaje al entrenar.

## Trazabilidad y comprobaciones

Única base: fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv,
SHA256 `{sha(cfg.BASE)}`. 231 filas,33 territorios por2018/2019/2021–2025;
198 históricas exactas y prefijo literal. Normalización05/5 y08/8 solo en memoria.
No se usa candidato ni se repite censo raw; 2020 excluido definitivamente, sin auditoría/sensibilidad.
Población/filtros/media global recibida/geografía del colegio/IPM (1), tasas (15), ambas (16), peso igual
se conservan según protocolo2.0.2 §§1–2 y continuidad. No se cambian criterios según resultados.

Manifiesto fase2, congelación,100 parámetros completos, ventanas y lock comprobados
antes del primer ajuste: integridad_inicial.json, entorno.json. Entorno compatible existente
Python3.12.14/sklearn1.9.1, sin preparación adicional, instalación o red. Pruebas sintéticas
y dobles aprobadas antes del piloto: pruebas_sinteticas.json/log, separadas de resultados
reales y presupuesto del panel; incidencias iniciales conservadas. Congelación operativa
previa a ajuste: congelacion_operativa.json. Enmienda de agregado interno por regex
reconoce etiqueta temporal completa, sin modificar código congelado/selección/evaluación:
fuentes/enmienda_reporte.py y registro_problemas F3-05.

Verificación independiente: verificacion_resultados.json, cobertura `{r['cobertura']}`;
{r['predicciones_artefactos_verificadas']} predicciones por artefacto revisadas y
{r['filas_predicciones_internas']} filas internas agregadas. Predicciones externas
con llaves, ID, ajuste, observado, predicción/error y selección_sha256 en
predicciones_externas.csv; internas en predicciones_internas.csv. Modelos v2 completos,
transformaciones ajustadas, entradas, parámetros, semilla, versiones por huella, tiempos,
fallos y huellas en piloto/ajustes/ETIQUETA. Las repeticiones tienen IDs propios.
Anterioridad,33 filas por validación, observados contra panel, parámetros, escaladores y
cobertura idéntica auditados sin acceder a errores externos desde el selector.

Notebook01_resultados_piloto.ipynb generado y validado con nbformat desde fuente Python
editable; tres celdas de código ejecutadas realmente mediante Python exec, sin kernel
Jupyter ni entrenamiento adicional. Modo explícito en metadata/verificacion_notebook.json.
Contiene lectura de artefactos ya verificados; no presenta salidas de ajustes no ejecutados.

## Conservación, advertencias y pendientes

{len(conserved)} archivos versionados previos y siete fuentes originales intactos,
con huellas en conservacion_final.json. Única actualización previa autorizada:
CONTINUIDAD_V2.md. Fases1–2/originales/v1/CONTINUIDAD_OBJETIVO_3.md/.gitignore intactos.
Todas las entregas nuevas están en fase3; sin descargas de datos, simulación, objetivo4,
push ni ejecución de fase4. Manifest incluye entregables nuevos y continuidad v2;
commit local se informa fuera del manifiesto para evitar autorreferencia.

Persisten casos completos/Guainía (238 frente404, diferencia descriptiva21.012106 puntos:
fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local sin autenticación
independiente, comparabilidad IPM (protocolo v1 §8/notas fase1), colegio versus residencia
de hogares/enlace ecológico, dependencia temporal/territorial y pocos años. No se
atribuyen efectos causales ni sesgos cuantificados causalmente. 2025 exploratorio,
no reserva inédita. Antecedentes59/esquema82, causa antigua20212 y regla global desconocida
siguen archivados sin nueva evidencia, según registro_problemas.md.

Pendiente únicamente trabajo posterior autorizado expresamente: revisión de fase4 y
notebook personal condicionado. Estado completo, mejora y presupuesto verificables en
verificacion_resultados.json; no se avanza automáticamente aunque el umbral se satisfaga.
'''
 (F3/'INFORME_PILOTO.md').write_text(text)
 guardar(out/'conservacion_final.json',dict(aprobado=True,commit_partida=initial['commit_partida'],archivos_versionados_intactos=len(conserved),fuentes_originales_intactas=len(sources),excepcion_autorizada=dict(archivo=continuity,antes=initial['snapshot_versionados'][continuity],despues=sha(ROOT/continuity)),fase1_intacta=True,fase2_intacta=True,originales_intactos=True,congelacion_operativa_intacta=True,pdf_leidos=[],push=False))
 files={str(p.relative_to(ROOT)):sha(p) for p in sorted(F3.rglob('*')) if p.is_file() and p.name!='manifiesto_cierre.json' and '__pycache__' not in p.parts};files[continuity]=sha(ROOT/continuity)
 guardar(out/'manifiesto_cierre.json',dict(fase='v2/fase3',fecha_cliente='2026-10-10',commit_partida=initial['commit_partida'],entregables_sha256=files,completo=r['completo'],mejora_porcentaje=r['mejora_porcentaje'],ajustes=r['ajustes'],presupuesto_consumido=r['segundos_consumidos'],pdf_leidos=[],push=False));print(f'Cierre conservado: {len(conserved)} previos y {len(files)} entregables en manifiesto.')
if __name__=='__main__':close()
