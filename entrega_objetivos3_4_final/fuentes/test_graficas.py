"""Pruebas contra desalineación, métricas inventadas y etiquetas equivocadas."""
import unittest
import numpy as np
from analisis import data, metrics, results, LABELS
class TestEvidence(unittest.TestCase):
    def test_metric_hand_calculation(self):
        m=metrics([10,20],[12,19]);self.assertEqual(m['MAE'],1.5);self.assertEqual(m['sesgo'],.5)
        self.assertAlmostEqual(m['RMSE'],np.sqrt(2.5))
    def test_reject_mismatched_or_nonfinite(self):
        for a,b in [([1,2],[1]),([1],[float('nan')]),([],[])]:
            with self.assertRaises(AssertionError):metrics(a,b)
    def test_pair_coverage_and_identity(self):
        d=data();self.assertEqual(len(d),165);self.assertEqual(d.code.nunique(),33)
        self.assertFalse(d.duplicated(['code','year']).any());self.assertTrue(d.groupby('year').size().eq(33).all())
        np.testing.assert_array_equal(d[d.year<2025].seleccion,d[d.year<2025].persistencia)
    def test_aggregate_matches_archived_primary(self):
        t=results(data());self.assertEqual(len(t),18)
        self.assertTrue(t[t.anio=='conjunto'].n.eq(165).all())
    def test_improvement_is_not_poverty_improvement(self):
        t=results(data()).query('anio == "conjunto"').set_index('modelo')
        self.assertGreater(t.loc['pobreza','MAE'],t.loc['persistencia','MAE'])
        self.assertIn('historia',LABELS['seleccion']);self.assertNotIn('IPM',LABELS['seleccion'])
if __name__=='__main__':unittest.main()
