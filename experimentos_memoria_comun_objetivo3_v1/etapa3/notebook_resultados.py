"""Fuente editable de notebook lector. Orden: después de auditoría/documentación."""
CELLS=[
'''from pathlib import Path
import sys, os, json, math, csv, platform, importlib.metadata as md, subprocess
root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p/'experimentos_memoria_comun_objetivo3_v1/etapa3/auditor.py').exists())
stage = root/'experimentos_memoria_comun_objetivo3_v1/etapa3'
sys.path.insert(0,str(stage))
from auditor import load, rows, metrics, select, CAND
lock = dict(line.strip().split('==') for line in (root/'experimentos_objetivo3_v5/etapa1/requirements.lock.txt').read_text().splitlines() if '==' in line and not line.startswith('#'))
assert platform.python_version()=='3.12.14' and len(lock)==54
assert all(md.version(k)==v for k,v in lock.items()) and md.version('scikit-learn')=='1.9.1'
assert os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'
assert subprocess.run([sys.executable,'-m','pip','check'],capture_output=True).returncode==0
seed=20261010
assert load(stage/'AUDITORIA_INDEPENDIENTE.json')['aprobado'] and load(stage/'AUDITORIA_COMPLEMENTARIA.json')['aprobado']
print('Entorno exacto; semilla contractual',seed,'; cero fits/cargas de modelos. Entradas: etapa2 guardada y tablas etapa3. Lectura y cálculo sin escritura.')''',
'''external=rows(root/'experimentos_memoria_comun_objetivo3_v1/etapa2/resultados/predicciones_externas.csv')
recalculated={p:metrics([r for r in external if r['policy']==p]) for p in CAND+['global']}
base=recalculated['persistencia']['MAE']
assert base>0 and math.isfinite(base)
for p,m in recalculated.items():
    m['improvement_percent']=100*(base-m['MAE'])/base
    print(p, json.dumps(m))
print('Primario global: meta5% satisfecha =',recalculated['global']['improvement_percent']>=5)
assert recalculated['global']['MAE']==load(stage/'AUDITORIA_INDEPENDIENTE.json')['global']['MAE']''',
'''coefficients=rows(stage/'tablas/coeficientes_todos_41.csv')
mem=[r for r in coefficients if r['component']=='memoria']
corr=[r for r in coefficients if r['component']=='correccion']
assert len(mem)==11 and all(float(r['coef_lag_standardized'])==0 for r in mem)
assert len(corr)==10 and all(float(r['coef_lag_standardized'])==float(r['intercept_points'])==0 for r in corr)
assert all(r['intercept_in_median_interval']=='True' for r in coefficients)
print('Memoria:11ajustes coeficiente0; predicción=previo+constante histórica. No demuestra dinámica ni causa exclusiva alpha1.')
for r in mem:
    if r['role']=='externa': print(r['evaluated'],r['n_train'],r['intercept_points'])
print('Corrección:10ajustes coeficiente/intercepto0. Común/común+corrección iguales en165externas, bajo configuración actual.')''',
'''internal=rows(root/'experimentos_memoria_comun_objetivo3_v1/etapa2/resultados/predicciones_internas_originales.csv')
for year in range(2022,2026):
    ms={c:metrics([r for r in internal if int(r['external'])==year and r['candidate']==c]) for c in CAND}
    winner,p1,p2=select(ms)
    print(year,'ganador',winner,'poolMAE',p1,'poolRMSE',p2)
print('2021 externo fijo;2021 internas respaldadas y puntuadas. Solo internas seleccionan; externas memoria no rescatan primario.')''',
'''annual=rows(stage/'tablas/por_anio.csv')
territorial=rows(stage/'tablas/por_territorio.csv')
for r in annual:
    if r['policy']=='global': print(json.dumps(r,ensure_ascii=False))
t=[r for r in territorial if r['policy']=='global']
print('Territorios mejoran/empeoran:',sum(float(r['benefit_MAE_points'])>0 for r in t),sum(float(r['benefit_MAE_points'])<0 for r in t))
assert all(float(r['benefit_MAE_points'])==0 for r in annual if r['policy']=='global' and int(r['year'])<2025)
print('Toda mejora global2025.165pares dependientes; no165observaciones independientes. Tablas completas en tablas/.')''',
'''audit=load(stage/'AUDITORIA_INDEPENDIENTE.json')
print('Cobertura',audit['coverage'],'fits históricos',audit['fits_historicos'],'consumo histórico',audit['ledger_used_seconds'])
print('Nuevos fits0; modelos cargados0. Todos2021–2025vistos:exploratorio, sin confirmación independiente/causalidad.')
print('Advertencias:procedencia local no autenticada,Guainía,IPMhogares-alumnos,colegio-residencia,ecología,dependencia,pocos años.')
print('PROPUESTAS_FUTURAS.md: referencia constante y contraste de rezago/regularización; requieren protocolo/autorización separados. Ningún experimento implementado.')'''
]
