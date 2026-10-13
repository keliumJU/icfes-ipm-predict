# Entrega para la última revisión

Comenzar por CONTENIDO_OBJETIVO4.docx. Son resultados nuevos del diseño focal autorizado, con lenguaje explicativo, dos figuras y trazabilidad. ACA2 no fue editado. El plan prospectivo es PLAN_Y_PROTOCOLO.md; la matriz de cumplimiento y las brechas están en MATRIZ_REQUISITOS.md. HALLAZGO_OBJETIVO3.md explica por qué este complemento no reemplaza automáticamente fase6/V2/V6.

## Integración sugerida

En el apartado del objetivo3, después de la evolución de versiones, incorporar «Un diseño focal para comparar aportes de la pobreza»: especificaciones, regularización, reglas y parámetros nuevos. Los antecedentes pueden reutilizarse de entrega_objetivos3_4_final/objetivo3/CONTENIDO_OBJETIVO3.docx; allí las métricas históricas conservan su periodo/procedimiento. En objetivo4, incorporar «Evaluación temporal y referencias», «Construcción y límites de los escenarios» y «Alcance de las conclusiones». El comienzo de este nuevo Word conecta ambos objetivos.

Revisar la metodología de ACA2 pp.58–60 para que describa lo efectivamente hecho: 231 celdas2018–2025 sin2020; tendencia/indicador2021; selector temporal con LOYO aparte; dos cortes separados; evaluación retrospectiva con años vistos; referencias; mediana departamental13.0; escenariosIPMagregado delimitados. No copiar resultados dentro de una promesa de «reserva nunca vista». No afirmar que se ejecutaron escenarios dimensionales coherentes. La aceptación de esas reformulaciones corresponde a la revisión académica; está pendiente y no se declara en nombre del asesor.

No reemplazar globalmente2024por2025: los antecedentes198celdas y resultados fase6 siguen siendo2018–2024. Tampoco ampliar objetivos1/2 sin decisión académica expresa. Las correcciones indispensables de población ya se explican en el Word; otros pendientes de objetivos1/2 siguen fuera de esta fase.

## Cómo reproducir manualmente

Orden de notebooks: 01_preparacion.ipynb y 02_validacion_escenarios.ipynb. Ambos se generaron desde fuentes Python, se validaron con nbformat y tienen salidas de ejecución real secuencial de Python, sin kernel. El segundo conserva las salidas reales del ajuste de7641fits; su celda final añade diez pruebas y figuras verificadas, sin repetir ajustes. Las primeras nueve pruebas fueron las existentes al ajuste; la décima comprueba la publicación gráfica. Ningún resultado fue simulado.

La lectura normal del segundo notebook reutiliza los resultados cerrados. Para un entrenamiento manual nuevo, copiar toda esta carpeta a otra carpeta hermana dentro de este repositorio y retirar únicamente resultados/ de esa copia; ejecutar el notebook desde la copia. No ejecutar sobre originales, editar inventarios cerrados ni borrar resultados de esta entrega. Las rutas de fuentes de datos se resuelven en el repositorio padre; se conservan funciones/semilla/protocolo y el presupuesto3600s/12000fits. Guardar esa reproducción como entrega independiente con su propio control. Si se cambia ubicación, revisar rutas antes de ejecutar.

Entornos usados sin modificaciones: agregación XLSX/TXT y Word con Python3.12.14 del runtime documental existente (pandas/openpyxl/python-docx); modelos, pruebas y notebooks con /tmp/icfes-v2-fase2-venv/bin/python (numpy2.5.3,pandas2.2.3,scikit-learn1.9.1). Las versiones reales del modelo se conservan en resultados/CONGELACION_PREVIA.json. La preparación manual necesita openpyxl, además de pandas/numpy; el notebook02 necesita scikit-learn,joblib,matplotlib. No instalar por defecto. La copia del panel y las salidas contienen únicamente agregados departamentales.

Fuentes editables: preparar.py, modelos.py, resumen.py, graficas.py, tests.py; generadores generar_notebooks.py y actualizar_notebook_publicacion.py. crear_word.py transforma TEXTO_PARA_TESIS.md en Word. PUBLICACION.json distingue modificaciones de presentación posteriores del protocolo/modelo congelados.

## Resultado que se puede defender

El diseño nuevo mejora respecto a composición/tiempo al añadir pobreza, pero no supera persistencia. Tres reducciones efectivas1pp superan soporte; la diferencia estimada es0.574puntos en Meta,Sucre,Tolima. No son impactos de políticas. Ningún3/5pp ni convergencia efectiva pasa los controles. Guardar la brecha sin ampliar soporte para obtener más escenarios. Los criterios son conservadores y no una ley universal de factibilidad; los rechazos significan falta de soporte bajo este protocolo.

La ejecución está completada; no se necesita abrir otra sesión para terminarla. PROMPT_CONTINUIDAD.md sirve únicamente si se continúa integración académica o reproducción en otra sesión. No está autorizado modificar ACA2 original. Esta entrega no certifica los cuatro objetivos ni la tesis completa.

## Ubicaciones de los antecedentes usados como contexto

Informe2018–2024: fase6/entrega/informe_objetivo_3_revisado.md, evaluación2023–2024. Contraste posterior V2: experimentos_objetivo3_v2/fase3/resultados/predicciones_externas.csv, procedimiento_v2. Versión de historia: experimento_final_objetivo3_v6/ejecucion_autorizada/, protocolo y resultados global_v6. La consolidación previa verificable es entrega_objetivos3_4_final/fuentes/analisis.py y sus resultados; no se ejecutaron nuevamente notebooks de estas versiones. Su evolución corresponde al objetivo3 y aquí se reutiliza únicamente para explicar por qué los escenarios requieren un modelo que incluyaIPM.
