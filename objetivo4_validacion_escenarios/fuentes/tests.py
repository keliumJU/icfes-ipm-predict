"""Pruebas independientes de métricas, separación, soporte y datos publicados."""
import unittest,json
import numpy as np
import pandas as pd
from modelos import HERE,OUT,metrics,folds,candidates,select,panel,specs
class Reglas(unittest.TestCase):
    def test_metricas_manual(self):
        v=metrics([1,3],[2,1]);self.assertEqual(v['MAE'],1.5);self.assertAlmostEqual(v['RMSE'],np.sqrt(2.5));self.assertEqual(v['sesgo'],-.5);self.assertEqual(v['R2'],-1.5)
    def test_metricas_invalidas(self):
        for y,p in [([],[]),([1],[np.nan]),([1,2],[1])]:
            with self.assertRaises(AssertionError):metrics(y,p)
    def test_folds(self):
        years=[2018,2019,2021,2022,2023]
        for train,test in folds(years,'temporal'):self.assertLess(max(train),test);self.assertNotIn(test,train)
        for train,test in folds(years,'loyo'):self.assertNotIn(test,train);self.assertEqual(len(train),4)
    def test_seleccion_predefinida(self):
        rows=[dict(id='A',MAE=1,RMSE=2,order=1),dict(id='B',MAE=1.05,RMSE=2.05,order=0),dict(id='C',MAE=1.2,RMSE=1,order=2)]
        self.assertEqual(select(rows),'B');self.assertEqual(len(candidates()),15)
    def test_preparacion(self):
        d=panel();self.assertEqual(len(d),231);self.assertTrue(d.prop_oficial.between(0,1).all());self.assertTrue(d.prop_urbana.between(0,1).all());self.assertTrue(d.mat34.between(0,100).all());self.assertEqual(len(specs(d)['componentes']),25)
        self.assertTrue(json.loads((HERE/'preparacion/CONTROL_PREPARACION.json').read_text())['aprobado'])
class Resultados(unittest.TestCase):
    def test_metricas_csv(self):
        p=pd.read_csv(OUT/'predicciones.csv',dtype={'codigo_departamento':str});m=pd.read_csv(OUT/'metricas.csv',dtype={'anio':str})
        for r in m.itertuples():
            q=p[(p.exercise==r.exercise)&(p.method==r.method)&(p.target==r.target)&(p.spec==r.spec)]
            if r.anio!='conjunto':q=q[q.anio==int(r.anio)]
            v=metrics(q.observed,q.predicted)
            for name in ['MAE','RMSE','sesgo']:self.assertAlmostEqual(v[name],getattr(r,name),places=10)
    def test_exclusion_territorial(self):
        decisions=json.loads((OUT/'DECISIONES_TERRITORIALES.json').read_text());self.assertEqual(len(decisions),99)
        for r in decisions:self.assertNotIn(r['omitido'],r['territorios_train']);self.assertEqual(len(r['territorios_train']),32)
    def test_escenarios(self):
        s=pd.read_csv(OUT/'escenarios.csv',dtype={'codigo_departamento':str});d=panel();bounds=json.loads((OUT/'SOPORTE.json').read_text());self.assertEqual(len(s),165)
        a=s[s.admitido];rejected=s[~s.admitido]
        self.assertTrue(rejected.prediccion_escenario.isna().all());self.assertTrue(rejected.diferencia.isna().all());self.assertTrue(a.motivos.fillna('').eq('').all())
        np.testing.assert_allclose(a.diferencia,a.prediccion_escenario-a.prediccion_base,atol=1e-10)
        for r in a.itertuples():
            train=d[(d.anio<=2023)&(d.codigo_departamento==r.codigo_departamento)]
            self.assertTrue(train.ipm.min()<=r.ipm_escenario<=train.ipm.max());self.assertLessEqual(r.distancia,bounds['nn_p95']);self.assertLessEqual(r.distancia_base,bounds['nn_p95'])
        z=a[a.escenario=='sin_cambio'];np.testing.assert_allclose(z.diferencia,0,atol=1e-10)
    def test_presupuesto(self):
        r=json.loads((OUT/'EJECUCION.json').read_text());self.assertTrue(r['completo']);self.assertLessEqual(r['fits'],12000);self.assertLess(r['seconds'],3600)
    def test_graficas(self):
        from graficas import run
        run()
        q=pd.read_csv(HERE/'figuras/datos_errores.csv').set_index('spec');m=pd.read_csv(OUT/'metricas.csv',dtype={'anio':str})
        z=m.query('exercise=="corte2023" and method=="temporal" and target=="prom_punt_global" and anio=="conjunto"').set_index('spec')
        np.testing.assert_allclose(q.MAE,z.loc[q.index,'MAE'],atol=1e-10)
        s=pd.read_csv(OUT/'escenarios.csv');a=s[s.admitido & s.reduccion_pp.gt(0)]
        c=pd.read_csv(HERE/'figuras/datos_escenarios.csv').set_index('escenario');self.assertEqual(int(c['size'].sum()),len(a))
        for name,r in c.iterrows():self.assertAlmostEqual(r['mean'],a[a.escenario==name].diferencia.mean(),places=10)
def run(final=False):
    suite=unittest.TestSuite();suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Reglas))
    if final:suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Resultados))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    assert result.wasSuccessful(),'Pruebas fallidas';return result.testsRun
if __name__=='__main__':run((OUT/'EJECUCION.json').exists())
