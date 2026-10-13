# %% [markdown]
# Validación y escenarios condicionales
# Leer PLAN_Y_PROTOCOLO.md. La selección usa solo desarrollo; 2023–2025 fueron vistos previamente, por lo que estos resultados son retrospectivos y exploratorios. Una diferencia de predicciones no es un efecto causal. Orden: preparación, pruebas previas, modelos, pruebas de resultados, tablas y gráficas.
# %%
from pathlib import Path
import sys,json
BASE=Path.cwd()
if not (BASE/'PLAN_Y_PROTOCOLO.md').exists():BASE=BASE/'objetivo4_validacion_escenarios'
sys.path.insert(0,str(BASE/'fuentes'))
from tests import run as probar
print('Pruebas previas:',probar(False))
# %% [markdown]
# Ejecución de los modelos
# La primera ejecución realiza los ajustes. Las siguientes lecturas reutilizan la entrega cerrada. Para una reproducción nueva, copiar esta carpeta y eliminar únicamente los resultados de la copia, conservando originales. No modificar protocolo ni fuentes para mejorar métricas.
# %%
from modelos import run,OUT
if (OUT/'EJECUCION.json').exists():
    print('Resultados anteriores de esta entrega; no se repitieron ajustes.')
    resultado=json.loads((OUT/'EJECUCION.json').read_text())
else:resultado=run()
print(json.dumps(resultado,ensure_ascii=False,indent=2))
# %%
print('Pruebas completas:',probar(True))
import pandas as pd
m=pd.read_csv(OUT/'metricas.csv',dtype={'anio':str})
print(m.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global"').to_string(index=False))
s=pd.read_csv(OUT/'escenarios.csv')
print(s.groupby('escenario').agg(admitidos=('admitido','sum'),total=('admitido','size')).to_string())
# %%
from graficas import run as graficar
print(graficar())
# %%
from resumen import run as diagnosticar
print(diagnosticar())
# %% [markdown]
# Verificación final de la publicación
# Los modelos anteriores no se vuelven a ajustar. Se excluyen de la gráfica los escenarios sin reducción efectiva y se comprueban los datos de cada figura contra los resultados originales. Las diez pruebas finales incluyen estas comprobaciones adicionales.
# %%
from pathlib import Path
import sys
BASE=Path.cwd()
if not (BASE/'PLAN_Y_PROTOCOLO.md').exists():BASE=BASE/'objetivo4_validacion_escenarios'
sys.path.insert(0,str(BASE/'fuentes'))
from tests import run as pruebas_finales
print('Pruebas finales aprobadas:',pruebas_finales(True))
