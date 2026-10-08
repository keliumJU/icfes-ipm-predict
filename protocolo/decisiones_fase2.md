# Registro de problemas y decisiones — fase 2

2026-10-08, America/Bogota. Partida `a68f0bb58b7b5268e6025ef33afc64862f8e8cc8`,
Git limpio. Solo decisiones prospectivas, controles sobre agregados y documentación.
No se consultaron métricas históricas para elegir grillas. No se entrenó ni simuló.

| ID / origen | Evidencia y problema | Impacto sobre objetivo | Alternativa verificable | Decisión y comprobación / estado |
|---|---|---|---|---|
| D01 / usuario + comprobación | Continuidad, criterios 1–2; diccionario y cotejo raw/final: promedio usado, mediana no comparada | Confundir centro típico con desempeño promedio cambiaría y | Mantener media del registro elegible o formular otro estimando explícito | Mantener media, suma/denominador sin redondeo; no afirmar superioridad; no contraste de medianas necesario. Ver protocolo §2 y controles. Resuelto |
| D02 / usuario + comprobación | Base 198, filtros y validación fechada; calendario incluye más que A/B | Exclusiones nuevas cambiarían población y comparabilidad | Usar panel reconstruido validado y cotejar solo integridad actual | 33 territorios, Bogotá y 2021; mismos seis años/filtros; sin calendario añadido. Ver verificacion_fase2.json y controles.verificar. Resuelto |
| D03 / nueva | Diccionario: incidencia % personas y tasas % hogares; DANE algoritmo §§4.1–4.5 | Promedios inventados de dimensión perderían significado oficial; colinealidad puede desestabilizar regresión | Mantener 15 tasas, agrupar solo para documentación; regularizar candidato lineal | Tres especificaciones exactas, cinco agrupaciones, Ridge; sin selección por correlación. 15 nombres únicos comprobados. Resuelto |
| D04 / nueva | Cuatro años de desarrollo; ventanas 33/66/99 filas | CV por filas rompe año; CV anidada temporal no cabe en primera ventana; selección puede ser optimista | Máscara por año completo y búsqueda pequeña fija, con posterior evaluación congelada | Tres ventanas, 67 configuraciones; métricas de selección explícitas, sin independencia fingida. Particiones verificadas por código. Resuelto con limitación |
| D05 / usuario + evidencia histórica | Continuidad: prom.pdf pp. físicas 13–14,18,22; nueva ivestigacion .pdf pp.5–7 ya comparan 2023–2024 | No existe prueba totalmente inédita; volver a ajustar por esos resultados produciría fuga | Reevaluación temporal con selección exclusiva hasta 2022 y artefactos congelados | Evaluar ambos años separados/juntos sin reentrenar en 2023 ni reescoger ganador; no se calcularon errores ahora. Protocolo §§4,7. Resuelto con limitación histórica |
| D06 / usuario + nueva | IPM de mismo año en base; continuidad criterio4 | Llamarlo anticipación supondría entradas aún desconocidas | Estimación contemporánea; si se exige anticipación, futuro diseño con entradas anteriores y calendario de publicación | Mantener alcance contemporáneo; no hay instrucción actual que exija anticipación. Alternativa rezagada no implementada ni sustituye objetivo. Resuelto |
| D07 / nueva | Resultado en puntos; métricas históricas de clasificación no reproducidas | Logística/AUC/Brier responderían a otra pregunta | Regresión de media agregada con referencias continuas y errores en puntos | Media y OLS + Ridge/RF/GBR, grillas finitas, MAE/RMSE/sesgo/R², desempate 0.1. Manifestación de 67 candidatos sin ajuste. Resuelto |
| D08 / nueva | Registros por territorio difieren; diccionario n_estudiantes_saber | Ponderar por estudiantes cambia estimando de error hacia territorios grandes | Peso igual por celda; mantener n para diagnóstico | Peso principal uniforme, sin conteos/códigos/año como X. Protocolo §§2–3. Resuelto |
| D09 / evidencia previa | notas_ipm.csv: IPM_Departamentos A50–A53; IPM_Variables_Departamento A864–A868 | Rupturas de medición pueden limitar transporte y atribución de variación | Conservar fuente, reconocer notas y mostrar métricas anuales posteriores | No corregir tasas/excluir 2021; evaluación anual fijada y limitación de encuesta/ecología. No requiere recenso. Resuelto como limitación, no autenticación |
| D10 / evidencia previa | formula20222_raw.csv: 414 diferencias grado11, procedencia conservada | Recalcular global alteraría y sin regla oficial conocida | Conservar puntaje recibido y advertencia | Sin imputación/recalculo; controles actuales de rango/denominador, procedencia fase1 citada. Explicación aritmética desconocida permanece, conservación resuelta |
| D11 / nueva | Solo cuatro años y 33 territorios repetidos | Contraste territorial no equivale a transporte temporal; parámetros ya seleccionados generan optimismo | Contraste leave-one-territory-out fijo en desarrollo, separado y sin reselección | 33 grupos de cuatro filas, entrenamiento32 grupos, reporte diagnóstico con limitación de selección. No ejecutado. Diseño resuelto |
| D12 / nueva comprobación | /usr/bin/python3=3.14.7 sin paquetes; runtime disponible=3.12.14; sklearn/nbformat/ipykernel ausentes | Suponer entorno histórico/Jupyter ejecutado produciría evidencia falsa | Controles y generador de subconjunto ipynb con biblioteca estándar; preparar entorno de modelos más adelante | CLI y celdas ejecutadas realmente; sin outputs, sin afirmar kernel/nbformat. Versiones en JSON; entorno de modelos pendiente de implementación previa a métricas. No bloquea cierre documental |
| D13 / usuario | Continuidad: 59 columnas archivadas; población/puntajes/unión reconstruidos por otra ruta | Reabrir ausencia histórica no añade validez actual | Conservar antecedente y exigir evidencia relevante antes de reabrir | Sin investigación nueva de 59 columnas/esquema82. Archivado, no pendiente activo |
| D14 / nueva | Fallos/advertencias pueden producir ranking con cobertura desigual | Omitir ventanas o recortar predicciones favorecería configuraciones | Cobertura completa; registro de fallo; detención ante integridad/fuga | Inelegible con ventana fallida; sin ampliar búsqueda; no clipping; versionar cualquier enmienda antes de métricas. Protocolo §6. Resuelto |

## Separación entre antecedentes y problemas activos

No hay decisión indispensable activa sin resolver en fase 2. No se cierran artificialmente
controles: panel, variables, particiones y evidencia anterior se verifican por código.
Las limitaciones de D04/D05/D09/D10/D11 permanecen visibles; no impiden el estimando local
acordado ni se convierten en causas demostradas.

Archivados con ubicación y motivo: selección59/esquema82 y causa antigua20212
(`CONTINUIDAD_OBJETIVO_3.md`, salvedades; `auditoria/diagnostico_calidad.md`),
no autenticación de descarga y entorno histórico ausente (mismas fuentes). La nueva ruta
no depende de reconstruir esos criterios; no se transfieren métricas ausentes. Solo se
reabren ante nuevos insumos o discrepancia que afecte población, y, unión o validez.
Adopción de propuesta de tesis por el grupo: pendiente editorial externo, no hecho ni
condición metodológica del protocolo. Modelos, compatibilidad de su entorno, métricas,
contraste territorial y escenarios: tareas posteriores aún no ejecutadas/autorizadas.

Comprobaciones ejecutadas: `fuentes/controles.py`, `fuentes/generar_notebooks.py` y
`fuentes/verificar_cierre.py`; evidencia en `evidencia/`. Los scripts y manifestaciones
se congelan junto con este registro. No se modifica ningún original ni .gitignore.
