"""Limpieza del consolidado FIX (con 20212 normalizado). Universo: solo ESTUDIANTE, sin 2020.

Replica los 4 filtros de limpiarDatos1.py y agrega:
- fail-fast si queda residuo tabulado,
- PERIODO normalizado a string,
- reporte de mermas por periodo y por filtro (CSV + consola) para la evidencia .md.
"""
import numpy as np
import pandas as pd

ARCHIVO_ORIGINAL = "recuperacion_20212/Saber_11_Consolidado_Total_FIX.csv"
ARCHIVO_LIMPIO = "recuperacion_20212/icfes_limpio_FIX_2018_2024.csv"
REPORTE_PERIODO = "recuperacion_20212/mermas_por_periodo.csv"
REPORTE_FILTROS = "recuperacion_20212/mermas_por_filtro.csv"

print("Cargando consolidado FIX...")
df = pd.read_csv(ARCHIVO_ORIGINAL, sep=";", encoding="utf-8-sig", low_memory=False)
if df.shape[1] <= 1:  # fallback por si el archivo viniera en otro encoding
    df = pd.read_csv(ARCHIVO_ORIGINAL, sep=";", encoding="latin-1", low_memory=False)

# FAIL-FAST del bloque tab (causa de la perdida de 20212)
if any("\t" in str(c) for c in df.columns):
    raise ValueError("Consolidado con columna tabular: regenerar con normalizar_txt_icfes.py")

df.columns = df.columns.str.strip().str.lower().str.lstrip("﻿")
total_inicial = len(df)
print(f"Registros iniciales: {total_inicial:,} | Columnas: {df.shape[1]}")

# PERIODO normalizado a string ("20181.0" -> "20181", "20212" -> "20212")
df["periodo"] = df["periodo"].astype(str).str.strip()
df["periodo_norm"] = df["periodo"].str.split(".").str[0]

# 1. Puntaje
df["punt_global"] = pd.to_numeric(
    df["punt_global"].astype(str).str.replace(",", ".", regex=False), errors="coerce"
)
nulos_global = int(df["punt_global"].isna().sum())
ceros_global = int((df["punt_global"] <= 0).sum())
print(f"punt_global nulo/invalido: {nulos_global:,} | <= 0: {ceros_global:,}")

# 2. Departamento en cascada
df["depto_analisis"] = np.nan
for col in ["cole_depto_ubicacion", "estu_depto_reside", "estu_depto_presentacion"]:
    if col in df.columns:
        df["depto_analisis"] = df["depto_analisis"].fillna(df[col])
df["depto_analisis"] = (
    df["depto_analisis"].astype(str).str.upper().str.strip()
    .str.replace("Á", "A", regex=False).str.replace("É", "E", regex=False)
    .str.replace("Í", "I", regex=False).str.replace("Ó", "O", regex=False)
    .str.replace("Ú", "U", regex=False)
    .str.replace("BOGOTA D.C.", "BOGOTA", regex=False)
    .str.replace("BOGOTÁ", "BOGOTA", regex=False)
    .str.replace("BOGOTA D. C.", "BOGOTA", regex=False)
)

# 3. Filtros (misma logica que limpiarDatos1.py)
f_puntaje = (df["punt_global"] > 0) & df["punt_global"].notna()
f_depto = ~df["depto_analisis"].isin(["NAN", "NONE", "", "DESCONOCIDO", "NULL"])
if "estu_estudiante" in df.columns:
    f_est = df["estu_estudiante"].astype(str).str.strip().str.upper() == "ESTUDIANTE"
else:
    f_est = pd.Series(True, index=df.index)
if "estu_privado_libertad" in df.columns:
    f_lib = df["estu_privado_libertad"].fillna("N").astype(str).str.strip().str.upper() != "S"
else:
    f_lib = pd.Series(True, index=df.index)

for nombre, f in [("puntaje", f_puntaje), ("depto", f_depto),
                  ("estudiante", f_est), ("libertad", f_lib)]:
    print(f"incumplen {nombre}: {int((~f).sum()):,}")

condicion_final = f_puntaje & f_depto & f_est & f_lib
df_limpio = df[condicion_final].copy()
total_final = len(df_limpio)
print(f"Conservados: {total_final:,} | Eliminados: {total_inicial - total_final:,}")

# 4. Reportes de mermas
tot = df.groupby("periodo_norm").size().rename("total")
kept = df_limpio.groupby("periodo_norm").size().rename("conservados")
rep = pd.concat([tot, kept], axis=1).fillna(0).astype(int)
rep["eliminados"] = rep["total"] - rep["conservados"]
rep["pct_eliminado"] = (rep["eliminados"] / rep["total"] * 100).round(2)
for nombre, f in [("falla_puntaje", ~f_puntaje), ("falla_depto", ~f_depto),
                  ("falla_estudiante", ~f_est), ("falla_libertad", ~f_lib)]:
    rep[nombre] = df.assign(_f=np.asarray(f)).groupby("periodo_norm")["_f"].sum().astype(int)
rep = rep.sort_index()
rep.to_csv(REPORTE_PERIODO, sep=";", encoding="utf-8-sig")
print(rep.to_string())
rep_filtros = pd.DataFrame({
    "filtro": ["puntaje", "depto", "estudiante", "libertad"],
    "incumplen": [int((~f_puntaje).sum()), int((~f_depto).sum()),
                  int((~f_est).sum()), int((~f_lib).sum())],
})
rep_filtros["pct_sobre_total"] = (rep_filtros["incumplen"] / total_inicial * 100).round(2)
rep_filtros["pct_sobre_eliminados"] = (
    rep_filtros["incumplen"] / (total_inicial - total_final) * 100).round(2)
rep_filtros.to_csv(REPORTE_FILTROS, sep=";", index=False, encoding="utf-8-sig")
print(rep_filtros.to_string(index=False))

# Intersecciones disjuntas de fallo (para el .md)
df["_clave"] = (np.where(f_puntaje, "", "punt+") + np.where(f_depto, "", "depto+")
                + np.where(f_est, "", "est+") + np.where(f_lib, "", "lib+")).astype(str)
inter = df.loc[~condicion_final, "_clave"].value_counts()
print("\nIntersecciones de fallo:")
print(inter.to_string())
inter.to_csv("recuperacion_20212/mermas_intersecciones.csv", sep=";",
             encoding="utf-8-sig", header=["registros"])

# 5. Guardar limpio FIX (sin columna auxiliar)
df_limpio = df_limpio.drop(columns=["periodo_norm", "_clave"], errors="ignore")
df_limpio.to_csv(ARCHIVO_LIMPIO, sep=";", index=False, encoding="utf-8-sig")
print(f"\nGuardado: {ARCHIVO_LIMPIO}")
