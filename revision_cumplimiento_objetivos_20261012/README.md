# Revisión documental de cumplimiento de tesis

12/10/2026. Empezar por REVISION_CUATRO_OBJETIVOS.md. CIERRE_RAMA_HISTORICA.md conserva la decisión humana de detener la investigación de versiones sin certificar pendientes. CONTINUIDAD.md registra estado y preguntas pendientes del objetivo3. LECTURAS_Y_LIMITES.md distingue nueva lectura, evidencia anterior y contenido no revisado.

No se modificaron tesis, investigaciones o resultados anteriores. No se ejecutaron modelos, escenarios ni cálculos analíticos nuevos. No se generan notebooks porque esta revisión no los necesita. La nueva carpeta separada evita cambiar el inventario interno de la investigación cerrada.

Fuente editable `fuentes/control.py`, anterior al inventario de conservación. Orden: aprobación en lectura de investigación anterior antes de ampliar; control.py inicio; revisión documental y textos; control.py cierre. PARTIDA.json registra estado externo previo; MANIFIESTO.json registra entrega y VERIFICACION.json el cierre. Exclusiones heredadas explícitas, sin afirmar certificación de destinos de enlaces/.git/runtime/cache. Verificar en lectura: `python3 -B fuentes/control.py verificar` desde esta carpeta. No volver a ejecutar inicio/cierre sobre entrega congelada.

La conservación verifica bytes e inventario, no certifica cumplimiento académico o disponibilidad histórica. Versiones comprobadas: Python del sistema 3.14.7, funciones estándar sin aleatoriedad ni semillas; pdftotext/Poppler 26.08.0 para extracción de páginas a /tmp. Las versiones y parámetros de modelos anteriores se encuentran en sus entregas respectivas, sin reconstruir ni modificar su entorno.
