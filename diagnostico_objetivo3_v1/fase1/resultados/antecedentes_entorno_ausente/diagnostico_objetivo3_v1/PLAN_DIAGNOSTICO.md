# Plan del diagnóstico objetivo3 v1 — preparación documental

Versión documental1.0. Fecha2026-10-11, America/Bogota.
Estado: SOLO preparación documental; diagnóstico NO iniciado.
La existencia de este plan y su prompt no autoriza ejecución. Esta entrega crea
únicamente cuatro documentos en diagnostico_objetivo3_v1; sin commits ni cambios previos.

## 1. Objetivo, acuerdos y punto de partida

Usuario: diagnosticar estabilidad temporal y capacidad informativa de las entradas
para fundamentar un posible nuevo punto de partida. Elección expresa: SOLO datos
y predicciones guardados, SIN nuevos ajustes. No prometer mejora ni una explicación
causal definitiva. Es una investigación separada, no etapa3v5 ni excepción a su
meta incumplida. Un nuevo experimento requiere protocolo y autorización separados.

Cierre histórico v5 comprobado en Git75c3a25182af363f47b0d743820f99084e18fed5,
asunto `etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora`; rama actual
codex/objetivo3-v5-mae, Git limpio al preparar, carpeta diagnóstico inexistente.
Resultados históricos guardados: mejora exacta0.0%, MAEglobal=referencia
3.429267191379531,350ajustes internos,11880filas internas,1155externas; global y
cinco grupos seleccionan persistencia en2021–2025. Ubicaciones: v5/etapa2/resultados/
meta.json,verificacion.json,piloto/seleccion_2021.json..seleccion_2025.json.
Comprobación actual de preparación: documentos/selecciones/huellas/manifiesto en
lectura, no recálculo de métricas ni reproducción de modelos.

Las observaciones conversacionales sobre caída2019/cambios posteriores y posibles
relaciones inestables son HIPÓTESIS por comprobar en el diagnóstico. No registrar
como causa establecida el cambio temporal, la redundancia o la ausencia de señal.

Conservar decisiones vigentes: ESTUDIANTE,no libertadS,grado11,seis puntajes presentes
positivos,sin filtro de calendario; media global recibida sin recalcular/redondear,
geografía colegio,peso igual territorio-año,conteos solo trazabilidad.2020excluido;
2018historial; previo máximo año anterior mismo territorio,2021previo2019; diferencias
sin anualizar/sin fabricar2020. Objetivo cambio observado en puntos originales.
No filtrar años/territorios/variables según resultados. No modificar criterio≥5%
ni selecciones v5, ni heredar su saldo para nuevos trabajos.

## 2. Entradas, trazabilidad y preflight de la futura sesión

Raíz /home/kelium/Documents/espcarlos/icfes-predict-improved.
Fuente única autorizada: experimentos_objetivo3_v2/fase1/reconstrucciones/
base_analitica_departamento_anio_v2.csv, SHA256
6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3.
Derivado propio congelado: experimentos_objetivo3_v5/etapa1/reconstrucciones/
panel_cambios.csv, SHA256aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc.
Cotejo histórico v4 de mismo SHA solo lectura. Estructura esperada231filas,33territorios,
198cambios2019/2021–2025. No raw ni fuentes adicionales.

Contratos: v5/etapa1/PROTOCOLO_V5.md y resultados/configuraciones_congeladas.json,
requirements.lock.txt y entorno.json. Entradas únicamente unión exacta de cinco
GRUPOS congelados, manteniendo orden de primera aparición; no agregar año/código/
conteos/otros puntajes como entradas. Año/código/intervalo solo llaves y descripción.

Predicciones y contexto: v5/etapa2/resultados/predicciones_internas.csv,
metricas_internas.csv,predicciones_externas.csv,metricas.csv,ganadores.csv,meta.json,
verificacion.json,auditoria_complementaria.json; piloto/seleccion_*.json,
contexto.json,indice_integridad.json,ledger.json,reproducibilidad.json y metadatos
JSON de ajustes. Fuentes/defaults/modelos propios se cotejan por hash, sin deserializar
modelos. Referencias históricas ya autorizadas se consultan solo si necesarias para
cotejar persistencia/v3; sin nuevas búsquedas, ajustes ni modelos cargados.

Antes de calcular: leer AGENTS y continuidad propia primero, secciones vigentes de
continuidades v2–v5; de ESTE plan §§1–5, sin planes de entrenamiento posteriores.
Comprobar cierre real/asunto/ascendencia/HEAD/rama y trabajo posterior, registro de
preparación/huellas y manifiestos. Esperar cuatro documentos propios sin commit;
no confundirlos con trabajo ajeno ni exigir artificialmente Git limpio. Reusar rama
actual sin reset ni cambio de rama. Documentar cualquier diferencia posterior;
no sobrescribir trabajo ajeno. Continuidades históricas se verifican en sus commits
reales cuando corresponda, sin excepciones para otras rutas.

Comprobar Python3.12.14/sklearn1.9.1/54paquetes exactos de lockv4/etapa1/pip check
antes de usar /tmp/icfes-v2-fase2-venv/bin/python. Si falta/difiere, documentar y
consultar, sin instalar ni descargar. PYTHONDONTWRITEBYTECODE=1 y semilla20261010
solo para controles inventados que requieran aleatoriedad. No afirmar disponibilidad
actual del entorno: esta preparación NO lo revalida.

Revalidar fuente/derivado en memoria por misma llave/campos/orden/valores, anterioridad,
intervalos y reconstrucción observada; sin llamar preparaciones/cierres/pilotos viejos
que escriban. Verificar artefactos e índice histórico sin regenerarlos. Fallo de
integridad/cobertura/inconsistencia no explicada: conservar diagnóstico incompleto,
detener cálculo dependiente y resolver dentro alcance o consultar contradicción material.

## 3. Procedimientos del diagnóstico — sin nuevos fits

### 3.1 Estabilidad temporal

Usar los198cambios completos,33por cada2019/2021–2025;2018solo historial, no imputar
su cambio ausente. Describir globalmente y por año: n,media,mediana,mínimo,máximo,
cuantiles0.10/0.25/0.75/0.90,desviación estándar muestral(ddof1),IQR y proporciones
negativa/cero/positiva por comparación exacta con0. Cuantiles con interpolación
lineal, sin redondear CSV. Por territorio: trayectoria completa de cambio e intervalo,
resumen de distribución y transiciones de signo, con cero como categoría propia.

Para cada partición interna original, comparar distribuciones de entrenamiento y
validación (mediana,IQR,signos) de objetivo y entradas; describir desplazamientos sin
inventar umbrales de ruptura ni pruebas de significancia. Distinción explícita:
2021respecto2019 es intervalo2; los otros intervalos son1. No anualizar, eliminar2019
ni tratar el salto como efecto causal. Gráficos: distribuciones anuales, trayectorias
territoriales y contraste entrenamiento-validación.

### 3.2 Variación, redundancia y asociaciones

Para la unión de entradas congeladas, describir por año y global: n,no finitos,
valores únicos,rango,IQR,desviación estándar y constantes exactas. Los198cambios
requieren entradas completas; no eliminar filas por omisión ni imputar. Calcular
Pearson y Spearman con cambio_observado por año (n33) y global (n198), y entre cada
par de entradas globalmente y por año. Spearman usa rangos medios para empates.
No sumar asociaciones globales y anuales como evidencias independientes.

Si columna constante o n insuficiente, resultado vacío con razón/n explícitos,
no correlación0 ni significancia. Mostrar el patrón por año y discrepancias entre
asociación agregada y anual; no interpretar diferencias territoriales de niveles
como capacidad para anticipar cambios. No introducir selección automática de
variables ni umbrales de correlación que decidan futuras grillas. Importancias de
modelos no se calculan ni se usan como prueba de ausencia de información.

### 3.3 Errores de predicciones históricas

Desde CSV, calcular observado−puntaje_previo como cambio observado; error=predicción−
observado, MAE con math.fsum(|error|)/n, RMSE=sqrt(fsum(error²)/n),sesgo=fsum(error)/n.
Predicción global debe igualar previo+cambio_predicho con valores exactos round_trip.
Comparador pareado=persistencia del mismo territorio/año. Guardar delta_error_absoluto
=|error_modelo|−|error_persistencia|,delta_error_cuadratico y error de cambio predicho,
proporción de dirección acertada (signo exacto −/0/+), |cambio_predicho| frente
|cambio_observado|; magnitud no sustituye precisión global.

Reportar n/métricas por candidato,familia,grupo,validación y ventana externa original;
por territorio con n explícito. Candidato persistencia no pertenece a grupo ajustado,
participa como comparador de todos. Recalcular los144registros internos y contrastar
con guardados; comparación aritmética de métricas internas atol1e-12/rtol0 por
acumulador histórico distinto, jamás tolerancia en valores/llaves de CSV. Mantener
selecciones originales; mínimos por familia/grupo son descripción retrospectiva,
no nuevos ganadores ni mejora confirmada. Externas: siete procedimientos guardados,
1155filas,165cadauno, solo seleccionados; no generar externas faltantes de35modelos.

### 3.4 Evidencia repetida entre ventanas

Auditar y conservar completas las11880filas internas con llave original
(externo,id,anio,codigo_departamento) única. Diez particiones acumuladas contienen
solo cuatro años de validación distintos (2021–2024); no diez años independientes.
Para síntesis sin repetición, agrupar (id,anio,codigo_departamento). Antes de colapsar,
exigir igualdad exacta de llaves,observado,previo,año_previo,cambio_predicho y predicción,
y equivalencia de entrenamiento/configuración/entradas/versiones/semilla en metadatos.
Solo etiqueta de ajuste/ventana puede variar por diseño. Conservar tabla de linaje de
cada copia y usar como representante el menor externo. Si coinciden todos los casos,
esperar4752filas únicas=36×4×33; esto es control esperado, NO resultado ya obtenido.
Si hay discrepancia, no escoger copia conveniente ni promediar: investigar/detener
síntesis dependiente y registrar evidencia. No deduplicar el análisis original por
ventana ni alterar sus métricas; mantener ambas tablas con propósito explícito.

### 3.5 Matriz de hallazgos y punto de partida posible

Cada hallazgo: ID,archivo/tabla/llave o procedimiento verificable,n,resultado,
impacto sobre mejora,hipótesis relacionada,evidencia a favor/en contra,explicación
alternativa,resolución y pendiente. Clasificar hipótesis en apoyada descriptivamente,
contradicha o insuficientemente evaluada, justificando sin puntuaciones inventadas.

Examinar candidatos de explicación: cambio temporal de distribución/relaciones;
redundancia/poca variación; predicciones de dirección/magnitud inadecuadas; insuficiencia
de historia/información adicional. Priorizar recencia si patrón temporal repetido
apoya estudiarla; simplificación si redundancia/variación justifica probarla; más
historia si evidencia temporal insuficiente; conservar persistencia si no se observa
ventaja reproducible. Correlación o error de modelo malo no demuestran inutilidad
intrínseca de entradas. Admitir empates y ninguna alternativa suficientemente
justificada. No forzar diagnóstico único ni prometer alcanzar5%.

Para cada alternativa propuesta: evidencia justificativa,incertidumbre,qué prueba
futura la distinguiría y qué cambio material requeriría autorización. No fijar
hiperparámetros,eliminar años,crear grilla,seleccionar un modelo final ni ejecutar
experimento posterior. 2021–2025examinados: todo este diagnóstico es exploratorio,
no confirmación independiente ni causalidad/pronóstico anticipado demostrado.

## 4. Controles, implementación y entregables futuros

Toda escritura futura exclusivamente diagnostico_objetivo3_v1/ y continuidad propia.
Implementar fuentes editables propias y lógica compartida reutilizable, destinos
restringidos también frente symlinks; funciones previas solo lectura sin invocar
runners/preflights/cierres/controles que escriban precedentes. Datos completos en
código/bloques; resúmenes pequeños al chat. No datos personales.

Pruebas inventadas: int/float0 exactos aceptados;1e-11/llaves/campos/orden distintos
rechazados; duplicados/omisiones/no finitos rechazados; rangos/empates/constantes y
correlaciones indefinidas; intervalos1/2 preservados; signo0/deltas/métricas por
aritmética independiente; repetición idéntica colapsada con linaje y discrepante
rechazada; orden y cobertura de candidaturas/ventanas; rutas prohibidas/symlinks.
No fits ni deserialización joblib/pickle en controles o celdas; revisión de imports
para impedir ejecución accidental de entrenamiento. No generar datos/predicciones
que simulen resultados reales pendientes.

Entregables futuros fase1/: README,PROTOCOLO_DIAGNOSTICO,informe,registro de hallazgos,
fuentesPython reutilizables y generador; tablas de estabilidad/variación/asociaciones/
errores internos originales y únicos/externos/linaje/matriz de hipótesis; gráficos
PNG con unidad y n. Resultados/preflight,lecturas,entorno,pruebas,auditoría,conservación,
manifiesto y verificación de notebook. Continuidad propia actualizar con antecedente
íntegro; no modificar v5. Nombres finales de tablas deben constar en README/protocolo.

Notebook útil de diagnóstico, no personal: fuenteeditablePython/generadorPython,
nbformat validado y celdas pertinentes realmente ejecutadas solo sobre guardados;
salidas exclusivamente realizadas, versiones/entradas/semilla si procede. Sin kernel
si ejecución Pythonexec suficiente, con método declarado; cero nuevos ajustes.

Aceptación: fuentes/manifiestos/huellas íntegros,33territorios/198cambios,11880internas
originales/144registros/36IDs/1155externas/7×165; identidad exacta y ausencia de
pseudo-repetición; cifras auditadas independientes; asociaciones indefinidas declaradas;
informe equilibrado/hipótesis clasificadas/pendientes explícitos; notebook ejecutado;
conservación/manifiesto/continuidad verificados. Cierre diagnóstico aun cuando no
justifique alternativa; diagnóstico incompleto si control indispensable irresuelto.
No commits sin nueva instrucción expresa, no push ni avance automático.

## 5. Límites, lecturas y preparación actual

Prohibidos nuevosfits/búsquedas/carga de modelos históricos/ganador externo
retrospectivo/filtros para conseguir métricas/nuevasfuentes/instalaciones/descargas/
simulación/objetivo4/notebookpersonal/entrenamientofinal. No usar remanentes7200s.
Conservar casos completos/Guainía238vs404/21.012106puntos (evidencia histórica
v2/fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local sin
autenticación independiente, comparabilidadIPM/hogares-alumnos/colegio-residencia/
enlace ecológico/dependencia temporal-territorial/pocos años. Antecedentes archivados
no reabrir sin nueva conexión; E2-01/errata v4 intactos, E3-01/E3-02 no nuevas cotas.

Preparación2026-10-11: solo AGENTS/continuidadv5vigente,estadoGit/inventario,estructuras
JSON v5 necesarias y huellas en lectura. Sin PDF,0páginas; sin nuevos cálculos de
estabilidad/asociaciones/errores/diagnóstico ni revalidación actual del entorno.
Inventario de versionados y SHA previos,documentos nuevos y comprobación final en
REGISTRO_PREPARACION.json. Fuentes ignoradas no se censan/reanalizan en esta preparación;
no afirmar comprobación binaria actual de todo raw. Se conservan sin escritura.
