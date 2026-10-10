# Fase 3: piloto temporal v2

Esta entrega implementa exclusivamente protocolo2.0.2 y100 configuraciones congeladas de
fase2. Todos los ajustes prospectivos son nuevos; modelos históricos se conservan.

Orden reproducible con `/tmp/icfes-v2-fase2-venv/bin/python`, Python3.12.14 y paquetes
exactos de fase2/requirements.lock.txt (validar antes de ejecutar, no asumir existencia):

1. `fuentes/piloto.py --preflight`: manifiesto, snapshot, panel/198 históricas/defaults/lock.
2. `fuentes/probar.py`: orquestación sobre valores sintéticos y dobles, worker sintético,
   separación/selección, persistencia/reanudación/límite/terminación. Cero ajustes panel.
3. `fuentes/piloto.py --freeze`: huellas operativas previas al primer ajuste real.
4. `fuentes/piloto.py`: ejecución serial autónoma,100 candidatos/ventanas congeladas,
   selección antes de externo; referencias y diez repeticiones. Semilla20261010.
5. `fuentes/enmienda_reporte.py`: invoca recálculo independiente y corrige por regex
   exclusivamente clasificación del agregado interno (registro_problemas F3-05).
6. `fuentes/generar_notebook.py`: genera/valida y ejecuta lectura de artefactos con Python
   exec; sin kernel y sin ajustes. Fuente editable01_resultados_piloto.py.
7. Actualizar continuidad v2 y ejecutar `fuentes/cerrar.py`: conservación e informe/manifiesto.

El ledger se conserva al reanudar. No borrar/recrear ledger para recuperar saldo. Un ajuste
pendiente tras caída agota conservadoramente saldo no demostrable. No volver a ejecutar
preflight/congelación sobre un piloto iniciado; ejecutar piloto reutiliza artefactos completos
con huella y repite la misma selección sin modificar su JSON. No hay reutilización de
internas entre externos ni búsqueda de semillas. Todos los ajustes, incluidos fallos,
referencias y repeticiones, consumen el mismo máximo7200s; tope prevalece. Cota de planificación corregida a1555 sin fallos: ENMIENDAS_TECNICAS.md E3-02.

Entradas: único panel fase1 SHA6cd37c…fb3; configuraciones/protocolo/funciones fase2 en
lectura y comparación v1 congelada. Salidas: INFORME_PILOTO.md, notebook de resultados,
resultados/ (predicciones, métricas conjuntas/anuales/territoriales, ganadores, deterioros,
fallos, verificaciones, ledger, modelos por ajuste, huellas/manifiesto y conservación).
Resultados históricos, pruebas sintéticas y reproducciones reales están identificados.

No notebook personal, fase4, simulación, ajuste final con todos los años, descargas ni push.
2020 excluido definitivamente. Mantener advertencias del protocolo y evitar interpretación
causal de predicciones ecológicas contemporáneas. No cambiar criterios para mejorar métricas.
