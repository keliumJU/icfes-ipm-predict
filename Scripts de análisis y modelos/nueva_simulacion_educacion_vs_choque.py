import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

# ==============================================================================
# 1. CARGA Y AJUSTE DEL MODELO GANADOR (ELASTICNET)
# ==============================================================================
df = pd.read_csv("./panel_departamento_anio_unido.csv", encoding="utf-8-sig")
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

# Entrenar con histórico 2018-2022
train_mask = df_clean["anio"].isin([2018, 2019, 2021, 2022])
X_train = df_clean.loc[train_mask, predictores]
y_train = df_clean.loc[train_mask, "target"]

modelo = Pipeline(
    [
        ("scaler", StandardScaler()),
        (
            "elasticnet",
            LogisticRegression(
                penalty="elasticnet",
                solver="saga",
                C=0.1,
                l1_ratio=0.8,
                class_weight="balanced",
                max_iter=10000,
                random_state=42,
            ),
        ),
    ]
)
modelo.fit(X_train, y_train)

# ==============================================================================
# 2. LÍNEA BASE (AÑO 2024)
# ==============================================================================
df_2024 = df_clean[df_clean["anio"] == 2024].copy().reset_index(drop=True)
X_base_2024 = df_2024[predictores]

prob_base = modelo.predict_proba(X_base_2024)[:, 1]

res_sim = pd.DataFrame(
    {
        "departamento": df_2024["departamento"],
        "Prob_Base_2024": prob_base,
    }
)

# ==============================================================================
# 3. ESCENARIOS NUEVOS A SIMULAR
# ==============================================================================

# ESCENARIO A: "Intervención Educativa Pura" (-50% en privaciones educativas)
# Reducimos a la mitad: Analfabetismo, Inasistencia escolar y Rezago escolar
X_sim_edu = X_base_2024.copy()
vars_educativas = ["Analfabetismo", "Inasistencia escolar", "Rezago escolar"]
for var in vars_educativas:
    X_sim_edu[var] = X_sim_edu[var] * 0.50

res_sim["Prob_Educativa_Pura (-50%)"] = modelo.predict_proba(X_sim_edu)[:, 1]

# ESCENARIO B: "Plan de Choque Integral Agresivo" (-60% en todo el IPM y dimensiones)
# Buscamos responder: ¿Un choque del 60% rescata a Chocó, La Guajira y Vichada?
X_sim_choque = X_base_2024 * 0.40  # Reducción del 60%
res_sim["Prob_Plan_Choque (-40% Integral)"] = modelo.predict_proba(
    X_sim_choque
)[:, 1]

# ==============================================================================
# 4. ANÁLISIS DE LA PERIFERIA PROFUNDA (LOS 5 MÁS REZAGADOS)
# ==============================================================================
periferia = ["Vichada", "Vaupés", "Chocó", "Guainía", "La Guajira"]
df_periferia = res_sim[res_sim["departamento"].isin(periferia)].copy()

print("=" * 85)
print(
    "IMPACTO SOBRE LA PERIFERIA ESTRUCTURAL: EDUCATIVO PURO vs. PLAN DE CHOQUE (-30%)"
)
print("=" * 85)
print(df_periferia.to_string(index=False))

# Guardar en CSV
res_sim.to_csv("nueva_simulacion_educativa_vs_choque.csv", index=False)
print("\n[OK] Datos guardados en 'nueva_simulacion_educativa_vs_choque.csv'")

# ==============================================================================
# 5. GRÁFICA COMPARATIVA DEL EXPERIMENTO
# ==============================================================================
plt.figure(figsize=(11, 8.5))
graf_df = res_sim.sort_values(by="Prob_Base_2024", ascending=True)
y_pos = np.arange(len(graf_df))

# Líneas y puntos de Línea Base
plt.scatter(
    graf_df["Prob_Base_2024"],
    y_pos,
    color="crimson",
    s=35,
    label="Línea Base 2024",
    zorder=3,
)

# Puntos de Intervención Educativa
plt.scatter(
    graf_df["Prob_Educativa_Pura (-50%)"],
    y_pos,
    color="darkorange",
    s=35,
    marker="^",
    label="Escenario Educativo (-50% Analfabetismo/Rezago/Inasistencia)",
    zorder=3,
)

# Puntos de Plan de Choque Integral
plt.scatter(
    graf_df["Prob_Plan_Choque (-40% Integral)"],
    y_pos,
    color="dodgerblue",
    s=35,
    marker="s",
    label="Plan de Choque (-40% Multidimensional)",
    zorder=3,
)

plt.axvline(
    x=0.5,
    color="black",
    linestyle="--",
    alpha=0.7,
    label="Umbral Satisfactorio (50%)",
)

plt.yticks(y_pos, graf_df["departamento"], fontsize=8)
plt.xlabel("Probabilidad de Desempeño Satisfactorio")
plt.title(
    "Comparación de Políticas: Intervención Educativa Focalizada vs. Plan de Choque Integral",
    fontsize=11,
    weight="bold",
)
plt.legend(loc="lower right", fontsize=8.5)
plt.tight_layout()
plt.savefig("grafico_comparativo_politicas.png", dpi=300)
plt.show()
print("[OK] Gráfica guardada como 'grafico_comparativo_politicas.png'")