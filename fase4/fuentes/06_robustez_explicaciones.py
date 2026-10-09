# %% [markdown]
# Robustez y explicaciones de alcance predictivo

Este cuaderno consume el contraste territorial ejecutado y los resultados temporales cerrados de fase3. Los mantiene separados: cambian la pregunta de transporte y los años evaluados, por lo que sus métricas no deben interpretarse como una prueba de superioridad entre diseños. No se vuelve a entrenar ningún modelo aquí ni se utiliza 2023–2024 para modificar criterios.

La robustez de la comparación se describe con 2.000 remuestreos pareados de 33 territorios completos, semilla 20261008. Cada grupo conserva sus cuatro años de desarrollo o sus dos años de reevaluación, respectivamente. Las réplicas remuestrean errores fijos; no vuelven a ajustar ni seleccionar. Sus percentiles describen dispersión condicional sobre territorios y estos años observados. No incorporan incertidumbre de búsqueda, solapamiento de entrenamientos, encuesta IPM o variación entre años futuros, ni se usan como p-valores o confirmación independiente.

Las explicaciones longitudinales usan exclusivamente desarrollo. Se calculan asociaciones entre medias territoriales, dentro de cada territorio tras restar su media, y tras restar también medias de año. Separan patrones geográficos y variación longitudinal; el doble centrado tampoco identifica causalidad. Todos los indicadores permanecen, sin selección por correlación. Los coeficientes estandarizados provienen de los OLS ya congelados, por una desviación estándar de entrenamiento. No son importancias del Gradient Boosting ni efectos de intervenir sobre tasas.

Se examina la colinealidad mediante correlaciones y SVD de entradas estandarizadas, así como los tamaños Saber frente al error y la influencia de cada grupo de errores. Omitir un grupo de la agregación de errores es un diagnóstico distinto de retirar ese territorio del entrenamiento, ya hecho en el cuaderno05. No se pondera por estudiantes: hacerlo cambiaría el estimando. Los rangos marginales no certifican soporte conjunto ni precisión de predicción.

Las poblaciones Saber e IPM difieren; las notas IPM locales documentan límites de comparabilidad. No disponemos aquí de composición individual validada ni errores estándar de encuesta para cuantificar sus contribuciones. Son límites de medición y posibles hipótesis, no evidencia causal del deterioro de 2024. La selección histórica59 permanece archivada y las simulaciones están fuera de esta fase.
# %%
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'fase4/fuentes'))
import analisis as a
a.robustez()
# %% [markdown]
## Discusión de resultados efectivamente calculados

Las tablas anteriores conservan signos y diferencias desfavorables. Una diferencia MAE negativa favorece al primer modelo únicamente bajo estos datos y procedimiento; un rango de remuestreo que cruza cero evidencia sensibilidad de la comparación territorial condicional, sin resolver el sesgo de selección. No se reescoge ganador.

Las asociaciones entre y dentro de territorios pueden diferir. Esta discrepancia restringe explicaciones que trasladen un patrón geográfico al cambio temporal del mismo territorio o al individuo. Las tasas son marcadores territoriales potenciales, no mecanismos identificados. Los coeficientes OLS pueden cambiar al controlar otros predictores correlacionados; interpretar un signo aislado como un efecto social sería injustificado. El número de condición describe geometría del diseño, sin un umbral de descarte inventado.

El informe fase4/informe.md recoge cifras, ubicaciones, impacto y alternativas verificadas. Todos los remuestreos y las asociaciones se guardan, además de los resúmenes. La condición de avance sigue requiriendo autorización expresa de la fase posterior y decisiones prospectivas de escenarios; aquí no se ha simulado ningún escenario.
# %%
print('Diagnóstico tamaños (correlación descriptiva, sin pesos):')
print(a.readcsv(a.OUT/'diagnostico_tamanos.csv').to_string(index=False))
print('Sensibilidad del MAE al omitir de la evaluación un grupo de errores:')
t=a.readcsv(a.OUT/'influencia_grupos_errores.csv')
print(t.groupby('id').mae.agg(['min','max']).to_string())
print('Coeficientes IPM congelados, por SD de entrenamiento:')
c=a.readcsv(a.OUT/'coeficientes_ols_congelados.csv')
print(c[c.variable=='ipm'].to_string(index=False))

# %% [markdown]
## Resultados concretos de esta ejecución

El bootstrap territorial tasas−ambas dio−0.241788 y percentiles[−0.569529,0.045591]: la diferencia cambia bajo composición territorial remuestreada. IPM entre territorios r=−0.764626, dentro r=+0.116285 y doble centrado r=−0.136136, lo que impide trasladar sin más el patrón geográfico al longitudinal. Número de condición: tasas12.644109, ambas30.647008; coeficientes no identifican aportes causales. Las14.000 réplicas y todas las asociaciones se conservan. El informe documenta impacto, alternativa y decisión, sin atribuir causas al deterioro2024.
