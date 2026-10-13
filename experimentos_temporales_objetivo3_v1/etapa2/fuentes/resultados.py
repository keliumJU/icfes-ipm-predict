"""Tablas/gráficos descriptivos; solo guardados auditados, ningún fit."""
import json,math,os
from pathlib import Path
import numpy as np,pandas as pd
os.environ['MPLCONFIGDIR']=str(Path(__file__).absolute().parents[1]/'resultados/matplotlib_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from auditar import ROOT,OUT,E2,K,read,csv,metrics

def main():
    assert read(OUT/'auditoria_independiente.json')['aprobado']
    out=OUT/'tablas';out.mkdir(exist_ok=True);fig=OUT/'graficos';fig.mkdir(exist_ok=True)
    e=csv(OUT/'predicciones_externas.csv');orig=csv(OUT/'predicciones_internas.csv');unique=csv(OUT/'internas_unicas.csv')
    persist=e[e.procedimiento=='persistencia'][K+['prediccion']].rename(columns={'prediccion':'referencia_persistencia'})
    errors=e.merge(persist,on=K,validate='many_to_one',sort=False)
    errors['error_absoluto']=abs(errors.error);errors['error_cuadrado']=errors.error**2
    errors['error_persistencia']=errors.referencia_persistencia-errors.observado
    errors['delta_error_absoluto']=errors.error_absoluto-abs(errors.error_persistencia)
    errors['delta_error_cuadrado']=errors.error_cuadrado-errors.error_persistencia**2
    errors['cambio_observado']=errors.observado-errors.puntaje_previo
    errors['direccion_observada']=np.sign(errors.cambio_observado).astype(int)
    errors['direccion_predicha']=np.sign(errors.cambio_predicho).astype(int)
    errors['direccion_correcta']=errors.direccion_observada==errors.direccion_predicha
    errors['magnitud_observada']=abs(errors.cambio_observado);errors['magnitud_predicha']=abs(errors.cambio_predicho)
    errors['error_magnitud']=errors.magnitud_predicha-errors.magnitud_observada
    errors.to_csv(out/'predicciones_errores_pareados.csv',index=False)
    rows=[]
    for scope,cols in [('global',['procedimiento']),('anio',['procedimiento','anio']),('territorio',['procedimiento','codigo_departamento'])]:
        for key,part in errors.groupby(cols,sort=False):
            key=key if isinstance(key,tuple) else (key,)
            r=dict(corte=scope,**dict(zip(cols,key)),**metrics(part))
            r.update(delta_mae=math.fsum(part.delta_error_absoluto)/len(part),delta_mse=math.fsum(part.delta_error_cuadrado)/len(part),direccion_aciertos=int(part.direccion_correcta.sum()),direccion_porcentaje=100*int(part.direccion_correcta.sum())/len(part),magnitud_observada_media=math.fsum(part.magnitud_observada)/len(part),magnitud_predicha_media=math.fsum(part.magnitud_predicha)/len(part));rows.append(r)
    for label,mask in [('2021–2024',errors.anio<=2024),('2025',errors.anio==2025)]:
        for role,part in errors[mask].groupby('procedimiento',sort=False):rows.append(dict(corte=label,procedimiento=role,**metrics(part),delta_mae=math.fsum(part.delta_error_absoluto)/len(part)))
    summaries=pd.DataFrame(rows);summaries.to_csv(out/'metricas_externas.csv',index=False)
    internal=[]
    for label,frame in [('original_por_ventana',orig),('unicas_condicionadas',unique)]:
        groups=['externo','id'] if label=='original_por_ventana' else ['id']
        for key,part in frame.groupby(groups,sort=False):
            key=key if isinstance(key,tuple) else (key,);internal.append(dict(alcance=label,**dict(zip(groups,key)),**metrics(part)))
        for (ident,year),part in frame.groupby(['id','anio'],sort=False):internal.append(dict(alcance=label+'_por_anio',id=ident,anio=year,**metrics(part)))
    pd.DataFrame(internal).to_csv(out/'metricas_internas.csv',index=False)
    records=read(OUT/'registros_internos.json');pd.DataFrame([{**r,'ventanas':json.dumps(r['ventanas'])} for r in records]).to_csv(out/'registros_144.csv',index=False)
    selections=[]
    for year in range(2021,2026):
        d=read(OUT/f'seleccion_{year}.json')['decision']
        selections.extend(dict(anio=year,procedimiento=role,id=ident,seleccion='fija sin puntuación' if year==2021 else 'internas antes externo') for role,ident in {'global':d['global_id'],**d['especificaciones'],'persistencia':'persistencia'}.items())
    pd.DataFrame(selections).to_csv(out/'selecciones.csv',index=False)
    weights=[]
    for file in sorted((OUT/'metadatos').glob('*.json')):
        m=read(file)
        weights.extend(dict(ajuste=file.stem,id=m['id'],codigo_departamento=code,anio=year,ancla_train=m['pesos']['ancla_train'],peso_bruto=raw,peso_normalizado=w) for (code,year),raw,w in zip(m['pesos']['llaves'],m['pesos']['pesos_brutos'],m['pesos']['pesos']))
    pd.DataFrame(weights).to_csv(out/'pesos_por_fila_ajuste.csv',index=False)
    annual=summaries[(summaries.corte=='anio')&summaries.procedimiento.isin(['global','persistencia'])]
    fig1,ax=plt.subplots(figsize=(8,4));years=list(range(2021,2026));x=np.arange(5)
    for offset,role,label in [(-.18,'global','Recencia global'),(.18,'persistencia','Persistencia = uniforme v5')]:
        vals=[float(annual[(annual.procedimiento==role)&(annual.anio==year)].mae.iloc[0]) for year in years]
        ax.bar(x+offset,vals,width=.36,label=label)
    ax.set_xticks(x,years);ax.set_ylabel('MAE (puntos de puntaje global)');ax.set_title('Comparación exploratoria por año · n=33 pares/año');ax.legend();fig1.tight_layout();fig1.savefig(fig/'mae_por_anio.png',dpi=150);plt.close(fig1)
    territory=summaries[(summaries.corte=='territorio')&(summaries.procedimiento=='global')].sort_values('delta_mae')
    fig2,ax=plt.subplots(figsize=(11,4));ax.bar(territory.codigo_departamento,territory.delta_mae);ax.axhline(0,color='black',linewidth=.7);ax.set_xlabel('Código de territorio del colegio');ax.set_ylabel('MAE recencia − persistencia (puntos)');ax.set_title('Diferencias descriptivas · n=5 pares/territorio, 33 territorios');fig2.tight_layout();fig2.savefig(fig/'delta_mae_territorio.png',dpi=150);plt.close(fig2)
    primary=errors[errors.procedimiento=='global'];fig3,ax=plt.subplots(figsize=(6,5));ax.scatter(primary.cambio_observado,primary.cambio_predicho,s=18,alpha=.6);bounds=[min(primary.cambio_observado.min(),primary.cambio_predicho.min()),max(primary.cambio_observado.max(),primary.cambio_predicho.max())];ax.plot(bounds,bounds,color='black',linewidth=.8);ax.set_xlabel('Cambio observado (puntos)');ax.set_ylabel('Cambio predicho (puntos)');ax.set_title('Recencia global · n=165 pares ya vistos');fig3.tight_layout();fig3.savefig(fig/'cambios_global.png',dpi=150);plt.close(fig3)
    meta=read(OUT/'meta.json');audit=read(OUT/'auditoria_independiente.json');status='SATISFECHA' if meta['cumple'] else 'NO SATISFECHA'
    text=f'''# Piloto exploratorio recencia_h2 — informe completo

2026-10-11, America/Bogota. Meta original {status}. Primario fijo: recencia/global,
165 pares (33 territorios × 5 años), igual peso territorio-año.

MAE recencia/global: {meta['mae_recencia_global']!r} puntos; MAE persistencia:
{meta['mae_persistencia']!r} puntos. Mejora exacta: {meta['mejora_porcentaje']!r}%.
Decisión computada sin redondear: 100*(MAEpersistencia−MAEglobal)/MAEpersistencia ≥5.
Delta MAE frente uniforme v5/global: {meta['delta_mae_v5']!r} puntos, descriptivo sin
umbral nuevo. Los CSV v5/global y v3/persistencia son numéricamente idénticos y no
aportan dos evidencias independientes. Ubicación: resultados/meta.json; procedimiento
autónomo fuentes/auditar.py, referencia reconstruida y cotejada sobre 165 llaves.

La ponderación fue el único cambio material: semivida fija2, ancla máximo train,
todos los años retenidos, media de pesos1; scaler/regresor ponderados o boosting
sample_weight. Entradas/defaults/36IDs/bandas/particiones/semilla20261010 conservados.
2021 persistencia fija sin fit/selección. Cada ventana tuvo ajustes propios; selección
guardada antes externo, deduplicación externa solo por ID. Grupos son secundarios;
ningún grupo/corte/control reemplaza el primario ni rescata la meta.

Ejecución actual: {audit['intentos']} intentos, {audit['segundos']!r} segundos de
presupuesto7200s, incluyendo spawn/Pipeline/comunicación, sin saldo histórico.
350internos; externas/repeticiones ajustadas constan por etiqueta en ledger.json.
Persistencia sin fit y tiempo separado en tiempos_persistencia.json. Cinco controles
globales aprobados, predicciones repetidas en repeticiones/; atol1e−10 rtol0 solo
para repetición, CSV exactos. Ningún modelo histórico cargado ni nuevos fits uniformes.
Modelos propios de cada ajuste guardados como artefactos auditables, no modelo final.

Auditoría independiente APROBADA: 11880 internas originales, 144 registros, 36IDs,
1155 externas (7×165); 4752 únicas condicionadas tras igualdad exacta de copias y
firmas train/X/y/pesos/defaults/semilla/versiones. Representante menor externo;
linaje completo11880, sin promediar discrepancias. Diez internas acumuladas contienen
cuatro años únicos de validación; no diez años independientes. originales se conservan.
CSV intfloat0 equivalente; pruebas de rechazo1e−11/campos/orden/no finito aprobadas.
Matrices/objetivos/pesos por fila/scaler/warnings y huellas auditados sin deserializar
modelos. Ubicaciones: auditoria_independiente.json, firmas_internas.json, metadatos/,
linaje_internas.csv, predicciones_internas.csv, internas_unicas.csv y tablas/.

Tablas completas: predicciones_errores_pareados.csv contiene errores absolutos,
cuadrados, deltas pareados, dirección exacta−/0/+, magnitudes; metricas_externas.csv
incluye MAE/RMSE/sesgo/n/deltas por procedimiento, año, territorio y cortes2021–2024
frente2025. metricas_internas.csv conserva ventanas originales y síntesis únicas;
registros_144.csv incluye todos los candidatos; selecciones.csv registra35 salidas;
pesos_por_fila_ajuste.csv registra pesos de cada entrenamiento. Gráficos descriptivos
con unidades y n en resultados/graficos/, sin inferencia causal ni nueva selección.

Hallazgo actual: el contraste primario determina {status.lower()} para la meta.
Impacto: solo este resultado puede evaluar el objetivo acordado. Alternativa lógica:
conservar persistencia como referencia y reportar todas las salidas/cortes sin rescate;
resuelto en esta fase mediante tablas/auditoría/informe. Eficacia futura y estabilidad
no se deducen de esta evaluación retrospectiva. Más historia o confirmación requiere
fuentes comparables/fechas y autorización separadas; no se descargaron aquí.

Todos2021–2025 ya vistos: resultado EXPLORATORIO, sin confirmación independiente,
causalidad o pronóstico anticipado demostrado. Guainía238vs404/21.012106 puntos es
evidencia histórica en v2/fase1/resultados/diagnostico_medias_disponibles.csv; no
nuevo hallazgo recencia. Procedencia local no autenticada; IPMhogares-alumnos,
geografía colegio frente residencia, enlace ecológico, dependencia y pocos años.
Antecedentes archivados no reabiertos. Meta v5 no satisfecha intacta; no etapa3v5,
simulación/notebookpersonal/objetivo4/entrenamiento final/commit/push/avance automático.

Incidencia propia anterior al primerfit: helper de conservación leyó `destino` en vez
de `enlace` del inventario de symlink. Corregido y recongelado como v2, sin cambiar
criterios científicos. Fallo original/salida y congelaciónv1 conservados; incompleto.json
corresponde exclusivamente a ese intento con fits0, no al estado final. Ver registro.
'''
    (E2/'INFORME.md').write_text(text)
    print('Tablas completas, 3 gráficos e informe generados')
if __name__=='__main__':main()
