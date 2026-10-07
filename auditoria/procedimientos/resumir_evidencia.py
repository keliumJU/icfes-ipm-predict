"""Tablas compactas de reconciliación desde controles íntegros ya calculados."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'auditoria/evidencia'
def main():
    a=pd.read_csv(OUT/'agregados_Saber_11_Listo_2018_2024.csv')
    h=pd.read_csv(ROOT/'panel_departamento_anio_unido.csv',sep=';')
    rows=[]
    for version,g in [('panel_raiz_historico',h[h._merge.eq('both')]),('consolidado_todos_grados_actual',a[a.subconjunto.eq('recibido')]),('consolidado_grado11_control_actual',a[a.subconjunto.eq('grado11_control')])]:
        for partition,years in [('muestra_entrenamiento_reportada',[2018,2019,2021,2022]),('muestra_evaluacion_reportada',[2023,2024])]:
            p=g[g.anio.isin(years)]
            rows.append({'version':version,'particion_historica_solo_conteo':partition,'n_celdas':len(p),'positivos_promedio_ge250':int(p.prom_punt_global.ge(250).sum()),'negativos':int(p.prom_punt_global.lt(250).sum()),'no_entrenado':True})
    pd.DataFrame(rows).to_csv(OUT/'reconciliacion_muestras.csv',index=False)
    c=pd.read_csv(OUT/'controles_todos.csv'); f=c[c.archivo.eq('Saber_11_Listo_2018_2024')&c.control.isin(['filas','grado11','grado26'])].copy();f['anio']=f.periodo.astype(str).str[:4].astype(int)
    p=f.groupby(['anio','control']).n.sum().unstack().reset_index()
    p['n_panel_raiz']=p.anio.map(h.groupby('anio').n_estudiantes_saber.sum())
    p['diferencia_actual_menos_panel']=p.filas-p.n_panel_raiz
    p['fuera_grado11']=p.filas-p.grado11
    p.to_csv(OUT/'reconciliacion_anual.csv',index=False)
    # Direct rounding at publication precision; do not silently introduce double rounding.
    actual=pd.read_csv(OUT/'contraste_tabla7.csv').set_index('anio')
    declared={2018:[27.9,250.0,16.7,259.3],2019:[26.1,244.2,16.8,253.4],2021:[23.7,242.8,16.4,251.9],2022:[20.8,247.3,16.9,255.9],2023:[20.0,249.5,17.0,258.1],2024:[17.7,253.2,17.3,261.6]}
    fields=['ipm_media','media_global_simple','de_global_simple','media_global_estudiantes']
    checks=[]
    for year,vals in declared.items():
        for field,v in zip(fields,vals):
            computed=float(actual.loc[year,field]); rounded=round(computed,1)
            checks.append({'ubicacion':'ACA2.pdf p.73 tabla7','anio':year,'variable':field,'declarado':v,'actual_sin_redondear':computed,'actual_redondeo_directo_1decimal':rounded,'coincide_precision_declarada':abs(v-rounded)<1e-10})
    pd.DataFrame(checks).to_csv(OUT/'cotejo_tabla7_declarado.csv',index=False)
    grade=a[a.subconjunto.eq('grado11_control')].copy()
    ipm=pd.read_csv(ROOT/'Fuente del IPM/ipm_departamental_limpio_sin_2020.csv',sep=';')
    grade=grade.merge(ipm,on=['codigo_departamento','anio'],validate='one_to_one')
    years=[2018,2019,2021,2022,2023,2024]
    published={'punt_global':[-.79,-.75,-.74,-.74,-.76,-.64,-.72],'punt_matematicas':[-.71,-.70,-.68,-.70,-.70,-.60,-.67],'punt_lectura_critica':[-.84,-.80,-.77,-.75,-.79,-.65,-.77],'punt_c_naturales':[-.71,-.67,-.69,-.68,-.73,-.61,-.66],'punt_sociales_ciudadanas':[-.79,-.73,-.72,-.74,-.74,-.63,-.70],'punt_ingles':[-.83,-.81,-.82,-.79,-.82,-.72,-.77]}
    correlations=[]
    for field,vals in published.items():
        grade['__mean']=grade['sum_'+field]/grade['n_'+field]
        for year,val in zip(years+['2018-2024'],vals):
            g=grade if isinstance(year,str) else grade[grade.anio.eq(year)]
            computed=g.ipm.corr(g.__mean)
            correlations.append({'ubicacion':'ACA2.pdf p.106 tabla10','anio':year,'variable':field,'n_celdas':len(g),'declarado':val,'actual_sin_redondear':computed,'actual_redondeo_directo_2decimales':round(computed,2),'coincide_precision_declarada':abs(round(computed,2)-val)<1e-10})
    pd.DataFrame(correlations).to_csv(OUT/'cotejo_tabla10_puntajes.csv',index=False)
    inputs=pd.read_csv(ROOT/'auditoria/inventario_trazabilidad.csv')
    assert inputs.sha256.dropna().str.fullmatch('[0-9a-f]{64}').all()
    assert inputs.loc[inputs.estado_git.eq('ignorado')].shape[0]==12
    assert p.filas.sum()==3401100 and p.grado11.sum()==2984199
    assert int(p.diferencia_actual_menos_panel.sum())==534706
    # These are data-integrity/reconciliation assertions, not training or metric optimization.
    (OUT/'comprobaciones_integridad.json').write_text(json.dumps({'insumos_ignorados':12,'registro_fuentes_csv':'3.973.901 filas periódicas y 3.401.100 consolidadas','reconciliacion_neta':{'faltante_panel_20212':534706,'fuera_grado11_consolidado':416901,'diferencia_tesis_menos_panel':117805},'originales_sin_reescritura':True,'modelos_entrenados':0,'base_analitica_entregada':False,'fecha_cliente':'2026-10-07'},indent=2,ensure_ascii=False))
    print('Reconciliación e inventario comprobados; no hay base analítica declarada validada.')
if __name__=='__main__':main()
