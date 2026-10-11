# Etapa1 v3 — diseño congelado y controles

Entradas: único panel agregado autorizado fase1v2, JSON/lock/funciones fase2v2,
manifiestos/evidencias fase3 y fase4. Salidas exclusivamente v3. Sin piloto operativo.
Entorno existente `/tmp/icfes-v2-fase2-venv/bin/python`, Python3.12.14/sklearn1.9.1,
lock exacto; puede ser transitorio. Si falta o difiere, detenerse; no instalar automáticamente.
Semilla20261010. Ejecutar desde la raíz del proyecto con PYTHONDONTWRITEBYTECODE=1.

Orden realmente ejecutado:

1. `etapa1/fuentes/preparar.py`: versiones/manifiestos/huellas, panel derivado y grilla;
   solo estructura real. Reejecución exige igualdad de grilla existente.
2. `etapa1/fuentes/controles.py`: sintéticos/dobles; cada ejecución conserva ledger
   de prueba distinto en resultados/sinteticos/prueba_*. Nunca ledger operativo.
3. `etapa1/fuentes/generar_notebook.py`: genera/valida/ejecuta tres celdas mediante exec;
   controles separados en notebook_sinteticos. Fuente editable01_controles.py.
4. `etapa1/fuentes/cerrar.py`: conservación/manifiesto y congelación v3.

Verificación posterior sin escribir: ejecutar `etapa1/fuentes/cerrar.py --verificar`.
Tras cierre, regenerar/ejecutar notebook altera evidencias y requiere cierre nuevo
explícito antes de comparar con manifiesto. Abrir el notebook es lectura y no ejecuta.
No existe orquestador de piloto ni notebooks de modelos/simulación. Funciones reutilizables
para etapa2 están en comun_v3.py; cada escritura valida destino dentro v3.

Entregables principales: PROTOCOLO_V3.md; configuraciones_congeladas/entorno/estructura_real/
referencias_guardadas/integridad_antecedentes/congelacion_previa/conservacion_final/manifiesto_cierre;
reconstrucciones/panel_historial.csv; notebooks/01_controles.ipynb. Todas las evidencias
indican origen real estructural o sintético. Nueve grupos de controles aprobados.
Cota sin fallos1010, presupuesto futuro7200s, cero segundos de piloto consumidos.

Siguiente sesión: PROMPT_ETAPA2_NUEVA_SESION.md en raízv3; no ejecutarlo en etapa1.
