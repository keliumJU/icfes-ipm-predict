import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    brier_score_loss,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedGroupKFold

# Ignorar advertencias de convergencia durante pruebas de hiperparámetros
warnings.filterwarnings("ignore")

# ==============================================================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ==============================================================================
# Cargar el dataset final
df = pd.read_csv("panel_departamento_anio_unido.csv", encoding="utf-8-sig")

# Filtro metodológico: Solo cruces exitosos y excluir 2021 por anomalía de muestra
df_clean = df[(df["_merge"] == "both")].copy()

# Definición de la variable objetivo: 1 si supera o iguala 250 puntos, 0 si no
UMBRAL = 250
df_clean["target"] = (df_clean["prom_punt_global"] >= UMBRAL).astype(int)

# Lista exacta de tus 16 predictores (IPM global + 15 dimensiones)
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
# 2. PARTICIÓN TEMPORAL (TRAIN vs TEST)
# ==============================================================================
# Cohortes de entrenamiento: 2018, 2019, 2022
train_mask = df_clean["anio"].isin([2018, 2019, 2021, 2022])
# Cohortes de evaluación fuera de muestra: 2023, 2024
test_mask = df_clean["anio"].isin([2023, 2024])

X_train = df_clean.loc[train_mask, predictores]
y_train = df_clean.loc[train_mask, "target"]
grupos_train = df_clean.loc[train_mask, "codigo_departamento"]

X_test = df_clean.loc[test_mask, predictores]
y_test = df_clean.loc[test_mask, "target"]

print(
    f"Dimensiones de entrenamiento: {X_train.shape[0]} filas (departamentos-año)"
)
print(f"Dimensiones de prueba: {X_test.shape[0]} filas (departamentos-año)")
print(f"Distribución del target en Train:\n{y_train.value_counts(normalize=True)}")

# ==============================================================================
# 3. PIPELINE CORREGIDO Y MALLA DE HIPERPARÁMETROS
# ==============================================================================
pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        (
            "elasticnet",
            LogisticRegression(
                penalty="elasticnet",
                solver="saga",
                class_weight="balanced",  # Corrige el desbalance 69% vs 31%
                max_iter=10000,
                random_state=42,
            ),
        ),
    ]
)

# Valores de C más realistas (C altos = penalidad moderada/suave)
param_grid = {
    "elasticnet__C": [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0],
    "elasticnet__l1_ratio": [
        0.05,
        0.2,
        0.5,
        0.8,
    ],  # Balance entre Ridge y Lasso
}

# Validación cruzada balanceada por grupos (departamentos)
cv_estrategia = StratifiedGroupKFold(n_splits=5)

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=cv_estrategia,
    scoring="roc_auc",
    n_jobs=-1,
)

# ==============================================================================
# 4. ENTRENAMIENTO CORREGIDO
# ==============================================================================
print("\nEntrenando con StratifiedGroupKFold...")
# Pasamos y_train como etiquetas para estratificar y grupos_train para no romper departamentos
grid_search.fit(X_train, y_train, groups=grupos_train)

best_model = grid_search.best_estimator_
print(f"Mejores hiperparámetros encontrados: {grid_search.best_params_}")
print(f"Mejor ROC-AUC promedio en CV: {grid_search.best_score_:.4f}")
# ==============================================================================
# 5. EVALUACIÓN FUERA DE MUESTRA (TEST: 2023 - 2024)
# ==============================================================================
# Predecir probabilidades y clases en el conjunto de prueba
y_probs_test = best_model.predict_proba(X_test)[:, 1]
y_pred_test = (y_probs_test >= 0.5).astype(int)

# Métricas solicitadas por los objetivos
auc = roc_auc_score(y_test, y_probs_test)
brier = brier_score_loss(y_test, y_probs_test)

print("\n--- RESULTADOS EN EL CONJUNTO DE PRUEBA (2023-2024) ---")
print(f"ROC-AUC fuera de muestra: {auc:.4f}")
print(f"Brier Score (Calibración/Error Cuadrático): {brier:.4f}")
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred_test))

# ==============================================================================
# 6. INTERPRETACIÓN DE COEFICIENTES (Para el texto de la tesis)
# ==============================================================================
# Extraemos los coeficientes del modelo final entrenado
coeficientes = best_model.named_steps["elasticnet"].coef_[0]

df_coef = pd.DataFrame(
    {"Variable": predictores, "Coeficiente": coeficientes}
).sort_values(by="Coeficiente", ascending=True)

print("\n--- COEFICIENTES ESTIMADOS (Efecto sobre probabilidad de éxito) ---")
print(df_coef.to_string(index=False))

# Si un coeficiente es 0, ElasticNet determinó que esa variable no aporta información adicional
variables_eliminadas = df_coef[df_coef["Coeficiente"] == 0]["Variable"].tolist()
print(f"\nVariables anuladas por ElasticNet (L1): {len(variables_eliminadas)}")