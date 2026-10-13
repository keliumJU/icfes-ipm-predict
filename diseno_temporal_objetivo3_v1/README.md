# Diseño temporal objetivo3 v1 — documentos preparados, piloto no iniciado

Propuesta1.0.0,2026-10-11. Usuario autorizó diseñar el siguiente protocolo,sin entrenar.
Se propone conservar36candidatos/grupos/selecciónv5 y cambiar únicamente pesos de
entrenamiento:recenciaexponencial consemivida2años,toda historia retenida.
La evaluación sigueigualpeso territorio-año ymeta5%global frentepersistencia.
No eficacia demostrada;todos2021–2025vistos,solo evaluaciónexploratoria disponible.

- PROTOCOLO_TEMPORAL.md:comparación,decisiones materiales,ventanas/criterios/controles.
- ESPECIFICACION_PROPUESTA.json:36candidatos/defaults/grupos copiados exactos,reglas
  de pesos/aplicación/selección/evaluación/presupuesto futuro;no configuraciónoperativa.
- HISTORIA_Y_EVALUACION.md:inventario231/33/7años,ningún holdoutinédito disponible.
- EVIDENCIA_Y_DECISIONES.md/resultados/evidencias.json:archivo/llave/n/SHA/impacto/
  alternativa/resolución;separar usuario,comprobaciones ypropuestasnuevas.
- PLAN_DISENO.md/CONTINUIDAD_DISENO.md:alcance y cierre documental propio.
- PROMPT_FASE1_IMPLEMENTACION.md:solo al enviarlo aprueba propuesta y autoriza
  implementación/pruebasinventadas/congelación,SIN fits reales.
- PROMPT_FASE2_PILOTO.md:solo al enviarlo despuésfase1válida autoriza piloto aparte.
- fuentes/generar_diseno.py:generador/validador documental stdlib,sinestimadores.
- resultados/:partida/snapshotprevio,lecturas/registro/aceptación/conservación/manifiesto.

Verificación solo lectura,desde raíz:
`PYTHONDONTWRITEBYTECODE=1 python3 diseno_temporal_objetivo3_v1/fuentes/generar_diseno.py --verificar`
No volver a generar sobre destinos existentes. No modelos/pesosreales/predicciones/
métricas/controlesexperimentales/notebooks/ledger nuevos en esta fase.

El diagnóstico íntegro permanece en diagnostico_objetivo3_v1,inclusocontinuidad;
v1–v5intactos. No commit,push,instalaciones/descargas/nuevasfuentes.
Los prompts son artefactos guardados,no autorizaciones implícitas. La semivida2 y
ponderaciónscaler/modelo deben aprobarse al autorizarfase1;no experimentoejecutado.
