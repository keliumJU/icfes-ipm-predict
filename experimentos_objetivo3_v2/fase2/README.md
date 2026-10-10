# Fase 2 v2 — protocolo, funciones y verificación

Solo fase2. Leer PROTOCOLO_V2.md y registro_problemas.md. Evidencia ejecutada:
INFORME_CIERRE.md, resultados/controles.json y verificacion_notebook.json.
No candidatos ajustados ni predicciones sobre datos reales. Los CSV nuevos de predicción
contienen únicamente tres ejemplos sintéticos, etiquetados con ID `doble`.

## Orden y fuentes editables

1. configuracion.py: panel/rutas, entradas, años, grillas, semilla, ventanas y constructor común.
2. comun.py: normalización de códigos, panel/union/agregación, separación, métricas,
   predicciones guardadas, selector, umbral y presupuesto persistente/interrumpible.
3. 01_protocolo_verificacion.py: fuente de celdas, rutas relativas a la carpeta de trabajo.
4. generar_notebook.py --solo-generar: nbformat y compilación de celdas, sin ejecución.
5. congelar.py: 100 configuraciones/defaults completos y referencia v1, versiones,
   fuentes operativas y protocolo; sin fit/predict. Solo preparación antes del piloto.
6. verificar.py: nueve controles y cotejo de manifiestos; integra pruebas sintéticas/dobles.
7. generar_notebook.py: kernel real del mismo ejecutable, solo modo verificación;
   valida notebook y guarda evidencia. No crea/ejecuta notebooks de modelos.
8. cerrar.py: conservación de snapshot, informe factual, manifiesto. Es cierre antes del
   commit de esta fase; su guardia HEAD impide atribuir otra partida por accidente.

Entorno compatible efectivo: /tmp/icfes-v2-fase2-venv/bin/python,
Python3.12.14/sklearn1.9.1, reconstruido con paquetes exactos de caché local v1
(sin red). Entorno temporal no versionado; no afirmar que existirá en sesión futura.
requirements.lock.txt registra versiones resueltas, resultados/entorno.json incluye
pip check y procedencia. Copia de paquetes local recuperada en
/tmp/icfes-v2-wheels-compatible; instalar offline con `pip install --no-index
--find-links /tmp/icfes-v2-wheels-compatible -r requirements.lock.txt` en un entorno
compatible si esa caché todavía existe. No descargar datos ni sustituir versiones por métricas.

Comandos ejecutados desde raíz del repositorio (PYTHONDONTWRITEBYTECODE=1):

```text
/tmp/icfes-v2-fase2-venv/bin/python experimentos_objetivo3_v2/fase2/fuentes/generar_notebook.py --solo-generar
/tmp/icfes-v2-fase2-venv/bin/python experimentos_objetivo3_v2/fase2/fuentes/congelar.py
/tmp/icfes-v2-fase2-venv/bin/python experimentos_objetivo3_v2/fase2/fuentes/verificar.py
/tmp/icfes-v2-fase2-venv/bin/python experimentos_objetivo3_v2/fase2/fuentes/generar_notebook.py
/tmp/icfes-v2-fase2-venv/bin/python experimentos_objetivo3_v2/fase2/fuentes/cerrar.py
```

La enmienda explícita de semilla usó `congelar.py --enmienda-semilla` después de archivar
la versión anterior; no usar ese indicador para modificar criterios sin decisión previa.
El kernel Jupyter requirió conexiones locales fuera del aislamiento, autorizadas; su
fuente comprueba esa capacidad antes de iniciar para evitar otra espera bloqueada.
El notebook parte de su propia carpeta o de fase2/raíz, sin rutas absolutas incrustadas.
Incluye outputs mínimos de una ejecución real; no datos individuales ni métricas reales.

## Repetición y conservación

Los scripts escriben evidencia nueva dentro de fase2, incluidos tiempos variables de
pruebas. Para reproducir después del cierre, usar copia separada de repositorio/entradas
conservando jerarquía, congelación y fuentes, y comparar resultados de control; no
sobrescribir este cierre para fingir huellas iguales. La validación de manifiesto lee
archivos y compara SHA256 sin regenerarlos. Las incidencias y primeras congelaciones
son antecedentes locales de esta fase, no entregables históricos modificados.
El manifiesto final incluye notebook ejecutado, lock, código, informes y continuidad v2;
excluye su propio archivo para evitar autorreferencia. Commit informado al usuario,
sin guardar su hash en un archivo que pertenezca al mismo commit.

Pendiente: únicamente autorización de fase3 y su orquestación/ejecución sobre estas
funciones y reglas; hasta entonces no entrenar ni generar predicciones reales. Dos
horas acumuladas incluyen referencias y repeticiones. Informe completo incluso sin
mejora; notebook personal solo con regla del5% satisfecha, sin tres-de-cinco-años.
