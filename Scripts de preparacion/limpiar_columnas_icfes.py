import numpy as np
import pandas as pd
import unicodedata

ARCHIVO_ORIGINAL = "Saber_11_Consolidado_Total.csv"
ARCHIVO_LIMPIO = "icfes_limpio_2018_2024.csv"

print(" Cargando dataset consolidado...")

# Lectura segura con manejo de encoding
try:
    df = pd.read_csv(
        ARCHIVO_ORIGINAL, sep=",", encoding="utf-8-sig", low_memory=False
    )
except Exception:
    df = pd.read_csv(
        ARCHIVO_ORIGINAL, sep=",", encoding="latin-1", low_memory=False
    )

# Normalizar nombres de columnas
df.columns = df.columns.str.strip().str.lower()
print(f" Registros iniciales: {len(df):,} | Columnas: {df.shape[1]}")

# ==========================================
# 1. NORMALIZACIÓN DE PUNTAJE GLOBAL
# ==========================================
print("\n Normalizando puntajes...")
if "punt_global" in df.columns:
    df["punt_global"] = pd.to_numeric(
        df["punt_global"]
        .astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False),
        errors="coerce",
    )

# ==========================================
# 2. CONSOLIDACIÓN INTELIGENTE DE DEPARTAMENTO
# ==========================================
print(" Rescatando departamentos en cascada...")

cols_depto = [
    "cole_depto_ubicacion",
    "estu_depto_reside",
    "estu_depto_presentacion",
]
existentes = [c for c in cols_depto if c in df.columns]

# Reemplazar valores de texto que simulan ser nulos antes de hacer el coalesce
for c in existentes:
    df[c] = df[c].replace(
        ["", "NAN", "NONE", "NULL", "nan", "None", "-"], np.nan
    )

# Coalesce (toma el primer valor válido disponible)
df["depto_analisis"] = df[existentes].bfill(axis=1).iloc[:, 0]


# Función para quitar tildes y caracteres raros
def limpiar_texto(texto):
    if pd.isna(texto):
        return np.nan
    texto = str(texto).strip().upper()
    # Normalizar acentos (á -> a, ó -> o, etc.)
    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    # Estandarizaciones comunes
    if "BOGOTA" in texto:
        return "BOGOTA"
    if "SAN ANDRES" in texto or "PROVIDENCIA" in texto:
        return "SAN ANDRES"
    if texto in ["", "NAN", "NONE", "DESCONOCIDO", "NULL"]:
        return np.nan
    return texto


df["depto_analisis"] = df["depto_analisis"].apply(limpiar_texto)

# ==========================================
# 3. FILTRADO
# ==========================================
print(" Aplicando filtros de calidad...")

# Filtro 1: Puntaje válido > 0
f_puntaje = df["punt_global"].notna() & (df["punt_global"] > 0)

# Filtro 2: Departamento identificado
f_depto = df["depto_analisis"].notna()

# Filtro 3: Privados de la libertad (excluir solo 'S' confirmada)
if "estu_privado_libertad" in df.columns:
    f_libertad = (
        df["estu_privado_libertad"].fillna("N").astype(str).str.upper() != "S"
    )
else:
    f_libertad = pd.Series(True, index=df.index)

df_final = df[f_puntaje & f_depto & f_libertad].copy()

# ==========================================
# 4. REPORTE
# ==========================================
print("\n" + "=" * 50)
print(f" Registros iniciales : {len(df):,}")
print(f" Registros finales   : {len(df_final):,}")
print(f" Filas descartadas   : {len(df) - len(df_final):,}")
print("=" * 50)

# Guardar
df_final.to_csv(ARCHIVO_LIMPIO, sep=";", index=False, encoding="utf-8-sig")
print(f" Guardado exitosamente en '{ARCHIVO_LIMPIO}'")