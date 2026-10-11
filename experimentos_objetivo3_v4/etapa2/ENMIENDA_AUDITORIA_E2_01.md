# E2-01 — inferencia de tipos de CSV en comparación de artefactos

Fecha cliente2026-10-10. Justificada después de terminar el piloto y ANTES de
calcular métricas conjuntas/meta. No cambia los criterios ni las fuentes congeladas.

Ubicación: fuentes/verificar.py, comparación de q[allframes[label].columns] con
predicciones.csv de persistencia, línea126. Primera auditoría detenida en2021;
cambio_predicho leido int64 para33 ceros en artefacto individual, float64 en el CSV
conjunto que incluye otros IDs y predicciones fraccionarias. assert_frame_equal
rechazó dtype, no valores. No meta ni tablas de evaluación agregadas se produjeron
en ese intento. Piloto completó todas las ventanas; no nuevos ajustes requeridos.

Impacto: impedía concluir auditoría de equivalencia de archivos cuyo CSV no declara
tipos pandas. Alternativa lógica: preservar todos los campos/llaves/orden/valores
y exigir igualdad exacta, permitiendo solo inferencia distinta del tipo numérico.
No relajar atol de repetición ni tolerancias de selección. Cero int/float representa
la misma predicción y no modifica el cálculo estadístico.

Resolución: extensión independiente fuentes/verificar_extension.py lee el verificador
original por inspect, exige un único punto exacto documentado y recompila en memoria
solo esa comparación con check_dtype=False/check_exact=True. Esta comparación es
estricta en valores, también en los campos flotantes donde pandas por defecto puede
usar tolerancia. Todas las demás comprobaciones permanecen sin cambios. El archivo
congelado y la orquestación se conservan por sus SHA. No cargar modelos/ajustar/
seleccionar de nuevo con externos. Ledger debe mantener SHA antes/después.

Pruebas exclusivamente inventadas: acepta cero entero/flotante; rechaza cambio1e-11,
código/año distintos. Congelacion_extension_auditoria.json fija fuente/documento y
pruebas antes del primer recálculo de meta; verificacion_extension_auditoria.json
registra ejecución, ledger intacto y cero ajustes. Esta extensión es una corrección
explícita de auditoría, no un cambio en el experimento ni una modificación silenciosa
del congelado. Fuentes originales siguen verificándose con congelacion_operativa.json.
Para reauditar después del cierre usar la extensión; cerrar.py --verificar comprueba
conservación/manifiesto que incluye sus huellas, sin volver a ejecutar el piloto.
