"""Documentación y figuras estáticas desde recálculos guardados, sin ajustes."""
from auditor import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def textfile(name,text):
 p=HERE/name; check(not p.exists(),'no sobrescribir '+name); p.write_text(text)

def main():
 a=load(HERE/'AUDITORIA_INDEPENDIENTE.json'); check(a['aprobado'] and load(HERE/'AUDITORIA_COMPLEMENTARIA.json')['aprobado'],'auditorías')
 (HERE/'graficos').mkdir(exist_ok=True)
 plt.rcParams.update({'font.size':10,'figure.dpi':130})
 year=rows(HERE/'tablas/por_anio.csv'); territory=rows(HERE/'tablas/por_territorio.csv'); coefs=rows(HERE/'tablas/coeficientes_todos_41.csv')
 fig,ax=plt.subplots(figsize=(9,5))
 for c,label in [('persistencia','Persistencia'),('memoria','Memoria'),('comun','Común = común + corrección'),('global','Global primario')]:
  z=[r for r in year if r['policy']==c]; ax.plot([int(r['year']) for r in z],[float(r['MAE_points']) for r in z],marker='o',label=label)
 ax.set(xlabel='Año externo (33 pares por año; 165 en total)',ylabel='MAE (puntos del puntaje global)',xticks=list(range(2021,2026)),title='Errores externos guardados: recálculo exploratorio')
 ax.legend(fontsize=9); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(HERE/'graficos/mae_por_anio.png'); plt.close(fig)
 fig,ax=plt.subplots(figsize=(11,5))
 z=[r for r in territory if r['policy']=='global']; values=[float(r['benefit_MAE_points']) for r in z]
 ax.bar([r['code'] for r in z],values,color=['#187763' if v>0 else '#b95151' for v in values]); ax.axhline(0,color='black',linewidth=.7)
 ax.set(xlabel='Código del territorio del colegio (33 territorios; 5 pares por territorio)',ylabel='MAE persistencia − MAE global (puntos)',title='Beneficio global por territorio: 18 mejoran / 15 empeoran')
 ax.tick_params(axis='x',labelsize=8); fig.tight_layout(); fig.savefig(HERE/'graficos/beneficio_territorial.png'); plt.close(fig)
 fig,axes=plt.subplots(1,2,figsize=(10,4.5))
 z=[r for r in coefs if r['role']=='externa' and r['component']=='memoria']; xs=[int(r['evaluated']) for r in z]
 axes[0].plot(xs,[float(r['coef_lag_standardized']) for r in z],'o-'); axes[0].set(xlabel='Año externo',ylabel='Coeficiente (puntos por unidad de rezago estandarizado)',title='Rezago: coeficiente cero en 4 externos',xticks=xs)
 axes[1].plot(xs,[float(r['intercept_points']) for r in z],'o-'); axes[1].axhline(0,color='grey',linewidth=.6); axes[1].set(xlabel='Año externo',ylabel='Cambio constante aprendido (puntos)',title='Memoria aprende un nivel histórico',xticks=xs)
 fig.suptitle('Memoria: 33, 66, 99 y 132 filas de entrenamiento; 1–4 años'); fig.tight_layout(); fig.savefig(HERE/'graficos/memoria_nivel_y_rezago.png'); plt.close(fig)
 # Tablas de dirección y contrastes adicionales a nivel de pares.
 paired=rows(HERE/'tablas/errores_pareados_825.csv'); out=[]
 for e in range(2021,2026):
  z=[r for r in paired if r['policy']=='persistencia' and int(r['year'])==e]; ds=[float(r['observed_change_points']) for r in z]
  out.append({'year':e,'n':33,'negative_changes':sum(d<0 for d in ds),'zero_changes':sum(d==0 for d in ds),'positive_changes':sum(d>0 for d in ds),'mean_change_points':math.fsum(ds)/33,'median_change_points':median(ds)})
 from analizar import table
 table('direccion_cambios.csv',out)
 contrasts=[]
 for policy,reference in [('memoria','persistencia'),('comun','persistencia'),('comun_correccion','comun')]:
  for r in [r for r in paired if r['policy']==policy]:
   b=next(q for q in paired if q['year']==r['year'] and q['code']==r['code'] and q['policy']==reference)
   contrasts.append({'year':r['year'],'code':r['code'],'policy':policy,'reference':reference,'n_pair':1,'benefit_absolute_error_points':float(b['absolute_error_points'])-float(r['absolute_error_points']),'difference_signed_error_points':float(r['signed_error_points'])-float(b['signed_error_points']),'exploratory':True})
 table('contrastes_pareados_495.csv',contrasts)
 report='''# Fase4 — auditoría independiente, interpretación y cierre

Fecha: 2026-10-11, America/Bogota. **Recálculos actuales de guardados; cero nuevos fits y cero modelos cargados.** El primario global predefinido mejora 1.7979745286559843%, por debajo de la meta fija del 5%. La auditoría técnica pasó; esta aceptación no acredita autenticidad, disponibilidad temporal ni confirmación científica.

## 1. Entrada, alcance y procedimiento

El primer comando fue `cerrar_fase3.py --verificar`, con PYTHONDONTWRITEBYTECODE=1: aprobado, completa, 1018 huellas, 31245 protegidos y sin diferencias. Su salida se transcribe en REGISTRO_FASE4.json. El auditor independiente `auditor.py` cotejó los manifiestos originales de fase1 (28 huellas), fase2 (234) y fase3 (1018); aceptación, congelaciones y notebooks previos. La continuidad histórica de fase2 se verificó íntegra desde etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md contra el manifiesto original. La continuidad actual de fase3 se preservó antes de actualizarla. No se exige al inventario histórico de fase2 incorporar los artefactos posteriores.

Git HEAD75c3a25182af363f47b0d743820f99084e18fed5, asunto «etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora», rama codex/objetivo3-v5-mae, ascendencia y ausencia de trabajo posterior versionado comprobados en PREFLIGHT_FASE4.json. V5etapa1 se cotejó en su commit real109797407d75d2097e5b71f8bcef3fc266bc61d2; temporaletapa1 únicamente por texto preservado y huella en su etapa2/resultados/partida.json. No reset, commits ni push.

ENTORNO_FASE4.json acredita Python3.12.14/sklearn1.9.1/54paquetes exactos lock/pipcheck0/PYTHONDONTWRITEBYTECODE=1/semilla20261010 antes de cálculos. Semilla contractual, sin operaciones aleatorias nuevas. Fuentev2 SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5 SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc intactos. Originales conservados. PRUEBAS_AUDITOR.json y AUDITORIA_COMPLEMENTARIA.json guardan ensayos inventados sin fit, positivos y negativos, separados de guardados reales.

`analizar.py:panel/audit`, sin importar selector, constructores ni runners operativos, reconstruyó los 231 niveles/198 cambios, los campos derivados, d/c/r, X/y/llaves/entradas/unidades/contextos, scaler y puntajes de todos los jobs. Los modelos se inspeccionan por parámetros JSON; no se deserializan. Los coeficientes se aplican al scaler guardado, no se estiman. Scaler contrastado aritméticamente con atol1e-12/rtol0 por diferencias de suma; matrices/CSV/contextos/predicciones exigen igualdad exacta. Repetición ajustada: atol1e-10/rtol0. No son relajaciones del cotejo CSV.

Se conserva población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario/media recibida/geografía colegio, 2020excluido, 2018historial, d sin anualizar, 2021externo fijo, 165pares/igualpeso/meta5%. 2019 solo historial, sin respuesta con lag inexistente. El máximo previo de2021 es2019 y el intervalo2 no divide el cambio. La cronología lógica se verifica, pero no autentica fechas de publicación. Cero años completos implica respaldo declarado sin fit; uno permite ajuste. Común1fila/año; territoriales33filas/año. Cuatro candidatos exactos con Pipelines separados y componentes comunes propios; defaults congelados, sin recencia, código como entrada o efecto individual.

## 2. Integridad de cobertura, selección y ejecución histórica

AUDITORIA_INDEPENDIENTE.json:1320internas originales,16registros,825externas,528únicas,1320linajes y5comprobaciones globales. Cada copia interna tiene idénticos valores/contexto y representante de menor externo. Diez internas acumuladas son copias de cuatro años de validación, no diez años independientes. Global reutiliza únicamente candidato y ventana correspondientes. Externa2021 no ajusta ni puntúa ni selecciona; internas2021 sí se puntúan con respaldos. CSV cotejado exactamente contra salidas JSON y copias control_csv, aceptando int/float0 y rechazando1e-11 en pruebas.

Ledger histórico cerrado:41fits=24internos+16externos+1repetición, sin fallos/retries,58.63946153299912segundos de7200 y cota46 sin fallos. AUDITORIA_COMPLEMENTARIA.json coteja95snapshots (0000–0094), arranque durable pending de31jobs ajustados antes success,61jobs totales incluyendo respaldos, ejecución serial, tiempos monotónicos crecientes, identidad acumulada, procesos terminados con retorno0 y cierre final exactamente igual al ledger. La suma de intentos medidos36.574579537005775s no reemplaza el total: este incluye preparación/comunicación/pausas hasta el cierre. No saldo reutilizado ni reapertura. Los registros locales no son autenticación externa de tiempos.

## 3. Resultado primario y contrastes descriptivos

Todas las métricas usan fsum, igual peso y las mismas165llaves/observados (33territorios×5años); RMSE raíz de la media de errores cuadrados. Denominador MAE de persistencia positivo y finito. Tabla completa: tablas/metricas_165.csv.

| Política | MAE (puntos) | RMSE (puntos) | Sesgo predicho−observado (puntos) | Mejora MAE (%) |
|---|---:|---:|---:|---:|
| Persistencia |3.429267191379531|4.314920647368904|−2.0960105973100562|0|
| **Global primario** |**3.3676098407589707**|4.306243910848592|−1.5242014817652496|**1.7979745286559843**|
| Memoria exploratoria |3.004299017227967|4.212665669505837|−0.965693505233788|12.392390281511053|
| Común |3.436546823383837|4.476778255626107|−1.4260966275450535|−0.21227952206830963|
| Común+corrección |3.436546823383837|4.476778255626107|−1.4260966275450535|−0.21227952206830963|

Los resultados declarados por fase3 se cotejaron: discrepancias numéricas ninguna. La política memoria es diagnóstico; su12.392% no sustituye el global para declarar éxito. V3/persistencia, v5/global y recencia/global coinciden exactamente con la misma referencia165pares en tablas/referencias.csv; son una referencia compartida, no tres evidencias independientes.

## 4. Qué aprendió memoria

En los11ajustes guardados de memoria (6internos+4externos+1repetición), coeficiente del rezago exactamente0. Todas las predicciones reconstruidas son **puntaje previo + intercepto constante**. Tabla verificable: tablas/coeficientes_todos_41.csv, filtrando component=memoria; cada fila identifica archivo JSON/pipelines/memoria. Los interceptos externos2022–2025 son −1.2006135943734648,1.6516505643865287,2.341502912644245 y2.8590455777240322puntos.

El intercepto está en el intervalo de medianas empíricas de las respuestas territoriales históricas apiladas; con n par el óptimo de pérdida absoluta puede ser cualquier punto de ese intervalo, por lo que no se exige la mediana promediada. La referencia documental futura de cambio histórico debe fijar esa convención antes de resultados. Impacto: la mejora exploratoria de memoria acredita aquí beneficio de un nivel histórico constante, **no una relación aprendida entre cambios sucesivos**. Alternativa verificable resuelta en esta fase: reconstruir todas las predicciones con coeficiente/intercepto guardados y cotejar el intervalo de mediana, sin fit. Atribuir el cero exclusivamente a alpha1 requeriría un contraste separado que no se ejecutó.

## 5. Común y corrección

Las165predicciones externas de común y común+corrección son exactamente iguales: tablas/correccion_comun.csv y contrastes_pareados_495.csv. Los10ajustes de corrección (6internos+4externos) tienen coeficiente0 e intercepto0; no añaden movimiento territorial bajo esta configuración. Los20componentes comunes separados (10por candidato) se auditaron sin compartir ajuste; sus coeficientes también0 y sus interceptos pertenecen al intervalo de mediana de cambios comunes anuales. Común resume1–4respuestas anuales, frente a33–132territoriales en memoria. Común puede aportar un nivel histórico de movimientos medianos, pero aquí su MAE agregado es ligeramente peor que persistencia. Igualdad y corrección nula no prueban inutilidad en otras configuraciones ni otros periodos.

## 6. Por qué global difiere de memoria

Tabla completa: tablas/decisiones_internas.csv; cada ventana usa únicamente sus internas, MAE≤mínimo+0.1, luego RMSE≤mínimo del pool+0.1, luego entradas0/1/1/2 y orden.

- 2022: las cuatro internas2021 son respaldos iguales (MAE2.6402236932057406/RMSE3.5097490978755155); todos quedan en ambos pools; persistencia gana por0entradas.
- 2023: persistencia MAE3.8660950033867016; memoria4.395729786151121 supera3.9660950033867016. Solo persistencia entra al pool MAE.
- 2024: memoria MAE3.6163992477074265 frente3.6464872456777355 de persistencia; ambas entran al pool MAE. Memoria RMSE4.718798774674416 supera el límite4.543974419419438; el filtro RMSE conserva solo persistencia.
- 2025: memoria MAE3.2707967025508324 frente3.7249352319645874 de persistencia; solo memoria en ambos pools. Global usa memoria2025 y persistencia2021–2024.

La ventaja externa posterior de memoria no estaba disponible para seleccionar antes de evaluar esos años. Usarla retrospectivamente alteraría el procedimiento primario. Un retraso de la selección acumulada frente a cambios del nivel es una hipótesis compatible con este patrón, no una causa demostrada ni una autorización para cambiar ventanas o criterios.

## 7. Distribución del beneficio y deterioro

Tablas completas por año/territorio: por_anio.csv (25filas), por_territorio.csv (165filas), errores_pareados_825.csv y contrastes_pareados_495.csv. Se guardan errores absolutos/firmados, sesgo, cambios observados/predichos y coincidencia de dirección exacta. direccion_cambios.csv conserva signos y medianas anuales. Gráficos con unidades/n: graficos/mae_por_anio.png, beneficio_territorial.png y memoria_nivel_y_rezago.png.

Global coincide con persistencia en132pares2021–2024; toda su mejora agregada procede de2025. En2025 n33, MAEglobal1.9383082759365036puntos, beneficio MAE0.3082867531028031puntos,18territorios mejoran y15empeoran, sin empates. El beneficio agregado sobre165 es0.0616573506205602puntos; sus posibles diferencias de últimos dígitos al operar MAE o beneficios se deben al orden de aritmética binaria. Por territorio en los cinco años también18mejoran y15empeoran porque solo cambia2025. En2025 predice cambio positivo uniforme: coincide con la dirección en27de33; sesgo global+1.364113221808658puntos (sobrepredicción), aunque el sesgo agregado sigue negativo. Acierto de signo no equivale a mejora de magnitud.

No se presentan165pares como observaciones independientes ni copias internas como réplicas científicas. No p-valores ni intervalos de confirmación; pocos años, dependencia territorial/temporal y selección acumulada limitan generalización. Contrastes memoria/persistencia, común/persistencia y corrección/común son descriptivos y exploratorios.

## 8. Hipótesis futuras, límites y cierre

PROPUESTAS_FUTURAS.md especifica preguntas, contrastes, evidencia necesaria y límites. La evidencia justifica estudiar una referencia simple de cambio histórico y separar su aporte del rezago/regularización; no justifica afirmar dinámica predictiva confirmada, elegir hiperparámetros nuevos ni usar estos años como confirmación. No se implementa ningún experimento futuro.

Procedencia local no autenticada. Guainía238vs404/21.012105832431985puntos es antecedente histórico v2/fase1/resultados/diagnostico_medias_disponibles.csv, filas57y90; media recibida intacta. IPMhogares-alumnos, colegio-residencia, ecología sin inferencia individual, dependencia y pocos años permanecen. Todos2021–2025vistos: exploratorio, sin confirmación independiente ni causalidad. Aceptación técnica no resuelve origen oficial, publicación o disponibilidad temporal.

Pendientes indispensables técnicos: ninguno después del cierre verificado. Pendientes científicos: autenticidad/disponibilidad y confirmación independiente, prueba del aporte del rezago/regularización y de referencia simple; requieren protocolo y autorización separados. Sin nuevos fits, búsquedas, regularización cambiada, rediseño, fuentes/instalaciones, commit/push, modelo final, notebook personal, simulación, objetivo4 ni avance automático.
'''
 textfile('INFORME_FASE4.md',report)
 textfile('PROPUESTAS_FUTURAS.md','''# Propuestas documentales — no implementadas ni autorizadas

2026-10-11. Evidencia de partida: INFORME_FASE4.md §§4–7; tablas/coeficientes_todos_41.csv, decisiones_internas.csv y errores_pareados_825.csv. Todos2021–2025 vistos; estos años solo sustentan hipótesis exploratorias. Ningún parámetro nuevo elegido, modelo implementado o ajuste ejecutado.

| Pregunta | Contraste a predefinir en protocolo separado | Evidencia necesaria | Limitaciones |
|---|---|---|---|
| ¿El nivel histórico explica el beneficio sin rezago? | Persistencia frente a referencia de cambio histórico constante; definir población, historia anterior admisible y convención de mediana cuando n sea par antes de observar resultados. Cotejar documentalmente con el intercepto guardado, distinguiendo identidad retrospectiva de evaluación futura. | Predicciones anticipadas guardadas antes de nuevos observados; mismas llaves/objetivo/unidades/peso y registro temporal auditable. | El nivel cambia con el historial; los interceptos pares no son siempre la mediana promediada. Igualdad en este piloto no implica igualdad futura ni éxito global. |
| ¿El rezago aporta sobre un nivel histórico? | Nivel constante frente al mismo nivel más término de rezago, manteniendo datos y evaluación comparables; fijar de antemano estimador, parámetros y regla de selección, sin escogerlos en este informe. | Ablación separada, auditoría de coeficientes y predicciones, evaluación temporal independiente; distinguir aporte dentro de entrenamiento del aporte predictivo externo. | Coeficiente cero observado no identifica su causa. Pocos años y cambios de nivel pueden ocultar o imitar dinámica. |
| ¿La regularización explica el rezago cero? | Contraste de regularización definido y autorizado antes de la evaluación; separar esta pregunta del contraste de referencia constante. No proponer ahora valores elegidos por desempeño. | Parámetros predeclarados, mismas matrices anteriores, scaler controlado, diagnóstico de objetivo/solución y predicciones independientes. | No basta ver alpha1 junto a coef0 para atribuir causalidad; posible interacción de escala, pérdida, historia y señal. Sin confirmación con2021–2025. |
| ¿La selección acumulada reacciona tarde? | Formalizar la hipótesis de adaptación del nivel y una comparación de procedimientos definida antes de nuevos resultados; conservar el global de este piloto como antecedente y no reescribirlo. | Predicciones y decisiones anticipadas con historia comparable; suficiente número de ventanas nuevas y análisis pareado bajo dependencia. | La memoria externa ya vista no puede usarse para elegir retrospectivamente. Comparar otras ventanas ahora sería otro experimento. |

Condiciones de cualquier futuro trabajo: protocolo y autorización separados; fuentes comparables y fechas de disponibilidad verificables cuando sean autorizadas; mantener las advertencias de procedencia/ecología/dependencia. No promesa de mejora5%, causalidad ni confirmación basada en años ya vistos.
''')
 textfile('REGISTRO_HALLAZGOS.md','''# Hallazgos: evidencia, impacto, alternativa y resolución

| ID/estado | Evidencia verificable | Impacto | Alternativa verificable y resolución actual |
|---|---|---|---|
| H1 actual | AUDITORIA_INDEPENDIENTE.json/global; tablas/metricas_165.csv/global | Meta5% no satisfecha, mejora1.7979745%. | Recalcular primario fijo con fsum y165llaves: resuelto sin sustitución por memoria. |
| H2 actual | tablas/coeficientes_todos_41.csv/component=memoria; JSON referidos en source | Rezago0 en11ajustes; ventaja de nivel histórico, dinámica no demostrada. | Reconstrucción constante e intervalo de mediana: resuelto; causa del cero pendiente de protocolo separado. |
| H3 actual | coeficientes/component=correccion; tablas/correccion_comun.csv | Corrección0/0 y externas idénticas bajo configuración actual. | Cotejo exacto165predicciones y componentes propios: resuelto; no generalización universal. |
| H4 actual | tablas/decisiones_internas.csv/external2022–2025 | Global no puede rescatarse por ventaja externa retrospectiva. | Reconstruir poolsMAE/RMSE y desempate: resuelto. Adaptación tardía solo hipótesis. |
| H5 actual | tablas/por_anio.csv/global2025 y por_territorio.csv/global | Toda mejora2025;18mejoran/15empeoran. | Tablas pareadas completas/firmadas/dirección: resuelto; independencia/confirmación pendientes. |
| H6 actual | AUDITORIA_COMPLEMENTARIA.json; etapa2/resultados/piloto/historia/0000–0094.json | Ledger41fits cerrado íntegro, sin reabrir saldo. | Cotejo estados/monotonía/terminación/bytes y cota46: resuelto. |
| H7 límite activo | INFORME_FASE4.md §§1,8 y antecedentes vigentes | Autenticidad/temporalidad/ecología/pocos años no resueltos por hashes. | Preservar advertencias y exigir evidencia/autorización futura: pendiente científica explícita. |

Incidencias propias archivadas, sin cambios en originales ni criterios: lectura inicial accidental del plan completo pese al límite (no autorización/ejecución adicional); salidas conjuntas truncadas corregidas por rangos y lectura íntegra local registrada. Auditor001 supuso orden fuente/derivado;002 aún omitía normalizaciónzfill2 de código5/05;003 usó etiqueta de respaldo distinta a la guardada(cero_pares). Fuentes y errores preservados en antecedentes/analizar_001–003.py e INCOMPLETO_AUDITORIA_001–003.json; versión final ordena solo en memoria por llaves, normaliza según contrato y exige etiqueta guardada. No discrepancia de datos. Complemento001 esperaba running pero el registro contractual es pending;002 contó94snapshots sin incluir0000; fuentes preservadas en antecedentes/complementar_001–002.py. Resultado final95snapshots aprobado. Archivadas porque controles finales resueltos, no faltantes fabricados ni criterios alterados.

Antecedentes históricos ya archivados (ausencia de entorno diagnóstico, helper temporal, preflight nombres fase3): no reabiertos; procedencia/confirmación siguen activos.
''')
 save('REGISTRO_FASE4.json',{'fecha':'2026-10-11 America/Bogota','autorizacion':'envío humano exclusivo fase4; continua mantiene alcance','primer_control':{'aprobado':True,'completa':True,'huellas':1018,'conservacion':{'aprobado':True,'protegidos':31245,'diferencias':[],'ajenos_nuevos':[],'versionados':29640},'modo':'lectura; sin fits/escrituras'},'fits_nuevos':0,'modelos_cargados':0,'discrepancias_resultados':[],'incidencias_archivadas':['lectura plan completo accidental','salidas truncadas corregidas','auditor001–003','complementar001–002'],'pendientes_cientificos':['autenticidad','disponibilidad temporal','confirmación independiente','aporte del rezago/regularización'],'avance_automatico':False})
 print('Informe, propuestas y 3 gráficos guardados')
if __name__=='__main__': main()
