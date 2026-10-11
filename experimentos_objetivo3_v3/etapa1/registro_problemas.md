# Hallazgos y decisiones — etapa1 v3

Todos preceden cualquier resultado predictivo real v3. No quedan controles indispensables
pendientes. Evidencia estructural: resultados/estructura_real.json; sintética:
resultados/sinteticos/controles.json y notebook_sinteticos/controles.json.

- **Partida documental posterior a v2.** Git9df055a añade cuatro documentos, sin etapa
  ejecutada. Impacto: evitar atribuir una ejecución al plan. Alternativa: conservarlos
  y comenzar desde HEAD real. Resuelto con rama nueva y snapshot en partida.json.
  Git inicialmente limpio; snapshot se tomó después de crear fuentes propias no
  versionadas, por eso registra `?? .../etapa1/`, no trabajo encontrado ajeno.
- **.git de solo lectura en aislamiento.** Intento inicial de crear rama rechazado.
  Impacto: no se podía satisfacer rama/commit local. Alternativa: aprobación de acceso
  Git requerido por aislamiento; rama creada desde9df055a tras aprobación, sin reset
  ni sobrescritura. No afecta artefactos ni diseño.
- **2018 no tiene objetivo;2021 no tiene interna de modelos.** Impacto: v2 no puede
  copiarse como motor intacto. Alternativa: adapter para cambio, entrenar desde2019,
  persistencia fija2021 sin métricas de candidatos. Resuelto en comun_v3.py y controles.
  Prueba sintética2019→2021=13 puntos, sin dividir por dos, y aislamiento entre territorios.
- **Cota distinta de v2.** Impacto: no trasladar1555 ni diez repeticiones. Alternativa:
  enumerar grilla/ventanas/roles sin suprimir global/especificaciones. Resuelto:990
  internos+≤16 externos+≤4 repeticiones ajustadas=≤1010 sin fallos. Comparadores guardados
  y persistencia sin fit. E3-01 regex completa/E3-021555 siguen antecedentes v2.
- **Entorno transitorio existente.** Impacto: no asumir persistencia en próxima sesión.
  Alternativa: comprobar versiones y todos los paquetes del lock y pip check sin
  instalación. Resuelto; entorno.json. Advertencia de caché pip sin escritura no
  afecta pip check; no instalación, caché ni descarga realizadas.
- **Métricas del cambio serían otro estimando.** Impacto: R² del cambio constante puede
  no estar definido aunque el global varíe. Alternativa: reconstruir y calcular métricas
  en puntos originales. Resuelto con prueba sintética en tres especificaciones,
  recálculo independiente math.fsum y ningún error/MAE real calculado.
- **Continuidades históricas cambian por sesiones posteriores.** Impacto: cotejo directo
  contra manifiestos viejos fallaría. Alternativa verificable: usar sus commits de cierre
  exclusivos para esa ruta. Resuelto en preparar.py con0664ac/b37a2f/cc21529;
  todos los demás archivos cotejados actuales, sin excepciones inventadas.

Advertencias activas y antecedentes archivados conservados en PROTOCOLO_V3.md §6 y
CONTINUIDAD_V3.md. No nueva evidencia que reabra59/esquema82,20212 ni fórmula global.
No se revisaron PDFs (cero páginas); citas históricas siguen siendo antecedentes.
