# Hallazgos etapa2 — impacto, alternativa y resolución

Fecha cliente2026-10-10, America/Bogota. No cambios metodológicos ni de criterios.

1. **Partida real y cierre previo.** Git identifica45fa051ffadc0fc25a326605069dd2f93920898f
   por el asunto solicitado; rama correcta limpia, ancestro v2cc215295. Impacto:
   permite continuar conservando etapa1 y antecedentes. Alternativa: comprobar
   ascendencia/huellas antes de reutilizar. Resuelto en resultados/partida.json,
   verificación inicial `etapa1/fuentes/cerrar.py --verificar` aprobada, sin escribir.
2. **Entorno transitorio disponible.** Python3.12.14 y54 paquetes exactos, pip check
   sin dependencias rotas. La caché pip no escribible produce advertencia, no error
   de dependencias. Impacto: ejecución en entorno congelado disponible sin instalar.
   Alternativa: comprobar versiones una a una y no asumir disponibilidad. Resuelto
   en resultados/entorno.json; no descarga ni instalación ni cambio a lock.
3. **Columna de trazabilidad del derivado.** Primer preflight detectó36 columnas frente
   a35 reconstruidas: `fuente_sha256` fue añadida explícitamente por preparar.py:59
   de etapa1. Impacto: comprobación de igualdad debe incluir trazabilidad. Alternativa:
   reconstruir también esa columna y comparar todas, nunca eliminarla de la fuente.
   Resuelto antes de cualquier fit, preflight aprobado; código piloto.py/preflight.
   Fuente/derivado/criterios intactos. No era divergencia numérica ni control pendiente.
4. **Error del doble para prueba de límite.** Primer ensayo completo recorrió cinco
   ventanas, pero la prueba aislada pasóNone a un doble que exige arrays finitos.
   Impacto: control de límite no demostrado por ese ensayo. Alternativa: arrays
   inventados compatibles con el contrato. Resuelto repitiendo suite completa con
   doble corregido; ambas carpetas sintéticas conservadas en resultados/sinteticos.
   Cero consumo de ledger real. Evidencia aprobada en pruebas_sinteticas.json.
5. **Global no necesariamente igual a ganador de su especificación.** Las bandas se
   recalculan por ámbito. Impacto: asumir coincidencia podría omitir un externo.
   Alternativa: unir IDs de cuatro roles, deduplicando solo ID igual por ventana.
   Resuelto con prueba de cuatro IDs distintos (103 ajustes dobles:99+4), y ventanas
   completas con1006 ajustes dobles (990+12+4), más persistencia sin fit. Evidencia
   en pruebas_sinteticas.json y carpeta cuatro_externos. Cota1010 conservada.
6. **Contabilidad y reanudación.** Repetir un intento de infraestructura después de
   reanudar no debe devolver intentos/saldo. Impacto: límite efectivo podría ampliarse.
   Alternativa: contar intentos guardados en ledger antes de fit y cargar todo fallo.
   Resuelto en Runner.fit y pruebas reintento/permanente/numerico/caida/limite/terminacion.
   Una caída pendiente no medida agota conservadoramente; no reinicio ni ampliación.
7. **Continuidad mutable y manifiesto histórico.** El manifiesto etapa1 incluye la
   continuidad de su cierre. Impacto: tras actualización autorizada, compararla como
   actual daría una divergencia esperada. Alternativa verificable: cotejar únicamente
   esa continuidad en su commit45fa051 y todas las otras rutas en disco, conservar
   antecedente íntegro. Resuelto en verificar_etapa1; no excepción para fuentes,
   grilla, protocolo, datos o evidencia. Snapshot etapa2 protege todo lo demás.

E3-01 temporal regex completa y E3-02 cota1555 v2 permanecen antecedentes resueltos,
con evidencia en etapa1/PROTOCOLO_V3.md §4 y registros v2. No se reabren ni se trasladan
como errores activos v3. Cota propia1010 y límite7200s intactos.

Límites científicos activos heredados: casos completos/Guainía238 frente404 y
21.012106 puntos (experimentos_objetivo3_v2/fase1/resultados/diagnostico_medias_disponibles.csv),
procedencia local no autenticada independientemente, comparabilidad IPM, poblaciones
hogares/alumnos, geografía residencia/colegio/enlace ecológico, dependencia territorial/
temporal y pocos años. Alternativa dentro de etapa2: declararlos, preservar población/
territorios/valores y cobertura; no cambiar filtros ni atribuir efectos causales.
2021–2025 previamente examinados, no confirmación independiente ni pronóstico previo
al IPM.59/esquema82, causa antigua20212 y fórmula global desconocida siguen archivados
con evidencia/motivo heredados en continuidadv2; sin información nueva, no reapertura.

8. **Persistencia ganó todas las ventanas.** Impacto: la mejora conjunta frentev2 no
   prueba contribución incremental del IPM ni de los99 modelos de cambio. Alternativa:
   informar ganador real, dependencia histórica y mínimos internos, sin elegir otro
   modelo por externos. Resuelto en INFORME_PILOTO.md, ganadores.csv y seleccion_AAAA.json.
9. **Deterioro2022 y mayor magnitud del sesgo conjunto.** Impacto: mejoraMAE conjunta
   no es beneficio uniforme. Alternativa: conservar métricas completas y explicitar
   deterioro sin modificar filtros/bandas. Resuelto en informe y metricas.csv. Revisión
   completa territorial/cortes/diferencias queda para etapa3 separada, no control
   indispensable pendiente de etapa2. No ajuste nuevo ni prueba de significancia.

Cierre actual:990 ajustes reales,0 fallos/advertencias,165 externas por procedimiento,
cinco repeticiones diferencia0; auditoría independiente aprobada. No quedan controles
indispensables pendientes de etapa2. Presupuesto y criterios intactos.

10. **Git interpretó cuatro modelos comprimidos como texto.** El control de espacios
    marcó bytes de cuatro modelo.joblib como espacios finales; son artefactos binarios,
    no líneas de fuente. Impacto: falsos positivos en revisión del diff, sin diferencia
    numérica ni corrupción (huellas comprobadas). Alternativa: declarar *.joblib binary
    mediante .gitattributes exclusivamente dentro de etapa2. Resuelto sin tocar modelos,
    .gitignore ni atributos externos; volver a verificar diff/conservación/manifiesto.
    El primer commit local6a10eef conservó íntegros los artefactos; el complemento local
    clasifica binarios y actualiza la evidencia, sin push ni nuevos ajustes.
