# %% [markdown]
# Piloto temporal v2 — lectura de artefactos verificados
# Orden: preflight → pruebas sintéticas → congelación → piloto serial → recálculo → este notebook.
# Entradas: CSV/JSON guardados en fase3/resultados. Este notebook no entrena.
# Python3.12.14; sklearn1.9.1; semilla20261010. Panel231 filas; externos165 por procedimiento.
# Alcance: fase3 exclusivamente. 2025 exploratorio; no efectos causales ni significancia del5%.
# %%
from pathlib import Path
import json, pandas as pd
root=Path.cwd()
if not (root/'experimentos_objetivo3_v2').exists():
    root=next(p for p in Path.cwd().parents if (p/'experimentos_objetivo3_v2').exists())
out=root/'experimentos_objetivo3_v2/fase3/resultados'
verified=json.loads((out/'verificacion_resultados.json').read_text())
assert verified['aprobado']
print(json.dumps({k:verified[k] for k in ('completo','ajustes','segundos_consumidos','saldo','cobertura','mejora_porcentaje','umbral_futuro_satisfecho')},ensure_ascii=False,indent=2))
# %% [markdown]
# Ganadores por ventana y comparación externa
# Las selecciones se guardaron antes de predecir cada año externo; la evaluación principal
# corresponde al procedimiento completo con posibles configuraciones distintas por año.
# %%
print(pd.read_csv(out/'ganadores.csv').to_string(index=False))
metrics=pd.read_csv(out/'metricas.csv')
print(metrics[metrics.ambito.eq('conjunto')].to_string(index=False))
print(metrics[metrics.ambito.eq('anual') & metrics.procedimiento.isin(['procedimiento_v2','referencia_v1'])].to_string(index=False))
# %% [markdown]
# Deterioros, trazabilidad y límites
# Métricas territoriales completas en metricas.csv; todas las internas en metricas_internas.csv.
# Predicciones con llaves en predicciones_internas.csv y predicciones_externas.csv.
# Artefactos por ajuste, transformaciones, advertencias, tiempos/ledger y diez repeticiones
# están en resultados/piloto. Recalculo independiente: fuentes/verificar_resultados.py y
# enmienda_reporte.py. No se reutilizan métricas históricas ni se recortan predicciones.
# %%
deterioros=pd.read_csv(out/'deterioros.csv')
selected=deterioros[deterioros.procedimiento.eq('procedimiento_v2')]
print(selected[selected.ambito.eq('anual')].to_string(index=False))
print('Territorios con mayor MAE v2 que v1:', int(selected[selected.ambito.eq('territorial')].deteriora_mae.sum()))
failures=json.loads((out/'fallos.json').read_text())
print('Ajustes fallidos:',len(failures['ajustes_fallidos']),'Ajustes con advertencias:',len(failures['advertencias']))
print('Advertencias: casos completos/Guainía, procedencia local, comparabilidad IPM, enlace ecológico y dependencia temporal/territorial.')
print('PDF leídos: ninguno. Notebook personal y fase4 pendientes de autorización expresa; no se entregan aquí.')
