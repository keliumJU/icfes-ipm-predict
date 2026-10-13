# Etapa1 temporal — implementación y controles, sin fits reales

Fecha 2026-10-11, America/Bogota. El prompt enviado por el usuario aprueba el
protocolo documental 1.0.0 y la semivida fija 2. No autoriza piloto. No había
continuidad experimental previa; se inició con inventario.

La implementación y los 17 grupos de controles finales están aprobados. El notebook
`notebooks/01_controles_recencia.ipynb` ejecutó sus seis celdas sobre inventados.
Las pruebas incluyen los 35 estimadores ponderados, su ruta uniforme y la ruta
original sin pesos, además de dobles seriales y procesos hijos. No hay ajuste,
modelo guardado, predicción, MAE ni meta nuevos sobre el panel real.

Orden y entradas/salidas:

1. `fuentes/preflight.py`: entorno exacto, Git y antecedentes → `resultados/entorno.json`,
   inventario y huellas. Verifica 29.640 versionados y 121 archivos diagnóstico/diseño.
2. `fuentes/comun.py`: constructor, reconstrucción, pesos, routing, selección,
   CSV, cobertura/linaje y referencias; todas las fuentes históricas solo lectura.
   Reconstrucción real únicamente en memoria, exacta 231/33/198; reporte en
   `resultados/reconstruccion_referencias.json`. No calcula pesos reales ni entrena.
3. `fuentes/worker.py`, `motor.py`, `orquestacion.py`: arquitectura propia serial,
   contratos v5, pesos nuevos y pruebas de fallos/tiempo. La interfaz ejecutable de
   etapa1 exige origen inventado y guarda estados solo en `resultados/inventados/`.
   No importa runners viejos ni activa el ámbito operativo de fase2.
4. `fuentes/pruebas.py`: 17 grupos → `resultados/pruebas_cierre.json` y fixtures
   propios inventados. Los reportes `pruebas.json` (fallo inicial) y
   `pruebas_finales.json` (primera corrección) se conservan. Los fixtures incluyen
   symlinks rechazados y estado corrupto deliberado: no son un ledger operativo.
5. `fuentes/01_controles.py` + `generar_notebook.py`: Python editable → notebook
   nbformat validado y `resultados/notebook.json`. Ejecución real por celda mediante
   exec Python, stdout capturado; no se afirma ejecución por kernel.
6. `fuentes/cerrar_etapa1.py`: controles/documentos → configuración operativa,
   congelación, conservación, aceptación y manifiesto, con verificación independiente.

Usar exclusivamente `/tmp/icfes-v2-fase2-venv/bin/python`,
`PYTHONDONTWRITEBYTECODE=1`, Python3.12.14/sklearn1.9.1/54 paquetes exactos lock v4;
semilla 20261010. Los entregables son de creación exclusiva; para repetir controles
usar nuevos nombres propios, sin sobrescribir reportes previos. Un cambio de fuentes
obliga revalidación y nueva congelación antes de cualquier fit real autorizado.

La congelación operativa corresponde a esta implementación y sus controles;
no equivale a una autorización de ejecución. La fase2 requerirá su prompt enviado,
comprobación del cierre y del entorno, y ámbito de persistencia propio de etapa2.
Reutilizar funciones y defaults congelados, sin importar runners históricos.
7200s/378 son contrato futuro, sin saldo disponible actual. No modificar el diseño
documental, la semivida o criterios después de resultados.

Advertencias vigentes: Guainía238vs404/21.012106 puntos, evidencia histórica en
`experimentos_objetivo3_v2/fase1/resultados/diagnostico_medias_disponibles.csv`;
procedencia local no autenticada; IPM hogares/alumnos; colegio/residencia/enlace
ecológico; dependencia territorial/temporal y pocos años. 2021–2025 ya vistos:
exploratorio, sin confirmación independiente, causalidad o pronóstico anticipado
demostrado. V5 sigue con meta no satisfecha. Antecedentes archivados no reabiertos;
no etapa3v5/notebook personal/simulación/objetivo4/entrenamiento final/commit/push.
