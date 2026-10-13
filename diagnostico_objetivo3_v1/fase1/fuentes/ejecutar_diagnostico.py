"""A–D: diagnóstico descriptivo integral desde panel/CSV/JSON congelados, cero fits.

Falla antes de síntesis dependiente si cobertura, valores o linaje discrepan.
No importa código anterior ni estimadores, no deserializa modelos ni altera selección.
"""
from comun_diagnostico import *
from itertools import combinations


def verify_documental():
    from preflight_documental import verify, git
    prep = read_json(OWN / 'REGISTRO_PREPARACION.json')
    protected = verify(prep['inventario_protegido']['sha256_versionados'])
    assert protected['aprobado']
    historical = read_json(OUT / 'preflight_documental_final/huellas_antecedentes.json')
    for source, result in historical.items():
        for row in result['archivos']:
            if row.get('igual_historico'):
                content = subprocess.check_output(['git', 'show', f"{row['commit_historico']}:{row['archivo']}"], cwd=ROOT)
                assert hashlib.sha256(content).hexdigest() == row['sha256_esperado']
            else:
                assert sha(ROOT / row['archivo']) == row['sha256_esperado']
    assert git('rev-parse', 'HEAD').strip() == prep['commit_partida']
    assert git('branch', '--show-current').strip() == prep['rama']
    for name, expected in prep['sha256_documentos'].items():
        if name.endswith('CONTINUIDAD_DIAGNOSTICO.md'):
            initial = read_json(OUT / 'preflight_documental_final/preflight.json')['documentos_preparacion']
            assert initial['aprobado']  # Antes de actualización propia; antecedente íntegro conservado.
        else:
            assert sha(ROOT / name) == expected
    return dict(aprobado=True, versionados_protegidos=protected['n'], head=prep['commit_partida'],
                rama=prep['rama'], fuentes_historicas_intactas=True)


def stability(changes, inputs, conf):
    rows = [dict(periodo='global_2019_2021_2025', intervalo='mixto_1_2', **distribution(changes.cambio_observado))]
    for year, sub in changes.groupby('anio', sort=True):
        rows.append(dict(periodo=str(year), intervalo=int(sub.intervalo.iloc[0]), **distribution(sub.cambio_observado)))
    write_csv('estabilidad_anual.csv', pd.DataFrame(rows))
    trajectory = changes[[*KEYS, 'departamento', 'anio_previo', 'intervalo', 'prom_punt_global',
                          'puntaje_previo', 'cambio_observado']].copy()
    trajectory['signo'] = np.sign(trajectory.cambio_observado).astype(int)
    write_csv('trayectorias_33.csv', trajectory)
    transitions = []
    for code, sub in trajectory.groupby('codigo_departamento', sort=True):
        records = sub.sort_values('anio').to_dict('records')
        for a, b in zip(records, records[1:]):
            transitions.append(dict(codigo_departamento=code, departamento=a['departamento'],
                                    anio_desde=int(a['anio']), anio_hasta=int(b['anio']),
                                    intervalo_desde=int(a['intervalo']), intervalo_hasta=int(b['intervalo']),
                                    cambio_desde=a['cambio_observado'], cambio_hasta=b['cambio_observado'],
                                    signo_desde=a['signo'], signo_hasta=b['signo'], cambia_signo=a['signo'] != b['signo']))
    tr = pd.DataFrame(transitions)
    write_csv('transiciones_signo.csv', tr)
    write_csv('transiciones_resumen.csv', tr.groupby(['anio_desde', 'anio_hasta', 'signo_desde', 'signo_hasta'],
                                                   as_index=False).size().rename(columns={'size': 'n_territorios'}))
    write_csv('estabilidad_territorial.csv', pd.DataFrame([
        dict(codigo_departamento=code, departamento=sub.departamento.iloc[0],
             **distribution(sub.cambio_observado)) for code, sub in changes.groupby('codigo_departamento')]))
    contrasts = []
    for window in conf['ventanas']:
        for internal in window['internas']:
            train = changes[changes.anio.isin(internal['entrenamiento'])]
            valid = changes[changes.anio == internal['validacion']]
            for variable in ['cambio_observado', *inputs]:
                a, b = distribution(train[variable]), distribution(valid[variable])
                row = dict(externo=window['externo'], validacion=internal['validacion'],
                           entrenamiento=json.dumps(internal['entrenamiento']), variable=variable,
                           intervalo_validacion=int(valid.intervalo.iloc[0]),
                           delta_mediana=b['mediana'] - a['mediana'], delta_iqr=b['iqr'] - a['iqr'])
                row.update({'train_' + k: v for k, v in a.items()})
                row.update({'valid_' + k: v for k, v in b.items()})
                contrasts.append(row)
    write_csv('contrastes_particiones_originales.csv', pd.DataFrame(contrasts))


def associations(changes, inputs):
    variation, target, redundant, exact_pairs = [], [], [], []
    periods = [('global', changes), *[(str(year), sub) for year, sub in changes.groupby('anio')]]
    for period, sub in periods:
        for name in inputs:
            a = sub[name].to_numpy(float)
            variation.append(dict(periodo=period, entrada=name, valores_unicos=np.unique(a).size,
                                  constante_exacta=bool(np.unique(a).size == 1), **distribution(a)))
            for method in ['pearson', 'spearman']:
                target.append(dict(periodo=period, entrada=name, metodo=method,
                                   **correlation(a, sub.cambio_observado, method)))
        for x, y in combinations(inputs, 2):
            same = bool(np.array_equal(sub[x].to_numpy(), sub[y].to_numpy()))
            exact_pairs.append(dict(periodo=period, entrada_x=x, entrada_y=y, n=len(sub), iguales_exactamente=same))
            for method in ['pearson', 'spearman']:
                redundant.append(dict(periodo=period, entrada_x=x, entrada_y=y, metodo=method,
                                      **correlation(sub[x], sub[y], method)))
    write_csv('variacion_entradas.csv', pd.DataFrame(variation))
    write_csv('asociaciones_objetivo.csv', pd.DataFrame(target))
    write_csv('asociaciones_entre_entradas.csv', pd.DataFrame(redundant))
    write_csv('redundancia_exacta.csv', pd.DataFrame(exact_pairs))


def audit_predictions(panel, conf):
    pilot = E2 / 'resultados/piloto'
    internal = csv(E2 / 'resultados/predicciones_internas.csv')
    external = csv(E2 / 'resultados/predicciones_externas.csv')
    cs = {c['id']: c for c in conf['configuraciones']}
    assert len(cs) == 36 and [c['orden'] for c in cs.values()] == list(range(36))
    assert len(internal) == 11880 and len(external) == 1155
    validate(internal, ['externo', 'id', *KEYS], finite_fields=['observado', 'puntaje_previo', 'anio_previo', 'cambio_predicho', 'prediccion', 'error'])
    validate(external, ['procedimiento', *KEYS], finite_fields=['observado', 'puntaje_previo', 'anio_previo', 'cambio_predicho', 'prediccion', 'error'])
    assert set(internal.id) == set(cs) and set(internal.anio) == {2021, 2022, 2023, 2024}
    context = read_json(pilot / 'contexto.json')
    oldenv = read_json(E2 / 'resultados/entorno.json')
    nowenv = environment()
    assert oldenv['python'] == nowenv['python'] and oldenv['paquetes'] == nowenv['paquetes']
    assert context['configuraciones'] == conf['configuraciones']
    assert context['entorno'] == oldenv
    signatures, metas = {}, []
    allparts, n_fits = [], 0
    for w in conf['ventanas']:
        for part in w['internas']:
            year, ext = part['validacion'], w['externo']
            train = panel[panel.anio.isin(part['entrenamiento'])].sort_values(KEYS).reset_index(drop=True)
            test = panel[panel.anio == year].sort_values(KEYS).reset_index(drop=True)
            for ident, c in cs.items():
                label = f'e{ext}_i{year}_{ident}'
                kind = 'persistencia' if ident == 'persistencia' else 'ajustes'
                base = pilot / kind / label
                path = base / ('calculo.json' if kind == 'persistencia' else 'ajuste.json')
                info = read_json(path)
                pred = csv(base / 'predicciones.csv')
                expected = internal[(internal.externo == ext) & (internal.id == ident) & (internal.anio == year)]
                assert len(expected) == 33 and pred.ajuste.eq(label).all() and pred.id.eq(ident).all()
                exact(pred.assign(externo=ext).reset_index(drop=True), expected.reset_index(drop=True))
                validate(pred, KEYS, test[KEYS], ['observado', 'puntaje_previo', 'cambio_predicho', 'prediccion', 'error'])
                for field, actual in [('observado', test.prom_punt_global), ('puntaje_previo', test.puntaje_previo),
                                      ('anio_previo', test.anio_previo), ('prediccion', pred.puntaje_previo + pred.cambio_predicho),
                                      ('error', pred.prediccion - pred.observado)]:
                    assert np.array_equal(pred[field].to_numpy(), actual.to_numpy())
                assert info['predicciones_sha256'] == sha(base / 'predicciones.csv')
                assert info['entradas_prediccion_sha256'] == sha(base / 'entradas_prediccion.csv')
                exact(csv(base / 'entradas_prediccion.csv'), test[[*KEYS, *c['entradas']]])
                sig = dict(configuracion=c, entrenamiento=part['entrenamiento'],
                           llaves=train[KEYS].values.tolist(), versiones=oldenv['paquetes'],
                           python=oldenv['python'], semilla=conf['semilla'])
                if kind == 'ajustes':
                    n_fits += 1
                    assert info['id'] == ident and info['estado'] == 'ok' and info['etiqueta'] == label
                    assert info['entrenamiento'] == part['entrenamiento'] and info['llaves_entrenamiento'] == train[KEYS].values.tolist()
                    assert info['n'] == len(train) and info['semilla'] == conf['semilla'] == SEED
                    assert info['parametros_completos'] == c['parametros_completos'] and info['entradas'] == c['entradas']
                    assert info['objetivo'] == 'cambio_observado' and info['origen'] == 'real'
                    assert info['datos_X_sha256'] == hashlib.sha256(train[c['entradas']].to_numpy(float).tobytes()).hexdigest()
                    assert info['datos_y_sha256'] == hashlib.sha256(train.cambio_observado.to_numpy(float).tobytes()).hexdigest()
                    assert info['panel_sha256'] == PANEL_SHA and info['entorno_sha256'] == sha(E2 / 'resultados/entorno.json')
                    assert info['congelacion_sha256'] == sha(E2 / 'resultados/congelacion_operativa.json')
                    assert info['modelo_sha256'] == sha(base / 'modelo.joblib')  # Bytes, nunca cargar.
                    assert info['entradas_entrenamiento_sha256'] == sha(base / 'entradas_entrenamiento.csv')
                    exact(csv(base / 'entradas_entrenamiento.csv'), train[[*KEYS, *c['entradas'], 'cambio_observado']])
                    sig['transformacion_ajustada'] = info['transformacion_ajustada']
                    sig['datos_X_sha256'] = info['datos_X_sha256']
                    sig['datos_y_sha256'] = info['datos_y_sha256']
                else:
                    assert info['ajustes'] == 0 and info['llaves'] == test[KEYS].values.tolist()
                    assert np.array_equal(pred.prediccion, pred.puntaje_previo) and pred.cambio_predicho.eq(0).all()
                signatures[(ext, ident, year)] = sig
                metas.append(dict(externo=ext, id=ident, anio=year, etiqueta=label,
                                  archivo_metadata=str(path.relative_to(ROOT)), metadata_sha256=sha(path),
                                  entrenamiento=json.dumps(part['entrenamiento']), n_train=len(train),
                                  n_valid=33, firma_linaje=hashlib.sha256(json.dumps(sig, sort_keys=True).encode()).hexdigest()))
                allparts.append(pred.assign(externo=ext))
    assert n_fits == 350 and len(allparts) == 360
    # Las fuentes internas concatenadas originales están conservadas en su orden original.
    reconstructed = pd.concat(allparts, ignore_index=True)
    exact(reconstructed.sort_values(['externo', 'id', *KEYS]).reset_index(drop=True),
          internal.sort_values(['externo', 'id', *KEYS]).reset_index(drop=True))
    unique, lineage = collapse(internal, signatures)
    assert len(unique) == 4752 and len(lineage) == 11880 and lineage.es_representante.sum() == 4752
    write_csv('auditoria_metadatos_copias.csv', pd.DataFrame(metas))
    write_csv('linaje_copias.csv', lineage)
    scores = csv(E2 / 'resultados/metricas_internas.csv')
    assert len(scores) == 144
    validate(scores, ['externo', 'id'], finite_fields=['mae', 'rmse'])
    checkrows = []
    role_ids = {}
    for w in conf['ventanas']:
        ext = w['externo']
        selpath = pilot / f'seleccion_{ext}.json'
        sel = read_json(selpath)
        assert sel['externo'] == ext
        if ext == 2021:
            assert not sel['metricas_internas'] and sel['global_id'] == 'persistencia'
        else:
            saved = sel['metricas_internas']
            assert len(saved) == 36 and [r['id'] for r in saved] == list(cs)
            assert scores[scores.externo == ext].id.tolist() == list(cs)
            for record in saved:
                q = internal[(internal.externo == ext) & (internal.id == record['id'])]
                assert record['estado'] == 'completo' and record['ventanas'] == [p['validacion'] for p in w['internas']]
                m = metrics(q)
                s = scores[(scores.externo == ext) & (scores.id == record['id'])].iloc[0]
                assert s.estado == record['estado'] and json.loads(s.ventanas) == record['ventanas']
                for key in ['mae', 'rmse']:
                    assert abs(m[key] - record[key]) <= 1e-12 and abs(m[key] - s[key]) <= 1e-12
                checkrows.append(dict(externo=ext, id=record['id'], n=len(q), mae=m['mae'], rmse=m['rmse'],
                                      mae_guardado=record['mae'], rmse_guardado=record['rmse'],
                                      diferencia_mae=m['mae']-record['mae'], diferencia_rmse=m['rmse']-record['rmse']))
        role_ids[ext] = {'global': sel['global_id'], **sel['especificaciones'], 'persistencia': 'persistencia'}
        assert set(role_ids[ext].values()) == {'persistencia'}
        assert set(external[external.anio == ext].procedimiento) == set(role_ids[ext])
        frozen_ext = csv(pilot / f'externas_{ext}.csv')
        exact(frozen_ext, external[external.anio == ext].reset_index(drop=True))
        test = panel[panel.anio == ext].sort_values(KEYS).reset_index(drop=True)
        for role, ident in role_ids[ext].items():
            q = external[(external.anio == ext) & (external.procedimiento == role)].reset_index(drop=True)
            validate(q, KEYS, test[KEYS], ['observado', 'prediccion', 'cambio_predicho'])
            assert len(q) == 33 and q.id.eq(ident).all() and q.seleccion_sha256.eq(sha(selpath)).all()
            assert np.array_equal(q.observado, test.prom_punt_global) and np.array_equal(q.puntaje_previo, test.puntaje_previo)
            assert np.array_equal(q.anio_previo, test.anio_previo)
            assert np.array_equal(q.prediccion, q.puntaje_previo + q.cambio_predicho)
            assert np.array_equal(q.error, q.prediccion - q.observado)
    assert external.groupby('procedimiento').size().eq(165).all() and external.procedimiento.nunique() == 7
    write_csv('cotejo_144_metricas_guardadas.csv', pd.DataFrame(checkrows))
    return paired(internal), paired(unique), paired(external), dict(
        aprobado=True, internos_originales=len(internal), internos_unicos=len(unique), linaje=len(lineage),
        candidatos=36, artefactos_internos=360, metadatos_ajustados=350, externas=len(external),
        procedimientos=7, metricas_internas=144, copias_iguales_exactamente=True,
        resumen_unico_representante='menor externo', modelos_deserializados=0, fits=0,
        max_diferencia_metricas=float(pd.DataFrame(checkrows)[['diferencia_mae', 'diferencia_rmse']].abs().to_numpy().max()))


def metrics_all(internal, unique, external, conf):
    byid = {c['id']: c for c in conf['configuraciones']}
    annual_rows = []
    for name, frame in [('internas_originales', internal), ('internas_unicas', unique), ('externas', external)]:
        write_csv('errores_' + name + '.csv', frame)
        rows = []
        groups = ['externo', 'id'] if name == 'internas_originales' else ['id'] if name == 'internas_unicas' else ['procedimiento', 'id']
        for values, sub in frame.groupby(groups, sort=True, dropna=False):
            if not isinstance(values, tuple):
                values = (values,)
            meta = dict(zip(groups, values))
            c = byid[meta['id']]
            meta.update(familia=c['familia'], grupo=c['especificacion'] or 'comparador_todos_grupos')
            # No pooling de configuraciones ni copias entre ventanas.
            slices = [('total', sub), *[('anio_' + str(y), q) for y, q in sub.groupby('anio')],
                      *[('territorio_' + code, q) for code, q in sub.groupby('codigo_departamento')]]
            if name == 'externas':
                slices.extend([('2021_2024', sub[sub.anio <= 2024]), ('2025', sub[sub.anio == 2025])])
            for period, q in slices:
                row = dict(**meta, periodo=period, anios=json.dumps(sorted(q.anio.unique().tolist())), **metrics(q))
                rows.append(row)
                if period.startswith('anio_'):
                    annual_rows.append(dict(conjunto=name, **row))
        write_csv('metricas_' + name + '.csv', pd.DataFrame(rows))
    write_csv('errores_anuales_candidato_familia_grupo.csv', pd.DataFrame(annual_rows))
    # Mínimos descriptivos internos por familia/grupo, sin elegir nueva configuración.
    originals = csv(TABLES / 'metricas_internas_originales.csv')
    retrospectives = []
    for (ext, family, group), sub in originals[originals.periodo == 'total'].groupby(['externo', 'familia', 'grupo']):
        minimum = sub.mae.min()
        retrospectives.append(dict(externo=int(ext), familia=family, grupo=group, n_configuraciones=len(sub),
                                   n_por_configuracion=int(sub.n.iloc[0]), minimo_mae_retrospectivo=minimum,
                                   mae_persistencia=float(sub.mae_persistencia.iloc[0]),
                                   delta_minimo_retrospectivo=minimum-float(sub.mae_persistencia.iloc[0]),
                                   ids_empatados=json.dumps(sub[sub.mae == minimum].id.tolist()),
                                   uso='Descripción retrospectiva interna; NO nuevo ganador/selección'))
    write_csv('minimos_internos_retrospectivos.csv', pd.DataFrame(retrospectives))


def arithmetic_audit():
    # Aritmética independiente con racionales de los errores IEEE exactos.
    from fractions import Fraction
    rows = []
    for name in ['internas_originales', 'internas_unicas', 'externas']:
        f = csv(TABLES / f'errores_{name}.csv')
        groups = ['externo', 'id'] if name == 'internas_originales' else ['id'] if name == 'internas_unicas' else ['procedimiento', 'id']
        for values, sub in f.groupby(groups):
            errors = [Fraction.from_float(float(p)-float(o)) for p, o in zip(sub.prediccion, sub.observado)]
            n = len(errors)
            independent = dict(mae=float(sum(map(abs, errors), Fraction())/n),
                               rmse=math.sqrt(float(sum((e*e for e in errors), Fraction())/n)),
                               sesgo=float(sum(errors, Fraction())/n))
            m = metrics(sub)
            diffs = {k: abs(independent[k]-m[k]) for k in independent}
            assert max(diffs.values()) <= 1e-12
            rows.append(dict(conjunto=name, grupo=str(values), n=n, **{'diferencia_' + k: v for k, v in diffs.items()}))
    write_csv('auditoria_aritmetica_independiente.csv', pd.DataFrame(rows))
    return dict(aprobado=True, grupos=len(rows), procedimiento='Fraction.from_float(error IEEE); sumas racionales exactas; raíz final', atol=1e-12)


def plots(changes):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    years = sorted(changes.anio.unique())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot([changes[changes.anio == year].cambio_observado for year in years], tick_labels=years)
    ax.axhline(0, color='gray', linewidth=.8)
    ax.set(title='Cambio observado por año: 33 territorios por año; n total=198', xlabel='Año observado (2021: previo 2019; intervalo 2)', ylabel='Cambio del puntaje global (puntos; sin anualizar)')
    fig.tight_layout(); fig.savefig(destination(FIGS / '01_distribuciones_anuales.png'), dpi=160); plt.close(fig)
    pivot = changes.pivot(index='codigo_departamento', columns='anio', values='cambio_observado')
    labels = changes.drop_duplicates('codigo_departamento').set_index('codigo_departamento').departamento
    fig, ax = plt.subplots(figsize=(10, 11))
    lim = abs(pivot.to_numpy()).max()
    im = ax.imshow(pivot, aspect='auto', cmap='RdBu_r', vmin=-lim, vmax=lim)
    ax.set_xticks(range(6), pivot.columns)
    ax.set_yticks(range(33), [f'{c} {labels[c]}' for c in pivot.index])
    ax.set(title='Trayectorias: 33 territorios × 6 cambios; n=198', xlabel='Año; 2021 tiene intervalo 2 sin anualizar')
    fig.colorbar(im, ax=ax, label='Cambio observado (puntos)')
    fig.tight_layout(); fig.savefig(destination(FIGS / '02_trayectorias_33.png'), dpi=160); plt.close(fig)
    contrasts = csv(TABLES / 'contrastes_particiones_originales.csv')
    c = contrasts[contrasts.variable == 'cambio_observado']
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(c))
    ax.bar(x-.18, c.train_mediana, .36, label='Mediana entrenamiento')
    ax.bar(x+.18, c.valid_mediana, .36, label='Mediana validación')
    ax.set_xticks(x, [f'e{r.externo}/v{r.validacion}\ntrain n={r.train_n}; val n=33' for r in c.itertuples()], rotation=45, ha='right')
    ax.axhline(0, color='gray', linewidth=.8); ax.legend()
    ax.set(title='10 particiones originales; solo 4 años de validación únicos', ylabel='Cambio observado (puntos)', xlabel='Ventana externa/validación; copias conservadas')
    fig.tight_layout(); fig.savefig(destination(FIGS / '03_contrastes_particiones.png'), dpi=160); plt.close(fig)
    assoc = csv(TABLES / 'asociaciones_objetivo.csv')
    a = assoc[(assoc.metodo == 'spearman') & (assoc.periodo != 'global')].pivot(index='entrada', columns='periodo', values='correlacion')
    fig, ax = plt.subplots(figsize=(13, 8))
    im = ax.imshow(a, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    ax.set_xticks(range(6), a.columns); ax.set_yticks(range(18), a.index)
    ax.set(title='Spearman descriptivo con cambio observado: n=33 por celda', xlabel='Año; rangos medios; asociación no equivale a capacidad predictiva')
    fig.colorbar(im, ax=ax, label='Correlación (sin unidades; vacío si indefinida)')
    fig.tight_layout(); fig.savefig(destination(FIGS / '04_asociaciones_anuales.png'), dpi=160); plt.close(fig)
    errs = csv(TABLES / 'metricas_internas_unicas.csv')
    a = errs[errs.periodo.str.startswith('anio_')]
    fig, axes = plt.subplots(1, 4, figsize=(14, 5), sharey=True)
    for ax, year in zip(axes, range(2021, 2025)):
        sub = a[a.periodo == f'anio_{year}']
        fams = ['mediana', 'boosting_absoluto']
        ax.boxplot([sub[sub.familia == f].delta_mae_pareado for f in fams], tick_labels=['Mediana\n15configs', 'Boosting\n20configs'])
        ax.axhline(0, color='gray', linewidth=.8); ax.set_title(f'{year}: 33pares/configuración')
    axes[0].set_ylabel('MAE candidato − MAE persistencia (puntos)')
    fig.suptitle('Errores internos únicos: distribución entre configuraciones; retrospectivo, sin nueva selección')
    fig.tight_layout(); fig.savefig(destination(FIGS / '05_deltas_internos.png'), dpi=160); plt.close(fig)


def main():
    if (OUT / 'auditoria_diagnostico.json').exists() or TABLES.exists():
        raise RuntimeError('No sobrescribir resultados; investigar/reanudar explícitamente')
    env = environment()
    write_json(OUT / 'entorno_diagnostico.json', env)
    documentary = verify_documental()
    panel, changes, conf, inputs = load_panel()
    write_json(OUT / 'preflight_actual.json', dict(documental=documentary, reconstruccion_exacta=True,
        filas=231, territorios=33, cambios=198, fuente_sha256=SOURCE_SHA, derivado_sha256=PANEL_SHA,
        entradas_union_exacta=inputs, fuente_unica=True, previo_2021=2019, anualizado=False))
    # Linaje se comprueba antes de cualquier síntesis estadística de copias.
    internal, unique, external, audit = audit_predictions(panel, conf)
    stability(changes, inputs, conf)
    associations(changes, inputs)
    metrics_all(internal, unique, external, conf)
    arith = arithmetic_audit()
    plots(changes)
    write_json(OUT / 'auditoria_diagnostico.json', dict(**audit, aritmetica=arith,
        reconstruccion_panel_exacta=True, no_pseudorepeticion=True, analisis_original_por_ventana_conservado=True,
        nuevas_externas_no_seleccionadas=0, selecciones_originales_intactas=True,
        entorno_verificado=True, analisis='A–D ejecutados; E documental y cierre pendientes'))
    print(json.dumps(dict(auditoria=audit, aritmetica=arith, tablas=len(list(TABLES.glob('*.csv'))), graficos=5), ensure_ascii=False))


if __name__ == '__main__':
    main()
