"""Concentración territorial y reconciliaciones desde agregados, sin microdatos nuevos."""
import sys
sys.dont_write_bytecode = True
import pandas as pd
from auditar_2025 import ROOT, V2, OUT, SCORES, csv_out
from integridad import save, verificar_conservacion

def main():
    verificar_conservacion()
    f = pd.read_csv(OUT / 'filtros_territorio_periodo.csv', dtype={'codigo_departamento': str})
    stages = ['01_recibido', '02_estudiante', '03_sin_libertad',
              '04_seis_puntajes', '05_codigo_colegio', '06_grado11']
    pivot = f.pivot(index=['periodo', 'codigo_departamento'], columns='control', values='n').fillna(0)
    records = []
    for (period, code), r in pivot.iterrows():
        for before, after in zip(stages, stages[1:]):
            a, b = int(r.get(before, 0)), int(r.get(after, 0))
            assert 0 <= b <= a
            records.append(dict(periodo=period, codigo_departamento=code, etapa=after,
                denominador_previo=a, excluidos=a-b, retenidos=b,
                proporcion_excluida=(a-b)/a if a else None))
    csv_out(records, 'concentracion_exclusiones_territorio_periodo.csv')
    diag = pd.read_csv(OUT / 'diagnostico_medias_disponibles.csv')
    diag['proporcion_excluida_otras_pruebas'] = diag.excluidos_por_otras_pruebas / diag.n_global_disponible
    csv_out(diag, 'concentracion_otras_pruebas.csv')
    agg = pd.read_csv(OUT / 'agregados_periodo_2025.csv')
    checks = []
    for period, g in agg[agg.poblacion.eq('06_grado11')].groupby('periodo'):
        control = f[(f.periodo.eq(period)) & f.control.eq('06_grado11')].n.sum()
        assert int(control) == int(g.n_estudiantes_saber.sum())
        for r in g.to_dict('records'):
            for score in SCORES:
                assert r['n_' + score] == r['n_estudiantes_saber']
                assert abs(r['prom_' + score] - r['sum_' + score] / r['n_' + score]) < 1e-10
        checks.append(dict(periodo=int(period), territorios_con_casos=len(g),
                           registros=int(control), medias_verificadas=len(g)*6))
    annual = agg[agg.poblacion.eq('06_grado11')].groupby('codigo_departamento').sum(numeric_only=True)
    historical = pd.read_csv(ROOT / 'auditoria/base_analitica_departamento_anio.csv')
    last = historical[historical.anio.eq(2024)].set_index('codigo_departamento')
    compare = []
    for code, r in annual.iterrows():
        n = int(r.n_estudiantes_saber)
        old = int(last.loc[code, 'n_estudiantes_saber'])
        compare.append(dict(codigo_departamento=code, n_historico2024=old, n_actual2025=n,
                            diferencia=n-old, cambio_relativo=(n-old)/old))
    csv_out(compare, 'comparacion_cobertura_territorial_2024_2025.csv')
    totals = pd.read_csv(OUT / 'filtros_raw_2025.csv')
    for period in [20251, 20252]:
        t = totals[totals.periodo.eq(period)].set_index('control').n
        assert t['01_recibido'] == t['filas_fisicas']
        for stage in stages:
            assert f[f.periodo.eq(period) & f.control.eq(stage)].n.sum() == t[stage]
    save(OUT / 'controles_complementarios.json', dict(aprobado=True, periodos=checks,
        reconciliacion_filas_fisicas_y_etapas=True, concentracion_territorial_calculada=True,
        comparacion_historica='Conteos elegibles 2024 vs 2025 y filtros por periodo históricos; no se dispone de exclusiones raw históricas por territorio en esta evidencia.',
        paginas_pdf_nuevas=[], semillas='No aplica; cálculos deterministas.', entrenamiento=False))
    print(checks)

if __name__ == '__main__':
    main()
