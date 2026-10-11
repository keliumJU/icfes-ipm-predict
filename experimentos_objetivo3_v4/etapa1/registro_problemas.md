# Hallazgos — etapa1 v4

Cada resolución mantiene el objetivo y los criterios del usuario; no resultados v4.

|Hallazgo y ubicación|Impacto|Alternativa verificable y resolución|
|---|---|---|
|HEAD documental46193a5/Git; REGISTRO_PREPARACION.json|Partida ya incluye documentos sin ejecución|Conservarlos, cotejar snapshot15349/tres huellas/registro en Git y crear rama desdeHEAD; resuelto|
|Entorno transitorio; resultados/entorno.json|No asumir Python/Huber disponible|Verificar54 versiones y pip check; aprobado, ninguna instalación|
|.git solo lectura; intento git switch rechazado|Rama local requerida no se podía crear|Acceso Git escalado autorizado por herramienta; rama creada sin reset|
|Git cita nombres con acentos; preparar.py primer intento falló al leer ruta citada|Snapshot inicial no podía completarse|Enumerar git ls-files -z y decodificar nombres completos; corregido antes de estructura/diagnóstico|
|Lectura inicial del plan incluyó texto posterior a§3|Incumplimiento del límite de lectura, sin ampliar autorización|Registrar el incidente y limitar protocolo a§§1–3; ninguna fase posterior ejecutada|
|Persistencia ganó v3; referencias_guardadas.json/selecciones históricas|No prueba aporte incremental de modelos/IPM|Diagnóstico explícito y29hipótesis del usuario, sin ajuste real ni cambiar grilla; resuelto en protocolo|
|2022/sesgo; metricas_historicas.csv|Beneficio conjunto no uniforme y dirección del error variable|Conservar todos errores/cortes/deterioros, describir identidad pred−observado sin causalidad; resuelto en informe|
|Cinco territorios y66 pares deterioran frentev2; deterioros CSV|No permite afirmar beneficio uniforme|Tablas completas sin exclusiones ni corrección retrospectiva; resuelto|
|Covariables previas/2019→2021; trazabilidad_198.csv|Diferencias deben compartir llave del puntaje y no ser anuales|Cotejo198 filas/16covariables con fuente y controles sintéticos; aprobado|
|Global puede diferir del ganador de su grupo; controles.py|Deduplicación por grupo perdería roles|Caso sintético global y grupo distintos/seis IDs, deduplicar solo ID; aprobado|
|Fallos numéricos deben conservar inelegibilidad al reanudar; comun_v4.py|Un reintento podría rescatar candidato indebidamente|Clase de fallo persistente en ledger sintético, prueba reanudada; aprobado|
|Cota308; configuraciones_congeladas.json|No heredar100 candidatos/1010v3/1555v2|Cálculo28×10+6×4+4, tope futuro7200 prevalece; resuelto|

Advertencia pip: caché de usuario no escribible, pip check aprobado; no instalación/red
ni caché escrita. Lecturas actuales: AGENTS, continuidades vigentesv2/v3/v4, protocolo
completov3/README/informe/controles/congelación/manifiesto/conservación y CSV/selecciones
históricas; PDFs ninguno. Los modelos no se cargaron; solo se comprobaron sus huellas.
Antecedentes históricos archivados y advertencias activas: PROTOCOLO_V4.md sección límites;
no nueva conexión pertinente, no reapertura. No contradicción material irresoluble.

Incidencias adicionales resueltas antes de congelación final:

- Importaciones heredadas anteponían carpetas v3/v2; el hijo spawn del notebook no
  encontraba la nueva clase NoConverge y devolvió EOFError. Impacto: control de
  convergencia notebook incompleto. Alternativa: restaurar prioridad de fuentesv4 en
  comun_v4 y clasificar EOF como infraestructura. Resuelto mediante reejecución completa
  de controles y notebook. Carpetas de prueba fallidas conservadas separadas; no fits reales.
- Primer cierre descartó espacio inicial de git status mediante strip y rechazó ruta
  v4 válida. Impacto: cierre detenido, aún sin congelación válida. Alternativa: leer
  salida de estado sin strip; corregido. No excepciones para rutas exteriores.
- Control anti-evidencia obsoleta: fuentes_sha256 en controles y cotejo fuente/notebook
  en cierre. Resolución: ninguna salida anterior se acepta tras modificar fuentes.
