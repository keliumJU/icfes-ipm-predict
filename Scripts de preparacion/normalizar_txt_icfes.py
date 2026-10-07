"""Normaliza los .txt originales del ICFES a CSV _limpio.csv unificados.

Paso 1 del pipeline (documenta la transformacion 85 -> 77 columnas que antes era manual):
- Detecta separador (;/tab/,) y encoding (utf-8-sig/latin-1) por archivo.
- Estandariza encabezado a minusculas y selecciona el esquema canonico de 77 columnas
  (excluye: estu_consecutivo, cole_calendario, cole_cod_dane_establecimiento,
   cole_cod_dane_sede, cole_codigo_icfes, estu_etnia, estu_generacione, estu_tieneetnia).
- Escribe con sep=";", encoding utf-8-sig. Excluye 20201/20202 por decision de universo.
- No modifica los .txt originales.
"""
import csv
import glob
import os

DROP_COLS = {
    "estu_consecutivo", "cole_calendario", "cole_cod_dane_establecimiento",
    "cole_cod_dane_sede", "cole_codigo_icfes", "estu_etnia",
    "estu_generacione", "estu_tieneetnia", "estu_pilopaga",  # pilopaga solo existe en 20181
    "estu_grupoetnia",  # columna nueva en 20232/20241/20242, se excluye para esquema 77
}
EXCLUIR = ("20201", "20202")  # universo 2018-2024 sin 2020
SEPS = [";", "\t", ","]
ENCODINGS = ["utf-8-sig", "latin-1"]


def detectar_formato(path):
    for enc in ENCODINGS:
        try:
            with open(path, encoding=enc) as f:
                header = f.readline()
            if not header:
                continue
            for sep in SEPS:
                n = header.count(sep)
                if n >= 70:  # 77-85 columnas esperadas
                    return sep, enc
        except Exception:
            continue
    raise ValueError(f"No se pudo detectar formato de {path}")


def normalizar_archivo(origen, destino, canon=None):
    sep, enc = detectar_formato(origen)
    with open(origen, encoding=enc, newline="") as f:
        reader = csv.DictReader(f, delimiter=sep)
        cols = [(c or "").strip().lower().lstrip("﻿") for c in (reader.fieldnames or [])]
        reader.fieldnames = cols
        if canon is None:
            canon = [c for c in cols if c not in DROP_COLS]
        faltantes = [c for c in canon if c not in cols]
        with open(destino, "w", encoding="utf-8-sig", newline="") as out:
            w = csv.DictWriter(out, fieldnames=canon, delimiter=";",
                              extrasaction="ignore", quoting=csv.QUOTE_MINIMAL)
            w.writeheader()
            n = 0
            for row in reader:
                w.writerow(row)
                n += 1
    return sep, enc, n, canon


def main(carpeta_txt, carpeta_out, patron="Examen_Saber_11_*.txt"):
    os.makedirs(carpeta_out, exist_ok=True)
    archivos = sorted(glob.glob(os.path.join(carpeta_txt, patron)))
    archivos = [a for a in archivos
                if not any(e in os.path.basename(a) for e in EXCLUIR)]
    # canon se toma del primer archivo ; (p. ej. 20182) para fijar orden de 77 cols
    canon = None
    for a in archivos:
        sep, enc = detectar_formato(a)
        if sep == ";":
            with open(a, encoding=enc, newline="") as f:
                r = csv.DictReader(f, delimiter=sep)
                cols = [(c or "").strip().lower().lstrip("﻿") for c in r.fieldnames]
            canon = [c for c in cols if c not in DROP_COLS]
            print(f"Esquema canonico ({len(canon)} cols) tomado de: {os.path.basename(a)}")
            break
    for a in archivos:
        base = os.path.basename(a).replace(".txt", "_limpio.csv")
        dest = os.path.join(carpeta_out, base)
        sep, enc, n, _ = normalizar_archivo(a, dest, canon)
        print(f"{base}: sep={repr(sep)} enc={enc} filas={n:,}")


if __name__ == "__main__":
    main(r"D:\Especializacion\datos y scripts\datos_sin_cambios",
         r"D:\Especializacion\datos y scripts\limpieza_de_datos\recuperacion_20212\insumos_fix")
