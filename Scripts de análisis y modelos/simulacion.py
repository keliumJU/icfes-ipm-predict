import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

# ==============================================================================
# 1. CARGA DE DATOS Y ENTRENAMIENTO DEL MODELO GANADOR (ELASTICNET)
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

# Entrenamos con los datos históricos (2018-2022) con los mejores hiperparámetros encontrados
train_mask = df_clean["anio"].isin([2018, 2019, 2021, 2022])
X_train = df_clean.loc[train_mask, predictores]
y_train = df_clean.loc[train_mask, "target"]

modelo_elasticnet = Pipeline(
    [
        ("scaler", StandardScaler()),
        (
            "elasticnet",
            LogisticRegression(
                penalty="elasticnet",
                solver="saga",
                C=0.1,  # Hiperparámetro óptimo
                l1_ratio=0.8,  # Hiperparámetro óptimo
                class_weight="balanced",
                max_iter=10000,
                random_state=42,
            ),
        ),
    ]
)
modelo_elasticnet.fit(X_train, y_train)

# ==============================================================================
# 2. DEFINICIÓN DE LÍNEA BASE (COHORTE 2024)
# ==============================================================================
df_2024 = df_clean[df_clean["anio"] == 2024].copy().reset_index(drop=True)
X_base_2024 = df_2024[predictores]

# Probabilidad actual en 2024 según el modelo
prob_base = modelo_elasticnet.predict_proba(X_base_2024)[:, 1]

# DataFrame para consolidar resultados
sim_df = pd.DataFrame(
    {
        "codigo_departamento": df_2024["codigo_departamento"],
        "departamento": df_2024["departamento"],
        "prom_punt_global_2024": df_2024["prom_punt_global"],
        "ipm_actual": df_2024["ipm"],
        "Prob_Base_2024": prob_base,
    }
)

# ==============================================================================
# 3. CONSTRUCCIÓN DE ESCENARIOS CONTRAFACTUALES
# ==============================================================================

# ESCENARIO 1: Reducción uniforme del 10% en todas las privaciones
X_sim1 = X_base_2024 * 0.90
sim_df["Prob_Escenario_1 (-10% General)"] = (
    modelo_elasticnet.predict_proba(X_sim1)[:, 1]
)

# ESCENARIO 2: Reducción uniforme del 25% en todas las privaciones
X_sim2 = X_base_2024 * 0.75
sim_df["Prob_Escenario_2 (-25% General)"] = (
    modelo_elasticnet.predict_proba(X_sim2)[:, 1]
)

# ESCENARIO 3: Reducción del 30% en factores críticos (Excretas, Informalidad, Agua)
X_sim3 = X_base_2024.copy()
variables_criticas = [
    "Inadecuada eliminacion de excretas",
    "Trabajo informal",
    "Sin acceso a fuente de agua mejorada",
]
for var in variables_criticas:
    X_sim3[var] = X_sim3[var] * 0.70

sim_df["Prob_Escenario_3 (-30% Saneamiento e Informalidad)"] = (
    modelo_elasticnet.predict_proba(X_sim3)[:, 1]
)

# ==============================================================================
# 4. ANÁLISIS DE IMPACTO Y DEPARTAMENTOS QUE CAMBIAN DE ESTADO
# ==============================================================================
# Calcular el incremento de probabilidad frente a la línea base
sim_df["Delta_Prob_Esc3"] = (
    sim_df["Prob_Escenario_3 (-30% Saneamiento e Informalidad)"]
    - sim_df["Prob_Base_2024"]
)

# Identificar departamentos que cruzan el umbral del 50% de probabilidad
sim_df["Clasif_Base"] = (sim_df["Prob_Base_2024"] >= 0.5).astype(int)
sim_df["Clasif_Esc3"] = (
    sim_df["Prob_Escenario_3 (-30% Saneamiento e Informalidad)"] >= 0.5
).astype(int)

departamentos_beneficiados = sim_df[
    (sim_df["Clasif_Base"] == 0) & (sim_df["Clasif_Esc3"] == 1)
]

print("=" * 80)
print("DEPARTAMENTOS QUE LOGRAN SUPERAR EL UMBRAL SATISFACTORIO EN EL ESCENARIO 3")
print("=" * 80)
if len(departamentos_beneficiados) > 0:
    print(
        departamentos_beneficiados[
            [
                "departamento",
                "ipm_actual",
                "prom_punt_global_2024",
                "Prob_Base_2024",
                "Prob_Escenario_3 (-30% Saneamiento e Informalidad)",
            ]
        ].to_string(index=False)
    )
else:
    print("Ningún departamento no satisfactorio logra cruzar el 50% en el E3.")

# ==============================================================================
# 5. TABLA DE LOS 10 DEPARTAMENTOS CON MAYOR GANANCIA EN PROBABILIDAD
# ==============================================================================
print("\n" + "=" * 80)
print(
    "TOP 10 DEPARTAMENTOS CON MAYOR INCREMENTO EN PROBABILIDAD (ESCENARIO 3: SANEAMIENTO + INFORMALIDAD)"
)
print("=" * 80)
top_ganancias = sim_df.sort_values(by="Delta_Prob_Esc3", ascending=False).head(
    10
)
print(
    top_ganancias[
        [
            "departamento",
            "ipm_actual",
            "Prob_Base_2024",
            "Prob_Escenario_3 (-30% Saneamiento e Informalidad)",
            "Delta_Prob_Esc3",
        ]
    ].to_string(index=False)
)

# Exportar tabla completa para el anexo de la tesis
sim_df.to_csv("resultados_simulacion_escenarios_2024.csv", index=False)
print("\n[OK] Archivo guardado: 'resultados_simulacion_escenarios_2024.csv'")

# ==============================================================================
# 6. GRÁFICA COMPARATIVA PARA EL DOCUMENTO DE GRADO
# ==============================================================================
plt.figure(figsize=(10, 8))
# Ordenamos por probabilidad base
graf_df = sim_df.sort_values(by="Prob_Base_2024", ascending=True)

y_pos = np.arange(len(graf_df))

plt.hlines(
    y=y_pos,
    xmin=graf_df["Prob_Base_2024"],
    xmax=graf_df["Prob_Escenario_3 (-30% Saneamiento e Informalidad)"],
    color="grey",
    alpha=0.6,
    linewidth=1.5,
)
plt.scatter(
    graf_df["Prob_Base_2024"],
    y_pos,
    color="crimson",
    alpha=0.9,
    label="Línea Base 2024",
    s=40,
)
plt.scatter(
    graf_df["Prob_Escenario_3 (-30% Saneamiento e Informalidad)"],
    y_pos,
    color="teal",
    alpha=0.9,
    label="Escenario 3 (-30% Excretas/Informalidad/Agua)",
    s=40,
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
    "Impacto Contrafactual: Mejora en la Probabilidad por Reducción de Pobreza Estructural",
    fontsize=11,
    weight="bold",
)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("grafico_simulacion_escenarios.png", dpi=300)
plt.show()
print("[OK] Gráfica guardada: 'grafico_simulacion_escenarios.png'")
