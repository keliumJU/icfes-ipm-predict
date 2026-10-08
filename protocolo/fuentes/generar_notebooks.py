"""Genera y verifica nuestro subconjunto de nbformat 4.5 sin dependencias externas.

Solo admite celdas Markdown/code sin salidas; nunca genera etapas no autorizadas.
No sustituye un validador JSON Schema completo de nbformat para notebooks arbitrarios.
"""
import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FUENTE = ROOT / "protocolo/fuentes/01_protocolo_controles.py"
DESTINO = ROOT / "notebooks/01_protocolo_controles.ipynb"


def construir():
    partes = re.split(r"^# %%([^\n]*)\n", FUENTE.read_text(encoding="utf-8"), flags=re.M)
    assert partes[0] == ""
    celdas = []
    for indice in range(1, len(partes), 2):
        marcador, fuente = partes[indice:indice + 2]
        markdown = marcador.strip() == "[markdown]"
        if markdown:
            assert all(linea.startswith("#") or not linea for linea in fuente.splitlines())
            fuente = "\n".join(linea.removeprefix("# ").removeprefix("#")
                                for linea in fuente.splitlines()) + "\n"
        else:
            assert marcador.strip() == ""
            ast.parse(fuente)
        celda = {"cell_type": "markdown" if markdown else "code", "metadata": {},
                 "id": hashlib.sha256(f"{indice}:{fuente}".encode()).hexdigest()[:12],
                 "source": fuente.splitlines(keepends=True)}
        if not markdown:
            celda.update(execution_count=None, outputs=[])
        celdas.append(celda)
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}}, "cells": celdas}


def validar(nb):
    assert set(nb) == {"nbformat", "nbformat_minor", "metadata", "cells"}
    assert nb["nbformat"] == 4 and nb["nbformat_minor"] == 5
    assert isinstance(nb["metadata"], dict) and isinstance(nb["cells"], list) and nb["cells"]
    ids = []
    for celda in nb["cells"]:
        tipo = celda["cell_type"]
        assert tipo in ("markdown", "code")
        campos = {"cell_type", "metadata", "id", "source"}
        if tipo == "code":
            campos |= {"execution_count", "outputs"}
            assert celda["execution_count"] is None and celda["outputs"] == []
            ast.parse("".join(celda["source"]))
        assert set(celda) == campos and isinstance(celda["metadata"], dict)
        assert isinstance(celda["source"], list) and all(isinstance(v, str) for v in celda["source"])
        assert re.fullmatch(r"[A-Za-z0-9_-]{1,64}", celda["id"])
        ids.append(celda["id"])
    assert len(set(ids)) == len(ids)


def main():
    nb = construir()
    validar(nb)
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    relectura = json.loads(DESTINO.read_text(encoding="utf-8"))
    validar(relectura)
    assert relectura == nb
    # Verificación real, secuencial de las celdas; no se incrustan salidas en .ipynb.
    espacio = {"__name__": "__notebook_control__"}
    for celda in nb["cells"]:
        if celda["cell_type"] == "code":
            exec(compile("".join(celda["source"]), str(DESTINO), "exec"), espacio)
    evidencia = {"fuente": str(FUENTE.relative_to(ROOT)), "notebook": str(DESTINO.relative_to(ROOT)),
                 "fuente_sha256": hashlib.sha256(FUENTE.read_bytes()).hexdigest(),
                 "notebook_sha256": hashlib.sha256(DESTINO.read_bytes()).hexdigest(),
                 "formato": "4.5; subconjunto sin salidas validado por generar_notebooks.validar",
                 "celdas": len(nb["cells"]), "celdas_codigo_ejecutadas": 3,
                 "ejecucion": "compile/exec secuencial; no kernel Jupyter", "outputs_distribuidos": 0}
    (ROOT / "protocolo/evidencia/verificacion_notebook.json").write_text(
        json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
