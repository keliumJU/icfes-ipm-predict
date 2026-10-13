"""Texto académico claro con cifras ligadas al recálculo desde notebook."""
from pathlib import Path
import json
import pandas as pd
HERE=Path(__file__).resolve().parents[1]
def build():
    t=pd.read_csv(HERE/'objetivo3/tablas/metricas_comparables.csv')
    q=t[t.anio=='conjunto'].set_index('modelo')
    f=lambda v:f'{v:.3f}'.replace('.',',')
    imp=100*(q.loc['persistencia','MAE']-q.loc['seleccion','MAE'])/q.loc['persistencia','MAE']
    annual=[]
    for y in range(2021,2026):
        z=t[t.anio.astype(str)==str(y)].set_index('modelo')
        annual.append(f"| {y} | {f(z.loc['pobreza','MAE'])} | {f(z.loc['persistencia','MAE'])} | {f(z.loc['seleccion','MAE'])} |")
    text=f'''# Diseño y evaluación del modelo predictivo departamental

## Propósito del modelo y relación con la investigación

El tercer objetivo examina qué tan bien puede estimarse el desempeño académico promedio de un departamento a partir de la pobreza multidimensional. Esta pregunta complementa la descripción de los territorios: observar que dos características se relacionan no asegura que una permita predecir la otra con suficiente precisión. Por ello se compararon las estimaciones del modelo con los puntajes efectivamente observados y con referencias sencillas. El resultado se expresa en puntos del puntaje global de Saber 11, lo que permite reconocer tanto los aciertos como las limitaciones del procedimiento.

El análisis predictivo se extendió hasta 2025 y reunió 231 observaciones de 33 territorios en 2018, 2019 y 2021–2025. Se mantuvo la media del puntaje global recibido, calculada entre los registros elegibles de grado once y asignada al departamento del colegio. Se conservaron los filtros auditados y no se añadió una restricción de calendario. Cada territorio-año recibió el mismo peso. Por tanto, los resultados describen la precisión entre promedios departamentales y no el error de un estudiante individual ni un promedio nacional ponderado por matrícula.

El periodo ampliado no cambia el contenido de las 198 observaciones anteriores: sus medias y denominadores coinciden con los del panel auditado. La evaluación principal de la ampliación abarca 165 pares de 2021–2025; 2018 y 2019 proporcionan antecedentes de entrenamiento o historia, según el procedimiento. No se incorporó 2020. En los modelos históricos, el antecedente de 2021 es 2019, sin convertir ese intervalo en un cambio anual ordinario.

## Evolución del diseño y decisiones adoptadas

### La versión base con indicadores de pobreza

El punto de partida estimó el puntaje a partir del IPM, de las quince tasas de privación o de ambas entradas. Las cinco dimensiones sirvieron para organizar los indicadores; no se construyeron sus contribuciones oficiales mediante promedios de tasas. Se compararon una media constante, regresión lineal, Ridge, Random Forest y Gradient Boosting. La regresión lineal ofrece una relación sencilla; Ridge modera coeficientes cuando las entradas están relacionadas; los árboles permiten relaciones más flexibles.

La elección se realizó usando años de desarrollo hasta 2022. El modelo elegido fue Gradient Boosting con IPM y quince tasas. Puede entenderse como una secuencia de árboles pequeños: cada árbol intenta corregir parte del error que dejaron los anteriores. Se fijaron 100 etapas, una tasa de aprendizaje de 0,1, profundidad máxima de dos y un mínimo de tres observaciones por hoja. La profundidad limita las divisiones de cada árbol y la tasa de aprendizaje controla el tamaño de cada corrección. Esos parámetros se eligieron con el procedimiento de desarrollo, no después de conocer los errores de 2023 y 2024.

En esa reevaluación se obtuvo un MAE de 6,346 puntos, con mayor error en 2024 que en 2023. Ese resultado corresponde a un modelo congelado y a 66 pares de esos dos años. Se conserva como evidencia de la versión base y no se compara directamente con una evaluación posterior de 165 pares. Las diferencias de muestra y actualización impedirían atribuir cualquier diferencia de MAE únicamente a una mejora del modelo.

### La ampliación y la referencia de persistencia

La ampliación con pobreza incorporó 2025 y una comparación de familias que incluyó regresión lineal, Ridge, ElasticNet, regresión de soporte vectorial, Gradient Boosting y Extra Trees, además de la media. Se definieron 100 configuraciones antes de evaluar sus resultados. ElasticNet combina formas de penalización; los otros procedimientos exploran relaciones lineales o flexibles. La lista completa y sus parámetros se conservan en el cuaderno reproducible. Ampliar esa lista fue una decisión de comparación, no una garantía de reducir el error.

Para cada año externo, los procedimientos se seleccionaron únicamente con validaciones de años anteriores y se ajustaron con información anterior a ese año. Esta organización permite preguntar cuánto error produce el procedimiento de selección completo, en lugar de escoger retrospectivamente el candidato que acertó más en los datos externos.

La referencia de persistencia hizo más exigente la evaluación: para estimar un año, utiliza el último puntaje conocido del mismo territorio. Si un departamento mantiene una posición relativamente estable, esta regla puede ser difícil de superar. No aprender nuevos parámetros no significa que sea una referencia irrelevante; representa información histórica que un modelo más complejo debería justificar.

### El examen del nivel histórico y de los cambios

La última comparación exploró 39 candidatos basados exclusivamente en historia: persistencia, medias y medianas de cambios, regresiones de mediana con distintas penalizaciones, Ridge, árboles pequeños y procedimientos que separan un cambio común de una corrección territorial. La regresión de mediana estima un cambio central; la penalización limita cuánto puede depender del cambio anterior. Los árboles se restringieron a profundidades de uno o dos y a un mínimo de once observaciones por hoja.

También se comparó usar toda la historia elegible o sus respuestas más recientes. El primer año, 2021, mantuvo persistencia fija porque no había respuestas previas elegibles para ese diseño. Los resultados de esta etapa permiten examinar si aprender cambios mejora la referencia. Como sus entradas no contienen IPM ni privaciones, una mejora no demuestra que el modelo haya aprendido una relación predictiva con pobreza.

## Criterios para seleccionar y evaluar

La medida principal fue el error absoluto medio, MAE. Si una predicción se aparta tres puntos por encima y otra cinco por debajo, sus errores absolutos son tres y cinco; el MAE es su promedio. Esta medida mantiene una interpretación directa en puntos de Saber 11. El RMSE complementa la lectura porque da mayor peso a errores grandes. El sesgo muestra si el procedimiento tiende a sobreestimar o subestimar: un valor negativo corresponde a puntajes previstos menores que los observados.

La regla de selección admitió candidatos hasta 0,1 puntos por encima del menor MAE interno. Dentro de ese grupo aplicó la misma banda al RMSE y después prefirió menos entradas predictoras y un orden previamente definido. La banda evitó decidir por diferencias muy pequeñas; no representa un umbral demostrado de importancia educativa. En la última comparación, la persistencia tenía prioridad en el desempate y las estadísticas constantes contaban como procedimientos sin entradas predictoras, aunque sí aprendían de respuestas históricas.

Los cambios de escala se calcularon dentro de cada entrenamiento. El año evaluado no se incorporó a su ajuste ni a su selección. Sin embargo, esos años ya habían sido examinados durante la investigación. La evaluación es, por ello, exploratoria: la separación temporal controla el uso directo del año evaluado, pero no transforma una investigación que ya conoce esos años en una prueba inédita.

## Resultados sobre una muestra comparable

La siguiente tabla usa los mismos pares, observados y pesos en los tres procedimientos. Sus cifras se recalcularon desde predicciones previamente guardadas; no se entrenaron nuevos modelos para esta consolidación.

| Procedimiento | MAE | RMSE | Sesgo |
| --- | --- | --- | --- |
| Modelo con pobreza ampliado | {f(q.loc['pobreza','MAE'])} | {f(q.loc['pobreza','RMSE'])} | {f(q.loc['pobreza','sesgo'])} |
| Persistencia | {f(q.loc['persistencia','MAE'])} | {f(q.loc['persistencia','RMSE'])} | {f(q.loc['persistencia','sesgo'])} |
| Selección final basada en historia | {f(q.loc['seleccion','MAE'])} | {f(q.loc['seleccion','RMSE'])} | {f(q.loc['seleccion','sesgo'])} |

Fuente: recálculo de predicciones guardadas sobre 165 pares territorio-año de 2021–2025. Unidades: puntos del puntaje global; igual peso por par. Sesgo: predicho menos observado.

![Comparación del error en la misma muestra](figuras/02_comparacion_misma_muestra.png)

Figura. Error absoluto medio sobre la misma muestra. La selección final utiliza historia del puntaje; su barra no representa un modelo con pobreza. Fuente: predicciones guardadas y recálculo reproducible.

El procedimiento ampliado con pobreza no superó persistencia. Esto es un resultado válido del análisis: los indicadores examinados no produjeron una ventaja frente a esa referencia bajo las reglas evaluadas. No prueba ausencia de relación entre pobreza y educación, ni que cualquier modelo posible obtendría el mismo resultado.

La selección final basada en historia redujo el MAE frente a persistencia en {f(imp)} %. En el experimento original se había establecido una meta exploratoria del 5 %, que no se alcanzó; aquí se conserva ese antecedente y no se adopta como criterio nuevo. Hasta 2024, la selección mantuvo persistencia. En 2025 eligió añadir al puntaje previo la mediana de los cambios históricos elegibles, estimada en 2,834 puntos. La mejora agregada se concentra en ese último año y no es uniforme en el periodo.

| Año | Pobreza ampliada | Persistencia | Selección histórica |
| --- | --- | --- | --- |
{chr(10).join(annual)}

Fuente: mismos 33 territorios por año; MAE en puntos. Las coincidencias entre persistencia y selección histórica hasta 2024 son resultados, no datos faltantes.

![Error por año](figuras/01_error_anual.png)

Figura. Error absoluto medio por año. Se conservan todas las anualidades y los resultados desfavorables. Fuente: recálculo de predicciones guardadas.

## Qué mejoró y qué permanece limitado

La evolución hizo explícita una referencia histórica, separó la selección de la evaluación externa y permitió comprobar las métricas sobre muestras idénticas. Estas son mejoras del diseño y de la trazabilidad. La reducción de error adicional fue pequeña y se obtuvo con historia, no con pobreza. Algunos candidatos individuales presentaron menores errores externos que el procedimiento seleccionado, pero no se adoptaron como ganadores después de observarlos. Hacerlo habría cambiado la regla de elección.

En la última comparación, la penalización elevada produjo coeficientes nulos de rezago en los diez ajustes auditados con historia completa. En esos casos, la regresión estimó un cambio constante. Este hallazgo ayuda a distinguir aprender un nivel histórico de aprender una dependencia activa del cambio anterior. Tampoco se atribuye toda diferencia entre procedimientos a un único parámetro cuando cambian varias características a la vez.

La población examinada corresponde a quienes presentan Saber 11 y cumplen los filtros, mientras que el IPM describe pobreza de hogares. Además, el departamento del colegio no necesariamente coincide con el de residencia. El enlace es agregado y no permite explicar mecanismos individuales. Los pocos años y la dependencia territorial limitan la generalización. La conservación y comprobación de archivos locales no certifican por sí solas su autenticidad oficial ni que las variables estuvieran disponibles antes de una fecha de pronóstico.

El alcance ejecutado tampoco coincide íntegramente con la metodología originalmente escrita: no incluye su línea base de año y composición, las contribuciones oficiales de cinco dimensiones ni la robustez mediante la proporción en niveles 3–4 de Matemáticas. Por ello, estas comparaciones no contrastan íntegramente H3 frente a esa línea base ni demuestran una reducción significativa de error atribuible a pobreza. La ampliación a 2025 exige conciliar el periodo declarado de la investigación con estos resultados.

## Relación con la validación y los escenarios

El objetivo 3 aporta procedimientos documentados para estimar y comparar el desempeño departamental, con sus parámetros, criterios y límites. La evidencia favorece persistencia como referencia exigente y no demuestra utilidad incremental de pobreza en la comparación realizada. Esta conclusión responde al propósito predictivo sin forzar un resultado favorable.

El objetivo 4 debe distinguir la precisión comprobada de las estimaciones bajo escenarios. Un procedimiento que solo usa historia no cambia al modificar IPM y no puede fundamentar escenarios de reducción de pobreza. Para esos escenarios se necesita una especificación que utilice pobreza y entradas plausibles dentro de su soporte. Las diferencias entre predicciones serían condicionales al modelo y no efectos causales de políticas. Esa parte requiere una decisión propia antes de declarar cumplido el objetivo.
'''
    path=HERE/'objetivo3/TEXTO_PARA_TESIS.md';path.write_text(text)
    evidence={'texto':str(path.relative_to(HERE)),'numeros_tablas':'objetivo3/tablas/metricas_comparables.csv','base_y_parametros':'fase6/entrega/informe_objetivo_3_revisado.md §§3–5; fase3/resultados/congelacion.json','historia_y_decisiones':'experimento_final_objetivo3_v6/ejecucion_autorizada/PROTOCOLO_V6.md §§2–5; fase3/DIAGNOSTICO_SELECCION.json; fase3/tablas/decisiones_globales.csv','requisitos_originales':'Tesis Vigente/ACA2.pdf pp.25–26,58–60','ampliacion':'decisión humana 12/10/2026; control exacto de 198 medias y denominadores en analisis.data','mejora_porcentaje':float(imp),'no_fits':True}
    (HERE/'objetivo3/EVIDENCIAS_TEXTO.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    return path
if __name__=='__main__':print(build())
