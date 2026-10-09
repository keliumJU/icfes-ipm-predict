"""Coteja cobertura, cálculos independientes, huellas, selección y reproducción."""
import sys
sys.dont_write_bytecode=True
from comun import *
import nbformat
from datetime import datetime,timezone

def main():
    panel_data=panel();dev=panel_data.query('anio<=2022');reserve=panel_data.query('anio>=2023')
    prep=read('preparacion.json');f=read('congelacion.json');re=read('reevaluacion.json')
    for name,h in prep['entradas_sha256'].items(): assert huella(ROOT/name)==h
    assert re['congelacion_sha256']==huella(OUT/'congelacion.json')
    assert re['ganador_inalterado']==f['ganador_global'] and not re['entrenamiento_actualizado'] and not re['prueba_inedita']
    cv=pd.read_csv(OUT/'predicciones_desarrollo.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    table=pd.read_csv(OUT/'comparacion_desarrollo.csv');assert len(table)+len({v['id'] for v in read('fallos.json')})==67
    assert select(table)==f['ganador_global']
    for spec in cfg.ESPECIFICACIONES:
        assert select(table[(table.especificacion==spec)|(table.familia=='media')])==f['ganadores_especificacion'][spec]
    independent=[]
    for _,row in table.iterrows():
        pred=cv[cv.id==row.id];assert len(pred)==99 and not pred.duplicated(['codigo_departamento','anio']).any()
        assert set(pred.anio)=={2019,2021,2022}
        assert pred.groupby('ventana').size().to_dict()=={1:33,2:33,3:33}
        yy=pred.observado.to_numpy();pp=pred.prediccion.to_numpy();err=pp-yy
        # Cálculo independiente de las cuatro métricas, sin llamar metrics.
        vals=[sum(abs(err))/99,(sum(err*err)/99)**.5,sum(err)/99,1-sum(err*err)/sum((yy-yy.mean())**2)]
        np.testing.assert_allclose(vals,[row.mae,row.rmse,row.sesgo,row.r2],rtol=1e-12,atol=1e-12)
        joined=pred.merge(dev[KEY+[cfg.RESULTADO]],on=KEY,validate='one_to_one');assert len(joined)==99
        np.testing.assert_array_equal(joined.observado,joined[cfg.RESULTADO])
    pred=pd.read_csv(OUT/'predicciones_reevaluacion.csv',dtype={'codigo_departamento':str},float_precision='round_trip')
    scores=pd.read_csv(OUT/'metricas_reevaluacion.csv',dtype={'periodo':str})
    candidates={c['id']:c for c in cfg.candidatos()}
    for name,h in f['artefactos_sha256'].items():
        path=ROOT/name;assert huella(path)==h
        c=candidates[path.stem];model=joblib.load(path);saved=pred[pred.id==c['id']]
        assert len(saved)==66 and saved.groupby('anio').size().to_dict()=={2023:33,2024:33}
        assert not saved.duplicated(['codigo_departamento','anio']).any()
        np.testing.assert_allclose(model.predict(x(reserve,c)),saved.prediccion.to_numpy(),rtol=1e-12,atol=1e-12)
        for year in ('2023','2024','conjunto'):
            part=saved if year=='conjunto' else saved[saved.anio==int(year)]
            expected=metrics(part.observado,part.prediccion);r=scores[(scores.id==c['id'])&(scores.periodo==year)].iloc[0]
            np.testing.assert_allclose(list(expected.values()),[r.mae,r.rmse,r.sesgo,r.r2],rtol=1e-12,atol=1e-12)
    # Repetir únicamente las tres ventanas del ganador: prueba necesaria de determinismo.
    c=candidates[f['ganador_global']]
    for number,(years,year) in enumerate(cfg.VENTANAS,1):
        train=dev[dev.anio.isin(years)];valid=dev[dev.anio==year]
        model,r,w=fit_predict(c,train,valid,'verificacion_reproduccion')
        previous=cv[(cv.id==c['id'])&(cv.ventana==number)]
        np.testing.assert_allclose(r.prediccion,previous.prediccion,rtol=1e-12,atol=1e-12)
        independent.append({'ventana':number,'predicciones_reproducidas':33})
    notebooks=read('verificacion_notebooks.json')
    for entry in notebooks:
        nb=nbformat.read(ROOT/entry['notebook'],as_version=4);nbformat.validate(nb)
        assert all(c.execution_count is not None and not any(o.output_type=='error' for o in c.outputs) for c in nb.cells if c.cell_type=='code')
        assert huella(ROOT/entry['notebook'])==entry['notebook_sha256']
    # Todos los archivos versionados anteriores, salvo continuidad, deben permanecer idénticos.
    original_files=subprocess.check_output(['git','ls-tree','-r','-z','--name-only','7e95ffe823c3d08f345620c0f9bc65dc72fae7d5'],cwd=ROOT).decode().rstrip('\0').split('\0')
    for name in original_files:
        if name=='CONTINUIDAD_OBJETIVO_3.md':continue
        original=subprocess.check_output(['git','show',f'7e95ffe823c3d08f345620c0f9bc65dc72fae7d5:{name}'],cwd=ROOT)
        assert hashlib.sha256(original).hexdigest()==huella(ROOT/name),name
    save('verificacion.json',{'fecha_utc':datetime.now(timezone.utc).isoformat(),'aprobada':True,'versionados_anteriores_conservados':len(original_files)-1,'candidatos_completos':len(table),'ajustes_ventanas':201,'ajustes_finales':len(f['artefactos_sha256']),'ajustes_adicionales_verificacion':3,'predicciones_cv':len(cv),'predicciones_reserva':len(pred),'reproduccion_ganador':independent,'nbformat_kernel_ejecutado':True,'base_sha256':huella(ROOT/'auditoria/base_analitica_departamento_anio.csv'),'simulaciones':0,'contraste_territorial_ejecutado':False})
    files=[p for p in (ROOT/'fase3').rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']+[ROOT/e['notebook'] for e in notebooks]
    save('manifiesto_cierre.json',{str(p.relative_to(ROOT)):huella(p) for p in files})
    print('Cierre verificado: cobertura, métricas, selección, artefactos, reproducción, notebooks e integridad histórica.')

if __name__=='__main__':main()
