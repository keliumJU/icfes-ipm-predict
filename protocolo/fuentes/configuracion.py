"""Decisiones prospectivas v1.0; no construye ni entrena estimadores."""
from itertools import product

VERSION = "1.0"
COMMIT_PARTIDA = "a68f0bb58b7b5268e6025ef33afc64862f8e8cc8"
BASE_SHA256 = "609d73153ec7691567af5d460ffcf546cb54af1926662effd017a9ae05c50866"
DICCIONARIO_SHA256 = "6f6c662a3a68b9955e3597e5d8203d0fac9fb009b04ddc9dee73687d77599c68"
SEMILLA = 20261008
DESARROLLO = (2018, 2019, 2021, 2022)
REEVALUACION = (2023, 2024)
RESULTADO = "prom_punt_global"
DIMENSIONES = {
    "Condiciones educativas del hogar": ["Analfabetismo", "Bajo logro educativo"],
    "Condiciones de la niñez y juventud": [
        "Barreras a servicios para cuidado de la primera infancia",
        "Inasistencia escolar", "Rezago escolar", "Trabajo infantil"],
    "Trabajo": ["Desempleo de larga duracion", "Trabajo informal"],
    "Salud": ["Barreras de acceso a servicios de salud", "Sin aseguramiento en salud"],
    "Acceso a servicios públicos domiciliarios y condiciones de la vivienda": [
        "Hacinamiento critico", "Inadecuada eliminacion de excretas",
        "Material inadecuado de paredes exteriores", "Material inadecuado de pisos",
        "Sin acceso a fuente de agua mejorada"],
}
TASAS = [v for grupo in DIMENSIONES.values() for v in grupo]
ESPECIFICACIONES = {"ipm": ["ipm"], "tasas": TASAS, "ambas": ["ipm", *TASAS]}
VENTANAS = [(DESARROLLO[:i], DESARROLLO[i]) for i in range(1, len(DESARROLLO))]
GRILLAS = {
    "ridge": {"alpha": [0.1, 1.0, 10.0, 100.0, 1000.0]},
    "random_forest": {"max_depth": [2, 4], "min_samples_leaf": [3, 8],
                      "max_features": [0.5, 1.0]},
    "gradient_boosting": {"n_estimators": [50, 100], "learning_rate": [0.03, 0.1],
                          "max_depth": [1, 2]},
}
FIJOS = {
    "media": {"strategy": "mean"},
    "ols": {"fit_intercept": True},
    "ridge": {"fit_intercept": True, "solver": "svd"},
    "random_forest": {"n_estimators": 300, "criterion": "squared_error",
                      "bootstrap": True, "min_samples_split": 2, "n_jobs": 1,
                      "random_state": SEMILLA, "oob_score": False},
    "gradient_boosting": {"loss": "squared_error", "min_samples_leaf": 3,
                          "min_samples_split": 2, "subsample": 1.0,
                          "max_features": None, "n_iter_no_change": None,
                          "random_state": SEMILLA},
}
TOLERANCIA_PUNTOS = 0.1
ORDEN_FAMILIAS = ["media", "ols", "ridge", "random_forest", "gradient_boosting"]


def candidatos():
    """Orden determinista; referencias incluidas en la comparación futura."""
    yield {"id": "media", "familia": "media", "especificacion": None, "parametros": FIJOS["media"]}
    for especificacion in ESPECIFICACIONES:
        yield {"id": f"ols_{especificacion}", "familia": "ols",
               "especificacion": especificacion, "parametros": FIJOS["ols"]}
        for familia, grilla in GRILLAS.items():
            for numero, valores in enumerate(product(*grilla.values())):
                yield {"id": f"{familia}_{especificacion}_{numero:02d}", "familia": familia,
                       "especificacion": especificacion,
                       "parametros": {**FIJOS[familia], **dict(zip(grilla, valores))}}
