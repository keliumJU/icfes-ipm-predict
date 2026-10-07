import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    brier_score_loss,
    classification_report,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
import xgboost as xgb

warnings.filterwarnings("ignore")

# ==============================================================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ==============================================================================
df = pd.read_csv("panel_departamento_anio_unido.csv", encoding="utf-8-sig")
df_clean = df[df["_merge"] == "both"].copy()

UMBRAL = 250
df_clean["target"] = (df_clean["prom_punt_global"] >= UMBRAL).astype(int)

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

# Peso para compensar el desbalance (negativos / positivos en train ≈ 91 / 41 ≈ 2.2)
ratio_desbalance = (y_train == 0).sum() / (y_train == 1).sum()

# ==============================================================================
# 3. MALLA DE HIPERPARÁMETROS REGULARIZADOS
# ==============================================================================
xgb_clf = xgb.XGBClassifier(
    eval_metric="logloss",
    random_state=42,
    scale_pos_weight=ratio_desbalance,  # Balancea clases
)

param_grid = {
    "n_estimators": [50, 100],  # Pocos árboles para evitar overfitting
    "max_depth": [2, 3],  # Árboles muy poco profundos
    "learning_rate": [0.01, 0.03, 0.05],  # Tasa de aprendizaje prudente
    "subsample": [0.7, 0.85],  # Submuestreo de filas
    "colsample_bytree": [0.5, 0.7],  # Submuestreo de variables
    "reg_alpha": [0.1, 1.0],  # Regularización L1 (Lasso)
    "reg_lambda": [1.0, 5.0],  # Regularización L2 (Ridge)
}

# Misma estrategia de validación agrupada por departamento
cv_estrategia = StratifiedGroupKFold(n_splits=5)

grid_search_xgb = GridSearchCV(
    estimator=xgb_clf,
    param_grid=param_grid,
    cv=cv_estrategia,
    scoring="roc_auc",
    n_jobs=-1,
)

# ==============================================================================
# 4. ENTRENAMIENTO
# ==============================================================================
print("Entrenando XGBoost con regularización estricta...")
grid_search_xgb.fit(X_train, y_train, groups=grupos_train)

best_xgb = grid_search_xgb.best_estimator_
print(f"Mejores hiperparámetros encontrados: {grid_search_xgb.best_params_}")
print(f"Mejor ROC-AUC promedio en CV: {grid_search_xgb.best_score_:.4f}")

# ==============================================================================
# 5. EVALUACIÓN FUERA DE MUESTRA (TEST: 2023 - 2024)
# ==============================================================================
y_probs_xgb = best_xgb.predict_proba(X_test)[:, 1]
y_pred_xgb = (y_probs_xgb >= 0.5).astype(int)

auc_xgb = roc_auc_score(y_test, y_probs_xgb)
brier_xgb = brier_score_loss(y_test, y_probs_xgb)

print("\n--- RESULTADOS XGBOOST EN TEST (2023-2024) ---")
print(f"ROC-AUC fuera de muestra: {auc_xgb:.4f}")
print(f"Brier Score (Calibración): {brier_xgb:.4f}")
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred_xgb))

# ==============================================================================
# 6. IMPORTANCIA DE VARIABLES (Weight / Gain)
# ==============================================================================
importancias = best_xgb.feature_importances_
df_importancias = pd.DataFrame(
    {"Variable": predictores, "Importancia (Gain)": importancias}
).sort_values(by="Importancia (Gain)", ascending=False)

print("\n--- IMPORTANCIA DE VARIABLES EN XGBOOST ---")
print(df_importancias.to_string(index=False))