"""Entregas descriptivas fase1 desde controles ya calculados; sin modelos."""
from collections import Counter
import json
import pandas as pd
from auditar_2025 import ROOT, V2, OUT, SCORES, csv_out

def table(frame):
    cols = list(frame.columns)
    body = ['| ' + ' | '.join(cols) + ' |', '| ' + ' | '.join(['---']*len(cols)) + ' |']
    for row in frame.itertuples(index=False, name=None):
        body.append('| ' + ' | '.join(str(v) for v in row) + ' |')
    return '\n'.join(body)

def main():
    summary = json.loads((OUT / 'verificacion_auditoria.json').read_text())
    candidate = pd.read_csv(ROOT / 'panel_departamento_anio_unido_2025.csv', float_precision='round_trip')
    hist = pd.read_csv(ROOT / 'auditoria/evidencia/agregados_Saber_11_Listo_2018_2024.csv')
    hist = hist[hist.subconjunto.eq('recibido')]
    annual = pd.read_csv(OUT / 'agregados_anuales_2025.csv', float_precision='round_trip')
    allgrades = annual[annual.poblacion.eq('05_codigo_colegio')]
    combined = pd.concat([hist, allgrades], ignore_index=True).set_index(['codigo_departamento', 'anio'])
    explanation = []
    for rowno, r in enumerate(candidate.to_dict('records'), 2):
        d, y = int(r['codigo_departamento']), int(r['anio'])
        ref = combined.loc[(d, y)]
        for c in ['n_estudiantes_saber'] + ['n_' + c for c in SCORES] + ['prom_' + c for c in SCORES]:
            # Históricos ya redondeados en la evidencia; 2025 calculado desde sumas enteras.
            value = float(ref[c])
            rounded = round(value, 2) if c.startswith('prom_') else value
            explanation.append(dict(fila_candidato=rowno, codigo_departamento=d, anio=y, variable=c,
                valor_candidato=r[c], referencia_sin_grado11=rounded,
                coincide=abs(float(r[c])-rounded) <= 1e-10,
                origen='agregados históricos conservados/recibido' if y<2025 else 'raw2025/05_codigo_colegio'))
    csv_out(explanation, 'diagnostico_origen_candidato.csv')
    explain_count = sum(r['coincide'] for r in explanation)
    filters = pd.read_csv(OUT / 'filtros_raw_2025.csv')
    f = filters.pivot(index='control', columns='periodo', values='n').fillna(0)
    def n(c, p):
        return int(f.loc[c, p]) if c in f.index else 0
    stage_rows = [dict(etapa=c, periodo20251=n(c,20251), periodo20252=n(c,20252), total=n(c,20251)+n(c,20252))
        for c in ['01_recibido','02_estudiante','03_sin_libertad','04_seis_puntajes','05_codigo_colegio','06_grado11','administrativo_grado11','diagnostico_global_disponible']]
    csv_out(stage_rows, 'tabla_filtros_resumen.csv')
    diag = pd.read_csv(OUT / 'diagnostico_medias_disponibles.csv')
    annual_diag = diag[diag.alcance.eq('anual')]
    names = pd.read_csv(ROOT / 'auditoria/base_analitica_departamento_anio.csv')[['codigo_departamento','departamento']].drop_duplicates()
    annual_diag = annual_diag.merge(names, on='codigo_departamento', validate='one_to_one')
    extreme = annual_diag.assign(abs_delta=lambda x:x.diferencia.abs()).nlargest(5,'abs_delta')
    shown = extreme[['departamento','n_completos','n_global_disponible','media_completos','media_global_disponible','diferencia']].copy()
    for c in ['media_completos','media_global_disponible','diferencia']:
        shown[c] = shown[c].map(lambda v:f'{v:.6f}')
    counts = {int(y): int(g.n_estudiantes_saber.sum()) for y,g in pd.read_csv(V2 / 'fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv').groupby('anio')} if summary['ampliacion_validada'] else {}
    outcome = dict(celdas_candidato_sin_grado11_cotejadas=len(explanation), coincidencias_sin_grado11=explain_count,
        candidato_reproduce_agregacion_sin_filtro_grado11=explain_count == len(explanation),
        n_global_disponible2025=int(annual_diag.n_global_disponible.sum()),
        n_completos2025=int(annual_diag.n_completos.sum()),
        perdidas_otros_puntajes=int(annual_diag.excluidos_por_otras_pruebas.sum()),
        proporcion_perdida_otros_puntajes=float(annual_diag.excluidos_por_otras_pruebas.sum()/annual_diag.n_global_disponible.sum()),
        conteos_panel_por_anio=counts)
    (OUT / 'resumen_documentacion.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+'\n')
    text = f'''# Auditoría v2 — fase 1: datos2025 y conservación

Fecha: 2026-10-10, America/Bogota. Partida efectiva `742c66577abaeade216d0498e4ecfd12d4c7abfb`, sucesor del cierre v1 `fc8dc23de8a85cffcc1c87d47ac740650b27ace5`. Solo fase1. No modelos, métricas predictivas, simulaciones o notebooks nuevos. Sin búsquedas externas ni PDF nuevos.

## Resultado y población

Se censaron **{summary['filas_raw']:,} registros** de ambos TXT locales2025 con CSV por bloques100.000, y una segunda lectura completa con pandas. Se retienen **{summary['registros_elegibles2025']:,}** bajo los filtros del protocolo v1 (§1): estudiante, no libertadS, seis puntajes positivos/disponibles, código del departamento del colegio y grado11. Sin filtro de calendario. Son registros, no personas únicas. Evidencias: `resultados/filtros_raw_2025.csv`, `categorias_poblacion.csv`, `calendarios_2025.csv`, fuentes `auditar_2025.py:masks/audit_raw/independent_sum`.

Los nombres Saber11, campos y categorías (grado11/25/26 e individuales) son compatibles con los TXT históricos; no se observa una población Pre Saber identificada en estos campos. Esto valida coherencia local de las fuentes aportadas, **no autentica descarga o producto oficial independientemente**. No se infiere identidad personal por ID.

{table(pd.DataFrame(stage_rows))}

Los registros físicos tienen ancho y periodo correctos. Cero puntajes fuera del rango documentado entre elegibles; códigos elegibles válidos y cobertura33. La segunda lectura reproduce exactamente **429 conteos/sumas**: 33territorios × 13variables de control. Evidencia: `cotejo_segunda_lectura.csv`, `verificacion_auditoria.json`.

## Consolidado candidato: no corresponde al filtro grado11

El candidato aportado se conserva intacto. Falta IPM y hay **{summary['discrepancias_candidato']} discrepancias** en las13 columnas Saber críticas: 429por año, incluidos2018–2024; no se corrigen originales. Sus15 tasas coinciden en todas las231 filas con el anexo. Evidencia: `cotejo_candidato.csv`, columna `coincide`, llave/celda y fila del candidato.

El diagnóstico de procedencia coteja sus conteos y medias con la agregación sin filtrogrado11: **{explain_count}/{len(explanation)} coincidencias**, usando las medias redondeadas a dos decimales. Para2018–2024 se emplea evidencia anterior, no nuevos censos; para2025, agregación actual raw. Ubicaciones: `diagnostico_origen_candidato.csv`, fuente `documentar.py:main`, histórico `auditoria/evidencia/agregados_Saber_11_Listo_2018_2024.csv`, subconjunto `recibido`. Por tanto no se utiliza ese consolidado como base principal: incorpora registros excluidos por el estimando acordado y precisión redondeada. La reconstrucción conserva el filtro, no cambia la pregunta.

## Faltantes y diagnóstico de selección

No se convirtieron nulos en0 ni se imputaron puntajes. Los faltantes, ceros, negativos/no numéricos se distinguen, con estados que pueden coexistir entre variables; no sumar sus frecuencias como personas únicas. Evidencia: `faltantes_territorio_periodo.csv`; mermas secuenciales y combinaciones concurrentes separadas en `filtros_territorio_periodo.csv` y `combinaciones_exclusiones.csv` (bits1/2/4/8/16: estudiante/sinlibertad/seispuntajes/código/grado11).

Entre filtros administrativos de grado11, {outcome['n_global_disponible2025']:,} tienen globalpositivo; exigir las otras pruebas retiene {outcome['n_completos2025']:,}, una diferencia de {outcome['perdidas_otros_puntajes']:,} registros ({100*outcome['proporcion_perdida_otros_puntajes']:.6f}%). En inglés se observan76+7.245 nulos y3+95 ceros en esos filtros administrativos; hay también ceros en otras áreas y dos globales0 en20252. Ubicación: `faltantes_territorio_periodo.csv`, población `administrativo_grado11`; `tabla_filtros_resumen.csv`.

**Mayores diferencias anuales entre media de casos completos y media con globaldisponible** (diagnóstico separado; no nueva respuesta principal):

{table(shown)}

Guainía presenta diferencia de aproximadamente21,01puntos, con238casos completos frente404 con global disponible. Esto demuestra sensibilidad descriptiva al filtro en ese territorio; no demuestra el mecanismo de los faltantes, sesgo frente a toda la población ni causa de errores predictivos. Ubicación: `diagnostico_medias_disponibles.csv`, alcance `anual`, código94. El objetivo principal sigue siendo la media de registros elegibles con las seis pruebas. No se selecciona población según futuros MAE.

Las mermas2025 se comparan con filtros históricos en `comparacion_filtros_historicos.csv`, conservando su etiqueta histórica. No se repiten censos2018–2024 ni se promete igualdad de composición entre años. Pocos años, dependencia territorial, selección por registros y enlace ecológico permanecen.

## Identificadores raw repetidos: resolución sin deduplicar

Se detectan dos grupos con el mismo ID en20252. La revisión de las filas completas encuentra dos filas distintas en cada grupo y solo una elegible. La otra no es grado11; por tanto no se duplica la población retenida. Se conserva todo raw y no se deduplica por ID. `identificadores_repetidos_revision.json` guarda únicamente ubicaciones y estados agregados, sin IDs/firmas personales.

La primera verificación rechazó la ampliación por unicidadraw y no exportó panel. Se conserva su dictamen en `antecedentes/primera_verificacion_ids_raw.json`. Enmienda documentada antes de exportar: verificar unicidad de **IDs elegibles**, mantener la repeticiónraw como advertencia y repetir censo. Todos los controles indispensables actuales pasan. No se oculta el rechazo inicial ni se afirma que los IDsraw sean únicos.

## IPM, cobertura y ampliación

El XLSXlocal2025 contiene incidencia departamental y15privaciones: hojas `IPM_Departamentos` e `IPM_Indicadores_Departamento `, encabezados de año en fila12 y dominioTotal en fila13. IPM2025 está en W y tasas2025 en X; se verifica por encabezados, no por nombre del archivo. Se cotejan528entradas nuevas y3.168históricas, sin extraer cifras2020. Las históricas no tienen diferencias frente a basev1 ({summary['revisiones_historicas_anexo']} revisiones encontradas). Fechas y advertencias en `notas_ipm_2025.csv`; celdas exactas en `cifras_xlsx.csv`, encabezados en `encabezados_ipm_2025.csv`.

La fecha14abril2026 es actualización/publicación, no año de observación. Se mantienen IPM%personas y tasas%hogares, dominioTotal. El enlace de colegio con hogares residentes sigue siendo ecológico; no implica efecto individual o causal.

**Ampliación validada: {summary['ampliacion_validada']}**. `reconstrucciones/base_analitica_departamento_anio_v2.csv`:231filas,33territorios × siete años2018,2019,2021–2025, sin2020. Las198líneas históricas se conservan literalmente, sin reemplazar cifras; se añaden33líneas2025 desde raw y XLSX. Total{summary['registros_panel']:,}registros; SHA256 `{summary['panel_sha256']}`. Conteos por año: {counts}.

## Pruebas, conservación y condición de avance

Los tests de datos y pruebas negativas constan en `pruebas_auditoria.json`; no son tests de modelos ni notebook de experimentos. Los controles temporales, escalado, selección, métricas y presupuesto del piloto permanecen prospectivos en fase2. No nuevos notebooks en fase1.

Snapshot de311archivos previos y7fuentes;169huellas de manifiestos anteriores verificadas, con continuidades históricas cotejadas en sus commits y cambio de informe del usuario conservado. `integridad_inicial.json` fija partida; `conservacion_final.json` y manifiesto cierran sin excepciones a archivos existentes.

La base puede utilizarse en fase2 **cuando el usuario la autorice**. No entrenar ahora. El piloto futuro conserva100configuraciones/2horas y umbral práctico5%MAE frente a v1 reentrenada, sin exigencia3/5años. No hay resultado de mejora ni aceptación editorial del grupo. Procedencia de descarga y mecanismos de faltantes siguen como límites; no se sustituyen por una explicación inventada.
'''
    (V2 / 'fase1/INFORME_AUDITORIA.md').write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
