"""Configuración prospectiva v2.0; importar/construir nunca ajusta modelos."""
from itertools import product
from pathlib import Path
import importlib.util
ROOT = Path(__file__).resolve().parents[3]
F2 = ROOT / 'experimentos_objetivo3_v2/fase2'
BASE = ROOT / 'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
BASE_SHA = '6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3'
HISTORICO = ROOT / 'auditoria/base_analitica_departamento_anio.csv'
HISTORICO_SHA = '609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866'
# Reutilizar exclusivamente nombres/orden v1, en lectura, sin ejecutar controles históricos.
_spec = importlib.util.spec_from_file_location('cfg_v1_lectura', ROOT/'protocolo/fuentes/configuracion.py')
_v1 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_v1)
ESPECIFICACIONES = _v1.ESPECIFICACIONES
RESULTADO = 'prom_punt_global'
LLAVES = ['codigo_departamento', 'anio']
ANIOS = (2018, 2019, 2021, 2022, 2023, 2024, 2025)
SEMILLA = 20261010
LIMITE_SEGUNDOS = 7200.0
TOL_MAE = TOL_RMSE = 0.1
ORDEN = ['media', 'ols', 'ridge', 'elastic_net', 'svr', 'gradient_boosting', 'extra_trees']
GRILLAS = {
 'ols': {},
 'ridge': {'alpha':[0.1,1,10,100]},
 'elastic_net': {'alpha':[0.01,0.1,1], 'l1_ratio':[0.2,0.8]},
 'svr': {'C':[1,10,100], 'epsilon':[0.1,1]},
 'gradient_boosting': {'n_estimators':[100,300], 'learning_rate':[0.03,0.1], 'max_depth':[1,2]},
 'extra_trees': {'max_features':[0.5,1.0], 'min_samples_leaf':[1,3,6,10]},
}
FIJOS = {
 'ols': {'fit_intercept':True, 'n_jobs':1},
 'ridge': {'fit_intercept':True,'solver':'svd'},
 'elastic_net': {'fit_intercept':True,'max_iter':20000,'selection':'cyclic','random_state':SEMILLA},
 'svr': {'kernel':'rbf','gamma':'scale'},
 'gradient_boosting': {'loss':'squared_error','min_samples_leaf':3,'subsample':1.0,'random_state':SEMILLA},
 'extra_trees': {'n_estimators':300,'max_depth':None,'n_jobs':1,'random_state':SEMILLA},
}

def candidatos():
 result = [dict(id='media',familia='media',especificacion=None,parametros={'strategy':'mean'})]
 for spec in ESPECIFICACIONES:
  for family, grid in GRILLAS.items():
   for i, values in enumerate(product(*grid.values())):
    result.append(dict(id=f'{family}_{spec}_{i:02d}',familia=family,especificacion=spec,
     parametros={**FIJOS[family],**dict(zip(grid,values))}))
 assert len(result)==100
 return result

def ventanas():
 return [dict(externo=year, entrenamiento=list(ANIOS[:i]),
  internas=[dict(entrenamiento=list(ANIOS[:j]), validacion=ANIOS[j]) for j in range(1,i)])
  for i,year in enumerate(ANIOS) if i>=2]

def construir(c):
 from sklearn.dummy import DummyRegressor
 from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
 from sklearn.svm import SVR
 from sklearn.ensemble import GradientBoostingRegressor, ExtraTreesRegressor
 from sklearn.pipeline import Pipeline
 from sklearn.preprocessing import StandardScaler
 classes=dict(media=DummyRegressor,ols=LinearRegression,ridge=Ridge,elastic_net=ElasticNet,
              svr=SVR,gradient_boosting=GradientBoostingRegressor,extra_trees=ExtraTreesRegressor)
 reg=classes[c['familia']](**c['parametros'])
 return Pipeline([('escalado',StandardScaler()),('modelo',reg)]) if c['familia'] in ORDEN[1:5] else reg

def referencia_v1():
 import json
 historic=json.loads((ROOT/'fase3/resultados/congelacion.json').read_text())
 gid=historic['ganador_global']
 assert gid=='gradient_boosting_ambas_07'
 return dict(id='referencia_v1',familia='gradient_boosting',especificacion='ambas',
             parametros={**historic['parametros_completos'][gid],'random_state':SEMILLA},
             semilla_historica=historic['parametros_completos'][gid]['random_state'],id_historico=gid)
