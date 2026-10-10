# Enmiendas técnicas de fase 3 — sin modificación del protocolo congelado

Fecha cliente2026-10-10. Se preserva fase2/PROTOCOLO_V2.md byte a byte y criterios2.0.2.
Ninguna enmienda modifica población, selección, métricas, modelos o presupuesto7200s.

## E3-01: clasificación de filas del agregado interno

Detectada por revisión estática antes del primer recálculo/evaluación conjunta real.
`fuentes/verificar_resultados.py` usaba subcadena `_i`, presente también en `_ipm` de
algunos externos. No afecta selección, que lee rutas eAAAA_iAAAA_ID exactas, ni métricas
externas guardadas por la orquestación. Impacto: el CSV agregado interno podría incorporar
filas externas IPM y deteriorar trazabilidad. Alternativa resuelta: extensión
`fuentes/enmienda_reporte.py`, regex de etiqueta temporal completa. Invoca auditoría
congelada y reconstruye exclusivamente agregado interno; además comprueba particiones
exactas/roles. Prueba sintética positiva/negativa en pruebas_recalculo.json. Con ejecución
completa sin fallos exige49.500 filas internas. No reentrenamiento ni cambio del selector.

## E3-02: cota aritmética de ajustes externos

Identificada contando etiquetas/estados del ledger, antes de leer métricas reales para
el informe. Evidencia: resultados/conteo_enmienda.json; ventana2022 contiene200 internos,
9 externos, cero fallos. El protocolo §7 estima máximo8 externos/ventana y1550 totales,
pero sus roles obligatorios permiten9 IDs distintos: ganador global(1), tres ganadores
por especificación(3), media(1), tres OLS(3), referencia v1(1). La selección por bandas
puede producir global distinto del ganador en su especificación: las bandas MAE y luego
RMSE se recalculan dentro de cada conjunto. No hay teorema de identidad que autorice
suprimir ese ajuste ni alguno de los comparadores requeridos.

Impacto: cota de planificación incorrecta; **no cambia la búsqueda100, las15 internas,
el orden operativo, ni el presupuesto estricto7200s**. Alternativas: suprimir roles/cambiar
selección reduciría cobertura o criterios y se descarta; conservar todos los roles y
deduplicar únicamente IDs iguales dentro de la misma ventana respeta §5 y §7 y la orden
del usuario. Decisión: implementación ya deduplica IDs por ventana en orden JSON y después
v1; no modificar ni repetir ajustes. Se corrige solo cota descriptiva a≤45 externos,
≤1555 totales sin fallos (1500 internos+45 externos+10 repeticiones). Cada ajuste se carga
al mismo ledger; el tope de tiempo prevalece. El1550 del protocolo es estimación del plan,
no un segundo presupuesto independiente. Conteo efectivo y tiempos se informan al cierre.
No se usa desempeño externo para tomar esta decisión ni se altera criterio para mejorar métricas.
