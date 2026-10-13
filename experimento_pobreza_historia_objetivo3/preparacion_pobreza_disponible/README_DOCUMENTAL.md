# Entrega documental de disponibilidad

Entrada principal: `INFORME_FACTIBILIDAD.md`. Propuesta sin ejecución: `PROPUESTA_PROTOCOLO.md`. Calendario por cada fuente/año/aplicación: `CALENDARIO.csv`. Cortes: `CORTES_PROPUESTOS.csv`. Procedencia: `REGISTRO_PROCEDENCIA_REVISIONES.md`. Hallazgos/alternativas: `HALLAZGOS_Y_PENDIENTES.md`.

Referencias con URL/consulta/ubicación: `REFERENCIAS.json` y `EXTRACTOS_DOCUMENTALES.md`. Lecturas parciales y páginas pendientes: `LECTURAS.json`. Documentos oficiales consultados preservados en `evidencia_oficial/`, sin datos raw nuevos. El contenido numérico incidental de PDFs no se extrae a ningún análisis.

Estado inicial: siete archivos de prompt guardado preservados íntegros en `antecedentes_prompt_guardado/`; 38.962 huellas previas en `PARTIDA_DOCUMENTAL.json` (inventario con exclusiones explícitas). Solo la continuidad propia se actualiza con copia previa; manifiestos/verificadores históricos no se adaptan. `MANIFIESTO.json`, `VERIFICACION.json`, `PARTIDA.json` y `verificar_preparacion.py` originales son del cierre del prompt, no de esta ampliación. El verificador histórico se aprobó antes de escribir, y después del crecimiento no se vuelve a presentar como verificador vigente del inventario ampliado.

Fuentes editables, sin librerías científicas ni cambios de runtime:

1. `python -B fuentes/documental.py`: huellas/metadatos; no lectura de registros.
2. `python -B fuentes/generar_calendario.py`: fechas y fuentes por AST; no evaluación, no panel analítico.
3. `python -B fuentes/registrar_lecturas.py`: archiva los documentos ya descargados en /tmp y extractos breves, declara páginas leídas y pendientes. Para consultar otras páginas explícitamente: `fuentes/leer_paginas.py /tmp/documento.pdf <páginas>`.
4. `python -B fuentes/cerrar_documental.py`: manifiesto de esta entrega y verificación actual, únicamente mientras se prepara este cierre. No inicia fases posteriores.
5. **Verificación posterior solo de lectura:** `python -B verificar_documental.py`. No necesita /tmp, red, pip, notebooks ni deserialización de modelos.

Estos pasos documentales 1–4 ya se realizaron en la sesión, con resultados registrados. Ninguno ejecuta modelos. No hace falta notebook; si otra fase lo necesitara, debe partir de .py y generador Python, con nueva autorización. Semillas no aplican: no hay aleatoriedad. Versiones de Python/Poppler y fecha de ejecución constan en cierre/lecturas. Las salidas verificables permanecen en esta carpeta; temporales solo /tmp. No ejecutar cierres históricos con excepciones nuevas.

El cierre documental es incompleto por procedencia y disponibilidad indispensables, aunque su inventario pase integridad. Ningún avance automático, ningún presupuesto heredado, ninguna causalidad.

Alcance exacto de conservación: archivos regulares sin enlaces simbólicos, como los seleccionó el inventario inicial. No se guardaron huellas iniciales de destinos de enlaces; por tanto no se certifica retrospectivamente su conservación. Se guardó una observación posterior de enlaces en `antecedentes_verificacion/enlaces_observados_en_cierre.json`, identificada expresamente como posterior. El primer cierre rechazó un symlink de una prueba antigua fuera de esta entrega; su dictamen se preservó en `antecedentes_verificacion/primer_rechazo.json`. Se alineó el verificador nuevo con el universo inicial, sin modificar el snapshot ni admitir symlinks en esta entrega. No se cambió un verificador histórico ni se reabrió ese experimento.
