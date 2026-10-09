# Fase 3: procedimiento y entregables reproducibles

Ejecución actual: 2026-10-09, America/Bogota. Partida limpia
`7e95ffe823c3d08f345620c0f9bc65dc72fae7d5`. Solo fase3, con reevaluación explícitamente
autorizada; sin contraste territorial, simulación, cambios de originales ni push.
El protocolo v1.0 queda intacto. Diferencias con el plan: decisiones.md (previas al ajuste).
Incidencias efectivamente encontradas: incidencias_ejecucion.md.

## Orden y entorno

Python 3.12.14 aislado en `/tmp/icfes-fase3-venv` (entorno transitorio, no versionado).
scikit-learn1.9.1, pandas 2.2.3, numpy 2.5.3, scipy 1.18.1, joblib 1.6.0,
threadpoolctl 3.7.0, nbformat 5.10.4, ipykernel 6.30.1, nbclient 0.10.2.
Todas las dependencias resueltas y sus versiones están en requirements.lock.txt;
preparacion.json incluye además Python, ejecutable y pip25.0.1.
Ninguna versión se eligió después de observar desempeño. Semilla20261008, sin búsqueda
de semillas. BLAS/OpenMP se limitaron a un hilo; RF también n_jobs1.

La secuencia realizada fue:

1. Crear venv con Python 3.12.14, instalar paquetes fijados, ejecutar pip check.
2. `comun.prepare()`: comprobar base/diccionario/evidencia/particiones, construir67
   estimadores sin ajustar, exportar parámetros íntegros/defaults, huellas y bloqueo.
3. `generar_notebooks.py`: generar con nbformat y ejecutar02→03→04 en kernel del venv.
   La ejecución de 03 guarda selección y ajusta7 modelos hasta 2022;04 aplica los mismos
   artefactos a ambos años reservados sin entrenamiento adicional.
4. Enriquecer únicamente la discusión Markdown con resultados reales desde fuentes .py;
   regenerar con `--reusar-salidas`, que exige código idéntico y conserva salidas/counts
   del kernel. No reentrena ni modifica JSON a mano. Se valida nbformat nuevamente.
5. `verificar_cierre.py`: cálculos independientes, cobertura, reproducción del ganador en
   sus tres ventanas, aplicación de artefactos a reserva, notebooks e integridad histórica.

Los comandos equivalentes, desde la raíz de una **copia de reproducción** con resultados
anteriores preservados (ver siguiente apartado), usando el ejecutable de su venv son:

```bash
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
/tmp/icfes-fase3-venv/bin/python -c "import sys; sys.path.insert(0,'fase3/fuentes'); from comun import prepare; prepare()"
/tmp/icfes-fase3-venv/bin/python fase3/fuentes/generar_notebooks.py
/tmp/icfes-fase3-venv/bin/python fase3/fuentes/verificar_cierre.py
```

El generador usa rutas relativas al proyecto y kernel explícito del ejecutable que lo
invoca. No instala un kernel global ni exige que python3 del sistema sea el mismo.
Jupyter requiere conexiones locales; dentro del sandbox el primer intento se bloqueó
antes de ajustar. La ejecución autorizada fuera del sandbox sí terminó. No se declara
como demostrada la causa de ese bloqueo.

## Repetir sin sobrescribir el cierre

Después del commit, `fuentes/reproducir.py /tmp/icfes-reproduccion-NUEVA` crea una copia Git
local en una ruta que debe ser inexistente, conserva los resultados/notebooks de este
cierre dentro de `fase3/archivo_cierre/`, prepara un venv nuevo usando exactamente el
bloqueo y ejecuta la misma secuencia. No modifica el repositorio fuente ni usa raw_data.
Puede necesitar permiso de descarga de paquetes y de conexiones locales. El script
registra el commit real de reproducción separado del commit de partida del estudio.
No se ejecutó una segunda búsqueda completa en esta sesión: se verificaron las tres
ventanas del ganador, 99 predicciones, y la reproducción de 462 predicciones de reserva
por carga de los7 artefactos. No se promete identidad binaria joblib entre plataformas;
las predicciones se cotejan con tolerancia de representación1e-12.

## Archivos para inspección

- `resultados/preparacion.json`: base198/huellas/versiones/defaults antes del primer ajuste.
- `resultados/comparacion_desarrollo.csv`: las67 configuraciones completas; métricas de selección.
- `resultados/metricas_ventanas.csv`: 201 filas candidato-ventana.
- `resultados/predicciones_desarrollo.csv`: 6.633 predicciones identificadas (67×99).
- `resultados/congelacion.json`: ganador global y por especificación,132 filas, parámetros,
  transformaciones lineales, huellas y fecha anterior a errores reservados.
- `resultados/modelos/`:7 objetos joblib, incluidos referencias y ganadores por especificación.
- `resultados/predicciones_reevaluacion.csv`:462 filas (7×66), territorio-año/observado/predicción/error.
- `resultados/metricas_reevaluacion.csv`:21 filas (7×3 conjuntos), métricas y diferencias frente a4 referencias.
- `resultados/fallos.json` y `advertencias_desarrollo.json`: vacíos en ejecución actual; no se ocultan fallos.
- `resultados/reevaluacion.json`: huella congelada, ganador inalterado, sin actualización/prueba inédita.
- `resultados/mae_temporal.png`: MAE anual del ganador y referencias, figura descriptiva.
- `resultados/verificacion_notebooks.json`, `verificacion.json`, `manifiesto_cierre.json`: controles y huellas.
- `informe.md`: resultados comparados y límites, con ubicaciones verificables.

Fuentes editables y funciones compartidas en `fuentes/`; notebooks explicativos ejecutados
02/03/04 en `notebooks/`. El notebook01 de fase2 y sus evidencias se conservan intactos.
No hay datos personales ni resultados ficticios incrustados. Los joblib contienen
estimadores de datos agregados y deben cargarse solo en el entorno de versiones fijadas.

## Lectura correcta

Desarrollo selecciona; reserva reevalúa. No se entrenó con 2023 ni se volvió a escoger
por2024. Se reporta explícitamente el caso en que OLS IPM supera a GBR IPM en reserva.
Los resultados actuales no son los rankings históricos de clasificación. La estimación
es contemporánea, ecológica y no causal. El contraste territorial definido por protocolo
queda para fase4 con autorización nueva; escenarios permanecen fuera de alcance.
