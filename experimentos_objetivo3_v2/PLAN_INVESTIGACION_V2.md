# Investigación v2: mejora predictiva con datos hasta 2025

Plan aprobado por el usuario; guardado el 2026-10-10 (America/Bogota). La autorización de esta sesión comprende crear estos documentos y **ejecutar únicamente fase 1**. Las fases 2–4 permanecen prospectivas y requieren autorización expresa. Este documento conserva sus definiciones, sin implementarlas anticipadamente.

## Decisiones y criterio de entrega

Investigar nuevas configuraciones sobre el panel departamental desde 2018 hasta 2025, **excluyendo definitivamente 2020**. Utilizar 2025 para exploración, sin presentarlo como reserva inédita.

Mantener población, filtros, respuesta, agregación, ponderación y especificaciones IPM/tasas/ambas. Preservar íntegramente el objetivo 3 cerrado. No incorporar otros datos, nuevos predictores, redes neuronales, simulaciones ni avanzar al objetivo 4.

El piloto tendrá **100 configuraciones y dos horas acumuladas de entrenamiento**, incluidas referencias y cualquier repetición necesaria.

**Criterio aprobado para entregar el notebook personal:** reducción de **al menos 5% del MAE conjunto** frente a la configuración ganadora v1 reentrenada y evaluada en las mismas ventanas:

`mejora = 100 × (MAE_referencia − MAE_v2) / MAE_referencia`

No exigir mejora en tres de cinco años. Mostrar siempre RMSE, sesgo y resultados por año y territorio, incluidos deterioros. El 5% es un umbral práctico de entrega, no una prueba de significancia estadística.

El informe completo se entregará aunque no haya mejora. El notebook personal se entregará únicamente si el piloto completo supera ese umbral y sus controles.

## Organización y fuentes

Trabajar en la rama `codex/objetivo3-v2-piloto`, conservando cambios existentes, y guardar todo lo nuevo bajo `experimentos_objetivo3_v2/`.

Crear `PLAN_INVESTIGACION_V2.md`, `PROMPT_INICIO_V2.md` y `CONTINUIDAD_V2.md`. Separar código editable, reconstrucciones, pruebas, notebooks, resultados y registros. No modificar originales, artefactos históricos, continuidad del objetivo 3 ni `.gitignore`. No hacer push.

Fuentes locales previstas:

- Base histórica validada de 198 filas.
- Archivos ICFES 20251 y 20252.
- `Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx`: cobertura declarada 2018–2025; actualización del 14 de abril de 2026. **No buscar ni descargar otro anexo.**
- **Nota adicional:** `panel_departamento_anio_unido_2025.csv` es un consolidado candidato aportado por el usuario. La inspección encontró 231 filas, 33 territorios por año, ausencia de 2020 y llaves únicas. Contiene las 15 tasas, pero no una columna `ipm`; deberá cotejarse y completarse desde el Excel en una reconstrucción separada.

No asumir que el consolidado está validado por su nombre o cantidad de filas.

## Fases de investigación

### Fase 1 — Auditoría y conservación

Registrar Git, commit inicial, cambios existentes y huellas. Consultar AGENTS, continuidad histórica, protocolo v1 y entrega revisada de fase 6.

Auditar íntegramente los archivos ICFES 2025 por bloques. Verificar periodos, población y correspondencia con Saber 11. Si corresponden a Pre Saber, registrar incompatibilidad y consultar antes de cambiar población.

Comprobar por territorio y periodo:

- Registros recibidos, elegibles y exclusiones.
- Faltantes, valores no numéricos, ceros y rangos documentados.
- Sumas, denominadores y medias.
- Concentración de exclusiones y diferencias respecto a controles históricos.

No convertir nulos en cero ni imputar puntajes. Conservar los seis puntajes disponibles y positivos exigidos históricamente.

Como diagnóstico separado, comparar la media de casos completos con la de registros que cumplen los demás filtros y tienen puntaje global válido, aunque falte otra prueba. No cambiar la respuesta principal ni afirmar que este diagnóstico demuestra ausencia de sesgo.

Cotejar el consolidado candidato contra las fuentes. Conservar exactamente las 198 filas históricas y añadir 2025 únicamente después de validar cifras, filtros y cobertura. Completar IPM desde el Excel con trazabilidad por celda.

Validar las 15 tasas y adaptar la lectura a `IPM_Indicadores_Departamento`. No reemplazar cifras históricas por revisiones del nuevo anexo.

Exigir 33 territorios completos y las tres especificaciones disponibles. Ante incompatibilidades materiales, consultar antes de entrenar. Si se consultan PDF, registrar páginas efectivamente revisadas.

Entregar auditoría, panel nuevo si procede, controles, registro de problemas, manifiesto y continuidad. **Sin entrenamiento.**

### Fase 2 — Protocolo, código y pruebas

Congelar panel, divisiones temporales, configuraciones, selección, métricas y criterio del notebook antes de ajustar modelos.

Probar 33 configuraciones por especificación:

| Familia | Configuraciones |
|---|---:|
| OLS | 1 |
| Ridge | 4 |
| Elastic Net | 6 |
| SVR radial | 6 |
| Gradient Boosting | 8 |
| Extra Trees | 8 |

Total: 99 entre IPM/tasas/ambas, más la media del entrenamiento.

Parámetros:

- Ridge: `alpha` = 0.1, 1, 10, 100.
- Elastic Net: `alpha` = 0.01, 0.1, 1; `l1_ratio` = 0.2, 0.8; `max_iter=20000`.
- SVR: `C` = 1, 10, 100; `epsilon` = 0.1, 1; `gamma="scale"`.
- Gradient Boosting: 100/300 árboles × aprendizaje 0.03/0.1 × profundidad 1/2; hoja mínima 3; `subsample=1`.
- Extra Trees: 300 árboles; `max_features` = 0.5/1.0; hoja mínima 1/3/6/10; profundidad sin límite; `n_jobs=1`.

Estandarizar entradas de modelos lineales y SVR exclusivamente con entrenamiento. Semilla `20261010`; registrar versiones y reutilizar el entorno compatible disponible.

Crear funciones compartidas y fuentes Python para generar y validar notebooks, sin editar JSON manualmente.

**Tests obligatorios:**

1. Panel: llaves únicas, años autorizados, ausencia de 2020, cobertura y preservación de filas históricas.
2. Unión: rechazar duplicados, territorios sin correspondencia y entradas indispensables ausentes.
3. Agregación: ejemplos pequeños con resultado conocido que detecten nulos convertidos en cero o denominadores incorrectos.
4. Separación temporal: ninguna fila externa participa en ajuste, transformación o selección.
5. Escalado: un valor extremo añadido al año externo no modifica los parámetros del transformador entrenado.
6. Métricas: ejemplos conocidos y recálculo independiente desde predicciones guardadas.
7. Selección: tolerancias y desempates producen el candidato esperado.
8. Presupuesto: registrar y detener ajustes al alcanzar el límite.
9. Notebook: estructura válida, rutas relativas a la carpeta, ausencia de datos personales y ejecución real del modo de verificación.

### Fase 3 — Piloto temporal

Evaluar ventanas externas 2021–2025. Entrenar únicamente con años anteriores disponibles, siempre excluyendo 2020.

Seleccionar internamente con validación expansiva anterior al año externo, empezando por entrenamiento 2018 y validación 2019.

Selección: MAE mínimo con tolerancia de 0.1; después RMSE con tolerancia de 0.1; menor número de entradas; orden media, OLS, Ridge, Elastic Net, SVR, Gradient Boosting, Extra Trees; finalmente identificador.

Comparar con media del entrenamiento y configuración ganadora v1 reentrenada por ventana con parámetros fijos. Guardar todos los ajustes como artefactos v2 y preservar el modelo congelado.

Registrar tiempos, fallos, predicciones y cobertura. Si el piloto queda incompleto, no comparar candidatos con cobertura desigual ni aplicar el criterio del notebook.

### Fase 4 — Revisión y notebook condicionado

Entregar métricas por año y conjunto, diferencias emparejadas y errores territoriales. Mostrar también 2021–2024 separado para distinguir el aporte de 2025.

Evaluar el umbral del 5% sobre el **procedimiento de selección predefinido**, sin escoger retrospectivamente otra configuración por sus resultados externos.

Si lo alcanza, generar un notebook personal que permita:

- Verificar los resultados guardados sin reentrenar, como modo predeterminado.
- Reejecutar voluntariamente el piloto completo con la configuración congelada.
- Consultar versiones, semillas, instrucciones y tiempo esperado.
- Recalcular comparaciones, métricas y gráficos.
- Ejecutar los controles pertinentes y guardar reproducciones por separado.

Generarlo desde Python y validarlo. Ejecutar realmente el modo de verificación; distinguir esa ejecución de un reentrenamiento completo. No afirmar una reproducción que no se realizó.

Aunque haya mejora, conservar deterioros y límites. No interpretar predicciones como efectos causales ni presentar la evaluación retrospectiva como pronóstico disponible antes de publicarse el IPM.

Cada fase cerrará con evidencia, problemas resueltos y pendientes, continuidad propia y commit local descriptivo. Cualquier fase siguiente requiere autorización expresa.

## Primer prompt para una nueva sesión

El prompt aprobado de entrada a fase 1 se conserva en `PROMPT_INICIO_V2.md`. Después de ejecutarlo, prevalece `CONTINUIDAD_V2.md`: no repetir la partida ni avanzar a fase 2 sin nueva autorización.
