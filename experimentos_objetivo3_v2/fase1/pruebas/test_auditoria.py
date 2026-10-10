"""Pruebas de datos fase1: no modelos ni métricas predictivas."""
import sys
from pathlib import Path
import unittest
import csv
import io
import json

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'fuentes'))
import pandas as pd
from auditar_2025 import ROOT, V2, OUT, SCORES, ADMIN, clean, masks, validate_keys
from integridad import verificar_conservacion

class AuditoriaTests(unittest.TestCase):
    def test_faltantes_y_ceros_no_entran_como_puntajes_validos(self):
        records = []
        for global_score, math, english in [('200', '50', '50'), ('250', '0', '50'),
                                             ('400', '50', ''), ('', '50', '50')]:
            r = {c: '50' for c in SCORES}
            r.update(punt_global=global_score, punt_matematicas=math, punt_ingles=english,
                     periodo='20251', estu_estudiante='ESTUDIANTE', estu_privado_libertad='N',
                     estu_grado='11', cole_cod_depto_ubicacion='5', cole_calendario='A',
                     estu_consecutivo=str(len(records)))
            records.append(r)
        df = clean(pd.DataFrame(records))
        num, _, stages, _ = masks(df)
        cc = num['punt_global'][stages['06_grado11']]
        available = num['punt_global'][stages['diagnostico_global_disponible']]
        self.assertEqual(cc.count(), 1)
        self.assertEqual(cc.sum(), 200)
        self.assertEqual(cc.mean(), 200)
        self.assertEqual(available.count(), 3)
        self.assertAlmostEqual(available.mean(), 850/3)
        self.assertTrue(pd.isna(num['punt_global'].iloc[3]))

    def test_uniones_rechazan_duplicados_y_cobertura_incompleta(self):
        ok = pd.DataFrame({'codigo_departamento': [5, 8], 'anio': [2025, 2025]})
        expected = {(5, 2025), (8, 2025)}
        validate_keys(ok, expected)
        for bad in [pd.concat([ok, ok.iloc[:1]]), ok.iloc[:1],
                    pd.DataFrame({'codigo_departamento': [5, 8], 'anio': [2020, 2025]})]:
            with self.assertRaises(ValueError):
                validate_keys(bad, expected)

    def test_huellas_fuentes_y_archivos_previos(self):
        verificar_conservacion()

    def test_panel231_preserva198_literal_y_valores(self):
        old = ROOT / 'auditoria/base_analitica_departamento_anio.csv'
        new = V2 / 'fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
        self.assertTrue(new.read_bytes().startswith(old.read_bytes()))
        a = pd.read_csv(old, float_precision='round_trip')
        b = pd.read_csv(new, float_precision='round_trip')
        pd.testing.assert_frame_equal(a, b.iloc[:198].reset_index(drop=True), check_exact=True, check_dtype=False)
        self.assertEqual(len(b), 231)
        self.assertNotIn(2020, set(b.anio))
        self.assertEqual(set(b.groupby('anio').size()), {33})
        self.assertFalse(b.isna().any().any())

    def test_medias_2025_desde_sumas_y_denominadores(self):
        panel = pd.read_csv(V2 / 'fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv', float_precision='round_trip')
        raw = pd.read_csv(OUT / 'agregados_anuales_2025.csv', float_precision='round_trip')
        raw = raw[raw.poblacion.eq('06_grado11')].set_index('codigo_departamento')
        for r in panel[panel.anio.eq(2025)].itertuples():
            a = raw.loc[r.codigo_departamento]
            for c in SCORES:
                self.assertEqual(getattr(r, 'n_' + c), a['n_' + c])
                self.assertAlmostEqual(getattr(r, 'prom_' + c), a['sum_' + c] / a['n_' + c], places=10)

    def test_entradas2025_coinciden_celdas_xlsx(self):
        panel = pd.read_csv(V2 / 'fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv', float_precision='round_trip').set_index(['codigo_departamento', 'anio'])
        cells = pd.read_csv(OUT / 'cifras_xlsx.csv')
        cells = cells[cells.anio.eq(2025)]
        self.assertEqual(len(cells), 528)
        for r in cells.itertuples():
            self.assertAlmostEqual(panel.loc[(r.codigo_departamento, r.anio), r.variable], r.valor, places=10)
            self.assertTrue(r.celda)

    def test_repeticiones_raw_no_duplican_poblacion_retenida(self):
        m = json.loads((OUT / 'identificadores_repetidos_revision.json').read_text())
        self.assertEqual(len(m['grupos']), 2)
        self.assertEqual(m['repeticiones_misma_fila'], 0)
        self.assertTrue(all(g['elegibles'] == 1 and g['filas_completas_distintas'] == 2 for g in m['grupos']))

    def test_alcance_sin_modelos_predicciones_notebooks(self):
        m = json.loads((OUT / 'verificacion_auditoria.json').read_text())
        self.assertTrue(m['ampliacion_validada'])
        self.assertEqual(m['modelos_ajustados'], 0)
        self.assertEqual(m['predicciones_nuevas'], 0)
        self.assertFalse(list(V2.rglob('*.ipynb')))

def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AuditoriaTests)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report = dict(pruebas_ejecutadas=result.testsRun, fallos=len(result.failures), errores=len(result.errors),
                  aprobado=result.wasSuccessful(), salida=stream.getvalue(),
                  alcance='Solo datos/auditoría. Tests de modelos y notebook pendientes de sus fases.')
    (OUT / 'pruebas_auditoria.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(stream.getvalue())
    if not result.wasSuccessful():
        raise SystemExit(1)

if __name__ == '__main__':
    main()
