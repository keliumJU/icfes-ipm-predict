# %% [markdown]
# Controles temporales — solo datos inventados
# Orden: llaves y pesos → intervalo → scaler/mediana → selección → CSV/aritmética.
# Entradas: inventados y configuración congelada de 36 IDs; ninguna lectura del panel.
# No demuestra eficacia de recencia. Semilla 20261010, entorno exacto documentado.
# %%
import sys
from pathlib import Path
project = Path('/home/kelium/Documents/espcarlos/icfes-predict-improved')
sys.path.insert(0, str(project/'experimentos_temporales_objetivo3_v1/etapa1/fuentes'))
from comun import pesos, ajustar_inventado, seleccionar, exact, metricas, CS, KEYS
from pruebas import train_inventado, inventado
import pandas as pd
import numpy as np
import math
from fractions import Fraction
print('Datos inventados; no ajustes sobre panel real. Semilla 20261010.')
# %% [markdown]
# Pesos fijos de semivida 2; el ancla solo usa los años de estas llaves train.
# %%
keys = pd.DataFrame({'codigo_departamento':['01']*3,'anio':[2019,2021,2023]})
w, weights_metadata = pesos(keys)
expected = [float(Fraction(3)*v/Fraction(7,4)) for v in [Fraction(1,4),Fraction(1,2),Fraction(1)]]
assert w.tolist() == expected and math.fsum(w) == 3.0
assert np.all(w > 0)
print('Pesos inventados:', w.tolist(), 'ancla train:', weights_metadata['ancla_train'])
# %% [markdown]
# El intervalo calendario modifica pesos y conserva el cambio observado sin anualizar.
# %%
history = inventado(1)
gap = history[history.anio.eq(2021)].iloc[0]
assert gap.anio_previo == 2019 and gap.intervalo == 2 and gap.cambio_observado == 6
print('Inventado: previo 2019; intervalo 2; cambio observado 6 puntos, sin anualizar.')
# %% [markdown]
# Pipeline de mediana: mismo peso en scaler/regresor. Auditoría por suma independiente.
# %%
train = train_inventado()
model_nb, meta_nb = ajustar_inventado(CS[1],train,dict(origen='inventado',uso='notebook_controles'))
assert meta_nb['ruta_fit'] == ['escalado__sample_weight','modelo__sample_weight']
assert meta_nb['origen'] == 'inventado' and meta_nb['routing'] is False
print('Scaler inventado auditado:', meta_nb['transformaciones'])
# %% [markdown]
# Selección interna igual peso; 2021 fijo. Los grupos no sustituyen al global.
# %%
rows = [dict(id=c['id'],estado='completo',ventanas=[2021],mae=10.,rmse=10.,razon=None) for c in CS]
rows[1].update(mae=2.,rmse=2.)
rows[4].update(mae=1.,rmse=1.)
decision = seleccionar(rows,[2021],2022)
assert decision['global_id'] == CS[4]['id']
assert decision['especificaciones']['historico'] == CS[1]['id']
assert seleccionar([],[],2021)['global_id'] == 'persistencia'
print('Selección inventada: global distinto de grupo histórico; 2021 persistencia fija.')
# %% [markdown]
# CSV exacto acepta 0 entero/flotante y rechaza diferencia 1e−11; MAE solo inventado.
# %%
a = pd.DataFrame({'codigo_departamento':['01'],'anio':[2021],'valor':[0.]})
b = a.copy(); b.valor = [0]
exact(a,b)
b.valor = [1e-11]
rejected = False
try:
    exact(a,b)
except ValueError:
    rejected = True
assert rejected
invented_metrics = metricas([0.,1.,-2.],[1.,3.,-4.])
assert invented_metrics['mae'] == float(Fraction(5,3))
print('CSV exacto y aritmética independiente aprobados SOLO con inventados.')
# %% [markdown]
# Los 17 grupos de la suite completa se ejecutan por separado en pruebas.py y quedan
# registrados con fallos iniciales y revisiones. Este notebook ejecuta seis celdas
# útiles, un ajuste inventado; no contiene datos personales, modelos guardados,
# evaluación real ni simulación. Fase2 exige prompt separado y fase1 completa.
