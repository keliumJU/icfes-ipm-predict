# Fuentes primarias consultadas

Consulta: 2026-10-07 (fecha del cliente, America/Bogota). Estas consultas son actuales, no certificaciones de versiones históricas ni sustituciones de archivos locales. Se conservaron los insumos suministrados y sus huellas.

| Fuente | Ubicación verificable | Uso y límite |
|---|---|---|
| DANE, pobreza multidimensional2024 | [Publicación2024](https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-multidimensional/pobreza-multidimensional-2024), fila«Anexo departamental»,22/04/2025 | Contrastar la edición y fecha publicada; no se descargó ni comprobó huella del XLSX remoto |
| DANE, catálogoIPM2024 | [Catálogo860](https://microdatos.dane.gov.co/index.php/catalog/860) y [materiales relacionados](https://microdatos.dane.gov.co/index.php/catalog/860/related-materials) | Procedencia de publicación; definición y celdas de cifras se verifican en XLSX local, no en otra serie |
| Anexo local DANE | `Fuente del IPM/anex-PMultidimensional-Departamental-2024.xlsx`; `evidencia/cotejo_ipm_celdas.csv` y `notas_ipm.csv` | Cotejo completo de3.168cifras y todas las notas de las hojas utilizadas; no acredita descarga histórica |
| scikit-learn, Probability calibration | [Sección1.16, nota sobre Brier](https://scikit-learn.org/stable/modules/calibration.html) | Brier combina fiabilidad, resolución e incertidumbre; menor valor no establece calibración superior |
| SHAP, TreeExplainer | [model_output](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html) | Diferencia salida raw/log-odds yprobability; no se calculaSHAP |
| ICFES, niveles Matemáticas2022 | [Niveles de desempeño](https://portalmigracion.icfes.gov.co/wp-content/uploads/2024/11/Niveles-de-desempeno-Matematicas-Saber-11.o-2022.pdf) | Límites35/50/70 para comparación completa contra categorías del consolidado |
| ICFES, niveles LecturaCrítica2022 | [Niveles de desempeño](https://www.icfes.gov.co/wp-content/uploads/2024/11/Niveles-de-desempeno-Lectura-Critica-Saber-11.o-2022.pdf) | Límites35/50/65 |
| ICFES, niveles CienciasNaturales2022 | [Niveles de desempeño](https://www.icfes.gov.co/wp-content/uploads/2024/11/Niveles-de-desempeno-Ciencias-Naturales-Saber-11.o-2022.pdf) | Límites40/55/70 |
| ICFES, niveles Sociales | [Documento oficial](https://www.icfes.gov.co/wp-content/uploads/2025/08/ND-sociales-y-ciudadanas.pdf) | Límites40/55/70; publicación posterior a parte de la serie, no prueba aislada de su versión histórica. La concordancia se verifica sobre todos los registros recibidos |
| ICFES, reporte de resultados | [Resultados Saber11](https://www.icfes.gov.co/evaluaciones-icfes/saber-11/resultados-examen-saber-11/) | Puntaje global, percentiles y niveles por prueba son conceptos distintos |
| ICFES, escala y ponderación | [Acuerdo2de2016, apartado de resultados](https://normograma.icfes.gov.co/compilacion/docs/acuerdo_icfes_0002_2016.htm) | Escala0–500 anclada en2014 y pesos3/3/3/3/1. Fórmula usada solo como diagnóstico, no para reemplazar puntajes; revisar excepciones/versiones para525diferencias20222 |

Se buscaron explicaciones oficiales de ajustes2022/puntaje global; los resultados encontrados no acreditaron una causa aplicable a las525observaciones. No se tomó como evidencia sobre Saber11 un documento de pruebas policiales o concursos docentes encontrado por coincidencia de términos. No se atribuyen las diferencias a recalificación, discapacidad ni modificación manual sin prueba.
