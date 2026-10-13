"""Controles inventados de contratos, aritmética, linaje, cobertura y rutas.
No estimadores, fits, deserialización ni resultados personales.
"""
from comun_diagnostico import *
from fractions import Fraction
import ast
import tempfile


def reject(action):
    try:
        action()
    except (ValueError, AssertionError):
        return
    raise AssertionError('Perturbación no rechazada')


def main():
    environment()
    passed = []
    a = pd.DataFrame(dict(codigo_departamento=['05', '08'], anio=[2021, 2021], delta=[0, 0]))
    b = a.copy(); b['delta'] = [0., 0.]
    exact(a, b)
    b.loc[0, 'delta'] = 1e-11
    reject(lambda: exact(a, b))
    b = a.copy(); b.loc[0, 'codigo_departamento'] = '09'; reject(lambda: exact(a, b))
    reject(lambda: exact(a, a.rename(columns={'delta': 'otra'})))
    reject(lambda: exact(a, a[['anio', 'codigo_departamento', 'delta']] ))
    reject(lambda: exact(a, a.iloc[::-1].reset_index(drop=True)))
    reject(lambda: exact(a, a.iloc[:1]))
    nullable = a.copy(); nullable['delta'] = pd.Series([pd.NA, 0], dtype='Int64')
    floats = a.copy(); floats['delta'] = [np.nan, 0.]
    exact(nullable, floats)
    passed.append('CSV exacto: int/float0; rechazo1e-11/llaves/campos/orden/filas; máscara nullable')

    validate(a, KEYS, a[KEYS], ['delta'])
    reject(lambda: validate(pd.concat([a, a.iloc[:1]], ignore_index=True), KEYS))
    reject(lambda: validate(a.iloc[:1], KEYS, a[KEYS]))
    for bad in [np.nan, np.inf, -np.inf]:
        b = a.copy(); b['delta'] = [bad, 0.]
        reject(lambda: validate(b, KEYS, finite_fields=['delta']))
    passed.append('Duplicados/omisiones/no finitos rechazados sin eliminar observaciones')

    d = distribution([-1, 0, 1, 2])
    assert d['n'] == 4 and d['q25'] == -.25 and d['q75'] == 1.25 and d['iqr'] == 1.5
    assert d['mediana'] == .5 and d['media'] == .5 and d['n_ceros'] == 1
    assert abs(d['desviacion_ddof1']-math.sqrt(5/3)) < 1e-14
    assert distribution([2, 2, 2])['rango'] == 0
    assert distribution([2])['desviacion_ddof1'] is None
    assert correlation([1, 1, 1], [1, 2, 3], 'pearson')['razon'] == 'constante_x'
    assert correlation([1, 2, 3], [1, 1, 1], 'spearman')['razon'] == 'constante_y'
    assert correlation([1], [2], 'pearson')['correlacion'] is None
    assert correlation([1, np.inf], [2, 3], 'pearson')['no_finitos'] == 1
    assert pd.Series([1., 1., 3.]).rank(method='average').tolist() == [1.5, 1.5, 3.]
    assert math.isclose(correlation([1, 1, 3], [2, 2, 4], 'spearman')['correlacion'], 1, abs_tol=1e-15)
    assert math.isclose(correlation([1, 2, 3], [3, 2, 1], 'pearson')['correlacion'], -1, abs_tol=1e-15)
    passed.append('Cuantiles lineales/ddof1/rangos medios/empates/constantes/correlaciones indefinidas')

    s = pd.DataFrame(dict(codigo_departamento=['05']*3, anio=[2018, 2019, 2021],
                          prom_punt_global=[100., 99., 103.], ipm=[2., 3., 1.]))
    p = add_history(s, ['ipm'])
    assert p.intervalo.iloc[1:].tolist() == [1, 2]
    assert p.cambio_observado.iloc[1:].tolist() == [-1., 4.]
    assert p.anio_previo.iloc[2] == 2019
    assert p.cambio_ipm.iloc[1:].tolist() == [1., -2.]
    passed.append('Previos por misma llave; intervalos1/2 preservados sin anualizar')

    f = pd.DataFrame(dict(codigo_departamento=['05', '08', '11'], anio=[2021]*3,
                          puntaje_previo=[10., 10., 10.], observado=[10., 12., 8.],
                          cambio_predicho=[0., 1., -3.], prediccion=[10., 11., 7.]))
    m = metrics(f); q = paired(f)
    assert m['mae'] == 2/3 and m['sesgo'] == -2/3 and m['rmse'] == math.sqrt(2/3)
    assert m['delta_mae_pareado'] == -2/3 and m['delta_ecm_pareado'] == -2
    assert m['direccion_acertada'] == 1 and m['n_mejora'] == 2 and m['n_empate'] == 1
    assert q.signo_observado.tolist() == [0, 1, -1] and q.signo_predicho.tolist() == [0, 1, -1]
    assert q.delta_error_absoluto.tolist() == [0, -1, -1]
    assert q.delta_error_cuadratico.tolist() == [0, -3, -3]
    assert m['magnitud_predicha_media'] == m['magnitud_observada_media'] == 4/3
    e = [Fraction.from_float(float(p)-float(o)) for p, o in zip(f.prediccion, f.observado)]
    assert float(sum(map(abs, e), Fraction())/3) == m['mae']
    persistence = f.copy(); persistence['prediccion'] = persistence.puntaje_previo; persistence['cambio_predicho'] = 0.
    assert metrics(persistence)['direccion_acertada'] == 1/3
    passed.append('Signo0/métricas/deltas/magnitud; aritmética racional independiente')

    copies = pd.concat([f.assign(externo=2023, id='inventado', ajuste='e2023'),
                        f.assign(externo=2022, id='inventado', ajuste='e2022')], ignore_index=True)
    copies['anio_previo'] = 2019; copies['error'] = copies.prediccion-copies.observado; copies['origen'] = 'inventado'
    sig = {(x, 'inventado', 2021): {'train': [2019], 'semilla': SEED} for x in [2022, 2023]}
    unique, lineage = collapse(copies, sig)
    assert len(unique) == 3 and len(lineage) == 6 and unique.externo.eq(2022).all()
    assert lineage.es_representante.sum() == 3
    for col in ['prediccion', 'cambio_predicho', 'observado', 'puntaje_previo', 'anio_previo']:
        bad = copies.copy(); bad[col] = bad[col].astype(float); bad.loc[0, col] += 1e-11
        reject(lambda: collapse(bad, sig))
    reject(lambda: collapse(pd.concat([copies, copies.iloc[:1]], ignore_index=True), sig))
    badsig = {**sig, (2023, 'inventado', 2021): {'train': [2019], 'semilla': 0}}
    reject(lambda: collapse(copies, badsig))
    passed.append('Copias idénticas: representante menor externo/linaje; discrepancias y semilla rechazadas')

    with tempfile.TemporaryDirectory(dir=destination(OUT / 'pruebas_inventadas/tmp').parent) as td:
        root = Path(td)
        allowed = destination(root / 'permitido.json')
        assert allowed.parent == root
        reject(lambda: destination(E2 / 'prohibido.json'))
        link = root / 'externo'; link.symlink_to(E2, target_is_directory=True)
        reject(lambda: destination(link / 'prohibido.json'))
        internal_link = root / 'interno'; internal_link.symlink_to(root, target_is_directory=True)
        reject(lambda: destination(internal_link / 'prohibido.json'))
    passed.append('Destinos/symlinks externos e internos rechazados; pruebas aisladas propias')

    candidates = pd.DataFrame(dict(id=['c0', 'c1', 'c2'], externo=[2022]*3))
    validate(candidates, ['externo', 'id'], candidates[['externo', 'id']])
    reject(lambda: validate(candidates.iloc[::-1].reset_index(drop=True), ['externo', 'id'], candidates[['externo', 'id']]))
    reject(lambda: validate(candidates.iloc[:2], ['externo', 'id'], candidates[['externo', 'id']]))
    assert set(copies.anio) == {2021} and len(copies) == 6 and len(unique) == 3
    passed.append('Orden/cobertura candidaturas y ventanas: omisión/orden rechazados')

    scanned = []
    for name in ['comun_diagnostico.py', 'ejecutar_diagnostico.py', 'pruebas_diagnostico.py']:
        path = F1 / 'fuentes' / name
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {'fit', 'fit_transform', 'partial_fit', 'fit_predict'}
            if isinstance(node, ast.Import):
                assert not any(n.name.split('.')[0] in {'joblib', 'pickle', 'cloudpickle'} for n in node.names)
            if isinstance(node, ast.ImportFrom):
                assert (node.module or '').split('.')[0] not in {'joblib', 'pickle', 'cloudpickle', 'piloto', 'worker', 'motor'}
        scanned.append(dict(archivo=str(path.relative_to(ROOT)), sha256=sha(path)))
    passed.append('AST/imports: sin llamadas de ajuste o deserialización; sin runners históricos')
    write_json(OUT / 'pruebas_inventadas/pruebas.json', dict(aprobado=True, grupos=passed,
        n_grupos=len(passed), origen='Datos inventados deterministas; no uso aleatorio', semilla=SEED,
        fits=0, modelos_cargados=0, fuentes=scanned))
    print(json.dumps(dict(aprobado=True, grupos=len(passed), fits=0), ensure_ascii=False))


if __name__ == '__main__':
    main()
