import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    brier_score_loss,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold

warnings.filterwarnings("ignore")

# ==============================================================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ==============================================================================
df = pd.read_csv("panel_departamento_anio_unido.csv", encoding="utf-8-sig")

# Filtro de cruces válidos (Saber + IPM)
df_clean = df[df["_merge"] == "both"].copy()

# Target binario: 1 si puntaje >= 250, 0 en caso contrario
UMBRAL = 250
df_clean["target"] = (df_clean["prom_punt_global"] >= UMBRAL).astype(int)

# Los 16 predictores
predictores = [
    "ipm",
    "Analfabetismo",
    "Bajo logro educativo",
    "Barreras a servicios para cuidado de la primera infancia",
    "Barreras de acceso a servicios de salud",
    "Desempleo de larga duracion",
    "Hacinamiento critico",
    "Inadecuada eliminacion de excretas",
    "Inasistencia escolar",
    "Material inadecuado de paredes exteriores",
    "Material inadecuado de pisos",
    "Rezago escolar",
    "Sin acceso a fuente de agua mejorada",
    "Sin aseguramiento en salud",
    "Trabajo infantil",
    "Trabajo informal",
]

# ==============================================================================
# 2. PARTICIÓN TEMPORAL
# ==============================================================================
train_mask = df_clean["anio"].isin([2018, 2019, 2021, 2022])
test_mask = df_clean["anio"].isin([2023, 2024])

X_train = df_clean.loc[train_mask, predictores]
y_train = df_clean.loc[train_mask, "target"]
grupos_train = df_clean.loc[train_mask, "codigo_departamento"]

X_test = df_clean.loc[test_mask, predictores]
y_test = df_clean.loc[test_mask, "target"]

# Nota: Los árboles de decisión NO requieren StandardScaler (son invariantes a escalas monótonas)

# ==============================================================================
# 3. MALLA DE HIPERPARÁMETROS REGULARIZADOS
# ==============================================================================
rf = RandomForestClassifier(random_state=42, class_weight="balanced")

# Espacio de búsqueda acotado para forzar árboles conservadores y no sobreajustados
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [2, 3, 4],  # Árboles poco profundos
    "min_samples_leaf": [3, 5, 8],  # Hojas con suficientes observaciones
    "min_samples_split": [6, 10, 15],  # Dificultad para dividir nodos
    "max_features": [
        "sqrt",
        0.3,
        0.5,
    ],  # Fracción de predictores por división
}

# Misma estrategia de validación cruzada agrupada por departamento
cv_estrategia = StratifiedGroupKFold(n_splits=5)

grid_search_rf = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=cv_estrategia,
    scoring="roc_auc",
    n_jobs=-1,
)

# ==============================================================================
# 4. ENTRENAMIENTO
# ==============================================================================
print("Entrenando Random Forest con regularización...")
grid_search_rf.fit(X_train, y_train, groups=grupos_train)

best_rf = grid_search_rf.best_estimator_
print(f"Mejores hiperparámetros encontrados: {grid_search_rf.best_params_}")
print(f"Mejor ROC-AUC promedio en CV: {grid_search_rf.best_score_:.4f}")

# ==============================================================================
# 5. EVALUACIÓN FUERA DE MUESTRA (TEST: 2023 - 2024)
# ==============================================================================
y_probs_rf = best_rf.predict_proba(X_test)[:, 1]
y_pred_rf = (y_probs_rf >= 0.5).astype(int)

auc_rf = roc_auc_score(y_test, y_probs_rf)
brier_rf = brier_score_loss(y_test, y_probs_rf)

print("\n--- RESULTADOS RANDOM FOREST EN TEST (2023-2024) ---")
print(f"ROC-AUC fuera de muestra: {auc_rf:.4f}")
print(f"Brier Score (Error Cuadrático): {brier_rf:.4f}")
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred_rf))

# ==============================================================================
# 6. IMPORTANCIA DE VARIABLES (Feature Importance)
# ==============================================================================
# Calculamos la importancia relativa de cada dimensión según la reducción de impureza Gini
importancias = best_rf.feature_importances_
df_importancias = pd.DataFrame(
    {"Variable": predictores, "Importancia": importancias}
).sort_values(by="Importancia", ascending=False)

print("\n--- IMPORTANCIA DE VARIABLES (Gini Importance) ---")
print(df_importancias.to_string(index=False))