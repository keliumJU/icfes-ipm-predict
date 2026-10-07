import numpy as np
import pandas as pd

# =========================================================================
# 1. CARGA DEL DATASET
# =========================================================================
file_path = "Examen_Saber_11_limpio_tildes.csv"
print("Cargando dataset... (esto puede tardar unos segundos por el tamaño)")

# low_memory=False ayuda a evitar advertencias de tipos mixtos
df = pd.read_csv(file_path, sep=";", low_memory=False)

# Estandarizar nombres de columnas a mayúsculas
df.columns = df.columns.str.upper().str.strip()

filas_iniciales = len(df)
print(f"Total registros iniciales: {filas_iniciales:,}\n" + "=" * 50)

# =========================================================================
# PASO 1: Población Regular y Estandarización de Llave DIVIPOLA
# =========================================================================
# 1.1 Filtrar nulos (elimina validantes / no regulares)
filas_antes = len(df)
df = df[df["COLE_COD_DEPTO_UBICACION"].notna()].copy()
filas_eliminadas_poblacion = filas_antes - len(df)

# 1.2 [NUEVO] Estandarizar código DIVIPOLA a texto de 2 dígitos (ej: 5 -> '05')
# Vital para que coincida con los códigos del DANE en el cruce futuro
df["COLE_COD_DEPTO_UBICACION"] = (
    df["COLE_COD_DEPTO_UBICACION"]
    .astype(str)
    .str.replace(r"\.0$", "", regex=True)
    .str.strip()
    .str.zfill(2)
)

print(
    f"1. Filtro Población Regular y DIVIPOLA ajustado:"
    f"\n   - Filas eliminadas: {filas_eliminadas_poblacion:,}"
    f"\n   - Filas restantes: {len(df):,}\n"
)

# =========================================================================
# PASO 2: [NUEVO] Creación de Llave Temporal (AÑO)
# =========================================================================
# Extrae el año de 'PERIODO' (ej: '20194' -> 2019) para cruzar con el IPM anual
if "PERIODO" in df.columns:
    df["PERIODO"] = df["PERIODO"].astype(str).str.strip()
    df["ANIO"] = df["PERIODO"].str[:4].astype(int)
    print(f"2. Llave Temporal creada (ANIO): {sorted(df['ANIO'].unique())}\n")

# =========================================================================
# PASO 3: Filtro de Calidad de Puntajes (PUNT_GLOBAL y Materias)
# =========================================================================
# Lista de todas las áreas evaluadas
materias = [
    "PUNT_MATEMATICAS",
    "PUNT_LECTURA_CRITICA",
    "PUNT_C_NATURALES",
    "PUNT_SOCIALES_CIUDADANAS",
    "PUNT_INGLES",
]

filas_antes = len(df)

# Asegurar que el puntaje global sea numérico y mayor a cero
df["PUNT_GLOBAL"] = pd.to_numeric(df["PUNT_GLOBAL"], errors="coerce")
filtro_puntajes = (df["PUNT_GLOBAL"].notna()) & (df["PUNT_GLOBAL"] > 0)

# [NUEVO] Asegurar que las materias no sean nulas ni tengan ceros (anulaciones parciales)
for m in materias:
    if m in df.columns:
        df[m] = pd.to_numeric(df[m], errors="coerce")
        filtro_puntajes = filtro_puntajes & (df[m].notna()) & (df[m] > 0)

df = df[filtro_puntajes].copy()
filas_eliminadas_puntajes = filas_antes - len(df)

print(
    f"3. Filtro Exámenes Anulados / Incompletos / Ceros:"
    f"\n   - Filas eliminadas: {filas_eliminadas_puntajes:,}"
    f"\n   - Filas restantes: {len(df):,}\n"
)

# =========================================================================
# PASO 4: Imputación - COLE_BILINGUE (NULL -> 'N')
# =========================================================================
nulos_bilingue_antes = (
    df["COLE_BILINGUE"].isna().sum() if "COLE_BILINGUE" in df.columns else 0
)

if "COLE_BILINGUE" in df.columns:
    df["COLE_BILINGUE"] = df["COLE_BILINGUE"].fillna("N")
    df["COLE_BILINGUE"] = df["COLE_BILINGUE"].astype(str).str.strip().str.upper()

print(
    f"4. Imputación de Bilingüismo (COLE_BILINGUE):"
    f"\n   - Valores imputados con 'N': {nulos_bilingue_antes:,}"
    f"\n   - Valores nulos residuales: {df['COLE_BILINGUE'].isna().sum():,}\n"
)

# =========================================================================
# RESUMEN FINAL Y EXPORTACIÓN
# =========================================================================
filas_finales = len(df)
total_eliminadas = filas_iniciales - filas_finales
pct_conservado = (filas_finales / filas_iniciales) * 100

print("=" * 50)
print(f"RESUMEN FINAL DEPURACIÓN:")
print(f"- Filas Iniciales:    {filas_iniciales:,}")
print(f"- Total Eliminadas:   {total_eliminadas:,}")
print(
    f"- Filas Finales:      {filas_finales:,} ({pct_conservado:.2f}% conservado)"
)
print("=" * 50)

# Exportar archivo listo para el cruce
print("Exportando dataset depurado...")
df.to_csv("Saber_11_Listo_2018_2024.csv", index=False)
print("¡Archivo exportado exitosamente con llaves 'COLE_COD_DEPTO_UBICACION' y 'ANIO' listas para el cruce!")