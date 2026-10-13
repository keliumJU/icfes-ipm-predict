# Camino propuesto para cerrar los cuatro objetivos de la tesis

Versión 1.0, 12/10/2026. Plan solicitado por el usuario; no ejecución de los análisis propuestos. Las preguntas y decisiones se atenderán en la nueva sesión por objetivo. No se presume respuesta a las preguntas presentadas en la sesión anterior.

## 0. Inicio, reglas comunes y decisiones generales

### Propósito y fuentes de partida

La pregunta de ACA2.pdf, p. 23, estudia la relación entre el IPM y el desempeño académico departamental en Colombia en 2018–2024. Pp. 24–25 contienen preguntas específicas y objetivos; p. 26, hipótesis; pp. 56–60, metodología. El fin de este camino es completar su correspondencia con resultados verificables, sin exigir una relación significativa, un modelo ganador o un escenario favorable.

Leer AGENTS.md, CONTINUIDAD.md de este paquete y esta sección 0. Consultar `../revision_cumplimiento_objetivos_20261012/REVISION_CUATRO_OBJETIVOS.md` y `CIERRE_RAMA_HISTORICA.md` para entender el diagnóstico, sin reconstruir todos los experimentos. Después leer solo la sección del objetivo que se vaya a abordar y su evidencia necesaria. No tratar planes viejos como protocolos nuevos autorizados.

Antes de escribir, verificar este paquete en lectura: `python3 -B plan_cierre_cuatro_objetivos_20261012/fuentes/control.py verificar` desde raíz. Guardar ese resultado y registrar una partida nueva. El verificador tiene inventario externo cerrado: usarlo antes de ampliar; después crear control propio para la ampliación, sin editar verificadores/manifiestos previos. La conservación de archivos no certifica cumplimiento científico.

Usar una carpeta nueva de trabajo, sugerida `cierre_tesis_por_objetivos/`, con subcarpetas por objetivo y continuación propia. Si ya existe, leer su continuidad y reusar su estado sin sobrescribir entregas cerradas. Preservar este paquete, revisión previa, investigaciones, originales y resultados. Temporales en /tmp. No modificar ACA2, .git ni runtime compartido; no commit/push. No nuevas descargas, microdatos, bases ICFES ni contactos por defecto. El plan no autoriza por sí solo ajustes, escenarios o adquisición de datos.

### Preguntas iniciales, antes de elegir alcance

Hacer un bloque breve, permitiendo respuesta libre y evitando preguntar otra vez lo ya contestado:

1. ¿Cuál es la fecha límite real y qué debes entregar: documento de tesis, resultados/notebooks, presentación u otro producto?
2. ¿Quieres conservar 2018–2024 como periodo central y separar 2025 como complemento, o necesitas discutir una ampliación formal con el director?
3. ¿Qué objetivos/metodología ya aprobó el director y qué cambios pueden acordarse? ¿Existen resultados adicionales, especialmente del objetivo 2, no incluidos en la revisión local?

Mientras llegan respuestas, se puede inventariar y organizar evidencia existente en lectura. No adoptar por silencio cambios de periodo, población, respuesta o evaluación. No pedir ahora al usuario todos los detalles técnicos de los cuatro objetivos: tratarlos cuando se llegue a cada uno.

### Estado y decisiones comunes

- Base de tesis auditada: 33 territorios, seis años 2018, 2019 y 2021–2024; 198 celdas. Departamento del colegio, registros elegibles de grado 11, ambos periodos sin filtro nuevo de calendario, media global recibida, mismos filtros, igual peso territorio-año. Fuente: auditoria/diagnostico_calidad.md y propuesta_correccion_tesis.md. No sustituir por el antiguo panel raíz defectuoso.
- Contraste complementario: 2018–2025, 231 celdas y 165 pares evaluados, con 2018/2019 para historia y salto 2019→2021 sin anualizar. Mantenerlo separado del periodo literal de tesis. No trasladar sus métricas a otro diseño como comparación directa.
- Rama de versiones históricas detenida por el usuario. Conservar falta de autenticación histórica DANE y de ediciones ICFES como limitaciones; no reabrir búsqueda ni escoger fecha de uso. La autenticación actual de libros DANE sí está respaldada. Estimación retrospectiva condicionada a pobreza conocida no acredita pronóstico disponible antes de la publicación.
- Los años de evaluación ya fueron examinados durante la investigación. Separación del entrenamiento no convierte una reevaluación en prueba inédita.
- Mantener persistencia e historia como referencias pertinentes; no heredar candidatos, presupuestos o umbral del 5 %. No cambiar reglas para obtener una mejora.
- Ante cada hallazgo: archivo/página/tabla/procedimiento, impacto, alternativa verificable, decisión y resolución o pendiente. No reabrir antecedentes archivados sin evidencia nueva pertinente.

### Cómo cerrar decisiones y ejecutar

Para cada objetivo entregar primero un diagnóstico breve y una propuesta concreta de alcance. Preguntar solo por preferencias o decisiones materiales que la evidencia no resuelva. Registrar declaraciones humanas, comprobaciones y propuestas nuevas por separado. La autorización de planificar o revisar no equivale a entrenar o simular; cuando se acuerde y autorice una fase concreta, completarla sin pedir permisos rutinarios repetidos.

Fijar especificación, evaluación, salidas y presupuesto nuevo antes de observar nuevos resultados. Crear fuentes .py antes del procesamiento y reutilizar funciones. Los notebooks deben aportar valor, generarse y validarse desde Python, sin datos personales o salidas ficticias. Cerrar cada fase con entrega, pendientes, verificación y continuidad propia; no avanzar a una ejecución distinta automáticamente.

## 1. Objetivo 1: consolidar descripción y corregir coherencia

**Pregunta:** ¿cómo se comportaron el IPM, sus dimensiones/indicadores y Saber 11 en el periodo? **Estado:** capítulo descriptivo sustancial y auditoría disponible; no corresponde rehacerlo todo.

### Preguntas de este objetivo

- ¿El grupo ya incorporó la corrección propuesta de pp. 115–117 o debe prepararse el reemplazo para revisión?
- ¿Necesitas cerrar los descriptivos esenciales o también verificar/completar las tablas y figuras complementarias prometidas?

### Trabajo propuesto

1. Mapear cada requisito a resultados existentes: IPM, cinco contribuciones dimensionales oficiales, quince tasas, puntaje global/áreas y denominadores. Usar ACA2 pp. 56, 65–114, mapa de auditoría y controles existentes; leer PDF por páginas necesarias, sin afirmar lectura integral.
2. Conciliar población, geografía, años y tabla 12 con la propuesta auditada de 198 celdas. Conservar la antigua construcción como antecedente distinto, sin retirar 2021/Bogotá.
3. Identificar qué cifras ya se comprobaron y cuáles requieren comprobación focal: contribuciones de dimensiones, figuras de tasas y composición/tabla socioeconómica. No convertir una lectura de texto en reproducción de cifras ni extender el cotejo IPM+15 tasas a otras hojas sin comprobarlas.
4. Corregir interpretaciones: separar correlaciones entre territorios y cambios entre extremos; evitar afirmaciones de mecanismos o eficacia de intervenciones. No inventar dimensiones oficiales con promedios de tasas.

**Entregables:** matriz de cobertura descriptiva, lista de correcciones con ubicaciones y texto/figuras reutilizables necesarios; si se autorizan cálculos, fuentes y comprobación por procedimiento. **Cierre:** requisitos descriptivos cubiertos y correcciones respaldadas, o pendientes concretos delimitados. Preparar texto no equivale a modificar ACA2 ni a aceptación del director.

## 2. Objetivo 2: localizar o realizar la estimación de asociación ajustada

**Pregunta:** ¿cuál es la magnitud y signo de la asociación al controlar diferencias territoriales y de año? **Estado:** no se localizó una entrega de efectos fijos en el alcance revisado. Correlaciones y doble centrado no cumplen por sí solos esta tarea.

### Preguntas de este objetivo

- ¿Existe una estimación de panel del grupo o del director que debamos revisar antes de planear una nueva?
- Si no existe, ¿se mantiene íntegramente el método de pp. 56–57 o se debe proponer al director un alcance justificado y acotado según el plazo?

### Preparación y ejecución condicionada

1. Localizar evidencia adicional si se aporta; no afirmar inexistencia absoluta ni ejecutar de nuevo algo ya defendible.
2. Si falta el análisis, preparar protocolo para la base acordada: respuesta media global, IPM en porcentaje, efectos de departamento y año, cobertura efectiva y asociación expresada en puntos de puntaje por punto porcentual de IPM.
3. Conciliar H1/H2 y promesas de p. 57: contemporáneo, rezagos, varianza entre/dentro, inferencia agrupada y diagnósticos/sensibilidades. Decidir explícitamente rezago calendario o periodo disponible: 2019→2021 no es un año. Verificar identificación, grados de libertad y estimabilidad antes de ajustar. Justificar procedimientos con pocos años/dependencia; no aplicar pruebas por lista sin revisar sus requisitos.
4. Presentar qué es esencial y qué es sensibilidad. Omitir o cambiar una tarea prometida requiere justificación previa y correspondencia académica, sin elegirla por significancia.
5. Solo tras acordar y autorizar alcance, estimar, comprobar y documentar coeficientes, incertidumbre, muestras y diagnósticos. Un resultado débil, nulo o no significativo puede cumplir el objetivo. No inferir causalidad.

**Entregables:** protocolo, fuentes/notebook útil, tabla de asociación y diagnósticos, interpretación y texto incorporable. **Cierre:** asociación condicional estimada y reportada con límites, o control indispensable sin resolver. No usar el contraste predictivo como sustituto de H1/H2.

## 3. Objetivo 3: decidir mejoras con el usuario y consolidar el modelo

**Pregunta:** ¿con qué error un modelo estima el promedio departamental a partir de pobreza? **Estado:** modelos e informe fase6 para 2018–2024 y complemento posterior frente a historia. Son ejercicios diferentes y ambos deben conservarse.

### Preguntas obligatorias al llegar aquí

El usuario pidió expresamente participar en las mejoras de este objetivo. Antes de elegir cambios, preguntarle:

1. ¿Qué quieres priorizar: cumplir el objetivo escrito con rigor y alcance acotado, ampliar comparación/evaluación, mejorar interpretación de indicadores, presentación para tesis/notebooks, o una combinación? ¿Hay algo concreto que debamos incluir o evitar?
2. ¿Quieres aprovechar el modelo existente como núcleo o estudiar una ampliación focalizada? Recomendar reutilizar y señalar el costo/beneficio de cada ampliación, sin prometer menor error.
3. ¿Qué requisitos de p. 58 necesitas mantener: composición/año, contribuciones dimensionales, familias regularizadas, Matemáticas como robustez? Mostrar primero qué existe y qué faltaría, para no exigir al usuario decidir a ciegas.

Usar fecha límite y periodo ya acordados, sin volver a preguntarlos. No interpretar silencio como preferencia ni seleccionar mejoras de antemano.

### Trabajo propuesto después de responder

1. Revisar el informe `fase6/entrega/informe_objetivo_3_revisado.md` y sus evidencias como núcleo reutilizable: estimación contemporánea, IPM/tasas/ambas, selección hasta 2022 y evaluación 2023–2024. Mantener diagnóstico territorial como tal.
2. Separar el complemento `experimento_pobreza_historia_objetivo3/TEXTO_OBJETIVO3_TESIS.md`: aporta contraste frente a historia bajo otro diseño y periodo; no equivale a todo el objetivo 3, no invalida asociaciones ni permite transferir métricas directamente.
3. Crear matriz p. 58 frente a implementación: controles, cinco dimensiones oficiales, quince tasas, familias, validación y respuesta alternativa. Elegir con el usuario entre conciliación del alcance existente y mejoras focalizadas. Conservar media, población y filtros salvo cambio material explícito y justificado.
4. Si se autorizan nuevos ajustes, congelar antes candidatos, entradas, transformaciones, selección, métricas, ventanas, referencias comparables y presupuesto. Tratar años vistos como exploratorios. Mantener desempeño desfavorable; no perseguir el 5 % ni reseleccionar usando errores externos.
5. Mejorar interpretación mediante preguntas concretas y bloques oficiales, teniendo en cuenta colinealidad y soporte. No equiparar correlación, coeficiente e importancia, ni agregar herramientas solo por sofisticación.
6. Preparar entrega académica unificada: propósito, datos, diseño, resultados, errores por año/territorio, referencias, limitaciones y relación con objetivo 4. Notebooks por etapas útiles, fuentes compartidas y ejecución verdadera solo en fase autorizada.

**Entregables:** decisiones del usuario, matriz de correspondencia, protocolo de mejoras si procede, resultados preservados y complementos separados, texto y tablas/figuras/notebooks necesarios. **Cierre:** modelo o procedimiento documentado y evaluación defendible dentro del alcance acordado; no requiere ganar a todas las referencias. Cambios de método/objetivos para la tesis requieren decisión académica, no una sustitución silenciosa.

## 4. Objetivo 4: cerrar validación y decidir escenarios por separado

**Pregunta:** ¿qué precisión tiene el modelo en años fuera del ajuste y qué estima bajo escenarios de pobreza? **Estado:** validación temporal existente con límites; escenarios actuales coherentes no acreditados en las entregas revisadas.

### Preguntas de este objetivo

- ¿Qué validaciones del diseño escrito se mantendrán después de acordar el objetivo 3 y cuáles ya quedan cubiertas por evidencia existente?
- ¿Debemos preparar escenarios condicionales defendibles, o plantear al director una modificación del alcance si el modelo/datos no los sustentan?
- Si los escenarios son viables, ¿qué reducciones y presentación interesan? Mostrar primero las opciones de p. 59 y sus límites; no preguntar por efectos causales que el diseño no identifica.

### Trabajo propuesto

1. Mapear validación existente: 2023–2024 fuera del ajuste, años previamente vistos; diagnóstico territorial con selección previa de parámetros. No exigir un año nuevo como condición añadida para toda la tesis, ni llamar confirmatorio al material expuesto.
2. Conciliar las referencias y robusteces de p. 59 con el alcance acordado: promedio territorial, especificación sin IPM, Matemáticas y exclusión 2021. No excluir años por mal desempeño ni combinar evaluaciones distintas en una métrica única.
3. Elegir un modelo que pueda responder a cambios de pobreza y revisar utilidad, soporte marginal/conjunto, unidades y coherencia. Una política que selecciona solo historia no sustenta sensibilidad a IPM; tampoco se debe forzar esa sensibilidad.
4. Definir escenarios antes de calcular: reducciones de p. 59 u opciones justificadas, variables que cambian, qué se mantiene constante, anclaje observado, límites de extrapolación y presentación de incertidumbre. Las tasas marginales no reconstruyen privaciones conjuntas: reducción proporcional no garantiza un cambio equivalente del IPM.
5. Ejecutar escenarios únicamente con autorización concreta de esa fase y guardar resultados separados. Interpretar diferencias como predicciones condicionales, no efectos de políticas. Si faltan soporte/coherencia o un modelo apto, documentar inviabilidad y alternativa académica; no fabricar escenarios ni declarar cumplida esa parte.

**Entregables:** matriz de validación, protocolo de escenarios o dictamen de inviabilidad, fuentes/notebook y resultados solo si se ejecutan, texto incorporable con límites. **Cierre:** ambas tareas cubiertas con evidencia o alcance académico modificado expresamente; validación sola no cumple toda la redacción original.

## 5. Integración final y cierre de tesis

Abordar esta sección cuando los cuatro objetivos tengan dictamen explícito. Preguntar qué versión editable/formato de entrega usar y si el usuario autoriza integrar cambios; conservar ACA2 y preparar una nueva versión por separado. La aprobación de escritura/edición no autoriza enviar al director ni publicar.

1. Matriz final objetivo → pregunta → método efectivamente ejecutado → resultado → ubicación → limitación/pendiente. Separar entregas terminadas, comprobaciones técnicas y aceptación académica.
2. Conciliar objetivos, hipótesis, metodología, periodo, población, tablas, resumen, discusión y conclusiones. No confundir asociación con aporte predictivo incremental o con causalidad.
3. Comprobar cada cifra y referencia material; revisar visualmente los artefactos finales cuando corresponda. Versiones, semillas, entradas, salidas y orden de notebooks en anexo técnico; sin datos personales.
4. Entregar materiales editables, reporte de verificaciones, pendientes externos y continuidad. No declarar la tesis completa si un objetivo indispensable sigue abierto; indicar qué falta y qué decisión lo resolvería.

## Prioridad ante plazo corto

Primero aprovechar descriptivos y modelos existentes; corregir incoherencias esenciales y resolver la brecha de efectos fijos. Después mejoras del objetivo 3 elegidas por el usuario y escenarios solo si resultan sustentables. Las ampliaciones opcionales no deben desplazar requisitos centrales. Estimar duración después de conocer plazo, alcance y disponibilidad de evidencia; no prometer resultados en horas ni una fecha de cierre sin esa información.
