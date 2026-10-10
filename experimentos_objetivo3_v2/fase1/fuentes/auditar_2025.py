"""Censo local2025, agregación y cotejo; no contiene lógica de modelos."""
from collections import Counter, defaultdict
from pathlib import Path
import csv
import hashlib
import json
import platform
import re
import sys
import time
import unicodedata

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import openpyxl
from integridad import ROOT, V2, OUT, save, verificar_conservacion, sha

CHUNK = 100000
SCORES = ['punt_global', 'punt_matematicas', 'punt_lectura_critica',
          'punt_c_naturales', 'punt_sociales_ciudadanas', 'punt_ingles']
ADMIN = ['periodo', 'estu_estudiante', 'estu_privado_libertad', 'estu_grado',
         'cole_cod_depto_ubicacion', 'cole_calendario', 'estu_consecutivo']
NA = ['', 'NA', 'N/A', 'NULL', 'null', 'NaN', 'nan', 'None', '<NA>']
HIST_YEARS = [2018, 2019, 2021, 2022, 2023, 2024]
KEY = ['codigo_departamento', 'anio']
BOOK = 'Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx'

def norm(x):
    t = ''.join(c for c in unicodedata.normalize('NFD', str(x)) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^A-Z0-9]+', ' ', t.upper()).strip()

def csv_out(rows, name):
    dest = OUT / name
    pd.DataFrame(rows).to_csv(dest, index=False, lineterminator='\n')

def clean(df):
    return df.replace(NA, np.nan)

def numbers(df):
    return {c: pd.to_numeric(df[c].str.replace(',', '.', regex=False), errors='coerce') for c in SCORES}

def masks(df):
    num = numbers(df)
    est = df.estu_estudiante.fillna('').str.strip().str.upper().eq('ESTUDIANTE')
    lib = ~df.estu_privado_libertad.fillna('N').str.strip().str.upper().eq('S')
    code = pd.to_numeric(df.cole_cod_depto_ubicacion, errors='coerce')
    school = code.notna()
    grade = pd.to_numeric(df.estu_grado, errors='coerce').eq(11)
    complete = pd.Series(True, index=df.index)
    for v in num.values():
        complete &= v.notna() & v.gt(0)
    stages = {
        '01_recibido': pd.Series(True, index=df.index),
        '02_estudiante': est,
        '03_sin_libertad': est & lib,
        '04_seis_puntajes': est & lib & complete,
        '05_codigo_colegio': est & lib & complete & school,
        '06_grado11': est & lib & complete & school & grade,
        'diagnostico_global_disponible': est & lib & school & grade & num['punt_global'].notna() & num['punt_global'].gt(0),
        'administrativo_grado11': est & lib & school & grade,
    }
    return num, code, stages, dict(estudiante=est, sin_libertad=lib, seis_puntajes=complete,
                                  codigo_colegio=school, grado11=grade)

def validate_keys(frame, expected):
    if frame.duplicated(KEY).any():
        raise ValueError('Llaves territorio-año duplicadas')
    got = set(map(tuple, frame[KEY].astype(int).to_numpy()))
    if got != expected:
        raise ValueError('Cobertura/llaves distintas de las esperadas')

def workbook(base, tasas):
    names = {norm(r.departamento): int(r.codigo_departamento) for r in base.itertuples()}
    names.update({'BOGOTA': 11, 'BOGOTA D C': 11, 'SAN ANDRES Y PROVIDENCIA': 88})
    varnames = {norm(c): c for c in tasas}
    w = openpyxl.load_workbook(ROOT / BOOK, read_only=True, data_only=True)
    source, notes, headers = {}, [], []
    for sn in ['IPM_Departamentos', 'IPM_Indicadores_Departamento ']:
        sheet = w[sn]
        rows = list(sheet.iter_rows())
        years = {}
        for c in rows[11]:
            t = str(c.value)
            if re.fullmatch(r'20\d\d\**', t):
                y = int(t[:4])
                if y in HIST_YEARS + [2025]:
                    years[y] = c.column - 1
                    headers.append(dict(hoja=sn, anio=y, celda=c.coordinate, texto=t,
                                        dominio_celda=rows[12][c.column-1].value))
        assert set(years) == set(HIST_YEARS + [2025])
        assert all(rows[12][i].value == 'Total' for i in years.values())
        dept = None
        for row in rows:
            vals = [c.value for c in row]
            first = vals[0]
            if isinstance(first, str) and any(t in first for t in ['Fuente:', 'Nota:', 'Actualizado', 'Datos expandidos']):
                notes.append(dict(archivo=BOOK, hoja=sn, celda=row[0].coordinate, texto=first))
            if norm(first) in names:
                dept = names[norm(first)]
            if sn == 'IPM_Departamentos':
                if norm(first) not in names:
                    continue
                var = 'ipm'
            else:
                var = varnames.get(norm(vals[1])) if len(vals) > 1 else None
                if not var or dept is None:
                    continue
            for y, i in years.items():
                k = (dept, y, var)
                if k in source:
                    raise ValueError(f'Fuente XLSX duplicada {k}')
                v = vals[i]
                assert isinstance(v, (int, float)) and 0 <= v <= 100, (k, row[i].coordinate)
                source[k] = dict(valor=v, hoja=sn, celda=row[i].coordinate)
    w.close()
    assert len(source) == 33 * 7 * 16
    csv_out(notes, 'notas_ipm_2025.csv')
    csv_out(headers, 'encabezados_ipm_2025.csv')
    csv_out([dict(codigo_departamento=d, anio=y, variable=v, archivo=BOOK, **spec)
             for (d, y, v), spec in sorted(source.items())], 'cifras_xlsx.csv')
    return source

def audit_raw(valid_codes):
    controls = Counter()
    groupcontrols = Counter()
    missing = Counter()
    combo = Counter()
    calendars = Counter()
    categories = Counter()
    aggregation = defaultdict(Counter)
    schemas = []
    ids = set()
    eligible_ids = set()
    for per in ['20251', '20252']:
        p = ROOT / f'raw_data/Examen_Saber_11_{per}.txt'
        with p.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            original = next(reader)
            header = [c.strip().lower() for c in original]
            assert len(header) == len(set(header))
            assert set(SCORES + ADMIN).issubset(header)
            schemas.extend(dict(archivo=str(p.relative_to(ROOT)), columna=c, posicion_1=i+1,
                                encoding='utf-8-sig', separador=';') for i, c in enumerate(header))
            idx = [header.index(c) for c in SCORES + ADMIN]
            block = []
            def process(block):
                df = clean(pd.DataFrame(block, columns=SCORES + ADMIN))
                num, code, stages, flags = masks(df)
                labels = code.map(lambda v: str(int(v)) if pd.notna(v) and float(v).is_integer() else '(sin_codigo_valido)')
                for name, mask in stages.items():
                    controls[(per, name)] += int(mask.sum())
                    for d, n in labels[mask].value_counts().items():
                        groupcontrols[(per, d, name)] += int(n)
                for name, flag in flags.items():
                    controls[(per, 'incumple_concurrente_' + name)] += int((~flag).sum())
                bits = sum((~v).astype(int) * (2 ** i) for i, v in enumerate(flags.values()))
                tmp = pd.DataFrame(dict(codigo=labels, combinacion=bits))
                for (d, b), n in tmp.groupby(['codigo', 'combinacion']).size().items():
                    combo[(per, d, int(b))] += int(n)
                for field in SCORES + ['estu_grado', 'cole_cod_depto_ubicacion']:
                    v = num[field] if field in num else pd.to_numeric(df[field], errors='coerce')
                    states = {'nulo': df[field].isna(), 'no_numerico': df[field].notna() & v.isna(),
                              'cero': v.eq(0), 'negativo': v.lt(0)}
                    if field in SCORES:
                        limit = 500 if field == 'punt_global' else 100
                        states['supera_rango_documentado'] = v.gt(limit)
                        states['no_entero'] = v.notna() & v.mod(1).ne(0)
                        controls[(per, 'fuera_rango_elegible_' + field)] += int((stages['06_grado11'] & ((v < 0) | (v > limit))).sum())
                    for scope, mask in [('recibido', stages['01_recibido']), ('administrativo_grado11', stages['administrativo_grado11'])]:
                        for status, bad in states.items():
                            for d, n in labels[mask & bad].value_counts().items():
                                missing[(per, d, scope, field, status)] += int(n)
                badcode = code.notna() & (~code.isin(valid_codes) | code.mod(1).ne(0))
                controls[(per, 'codigo_invalido_elegible')] += int((stages['06_grado11'] & badcode).sum())
                controls[(per, 'periodo_distinto_nombre')] += int(df.periodo.fillna('').str.replace(r'\.0$', '', regex=True).ne(per).sum())
                for value, n in df.estu_grado.fillna('(faltante)').value_counts().items():
                    categories[(per, 'grado_recibido', value)] += int(n)
                for value, n in df.estu_estudiante.fillna('(faltante)').value_counts().items():
                    categories[(per, 'tipo_examinando', value)] += int(n)
                for value, n in df.loc[stages['06_grado11'], 'cole_calendario'].fillna('(faltante)').value_counts().items():
                    calendars[(per, value)] += int(n)
                for value in df.estu_consecutivo:
                    if pd.isna(value):
                        controls[(per, 'id_faltante')] += 1
                    else:
                        digest = hashlib.sha256(str(value).encode()).digest()
                        if digest in ids:
                            controls[(per, 'id_repetido_exceso_ambos_periodos')] += 1
                        ids.add(digest)
                for value in df.loc[stages['06_grado11'], 'estu_consecutivo']:
                    if pd.isna(value):
                        controls[(per, 'id_faltante_elegible')] += 1
                    else:
                        digest = hashlib.sha256(str(value).encode()).digest()
                        if digest in eligible_ids:
                            controls[(per, 'id_repetido_exceso_elegible')] += 1
                        eligible_ids.add(digest)
                for scope in ['06_grado11', 'diagnostico_global_disponible', '05_codigo_colegio']:
                    mask = stages[scope]
                    t = pd.DataFrame({'codigo': code[mask]})
                    for c, v in num.items():
                        t[c] = v[mask]
                    for d, g in t.groupby('codigo'):
                        a = aggregation[(per, int(d), scope)]
                        a['n_estudiantes_saber'] += len(g)
                        for c in SCORES:
                            a['sum_' + c] += float(g[c].sum())
                            a['n_' + c] += int(g[c].count())
            for row in reader:
                controls[(per, 'filas_fisicas')] += 1
                if len(row) != len(header):
                    controls[(per, 'filas_ancho_incorrecto')] += 1
                    continue
                block.append([row[i] for i in idx])
                if len(block) >= CHUNK:
                    process(block)
                    block = []
            if block:
                process(block)
        print(json.dumps(dict(periodo=per, recibido=controls[(per, '01_recibido')],
                              grado11=controls[(per, '06_grado11')]), ensure_ascii=False), flush=True)
    # No IDs ni firmas individuales se serializan.
    csv_out([dict(periodo=p, control=c, n=n) for (p, c), n in sorted(controls.items())], 'filtros_raw_2025.csv')
    csv_out([dict(periodo=p, codigo_departamento=d, control=c, n=n) for (p, d, c), n in sorted(groupcontrols.items())], 'filtros_territorio_periodo.csv')
    csv_out([dict(periodo=p, codigo_departamento=d, poblacion=s, variable=v, estado=e, n=n)
             for (p, d, s, v, e), n in sorted(missing.items())], 'faltantes_territorio_periodo.csv')
    csv_out([dict(periodo=p, codigo_departamento=d, bits_incumplidos=b, n=n)
             for (p, d, b), n in sorted(combo.items())], 'combinaciones_exclusiones.csv')
    csv_out([dict(periodo=p, campo=c, categoria=v, n=n) for (p, c, v), n in sorted(categories.items())], 'categorias_poblacion.csv')
    csv_out([dict(periodo=p, calendario=c, n=n) for (p, c), n in sorted(calendars.items())], 'calendarios_2025.csv')
    csv_out(schemas, 'esquemas_2025.csv')
    records = []
    for (p, d, s), a in sorted(aggregation.items()):
        r = dict(periodo=p, codigo_departamento=d, anio=2025, poblacion=s, **a)
        for c in SCORES:
            r['prom_' + c] = a['sum_' + c] / a['n_' + c] if a['n_' + c] else None
        records.append(r)
    csv_out(records, 'agregados_periodo_2025.csv')
    annual = defaultdict(Counter)
    for (p, d, s), a in aggregation.items():
        annual[(d, s)].update(a)
    annual_rows = []
    for (d, s), a in sorted(annual.items()):
        r = dict(codigo_departamento=d, anio=2025, poblacion=s, **a)
        for c in SCORES:
            r['prom_' + c] = a['sum_' + c] / a['n_' + c] if a['n_' + c] else None
        annual_rows.append(r)
    csv_out(annual_rows, 'agregados_anuales_2025.csv')
    return controls, pd.DataFrame(annual_rows), pd.DataFrame(records)

def independent_sum():
    # Segunda lectura completa con otro lector/parser, cálculo vectorizado y suma agrupada.
    acc = defaultdict(Counter)
    for per in ['20251', '20252']:
        p = ROOT / f'raw_data/Examen_Saber_11_{per}.txt'
        for df in pd.read_csv(p, sep=';', encoding='utf-8-sig', dtype=str, usecols=SCORES + ADMIN,
                              keep_default_na=False, chunksize=CHUNK):
            df = clean(df)
            code = pd.to_numeric(df['cole_cod_depto_ubicacion'], errors='coerce')
            mask = df['estu_estudiante'].fillna('').str.strip().str.upper().eq('ESTUDIANTE')
            mask &= ~df['estu_privado_libertad'].fillna('N').str.strip().str.upper().eq('S')
            mask &= pd.to_numeric(df['estu_grado'], errors='coerce').eq(11) & code.notna()
            temp = pd.DataFrame({'codigo_departamento': code})
            for c in SCORES:
                v = pd.to_numeric(df[c].str.replace(',', '.', regex=False), errors='coerce')
                temp[c] = v
                mask &= v.notna() & v.gt(0)
            for d, g in temp.loc[mask].groupby('codigo_departamento'):
                a = acc[int(d)]
                a['n_estudiantes_saber'] += len(g)
                for c in SCORES:
                    a['sum_' + c] += float(g[c].sum())
                    a['n_' + c] += int(g[c].count())
    return acc

def main():
    start = time.monotonic()
    verificar_conservacion()
    OUT.mkdir(parents=True, exist_ok=True)
    base = pd.read_csv(ROOT / 'auditoria/base_analitica_departamento_anio.csv', float_precision='round_trip')
    tasas = list(base.columns[base.columns.get_loc('ipm') + 1:])
    codes = set(base.codigo_departamento.astype(int))
    assert len(tasas) == 15 and len(codes) == 33
    expected_hist = {(d, y) for d in codes for y in HIST_YEARS}
    validate_keys(base, expected_hist)
    candidate = pd.read_csv(ROOT / 'panel_departamento_anio_unido_2025.csv', float_precision='round_trip')
    validate_keys(candidate, expected_hist | {(d, 2025) for d in codes})
    source = workbook(base, tasas)
    controls, annual, periods = audit_raw(codes)
    principal = annual[annual.poblacion.eq('06_grado11')].copy()
    validate_keys(principal, {(d, 2025) for d in codes})
    independent = independent_sum()
    checks = []
    for r in principal.to_dict('records'):
        d = int(r['codigo_departamento'])
        for c in ['n_estudiantes_saber'] + ['sum_' + c for c in SCORES] + ['n_' + c for c in SCORES]:
            delta = r[c] - independent[d][c]
            checks.append(dict(codigo_departamento=d, variable=c, delta=delta))
            assert delta == 0, (d, c, delta)
    csv_out(checks, 'cotejo_segunda_lectura.csv')
    new = []
    for r in principal.to_dict('records'):
        d = int(r['codigo_departamento'])
        a = {c: r[c] for c in base.columns if c in r}
        a['departamento'] = base.loc[base.codigo_departamento.eq(d), 'departamento'].iloc[0]
        for c in ['ipm'] + tasas:
            a[c] = source[(d, 2025, c)]['valor']
        new.append(a)
    proposed = pd.DataFrame(new)[base.columns]
    complete = pd.concat([base, proposed], ignore_index=True).sort_values(KEY)
    cotejo = []
    historical_revisions = []
    for rowno, r in enumerate(candidate.to_dict('records'), 2):
        d, y = int(r['codigo_departamento']), int(r['anio'])
        actual = complete[(complete.codigo_departamento.eq(d)) & (complete.anio.eq(y))].iloc[0]
        for c in base.columns:
            if c in KEY or c == 'departamento' or c not in candidate:
                continue
            value = r[c]
            ref = float(actual[c])
            delta = float(value) - ref if pd.notna(value) else None
            spec = source.get((d, y, c), {})
            # Referencia histórica es base congelada; XLSX nuevo también se coteja por separado.
            cotejo.append(dict(fila_candidato=rowno, codigo_departamento=d, anio=y, variable=c,
                               valor_candidato=value, valor_reconstruido=ref, diferencia=delta,
                               coincide=pd.notna(value) and abs(delta) <= (0 if c.startswith('n_') else 1e-10),
                               hoja_2025=spec.get('hoja', ''), celda_2025=spec.get('celda', '')))
    for r in base.to_dict('records'):
        d, y = int(r['codigo_departamento']), int(r['anio'])
        for c in ['ipm'] + tasas:
            spec = source[(d, y, c)]
            historical_revisions.append(dict(codigo_departamento=d, anio=y, variable=c,
                valor_base=r[c], valor_anexo_2025=spec['valor'], diferencia=spec['valor'] - r[c],
                hoja=spec['hoja'], celda=spec['celda'], base_conservada=True))
    csv_out(cotejo, 'cotejo_candidato.csv')
    csv_out(historical_revisions, 'cotejo_historico_anexo_nuevo.csv')
    diag = []
    for period_mode, frame, idx in [('periodo', periods, ['periodo', 'codigo_departamento']),
                                    ('anual', annual, ['codigo_departamento'])]:
        for key, group in frame.groupby(idx):
            g = group.set_index('poblacion')
            if '06_grado11' not in g.index or 'diagnostico_global_disponible' not in g.index:
                continue
            cc, gg = g.loc['06_grado11'], g.loc['diagnostico_global_disponible']
            diag.append(dict(alcance=period_mode, periodo=cc.get('periodo', '2025'),
                codigo_departamento=int(cc.codigo_departamento),
                n_completos=int(cc.n_punt_global), n_global_disponible=int(gg.n_punt_global),
                excluidos_por_otras_pruebas=int(gg.n_punt_global-cc.n_punt_global),
                media_completos=cc.prom_punt_global, media_global_disponible=gg.prom_punt_global,
                diferencia=cc.prom_punt_global-gg.prom_punt_global))
    csv_out(diag, 'diagnostico_medias_disponibles.csv')
    historic_filters = pd.read_csv(ROOT / 'auditoria/evidencia/actualizacion_20261008/filtros_raw.csv', dtype={'periodo': str})
    history = historic_filters.pivot(index='periodo', columns='control', values='n').fillna(0)
    comparison = []
    for per in list(history.index) + ['20251', '20252']:
        received = int(history.loc[per, '01_recibido']) if per in history.index else controls[(per, '01_recibido')]
        stud = int(history.loc[per, '02_estudiante']) if per in history.index else controls[(per, '02_estudiante')]
        lib = int(history.loc[per, '03_sin_libertad']) if per in history.index else controls[(per, '03_sin_libertad')]
        scores = int(history.loc[per, '04_seis_puntajes']) if per in history.index else controls[(per, '04_seis_puntajes')]
        eligible = int(history.loc[per, '06_grado11']) if per in history.index else controls[(per, '06_grado11')]
        comparison.append(dict(periodo=per, evidencia='histórica conservada' if per in history.index else 'censo actual2025',
            recibido=received, estudiantes=stud, sin_libertad=lib, seis_puntajes=scores, grado11=eligible,
            proporcion_retenida=eligible/received, perdida_seis_puntajes=scores-lib,
            proporcion_perdida_puntajes=(lib-scores)/lib))
    csv_out(comparison, 'comparacion_filtros_historicos.csv')
    indispensable = {
        'ancho_periodo_correctos': sum(n for (p, c), n in controls.items() if c in ['filas_ancho_incorrecto', 'periodo_distinto_nombre']) == 0,
        'codigos_elegibles_validos': sum(n for (p, c), n in controls.items() if c == 'codigo_invalido_elegible') == 0,
        'rangos_elegibles_validos': sum(n for (p, c), n in controls.items() if c.startswith('fuera_rango_elegible_')) == 0,
        'ids_elegibles_completos_no_repetidos': sum(n for (p, c), n in controls.items() if c in ['id_faltante_elegible', 'id_repetido_exceso_elegible']) == 0,
        'cobertura33': len(principal) == 33 and set(principal.codigo_departamento.astype(int)) == codes,
        'segunda_lectura_exacta': all(r['delta'] == 0 for r in checks),
        'entradas_completas_rango': bool(complete[['ipm'] + tasas].notna().all().all() and complete[['ipm'] + tasas].ge(0).all().all() and complete[['ipm'] + tasas].le(100).all().all()),
        'denominadores_seis_positivos': bool(principal[['n_' + c for c in SCORES]].gt(0).all().all() and all(principal['n_' + c].eq(principal.n_estudiantes_saber).all() for c in SCORES)),
        'sin2020': 2020 not in set(complete.anio),
    }
    approved = all(indispensable.values())
    target = V2 / 'fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
    if approved:
        target.parent.mkdir(parents=True, exist_ok=True)
        historical_bytes = (ROOT / 'auditoria/base_analitica_departamento_anio.csv').read_bytes()
        assert historical_bytes.endswith(b'\n')
        append = proposed.sort_values(KEY).to_csv(index=False, header=False, lineterminator='\n').encode()
        target.write_bytes(historical_bytes + append)
        check = pd.read_csv(target, float_precision='round_trip')
        pd.testing.assert_frame_equal(base, check.iloc[:198].reset_index(drop=True), check_dtype=False, check_exact=True)
        validate_keys(check, expected_hist | {(d, 2025) for d in codes})
        assert not check.isna().any().any()
    elif target.exists():
        raise RuntimeError('No permitir un panel anterior con controles nuevos fallidos')
    discrepancies = [r for r in cotejo if not r['coincide']]
    revisions = [r for r in historical_revisions if abs(r['diferencia']) > 1e-10]
    summary = dict(fecha_cliente='2026-10-10', modelos_ajustados=0, predicciones_nuevas=0, simulaciones=0,
        chunksize=CHUNK, filas_raw=sum(controls[(p, '01_recibido')] for p in ['20251', '20252']),
        registros_elegibles2025=int(principal.n_estudiantes_saber.sum()),
        controles_indispensables=indispensable, ampliacion_validada=approved,
        panel=str(target.relative_to(ROOT)) if approved else None,
        filas_panel=len(complete) if approved else None,
        registros_panel=int(complete.n_estudiantes_saber.sum()) if approved else None,
        panel_sha256=sha(target) if approved else None, lineas_historicas_preservadas_literalmente=approved,
        celdas_candidato_cotejadas=len(cotejo), discrepancias_candidato=len(discrepancies),
        discrepancias_por_anio=dict(Counter(str(r['anio']) for r in discrepancies)),
        revisiones_historicas_anexo=len(revisions), celdas_xlsx_extraidas=len(source),
        celdas_segunda_lectura=len(checks),
        diagnostico_max_abs_delta_media=max(abs(r['diferencia']) for r in diag),
        identidad='Archivos locales denominados Saber11; esquema y categorías cotejados, grado11 filtrado. Descarga y producto de origen no autenticados independientemente.',
        pdf_paginas_nuevas=[], busquedas_externas=0, origen_local_no_autenticado=True,
        entorno=dict(python=sys.version, pandas=pd.__version__, numpy=np.__version__, openpyxl=openpyxl.__version__, plataforma=platform.platform()),
        duracion_segundos=time.monotonic()-start)
    save(OUT / 'verificacion_auditoria.json', summary)
    verificar_conservacion()
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False), flush=True)

if __name__ == '__main__':
    main()
