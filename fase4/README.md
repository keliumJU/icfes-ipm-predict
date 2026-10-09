# Fase 4 — ejecución y entregables

Alcance exclusivo: contraste territorial del protocolo §7, robustez y explicaciones descriptivas. Partida9a22b8adc406423fa6829b75e77d7473deffe710, árbol limpio. No modifica fase3, protocolo v1.0, originales o .gitignore; no push ni simulación. Diferencias plan/protocolo resueltas antes de calcular: decisiones_previas.md. Resultados e impacto de hallazgos: informe.md.

## Orden efectivamente realizado

Entorno aislado existente `/tmp/icfes-fase3-venv`; Python3.12.14 y dependencias exactas de fase3/requirements.lock.txt, verificadas contra preparacion.json. sklearn1.9.1, numpy2.5.3, pandas2.2.3, scipy1.18.1, nbformat5.10.4, nbclient0.10.2, ipykernel6.30.1. Semilla20261008; un hilo BLAS/OpenMP. Entorno transitorio: si desaparece, reconstruirlo con el bloqueo de fase3 antes de cargar modelos.

1. Leer continuidad/documentos y solo fase4 del plan; comprobar Git limpio y partida. Escribir decisiones_previas.md.
2. `analisis.prepare()`: verificar manifiesto fase3 e insumos de preparación/base/protocolo, pip check/versiones; snapshot inicial sin alterar evidencias.
3. `generar_notebooks.py`: generar desde marcadores Python, validar nbformat y ejecutar05→06 en kernel explícito del venv. El intento sandbox se interrumpió sin ajustes; ejecución fuera del sandbox aprobada terminó. Detalle en incidencias_ejecucion.md.
4. `verificar_cierre.py`: cálculo independiente de métricas/bootstrap/asociaciones, cobertura, conservación y tres ajustes focales adicionales por control (dos controles realizados, seis ajustes, 12 predicciones reproducidas en cada control). No búsqueda.
5. `documentar.py`: informe desde resultados reales y discusión concreta en fuentes. Generador `--reusar-salidas`: exige código idéntico, conserva salidas/counts del kernel y valida formato. No JSON manual ni reentrenamiento.
6. Actualizar continuidad, repetir controles finales de documentación/conservación y escribir manifiesto_cierre.json. Commit descriptivo local sin push.

## Reproducir sin sobrescribir cierre

No ejecutar preparación de nuevo en el árbol cerrado: la continuidad y el commit han cambiado deliberadamente. El script siguiente crea una copia **inexistente**, vuelve al commit de partida, copia las fuentes nuevas y decisiones previas, reutiliza el venv verificado y ejecuta la secuencia. Nunca escribe en el repositorio fuente:

```bash
/tmp/icfes-fase3-venv/bin/python fase4/fuentes/reproducir.py /tmp/icfes-fase4-reproduccion-NUEVA
```

Puede necesitar autorización para kernel/conexiones locales. La segunda ejecución completa en copia no se realizó en este cierre; sí las verificaciones concretas descritas. El script no instala paquetes, no relee raw_data ni hace push. La copia mantiene el protocolo y fase3 del commit autorizado. Los notebooks usan rutas relativas al proyecto y kernel explícito del ejecutable invocador.

## Entregables

- `resultados/predicciones_territoriales.csv`:396 filas, observados/predicciones y errores firmados/absolutos/cuadrados, código/año/modelo.
- `metricas_agrupadas.csv`, `metricas_territorio.csv`, `metricas_anio.csv`:3/99/12 filas, MAE/RMSE/sesgo/R². `particiones.json`:99 grupos con128/4 filas y parámetros fijos.
- `bootstrap_resumen.csv` y `bootstrap_replicas.csv`:7 comparaciones y14.000 réplicas pareadas; contextos territorial/temporal diferenciados. Sin ajustes en bootstrap.
- `asociaciones_longitudinales.csv`:16 asociaciones entre/dentro/doble centrado en desarrollo. `coeficientes_ols_congelados.csv`, `correlaciones_predictores.csv`, `pares_correlacion.csv`, `colinealidad.csv`: explicaciones diagnósticas sin causalidad ni nuevos OLS.
- `soporte_territorial.csv`, `resumen_soporte.csv`, `diagnostico_tamanos.csv`, `distribucion_errores.csv`, `influencia_grupos_errores.csv`, `mayores_errores_territoriales.csv`: diagnósticos completos sin excluir observaciones.
- `fallos.json`/`advertencias.json`: vacíos porque todos los modelos completaron; incidencia de infraestructura separada.
- `preparacion.json`, `verificacion.json`, `verificacion_notebooks.json`, `manifiesto_cierre.json`:huellas/versiones/conservación/evidencia.
- `notebooks/05_contraste_territorial.ipynb`, `06_robustez_explicaciones.ipynb`:ejecutados realmente, narrativa amplia, discusión concreta después, fuentes editables bajo fase4/fuentes. No escenarios.

Los archivos de resultados de esta lista están bajo fase4/resultados, salvo notebooks. Los132 errores por especificación no son132 réplicas independientes. El contraste tiene sesgo de selección; los percentiles bootstrap son dispersión condicional, no incertidumbre entre años futuros. Ganador y reevaluación temporal de fase3 permanecen cerrados. No hay controles indispensables activos; límites y condición de avance en informe y continuidad. Los originales e históricos se preservan.
