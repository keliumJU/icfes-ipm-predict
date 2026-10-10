# Fase 5: informe para la tesis

Partida `da48e1a4f85d206e8753fbad85b78ba2e3858b1a`, Git limpio. Fecha2026-10-09, America/Bogota. Únicamente documentación de resultados existentes, sin entrenamiento, reselección, referencias nuevas, bootstrap nuevo, simulaciones o push. Referencia operativa: protocolo v1.0 y cierres fases3–4. Diferencias plan/procedimiento: decisiones_previas.md, escrito antes de redactar. Lecturas del plan: exclusivamente fase5 líneas110–128. No lecturas PDF nuevas; registro en referencias_verificadas.md.

## Entregables y entradas

- `../informe_objetivo_3.md`: ocho secciones académicas, diez tablas y cuatro figuras, referencias y ubicaciones empíricas.
- `fuentes/informe_plantilla.md`: narrativa editable; `documentar.py`: funciones compartidas de lectura, métricas de comprobación, tablas y figuras; entradas: base198 y CSV existentes de fases3–4. No carga joblib ni importa funciones de ajuste.
- `resultados/tabla_*.csv`: diez tablas derivadas. `generacion.json`: huellas de entradas, versiones, contextos y91 filas de métricas cotejadas (67 selección+21 temporal+3 territorial).
- `figuras/01_particion_temporal`, `02_observado_predicho`, `03_errores_territoriales`, `04_estabilidad_interpretativa`: cada una en PNG y SVG. Figuras nuevas derivadas exclusivamente de fuentes existentes.
- `fuentes/07_informe_tesis.py` y `generar_notebook.py` → `notebooks/07_informe_tesis.ipynb`, bajo fase5 para preservar notebooks congelados. Dos celdas de código ejecutadas con Python secuencial compile/exec, salidas reales, validación nbformat. No afirmar ejecución en kernel Jupyter. No notebook de modelos o simulación.
- `resultados/integridad_inicial.json`, `conservacion_final.json`, `verificacion_notebook.json`, `verificacion_informe.json`, `manifiesto_cierre.json`: evidencia de controles y conservación. No incluyen microdatos personales.

## Orden, entorno y reproducción documental

Entorno disponible `/tmp/icfes-fase3-venv/bin/python` (transitorio), Python3.12.14, pandas2.2.3, numpy2.5.3, matplotlib3.10.7 y nbformat5.10.4. Versiones de documentación registradas en generacion.json; bloqueo del entorno preexistente en fase3/requirements.lock.txt. No se instalan paquetes ni se invoca sklearn para documentar. Cálculos deterministas; no aplica semilla nueva. Semilla20261008 del ajuste/remuestreo previo se cita como previa.

Secuencia efectivamente realizada desde raíz: comprobar Git/lecturas; `verificar_integridad.py --inicio`; guardar decisiones previas; generar informe/tablas/figuras; inspeccionar cuatro imágenes y corregir pie/leyenda y título para distinguir configuración de artefacto congelado; generar/validar/ejecutar notebook; `verificar_informe.py`; actualizar continuidad; repetir comprobación tras cambios documentales finales; `finalizar.py`; commit local.

Para reproducir documentación, sin ajustes, desde raíz de una copia nueva del cierre:

```bash
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-fase3-venv/bin/python fase5/fuentes/generar_notebook.py
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-fase3-venv/bin/python fase5/fuentes/verificar_informe.py
```

La generación sobrescribe solo informe y derivados fase5 dentro de esa copia; preserva fuentes anteriores. No volver a ejecutar `--inicio` en un cierre nuevo: exige commit de partida y continuidad exactos de cierre4, y podría sustituir snapshot original. `finalizar.py` verifica y fija manifiesto; no incluye su propio manifiesto ni hash de commit autocontenido. Git identifica el commit de cierre.

## Alcance del control

Se recalculan errores/métricas con predicciones existentes, sin aplicar modelos de nuevo. Se comprueban cifras narrativas desfavorables, cobertura de secciones/tablas/figuras, referencias locales de imágenes, formato/ejecución del notebook, límites de ejes y huellas. Revisión visual realizada de las cuatro figuras; pie temporal y leyendas corregidos antes de cierre. No hay atribuciones causales ni referencias históricas inventadas. Las huellas antiguas de continuidad de fases2–3 se identifican como sustituidas documentadamente; continuidad vigente coincide con cierre4 antes de editarla. Base, protocolo, modelos y demás entregables coinciden sin excepciones. Snapshot inicial de todos los archivos versionados permite verificar conservación final, con única excepción intencional de continuidad.

Pendientes: revisión editorial/adopción del grupo, ajena a la validación local; sin controles indispensables activos de fase5. Persistencia no evaluada es límite explícito, no tarea autorizada para completar aquí. Fases posteriores requieren autorización nueva y decisiones prospectivas. No push.
