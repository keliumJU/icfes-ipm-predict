# Prompt para una nueva sesión — únicamente etapa 1 v3

Continúa en `/home/kelium/Documents/espcarlos/icfes-predict-improved`. Inicia únicamente
la etapa1 de `experimentos_objetivo3_v3`: diseño, congelación y controles de un enfoque
con historial territorial. No ejecutes el piloto ni empieces etapas posteriores.

## Lectura y partida

Lee primero `AGENTS.md`, `experimentos_objetivo3_v2/CONTINUIDAD_V2.md` y, si existe,
`experimentos_objetivo3_v3/CONTINUIDAD_V3.md`. Distingue preparación documental de
etapas realizadas. Después lee únicamente §§1–3 del
`experimentos_objetivo3_v3/PLAN_INVESTIGACION_V3.md`: definiciones comunes y etapa1.
Si no existe continuidad, comenzar con inventario; no inventar estados anteriores.

Comprueba Git y registra el commit real. Cierre conocido v2:
`cc21529532668a966d500e435dca65ef11db09a3`. Puede haber un commit posterior que guarda
este plan/prompt; no es una ejecución de v3. Documenta diferencias y conserva cambios.
Crea/reutiliza `codex/objetivo3-v3-historial` desde la partida real comprobada. Si existe,
inspecciona su estado/ascendencia antes de reutilizarla; no sobrescribas trabajo.

Consulta en lectura protocolo v2.0.2/configuraciones/lock/funciones compartidas fase2;
informe/evidencias fase4; manifiesto/conservación/verificación/ledger/reproducibilidad,
predicciones/selecciones y código necesario fase3. Conservar E3-01 (regex temporal
completa) y E3-02 (cota descriptiva1555 del piloto v2). No trasladar la cota v2 sin
calcular la nueva. No ejecutar cierres/verificaciones/congelaciones que escriban en v2.

## Diseño aprobado, sin decisiones abiertas

- Único panel: fase1 v2/reconstrucciones/base_analitica_departamento_anio_v2.csv,
  SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3`.
- Conservar población/filtros/media global recibida/geografía del colegio y peso igual
  territorio-año. 2020 excluido definitivamente; sin extracción ni sensibilidad.
- `puntaje_previo`: último año autorizado estrictamente anterior del mismo territorio;
  para2021 corresponde2019. No fabricar2020 ni anualizar cambios. 2018 aporta historial,
  pero no tiene objetivo de cambio y no se imputa.
- Persistencia predice puntaje previo, sin ajustar modelo. Modelos aprenden
  `y_actual-puntaje_previo`; predicción final suma cambio estimado y puntaje previo.
  Selección/métricas sobre puntos reconstruidos del global original, no R² del cambio.
- Entradas en orden: puntaje previo seguido de IPM, tasas(15) o ambas(16), con orden
  original. Especificaciones2/16/17 entradas. Código solo llave, sin año/conteos,
  otras pruebas Saber/variables nuevas, imputación ni clipping.
- Exactamente100 configuraciones: `persistencia` más99 configuraciones no correspondientes
  a media del JSON v2, con IDs `delta_`+IDv2. Reutilizar sus familias/parámetros/defaults.
  Semilla20261010; entorno exacto de referencia Python3.12.14/sklearn1.9.1/lockv2,
  comprobado antes de asumir existencia. No instalar automáticamente.
- Escalado exclusivamente dentro del entrenamiento para las familias que lo requieren.
  Selección: bandas MAE/RMSE0.1, menos entradas ajustadas, persistencia antes de familias
  OLS/Ridge/ElasticNet/SVR/GradientBoosting/ExtraTrees y orden JSON. Persistencia tiene
  cero entradas ajustadas para desempate; declarar que usa un puntaje histórico.
- Conservar165 pruebas externas2021–2025. En2021 persistencia fija para procedimiento
  global/especificaciones, sin selección ni entrenamiento de modelos. Desde2022 usar
  internas expansivas2021;2021/2022;2021/2022/2023;2021/2022/2023/2024 respectivamente.
  Cada interna entrena solo años anteriores con cambio observable, empezando2019.
  Nunca inventar validación de modelos2019, ni puntuar candidatos no evaluados2021.
- Guardar ganador global y por especificación, persistencia común elegible. Declarar
  cambio de entrenamiento interno frente a v2 aunque los externos sean idénticos.
- Piloto FUTURO: máximo7200s acumulados para todos los ajustes con transformaciones,
  fallos, arranque/comunicación y repeticiones; ledger propio persistente/serial/terminable.
  Persistencia se calcula sin ajuste ficticio y documenta duración aparte. No alterar
  saldo/modelos/ledgerv2, ni reiniciar ledger para continuar.
- Cinco comprobaciones de repetición del global (una/año), persistencia recalculada sin
  ajuste; atol1e-10/rtol0. No heredar las diez repeticionesv2. Calcular cota nueva antes
  del piloto usando grilla/ventanas/roles y deduplicando solo IDs externos idénticos.
- Referencias futuras: persistencia y predicciones GUARDADASv2global/v1/media/tresOLS,
  verificando huellas e idénticas llaves. No nuevas búsquedas/ajustes de comparadoresv2.
- Meta futura exacta: mejora MAE global≥5% frente a v2 en165 filas, procedimiento
  completo y denominador positivo/finito; sin redondeo extra ni tres-de-cinco-años.
  Informe completo aunque no mejore; notebook personal posterior condicionado a meta.
- Revisión futura: métricas conjuntas/anuales/territoriales y2021–2024/2025 separados;
  diferencias emparejadas firmadas/absolutas/cuadráticas, todos los errores/deterioros.
  Ninguna selección retrospectiva por externos ni pruebas nuevas de significancia.
- Investigación exploratoria:2021–2025 ya examinados. No confirmación independiente,
  causalidad ni pronóstico anterior a publicar el IPM contemporáneo.

## Trabajo autorizado en esta sesión

Escribir exclusivamente dentro de `experimentos_objetivo3_v3/`. No modificar
originales/v1/v2/continuidades previas/.gitignore ni repetir censos raw/descargas.
Conservar estos documentos de planificación; extenderlos solo con decisiones de
implementación justificadas sin modificar el diseño aprobado.

Crear protocolo prospectivo y grilla congelada, panel derivado agregado separado,
fuentes editables/reutilizadas, parámetros/entorno/lock, instrucciones y continuidad
propia. Validar231 registros fuente,198 cambios disponibles y165 externas mediante
código completo; no usar2018 como objetivo ni introducir2020.

No ajustar candidatos sobre el panel real ni calcular predicciones/errores/MAE/selecciones
reales en esta etapa. Usar datos sintéticos/dobles para transformación, reconstrucción,
escalado, selección, métricas y presupuesto. Con datos reales: solo estructura, igualdad,
conservación y trazabilidad. No gastar tiempo del piloto ni crear su ledger operativo
como si se hubiera iniciado.

Controles: historial del mismo territorio estrictamente anterior; manejo2018/2021;
salto2019→2021 sin anualizar; cobertura165; entradas y parámetros exactos100;
reconstrucción de puntajes; escalado/selección sin fuga; persistencia y desempates;
referencias/huellas; métricas independientes; persistencia/reanudación/interrupción/
límite del presupuesto; escrituras solo v3. Separar prueba sintética de resultados reales.

Crear únicamente un notebook útil de controles desde Python editable y un generador
Python que produzca/valide .ipynb. Ejecutar realmente controles, sin salidas inventadas.
No notebooks de modelos ni simulación. Registrar versiones/semillas/rutas/orden/entradas/
salidas y modo de ejecución real; no guardar datos personales.

## Cierre y límite

Cerrar etapa1 con entregables verificables, hallazgos/impacto/alternativa/resolución,
controles aprobados, conservación/manifiesto, continuidad propia y commit local
exclusivamentev3, sin push. Registrar huellas antes del primer ajuste real futuro.
No cerrar controles indispensables sin resolverlos. Conservar antecedentes archivados,
casos completos/Guainía, procedencia local, comparabilidad IPM y dependencia/enlace ecológico.
PDF por secciones/páginas solo si necesarios; indicar páginas realmente leídas.

Guardar un prompt autocontenido que autorice únicamente etapa2 en sesión posterior.
No ejecutarlo. No piloto, fase posterior, entrenamiento final, simulación ni objetivo4.
Una decisión material contradictoria que no pueda resolverse con evidencia requiere
consulta previa; nunca modificar criterios para conseguir mejores métricas.
