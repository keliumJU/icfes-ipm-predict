"""Controles de fase 2 sobre agregados existentes; biblioteca estándar únicamente."""
import csv
import hashlib
import importlib.metadata
import json
import math
import sys
sys.dont_write_bytecode = True
from collections import Counter
from pathlib import Path

from configuracion import (BASE_SHA256, DICCIONARIO_SHA256, COMMIT_PARTIDA, DESARROLLO, DIMENSIONES, ESPECIFICACIONES,
                          REEVALUACION, RESULTADO, SEMILLA, TASAS, VERSION, VENTANAS,
                          candidatos)

ROOT = Path(__file__).resolve().parents[2]
EVIDENCIA = ROOT / "protocolo/evidencia"


def huella(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def leer_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def verificar():
    base = ROOT / "auditoria/base_analitica_departamento_anio.csv"
    diccionario = ROOT / "auditoria/diccionario_base_analitica.csv"
    assert huella(base) == BASE_SHA256, "Cambio de base: detener y justificar antes de evaluar"
    assert huella(diccionario) == DICCIONARIO_SHA256, "Cambio de diccionario"
    columnas, filas = leer_csv(base)
    _, definiciones = leer_csv(diccionario)
    assert columnas == [r["variable"] for r in definiciones]
    assert len(filas) == 198
    llaves = [(r["codigo_departamento"], int(r["anio"])) for r in filas]
    assert len(set(llaves)) == len(llaves)
    assert Counter(a for _, a in llaves) == {a: 33 for a in (*DESARROLLO, *REEVALUACION)}
    territorios = {c for c, _ in llaves}
    assert len(territorios) == 33 and "11" in territorios
    assert all(len(c) == 2 and c.isdigit() for c in territorios)
    assert all({r["codigo_departamento"] for r in filas if int(r["anio"]) == a} == territorios
               for a in (*DESARROLLO, *REEVALUACION))
    assert all(v != "" for r in filas for v in r.values())
    numericas = [v for v in columnas if v not in ("codigo_departamento", "departamento")]
    assert all(math.isfinite(float(r[v])) for r in filas for v in numericas)
    assert all(0 < float(r[RESULTADO]) <= 500 for r in filas)
    assert all(0 <= float(r[v]) <= 100 for r in filas for v in ["ipm", *TASAS])
    conteos = [v for v in columnas if v.startswith("n_")]
    assert all(int(r[v]) > 0 and int(r[v]) == int(r["n_estudiantes_saber"])
               for r in filas for v in conteos)
    assert sum(int(r["n_estudiantes_saber"]) for r in filas) == 2984199
    assert len(TASAS) == len(set(TASAS)) == 15 and len(DIMENSIONES) == 5
    assert [len(v) for v in ESPECIFICACIONES.values()] == [1, 15, 16]
    assert all(set(v) <= set(columnas) and RESULTADO not in v for v in ESPECIFICACIONES.values())
    assert set(TASAS) == set(columnas[columnas.index("ipm") + 1:])
    previa = ROOT / "auditoria/evidencia/actualizacion_20261008"
    validacion = json.loads((previa / "validacion_reconstruccion.json").read_text())
    assert validacion["reconstruccion_validada"] and all(validacion["condiciones"].values())
    assert validacion["filas_base"] == 198 and validacion["suma_registros_base"] == 2984199
    _, cotejos = leer_csv(previa / "cotejo_agregacion_raw_final.csv")
    assert len(cotejos) == 2574 and all(float(r["delta_raw_menos_final"]) == 0 for r in cotejos)
    particiones = []
    for numero, (anios, validacion_anio) in enumerate(VENTANAS, 1):
        entrenamiento = [k for k in llaves if k[1] in anios]
        validacion_llaves = [k for k in llaves if k[1] == validacion_anio]
        assert len(entrenamiento) == 33 * len(anios) and len(validacion_llaves) == 33
        assert not set(entrenamiento) & set(validacion_llaves)
        assert max(anios) < validacion_anio and not set(anios) & set(REEVALUACION)
        particiones.append({"ventana": numero, "entrenamiento": list(anios),
                            "validacion": validacion_anio, "n_entrenamiento": len(entrenamiento),
                            "n_validacion": len(validacion_llaves)})
    candidatos_lista = list(candidatos())
    assert len(candidatos_lista) == len({c["id"] for c in candidatos_lista}) == 67
    paquetes = {}
    for paquete in ("pandas", "numpy", "scikit-learn", "nbformat", "ipykernel"):
        try:
            paquetes[paquete] = importlib.metadata.version(paquete)
        except importlib.metadata.PackageNotFoundError:
            paquetes[paquete] = None
    insumos = [base, diccionario, previa / "validacion_reconstruccion.json",
               previa / "verificacion_cierre.json", previa / "cotejo_agregacion_raw_final.csv",
               ROOT / "auditoria/evidencia/notas_ipm.csv"]
    return {"fecha_cliente": "2026-10-08", "version_protocolo": VERSION,
            "commit_partida": COMMIT_PARTIDA, "base_filas": len(filas), "territorios": 33,
            "registros": 2984199, "cotejos_previos_comprobados": len(cotejos),
            "desarrollo_filas": 132, "reevaluacion_filas": 66, "ventanas": particiones,
            "candidatos_definidos_no_entrenados": len(candidatos_lista), "semilla_futura": SEMILLA,
            "python_actual": sys.version, "paquetes_actuales_no_historicos": paquetes,
            "insumos_sha256": {str(p.relative_to(ROOT)): huella(p) for p in insumos},
            "modelos_entrenados_en_este_procedimiento": 0, "simulaciones_ejecutadas": 0,
            "metricas_evaluacion_calculadas": False, "controles_aprobados": True}


def guardar():
    resultado = verificar()
    EVIDENCIA.mkdir(parents=True, exist_ok=True)
    (EVIDENCIA / "verificacion_fase2.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EVIDENCIA / "candidatos_congelados.json").write_text(
        json.dumps(list(candidatos()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: resultado[k] for k in ("base_filas", "desarrollo_filas", "reevaluacion_filas",
                                               "controles_aprobados")}, ensure_ascii=False))


if __name__ == "__main__":
    guardar()
