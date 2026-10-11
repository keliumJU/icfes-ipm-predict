# Etapa1 v4 — diseño y diagnóstico histórico, sin piloto

Fecha cliente2026-10-10. Protocolo4.0.0. Ejecutar desde raíz del proyecto usando
PYTHONDONTWRITEBYTECODE=1 y /tmp/icfes-v2-fase2-venv/bin/python solo tras verificar
Python3.12.14 y cada paquete requirements.lock.txt/pip check. Sin instalaciones.
Semilla20261010. Originales preservados; toda salida dentro v4.

Orden ejecutado:

1. fuentes/preparar.py: huellas/entorno/antecedentes, derivado231 filas/198 cambios,
   grilla29/defaults y diagnóstico desde CSV históricos (sin nuevos fits).
2. fuentes/controles.py: datos inventados y dobles; carpeta única por ejecución.
3. fuentes/generar_notebook.py: genera/valida y ejecuta tres celdas de
   fuentes/01_diagnostico_controles.py con Python exec. Notebook01_diagnostico_controles.ipynb.
4. fuentes/cerrar.py: conservación, congelación y manifiesto. --verificar solo lee.

Notebook: integridad histórica, métricas guardadas, controles sintéticos. No notebook
personal/modelos/simulación. Reejecutar escribe evidencias nuevas dentro v4 y exige cierre
nuevo explícito; abrirlo solo es lectura. No llamar scripts de piloto anteriores.

Entradas únicas: panel v2 aprobado; código/defaults/lock anteriores en lectura;
CSV v3 y comparadores históricos v2 guardados, selecciones y manifiestos.
Salidas: reconstrucciones/panel_cambios.csv; resultados/configuraciones_congeladas.json,
entorno/integridad_antecedentes/estructura_real/referencias_guardadas; trazabilidad_198.csv;
metricas_historicas/comparaciones_agregadas/diferencias_emparejadas/deterioros_pares/
deterioros_agregados.csv; controles/notebook; informe/registro; congelación/conservación/
manifiesto. El MAE histórico no es resultado v4. Cero fits/correcciones reales y cero
consumo de piloto; ledgers únicamente sintéticos. Etapa2 requiere autorización separada,
su propia congelación operativa y presupuesto7200s; no se ejecuta el prompt guardado.
