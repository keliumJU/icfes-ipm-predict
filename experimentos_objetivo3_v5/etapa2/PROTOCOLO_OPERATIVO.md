# Etapa2 v5 — contrato operativo previo al primer fit

Autorización enviada por el usuario el 2026-10-10 America/Bogota. Protocolo
5.0.0, grupos, grilla36, defaults, población, fuente, particiones, selección y
meta de etapa1 permanecen intactos. Solo escritura etapa2 y continuidad v5.

piloto.py es una adaptación propia explícita de la estructura v4 leída:
importa comun_v5 de etapa1, no importa ni ejecuta piloto.py v4; usa motor.py y
worker.py propios, cobertura siete roles, registros36 con razones, cota378,
comparación exacta CSV int/float y entorno exacto. No hereda candidatos29 ni ledger.
Worker spawn ejecuta Pipeline completo; motor cuenta arranque, fit, comunicación,
fallos, retry y repeticiones. Contexto/índice/huellas e intento se guardan antes
lanzamiento. Éxito sin artefacto íntegro detiene; caída pendiente agota saldo.
Todo intento serial tiene proceso terminable; límite detiene, sin meta parcial.
Numérico/convergencia inelegible persistente por ajuste; infra máximo un retry,
segundo fallo detiene. Presupuesto real7200 no reiniciable ni ampliable.
Persistencia recalculada y cronometrada aparte sin fit. No cache entre externos.

Auditor propio verificar.py relee todos artefactos/350 internos potenciales,
parámetros completos/matrices/años/observados/transforms/modelos por hash sin
cargarlos; selección antes externo, IDs deduplicados solo por identidad, ledger,
repeticiones, 7×165 externas, fuentes y referencias CSV históricas. Métricas
independientes math.fsum; global único decide mejora exacta≥5%. Auditor reconoce
E2-01 externo2022/persistencia/cambio_predicho por valores exactos; fuentes v4 intactas.

Pruebas inventadas/dobles y worker real inventado antes de congelación nueva;
fuentes/defaults/entradas/entorno ligados por SHA. Notebook de resultados solo
lee resultados guardados; no notebook personal/etapa3/simulación/modelo final.
2021–2025 examinados: exploratorio sin confirmación independiente ni causalidad.
