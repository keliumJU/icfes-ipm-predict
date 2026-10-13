"""Diseño documental autorizado; stdlib, sin estimadores, fits, métricas o notebooks.

Preserva íntegro el diagnóstico cerrado, incluso su continuidad no versionada.
El parámetro temporal se PROPONE antes de cualquier evaluación nueva. Los prompts
guardados exigen autorización separada y nunca se ejecutan desde este generador.
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OWN = ROOT / 'diseno_temporal_objetivo3_v1'
DIAG = ROOT / 'diagnostico_objetivo3_v1'
V5 = ROOT / 'experimentos_objetivo3_v5'
SOURCE = ROOT / 'experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv'
PANEL = V5 / 'etapa1/reconstrucciones/panel_cambios.csv'
CONFIG = V5 / 'etapa1/resultados/configuraciones_congeladas.json'
EXPECTED_HEAD = '75c3a25182af363f47b0d743820f99084e18fed5'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for b in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def read(path):
    return json.loads(Path(path).read_text())


def destination(relative):
    p = OWN / relative
    if not p.resolve().is_relative_to(OWN.resolve()):
        raise ValueError('Destino fuera de diseño propio')
    for q in [p, *p.parents]:
        if q == ROOT:
            break
        if q.is_symlink():
            raise ValueError('Symlink prohibido')
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def save(name, value):
    with destination(name).open('x') as stream:
        if isinstance(value, str):
            stream.write(value)
        else:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n')


def check_hashes(mapping):
    bad = [n for n, h in mapping.items() if not (ROOT / n).is_file() or sha(ROOT / n) != h]
    if bad:
        raise RuntimeError(f'Integridad irresuelta: {bad[:5]}')


def verify():
    m = read(OWN / 'resultados/manifiesto_diseno.json')
    check_hashes(m['entregables_sha256'])
    p = read(OWN / 'resultados/partida.json')
    check_hashes(p['protegidos_sha256'])
    assert git('rev-parse', 'HEAD') == p['head']
    assert git('branch', '--show-current') == p['rama']
    assert read(OWN / 'ESPECIFICACION_PROPUESTA.json')['estado'] == 'PROPUESTA DOCUMENTAL; NO ejecución autorizada'
    assert read(OWN / 'resultados/aceptacion_diseno.json')['fits'] == 0
    return dict(aprobado=True, entregables=len(m['entregables_sha256']),
                protegidos=len(p['protegidos_sha256']), head=p['head'],
                modo='Solo lectura documental', fits=0, modelos_cargados=0,
                protocolo_operativo_congelado=False, piloto_autorizado=False, commits=0, push=False)


def main():
    if '--verificar' in sys.argv:
        print(json.dumps(verify(), ensure_ascii=False))
        return
    if (OWN / 'resultados/partida.json').exists():
        raise RuntimeError('No sobrescribir diseño existente')
    prep = read(DIAG / 'REGISTRO_PREPARACION.json')
    frozen = read(DIAG / 'fase1/resultados/manifiesto_cierre.json')
    check_hashes(prep['inventario_protegido']['sha256_versionados'])
    check_hashes(frozen['entregables_sha256'])
    assert git('rev-parse', 'HEAD') == EXPECTED_HEAD
    assert git('show', '-s', '--format=%s', 'HEAD') == 'etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora'
    assert git('branch', '--show-current') == 'codex/objetivo3-v5-mae'
    subprocess.run(['git', 'merge-base', '--is-ancestor', EXPECTED_HEAD, 'HEAD'], cwd=ROOT, check=True)
    previous = {str(p.relative_to(ROOT)): sha(p) for p in sorted(DIAG.rglob('*')) if p.is_file()}
    protected = {**prep['inventario_protegido']['sha256_versionados'], **previous}
    configs = read(CONFIG)
    assert len(configs['configuraciones']) == 36 and configs['semilla'] == 20261010
    with SOURCE.open() as stream:
        rows = list(csv.DictReader(stream))
    normalized = [(r['codigo_departamento'].zfill(2), int(r['anio'])) for r in rows]
    years = dict(sorted(collections.Counter(y for _, y in normalized).items()))
    assert len(normalized) == len(set(normalized)) == 231
    assert len(set(c for c, _ in normalized)) == 33
    assert years == {2018:33, 2019:33, 2021:33, 2022:33, 2023:33, 2024:33, 2025:33}
    save('resultados/partida.json', dict(fecha_cliente='2026-10-11', timezone='America/Bogota',
        autorizacion_usuario='genial, procede: fase de diseño de protocolo, todavía sin entrenar',
        alcance='Documentos/configuración propuesta/evidencia/continuidad propia;sin implementación de estimadores',
        carpeta_previa='Inexistente antes de esta sesión;fuente generadora propia creada primero',
        head=EXPECTED_HEAD, asunto=git('show','-s','--format=%s','HEAD'), rama=git('branch','--show-current'),
        trabajo_posterior=git('log','--format=%H %s',f'{EXPECTED_HEAD}..HEAD'),
        status_inicial=git('status','--porcelain','--untracked-files=all').splitlines(),
        protegidos_sha256=protected, versionados_protegidos=29640, diagnostico_protegido=len(previous),
        fuente_unica_sha256=sha(SOURCE), derivado_sha256=sha(PANEL), configuraciones_v5_sha256=sha(CONFIG),
        lectura_fuente='Solo inventario completo de años/llaves;no estadísticas ni nuevos resultados predictivos',
        pdf_paginas=0, fits=0, modelos_cargados=0))
    specification = dict(version='1.0.0', estado='PROPUESTA DOCUMENTAL; NO ejecución autorizada',
        objetivo='Contrastar ponderación temporal de entrenamiento frente procedimiento uniforme v5 y persistencia',
        fecha_cliente='2026-10-11',
        procedimiento_primario=dict(esquema='recencia_h2', procedimiento='global',
                                   seleccionado_antes_externo=True, no_rescate_retrospectivo=True),
        recencia=dict(semivida_anios_calendario=2.0, ancla='máximo año del entrenamiento recibido',
                     peso_bruto='2 ** (-(max(anios_train)-anio_fila)/2.0)',
                     peso_normalizado='n_train * peso_bruto / math.fsum(pesos_brutos)',
                     normalizacion='media1;calcular SOLO con train y en orden de llaves congelado',
                     todos_positivos=True, no_eliminar_anios=True,
                     validacion_y_externas_ponderadas=False, peso_igual_territorio_dentro_anio=True,
                     parametros_busqueda=[], origen_semivida='Decisión nueva de diseño para contraste único;no optimizada con MAE nuevo ni afirmada óptima',
                     pesos_uniformes='Vector exactamente1;usar ruta de fit original sin sample_weight en todos pasos'),
        heredado=dict(configuracion_archivo=str(CONFIG.relative_to(ROOT)), configuracion_sha256=sha(CONFIG),
                      fuente_archivo=str(SOURCE.relative_to(ROOT)), fuente_sha256=sha(SOURCE),
                      derivado_archivo=str(PANEL.relative_to(ROOT)), derivado_sha256=sha(PANEL),
                      grupos=configs['grupos'], candidatos=configs['configuraciones'], ventanas=configs['ventanas'],
                      orden_familias=configs['orden_familias'], semilla=configs['semilla'],
                      bandas=dict(mae=0.1, rmse=0.1), entradas_sin_modificacion=True),
        aplicacion=dict(mediana=['escalado__sample_weight=w','modelo__sample_weight=w'],
                        boosting_absoluto=['sample_weight=w'], persistencia='Sin estimador/fit/pesos aprendidos',
                        escalado='Media/varianza ponderadas SOLOtrain;sin escalado de objetivo',
                        metadata_routing='Desactivar routing automático;usar parámetros explícitos por paso',
                        anio='Metadata para pesos;no agregar columna al X ni modelo'),
        referencias=dict(uniforme_global='CSV guardado v5,procedimiento=global,n165;sin nuevos fits ni modelos cargados',
                         persistencia='Previo independiente y CSVv3,165llaves/observados iguales',
                         v5_global_equivale_persistencia=True),
        evaluacion=dict(anios=[2021,2022,2023,2024,2025], territorios=33, pares_primarios=165,
                        externas_recencia=1155, internas_originales_esperadas=11880,
                        internas_unicas_condicionadas=4752, registros_internos=144,
                        pesos='Igual peso territorio-año en todas métricas/selección/meta',
                        meta_formula='100*(MAE_persistencia-MAE_recencia_global)/MAE_persistencia >= 5',
                        meta_porcentaje=5, referencia_historica_mae=3.429267191379531,
                        contraste_temporal='MAE_recencia_global-MAE_v5_global;pareado,sin umbral nuevo de éxito',
                        confirmacion_independiente=False, uso='Exploratorio:todos2021–2025ya vistos'),
        presupuesto_futuro=dict(segundos=7200, saldo_nuevo=True, saldo_previo_reutilizable=False,
                                cota_sin_fallos=dict(internos=350, externos_maximos=24, repeticiones_maximas=4, total=378),
                                controles_uniformidad='Inventados en fase1;sin nuevosfits reales de control',
                                persistencia_fuera_tiempo_fits=True),
        futuras_autorizaciones=['Fase1 implementación/controles inventados/congelación,sin fits reales',
                                'Fase2 piloto recencia36/auditoría/cierre,solo después de fase1 y autorización separada'],
        fuentes_extra_autorizadas=False, historia_nueva_autorizada=False, modelos_ajustados_ahora=0)
    save('ESPECIFICACION_PROPUESTA.json', specification)
    save('PLAN_DISENO.md', """# Plan de diseño temporal — fase documental autorizada

Versión 1.0; fecha 2026-10-11, America/Bogota. El usuario autorizó preparar el
protocolo, sin entrenar, después del diagnóstico objetivo3 v1. No existía
continuidad ni carpeta de este diseño: se comenzó con inventario.

## 1. Fase actual: diseño y evidencia

Verificar AGENTS, continuidad y cierre del diagnóstico, protocolo v5 5.0.0,
fuente única, configuraciones y Git. Preservar tanto los 29.640 versionados como
todos los archivos no versionados del diagnóstico, incluida su continuidad.
Leer únicamente la evidencia necesaria; no reabrir antecedentes archivados.

## 2. Entregables de esta fase

PROTOCOLO_TEMPORAL.md; ESPECIFICACION_PROPUESTA.json; evidencia, decisiones,
inventario de historia/evaluación; README; dos prompts futuros separados y
guardados sin ejecutar; continuidad propia; registro, conservación y manifiesto.
Fuentes Python documentales y validación de referencias/configuración/cobertura.
No notebook necesario para esta fase estrictamente documental. No implementar
estimadores, generar pesos sobre el panel, ajustes, predicciones o métricas nuevas.

## 3. Aceptación y límite

Propuesta concreta que aísle recencia, decisiones materiales explicitadas antes
de futuros resultados; meta/población/objetivo/evaluación originales conservados;
incertidumbre y falta de años inéditos declaradas; rutas y evidencias verificables;
diagnóstico y v1–v5 intactos; prompts no ejecutados; continuidad propia actualizada.
La aceptación documental no autoriza implementación, congelación operativa o piloto.
Fases futuras se describen en documentos separados, no se ejecutan aquí.
Sin commit/push, instalaciones, descargas, nuevas fuentes, causalidad o promesa de mejora.
""")
    save('PROTOCOLO_TEMPORAL.md', """# Protocolo temporal propuesto 1.0.0 — recencia frente a historia uniforme

Fecha: 2026-10-11, America/Bogota. **Diseño documental completo; ejecución no
autorizada.** No es etapa3 v5 ni una excepción a su meta no satisfecha. El usuario
autorizó esta fase de diseño, todavía sin entrenar. Este protocolo es una propuesta
revisable; la implementación y el piloto requieren autorizaciones separadas.

## 1. Pregunta y evidencia que la motiva

¿Cambiar únicamente los pesos temporales del entrenamiento, conservando el
procedimiento de selección y evaluación de v5, mejora el MAE global frente a su
procedimiento uniforme y a persistencia?

El diagnóstico cerrado muestra cambios de distribución entre años y errores
concentrados de forma distinta: 0 de 35 configuraciones ajustadas superan
persistencia en 2021/2022/2023 por separado, y 33 de 35 en 2024. Ninguna mejora
el conjunto interno único. Esto motiva una comparación temporal, no establece
que recencia funcione, que 2019 deba eliminarse o que falte señal intrínseca.

Evidencia: `diagnostico_objetivo3_v1/fase1/tablas/matriz_hipotesis.csv`, H1/H5/H6/H7;
`conteos_ventaja_interna_por_anio.csv`, cuatro filas; `contrastes_particiones_originales.csv`,
variable=cambio_observado. Rutas completas, huellas y límites en EVIDENCIA_Y_DECISIONES.md.

## 2. Decisiones heredadas que se conservan

- Población ESTUDIANTE; no libertad S; grado 11; seis puntajes presentes y positivos;
  sin filtro de calendario; media global recibida, sin recalcular ni redondear.
- Geografía del colegio, no residencia; conteos únicamente para trazabilidad.
- Fuente única v2: `experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv`;
  SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
- Derivado v5: `experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv`;
  SHA256 `aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc`.
- 231 filas, 33 territorios; 2018 solo historial; 198 cambios; 2020 excluido;
  previo = máximo año anterior del mismo territorio; 2021 compara 2019.
- Cambio observado en puntos originales, sin anualizar el intervalo 2019–2021;
  reconstrucción = puntaje previo + cambio predicho; negativos válidos.
- Mismos 36 candidatos, grupos, entradas, orden, parámetros y defaults completos v5:
  1 persistencia, 15 regresiones de mediana, 20 boosting absoluto. Sin nuevas familias,
  variables, filtros, eliminación de años/territorios, PCA, imputación o clipping.
- Semilla 20261010; particiones originales y selección por MAE/RMSE con bandas 0.1,
  menos entradas ajustadas, familia y orden JSON. Persistencia cuenta 0; demás todas
  sus entradas, aunque algún coeficiente sea cero. No selección usando externas.
- **Todas las métricas, selección y meta conservan igual peso territorio-año.**
  La nueva ponderación afecta solo el aprendizaje, como cambio material explícito (§3).

## 3. Único cambio material propuesto: pesos del entrenamiento

Esquema primario `recencia_h2`, semivida fija **2 años calendario**. Para un
entrenamiento recibido, sea `a_max` el máximo año presente y `n` su número de filas:

```
peso_bruto_i = 2 ** (-(a_max - anio_i) / 2.0)
peso_i = n * peso_bruto_i / math.fsum(pesos_brutos)
```

Calcular en orden estable de llaves, únicamente con el entrenamiento recibido.
Mismo peso para los 33 territorios de un mismo año; todos los pesos positivos,
sin truncar ni eliminar años. Normalizar a media 1, para separar la distribución
temporal de la escala global de los pesos. No ponderar métricas o evaluación.
No usar el año externo, observados de validación, todo el panel o fechas desconocidas
para determinar `a_max`. Año sigue siendo metadata, no una nueva columna de X.

La semivida 2 es una **decisión nueva de diseño**, no una declaración del usuario,
un resultado histórico ni un parámetro optimizado. Propone un contraste único:
una separación de dos años reduce a la mitad el peso bruto; retiene toda la historia
y reconoce el salto calendario sin anualizar el objetivo. No se probarán otras
semividas en este experimento ni se cambiará esta después de observar resultados.
Su elección no se presume óptima y deberá aprobarse al autorizar la implementación.

Mediana: aplicar el mismo vector al StandardScaler y al QuantileRegressor, mediante
`escalado__sample_weight` y `modelo__sample_weight`. Scaler solo train: registrar y
auditar media/varianza ponderadas y suma de pesos. Boosting: `sample_weight` en su
entrenamiento, sin agregar scaler. Persistencia no tiene estimador ni fit.
No escalar el objetivo ni alterar regularización/defaults de los candidatos.

Con pesos uniformes, usar vector exactamente 1 y la ruta original sin parámetros
sample_weight en todos los pasos, para que el caso uniforme no cambie el cálculo
por una ruta numérica de escalado diferente. Probar esta equivalencia con datos
inventados; no realizar ahora ni en fase1 reproducciones sobre panel real.

El soporte de pesos fue inspeccionado en código instalado sklearn1.9.1, sin importar
estimadores ni ajustar. Compatibilidad integral del Pipeline, routing y los modelos
queda pendiente de pruebas inventadas en la fase de implementación; no se afirma
que esas pruebas ya estén realizadas. Ver registro de lecturas y referencias locales.

## 4. Procedimientos y contraste que distingue hipótesis

|Procedimiento|Origen futuro|Papel|
|---|---|---|
|Recencia global|Nueva selección interna con los mismos 36 candidatos y pesos §3|Primario, definido antes de externas|
|Uniforme v5 global|CSV guardado v5, 165 pares; sin volver a ajustar o cargar modelos|Control de la política temporal|
|Persistencia|Previo independiente cotejado con CSV v3, mismos 165 pares|Referencia contractual|

El uniforme global v5 y persistencia coinciden exactamente en los guardados actuales.
No son dos evidencias independientes. Describir el contraste recencia–uniforme
además del contraste recencia–persistencia, sin duplicar el n.

Se guardarán las siete salidas originales de la arquitectura para recencia:
global, cinco grupos y persistencia, cada una con 165 filas (1.155 en total).
El primario es **solo recencia/global**, nunca el mejor grupo externo. Los grupos
son secundarios descriptivos. Las referencias son archivos guardados; no fabricar
externas históricas ausentes para las 35 configuraciones no seleccionadas de v5.

No hay una búsqueda entre "uniforme o recencia" después de las externas: el primario
es recencia fijada. Si falla, se informa sin rescate. El control y los secundarios
no pueden sustituirlo para declarar cumplimiento de la meta.

La comparación evalúa una política de aprendizaje y selección, no identifica qué
coeficiente, covariable o paso produjo una diferencia, ni un efecto causal.
La simplificación queda fuera para no mezclarla con recencia: todos los candidatos
y grupos se mantienen. Más historia no se incorpora porque no existe historia
adicional autorizada y comparable en el panel; ese estudio requeriría otra fuente,
verificación de comparabilidad y autorización propia.

## 5. Particiones y evaluación: sin cambios oportunistas

|Externa|Internas originales|Train externo de cambios|
|---|---|---|
|2021|Ninguna; todos los procedimientos usan persistencia fija|Sin fit|
|2022|2021|2019,2021|
|2023|2021,2022|2019,2021,2022|
|2024|2021,2022,2023|2019,2021,2022,2023|
|2025|2021,2022,2023,2024|2019,2021,2022,2023,2024|

Cada interna entrena cambios estrictamente anteriores desde 2019. No validar 2019
ni reutilizar ajustes entre ventanas externas. En interna2021, train2019 tiene pesos
uniformes; no ofrece contraste temporal por sí sola. Diez internas acumuladas contienen
solo cuatro años de validación únicos; preservar copias y verificar linaje exacto.
Sintetizar únicas solo si coinciden predicciones y contexto, sin promediar discrepancias.
4.752 únicas=36×4×33 es expectativa futura condicionada, no resultado de recencia.

Meta original, con 165 llaves/observados idénticos y denominador positivo/finito:

```
100 * (MAE_persistencia - MAE_recencia_global) / MAE_persistencia >= 5
```

Referencia histórica 3.429267191379531 puntos; el denominador se recalcula desde
guardados cuando se autorice piloto. Nunca decidir con cifras redondeadas, tres
de cinco años, un grupo mejor, filtrado de territorios o una meta parcial.

MAE = fsum(abs(prediccion-observado))/n; RMSE = sqrt(fsum(error²)/n);
sesgo = fsum(error)/n. Deltas pareados absolutos y cuadrados; dirección exacta−/0/+,
magnitud; n y unidades explícitos. Resúmenes globales/anuales/territoriales y cortes
2021–2024 frente 2025, sin cambiar el primario de cinco años. CSV en lectura
round_trip: valores/llaves/campos/orden exactos; int/float0 equivalente; tolerancia
1e−12/rtol0 solo acumuladores internos; repeticiones de entrenamiento 1e−10/rtol0,
sin usar esa tolerancia para permitir cambios en CSV/observados o linaje.

El contraste MAE_recencia−MAE_uniforme se informa sin crear un nuevo umbral de éxito.
Cumplir 5% seguiría siendo resultado exploratorio en estos años ya vistos.

## 6. Qué historia hay y qué evaluación independiente falta

Inventario actual de la única fuente, leído completo solo para años/llaves:
2018,2019,2021,2022,2023,2024,2025,33 filas por año. No hay otros años en esa fuente.
2018 no ofrece cambio anterior;2020 sigue excluido;no fabricar historia ni cambiar
el objetivo para aumentar n. Ningún raw/fuente adicional fue examinado o incorporado.

Todos los resultados 2021–2025 ya fueron vistos y motivaron este protocolo.
No se puede convertir 2025 en holdout inédito, reservar ahora algunos territorios
como independientes ni sumar copias/candidatos como nuevas observaciones. Este
piloto propuesto puede comparar procedimientos exploratoriamente, no confirmar mejora.

Confirmación independiente requeriría uno o más bloques temporales cuyos objetivos
no se hubieran inspeccionado al congelar un protocolo futuro, población/definiciones
comparables y covariables disponibles en la fecha real de predicción. **No se ha
comprobado disponibilidad de tales bloques ni se fija aquí un año futuro como existente.**
Primero verificar fuentes/fechas/comparabilidad con otra autorización; si no existen,
dejar pendiente confirmación. Un año adicional tampoco demuestra estabilidad general
por sí solo. No crear un mínimo universal de años ni un cálculo de potencia ficticio.

## 7. Implementación, controles y límites futuros

Fase1 futura: autorización separada; constructor común desde JSON v5, función de
pesos parametrizada, worker/runner propios y destinos restringidos. Pruebas inventadas
antes de cualquier fit real, notebook de controles desde fuente editable/generador
Python, nbformat y celdas realmente ejecutadas. Congelar código, defaults, pesos,
entradas, entorno y pruebas, sin ledger operativo ni resultados reales nuevos.

Controles obligatorios: pesos positivos/normalizados/iguales dentro de año; solo
train; intervalos1/2; ausencia de anualización/filtrado; ruta uniforme idéntica;
scaler ponderado train y parámetros completos; mediana/boosting reciben los pesos;
bandas/36IDs/2021fijo/selección antes externo/global distinto grupo/dedup por ID;
CSV exacto/intfloat0/1e−11/llaves/orden/duplicados/omisiones/no finitos; copias/linaje;
rutas/symlinks/imports/terminación/fallos/reanudación/cobertura; cálculo aritmético
independiente y referencias guardadas. Pruebas no alteran v1–v5 o diagnóstico.

Fase2 futura: otra autorización después de fase1 válida. Piloto serial, nuevo ledger
7200s completo incluyendo arranque/Pipeline/comunicación/fallos/reintentos/repeticiones;
no heredar saldos ni ampliar. Persistencia tiempo aparte sin fit. Cota sin fallos:
350 internos+≤24externos+≤4repeticiones=378. Pruebas de uniformidad solo inventadas,
no sumar reproducciones reales del procedimiento v5 como si fueran gratis.
Cinco comprobaciones globales, persistencia recalculada o ganador ajustado repetido.
Todo ajuste real consume ledger, también si se usa con propósito de control.

Fallos: numérico/convergencia → inelegible con razón; infraestructura → máximo un
retry, segundo detiene; caída sin tiempo medido agota conservadoramente. Falta de
integridad/cobertura/referencia, pesos inválidos, imports/routing incompatible,
discrepancia de copias o límite → incompleto, sin rescate ni meta parcial.
No inferir que tiene que fallar o mejorar a partir del diseño actual.

Antes de usar el entorno: Python3.12.14/sklearn1.9.1/54paquetes exactos del lock v4/
pip check, PYTHONDONTWRITEBYTECODE=1, semilla20261010. Entorno ausente/diferente se
documenta y consulta; no sustituir versiones silenciosamente. Esta fase documental
no volvió a ejecutar pip check ni afirma congelación operativa de sklearn.

## 8. Conservación y advertencias

Este diseño escribe solo en `diseno_temporal_objetivo3_v1/`. El diagnóstico queda
cerrado e intacto, incluso su continuidad; el diseño tiene continuidad propia.
Una ejecución futura escribirá solo en `experimentos_temporales_objetivo3_v1/`,
etapa1/etapa2 y continuidad propia. Conservar originales/v1–v5/diagnóstico/diseño,
protocolos, atributos, .gitignore, modelos y ledgers. No commit/push sin autorización.

Casos completos/Guainía238vs404/21.012106 puntos conservados como evidencia histórica
en v2/fase1/resultados/diagnostico_medias_disponibles.csv; procedencia local no
autenticada;IPM hogares frente alumnos;colegio frente residencia/enlace ecológico;
dependencia temporal/territorial y pocos años. No causalidad, confirmación independiente
o pronóstico anticipado demostrado. Antecedentes archivados no se reabren sin nueva
conexión. V5 meta no satisfecha permanece intacta;no notebook personal/simulación/
objetivo4/entrenamiento final. Entregar informe aunque ninguna alternativa mejore.
""")
    evidence = [
        dict(id='E1', archivo='diagnostico_objetivo3_v1/fase1/tablas/matriz_hipotesis.csv', llave='id=H1,H5,H6,H7',
             n='7hipótesis;6años de cambios;4validaciones únicas',
             hallazgo='Variación temporal descriptiva;eficacia recencia insuficientemente evaluada',
             impacto='Motiva comparar política temporal sin afirmar causa',
             alternativa='Un único contraste con mismos36candidatos y toda historia', resolucion='Propuesta en protocolo§§3–5'),
        dict(id='E2', archivo='diagnostico_objetivo3_v1/fase1/tablas/conteos_ventaja_interna_por_anio.csv', llave='periodo=anio_2021..anio_2024',
             n='35configuraciones×33pares por cada4años únicos', hallazgo='0,0,0,33 configuraciones superiores a persistencia por año',
             impacto='No confundir ventaja de2024 con éxito de procedimiento completo', alternativa='Mantener165pares ycriterio5%;no cambiarobjetivo/ventanas', resolucion='Primario recencia/global fijado;sinrescate'),
        dict(id='E3', archivo=str(SOURCE.relative_to(ROOT)), llave='codigo_departamento.zfill(2),anio;inventario completo',
             n='231llaves únicas;33territorios×7años', hallazgo='No años adicionales en fuente autorizada;2018historial/2020excluido',
             impacto='Más historia/confirmación no disponibles en alcance actual', alternativa='Protocoloexploratorio ygate futuro de fuentes/fechas/comparabilidad', resolucion='No incorporar fuentes/no inventar holdout'),
        dict(id='E4', archivo='experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json', llave='configuraciones/grupos/ventanas/semilla',
             n='36IDs;5grupos;5externas', hallazgo='Grilla y contratos completos están guardados',
             impacto='Permite aislar recencia sin elegir otra familia o entradas por resultados', alternativa='Heredar exacto yponderarúnicamentetrain', resolucion='ESPECIFICACION_PROPUESTA.heredado copia exacta'),
        dict(id='E5', archivo='experimentos_objetivo3_v5/etapa2/resultados/meta.json', llave='mae_v5/mae_referencia/meta_satisfecha',
             n='165pares externos', hallazgo='V5global=persistencia,mejora0%,metaNOsatisfecha',
             impacto='Controluniforme no es independiente de persistencia', alternativa='Usar CSVguardados,nuevo primario sin rescate ni reentrenarcontrol', resolucion='Dos contrastes,una misma población emparejada'),
        dict(id='E6', archivo=str(SOURCE.relative_to(ROOT)), llave='representaciones originales5/05 y8/08',
             n='35textos de códigos;33códigos normalizados;231llaves', hallazgo='Conteo de textos sin zfill crea dos territorios ficticios',
             impacto='Un inventario ingenuo altera población aparente', alternativa='Regla existente zfill(2),misma llave;no cambiar valores fuente', resolucion='33territorios/231llaves comprobados;sin nueva incidencia analítica'),
    ]
    for row in evidence:
        row['sha256'] = sha(ROOT / row['archivo'])
    save('resultados/evidencias.json', dict(origen='Lectura de artefactos guardados;ningún nuevo MAE/fit/predicción', evidencias=evidence))
    save('HISTORIA_Y_EVALUACION.md', """# Historia disponible y evaluación independiente

Inventario actual mediante csv.DictReader de las 231 filas de la única fuente
autorizada. Años:2018/2019/2021/2022/2023/2024/2025,33filas cada uno. Códigos
normalizados con la regla existente zfill(2):33territorios,231llaves únicas.
Los textos5/05 y8/08 no son territorios distintos;original intacto. No raw ni
fuentes adicionales revisadas para buscar más historia. Procedimiento y SHA en
resultados/partida.json/evidencias.json y fuentes/generar_diseno.py.

Disponibles6años de cambios completos(198filas);2018solo historial. Para validación
interna hay4años únicos2021–2024, aunque10particiones acumuladas. No hay un número
de años universalmente suficiente establecido;no calcular potencia/significancia
ni contar territorios/candidatos/copies como años independientes.

2021–2025 ya vistos motivaron decisiones de diseño. Cualquier piloto sobre estos
165pares conserva la evaluación original pero es exploratorio. No se dispone
de evaluación confirmatoria independiente en la fuente autorizada. No reservar
2025 retrospectivamente ni llamar inédito un conjunto ya examinado.

Antes de una futura confirmación, con autorización propia:

1. Identificar bloques temporales aún no inspeccionados, sin asegurar que existan.
2. Documentar procedencia/comparabilidad de población/agregación/variables.
3. Verificar fechas reales de disponibilidad de X y objetivo y congelar protocolo
   antes de examinar los nuevos objetivos;no usar IPMpublicado después de predicción.
4. Preservar población/objetivo/referencia/criterios;justificar cualquier cambio
   material previamente. No prometer generalización por un único año adicional.

Más historia y confirmación independiente son cuestiones diferentes: más train
no crea automáticamente un test nuevo. Esta fase autoriza ninguna fuente nueva,
descarga ni recopilación. Si no hay bloques comparables e inéditos, confirmación
queda pendiente, aunque un resultado exploratorio cumpla la meta5%.
""")
    save('EVIDENCIA_Y_DECISIONES.md', """# Evidencia, decisiones de diseño y límites

Versión1.0,2026-10-11. Evidencias completas con archivo/llave/n/SHA,impacto,
alternativa/resolución en resultados/evidencias.json, E1–E6.

|Decisión|Procedencia|Justificación y límite|
|---|---|---|
|Preparar protocolo sin entrenar|Usuario:genial,procede tras propuesta de fase de diseño|Autoriza documentos;no implementación/piloto|
|Conservar población,media,geografía,objetivo ymeta≥5%|Acuerdos usuario/protocolo v5§§1–2|No cambiar para mejorar métricas|
|Mismos36candidatos/grupos/entradas/bandas|Nueva decisión de diseño compatible con acuerdos|Aísla la política temporal;sin ampliargrilla ni seleccionarvariables|
|Recencia exponencial,semivida2años,un solo contraste|Nueva propuesta del agente,no instrucción numérica del usuario|No optimizada;retiene toda historia;requiere aprobación al autorizar implementación|
|Peso desigual entre años SOLO en entrenamiento|Cambio material nuevo explícito|Evaluación/selección/meta siguen igualpeso territorio-año;no afirmar aprendizaje inalterado|
|Pesos mean1;scaler/modelo mismos pesos;sin añoenX|Nueva especificación técnica pendiente de pruebas|Evita mezcla de escalas de pesos/global;transformaciones solo train|
|Control uniforme=CSVv5global;persistencia=previo/CSVv3|Antecedentes comprobados,diagnóstico H7|Son idénticos en165pares,no evidencias independientes;sin nuevasreproduccionesfits|
|Primario fijo recencia/global|Nueva decisión previa a resultados nuevos|Grupo/mejorsecundario no lo sustituye;no rescate retrospectivo|
|2021fijo/internal2021entrena2019|Contrato v5 intacto|Peso uniforme,no contrastetemporal en esainterna;no eliminarla|
|Solo evaluación exploratoria2021–2025|Comprobación actual del inventario ylecturasdiagnóstico|No confirmación independiente;no holdout retrospectivo|
|No simplificación/máshistoria en este contraste|Decisión de alcance con evidencia H3/H4/H6|Evita confundir políticas;eficaciacovariables/otra historia siguen pendientes|
|Implementación/piloto en fases autorizadas separadamente|Usuario yAGENTS|Sin ajustes ahora;sin presupuesto/ledger operativo/modelos/notebooks nuevos|

El diseño especifica una comparación lógica, no garantiza una mejora. Un resultado
futuro negativo no demostraría que todas las recencias fallan;positivo exploratorio
no prueba causalidad/confirmación/operación antes de publicarIPM. No cambiar semivida,
familias,bandas o meta después de resultados. Cualquier ampliación sería protocolo
yautorización nuevos,con versiones yadvertencias completas.

No reabrir antecedentes archivados59/esquema82/causa20212/fórmula/E2-01/E3-01/E3-02
sin conexión nueva. Los códigos5/05y8/08 se resolvieron por regla existente,no por
redefinir territorios. Mantener advertenciasGuainía238vs404/21.012106puntos,
procedencialocal/IPMhogares/colegio-residencia/ecología/dependencia/pocosaños.
""")
    library_root = Path('/tmp/icfes-v2-fase2-venv/lib/python3.12/site-packages/sklearn')
    libraries = [(library_root/'linear_model/_quantile.py','143–184'),
                 (library_root/'preprocessing/_data.py','903–928'),
                 (library_root/'ensemble/_gb.py','626–645'),
                 (library_root/'pipeline.py','500–550')]
    save('resultados/lecturas.json', dict(
        agentes='AGENTS.md completo', continuidad='diagnóstico vigente líneas1–105;antecedentes heredados no atribuidos como nuevaslecturas',
        planes='Plan diagnóstico§§1–3.5 como antecedentes;plan propio fase actual§§1–3;no planes de entrenamiento posteriores',
        protocolo='v5etapa1/PROTOCOLO_V5.md completo;diagnósticoPROTOCOLO_DIAGNOSTICO.md completo',
        artefactos='101huellasmanifiestodiagnóstico+29.640versionados;configuracionesv5completas;aceptación/preflightdiagnóstico;matriz/alternativas/conteos guardados',
        fuente='Todas231filas solo años/llaves para inventario;normalización existente zfill(2)',
        codigo_local=[dict(archivo=str(p), lineas=lines, sha256=sha(p), uso='Inspección estática de soporte sample_weight;no import/fit') for p,lines in libraries],
        incidencia='Primera búsqueda rg de código local tuvo salida truncada;relecturas acotadas efectivas anotadas arriba',
        entorno='No entorno revalidado ni pipcheck ejecutado en fase documental;disponibilidadruta no equivale a validación',
        pdf_paginas=0, web_busquedas=0, modelos_cargados=0,
        pendientes='Pruebas inventadas/routing/compatibilidad/runtime/cierreoperativo;solo en futura fase1 autorizada'))
    save('PROMPT_FASE1_IMPLEMENTACION.md', f"""# Nueva sesión — implementación y controles de recencia, SIN fits reales

GUARDADO, NO EJECUTADO. Su existencia no autoriza trabajo. Solo su envío expreso
por el usuario aprueba la propuesta protocolo1.0.0 y autoriza esta fase1, no piloto.

Trabajar en {ROOT}. Leer primero AGENTS.md, diseno_temporal_objetivo3_v1/
CONTINUIDAD_DISENO.md y continuidad vigente diagnóstico. Si no existe continuidad
experimental nueva, comenzar con inventario, sin inventar fases previas.
Leer planpropio solo faseactual y PROTOCOLO_TEMPORAL.md/ESPECIFICACION_PROPUESTA.json/
EVIDENCIA_Y_DECISIONES.md/HISTORIA_Y_EVALUACION.md. Verificar manifiesto de diseño,
conservación de todos antecedentes,GitHEAD/asunto/rama/ascendencia/trabajo posterior.
No reset/checkout/sobrescribir ajenos ni exigir Gitlimpio artificial:hay diagnóstico
ydiseño no versionados. Contradicciónmaterial:resolverconevidenciaoconsultar.

Aprobación concreta por enviar este prompt:semivida2años fija,ninguna búsqueda,
todos años retenidos;pesos positivos n*wbruto/fsum(wbruto),anchamaxanioSOLOtrain;
ponderar scaler yregresor/boosting,cambiar solo entrenamiento,evaluación/selección
igualpesoterritorio-año. Mismos36IDs/grupos/entradas/defaults/semilla/bandasv5.
Primario futurorecencia/global;referenciasCSVv5global/persistencia independientes
del nuevofit pero idénticasentresí;2021fijo;externas2021–2025exploratorias.
No nueva familia/variable/simplificación/semivida/objetivo/umbral ni fuentesextra.

Crear solo experimentos_temporales_objetivo3_v1/etapa1/ y continuidadexperimental
propia;originales/v1–v5/diagnóstico/diseño ycontinuidades intactos. No alterar diseño
congelado documental;históricoscontinuidades ensucommitreal sin excepcionesotrasrutas.
Destinos guardados también frente symlinks;no importar runners operativos viejos.

Comprobar antesuso /tmp/icfes-v2-fase2-venv/bin/python:Python3.12.14/sklearn1.9.1/
54paquetesexactoslockv4 ypipcheck;PYTHONDONTWRITEBYTECODE=1,semilla20261010.
Si falta/difiere documentar/consultar sin sustituciones ni nuevas instalaciones
silenciosas. Revalidar SHAfuente {sha(SOURCE)} yderivado {sha(PANEL)},
reconstrucción enmemoriaexactallaves/campos/orden/valores231/33/198,previo2021=2019,
intervalo2sinanualizar,GRUPOSv5 yreferencias guardadas165pares;sinraw/fuentesextra.

Implementar fuentes comunes propias:funciónpesos,reconstrucción/constructor,
worker/motor/orquestación compatibles pero no ejecutar panelreal;adaptaciones
previas solo lectura. En mediana enviar escalado__sample_weight/modelo__sample_weight,
boosting sample_weight;casouniformevector1 y ruta original sin pesos explícitos.
Registrar pesos,contexto/trainaños/llaves/normalización/parámetros/transformaciones/
versiones/semilla/defaults/advertencias;metadatos ytests no afirmarán modelos reales.
No funciónpesos que mire validación/año externo ni Xcon año/código/intervalo/conteos.

Pruebas completas inventadas ydobles según protocolo§7:pesos/normalización/positividad/
uniformidad/train-only/intervalos1–2/scalerponderado/modelosrecibenpeso/routing;
36IDs/bandas/globaldistintogrupo/2021fijo/dedupID/cobertura;CSVexactointfloat0/rechazo
1e−11/llaves/campos/orden/duplicados/omisiones/no finitos;linaje/copiasdiscrepantes;
rutas/symlinks/importshijos/terminación/fallos/retry/reanudación/cotastiempo;
aritméticaindependiente/referenciasguardadas. Ajustes inventados permitidos solo
en destinos de pruebaspropios;ningún ajuste sobre panelreal o comparadoreshistóricos.

Notebook útil de controles desdefuentePythoneditable/generadorPython/nbformat,
celdaspertinentes realmenteejecutadas SOLO inventados;sin notebookmodelos/personal/
simulación. Congelaciónoperativacódigo/defaults/pesos/entradas/entorno/tests íntegra
ANTESdefitreal. Fase1 no crea ledgerreal/modelos/predicciones/MAE/meta de recencia.
README/protocoloimplementación/registro/lecturas/entorno/pruebas/notebook/
conservación/manifiesto/continuidad,pendientesexplícitos,cierrepropioverificado.

Detenerincompleto ante controlindispensableirresuelto,norescates/metaparcial.
No fase2auto:requiere su prompt enviado aparte yfase1 completa.7200s son presupuesto
futuro nuevo,no disponibleahora ni remanentev5;cota378contratada,noajustes ejecutados.
Preservar advertenciasGuainía238vs404/21.012106puntos,localnoautenticada,IPMhogares/
alumnos/colegio-residencia/ecología/dependencia/pocosaños.2021–2025vistos,no confirmación
independiente/causalidad/pronósticoanticipadodemostrado. Antecedentesarchivadosnoabrir
sinconexiónnueva. NOcommit/push/descargas/fuentesnuevas/etapa3v5/notebookpersonal/
simulación/objetivo4/entrenamientofinal. Informar cierre inclusosi controlesfallan.
""")
    save('PROMPT_FASE2_PILOTO.md', f"""# Nueva sesión — piloto exploratorio recencia36, SOLO después de fase1 aprobada

GUARDADO, NO EJECUTADO. La existencia o lectura de este archivo no autoriza fits.
Solo envío expreso por usuario autoriza fase2 y únicamente si fase1 experimental
está completa y congelada. Si no existe/no pasa,documentar ydetener,no iniciarla
automáticamente ni convertir el diseño documental en congelaciónoperativa.

Raíz {ROOT}. Leer AGENTS,continuidadexperimentalvigente/continuidad diseño/diagnóstico,
protocolo1.0.0/especificaciónpropuesta aprobada ycontratosfase1;delplanexperimental
solo secciónfase2. GitHEAD/asunto/rama/ascendencia/trabajoposterior e integridadtodos
antecedentes,continuidadeshistóricasensucommitreal;noreset/cambio silencioso ni
sobrescribirajenos. Revalidar entorno exacto Python3.12.14/sklearn1.9.1/54lock/pipcheck
antesuso,PYTHONDONTWRITEBYTECODE=1/semilla20261010. Ausencia/diferencia documentar/
consultar,no sustituciónsilenciosa ni fuenteadicional/instalaciónnoautorizada.

Revalidar fuentev2SHA{sha(SOURCE)},derivadov5SHA{sha(PANEL)},
231/33/198,campos/valores/llaves/ordenexactos/GRUPOS/defaults/36IDs,fuentes/pruebas/
notebook/congelaciónfase1 ycontroles/routing;referenciasCSV165paresoriginales.
Toda escritura exclusivamente experimentos_temporales_objetivo3_v1/etapa2/ y
continuidadexperimentalpropia,symlinksrestringidos;v1–v5/diagnóstico/diseño/etapa1/
atributos/.gitignore/ledgersmodeloshistóricos intactos;no modeloscomparadorescargados.

Ejecutar únicamente recencia_h2 según protocolo:samplespesos trainn*2**(-(maxtrainanio
-anio)/2)/fsum;todospositivos,noeliminaraños,noañadirano/códigoaX;scaler/regresor
ponderados/boostingpesoexplícito,uniformevector1rutaoriginal;ningunanueva semivida/
familia/variable/lambda/búsqueda/mezcla/imputación/clipping/objetivo. Mismos36candidatos,
5grupos/ventanas/bandas/orden/semilla,2021fijo persistenciasinfit/puntuación/selección.
Desde2022selección antesexterno,global puede diferirgrupo,dedupsoloIDigual,no reutilizar
fitsinternosentrewindows. Guardar36registros por4selecciones incluidas inelegibles.

Runner propio serial/terminable,presupuesto nuevo7200s/ledgerpersistentecon arranque/
Pipeline/comunicación/fallos/retries/repeticiones;persistenciatiempoaparte,sinfit.
Cota378sinfallos=350internos+≤24externos+≤4repeticiones. No fits gratis de uniformidad
sobrepanelreal;equivalencia ya probada coninventadosfase1. Cinco comprobacionesglobales
(persistenciarecálculo o ganadorajustadorepetidopresupuestado)atol1e−10rtol0.
Fallonuméricoinelegiblepersistente;infra1retrymáximo;segundodetiene;caídasintiempo
agotaconservadoramente;reanudar verifichuellas/contexto/artefactos/intentosconsumidos.

Registrar matrices/llaves/objetivos/weights/normalización/anios/pesosporfila/scaler
ponderadoparámetros/semilla/versiones/defaults/advertencias/tiempos/huellas/modelos
propios/predicciones/selecciones/repeticiones. Auditoría independiente,CSVexactos
intfloat0equivalente,rechazo1e−11/llaves/orden/nofinitos.11880internasoriginales,
36IDs/144registros,1155externasrecencia=7×165/33territorios×5años.4752únicascondicionadas
a copias/metadatainternosidénticos;linajecompleto ymenorexternorepresentante;
discrepanciasnosepromedian/escogen,detenersíntesisdependiente. Mantenerporventanaoriginal.

Primario recencia/globalfijo;controlCSVv5global ypersistenciaindependienteCSVv3son
numéricamenteidénticos yno evidenciasindependientes;no nuevosfits/cargasmodelos históricos.
Metaoriginalexacta100*(MAEpersistencia-MAErecenciaglobal)/MAEpersistencia≥5 sobre
165llaves/observados idénticos,denominadorpositivo/finito recalculado;sinredondeo/
tresdecinco/ganadorgrupoexterno/metaparcial. ContrasteMAErecencia−MAEv5globaldescriptivo,
sin nuevo umbral. No reemplazar primario por control o grupos si mejora otra salida.

Informe completo inclusosinfalla5%,tablaspredicciones/erroresMAE/RMSE/sesgo/deltas/
dirección/magnitud/anios/territorios/cortes/selecciones/linaje;gráficosdescriptivos
conunidadesyn. Notebook útil soloresultadosdesde fuentePython/generador/nbformat,
celdasrealmenteejecutadas;no notebookpersonal,modelofinal o simulación.
README/informe/registro/lecturas/auditoría/entorno/pruebas/conservación/manifiesto/
continuidad cierre propio verificable. Integridad/cobertura/pesos/referencia/presupuesto
irresueltos:conservarincompleto ydetener,sinrescate. Antecedentes archivados no reabrir.

TODOS2021–2025vistos:exploratorio,sinconfirmaciónindependiente/causalidad/pronóstico
anticipadodemostrado;ningunareservanueva/añofuturoinventado. Más historia/confirmación
requierefuentescomparables/fechas/autorizaciónseparadas,no descargarlas aquí.
Guainía238vs404/21.012106puntos,evidenciahistórica/localnoautenticada/IPMhogares-alumnos/
colegioresidencia/ecología/dependencia/pocosañospreservados. No etapa3v5/excepcióna
metaNOsatisfecha. NOcommit/push/fuentesextra/instalacionesnoautorizadas/entrenamientofinal/
simulación/objetivo4/notebookpersonal/avanceauto. No cambiar protocolo para mejorar MAE.
""")
    save('README.md', """# Diseño temporal objetivo3 v1 — documentos preparados, piloto no iniciado

Propuesta1.0.0,2026-10-11. Usuario autorizó diseñar el siguiente protocolo,sin entrenar.
Se propone conservar36candidatos/grupos/selecciónv5 y cambiar únicamente pesos de
entrenamiento:recenciaexponencial consemivida2años,toda historia retenida.
La evaluación sigueigualpeso territorio-año ymeta5%global frentepersistencia.
No eficacia demostrada;todos2021–2025vistos,solo evaluaciónexploratoria disponible.

- PROTOCOLO_TEMPORAL.md:comparación,decisiones materiales,ventanas/criterios/controles.
- ESPECIFICACION_PROPUESTA.json:36candidatos/defaults/grupos copiados exactos,reglas
  de pesos/aplicación/selección/evaluación/presupuesto futuro;no configuraciónoperativa.
- HISTORIA_Y_EVALUACION.md:inventario231/33/7años,ningún holdoutinédito disponible.
- EVIDENCIA_Y_DECISIONES.md/resultados/evidencias.json:archivo/llave/n/SHA/impacto/
  alternativa/resolución;separar usuario,comprobaciones ypropuestasnuevas.
- PLAN_DISENO.md/CONTINUIDAD_DISENO.md:alcance y cierre documental propio.
- PROMPT_FASE1_IMPLEMENTACION.md:solo al enviarlo aprueba propuesta y autoriza
  implementación/pruebasinventadas/congelación,SIN fits reales.
- PROMPT_FASE2_PILOTO.md:solo al enviarlo despuésfase1válida autoriza piloto aparte.
- fuentes/generar_diseno.py:generador/validador documental stdlib,sinestimadores.
- resultados/:partida/snapshotprevio,lecturas/registro/aceptación/conservación/manifiesto.

Verificación solo lectura,desde raíz:
`PYTHONDONTWRITEBYTECODE=1 python3 diseno_temporal_objetivo3_v1/fuentes/generar_diseno.py --verificar`
No volver a generar sobre destinos existentes. No modelos/pesosreales/predicciones/
métricas/controlesexperimentales/notebooks/ledger nuevos en esta fase.

El diagnóstico íntegro permanece en diagnostico_objetivo3_v1,inclusocontinuidad;
v1–v5intactos. No commit,push,instalaciones/descargas/nuevasfuentes.
Los prompts son artefactos guardados,no autorizaciones implícitas. La semivida2 y
ponderaciónscaler/modelo deben aprobarse al autorizarfase1;no experimentoejecutado.
""")
    save('CONTINUIDAD_DISENO.md', """# Continuidad diseño temporal objetivo3 v1 — fase documental completa

2026-10-11,America/Bogota. Primera sesión de este diseño:no existía continuidad
anterior,se comenzó con inventario. Usuario autorizó `genial,procede` después de
propuesta de diseñar protocolo SIN entrenar. Documentos completos,propuesta revisable;
implementación/congelación/piloto NO autorizados ni ejecutados. Sinfaseprevia inventada.

HEAD75c3a25182af363f47b0d743820f99084e18fed5/asuntoexactocierre v5,rama
codex/objetivo3-v5-mae/ascendencia/sintrabajoposterior verificados;sinreset/checkout.
Diagnóstico propio previamente no versionado protegido íntegro junto a29640versionados;
no exigir Gitlimpio artificial ni modificar su continuidad/manifiesto cerrado.
Todas escrituras actuales en diseno_temporal_objetivo3_v1/. Snapshot yconservación
enresultados/partida.json/conservacion_final.json/manifiesto_diseno.json.

Lecturasactuales:AGENTScompleto,continuidadvigentediagnóstico1–105,protocolo5.0.0
completo,plan diagnóstico§§1–3.5/planpropiofaseactual1–3,matriz/alternativas/conteos/
preflight/aceptación/manifiesto/configuracionesv5JSONcompleto. Fuenteautorizada231filas
solo inventarioaños/llaves:7años×33;normalizaciónexistentezfill(2) resuelve5/05y8/08,
33territorios,231llavesúnicas;no nuevo análisisestadístico. PDF0páginas/web0.
Código sklearnlocal soporte sample_weight enlecturaestática,sinimport/fit. Primera
búsqueda truncada corregida por rangosacotados. Entorno NO revalidado/pipcheck NO
ejecutado ahora,exigido en fasefutura antesuso;noinstalación/descarga actual.

Acuerdosusuario conservados:población/mediarecibida/geografíacolegio/objetivooriginal,
2020excluido/2018historial/2021previo2019/intervalo2sinanualizar/evaluaciónigualpesos/
meta5%global/165pares/semilla/bandas/seleccionesanteriores/protocolos/ledgersintactos.

DecisionesNUEVASpropuestasantesresultadosnuevos:único esquema recencia_h2,semivida2años
calendario,anchor maxanioSOLOtrain,wbruto2**(-(maxtrainanio-anio)/2),normalizarn/fsum,
todospositivos,mismo territorio dentroaño,toda historiaretenida. Cambiomaterial
exclusivamentepesostrain,scaler/modelo ponderados;añonoentraX. Evaluación/selección/
meta siguen igualpeso territorio-año. Misma grilla36/defaults/grupos/semilla/bandas;
primariorecencia/global,grupossecundariosnorescatan;controlCSVv5global/persistencia
idénticos,no evidenciaindependiente. Semivida es propuesta del agente,no eleccióndel
usuario ni valor óptimoestimado;aprobar explícitamente al autorizarimplementación.

No controlnuevo ajustado,pesosreales,MAE/prediccionesmodelos/notebook/ledger
operativo ni congelaciónexperimentales. EspecificaciónJSON/candidatosheredados son
documentales. Herenciaexacta validada contra configuracionesv5;no variablessimplificadas.
Historia autorizada no contiene años extra/todosexternosvistos;no holdoutindependiente.
Nuevo piloto soloexploratorio;fuentes/fechas/comparabilidad para confirmación futura
pendientes bajo autorizaciónseparada,ninguna fuenteextraobtenida ni añofuturoinventado.

Hallazgos/impactos/alternativasresueltosdocumentalmente:E1–E6evidencias yregistro,
sin causas/promesa5%. Guainía238vs404/21.012106puntos/evidenciahistórica,
procedencialocalnoautenticada/IPMhogares-alumnos/colegioresidencia/ecología/
dependenciatemporal-territorial/pocosañospreservados. Antecedentesarchivadosnoabrir
sinconexiónnueva. V5metaNOsatisfecha/condiciónetapa3intacta.

Entregablesverificables:plan/protocolo/especificación/historia/decisiones/README/
2prompts/continuidad propia/fuentegeneradora/partida/evidencia/lecturas/registro/
aceptación/conservación/manifiesto/verificación. Próximaautorizaciónposible:fase1
implementación/controlesinventados/congelaciónsinpanelreal,conpromptenviadoexpreso;
fase2requiereotraprompt yfase1aprobada. Nunca avanzar automáticamente.7200s y378
son contrato futuro propio,no saldoexistente/consumoactual;no usarremanentes.
Todosoutputsrealizadosdocumentales;sinNotebooknecesario paraestafase. Fits0,
modeloscargados0/push0/commits0/descargas0/instalaciones0. Sinexperimentos posteriores,
notebookpersonal/simulación/objetivo4/entrenamientofinal.
""")
    save('resultados/registro_hallazgos.json', dict(hallazgos=[
        dict(id='D1', ubicacion='diagnósticomatrizH1/H6 yprotocolo§1', impacto='No causa/eficaciarecencia establecida',
             alternativa='Comparacióncongrillaheredada,solo pesosdistintos', resolucion='Diseño concreto,esperarautorización/controles;sin nuevo MAE'),
        dict(id='D2', ubicacion='HISTORIA_Y_EVALUACION.md ypartida/fuente', impacto='No confirmacióninédita disponible',
             alternativa='Evaluaciónexploratoria ygate futuro fechas/fuentes', resolucion='No fabricarholdout/añofuturo ni nuevasfuentes'),
        dict(id='D3', ubicacion='PROTOCOLO_TEMPORAL.md§3', impacto='Ponderartrain cambia un acuerdo de aprendizaje,necesita aprobaciónconcreta',
             alternativa='Mantener evaluaciónigualpesos ydocumentar excepcióntemporal', resolucion='Especificaciónpropuesta/aprobaciónporpromptfase1,ningún cambioaplicado'),
        dict(id='D4', ubicacion='resultados/evidencias.json:E6', impacto='35textosdecódigo podrían aparentarpoblación distinta',
             alternativa='Reglaexistentenormalizarzfill(2)', resolucion='33territorios/231llaves,sin escribir fuente/reabrirhistórico'),
        dict(id='D5', ubicacion='Lecturaestáticasklearnlocalsegúnlecturas.json', impacto='Soporte interfaces no garantiza implementación completa',
             alternativa='Pruebasinventadasrouting/scaler/modelosenfase1', resolucion='Declarar soporteinspeccionado,controlespendientes/no fit'),
        dict(id='D6', ubicacion='Snapshotdiagnóstico completo yGit', impacto='Modificar continuidaddiagnóstico invalidaría su cierre',
             alternativa='Carpeta/continuidad nueva para diseño', resolucion='Diagnósticointacto porSHA,conservación sinexcepciones a archivosanteriores')],
        pendientes_indispensables_diseno=[], pendientes_implementacion=['Validaciónintegral pesos/routing/entorno/controles/congelación'],
        pendientes_cientificos=['eficaciarecencia','más historia comparable','confirmación independiente/fechasoperacionales']))
    # Validación documental: no pesos sobre datos reales ni nuevos resultados de evaluación.
    proposal = read(OWN / 'ESPECIFICACION_PROPUESTA.json')
    assert proposal['heredado']['candidatos'] == configs['configuraciones']
    assert proposal['heredado']['grupos'] == configs['grupos'] and proposal['heredado']['ventanas'] == configs['ventanas']
    assert proposal['recencia']['semivida_anios_calendario'] == 2.0 and not proposal['recencia']['parametros_busqueda']
    assert proposal['evaluacion']['meta_porcentaje'] == 5 and proposal['evaluacion']['pares_primarios'] == 165
    assert proposal['presupuesto_futuro']['cota_sin_fallos']['total'] == 350+24+4
    assert proposal['evaluacion']['externas_recencia'] == 7*33*5
    assert proposal['evaluacion']['internas_originales_esperadas'] == 36*33*(1+2+3+4)
    assert proposal['evaluacion']['internas_unicas_condicionadas'] == 36*33*4
    save('resultados/aceptacion_diseno.json', dict(aprobado=True, documentos_coherentes=True,
        herencia36_grupos_defaults_ventanas_exacta=True, cambios_materiales_explicitos=True,
        meta_original_5=True, evaluacion165_pesos_iguales=True, inventario_fuente231_33=True,
        confirmacion_independiente_disponible=False, evidencia_local_referenciada=True,
        fase='Diseño documental completo,no ejecución experimental',
        prompts_guardados_no_ejecutados=2, protocolo_operativo_congelado=False,
        notebook_necesario_en_fase_documental=False, pesos_reales_generados=0,
        fits=0, modelos_cargados=0, nuevas_metricas=0, nuevas_fuentes=0, commits=0, push=False))
    check_hashes(protected)
    assert git('rev-parse','HEAD') == EXPECTED_HEAD
    current_names = set(git('ls-files','-z').split('\0')) - {''}
    assert current_names == set(prep['inventario_protegido']['sha256_versionados'])
    assert all(line[3:].startswith(('diagnostico_objetivo3_v1/','diseno_temporal_objetivo3_v1/'))
               for line in git('status','--porcelain','--untracked-files=all').splitlines())
    save('resultados/conservacion_final.json', dict(aprobado=True, protegidos=len(protected),
        versionados=29640, diagnostico=len(previous), huellas_iguales=True,
        diagnostico_incluida_continuidad_intacto=True, v1_v5_modelos_ledgers_atributos_intactos=True,
        inventario_git_identico=True, head_igual=True, rama_reutilizada=True,
        nuevas_escrituras_solo_diseno=True, sin_excepciones_archivos_anteriores=True,
        raw_ignorado='No censo binario;no escritura', fits=0, commits=0, push=False))
    save('resultados/manifiesto_diseno.json', dict(version='1.0.0', completa_documental=True,
        protocolo_operativo_congelado=False, piloto_autorizado=False,
        entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(OWN.rglob('*')) if p.is_file()},
        exclusiones_autorreferencia=['resultados/manifiesto_diseno.json','resultados/verificacion_diseno.json'],
        fits=0, nuevas_metricas=0, nuevos_resultados=0, prompts_no_ejecutados=True,
        pendientes_indispensables_diseno=[], pendientes=['Autorizarfase1/controles','Autorizaciónposteriorpiloto','Confirmaciónindependiente/fuentesfechas'],
        commits=0, push=False))
    result = verify()
    save('resultados/verificacion_diseno.json', result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
