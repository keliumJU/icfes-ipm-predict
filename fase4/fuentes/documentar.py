"""Documentación de resultados reales; narrativa editable y tablas derivadas."""
import analisis as a
import pandas as pd

def table(t):
    def fmt(v): return f'{v:.6f}' if isinstance(v,float) else str(v)
    return '| '+' | '.join(t.columns)+' |\n| '+' | '.join(['---']*len(t.columns))+' |\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in t.itertuples(index=False,name=None))+'\n'
metrics=a.readcsv(a.OUT/'metricas_agrupadas.csv')
bootstrap=a.readcsv(a.OUT/'bootstrap_resumen.csv')
assoc=a.readcsv(a.OUT/'asociaciones_longitudinales.csv')
territory=a.readcsv(a.OUT/'metricas_territorio.csv')
support=a.readcsv(a.OUT/'soporte_territorial.csv')
influence=a.readcsv(a.OUT/'influencia_grupos_errores.csv')
correlations=a.readcsv(a.OUT/'correlaciones_predictores.csv').set_index('variable')
pairs=[]
cols=a.m.cfg.ESPECIFICACIONES['ambas']
for i,col in enumerate(cols):
    for other in cols[i+1:]:pairs.append({'a':col,'b':other,'r':correlations.loc[col,other]})
pairs=pd.DataFrame(pairs).assign(abs_r=lambda t:abs(t.r)).sort_values('abs_r',ascending=False)
a.csv('pares_correlacion.csv',pairs)
worst=territory.sort_values('mae',ascending=False).groupby('id').head(3)
a.csv('mayores_errores_territoriales.csv',worst)
support_counts=support.groupby(['id','variable']).fuera_rango.sum().reset_index(name='n_fuera_rango')
a.csv('resumen_soporte.csv',support_counts)
ranges=influence.groupby('id').mae.agg(['min','max']).reset_index()
text=f'''# Fase 4 — contraste territorial, robustez y explicaciones

2026-10-09, America/Bogota. Resultados actuales; no reproducción de rankings históricos. Partida `{a.START}`, Git limpio. Alcance exclusivo fase4. Diferencias frente a plan fase4 líneas87–104 documentadas antes de cálculos en decisiones_previas.md; prevalece protocolo v1.0. Se mantienen población198, promedio global recibido, filtros, Bogotá/2021, peso igual y predictores1/15/16. Selección59 archivada. No simulaciones ni push.

## Integridad y ejecución

resultados/preparacion.json verificó antes de ajustar todas las huellas del cierre3 y sus entradas, base SHA256 `{a.m.cfg.BASE_SHA256}`, protocolo y artefactos. Python3.12.14 y todas las dependencias coinciden exactamente con fase3/resultados/preparacion.json y requirements.lock.txt; pip check aprobado. Entorno `/tmp/icfes-fase3-venv`, sklearn1.9.1, semilla20261008, un hilo. Se reutilizan funciones de fase3 sin escribir allí. Los dos notebooks se ejecutaron realmente en kernel aislado; ver verificacion_notebooks.json. El bloqueo inicial del kernel dentro del sandbox y advertencia de caché pip se conservan en incidencias_ejecucion.md; no son fallos de modelos.

## Transporte territorial

Protocolo §7: 33 grupos por cada ganador seleccionado, 128 filas de32 territorios de desarrollo para entrenar y4 filas del excluido para evaluar. Los99 ajustes mantuvieron hiperparámetros, no reseleccionaron y no usaron2023–2024. Los ganadores GBR actuales no llevan transformaciones; el constructor compartido conserva pipelines internos de entrenamiento si corresponde. Particiones.json guarda membresía, años y parámetros. Predicciones_territoriales.csv conserva396 predicciones/error firmado/absoluto/cuadrado; métricas por99 territorio-modelo y12 año-modelo, advertencias/fallos vacíos. No hubo clipping.

{table(metrics)}

Tasas tiene MAE0.241788 menor que ambas en este diagnóstico; **no cambia el ganador global** `gradient_boosting_ambas_07` ni la reevaluación cerrada. Los hiperparámetros fueron seleccionados utilizando esos territorios en desarrollo: existe sesgo de selección y el contraste no es validación independiente. Transporta a un territorio excluido con años coetáneos disponibles; no mide transporte temporal ni anticipación. Comparar sus8.067691 puntos con6.345582 temporales no prueba deterioro por un mecanismo: cambian diseño y años.

Mayores errores territoriales (tabla completa permanece en metricas_territorio.csv):

{table(worst[['id','departamento','mae','rmse','sesgo','r2']])}

Los R² territoriales se apoyan en solo cuatro años y pueden ser muy negativos con poca variación del resultado. No se omiten. La sensibilidad de la agregación al retirar de evaluación un grupo de errores es:

{table(ranges)}

Estos rangos mantienen predicciones fijas; no son otros entrenamientos ni nuevas métricas para seleccionar. El retiro del entrenamiento se implementó en los33 grupos originales.

## Robustez de diferencias

2.000 remuestreos pareados por comparación, grupos completos de33 territorios, semilla20261008. Resultados exactos en bootstrap_resumen.csv y14.000 réplicas en bootstrap_replicas.csv. Cada territorio conserva cuatro años de desarrollo o dos años de reserva. Errores fijos, sin ajuste adicional. Diferencia a−b negativa favorece a bajo este procedimiento.

{table(bootstrap)}

El rango condicional tasas−ambas [−0.569529,0.045591] cruza cero, al igual que IPM−ambas. La ventaja de tasas no es uniforme frente a la composición territorial remuestreada. Los rangos temporales del ganador frente a media/OLS son negativos, pero proceden de resultados cerrados, reserva previamente expuesta y años fijos; no establecen superioridad independiente. Los percentiles no incorporan incertidumbre de selección, ajuste, dependencia entre particiones, precisión IPM o transporte a años futuros. No hay p-valores ni intervalos i.i.d.

## Explicaciones y medición

Asociaciones exclusivamente de desarrollo, sin ponderación, sin ajuste causal ni selección de tasas. Entre territorios usa33 medias; dentro usa132 desviaciones de media territorial; doble centrado resta también la media de año y añade la media global. Base equilibrada33×4. Todas las asociaciones están conservadas:

{table(assoc[['variable','r_entre_territorios','r_dentro_territorio','r_doble_centrado']])}

IPM–puntaje: entre−0.764626, dentro+0.116285, doble centrado−0.136136. La fuerte asociación geográfica no se traslada al cambio dentro del territorio. Es evidencia descriptiva comprobada, no un efecto de pobreza ni una contradicción causal. Rezago escolar también difiere: entre−0.773640, dentro+0.339428, doble−0.001334. Los cambios comunes por año pueden alterar asociaciones, pero el doble centrado no identifica su origen ni controla toda confusión.

Coeficientes OLS congelados, por una desviación estándar del entrenamiento, en coeficientes_ols_congelados.csv. IPM solo−12.028504 y ambas−10.314072. El coeficiente no es aporte causal ni importancia del GBR. Correlaciones/pares y colinealidad.csv muestran número de condición1.000000/IPM,12.644109/tasas y30.647008/ambas, rango completo1/15/16. Mayor condición con ambas es límite de separación de contribuciones, no permiso para eliminar variables. Pares más correlacionados:

{table(pairs[['a','b','r']].head(5))}

Diagnostico_tamanos.csv: tamaños Saber190–79.542 registros por celda de desarrollo; correlación error absoluto/log tamaño−0.213624/ambas,−0.037864/IPM,−0.244992/tasas. Es asociación diagnóstica, no prueba de precisión de encuesta o representatividad. Se conserva peso igual; no se cambia estimando con ponderación.

Soporte_territorial.csv registra **{int(support.fuera_rango.sum())} valores fuera de rango marginal** de entrenamiento entre {len(support)} entradas evaluadas (sumadas sobre especificaciones). Las tasas repetidas entre ambas/tasas no son casos independientes. Resumen_soporte.csv identifica indicador/modelo; rangos marginales no garantizan soporte conjunto, ausencia de extrapolación del resultado ni intervalos de predicción. Se conservan casos y errores.

Las notas de medición de IPM (auditoria/evidencia/notas_ipm.csv, IPM_Departamentos A50–A53 e IPM_Variables_Departamento A864–A868; protocolo §8) advierten comparabilidad. Saber geografía del colegio e IPM hogares residentes son poblaciones distintas. Composición de examinados, precisión de encuesta y cambios de medición son hipótesis posibles, sin insumos aquí para cuantificar su influencia ni explicar causalmente2024. La procedencia local, regla aritmética global desconocida, pocos años y dependencia permanecen. No se releen PDFs ni se alteran evidencias históricas.

## Hallazgos: impacto, alternativa, decisión y comprobación

| Evidencia / problema material | Impacto | Alternativa verificable | Decisión y comprobación |
|---|---|---|---|
| metricas_agrupadas.csv: tasas mejora0.241788 frente a ambas | Desaconseja afirmar ventaja territorial universal del ganador | Comparación pareada con errores completos y bootstrap predefinido | Se ejecutó; rango cruza0; informar sin reselección |
| asociaciones_longitudinales.csv: IPM entre/dentro difieren | Explicación geográfica no justifica mecanismo longitudinal | Centrar por territorio y luego por año | Se ejecutó y verificó; reportar patrones diferenciados sin causalidad |
| pares_correlacion.csv y colinealidad.csv | Aportes aislados no separables de covariación | Correlaciones completas, SVD y OLS congelados | Se ejecutó; conservar especificaciones, no ablar ni atribuir importancia GBR |
| mayores_errores_territoriales.csv y soporte_territorial.csv | Heterogeneidad y límites de transporte | Conservar extremos; inspección por grupos/rangos | Se ejecutó; ninguna exclusión ni clipping; no causas territoriales inventadas |
| Sin precisiones IPM/composición individual validada; protocolo §8 | No se puede cuantificar incertidumbre de medición ni causa2024 | Diagnóstico de tamaños y notas locales, distinguir hipótesis | Comprobado alcance; límite visible, no control de fuga pendiente ni imputación |
| Selección previa y entrenamientos solapados | Remuestreo no es confirmación independiente | Dispersión condicional de errores fijos, sin p-valores | 14.000 réplicas verificadas; limita interpretación y no cambia ganador |

## Verificaciones y condición de avance

Verificacion.json: cobertura396 sin duplicados,33×4 por especificación,99 particiones completas, errores y métricas recalculados independientemente,14.000 réplicas reproducidas, asociaciones cotejadas, seis ajustes focales adicionales en dos controles (primer código fijo) reprodujeron12 predicciones por control con tolerancia1e−12, sin búsqueda. Notebooks validados nbformat y sin errores de celdas.192 archivos previos se conservan contra snapshot inicial, salvo continuidad intencional. Manifiesto_cierre.json fija huellas de entrega. No se ejecutó una segunda reproducción completa en copia; hay reproducción parcial y verificación concretas descritas.

No quedan controles indispensables activos de fase4. Sensibilidades de año, exclusión2021, ponderación/ablaciones del plan no se ejecutan porque cambian decisiones congeladas; no son resultados ausentes ocultados ni fallos. Límites históricos archivados siguen intactos. Avance solo con autorización nueva y definición prospectiva de escenarios, conservando objetivo/modelos/población y sin interpretación causal. Adopción editorial de tesis permanece externa.
'''
(a.ROOT/'fase4/informe.md').write_text(text)
# Añadir discusión específica después de resultados reales, preservando código al regenerar.
for stage,discussion in [
('05_contraste_territorial','El cálculo completó99 ajustes y396 predicciones sin fallos/advertencias. MAE: IPM9.316132, tasas7.825903, ambas8.067691. Tasas mejora0.241788 frente a ambas en transporte territorial; este hallazgo restringe la ventaja universal del ganador global y no lo sustituye. El diagnóstico tiene sesgo de selección y no es validación independiente. Los rangos y errores desfavorables permanecen en tablas completas.'),
('06_robustez_explicaciones','El bootstrap territorial tasas−ambas dio−0.241788 y percentiles[−0.569529,0.045591]: la diferencia cambia bajo composición territorial remuestreada. IPM entre territorios r=−0.764626, dentro r=+0.116285 y doble centrado r=−0.136136, lo que impide trasladar sin más el patrón geográfico al longitudinal. Número de condición: tasas12.644109, ambas30.647008; coeficientes no identifican aportes causales. Las14.000 réplicas y todas las asociaciones se conservan. El informe documenta impacto, alternativa y decisión, sin atribuir causas al deterioro2024.')]:
    path=a.ROOT/'fase4/fuentes'/f'{stage}.py'
    original=path.read_text().split('# %% [markdown]\n## Resultados concretos de esta ejecución')[0]
    path.write_text(original+'\n# %% [markdown]\n## Resultados concretos de esta ejecución\n\n'+discussion+'\n')
print('Informe y discusión específica escritos desde resultados reales.')
