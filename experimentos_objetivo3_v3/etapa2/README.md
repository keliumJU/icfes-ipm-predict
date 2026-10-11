# Etapa2 v3 — orquestación y piloto exploratorio

Protocolo3.0.0 congelado en etapa1; fuentes editables propias reutilizan comun_v3,
constructor/métricas/bandas/motor de presupuesto v2 exclusivamente en lectura.
Entorno `/tmp/icfes-v2-fase2-venv/bin/python`, Python3.12.14, lock íntegro etapa1
(54 paquetes, sklearn1.9.1), semilla20261010. No instalación ni red.
Ejecutar desde raíz con `PYTHONDONTWRITEBYTECODE=1`.

Orden: comprobar etapa1 con `etapa1/fuentes/cerrar.py --verificar`; verificar cada
paquete y pip check; `etapa2/fuentes/piloto.py --preflight`; `probar.py` (inventados,
dobles y worker sintético); `piloto.py --freeze` antes del primer fit; `piloto.py`;
`verificar.py`; `generar_notebook.py`; documentación/continuidad; `cerrar.py`.
Posteriormente `cerrar.py --verificar` verifica sin escribir. No invocar cierres v2.
No recongelar ni ejecutar preflight después de iniciado el ledger.

Reanudación: misma orden `piloto.py`, mismo directorio/ledger/modelos. Cada ajuste
completado se carga solo tras comprobar su huella; interno nunca se comparte entre
ventanas externas. Hasta dos intentos de infraestructura contando tiempos anteriores;
numérico/convergencia inelegible. Caída pendiente no medida agota saldo conservador.
7200s acumulados seriales, Pipeline completo dentro de spawn terminable. Persistencia
sin estimador/fit, duración aparte. Conservar parciales si falta cobertura; no evaluar
meta sobre subconjunto. Estado incompleto y traceback se guardan ante interrupción.

Entrada: panel_historial.csv y grilla100 exacta de etapa1/resultados; fuente única
6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
No raw.2020 definitivamente excluido;2018 solo historial;2021 persistencia fija sin
selección/candidatos puntuados; internas2021–2024 entrenan cambios anteriores desde2019.
Previo+IPM/tasas/ambas2/16/17; global reconstruido sin clipping/imputación. Peso igual.
Selección global/especificaciones guardada antes externo; deduplicación solo ID idéntico
por ventana. Cinco repeticiones globales, persistencia recalculada, atol1e-10/rtol0.
Cota sin fallos1010 (990 internos+≤16 externos+≤4 repeticiones ajustadas), antecedente
E3-02 v2=1555; E3-01 regex temporal completa conserva separación `_ipm`/internas.

Salidas: resultados/piloto/ ledger, selecciones, modelos/transformaciones/parámetros/
versiones/huellas/advertencias y CSV por artefacto; predicciones internas/externas,
métricas conjuntas/anuales y por especificación, ganadores, meta exacta, fallos,
verificación independiente, controles sintéticos, congelación, conservación/manifiesto.
Notebook01_resultados_piloto resume artefactos guardados; fuente01_resultados_piloto.py
editable y generador nbformat, tres celdas realmente ejecutadas. No notebook personal.

Comparadores v2global/v1/media/tresOLS exclusivamente CSV guardados con huellas/llaves/
observados cotejados, sin búsquedas ni ajustes. Meta conjunta exacta≥5% frente v2 sobre
165 externas completas, denominador positivo/finito. Informe aunque no mejore.
2021–2025 ya examinados: exploratorio, sin confirmación independiente ni causalidad;
IPM contemporáneo impide presentarlo como pronóstico previo a publicación. Conservar
casos completos/Guainía, procedencia local, comparabilidad IPM y enlace ecológico.
Etapa3/revisión completa territorial/cortes/deterioros requiere otra autorización;
no simulación/objetivo4/entrenamiento final/push.
