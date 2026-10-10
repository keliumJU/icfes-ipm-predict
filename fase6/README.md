# Fase 6: revisión y entrega local

Fecha: 2026-10-09, America/Bogota. Partida real `10ebe23eb2fd1518956391213301439ef718b844`; padre/cierre5 `9becbc3239a540dfa8f31f45c281ac3a61361d19`. Git limpio al inicio. El commit intermedio del usuario, informe raíz y toda entrega previa se conservan. Autorización: solo fase6, sin push ni objetivo4.

## Entrega y trazabilidad

- [Informe revisado 1.1](entrega/informe_objetivo_3_revisado.md): resumen, ocho secciones, diez tablas compactas; preserva cifras a seis decimales, resultados adversos y límites.
- [Anexo técnico independiente](entrega/anexo_tecnico.md): decisiones operativas, controles, versiones y detalle completo con IDs/cifras/ubicaciones. Distingue fase5 histórica del proyecto de revisión6.
- [HTML para copia](entrega/informe_para_copiar.html): títulos/párrafos/tablas semánticos, referencias y enlaces a figuras separadas. Abrir en navegador, copiar contenido renderizado, pegar y revisar estilo en Google Docs. No copiar el código HTML ni presentar la prueba local como pegado real en Docs.
- `entrega/figuras/`: cuatro PNG y cuatro SVG, copias exactas de fase5, disponibles por separado; datos/diseños/pies conservados. Resolución y contenido corresponden a la generación previa.
- `resultados/matriz_trazabilidad.csv`: cada párrafo/pie/fila de tabla del informe raíz y revisado, con archivo/línea/sección y ubicación/procedimiento. Resumen cotejado contra tablas, ninguna afirmación de escenario calculado.
- `resultados/integridad_inicial.json`, `verificacion_numerica.json`, `verificacion_final.json`, `conservacion_final.json`, `presentacion_local.json`, `manifiesto_cierre.json`: controles y huellas. `tablas_cotejo/`: diez CSV de comprobación documental separados de originales.
- `decisiones_previas.md`, `registro_problemas.md`, `referencias_verificadas.md`: diferencias plan/procedimiento previas, hallazgos con evidencia/impacto/alternativa/decisión/control y lecturas efectivas. Plan consultado solo fase6 líneas129–136; PDF nuevos, ninguno.

## Fuentes editables y orden ejecutado

`fuentes/informe_plantilla.md` y `anexo_plantilla.md` son fuentes editables. `generar_entrega.py` produce derivados y copias de figuras; `verificar_revision.py` coteja todas las métricas/tablaturas y narrativa, asociaciones, SVD, coeficientes, réplicas guardadas y conservación. `integridad.py` registra inicio/cierre y excepciones históricas autenticadas mediante Git. `finalizar.py` fija manifiesto, excluyendo su propia huella. No JSON de notebook editado: no hace falta notebook nuevo para esta etapa; los anteriores se conservan.

Ejecutado: lecturas/Git → decisiones previas → integridad inicial → revisión/generación → controles aritméticos/editoriales → correcciones de presentación/regeneración → prueba en navegador → continuidad → verificación final/conservación → manifiesto → commit local. Un control detectó que un derivado no había sido regenerado después de abreviar Tabla1: se regeneró desde fuente, sin modificar cifras, y aprobó. No se ocultó como control aprobado antes de corregirlo. El control del primer commit detectó CRLF en matriz CSV y una línea vacía adicional de Markdown; se corrigió el generador a LF y el fin de fuente, regenerando derivados/manifiesto y actualizando solo el commit propio, sin cambios numéricos.

Entorno reutilizado: `/tmp/icfes-fase3-venv/bin/python`, Python3.12.14, pandas2.2.3, numpy2.5.3; versiones de comprobación en verificacion_numerica.json. La generación usa biblioteca estándar. La verificación reutiliza el control5 en lectura, sustituyendo sus dos funciones de escritura; la función de tablas escribe solo en fase6/resultados/tablas_cotejo. Ningún generador, control de entrenamiento o reproducción de modelos anterior se ejecuta. No instalaciones nuevas, semilla nueva, estimadores cargados, predicciones nuevas, ajustes o remuestreos.

Para regenerar únicamente la entrega documental en una copia del cierre, desde raíz:

```bash
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-fase3-venv/bin/python fase6/fuentes/generar_entrega.py
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-fase3-venv/bin/python fase6/fuentes/verificar_revision.py
PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-fase3-venv/bin/python fase6/fuentes/finalizar.py
```

El entorno transitorio debe restaurarse con versiones registradas si no existe. No ejecutar `integridad.py --inicio` en un commit posterior: el snapshot fija la partida real. El manifiesto no intenta contener el hash del commit que lo incluye; el cierre se identifica en Git por asunto `fase 6: revisar y entregar informe con anexo y conservacion verificada`.

## Comprobación de presentación y límites de cierre

HTML abierto en navegador local: diez tablas, máximo seis columnas, un título principal y nueve títulos de sección incluido resumen; sin desborde horizontal de página o tablas en ancho910px. Inspección visual de portada/resumen, tablas4–5, remuestreo/robustez/asociaciones. Figuras entregadas separadamente, cotejadas byte a byte con fase5 y comprobadas contra datos/ejes por el control heredado. No nueva lectura de PDF ni simulación. La prueba no acredita pegado real en Google Docs, documento que no fue enlazado o modificado.

El servidor temporal solo escuchó en127.0.0.1 y se detuvo después de probar. Su primer inicio en sandbox fue rechazado por permisos de socket; la misma operación local se autorizó fuera del sandbox. No transmite datos a un servicio remoto. La escritura del commit local puede requerir permiso técnico porque .git está protegido.

No quedan controles indispensables activos de revisión local. Persisten límites metodológicos e históricos documentados, causa2024 desconocida, persistencia no evaluada y aceptación editorial del grupo pendiente externa. El ganador global y la reevaluación permanecen cerrados. Cualquier avance requiere autorización nueva y diseño prospectivo; esta entrega no ejecuta el objetivo4.
