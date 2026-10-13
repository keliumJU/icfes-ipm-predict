from pathlib import Path
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone

ROOT = Path('/home/kelium/Documents/espcarlos/icfes-predict-improved')
PARENT = ROOT / 'experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible'
OUT = PARENT / 'resolucion_procedencia_versiones_historicas'

PLAN = '''# Nueva sesión: resolver procedencia y versiones históricas

## Objetivo y autorización

Determinar qué ediciones oficiales de pobreza y Saber 11 corresponden a los archivos locales y desde cuándo estaban efectivamente disponibles. Es una fase documental previa a decidir sobre el posible experimento de aporte adicional de pobreza a la historia académica territorial. No ejecutar el experimento.

Autorización expresa nueva: consultar documentación oficial del DANE y del ICFES y descargar anexos agregados históricos del DANE, exclusivamente para verificar versiones. No descargar microdatos, bases ICFES ni nuevos paneles; no crear datasets analíticos ni sustituir valores locales. No ajustar modelos, repetir el contraste, ejecutar escenarios u objetivo 4, ni heredar candidatos, meta del 5 %, criterios de éxito o presupuestos. No contactar terceros.

## Inicio y conservación

Trabajar en `/home/kelium/Documents/espcarlos/icfes-predict-improved`. Leer AGENTS.md y las continuidades del contraste, de su revisión de alcance y de la preparación documental; después únicamente decisiones, protocolos y pendientes pertinentes. La revisión de alcance está dentro de `experimento_pobreza_historia_objetivo3/revision_alcance_objetivo4/`. Mantener cerrado el contraste anterior.

Esta carpeta contiene solo el plan de arranque y su conservación, no una investigación ejecutada. Al comenzar, leer CONTINUIDAD.md y verificar esta entrega con `python3 -B verificar_plan.py`. Preservar su estado y registrar una nueva partida antes de añadir entregables de investigación. No sobrescribir estos documentos. El verificador anterior de preparación aprobó antes de crear esta carpeta; su inventario cerrado no incluye la ampliación. No modificarlo ni presentar un rechazo posterior por inventario añadido como alteración de sus archivos.

Guardar todos los entregables nuevos exclusivamente en `experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/resolucion_procedencia_versiones_historicas/`, con la investigación en su subcarpeta `investigacion/`. Usar /tmp para temporales. Registrar huellas SHA256 antes de escribir, con exclusiones explícitas. No modificar tesis, entregas anteriores, runtime compartido o .git; no commit/push. Crear primero fuentes .py; no se necesitan notebooks para esta fase. Cualquier notebook justificado debe generarse y validarse desde Python.

## Investigación y cotejo

**DANE.** Revisar IPM y quince indicadores de 2018, 2019 y 2021–2025. Identificar producto, organismo, periodo observado, población, geografía, edición, publicación y revisiones. Priorizar la recalibración de 2018, el anexo de 2019 y las ediciones anteriores a los libros locales de 2024 y 2025.

Registrar cada descarga oficial con URL solicitada y final, fecha de consulta y adquisición actual, edición declarada, huella y evidencia de publicación. Un archivo enlazado hoy desde una página histórica no demuestra que sea el archivo publicado entonces. Conservar por separado primera publicación, revisión, adquisición y modificación local.

Cotejar todas las celdas pertinentes del dominio Total: 33 territorios, IPM y quince tasas de los años locales. Documentar hojas, ubicación, unidades, definiciones, precisión, coincidencias y diferencias. Generar evidencia de comparación y resúmenes de diferencias, sin nuevos paneles ni incorporación de cifras externas al análisis. No repetir auditorías anteriores salvo el cotejo nuevo necesario con una edición oficial. Igualdad numérica, identidad de archivo y disponibilidad histórica son comprobaciones distintas; una huella actual no autentica una fecha pasada.

**ICFES.** Investigar documentalmente ambas aplicaciones de los siete años locales: publicación, revisiones, inventarios, diccionarios y cambios de versión. Revisar únicamente antecedentes locales necesarios de adquisición, huellas y metadatos, sin leer registros personales ni recalcular medias. Exigir evidencia que vincule cada TXT local con una edición oficial. No sustituir fechas de bases anonimizadas por fechas de resultados individuales o agregados con otra población. Si esta autorización no permite resolver la identidad, describir la brecha y la constancia o adquisición que requeriría otra autorización; no descargar bases ICFES.

**Disponibilidad.** Revisar los cortes documentales ya propuestos, sin escoger uno como decisión de uso. Separar disponibilidad de pobreza, historia académica y respuestas de entrenamiento; considerar también la edición elegible en cada corte de los ejemplos históricos. No suponer que un rezago anual garantiza disponibilidad ni retrofechar con actualizaciones o metadatos. Cuando solo exista intervalo, conservarlo y usar su extremo superior como límite conservador únicamente para una edición identificada.

Mantener inicialmente población y respuesta del contraste: 33 territorios, media local prom_punt_global, mismos filtros y aplicaciones, igual peso territorio-año, 2018 nivel histórico, 2019 historia, 2020 excluido, respuestas 2021–2025 y 165 pares nominales; salto 2019→2021 sin anualizar. Conservar persistencia e historia como referencias. Presentar cobertura demostrada, condicionada y no demostrada; cualquier cambio de entradas, ventana o población debe explicarse como pregunta nueva antes de evaluar resultados. No seleccionar cortes, años o modelos por errores favorables. Enero 1 a las 00:00 Bogotá sigue siendo recomendación pendiente, no decisión aceptada.

Comprobar documentalmente si existe un año anual comparable aún no examinado, sin adquirir sus datos ni afirmar independencia sin evidencia. Los años vistos solo permiten evaluación exploratoria. No interpretar predicciones como efectos causales de modificar pobreza.

## Entregables y comprobación

Entregar calendario por fuente/año/edición (fuente, año observado, edición, publicación, evidencia, correspondencia local, estado y limitación como mínimo); registro de procedencia y revisiones; resumen reproducible de cotejos; informe de factibilidad; complemento del protocolo sin ejecución; hallazgos con impacto, alternativa y resolución o pendiente; referencias y extractos con URL, consulta y página/sección/celda; lecturas revisadas y pendientes; manifiesto; verificador de solo lectura y continuidad propia de investigación.

Verificar conservación, integridad y trazabilidad, sin modificar manifiestos o verificadores anteriores. Distinguir esa aprobación de autenticación de fuentes y factibilidad científica. Leer PDF por páginas y secciones, conservando ubicaciones y pendientes.

## Condición de cierre

Dar por resuelto solo lo respaldado por evidencia de producto, edición, valores pertinentes y disponibilidad anterior al corte. Clasificar identidad exacta, igualdad numérica, compatibilidad nominal y ausencia de demostración por separado. No declarar un historial exhaustivo sin revisiones a partir de dos ediciones tardías iguales.

Si quedan controles indispensables abiertos, entregar cierre documental incompleto verificable, con evidencia faltante y alternativa concreta. Indicar qué quedó demostrado y qué decisiones requeriría autorizar después: uso/corte, cobertura y cambios de entradas o ventanas, evaluación exploratoria o prospectiva, criterio práctico, candidatos y presupuesto nuevo. No iniciar adquisiciones fuera del alcance ni ningún experimento automáticamente.
'''

PROMPT = '''# Inicio de nueva sesión: procedencia y versiones históricas

Trabaja en `/home/kelium/Documents/espcarlos/icfes-predict-improved`.

Lee AGENTS.md y luego la continuidad y el plan guardados en:
`experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/resolucion_procedencia_versiones_historicas/CONTINUIDAD.md`
`experimento_pobreza_historia_objetivo3/preparacion_pobreza_disponible/resolucion_procedencia_versiones_historicas/PLAN_NUEVA_SESION.md`

Implementa ese plan exclusivamente documental, verificando y preservando primero el estado existente. Autorizo documentación oficial DANE/ICFES y descarga de anexos agregados históricos DANE solo para cotejar versiones. No autorizo microdatos, bases ICFES, nuevos paneles o datasets analíticos, ajustes, escenarios, objetivo 4 ni repetición del contraste. No heredes presupuestos, candidatos o meta del 5 %.

Guarda la investigación únicamente en la subcarpeta `investigacion/` indicada por el plan, sin sobrescribir el paquete de arranque ni entregas anteriores. Temporales en /tmp. Fuentes .py antes de procesamiento; notebooks solo si aportan valor y generados desde Python. No modificar tesis, runtime compartido o .git; no commit/push.

Resuelve hasta donde la evidencia permita la procedencia, identidad de ediciones y disponibilidad histórica de IPM, quince indicadores y Saber 11 de los años locales. Distingue existencia de una publicación de disponibilidad de los valores locales. Mantén población y respuesta iniciales, y referencias de persistencia e historia. La fecha de uso sigue pendiente: no fijarla silenciosamente.

Cierra con entregables verificables, pendientes y continuidad. Si la evidencia indispensable no se resuelve, entrega cierre documental incompleto, sin modelos ni avance automático.
'''

VERIFIER = '''from pathlib import Path
import hashlib, json, os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def sha(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()

def verify():
    baseline = json.loads((HERE/'PARTIDA_PLAN.json').read_text())
    manifest = json.loads((HERE/'MANIFIESTO_PLAN.json').read_text())
    for name, expected in baseline['sha256'].items():
        assert sha(ROOT/name) == expected, f'Original alterado: {name}'
    for name, expected in manifest['sha256'].items():
        assert sha(HERE/name) == expected, f'Entrega alterada: {name}'
    actual = set()
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in baseline['exclusiones_directorios'] and not (Path(base)/d).is_symlink()]
        for name in names:
            p = Path(base)/name
            if p.is_file() and not p.is_symlink(): actual.add(p.relative_to(ROOT).as_posix())
    prefix = HERE.relative_to(ROOT).as_posix()+'/'
    own = {prefix+n for n in manifest['sha256']} | {prefix+n for n in manifest['exclusiones']}
    assert actual == set(baseline['sha256']) | own, 'Inventario cerrado cambió; requiere nueva partida, no modificar este verificador'
    return dict(conservacion_aprobada=True, archivos_previos=len(baseline['sha256']), archivos_paquete=len(manifest['sha256']), investigacion_ejecutada=False, modelos_ejecutados=False, disponibilidad_historica_certificada=False, avance_automatico=False)

if __name__ == '__main__': print(json.dumps(verify(), ensure_ascii=False))
'''

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

assert not OUT.exists(), 'No sobrescribir trabajo previo'
exclusions=json.loads((PARENT/'PARTIDA_DOCUMENTAL.json').read_text())['excluidos_inventario']
baseline={}
for base, dirs, names in os.walk(ROOT):
    dirs[:]=[d for d in dirs if d not in exclusions and not (Path(base)/d).is_symlink()]
    for name in names:
        p=Path(base)/name
        if p.is_file() and not p.is_symlink(): baseline[p.relative_to(ROOT).as_posix()]=sha(p)

stamp=datetime.now(timezone.utc).isoformat()
OUT.mkdir()
dump(OUT/'PARTIDA_PLAN.json', dict(fecha_utc=stamp, sha256=baseline, exclusiones_directorios=exclusions, limite='Solo archivos regulares; enlaces simbólicos y directorios excluidos no certificados. Huellas registradas antes de crear la carpeta.'))
(OUT/'PLAN_NUEVA_SESION.md').write_text(PLAN)
(OUT/'PROMPT_NUEVA_SESION.md').write_text(PROMPT)
(OUT/'verificar_plan.py').write_text(VERIFIER)
(OUT/'CONTINUIDAD.md').write_text('''# Continuidad: plan de nueva sesión guardado, investigación no iniciada

El usuario pidió cerrar la sesión con el plan guardado y un prompt para iniciar una nueva sesión. Autorizó mediante selección expresa documentación y anexos agregados oficiales DANE, exclusivamente para verificar versiones. Las bases ICFES y microdatos siguen excluidos. Esta entrega guarda instrucciones; no ejecuta la investigación.

Leer PLAN_NUEVA_SESION.md para el alcance completo y usar PROMPT_NUEVA_SESION.md para arrancar. Solo se crearon este paquete, partida, manifiesto y verificador propios. No se realizaron consultas oficiales nuevas, descargas de anexos, cotejos de valores, modelos, escenarios ni objetivo 4. No hay presupuesto heredado ni fecha de predicción aprobada. El cierre científico previo sigue incompleto en procedencia/disponibilidad; no se resolvió en esta sesión de guardado.

Antes de escribir se leyó AGENTS.md y la continuidad documental, se aprobó el verificador documental anterior y se registraron huellas de todos los archivos regulares dentro del universo de exclusiones previo. VERIFICACION_PREVIA.json conserva ese dictamen anterior. El verificador de la entrega anterior usa un inventario cerrado: esta ampliación futura lo excede, aunque sus archivos permanezcan idénticos. Se conserva intacto; no afirmar que aprueba el inventario ampliado. La conservación actual se comprueba con verificar_plan.py, sin modificar controles históricos.

Al comenzar la nueva sesión: verificar este paquete con `python3 -B verificar_plan.py`, preservar sus archivos y registrar una nueva partida antes de escribir en investigacion/. Si ya existe investigación, leer su continuidad y no sobrescribir su estado. El verificador de este paquete también tiene inventario cerrado y su aprobación de arranque debe registrarse antes de añadir la investigación; controles nuevos separados deben comprobar la ampliación posterior.

No modificar continuidades superiores, tesis, resultados previos, runtime compartido ni .git. No commit/push. No avance automático. La aprobación de conservación no autentica fuentes oficiales ni certifica disponibilidad histórica. Pendiente: ejecutar únicamente la investigación documental descrita en una nueva sesión, y cerrar con evidencia y pendientes antes de cualquier autorización experimental.
''')
dump(OUT/'VERIFICACION_PREVIA.json', dict(aprobado_integridad_documental=True, solo_lectura=True, archivos_previos_comprobados=38962, archivos_entrega_comprobados=44, fuentes_autenticadas=False, disponibilidad_valores_locales_certificada=False, pares_certificados=0, contexto='Resultado de python3 -B verificar_documental.py antes de crear esta carpeta; no dictamen posterior del inventario ampliado.'))
sources=OUT/'fuentes'
sources.mkdir()
(sources/'guardar_plan.py').write_bytes(Path(__file__).read_bytes())
excl=['MANIFIESTO_PLAN.json','VERIFICACION_PLAN.json']
dump(OUT/'MANIFIESTO_PLAN.json',dict(fecha_utc=stamp,sha256={p.relative_to(OUT).as_posix():sha(p) for p in OUT.rglob('*') if p.is_file() and p.name not in excl},exclusiones=excl))
dump(OUT/'VERIFICACION_PLAN.json', dict(estado='pendiente_de_verificacion', aprobado=False))
result=subprocess.run([sys.executable,'-B',str(OUT/'verificar_plan.py')],check=True,capture_output=True,text=True)
dump(OUT/'VERIFICACION_PLAN.json',json.loads(result.stdout))
print(result.stdout)
