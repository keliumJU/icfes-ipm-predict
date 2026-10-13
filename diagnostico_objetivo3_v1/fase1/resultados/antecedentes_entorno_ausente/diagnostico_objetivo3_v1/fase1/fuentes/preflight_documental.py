"""Verificación documental de solo lectura sobre antecedentes; cero cálculos diagnósticos.

Se ejecuta con biblioteca estándar del Python anfitrión, NO como sustituto del
entorno experimental exigido. Solo escribe resultados nuevos en fase1/resultados.
No importa código experimental ni carga modelos. Hashes binarios por bloques.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OWN = ROOT / "diagnostico_objetivo3_v1"
DEST = OWN / "fase1/resultados/preflight_documental_final"
CLOSE = "75c3a25182af363f47b0d743820f99084e18fed5"
ENV = Path("/tmp/icfes-v2-fase2-venv/bin/python")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git(*args, binary=False):
    return subprocess.check_output(["git", *args], cwd=ROOT,
                                   text=not binary)


def read(path):
    return json.loads((ROOT / path).read_text())


def safe_new_json(name, value):
    target = DEST / name
    for parent in [OWN, *target.relative_to(OWN).parents]:
        candidate = parent if parent.is_absolute() else OWN / parent
        if candidate.is_symlink():
            raise RuntimeError(f"Destino symlink prohibido: {candidate}")
    if not target.resolve().is_relative_to(OWN.resolve()) or target.is_symlink():
        raise RuntimeError("Destino fuera del diagnóstico")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x") as out:
        json.dump(value, out, indent=2, ensure_ascii=False)
        out.write("\n")


def verify(mapping, historical=None):
    rows = []
    for name, expected in mapping.items():
        p = ROOT / name
        actual = sha(p) if p.is_file() else None
        row = {"archivo": name, "sha256_esperado": expected,
               "sha256_actual": actual, "igual_actual": actual == expected}
        if actual != expected and historical and name == historical[0]:
            content = git("show", f"{historical[1]}:{name}", binary=True)
            row["commit_historico"] = historical[1]
            row["sha256_historico"] = hashlib.sha256(content).hexdigest()
            row["igual_historico"] = row["sha256_historico"] == expected
        rows.append(row)
    return {"n": len(rows), "aprobado": all(
        r["igual_actual"] or r.get("igual_historico", False) for r in rows),
        "archivos": rows}


def main():
    prep = read("diagnostico_objetivo3_v1/REGISTRO_PREPARACION.json")
    initial = {n: sha(ROOT / n) for n in prep["archivos_creados"]}
    documents = verify(prep["sha256_documentos"])
    protected = verify(prep["inventario_protegido"]["sha256_versionados"])
    current_tracked = set(git("ls-files", "-z").split("\0")) - {""}
    protected_names = set(prep["inventario_protegido"]["sha256_versionados"])
    protected["inventario_git_identico"] = current_tracked == protected_names
    head = git("rev-parse", "HEAD").strip()
    git_info = {"head": head, "asunto": git("show", "-s", "--format=%s", "HEAD").strip(),
                "rama": git("branch", "--show-current").strip(),
                "status_por_archivo": git("status", "--short", "--untracked-files=all").splitlines(),
                "trabajo_posterior": git("log", "--format=%H %s", f"{CLOSE}..HEAD").splitlines(),
                "cierre_ancestro": subprocess.run(["git", "merge-base", "--is-ancestor", CLOSE,
                                                     "HEAD"], cwd=ROOT).returncode == 0,
                "coincide_cierre": head == CLOSE}
    mappings = [
        ("etapa1/resultados/manifiesto_cierre.json", "entregables_sha256", True),
        ("etapa2/resultados/manifiesto_cierre.json", "entregables_sha256", False),
        ("etapa1/resultados/congelacion_previa.json", "artefactos_sha256", False),
        ("etapa2/resultados/congelacion_operativa.json", "artefactos_sha256", False),
        ("etapa2/resultados/piloto/indice_integridad.json", "archivos_sha256", False),
        ("etapa1/resultados/controles.json", "fuentes_sha256", False),
        ("etapa2/resultados/controles.json", "fuentes_sha256", False),
        ("etapa2/resultados/piloto/contexto.json", "fuentes_sha256", False),
    ]
    historic = ("experimentos_objetivo3_v5/CONTINUIDAD_V5.md",
                "109797407d75d2097e5b71f8bcef3fc266bc61d2")
    checks = {}
    for suffix, key, past in mappings:
        name = "experimentos_objetivo3_v5/" + suffix
        mapping = read(name)[key]
        if suffix.endswith("indice_integridad.json"):
            # Contrato original piloto.py:74–97: claves relativas a self.out.
            base = Path(name).parent
            checks[name] = verify({str(base / n): h for n, h in mapping.items()})
            actual_names = {str(p.relative_to(ROOT / base)) for p in (ROOT / base).rglob("*")
                            if p.is_file() and p.name != "indice_integridad.json"}
            checks[name]["base_claves"] = str(base)
            checks[name]["cobertura_exacta"] = actual_names == set(mapping)
            checks[name]["aprobado"] &= checks[name]["cobertura_exacta"]
        else:
            checks[name] = verify(mapping, historic if past else None)
    source_map = {
        "experimentos_objetivo3_v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv":
            prep["comprobaciones_actuales"]["fuente_sha256"],
        "experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv":
            prep["comprobaciones_actuales"]["derivado_sha256"],
        "experimentos_objetivo3_v5/etapa2/resultados/manifiesto_cierre.json":
            prep["comprobaciones_actuales"]["manifiesto_v5_sha256"],
    }
    sources = verify(source_map)
    selections = verify(prep["comprobaciones_actuales"]["selecciones_sha256"])
    lock = ROOT / "experimentos_objetivo3_v4/etapa1/requirements.lock.txt"
    env = {"ruta_exigida": str(ENV), "existe": ENV.exists(),
           "lock": str(lock.relative_to(ROOT)), "lock_sha256": sha(lock),
           "paquetes_exigidos": len(lock.read_text().splitlines()),
           "python_exigido": "3.12.14", "sklearn_exigido": "1.9.1",
           "version_python_verificada": False, "paquetes_verificados": False,
           "pip_check_ejecutado": False, "aprobado": False,
           "motivo": "Ruta exigida inexistente; detener cálculos y consultar al usuario",
           "instalaciones": 0, "descargas": 0,
           "python_documental": sys.version, "rol_python_documental": "stdlib: Git/JSON/SHA, sin análisis"}
    safe_new_json("entorno.json", env)
    safe_new_json("inventario_protegido_verificado.json", protected)
    safe_new_json("huellas_antecedentes.json", checks)
    approved = (documents["aprobado"] and protected["aprobado"]
                and protected["inventario_git_identico"] and sources["aprobado"]
                and selections["aprobado"] and all(c["aprobado"] for c in checks.values())
                and git_info["coincide_cierre"] and git_info["cierre_ancestro"])
    preflight = {"fecha_cliente": "2026-10-11", "timezone": "America/Bogota",
                 "estado": "INCOMPLETO: entorno obligatorio ausente",
                 "preflight_documental_aprobado": approved, "calculos_autorizados_por_controles": False,
                 "git": git_info, "preparacion_estado_historico": prep["estado"],
                 "preparacion_sha256": sha(ROOT / "diagnostico_objetivo3_v1/REGISTRO_PREPARACION.json"),
                 "documentos_preparacion": documents, "cuatro_archivos_iniciales": initial,
                 "fuentes_solo_huella": sources, "selecciones_solo_huella": selections,
                 "reconstruccion_en_memoria": "PENDIENTE; entorno no aprobado",
                 "estadisticas_predicciones_linaje_notebook": "PENDIENTES; no ejecutados",
                 "fits": 0, "modelos_deserializados": 0, "commits": 0,
                 "pip_check": "NO ejecutado: intérprete exigido inexistente"}
    safe_new_json("preflight.json", preflight)
    print(json.dumps({"documental_aprobado": approved,
                      "protegidos": protected["n"],
                      "manifiestos_indice_congelacion": {k: {"n": v["n"], "aprobado": v["aprobado"]}
                                                          for k, v in checks.items()},
                      "entorno_aprobado": False}, ensure_ascii=False))


if __name__ == "__main__":
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    main()
