# %% [markdown]
# Comparación temporal y congelación de modelos

## Pregunta, datos y justificación

¿Qué configuración conserva menor error absoluto al transportar una relación contemporánea entre pobreza y promedio Saber 11 hacia años posteriores del desarrollo? Usamos exclusivamente 132 celdas de 2018, 2019, 2021 y 2022, con peso uniforme. No se interpreta una relación aprendida como efecto individual o causal de pobreza. La referencia constante mide lo que se logra sin predictores; OLS mide la aportación de una relación lineal sin regularización; Ridge reduce inestabilidad por colinealidad; Random Forest y Gradient Boosting permiten relaciones no lineales bajo una búsqueda pequeña fijada antes de resultados.

Las tres especificaciones tienen IPM solo, tasas solas y ambas. No hay elección de columnas por correlación con el resultado. Véanse protocolo v1.0 §§3–6 y candidatos_congelados.json: un candidato media, tres OLS, 15 Ridge, 24 RF y 24 GBR, total 67. Ridge usa alpha 0.1,1,10,100,1000; RF usa 300 árboles, profundidad 2/4, hojas 3/8 y fracción 0.5/1; GBR usa 50/100 árboles, aprendizaje 0.03/0.1 y profundidad 1/2. Todos los demás parámetros se exportaron antes de ajustar. La semilla única es 20261008, no se buscan semillas. ElasticNet, XGBoost y persistencia del plan anterior no forman parte del protocolo operativo; diferencias documentadas en fase3/decisiones.md.

## Método, ecuaciones y supuestos

En cada ventana se ajusta únicamente con años anteriores. OLS y Ridge se implementan mediante un pipeline que calcula $z_j=(x_j-\bar x_{j,train})/s_{j,train}$. Su media/escala nunca se aprenden del año validado. Los árboles usan porcentajes originales. OLS minimiza suma de residuos cuadrados; Ridge añade $\alpha\|\beta\|_2^2$. Ambos estiman una media condicional mediante la pérdida cuadrática, aunque el criterio de selección sea error absoluto; no se cambia el estimando a mediana.

Cada candidato produce 99 predicciones fuera del ajuste de su ventana. Definimos $e_i=\hat y_i-y_i$, $MAE=m^{-1}\sum|e_i|$, $RMSE=\sqrt{m^{-1}\sum e_i^2}$, sesgo $m^{-1}\sum e_i$, y $R^2=1-\sum e_i^2/\sum(y_i-\bar y)^2$. Las métricas quedan en puntos salvo R². El RMSE concatenado no es el promedio de tres raíces. El sesgo positivo expresa sobreestimación. R² negativo es posible; denominador cero se informa no definido.

La regla congelada conserva candidatos hasta MAE mínimo+0.1; luego hasta RMSE mínimo del conjunto+0.1; prefiere menos entradas, orden media/OLS/Ridge/RF/GBR y primer ID de grilla. La regla se aplica globalmente y dentro de cada especificación con la media común. No se elige únicamente el menor MAE bruto ni se amplía búsqueda. La tolerancia es preferencia prospectiva por parsimonia, no evidencia de irrelevancia educativa.

La dependencia territorial y tres años validados limitan independencia. El desempeño del ganador en estas ventanas es métrica de selección, potencialmente optimista. No ofrecemos intervalos i.i.d. ni una validación anidada inexistente. El requisito de tres ventanas completas evita rankings con cobertura desigual: se registran tracebacks/advertencias; convergencia no satisfecha o predicciones no finitas inhabilitan. No se recortan predicciones.

## Procedimiento de ejecución y congelación

La celda ejecuta los 201 ajustes de ventanas definidos. Guarda todas las predicciones identificadas por territorio-año, métricas por ventana, tabla completa y fallos. Después ajusta los ganadores de especificación y referencias con las mismas 132 filas y exporta modelos joblib, parámetros íntegros, escalas/coeficientes lineales y huellas. El manifiesto congelacion.json marca el ganador global antes de cualquier error reservado. Esos archivos permiten aplicar exactamente el mismo ajuste a 2023 y 2024.
# %%
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path.cwd()
if not (root / 'fase3').exists(): root = root.parent
sys.path.insert(0, str(root / 'fase3/fuentes'))
from comun import develop, read
comparacion = develop()
print(comparacion.sort_values('mae').head(12).to_string(index=False))
# %% [markdown]
## Lectura de los resultados actuales

La tabla impresa muestra el orden bruto por MAE, mientras que el ganador comunicado por el procedimiento incorpora la tolerancia y parsimonia acordadas. Para no confundir ambos, la siguiente celda presenta el ganador congelado y resume todas las familias, incluyendo las referencias. Las tablas completas permiten revisar también configuraciones menos favorables: no se elimina una familia por tener mal desempeño. Los resultados son actuales y reproducidos; no reproducen los rankings de clasificación históricos.

Las diferencias por especificación responden al valor predictivo de grupos de entradas con este entrenamiento, no a la contribución causal de una dimensión. Incorporar más tasas puede aumentar varianza ante 33 filas en la primera ventana. Regularización y árboles se comparan bajo idénticas particiones, sin atribuir superioridad universal a ninguna familia.
# %%
from informes import resumen_desarrollo
resumen_desarrollo()
# %% [markdown]
## Discusión de esta ejecución actual

El mínimo y ganador coinciden: gradient_boosting_ambas_07 obtuvo MAE 6.332499 y RMSE 7.764136 puntos, sesgo +3.297261 y R² 0.779915 en las 99 predicciones de desarrollo. El mejor candidato con tasas solas alcanzó MAE 6.440524: queda 0.108025 puntos por encima del mínimo, fuera de la banda de 0.1 fijada prospectivamente. Por tanto, la preferencia por menos entradas no desplaza al candidato con ambas. No se interpreta esa pequeña diferencia como importancia causal del IPM ni evidencia de significación estadística.

El mejor Random Forest obtuvo MAE 6.504996; Ridge 7.074271; OLS 7.693311 y la media constante 13.842431. Son mínimos brutos por familia para describir la comparación; la selección aplica la regla completa. La referencia OLS no supera al mejor candidato de estas tres familias complejas en el desarrollo. El sesgo positivo del ganador indica sobreestimación en los años validados, mientras que R² negativo de la constante muestra que una media histórica puede rendir peor que la media del conjunto validado. Los 67 candidatos cumplieron las tres ventanas: no hubo exclusiones numéricas ni advertencias de entrenamiento.

Se congelaron siete artefactos (media, tres OLS, tres ganadores de especificación), todos entrenados únicamente en 132 filas. El ganador con IPM solo es gradient_boosting_ipm_02: 50 etapas, aprendizaje 0.1 y profundidad 1; los de tasas/ambas usan 100 etapas y profundidad 2, aprendizaje 0.1. Las hojas mínimas son 3, subsample 1 y semilla 20261008. El manifiesto conserva defaults completos además de estos parámetros principales. Son resultados actuales, distintos de métricas históricas de clasificación no reproducidas.

## Alcance de la conclusión y paso siguiente

El resumen anterior y fase3/resultados/comparacion_desarrollo.csv contienen los errores realmente calculados. Un modelo que gana esta selección conserva parámetros y huellas; no puede cambiarse por el resultado reservado. La reevaluación siguiente pregunta por estabilidad temporal del procedimiento ya elegido. Fallos y advertencias se mantienen visibles en sus JSON, incluso si las tablas contienen candidatos completos. No se ejecuta contraste territorial, que requiere fase4, ni escenarios predictivos. Las limitaciones de fuente y medición de protocolo §8 permanecen y no se resuelven mediante mejores métricas.
