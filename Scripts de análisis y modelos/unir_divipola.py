"""
Unión de datasets por código DIVIPOLA (departamento) y año.

Archivos esperados en la misma carpeta:
  - ipm_departamental_limpio_sin_2020.csv  (separador ';', encoding utf-8-sig)
      columnas clave: codigo_departamento, departamento, anio
  - Saber_11_Listo_2018_2024.csv           (separador ',', encoding utf-8)
      columnas clave: COLE_COD_DEPTO_UBICACION, PERIODO (-> ANIO)

 Genera:
  1) panel_departamento_anio_unido.csv  -> 1 fila por (depto, año): promedios Saber + IPM
  2) (opcional) saber_estudiante_con_ipm.csv -> cada estudiante con su IPM pegado

Uso:
    python unir_divipola.py
    python unir_divipola.py --modo panel
    python unir_divipola.py --modo estudiante
    python unir_divipola.py --modo ambos

Requisito: pip install pandas
"""

import argparse
import os
import re
import sys

import pandas as pd

# --------------------------------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IPM_PATH = os.path.join(BASE_DIR, "ipm_departamental_limpio_sin_2020.csv")
SABER_PATH = os.path.join(BASE_DIR, "Saber_11_Listo_2018_2024.csv")
OUT_PANEL = os.path.join(BASE_DIR, "panel_departamento_anio_unido.csv")
OUT_ESTUDIANTE = os.path.join(BASE_DIR, "saber_estudiante_con_ipm.csv")

COL_DEPTO_SABER = "COLE_COD_DEPTO_UBICACION"
CHUNKSIZE = 300_000


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def limpiar_nombre_col(col: str) -> str:
    """Quita BOM/raros del encabezado."""
    col = str(col).strip()
    col = re.sub(r"^[^A-Za-z0-9_]+", "", col)
    return col.strip().strip("'").strip('"').strip()


def normalizar_divipola_depto(serie: pd.Series) -> pd.Series:
    """Devuelve códigos depto como entero (5, 8, 11, ... 99)."""
    return pd.to_numeric(serie, errors="coerce").astype("Int64")


def periodo_a_anio(serie: pd.Series) -> pd.Series:
    """PERIODO ej. 20182 -> 2018. Toma los primeros 4 dígitos."""
    s = pd.to_numeric(serie, errors="coerce").astype("Int64").astype(str)
    anio = s.str.slice(0, 4)
    return pd.to_numeric(anio, errors="coerce").astype("Int64")


def cargar_ipm(path: str) -> pd.DataFrame:
    print(f"[IPM] Leyendo {path} ...")
    ipm = pd.read_csv(path, encoding="utf-8-sig", sep=";")
    ipm.columns = [limpiar_nombre_col(c) for c in ipm.columns]
    
    if "codigo_departamento" not in ipm.columns:
        raise KeyError(f"No se encontró 'codigo_departamento'. Columnas: {list(ipm.columns)}")
    if "anio" not in ipm.columns:
        raise KeyError(f"No se encontró 'anio'. Columnas: {list(ipm.columns)}")
        
    ipm["codigo_departamento"] = normalizar_divipola_depto(ipm["codigo_departamento"])
    ipm["anio"] = pd.to_numeric(ipm["anio"], errors="coerce").astype("Int64")
    ipm = ipm.dropna(subset=["codigo_departamento", "anio"])
    
    # Redondear columnas de IPM a 2 decimales si son floats
    cols_float = ipm.select_dtypes(include=["float64", "float32"]).columns
    ipm[cols_float] = ipm[cols_float].round(2)
    
    print(f"[IPM] Filas: {len(ipm)} | Años: {sorted(ipm['anio'].dropna().unique().tolist())}")
    return ipm


def detectar_col_periodo(columnas) -> str:
    for c in columnas:
        if "PERIODO" in c.upper():
            return c
    raise KeyError(f"No se encontró columna PERIODO. Columnas: {list(columnas)[:10]}")


def construir_panel_saber(saber_path: str, col_depto: str) -> pd.DataFrame:
    """Agrega Saber 11 a nivel (depto, año) por chunks: promedios + conteos."""
    print(f"[SABER] Agregando por {col_depto} + año (chunks de {CHUNKSIZE}) ...")

    candidatas_promedio = [
        "PUNT_GLOBAL", "PUNT_MATEMATICAS", "PUNT_LECTURA_CRITICA",
        "PUNT_C_NATURALES", "PUNT_SOCIALES_CIUDADANAS", "PUNT_INGLES",
        "PERCENTIL_GLOBAL", "ESTU_INSE_INDIVIDUAL",
    ]

    acumulados_suma = {}
    acumulados_n = {}
    conteos = {}

    preview = pd.read_csv(saber_path, encoding="utf-8", sep=",", nrows=5, engine="c")
    preview.columns = [limpiar_nombre_col(c) for c in preview.columns]
    col_periodo_real = detectar_col_periodo(preview.columns)

    if col_depto not in preview.columns:
        raise KeyError(f"No se encontró '{col_depto}'. Columnas disponibles: {list(preview.columns)[:15]}")

    cols_prom = [c for c in candidatas_promedio if c in preview.columns]
    usecols = [col_periodo_real, col_depto] + cols_prom

    total_filas = 0
    for chunk in pd.read_csv(
        saber_path, encoding="utf-8", sep=",", usecols=lambda c: limpiar_nombre_col(c) in usecols,
        chunksize=CHUNKSIZE, engine="c", low_memory=False,
    ):
        chunk.columns = [limpiar_nombre_col(c) for c in chunk.columns]
        chunk["__anio"] = periodo_a_anio(chunk[col_periodo_real])
        chunk["__depto"] = normalizar_divipola_depto(chunk[col_depto])
        chunk = chunk.dropna(subset=["__anio", "__depto"])
        if chunk.empty:
            continue
        chunk["__anio"] = chunk["__anio"].astype(int)
        chunk["__depto"] = chunk["__depto"].astype(int)
        total_filas += len(chunk)

        grp_n = chunk.groupby(["__depto", "__anio"]).size()
        for k, v in grp_n.items():
            conteos[k] = conteos.get(k, 0) + int(v)

        for c in cols_prom:
            chunk[c] = pd.to_numeric(chunk[c], errors="coerce")
            g = chunk.groupby(["__depto", "__anio"])[c].agg(["sum", "count"])
            for k, row in g.iterrows():
                if k not in acumulados_suma:
                    acumulados_suma[k] = {}
                    acumulados_n[k] = {}
                acumulados_suma[k][c] = acumulados_suma[k].get(c, 0.0) + float(row["sum"] or 0)
                acumulados_n[k][c] = acumulados_n[k].get(c, 0) + int(row["count"] or 0)

        print(f"  ... procesadas {total_filas} filas", end="\r")

    print(f"\n[SABER] Total filas procesadas: {total_filas}")

    # Construir DataFrame panel con REDONDEO y ENTEROS LIMPIOS
    filas = []
    for (depto, anio), n in sorted(conteos.items()):
        fila = {"codigo_departamento": depto, "anio": anio, "n_estudiantes_saber": int(n)}
        for c in cols_prom:
            nval = acumulados_n.get((depto, anio), {}).get(c, 0)
            sval = acumulados_suma.get((depto, anio), {}).get(c, 0.0)
            
            # --- AQUÍ ESTÁ LA CORRECCIÓN: redondeo a 2 decimales y n entero ---
            fila[f"prom_{c.lower()}"] = round(sval / nval, 2) if nval > 0 else None
            fila[f"n_{c.lower()}"] = int(nval) if nval > 0 else 0
            
        filas.append(fila)

    panel = pd.DataFrame(filas).sort_values(["anio", "codigo_departamento"]).reset_index(drop=True)
    return panel


def unir_panel_con_ipm(panel: pd.DataFrame, ipm: pd.DataFrame) -> pd.DataFrame:
    print("[MERGE] Uniendo panel Saber + IPM por (codigo_departamento, anio) ...")

    unido = pd.merge(
        panel, ipm,
        on=["codigo_departamento", "anio"],
        how="outer",
        indicator=True,
        suffixes=("", "_ipm"),
    )
    
    # Reordenar columnas
    cols = ["codigo_departamento", "anio"] + [c for c in unido.columns if c not in ("codigo_departamento", "anio", "_merge")] + ["_merge"]
    unido = unido[cols].sort_values(["anio", "codigo_departamento"]).reset_index(drop=True)

    # Forzar columnas n_* a enteros (Int64 admite nulos sin volverse float con .0)
    for col in unido.columns:
        if col.startswith("n_") or col in ["n_estudiantes_saber", "codigo_departamento", "anio"]:
            unido[col] = pd.to_numeric(unido[col], errors="coerce").astype("Int64")
        elif col.startswith("prom_"):
            unido[col] = pd.to_numeric(unido[col], errors="coerce").round(2)

    return unido


def unir_nivel_estudiante(saber_path: str, ipm: pd.DataFrame, col_depto: str, out_path: str):
    """Pega IPM a cada fila de Saber (many-to-one)."""
    print(f"[ESTUDIANTE] Generando {out_path} por chunks ...")
    preview = pd.read_csv(saber_path, encoding="utf-8", sep=",", nrows=5, engine="c")
    preview.columns = [limpiar_nombre_col(c) for c in preview.columns]
    col_periodo_real = detectar_col_periodo(preview.columns)

    primero = True
    total_in = 0
    for chunk in pd.read_csv(saber_path, encoding="utf-8", sep=",", chunksize=CHUNKSIZE, engine="c", low_memory=False):
        chunk.columns = [limpiar_nombre_col(c) for c in chunk.columns]
        chunk["anio"] = periodo_a_anio(chunk[col_periodo_real]).astype("Int64")
        chunk["codigo_departamento"] = normalizar_divipola_depto(chunk[col_depto])
        total_in += len(chunk)

        merged = chunk.merge(ipm, on=["codigo_departamento", "anio"], how="left", suffixes=("", "_ipm"))
        merged.to_csv(out_path, index=False, mode="w" if primero else "a",
                      header=primero, encoding="utf-8-sig", float_format="%.2f")
        primero = False
        print(f"  ... {total_in} filas escritas", end="\r")

    print(f"\n[ESTUDIANTE] Listo: {out_path}")


def main():
    ap = argparse.ArgumentParser(description="Unir IPM + Saber11 por DIVIPOLA y año")
    ap.add_argument("--modo", choices=["panel", "estudiante", "ambos"], default="panel")
    ap.add_argument("--col-depto", default=COL_DEPTO_SABER)
    ap.add_argument("--ipm", default=IPM_PATH)
    ap.add_argument("--saber", default=SABER_PATH)
    ap.add_argument("--out-panel", default=OUT_PANEL)
    ap.add_argument("--out-estudiante", default=OUT_ESTUDIANTE)
    args = ap.parse_args()

    if not os.path.exists(args.ipm):
        sys.exit(f"No se encontró IPM: {args.ipm}")
    if not os.path.exists(args.saber):
        sys.exit(f"No se encontró Saber: {args.saber}")

    ipm = cargar_ipm(args.ipm)

    if args.modo in ("panel", "ambos"):
        panel = construir_panel_saber(args.saber, args.col_depto)
        unido = unir_panel_con_ipm(panel, ipm)
        
        # Guardar con formato decimal controlado
        unido.to_csv(args.out_panel, index=False, encoding="utf-8-sig", float_format="%.2f")
        print(f"[OK] Panel unido guardado correctamente en: {args.out_panel}")

    if args.modo in ("estudiante", "ambos"):
        unir_nivel_estudiante(args.saber, ipm, args.col_depto, args.out_estudiante)


if __name__ == "__main__":
    main()