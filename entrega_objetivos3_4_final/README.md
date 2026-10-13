# Entrega del objetivo 3 y preparación separada del 4

Contenido principal: objetivo3/CONTENIDO_OBJETIVO3.docx, versión editable; objetivo3/TEXTO_PARA_TESIS.md; GUIA_DE_INTEGRACION.md. No se modificó ACA2. El texto explica versiones y decisiones en lenguaje académico claro; conserva resultados desfavorables.

Periodo principal decidido por el usuario: 2018–2025 para el análisis predictivo. La ampliación no recalcula automáticamente los objetivos 1/2. Ver continuidad y guía de integración para decisiones académicas aún indispensables.

## Reproducción

Abrir notebooks dentro del proyecto:

- 01_diseno_y_reproduccion.ipynb: diseño, entradas, parámetros completos y rutas manuales de ajuste base/V2/V6. Generado desde Python, validado, sin ejecutar ajustes nuevos. Todos los indicadores ENTRENAR_* son False. No cambiar reglas para mejorar métricas.
- 02_resultados_y_graficas.ipynb: ejecutado realmente. Recalcula predicciones guardadas de los mismos 165 pares; cinco pruebas; métricas y figuras nuevas. Cero entrenamientos.

Entorno analítico existente: /tmp/icfes-v2-fase2-venv/bin/python, Python 3.12.14, locks originales en fase3/requirements.lock.txt y V6/ENTORNO_DOCUMENTAL.json, semillas originales 20261008 y 20261010. No instalación/modificación del entorno. Generar/reproducir salidas: `MPLCONFIGDIR=/tmp/mpl_entrega_tesis PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python -B fuentes/generar_notebooks.py` desde esta carpeta. Jupyter requiere conexiones locales; en entorno restringido puede necesitar autorización de ejecución fuera del aislamiento.

Para regenerar texto: mismo entorno, `python -B fuentes/redactar.py`. Para Word: runtime documental empaquetado indicado por load_workspace_dependencies, `python -B fuentes/crear_word.py`. Gráficas y tablas nacen del notebook y de analisis.py compartido. Edite fuentes Python y regenere, no JSON manualmente. Entrenamiento manual es una ejecución nueva no realizada aquí; no ejecutar runners cerrados ni escribir sobre salidas anteriores.

Evidencia: INSUMOS.json, objetivo3/EVIDENCIAS.json, EVIDENCIAS_TEXTO.json, EJECUCION_NOTEBOOKS.json y REVISION_VISUAL.json. Control propio de conservación en fuentes/control.py. Objetivo 4: diagnóstico y pregunta pendiente; no escenarios. La consolidación editorial no equivale a certificación científica de todos los requisitos ni cierre de tesis.
