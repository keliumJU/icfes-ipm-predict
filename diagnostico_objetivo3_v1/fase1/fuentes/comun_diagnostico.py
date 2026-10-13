"""Funciones compartidas SOLO de lectura y estadística descriptiva; sin estimadores."""
import hashlib
import importlib.metadata as md
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OWN = ROOT / 'diagnostico_objetivo3_v1'
F1 = OWN / 'fase1'
OUT = F1 / 'resultados'
TABLES = F1 / 'tablas'
FIGS = F1 / 'graficos'
V5 = ROOT / 'experimentos_objetivo3_v5'
E1 = V5 / 'etapa1'
E2 = V5 / 'etapa2'
KEYS = ['codigo_departamento', 'anio']
YEARS = [2018, 2019, 2021, 2022, 2023, 2024, 2025]
SOURCE = ROOT / 'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
PANEL = E1 / 'reconstrucciones/panel_cambios.csv'
SOURCE_SHA = '6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3'
PANEL_SHA = 'aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc'
SEED = 20261010


def destination(path):
    p = Path(path)
    if not p.is_absolute():
        p = F1 / p
    if not p.resolve().is_relative_to(F1.resolve()):
        raise ValueError('Destino fuera de fase1')
    for candidate in [p, *p.parents]:
        if candidate == ROOT:
            break
        if candidate.is_symlink():
            raise ValueError('Destino symlink')
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


os.environ['MPLCONFIGDIR'] = str(destination(OUT / 'cache_matplotlib/config').parent)
import numpy as np
import pandas as pd


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, data):
    with destination(path).open('x') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def csv(path):
    return pd.read_csv(path, dtype={'codigo_departamento': str}, float_precision='round_trip')


def write_csv(name, frame):
    p = destination(TABLES / name)
    if p.exists():
        raise ValueError('No sobrescribir tabla existente')
    frame.to_csv(p, index=False, float_format='%.17g')


def environment():
    lock = ROOT / 'experimentos_objetivo3_v4/etapa1/requirements.lock.txt'
    wanted = {n.lower().replace('_', '-'): v for n, v in
              (line.split('==') for line in lock.read_text().splitlines())}
    actual = {d.metadata['Name'].lower().replace('_', '-'): d.version for d in md.distributions()
              if d.metadata['Name'].lower() != 'pip'}
    if platform.python_version() != '3.12.14' or actual != wanted or len(actual) != 54:
        raise RuntimeError('Entorno exacto no disponible')
    pip = subprocess.run([sys.executable, '-m', 'pip', 'check'], capture_output=True,
                         text=True, check=True)
    return dict(aprobado=True, python=platform.python_version(), paquetes=actual,
                sklearn=md.version('scikit-learn'), pip_check=pip.stdout.strip(),
                pip_version=md.version('pip'), lock_sha256=sha(lock), semilla=SEED,
                semilla_usada='No aleatoriedad en diagnóstico; reservada para controles inventados')


def exact(a, b):
    if a.columns.tolist() != b.columns.tolist() or a.shape != b.shape or not a.index.equals(b.index):
        raise ValueError('Campos/orden/índices/cobertura distintos')
    for column in a.columns:
        missing_a, missing_b = a[column].isna(), b[column].isna()
        if not np.array_equal(missing_a, missing_b):
            raise ValueError('Ausencias distintas')
        present = ~missing_a
        if not bool((a.loc[present, column].to_numpy() == b.loc[present, column].to_numpy()).all()):
            raise ValueError('Valores distintos; tolerancia prohibida')


def validate(frame, keys, expected_keys=None, finite_fields=()):
    if frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise ValueError('Llaves ausentes/duplicadas')
    if expected_keys is not None:
        exact(frame[keys].reset_index(drop=True), expected_keys.reset_index(drop=True))
    if finite_fields and not np.isfinite(frame[list(finite_fields)].to_numpy(float)).all():
        raise ValueError('Valores no finitos')


def add_history(source, covariates):
    p = source.sort_values(KEYS).reset_index(drop=True).copy()
    validate(p, KEYS)
    group = p.groupby('codigo_departamento', sort=False)
    p['anio_previo'] = group.anio.shift(1).astype('Int64')
    p['puntaje_previo'] = group.prom_punt_global.shift(1)
    p['cambio_observado'] = p.prom_punt_global - p.puntaje_previo
    for c in covariates:
        p['previo_' + c] = group[c].shift(1)
        p['cambio_' + c] = p[c] - p['previo_' + c]
    p['intervalo'] = p.anio - p.anio_previo
    return p


def load_panel():
    conf = read_json(E1 / 'resultados/configuraciones_congeladas.json')
    groups = conf['grupos']
    inputs = list(dict.fromkeys(x for columns in groups.values() for x in columns))
    cov = [c.removeprefix('cambio_') for c in groups['cambio_ambas'][1:]]
    assert len(inputs) == 18 and len(cov) == 16
    assert sha(SOURCE) == SOURCE_SHA and sha(PANEL) == PANEL_SHA
    source = csv(SOURCE)
    assert set(source.anio) == set(YEARS)
    source.codigo_departamento = source.codigo_departamento.str.zfill(2)
    p = add_history(source, cov)
    p['fuente_sha256'] = SOURCE_SHA
    frozen = csv(PANEL)
    exact(p, frozen)
    exact(p[source.columns], source.sort_values(KEYS).reset_index(drop=True))
    changes = p[p.anio > 2018].copy()
    assert len(p) == 231 and len(changes) == 198 and p.codigo_departamento.nunique() == 33
    assert changes.groupby('anio').size().to_dict() == {y: 33 for y in YEARS[1:]}
    assert changes[changes.anio == 2021].anio_previo.eq(2019).all()
    assert changes.intervalo.eq(changes.anio - changes.anio_previo).all()
    validate(changes, KEYS, finite_fields=['cambio_observado', *inputs])
    assert all(c not in inputs for c in ['anio', 'codigo_departamento', 'intervalo'])
    return p, changes, conf, inputs


def distribution(values):
    a = np.asarray(values, float)
    n = len(a)
    nonfinite = int((~np.isfinite(a)).sum())
    if nonfinite or not n:
        raise ValueError('Distribución incompleta/no finita')
    q10, q25, median, q75, q90 = np.quantile(a, [.1, .25, .5, .75, .9], method='linear')
    return dict(n=n, no_finitos=nonfinite, media=math.fsum(a.tolist()) / n, mediana=float(median),
                q10=float(q10), q25=float(q25), q75=float(q75), q90=float(q90),
                iqr=float(q75 - q25), desviacion_ddof1=float(np.std(a, ddof=1)) if n > 1 else None,
                minimo=float(a.min()), maximo=float(a.max()), rango=float(a.max() - a.min()),
                n_negativos=int((a < 0).sum()), n_ceros=int((a == 0).sum()), n_positivos=int((a > 0).sum()),
                proporcion_negativa=float((a < 0).mean()), proporcion_cero=float((a == 0).mean()),
                proporcion_positiva=float((a > 0).mean()))


def correlation(x, y, method):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    if len(y) != n:
        raise ValueError('Cobertura correlación')
    missing = int((~np.isfinite(x) | ~np.isfinite(y)).sum())
    reason = ('no_finitos_sin_eliminar' if missing else 'n_insuficiente' if n < 2 else
              'constante_x' if np.unique(x).size == 1 else
              'constante_y' if np.unique(y).size == 1 else None)
    if reason:
        return dict(n=n, no_finitos=missing, correlacion=None, razon=reason)
    if method == 'spearman':
        x, y = pd.Series(x).rank(method='average').to_numpy(), pd.Series(y).rank(method='average').to_numpy()
    elif method != 'pearson':
        raise ValueError('Método no acordado')
    return dict(n=n, no_finitos=0, correlacion=float(np.corrcoef(x, y)[0, 1]), razon=None)


def metrics(frame):
    validate(frame, ['anio', 'codigo_departamento'], finite_fields=['prediccion', 'observado', 'puntaje_previo', 'cambio_predicho'])
    y, pred, prev, delta = (frame[c].to_numpy(float) for c in ['observado', 'prediccion', 'puntaje_previo', 'cambio_predicho'])
    e = pred - y
    base = prev - y
    change = y - prev
    n = len(e)
    if not n:
        raise ValueError('Métricas vacías')
    return dict(n=n, mae=math.fsum(abs(float(v)) for v in e) / n,
                rmse=math.sqrt(math.fsum(float(v) ** 2 for v in e) / n), sesgo=math.fsum(e.tolist()) / n,
                mae_persistencia=math.fsum(abs(float(v)) for v in base) / n,
                delta_mae_pareado=math.fsum((np.abs(e) - np.abs(base)).tolist()) / n,
                delta_ecm_pareado=math.fsum((e * e - base * base).tolist()) / n,
                direccion_acertada=float((np.sign(delta) == np.sign(change)).mean()),
                n_direccion_acertada=int((np.sign(delta) == np.sign(change)).sum()),
                magnitud_predicha_media=math.fsum(np.abs(delta).tolist()) / n,
                magnitud_observada_media=math.fsum(np.abs(change).tolist()) / n,
                mae_cambio=math.fsum(np.abs(delta - change).tolist()) / n,
                sesgo_cambio=math.fsum((delta - change).tolist()) / n,
                delta_magnitud_media=math.fsum((np.abs(delta) - np.abs(change)).tolist()) / n,
                n_mejora=int((np.abs(e) < np.abs(base)).sum()), n_empate=int((np.abs(e) == np.abs(base)).sum()),
                n_deterioro=int((np.abs(e) > np.abs(base)).sum()))


def paired(frame):
    f = frame.copy()
    f['cambio_observado'] = f.observado - f.puntaje_previo
    f['error_recalculado'] = f.prediccion - f.observado
    f['error_persistencia'] = f.puntaje_previo - f.observado
    f['delta_error_absoluto'] = abs(f.error_recalculado) - abs(f.error_persistencia)
    f['delta_error_cuadratico'] = f.error_recalculado ** 2 - f.error_persistencia ** 2
    f['error_cambio_predicho'] = f.cambio_predicho - f.cambio_observado
    f['signo_observado'] = np.sign(f.cambio_observado).astype(int)
    f['signo_predicho'] = np.sign(f.cambio_predicho).astype(int)
    f['direccion_acertada'] = f.signo_observado == f.signo_predicho
    f['magnitud_observada'] = abs(f.cambio_observado)
    f['magnitud_predicha'] = abs(f.cambio_predicho)
    return f


def collapse(frame, signatures):
    key = ['id', 'anio', 'codigo_departamento']
    validate(frame, ['externo', *key])
    relevant = ['observado', 'puntaje_previo', 'anio_previo', 'cambio_predicho', 'prediccion', 'error', 'origen']
    compare = frame.groupby(key, sort=False)[relevant].nunique(dropna=False)
    if (compare > 1).any().any():
        raise ValueError('Copias discrepantes: no promediar ni escoger')
    for (ident, year), sub in frame.groupby(['id', 'anio'], sort=False):
        sigs = [signatures[(int(external), ident, int(year))] for external in sub.externo.unique()]
        if any(s != sigs[0] for s in sigs):
            raise ValueError('Linaje de entrenamiento/parametrización discrepante')
    sorted_frame = frame.sort_values(['externo', *key])
    unique = sorted_frame.drop_duplicates(key, keep='first').copy()
    reps = unique.set_index(key).externo
    lineage = frame[['externo', *key, 'ajuste']].copy()
    lineage['externo_representante'] = [int(reps.loc[tuple(r)]) for r in lineage[key].itertuples(index=False, name=None)]
    lineage['es_representante'] = lineage.externo == lineage.externo_representante
    return unique.reset_index(drop=True), lineage
