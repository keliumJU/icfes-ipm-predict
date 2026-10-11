# Hallazgos y resoluciones — etapa2 v4

Fecha cliente2026-10-10, America/Bogota. Evidencia de alcance en
PROTOCOLO_OPERATIVO.md; criterios congelados etapa1 intactos.

|Hallazgo y ubicación verificable|Impacto sobre el objetivo|Alternativa verificable y resolución|
|---|---|---|
|Git HEAD7f25ad066386965a75058e96b4716cdd8a9adb52, partida.json|No existe trabajo posterior que reconciliar|Reutilizar rama limpia codex/objetivo3-v4-correcciones y conservar snapshot íntegro; comprobado|
|Entorno transitorio, entorno.json|No asumir compatibilidad o disponibilidad|Python3.12.14/sklearn1.9.1/54 paquetes lock/pip check comprobados antes de ejecución; sin instalar|
|Guardia histórica cerrar.py etapa1 exige ausencia de etapa2|Su invocación posterior rechazaría etapa2 autorizada|Ejecutado --verificar antes de crear etapa2; verificador propio coteja mismas huellas y continuidad de etapa1 en Git7f25ad0, sin editar congelado; resuelto|
|Reanudación requiere más que modelo existente; piloto.Runner/índice/contexto y pruebas_sinteticas.json|Archivo faltante/alterado no puede rescatarse con nuevo fit o saldo|Verificar todos los archivos/contexto/llaves/observados/matrices/intentos/huellas; rechazo sintético de modelo alterado y persistencia ausente; resuelto|
|Global puede diferir de ganador de grupo; probar.py/seis_externos|Deduplicar por grupo perdería procedimientos|Caso sintético con seis IDs distintos/global diferente; deduplicar solo identidad, siete roles completos; aprobado|
|Corrección común estima una estadística; comun_v4.CorreccionComun y ajustes/entradas_entrenamiento.csv|No es persistencia ni puede estimarse con validación|Mediana de todas las filas train, par promedio de centrales, proceso presupuestado, huella de matrices y mediana guardada; controles sintéticos y auditoría propia|
|Saldo agotado antes de iniciar fit; piloto.Runner.fit y prueba agotado_sin_intento|No registrar un intento inexistente ni asociar el último intento a otro ajuste|Guardia de saldo antes de nuevo intento y prueba que conserva ledger sin ajuste ficticio; resuelto antes de fit real|
|Pruebas y fuentes deben coincidir; probar.py/check_hashes y congelacion_operativa.json|Controles anteriores no bastan después de cambiar código|Tres suites completas conservadas por directorio; suite definitiva liga huellas iniciales/finales idénticas. Cambios previos refuerzan saldo/orden/marcas de inicio/semilla; cero fit real antes de congelación|
|Importaciones en hijos y terminación; sintéticos worker_correccion_comun/worker_ridge/worker_huber y terminacion.json|Spawn podría fallar o dejar procesos después de límite|Procesos reales sobre inventados importan clases propias y Pipeline; terminación e inventario de hijos comprobados, sin ajustar panel real; resuelto|
|Numérico/convergencia versus infraestructura; fallos sintéticos y ledger|No rescatar candidato o dar reintentos ilimitados|Numérico inelegible persistente; infraestructura máximo un reintento presupuestado; caída no medida agota; fallo persistente/límite/integridad/cobertura detienen sin meta parcial; aprobado|
|Atributos previos conservados; etapa2/.gitattributes|Modelos nuevos deben tratarse como binarios en Git|Atributo exclusivamente local a etapa2 *.joblib binary; no alterar atributos/.gitignore anteriores|

Advertencia pip: caché de usuario no escribible, desactivada por pip; pip check
aprobado, sin instalación/red. PDF actualmente leídos: ninguno,0 páginas.
E3-01(regex completa)/E3-02(cota1555v2) son antecedentes resueltos, no cotas v4;
registros activos separados.59/esquema82/causa20212/fórmula global desconocida
permanecen archivados con evidencia y motivo heredados, sin nueva conexión pertinente.

Advertencias activas: casos completos/Guainía238vs404 y21.012106puntos en
v2/fase1/resultados/diagnostico_medias_disponibles.csv; procedencia local no autenticada
independientemente, comparabilidad IPM,hogares/alumnos,residencia/colegio/enlace ecológico,
dependencia territorial/temporal,pocos años.2021–2025 ya examinados: exploratorio,
sin confirmación independiente,causalidad ni pronóstico anticipado demostrado.
No cambiar criterios ni eliminar deterioros. Resultados reales en informe y controles
finales; continuación posterior únicamente mediante nueva autorización.

Aclaración de procedencia sintética: en carpetas worker_sintetico, `origen=real`
es el nombre del motor con proceso real (sin doble), no datos reales. Las filas
fueron inventadas por probar.py; contexto/panel_memoria_sha256 y hashes X/y
identifican esas entradas. panel_sha256/entorno referencian el contrato nominal
de entrada congelada. Esos ensayos quedan bajo resultados/sinteticos, no en
resultados/piloto, y nunca forman métricas o ledger del piloto real. Impacto:
evitar confundir ajuste real de datos inventados con ajuste del panel. Alternativa
resuelta mediante ubicación, código generador, entradas guardadas y esta aclaración.

## Hallazgos del piloto y auditoría completa

- E2-01,verificar.py:126: primera auditoría rechazó dtype int64/float64 de
  cambio_predicho en persistencia frente CSV conjunto. Impacto: cierre detenido,
  aún sin meta/tablasevaluación agregadas. Alternativa: valores exactos con tipos
  numéricos inferidos compatibles, manteniendo todas las llaves/campos/orden.
  Resuelto en extensión independiente documentada/congelada antes de meta;
  fuentes congeladas y ledger intactos. Tests aceptan0int/float, rechazan1e-11 y
  llaves distintas. Auditoría completa aprobada sin ajustes nuevos.
- Meta falsa,meta.json/metricas.csv/ganadores.csv: MAE3.6091786595605684 vs
  persistencia/v3=3.429267191379531; mejora exacta−5.246353175200156%. Impacto:
  experimento no alcanza mejora5%, sin notebook personal. Alternativa verificable:
  conservar global seleccionado y reportar todos resultados sin sustituirlo por
  persistencia o grupo retrospectivo. Resuelto con informe/notebook útil de resultados.
- Correcciónλ0.25 seleccionada internamente en2022 aumenta MAE externo a
  5.991523654472851 respecto a persistencia5.091966313567663 (valor exacto en CSV).
  Impacto: ganancia interna no implica ganancia externa. Alternativa: verificar
  mediana66filas train2019/2021, parámetros/particiones/selección antes externo y
  todas las predicciones. Auditoría aprobada; mantenerλ/criterios/observados y
  deterioro real. Otros cuatro años seleccionan persistencia; ninguna evidencia
  de aporte causalIPM o beneficio incremental de Ridge/Huber.
- Auditoríaverificacion.json:282ajustes=280internos+1externo+1repetición ajustada;
  282intentos,0fallos/advertencias,9570internas,siete×165externas,cinco comprobaciones
  diferencia0,259.8488030679364s propios. Impacto: resultado completo verificable,
  no meta parcial. Alternativa: cotejo independiente de todos los artefactos/orden/
  referencias/llaves/observados; aprobado sin modelos históricos cargados o fits.

Cierre: no controles indispensables pendientes. Revisión de etapa3 y fases
posteriores no ejecutadas; prompt exclusivo guardado para otra autorización.

Precisión documental E2-01: el primer punto de inferencia distinta es externo2022/
procedimiento persistencia, no2021 como decía la enmienda congelada. Se conserva
la enmienda y su SHA; FE_DE_ERRATAS_E2_01.md/diagnostico_tipos_csv.json corrigen la
ubicación con cotejo completo por ventanas. Sin cambios del control/criterios/
resultados/ledger ni ajustes nuevos; problema de transcripción resuelto explícitamente.
