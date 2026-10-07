import re
import numpy as np
import pandas as pd

# =========================================================================
# 1. CARGA DEL DATASET
# =========================================================================
ARCHIVO_ENTRADA = "icfes_limpio_FIX_2018_2024.csv"
ARCHIVO_SALIDA = "Examen_Saber_11_limpio_tildes.csv"

print("Cargando dataset...")
try:
    df = pd.read_csv(ARCHIVO_ENTRADA, sep=";", encoding="utf-8", low_memory=False)
except UnicodeDecodeError:
    df = pd.read_csv(ARCHIVO_ENTRADA, sep=";", encoding="latin-1", low_memory=False)

df.columns = df.columns.str.strip()

# Columnas geográficas a procesar
columnas_depto = [
    "cole_depto_ubicacion",
    "estu_depto_presentacion",
    "estu_depto_reside",
]

# =========================================================================
# 2. LISTA OFICIAL DANE (32 Departamentos + BOGOTA = 33)
# =========================================================================
DEPARTAMENTOS_OFICIALES = {
    "AMAZONAS", "ANTIOQUIA", "ARAUCA", "ATLANTICO", "BOGOTA", "BOLIVAR",
    "BOYACA", "CALDAS", "CAQUETA", "CASANARE", "CAUCA", "CESAR", "CHOCO",
    "CORDOBA", "CUNDINAMARCA", "GUAINIA", "GUAVIARE", "HUILA", "LA GUAJIRA",
    "MAGDALENA", "META", "NARINO", "NORTE DE SANTANDER", "PUTUMAYO",
    "QUINDIO", "RISARALDA", "SAN ANDRES", "SANTANDER", "SUCRE", "TOLIMA",
    "VALLE DEL CAUCA", "VAUPES", "VICHADA"
}

# =========================================================================
# 3. FUNCIONES DE LIMPIEZA Y HOMOLOGACIÓN
# =========================================================================
def normalizar_texto(texto):
    if pd.isna(texto):
        return np.nan

    texto = str(texto).strip().upper()

    reemplazos = {
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"
    }
    for sucio, limpio in reemplazos.items():
        texto = texto.replace(sucio, limpio)

    # Eliminar símbolos que no sean letras o números
    texto = re.sub(r"[^\w\s]", " ", texto)
    # Reducir espacios múltiples
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


DICCIONARIO_DPTOS = {
    # Bogotá
    "BOGOTA": "BOGOTA",
    "BOGOTA D C": "BOGOTA",
    "BOGOTA DC": "BOGOTA",
    "BOGOTÃ": "BOGOTA",
    "SANTAFE DE BOGOTA": "BOGOTA",
    "SANTAFE DE BOGOTA D C": "BOGOTA",
    # San Andrés
    "SAN ANDRES": "SAN ANDRES",
    "SAN ANDRES Y PROVIDENCIA": "SAN ANDRES",
    "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA": "SAN ANDRES",
    "ARCHIPIELAGO DE SAN ANDRES": "SAN ANDRES",
    # Otros con abreviaciones comunes
    "VALLE": "VALLE DEL CAUCA",
    "NORTE SANTANDER": "NORTE DE SANTANDER",
}


def homologar_departamento(depto_limpio):
    if pd.isna(depto_limpio):
        return np.nan

    # Solución comodín para NARIÑO (corrige 'NA RINO O', 'NARI O', etc.)
    if depto_limpio.startswith("NAR") or "RINO" in depto_limpio:
        return "NARINO"

    return DICCIONARIO_DPTOS.get(depto_limpio, depto_limpio)


# =========================================================================
# 4. APLICACIÓN Y DIAGNÓSTICO
# =========================================================================
print("\nIniciando estandarización de columnas geográficas...")

for col in columnas_depto:
    if col in df.columns:
        print(f"\nProcesando columna: {col}")

        valores_unicos = df[col].dropna().unique()
        mapeo_limpieza = {}

        for val in valores_unicos:
            val_limpio = normalizar_texto(val)
            val_final = homologar_departamento(val_limpio)
            mapeo_limpieza[val] = val_final

        df[col] = df[col].map(mapeo_limpieza)

        unicos_actuales = set(df[col].dropna().unique())
        print(f"   - Cantidad de departamentos únicos: {len(unicos_actuales)}")

        # Si hay más de 33, muestra el valor no oficial detectado
        no_oficiales = unicos_actuales - DEPARTAMENTOS_OFICIALES
        if no_oficiales:
            print(f"   ⚠️ ATENCIÓN: Valores fuera de los 33 oficiales del DANE: {no_oficiales}")

# =========================================================================
# 5. VERIFICACIÓN FINAL
# =========================================================================
print("\n" + "=" * 50)
print("LISTA FINAL DE DEPARTAMENTOS EN 'cole_depto_ubicacion':")
print("=" * 50)
print(sorted([str(x) for x in df["cole_depto_ubicacion"].dropna().unique()]))

# =========================================================================
# 6. EXPORTACIÓN
# =========================================================================
print(f"\nGuardando archivo final en '{ARCHIVO_SALIDA}'...")
df.to_csv(ARCHIVO_SALIDA, sep=";", index=False, encoding="utf-8")
print("¡Proceso terminado exitosamente!")