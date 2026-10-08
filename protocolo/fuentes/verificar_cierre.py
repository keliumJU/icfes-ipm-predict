"""Verificación de cierre fase 2, preservación de originales y manifiesto de huellas."""
import ast
import copy
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from configuracion import COMMIT_PARTIDA, DESARROLLO, REEVALUACION, candidatos
from controles import ROOT, EVIDENCIA, huella, verificar
from generar_notebooks import construir, validar, DESTINO


def main():
    assert sys.flags.optimize == 0, "No ejecutar controles con -O"
    actual = verificar()
    registrado = json.loads((EVIDENCIA / "verificacion_fase2.json").read_text())
    assert actual == registrado, "Regenerar evidencia con el mismo entorno"
    assert json.loads((EVIDENCIA / "candidatos_congelados.json").read_text()) == list(candidatos())
    notebook = json.loads(DESTINO.read_text())
    validar(notebook)
    assert construir() == notebook, "Notebook distinto de su fuente"
    nb_evidencia = json.loads((EVIDENCIA / "verificacion_notebook.json").read_text())
    assert huella(DESTINO) == nb_evidencia["notebook_sha256"]
    assert huella(ROOT / nb_evidencia["fuente"]) == nb_evidencia["fuente_sha256"]
    # Controles negativos sobre el validador, sin tocar artefactos distribuidos.
    rechazados = []
    for caso in ("ids_repetidos", "salida_incrustada", "codigo_invalido"):
        roto = copy.deepcopy(notebook)
        codigo = next(c for c in roto["cells"] if c["cell_type"] == "code")
        if caso == "ids_repetidos":
            roto["cells"][1]["id"] = roto["cells"][0]["id"]
        elif caso == "salida_incrustada":
            codigo["outputs"] = [{"text": "salida no autorizada"}]
        else:
            codigo["source"] = ["def :"]
        try:
            validar(roto)
        except (AssertionError, SyntaxError):
            rechazados.append(caso)
        else:
            raise AssertionError(f"El validador aceptó {caso}")
    originales = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", COMMIT_PARTIDA], cwd=ROOT, text=True).splitlines()
    originales = [p for p in originales if p != "CONTINUIDAD_OBJETIVO_3.md"]
    # Compara contenido de los archivos versionados de partida, no recensa datasets ignorados.
    subprocess.run(["git", "diff", "--quiet", COMMIT_PARTIDA, "--", *originales], cwd=ROOT, check=True)
    for nombre in ("PROTOCOLO_OBJETIVO_3.md", "decisiones_fase2.md", "README.md"):
        assert (ROOT / "protocolo" / nombre).is_file()
    continuidad = (ROOT / "CONTINUIDAD_OBJETIVO_3.md").read_text()
    assert "fase 2 cerrada" in continuidad and "132" in continuidad and "66" in continuidad
    assert not set(DESARROLLO) & set(REEVALUACION)
    fuentes = sorted((ROOT / "protocolo/fuentes").glob("*.py"))
    for fuente in fuentes:
        tree = ast.parse(fuente.read_text())
        # Solo controles/configuración: una llamada de entrenamiento/simulación no debe aparecer.
        assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                       and n.func.attr in {"fit", "fit_transform", "predict", "simulate"}
                       for n in ast.walk(tree)), fuente
    archivos = [ROOT / "CONTINUIDAD_OBJETIVO_3.md", DESTINO,
                *sorted((ROOT / "protocolo").glob("*.md")), *fuentes,
                EVIDENCIA / "verificacion_fase2.json", EVIDENCIA / "candidatos_congelados.json",
                EVIDENCIA / "verificacion_notebook.json"]
    resultado = {"fecha_cliente": "2026-10-08", "commit_partida": COMMIT_PARTIDA,
                 "fase2_cerrada": True, "originales_versionados_sin_cambios": len(originales),
                 "control_negativo_notebook_rechazado": rechazados,
                 "fuentes_python_sintaxis_valida": len(fuentes),
                 "notebook_reproducible_desde_fuente": True,
                 "modelos_entrenados": 0, "simulaciones_ejecutadas": 0,
                 "decisiones_indispensables_pendientes": [],
                 "entregables_sha256": {str(p.relative_to(ROOT)): huella(p) for p in archivos}}
    (EVIDENCIA / "manifiesto_cierre.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: resultado[k] for k in ["fase2_cerrada", "originales_versionados_sin_cambios",
                                              "notebook_reproducible_desde_fuente"]}))


if __name__ == "__main__":
    main()
