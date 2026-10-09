# Decisiones previas al primer ajuste — fase 3, 2026-10-09

Partida: 7e95ffe823c3d08f345620c0f9bc65dc72fae7d5; Git limpio. Autorización: solicitud del usuario de ejecutar exclusivamente fase 3, incluida reevaluación temporal congelada. Originales, evidencia anterior y .gitignore se conservan.

## F03-01: discrepancias entre plan y protocolo

Evidencia: PLAN_OBJETIVO_3.md líneas 65–85 frente a protocolo/PROTOCOLO_OBJETIVO_3.md §§3–7 y configuracion.py. El plan propone persistencia territorial, ElasticNet y XGBoost, OLS solo IPM, Ridge con 13 alphas, RF con 500 árboles y grilla mayor, semilla 42 y desempate general por complejidad. Protocolo v1.0 fija media y OLS con tres especificaciones, Ridge con cinco alphas, RF con 300 árboles y ocho combinaciones por especificación, GradientBoosting con ocho combinaciones, semilla 20261008, tolerancia 0.1 en MAE/RMSE y orden explícito. Persistencia, ElasticNet y XGBoost no forman parte de los 67 candidatos congelados.

Impacto: combinar documentos alteraría búsqueda y selección. Alternativa verificable: reproducir exactamente candidatos_congelados.json y usar las reglas del protocolo. Decisión previa a métricas: prevalece v1.0 por instrucción del usuario; no se agregan referencias ni familias del plan. La ausencia de esas familias es diferencia de diseño, no fallo ni exclusión por resultado. Comprobación: preparación exige igualdad de lista y huellas, exporta defaults completos antes del primer ajuste.

## F03-02: entorno

Evidencia: primer intento de instalación en entorno /tmp aislado falló por DNS del sandbox, sin ajuste realizado. Impacto: no se puede asumir compatibilidad por referencias web. Alternativa: descarga autorizada de los mismos paquetes. Decisión: instalar sklearn 1.9.1 con Python 3.12.14 y bloquear todas las versiones resueltas antes de ajustar. Comprobación: pip check, imports, construcción de 67 estimadores, API de pipeline y manifiesto preparacion.json. Los fallos de infraestructura y de candidatos se registran por separado.

## F03-03: límites de fase

Evidencia: PLAN fase3 (65–85), protocolo §7 y README etapa04. Reevaluación autorizada explícitamente ahora; contraste leave-one-territory-out responde a robustez de fase4 y el protocolo lo definió prospectivamente. Alternativa: separar reevaluación y diagnóstico territorial. Decisión: ejecutar reevaluación sin actualización con 2023; posponer contraste territorial y simulaciones a autorización posterior. No son controles de fuga pendientes del ajuste temporal. No se crean notebooks de simulación.

## F03-04: congelación y fallos

La preparación no calcula errores de reserva. Desarrollo recibe exclusivamente 132 filas. Se guardan parámetros/defaults de los 67 candidatos; cada pipeline aprende escalado dentro de cada ventana. Un candidato necesita tres ventanas válidas; warnings de convergencia y predicciones no finitas lo inhabilitan. Se conserva traceback, parámetros, ventana y versiones. Se congela la unión de ganadores por especificación (media común participa) y referencias antes de reevaluar; no se cambia ganador con errores reservados. Fechas y huellas prueban secuencia, no convierten reserva previamente expuesta en prueba inédita.
