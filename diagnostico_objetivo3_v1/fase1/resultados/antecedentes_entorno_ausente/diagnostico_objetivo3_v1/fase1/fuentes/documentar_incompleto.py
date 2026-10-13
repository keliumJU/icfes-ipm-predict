"""Documenta el bloqueo obligatorio, conserva antecedente y sella SOLO diagnóstico.

Biblioteca estándar, sin estadísticas, imports experimentales, fits o carga de modelos.
No cierra la fase como aceptada. No sobrescribe resultados de una ejecución previa.
"""
import hashlib
import json
from pathlib import Path

from preflight_documental import ROOT, OWN, ENV, git, sha, verify

F1 = OWN / "fase1"
RESULTS = F1 / "resultados"


def save(name, content):
    p = OWN / name
    if not p.resolve().is_relative_to(OWN.resolve()):
        raise RuntimeError("Destino prohibido")
    for parent in [p, *p.parents]:
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise RuntimeError("Symlink prohibido")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("x") as stream:
        if isinstance(content, str):
            stream.write(content)
        else:
            json.dump(content, stream, indent=2, ensure_ascii=False)
            stream.write("\n")


def main():
    pf = json.loads((RESULTS / "preflight_documental_final/preflight.json").read_text())
    prep = json.loads((OWN / "REGISTRO_PREPARACION.json").read_text())
    if ENV.exists() or not pf["preflight_documental_aprobado"]:
        raise RuntimeError("Revisar bloqueo antes de documentar")
    old = (OWN / "CONTINUIDAD_DIAGNOSTICO.md").read_text()
    expected = prep["sha256_documentos"]["diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md"]
    assert hashlib.sha256(old.encode()).hexdigest() == expected
    save("fase1/README.md", """# Diagnóstico objetivo3 v1 — fase1 INCOMPLETA

Fecha cliente: 2026-10-11, America/Bogota. El usuario envió expresamente el prompt
y autorizó el diagnóstico sin nuevos fits. Se inició únicamente revisión documental.
No se ha satisfecho la aceptación del plan §4.

Bloqueo: `/tmp/icfes-v2-fase2-venv/bin/python` no existe. El prompt §1 y
PLAN_DIAGNOSTICO.md §2 exigen documentar y consultar sin instalar ni descargar.
Se consultó al usuario por una ruta alternativa del entorno exacto o conservación
del estado incompleto. No sustituirlo por el Python anfitrión para los cálculos.

Entregables actuales:

- `PROTOCOLO_DIAGNOSTICO.md`: alcance vigente y controles pendientes.
- `INFORME_DIAGNOSTICO.md` y `registro_hallazgos.md`: comprobaciones documentales,
  impacto, alternativas y pendientes; ninguna conclusión estadística.
- `fuentes/preflight_documental.py`: huellas/Git/índice; biblioteca estándar.
- `fuentes/documentar_incompleto.py`: documentación, conservación y manifiesto.
- `resultados/preflight_documental_final/`: revisión documental corregida válida,
  entorno no aprobado, inventario protegido y huellas de antecedentes completos.
- `resultados/lecturas.json`, `auditoria_incompleta.json`, `conservacion_final.json`,
  `manifiesto_incompleto.json`, `verificacion_manifiesto.json`.
- Los cuatro JSON en la raíz de `resultados/` son la comprobación preliminar
  rechazada por interpretación incorrecta de la base del índice. Se conservan
  como antecedente técnico y NO acreditan integridad final.

Orden realmente ejecutado: preflight documental preliminar → corrección de base
relativa del índice → preflight documental final → documentación incompleta.
No volver a ejecutar estos generadores contra sus destinos existentes: usan escritura
exclusiva. Una continuación requiere nuevos registros separados y entorno aprobado.

Pendiente: entorno exacto/Python3.12.14/sklearn1.9.1/54paquetes/pip check; reconstrucción
en memoria/cotejo íntegro, análisis A–E, pruebas inventadas, auditoría aritmética,
tablas completas, gráficos y notebook diagnóstico ejecutado/validado. No se crearon
tablas ni notebook vacíos presentados como resultados. Fuente/derivado solo cotejados
por huella; 4752filas únicas continúa siendo expectativa condicionada no comprobada.
Sin commit, push, instalación, descarga, fit, carga de modelos o avance de v5.
""")
    save("fase1/PROTOCOLO_DIAGNOSTICO.md", """# Protocolo diagnóstico 1.0 — controles iniciales; ejecución incompleta

Fecha cliente2026-10-11,America/Bogota. Contrato metodológico completo vigente:
`../PLAN_DIAGNOSTICO.md` §§1–5 (SHA256
4c33307f11ec2da96ea108faf12a1eb44ba52eb805e7fd7ed9ad445eae6e7fe2).
Autorización actual: prompt enviado expresamente por el usuario; solo diagnóstico
con datos/predicciones guardados, sin nuevos fits. Separado de etapa3v5.

Decisiones del usuario intactas: poblaciónESTUDIANTE/no libertadS/grado11/seis
puntajes positivos presentes/sin calendario; media recibida/geografía colegio/peso
igualterritorio-año;2020excluido/2018historial/2021previo2019/sin anualizar.
Entradas unión exacta GRUPOSv5; año/código/intervalo únicamente descripción y llaves.
Objetivo original, criterios/selecciones v5 conservados. Fuente única v2 y derivado
v5 en plan §2. No fuentes adicionales, raw, modelos deserializados ni nuevos ajustes.

Comprobaciones actuales: HEAD/rama/ascendencia y ausencia de trabajo posterior;
tres huellas documentales de preparación, inventario protegido, manif./congelación/
controles/índice/fuentes/selecciones por huellas. Continuidad histórica v5 etapa1
cotejada exclusivamente en Git109797407d75d2097e5b71f8bcef3fc266bc61d2;
sin excepciones para otros archivos. Índice relativo a piloto/ por contrato original
`experimentos_objetivo3_v5/etapa2/fuentes/piloto.py`, líneas74–97, leído sin importar.

Decisión nueva de implementación: scripts propios stdlib para verificación documental,
destinos exclusivos en fase1 y guardias contra symlinks; registro preliminar conservado
y revisión corregida aparte. Python anfitrión solo Git/JSON/SHA; no sustituye entorno
experimental. No semilla aplicada: no se efectuó procedimiento aleatorio.

El entorno exigido está ausente. No se inicia análisis A–E ni controles inventados.
Las fórmulas, particiones, rangos medios, cuantiles lineales, ddof1, exactitud CSV,
tolerancia de acumuladores y linaje permanecen en plan §3; no se cambian tras resultados.
Acceptance plan§4 PENDIENTE. Nombres de tablas finales serán documentados al generarlas,
no hay resultados inexistentes. Notebook/generador diagnóstico pendientes.

Advertencias históricas conservadas: Guainía238vs404/21.012106puntos
(v2/fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local no autenticada,
IPMhogares/alumnos,colegio/residencia/enlaceecológico,pocosaños/dependencia temporal
territorial.2021–2025vistos:exploratorio,sinconfirmaciónindependiente/causalidad/
pronósticoanticipadodemostrado. Antecedentes archivados sin nueva conexión no se reabren.
""")
    save("fase1/INFORME_DIAGNOSTICO.md", """# Informe de estado — diagnóstico INCOMPLETO, sin análisis ejecutado

Fecha cliente2026-10-11,America/Bogota. La fase no cumple aceptación del plan§4.
El intérprete exigido no existe; Python/versiones54paquetes/sklearn/pip check NO
verificados. Evidencia: resultados/preflight_documental_final/entorno.json.
Se solicitó al usuario una ruta alternativa exacta o mantener estado incompleto.
No instalar/descargar ni calcular con otro entorno sin resolver ese control.

Verificaciones actuales: resultados/preflight_documental_final/preflight.json,
inventario_protegido_verificado.json y huellas_antecedentes.json. HEAD75c3a25182af363f47b0d743820f99084e18fed5,
asunto exacto y rama codex/objetivo3-v5-mae; no trabajo posterior ni cambios versionados.
29640huellas protegidas idénticas; tres documentos de preparación válidos ANTES de
actualizar continuidad propia. Manifiesto v5etapa2:6869huellas; etapa1:98,
continuidad etapa1 cotejada en su commit real. Índice2174huellas/coberturaexacta,
congelaciones40/55,fuentesdecontroles2/8/contexto8,cinco selecciones y fuente/derivado
cotejados por SHA, sin regenerar ni deserializar modelos.

La primera verificación propia del índice falló por base de rutas incorrecta;
el contrato piloto.py:74–97 muestra base piloto/. Se corrigió solo el verificador
propio y se conservó el registro fallido, sin modificar artefactos históricos.
No es una incidencia de integridad de v5 ni una nueva hipótesis explicativa.

Resultados históricos, NO diagnóstico actual: v5 metaNOsatisfecha, mejora0.0%,
MAE3.429267191379531,11880internas/1155externas; registrados en continuidad propia
antecedente y v5/etapa2/resultados/meta.json/manifiesto. No se recalcularon aquí.
231filas/33territorios/198cambios y4752únicas continúan pendientes de comprobación
actual en memoria/linaje. No afirmar resultados diagnósticos a partir de expectativas.

Hipótesis estabilidad temporal/capacidadinformativa/recencia/simplificación/máshistoria:
insuficientemente evaluadas en esta sesión. Ninguna alternativa nueva justificada;
esto significa ausencia de evaluación, no evidencia de inutilidad. Persistencia sigue
siendo referencia contractual; no se seleccionó otro candidato retrospectivamente.
No causa definitiva, mejora prometida ni pronóstico demostrado. Hallazgos administrativos,
impacto/alternativas/resoluciones en registro_hallazgos.md.

Pendientes indispensables: resolver entorno, reconstrucción exacta, análisis A–E,
pruebasinventadas/cobertura/aritmética independiente/copias/linaje y aceptación íntegra,
tablas/gráficos/notebook ejecutado. No se cierra el diagnóstico como logrado.
No fase posterior ni protocolo/grilla de entrenamiento nuevos. Cero fits/cargasmodelos/
instalaciones/descargas/búsquedas/commits/push. PDFs actuales0páginas.
""")
    save("fase1/registro_hallazgos.md", """# Registro de hallazgos documentales y bloqueo

|ID/ubicación verificable|n/evidencia|Impacto|Alternativa y resolución|Pendiente|
|---|---|---|---|---|
|D-01 preflight_documental_final/entorno.json/ruta_exigida|1ruta ausente; versiones no verificadas|Impide ejecutar controles y análisis bajo contrato|Consultar ruta alternativa exacta; documentar incompleto sin instalar|Respuesta y verificación Python3.12.14/54paquetes/sklearn1.9.1/pip check|
|D-02 preflight.json/git e inventario_protegido_verificado.json|29640huellas,HEAD/asunto/rama esperados|Permite preservar partida real y trabajar separado de v5|Reusar rama sin reset; todas huellas actuales iguales|Ninguno documental; conservar otra vez al cierre|
|D-03 resultados/huellas_antecedentes.json (preliminar); revisión final; piloto.py:74–97|2174entradas relativas a piloto/|Base errónea en verificador propio produce falso rechazo|Corregir base con contrato leído, conservar salida preliminar; todas huellas/cobertura final exactas|No reabrir v5 por este error propio|
|D-04 preflight.json/documentos_preparacion; continuidad propia|3huellas válidas antes de actualización|Preparación no era ejecución diagnóstica|Registrar autorización actual y conservar antecedente íntegro|Diagnóstico completo pendiente|

No hallazgos estadísticos. Matriz de hipótesis A–E pendiente; todas las hipótesis
descriptivas están insuficientemente evaluadas, sin evidencia nueva a favor/en contra.
Las advertencias activas y antecedentes archivados permanecen en protocolo/continuidad;
no nueva conexión que justifique reabrirlos. No cierre de controles indispensables.
""")
    reads = {"pdf_actuales": {"paginas": 0, "archivos": []},
             "agentes": {"archivo": "AGENTS.md", "lineas": "1–12", "lectura": "completa"},
             "continuidad_propia": {"archivo": "diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md",
                                    "lineas_preparacion": "1–93", "lectura": "completa antes de escritura"},
             "plan_propio": {"archivo": "diagnostico_objetivo3_v1/PLAN_DIAGNOSTICO.md",
                             "secciones": "1–5", "lineas": "1–226"},
             "continuidades_vigentes": {"v2": "1–100", "v3": "1–110", "v4": "1–115", "v5": "1–95"},
             "documentos_v5": ["etapa1/PROTOCOLO_V5.md completo (5.0.0)",
                               "etapa1/README.md", "etapa1/INFORME_CIERRE.md", "etapa1/registro_problemas.md",
                               "etapa2/README.md", "etapa2/INFORME_PILOTO.md", "etapa2/registro_problemas.md",
                               "etapa2/PROTOCOLO_OPERATIVO.md"],
             "json_actuales": "Registro preparación completo por código y resumen; manifiestos/congelaciones/controles/contexto/índice por estructura y huellas completas; configuraciones por estructura; selecciones por SHA",
             "lock": "v4/etapa1/requirements.lock.txt completo,54líneas; solo contrato, no entorno validado",
             "codigo_historico": "piloto.py v5etapa2 coincidencias rg líneas74–97 para base índice; no importado ni ejecutado",
             "incidencia_lecturas": "Consulta inicial conjunta truncada por inventario extenso; relecturas acotadas de continuidad propia/plan/continuidades vigentes/documentos v5. No atribuir lectura íntegra nueva de antecedentes históricos omitidos.",
             "historicas": "Advertencias Guainía/etc. heredadas de continuidades; no nuevo cálculo ni lectura PDF",
             "pendientes": "Defaults completos/configuraciones/metadatos semánticos/CSV/linaje/reconstrucción aún sin análisis; no atribuir auditoría semántica a SHA",
             "planes_posteriores": "No solicitados; no entrenamiento posterior ejecutado"}
    save("fase1/resultados/lecturas.json", reads)
    save("fase1/resultados/auditoria_incompleta.json", {
        "fase_aceptada": False, "documental_aprobado": True, "entorno_aprobado": False,
        "reconstruccion": "pendiente", "analisis_A_E": "pendiente",
        "pruebas_plan_4": "NO ejecutadas", "aritmetica_independiente": "NO ejecutada",
        "notebook": "NO creado ni ejecutado", "fits": 0, "modelos_cargados": 0,
        "diferencia_preliminar_resuelta": "base índice piloto.py:74–97; registros finales separados",
        "consulta_usuario": "Ruta alternativa exacta o conservar incompleto; respuesta pendiente al documentar",
        "pendientes_indispensables": ["entorno", "reconstrucción", "cobertura/linaje", "análisis A–E",
                                     "pruebas/aritmética", "tablas/gráficos/notebook", "aceptación plan§4"]})
    prefix = """# Continuidad diagnóstico objetivo3 v1 — INCOMPLETO por entorno ausente

Fecha cliente2026-10-11,America/Bogota. Usuario envió expresamente prompt y autorizó
diagnóstico separado, SOLO datos/predicciones guardados/sin nuevosfits. Se realizó
únicamente verificación documental inicial. No se alcanzó aceptación plan§4.

Control obligatorio detenido: /tmp/icfes-v2-fase2-venv/bin/python NO existe.
Python3.12.14/sklearn1.9.1/54paquetes/pip check no revalidados. No instalar/descargar
ni sustituir por Pythonanfitrión para cálculos. Consulta enviada por herramienta:
ruta alternativa exacta o conservar incompleto; respuesta pendiente al documentar.
Pythonanfitrión solo stdlib Git/JSON/SHA/documentación, sin cálculos diagnósticos.

HEAD75c3a25182af363f47b0d743820f99084e18fed5/asunto/rama codex/objetivo3-v5-mae/
ascendencia/sintrabajoposterior comprobados; rama reutilizada sin reset/checkout.
Los cuatro documentos propios de preparación no versionados estaban presentes;
tres huellas válidas antes de actualizar esta continuidad.29640versionados intactos.
Manifiestos v5etapa1/etapa2 98/6869huellas,continuidad histórica etapa1 cotejada en
commit109797407d75d2097e5b71f8bcef3fc266bc61d2 sin excepción para otros archivos.
Índice2174huellas/cobertura exacta;congelaciones40/55;controles/contexto/fuentes/
cinco selecciones/fuentev2/derivadov5 por SHA completos. No deserialización ni runners.

Incidencia propia: primera auditoría usó raízproyecto para índice relativo a piloto/;
contrato piloto.py:74–97 resolvió base. Salidas fallidas intactas en fase1/resultados/,
revisión final válida aparte en preflight_documental_final/. Ningún fallo histórico
ni nueva conexión que reabra antecedentes. Lectura conjunta inicial truncada corregida
por consultas acotadas; lecturas reales/pendientes en fase1/resultados/lecturas.json.
PDF0páginas. Defaults/metadatos/CSVsemánticos pendientes; huella no sustituye análisis.

Entregables nuevos: fase1/README,protocolo,informe,registro_hallazgos,fuentes stdlib,
preflight/entorno/lecturas/auditoríaincompleta/conservación/manifiestoincompleto.
No tablas estadíst./gráficos/notebook; no ejecuciones inexistentes. Reconstrucción
enmemoria231/33/198 y4752únicas condicionadas pendientes; no presentarlas como actuales.
Nuevosfits0/modeloscargados0/instalaciones0/descargas0/commits0/push0.

Acuerdos del usuario intactos: población/mediarecibida/colegio/pesoigualterritorio-año,
2020excluido/2018historial/2021previo2019/sinanualizar/objetivooriginal/GRUPOSv5exactos.
No criterios/grillas/selecciones/ledgers cambiados. MetaNOsatisfecha v5 sigue vigente.
Hipótesis estabilidad/capacidadinformativa insuficientemente evaluadas; no alternativa
nueva justificada por esta sesión, ni causa definitiva/mejora prometida.

Pendientes indispensables: entorno exacto → reconstrucción completa/semántica/linaje
→ A–E/pruebasinventadas/aritmética/tablas/gráficos/notebook desde fuente/generador
ejecutado/validado → aceptaciónplan§4. No iniciar experimento sin autorización separada.
Guainía238vs404/21.012106puntos/evidenciahistórica,procedencialocalnoautenticada,
IPMhogares/alumnos,colegio/residencia/enlaceecológico,pocosaños/dependencia temporal-
territorial conservados.2021–2025vistos:exploratorio/sinconfirmaciónindependiente/
causalidad/pronósticoanticipadodemostrado. Antecedentes archivados no reabiertos.

---

## Antecedente íntegro de preparación — no estado operativo actual

"""
    continuity = OWN / "CONTINUIDAD_DIAGNOSTICO.md"
    assert not continuity.is_symlink()
    continuity.write_text(prefix + old)
    protected = verify(prep["inventario_protegido"]["sha256_versionados"])
    conservation = {"aprobado": protected["aprobado"], "n_versionados": protected["n"],
                    "discrepancias": [r for r in protected["archivos"] if not r["igual_actual"]],
                    "head_igual": git("rev-parse", "HEAD").strip() == prep["commit_partida"],
                    "continuidad_propia_antecedente_sha256": hashlib.sha256(old.encode()).hexdigest(),
                    "antecedente_integro": continuity.read_text().endswith(old),
                    "plan_prompt_registro_preparacion_intactos": all(
                        sha(ROOT / n) == h for n, h in pf["cuatro_archivos_iniciales"].items()
                        if not n.endswith("CONTINUIDAD_DIAGNOSTICO.md")),
                    "escrituras_solo_diagnostico": True,
                    "raw_ignorado": "No censado por SHA; ninguna escritura",
                    "modelos": "Solo hashes binarios; no deserialización",
                    "status_final": git("status", "--short").splitlines()}
    assert conservation["aprobado"] and conservation["antecedente_integro"]
    save("fase1/resultados/conservacion_final.json", conservation)
    names = [p for p in OWN.rglob("*") if p.is_file()]
    manifest = {"estado": "INCOMPLETO; NO aceptación plan§4", "fase_aceptada": False,
                "bloqueo": "Entorno exigido inexistente", "commit_partida": prep["commit_partida"],
                "artefactos_sha256": {str(p.relative_to(ROOT)): sha(p) for p in sorted(names)},
                "exclusiones_autorreferencia": ["fase1/resultados/manifiesto_incompleto.json",
                                               "fase1/resultados/verificacion_manifiesto.json"],
                "fits": 0, "push": False}
    save("fase1/resultados/manifiesto_incompleto.json", manifest)
    checked = verify(manifest["artefactos_sha256"])
    save("fase1/resultados/verificacion_manifiesto.json", {
        "aprobado_huellas": checked["aprobado"], "n": checked["n"],
        "manifiesto_sha256": sha(RESULTS / "manifiesto_incompleto.json"),
        "aceptacion_diagnostico": False, "conservacion_aprobada": conservation["aprobado"]})
    print(json.dumps({"estado": "INCOMPLETO", "conservacion": conservation["aprobado"],
                      "huellas_entrega": checked["n"], "manifiesto_verificado": checked["aprobado"]}))


if __name__ == "__main__":
    main()
