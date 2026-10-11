# Etapa2 v5 — orquestación propia y piloto36

Autorización exclusiva enviada por el usuario el 2026-10-10 America/Bogota.
Protocolo5.0.0 y acuerdos de etapa1 intactos; sin instalación, descarga ni push.

Entradas: panel único v2 SHA2566cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;
derivado v4/propio v5 SHA256aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc;
configuraciones36/defaults y lock54 de etapa1; CSV/selecciones/huellas históricos
v1/v2/v3/v4/media/tresOLS, sin cargar sus modelos ni ajustarlos.
Entorno requerido /tmp/icfes-v2-fase2-venv/bin/python,Python3.12.14/sklearn1.9.1,
54 paquetes exactos y pip check; PYTHONDONTWRITEBYTECODE=1, semilla20261010.

Orden desde raíz, con ese entorno:

1. Etapa1 fuentes/cerrar.py --verificar en lectura ANTES de crear etapa2;
   Git asunto exacto/commit109797407d75d2097e5b71f8bcef3fc266bc61d2 y rama
   codex/objetivo3-v5-mae, limpia/sin trabajo posterior. No volver a ejecutar
   guardia histórica tras crear etapa2; verificar_etapa1 coteja huellas en lectura
   y exclusivamente continuidad en su commit histórico, sin excepción para otra ruta.
2. Etapa2 fuentes/piloto.py --preflight: entorno exacto, huellas/derivado completo,
   referencias/selecciones, snapshot inicial. Una vez, sin sobrescribir partida.
3. fuentes/probar.py: inventados/dobles en directorios separados, recorrido completo,
   reanudación/auditoría/errores/rutas/imports/terminación. Conserva ensayos previos.
4. fuentes/piloto.py --freeze: liga fuentes propias/reutilizadas en lectura,
   defaults,entradas,entorno y pruebas ANTES del primer fit real. No recongelar.
5. fuentes/piloto.py: serial/spawn terminable, ledger propio7200s persistente.
   Reanudación solo con contexto/índice/huellas íntegros, sin ampliar saldo.
   Persistencia sin fit cronometrada aparte; cota378 sin fallos/reintentos.
6. fuentes/verificar.py: auditoría integral desde artefactos/CSV guardados,
   cero nuevos ajustes/modelos cargados; métricas math.fsum y meta global exacta.
7. fuentes/generar_notebook.py: fuente editable01_resultados_piloto.py,
   nbformat, tres celdas de lectura realmente ejecutadas mediante Python exec.
   Notebook01_resultados_piloto.ipynb; no kernel ni reentrenamiento.
8. Documentación,continuidad con antecedente íntegro,prompt etapa3 guardado NO
   ejecutado; fuentes/cerrar.py y --verificar. Commit local únicamentev5.

Salida: resultados/piloto con contexto/índice/ledger/selecciones/ajustes propios,
modelos binarios/parámetros completos/entradas/transforms/versiones/semilla/
advertencias/tiempos/huellas/predicciones/repeticiones/estado; resultados de pruebas,
congelación,partida,entorno,lecturas,auditoría,métricas conjuntas/anuales/territoriales,
ganadores,diferencias emparejadas/todos deterioros,meta,fallos,notebookverificación,
conservación/manifiesto; INFORME_PILOTO.md/registro_problemas.md.

No notebook personal, etapa3, simulación, objetivo4 ni entrenamiento final.
2021–2025 ya examinados: exploratorio, sin confirmación independiente ni causalidad.
Estado definitivo y pendientes verificables en informe,meta y continuidad.
