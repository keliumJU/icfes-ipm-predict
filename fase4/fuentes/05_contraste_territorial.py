# %% [markdown]
# Contraste territorial de los ganadores congelados

Este cuaderno responde a una pregunta concreta: ¿qué error producen los tres ganadores de especificación cuando un territorio completo queda fuera del ajuste? La unidad es la media global de registros elegibles de grado 11 por departamento del colegio y año. Se mantienen Bogotá, 2021, los filtros auditados y el peso igual de cada territorio-año. Los datos son agregados; no se incluyen identificadores personales ni se releen microdatos.

El protocolo v1.0 §7 fijó este contraste antes de entrenar. Cada uno de los 33 territorios aporta sus cuatro filas de 2018, 2019, 2021 y 2022 a la evaluación. El entrenamiento contiene las 128 filas de los otros 32 territorios. Las tres especificaciones siguen siendo IPM, 15 tasas y ambas. Cada partición reconstruye el estimador con los parámetros seleccionados en fase3; cualquier transformación debe aprenderse solo del entrenamiento. Los ganadores actuales son Gradient Boosting y no escalan entradas.

Este transporte territorial no es transporte temporal: hay años coetáneos en el entrenamiento. Además, los hiperparámetros se seleccionaron antes utilizando esos territorios en desarrollo. Por tanto, estas predicciones son externas al ajuste de cada partición, pero el diagnóstico tiene sesgo de selección y no es validación independiente. No cambia el ganador global ni su reevaluación temporal cerrada.

Las diferencias entre plan y protocolo están resueltas antes de calcular en fase4/decisiones_previas.md. Las huellas y versiones exactas se comprobaron en fase4/resultados/preparacion.json. Se reutilizan las funciones compartidas, la semilla 20261008 y un hilo de ejecución; sin nueva búsqueda, clipping, exclusiones o simulación. Se conservan todos los errores y las advertencias/fallos, incluidos resultados desfavorables.
# %%
import sys
from pathlib import Path
root=Path.cwd()
sys.path.insert(0,str(root/'fase4/fuentes'))
import analisis as a
a.territorial()
# %% [markdown]
## Cómo leer los resultados ejecutados

La tabla anterior se obtiene de los 99 ajustes realizados por esta celda, no de una búsqueda nueva. MAE y RMSE expresan diferencias entre medias departamentales en puntos Saber; el sesgo positivo indica sobreestimación. La métrica agrupada usa las 132 filas por especificación con igual peso. El R² por territorio se apoya en solo cuatro valores y puede ser muy negativo; no demuestra por sí solo inutilidad general ni permite atribuir causas.

Las predicciones y errores completos están en predicciones_territoriales.csv. Las métricas por territorio y año, las particiones y los rangos de entrenamiento permiten inspeccionar heterogeneidad y soporte sin suprimir casos. El siguiente cuaderno contrasta asociaciones y robustez de estos errores con procedimientos prospectivos; no altera los criterios por el desempeño observado.
# %%
print('Errores anuales reales:')
print(a.readcsv(a.OUT/'metricas_anio.csv').to_string(index=False))
print('Mayores MAE territoriales por especificación (se conserva tabla completa de 99 territorios-modelo):')
t=a.readcsv(a.OUT/'metricas_territorio.csv')
print(t.sort_values('mae',ascending=False).groupby('id').head(3).to_string(index=False))
s=a.readcsv(a.OUT/'soporte_territorial.csv')
print('Valores fuera del rango marginal de entrenamiento:',int(s.fuera_rango.sum()))

# %% [markdown]
## Resultados concretos de esta ejecución

El cálculo completó99 ajustes y396 predicciones sin fallos/advertencias. MAE: IPM9.316132, tasas7.825903, ambas8.067691. Tasas mejora0.241788 frente a ambas en transporte territorial; este hallazgo restringe la ventaja universal del ganador global y no lo sustituye. El diagnóstico tiene sesgo de selección y no es validación independiente. Los rangos y errores desfavorables permanecen en tablas completas.
