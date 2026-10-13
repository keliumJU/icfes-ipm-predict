# Revisión de cumplimiento de los cuatro objetivos

12/10/2026. Revisión documental local solicitada por el usuario; no ejecución de análisis ni modificación de ACA2.pdf. Dictamen de correspondencia, no aprobación académica por el director o el grupo. No se afirma haber leído toda la tesis ni haber verificado nuevamente cada resultado anterior.

## Pregunta y objetivo general

ACA2.pdf, p. 23: la pregunta estudia la relación entre IPM y desempeño académico de educación media a nivel departamental en Colombia, 2018–2024. P. 25: objetivo general, analizar esa relación integrando información DANE e ICFES. Las preguntas específicas están en p. 24 y las hipótesis en p. 26.

El periodo escrito contiene seis años observados: 2018, 2019, 2021, 2022, 2023 y 2024, con 2020 excluido. La reconstrucción local auditada contiene 198 celdas y 2.984.199 registros elegibles; no personas únicas certificadas. Fuente: `../auditoria/diagnostico_calidad.md`, apartados Filtros y Base entregada. El contraste posterior usa 231 celdas 2018–2025 y evalúa 165 pares 2021–2025: no reemplaza silenciosamente el universo de tesis. Fuente: `../experimento_pobreza_historia_objetivo3/TEXTO_OBJETIVO3_TESIS.md`, párrafos iniciales.

| Objetivo de p. 25 | Evidencia localizada | Qué falta para cerrar su correspondencia |
|---|---|---|
| 1. Describir IPM, cinco dimensiones, quince indicadores y Saber 11 | Capítulo descriptivo de ACA2; dimensiones pp. 89–91, indicadores pp. 91–94, desempeño y asociaciones hasta p. 114. Auditoría reproduce población y cifras seleccionadas | Consolidar correcciones editoriales y trazabilidad de cifras aún no comprobadas. No hace falta rehacer íntegramente el descriptivo por la falta de sellado histórico |
| 2. Estimar asociación con efectos fijos de departamento y año | Método prometido pp. 56–57; hipótesis H1/H2 p. 26. Correlaciones pp. 104–109 y doble centrado en fase4 son descriptivos | No se encontró una entrega de estimación de ese modelo en los documentos y fuentes buscados. Localizarla si existe; si no, definir y ejecutar el análisis bajo autorización nueva. Correlación no sustituye coeficiente ni inferencia de efectos fijos |
| 3. Diseñar modelo ML departamental con pobreza | Informe revisado fase6, modelos congelados fase3 y diagnóstico fase4; contraste posterior historia/pobreza | Hay evidencia sustancial reutilizable, pero diferencias con método escrito p. 58. Elegir alcance y mejoras con el usuario, conciliar metodología y periodo y preparar una entrega integrable; no comenzar otra búsqueda por defecto |
| 4. Validar en años fuera del entrenamiento y estimar escenarios | Reevaluación 2023–2024 del modelo congelado hasta 2022 y diagnóstico territorial, fase6 §§4–5 | Validación temporal ya tiene evidencia, con años expuestos y límites. No se acredita ejecución de escenarios coherentes dentro de estas entregas. Definir modelo apto, entradas, soporte e interpretación antes de ejecutarlos o acordar modificación académica del alcance |

## Objetivo 1: aprovechar lo construido, corregir sin rehacer por defecto

La tesis declara su cumplimiento en p. 114. Esta revisión constata que existe un capítulo descriptivo, pero no eleva esa declaración a certificación de cada cifra. La auditoría tiene controles extensos de conteos, medios, IPM y asociaciones; su mapa mantiene explícitas las páginas/cifras verificadas y pendientes.

Pendientes concretos:

1. Resolver editorialmente la contradicción de pp. 115–117: la tabla antigua se construyó con otra población/geografía y 160 celdas. La propuesta auditada conserva colegio, grado 11, Bogotá y 2021 y entrega alternativa de 198 celdas. Fuente: `../auditoria/propuesta_correccion_tesis.md`, apartados Ajuste y Tabla 12. La adopción por el grupo no consta.
2. Comprobar mediante procedimientos existentes, si se requiere para entrega final, la trazabilidad de contribuciones dimensionales (pp. 89–91), tasas/figuras (pp. 91–94) y composición/tabla socioeconómica complementaria (pp. 104 y 112). En esta revisión solo se leyó el texto, sin recalcular esas cifras. No inventar dimensiones promediando tasas ni trasladar la certificación de IPM+15 tasas a contribuciones no cotejadas.
3. Matizar frases de pp. 108 y 113 que sugieren mecanismos o insuficiencia de intervenciones. Los cambios entre extremos no prueban ausencia de asociación longitudinal ajustada, causalidad ni eficacia de políticas. Alternativa: presentarlos como descriptivos e hipótesis, dejando la asociación condicional al objetivo 2.

Impacto: mejora coherencia y límites del capítulo existente. No requiere recuperar antecedentes técnicos ya archivados ni excluir 2021/Bogotá por el antiguo panel defectuoso.

## Objetivo 2: principal brecha de análisis localizada

El diseño escrito promete efectos fijos territoriales y de año, IPM contemporáneo, rezagos, incertidumbre agrupada y diagnósticos/sensibilidades (pp. 56–57). La auditoría declara que no ajustó regresión ni estimó efectos fijos; `fase4/resultados/asociaciones_longitudinales.csv` contiene correlaciones entre/dentro/doble centrado sobre 132 celdas de desarrollo. No es una entrega inferencial del objetivo 2 sobre el universo de tesis.

La búsqueda de términos efectos fijos/PanelOLS/fixed effects y objetivo 2 en fuentes/documentos pertinentes no localizó ese resultado. Es ausencia de evidencia localizada, no prueba exhaustiva de inexistencia. Primera alternativa: verificar si el usuario o el grupo dispone de una entrega fuera de ese alcance. Si no existe, es trabajo necesario para mantener el objetivo tal como está escrito.

Antes de estimar se requiere una especificación expresa: mismo universo auditado, respuesta media global, asociación en puntos por punto porcentual de IPM, efectos de departamento/año y procedimiento de incertidumbre adecuado a pocos años/dependencia. Los rezagos se construyen según años calendario o años disponibles de manera explícita; 2019→2021 no es un rezago anual ordinario. Las sensibilidades y pruebas prometidas deben ejecutarse justificadamente o conciliarse académicamente con el método final, no eliminarse después de ver resultados.

H1/H2 pueden no obtener respaldo y el objetivo aun así cumplirse si la estimación es válida y se informa íntegramente. El signo/significancia deseados no son un requisito de cumplimiento. No usar el resultado predictivo de historia/pobreza como contraste de H1/H2.

## Objetivo 3: evidencia útil y decisiones pendientes del usuario

Existen dos ejercicios que responden preguntas diferentes:

- **Modelo con pobreza 2018–2024:** `../fase6/entrega/informe_objetivo_3_revisado.md`, §§1–5, protocolo y artefactos fases3–4. Compara IPM, quince tasas y ambas; media/OLS/Ridge/RF/GBR. Selección con desarrollo hasta 2022; evaluación congelada 2023–2024. MAE conjunto del ganador 6,345582 puntos, ya reportado en tabla 5; no calculado de nuevo aquí. La referencia de persistencia no fue evaluada en ese ejercicio.
- **Complemento incremental frente a historia 2018–2025:** `../experimento_pobreza_historia_objetivo3/TEXTO_OBJETIVO3_TESIS.md`, tablas 1–3. La política ampliada no seleccionó pobreza y tuvo igual MAE que historia bajo sus reglas. Esto no refuta toda relación pobreza-educación ni invalida el modelo contemporáneo anterior. Sus métricas no son directamente comparables: cambian periodos, entradas y procedimiento.

La p. 58 de ACA2 promete controles de año/composición, contribuciones oficiales de las cinco dimensiones, Ridge/Lasso/ElasticNet y respuesta alternativa Matemáticas. El ejercicio de fase6 no ejecuta exactamente esa especificación; el contraste incremental tampoco. Es una diferencia de alcance que debe explicarse, no un fallo de software ni autorización para ejecutar todo.

Dos rutas posibles, pendientes de elegir:

1. Integrar y conciliar el modelo ya entregado con un alcance acotado y defendible, conservando resultados desfavorables y el complemento de historia como tal.
2. Autorizar mejoras focalizadas para responder brechas concretas: especificaciones/controles que se decida mantener, interpretación por bloques oficiales, referencias comparables y evaluación. Requiere protocolo nuevo antes de resultados, presupuesto y criterio práctico propios. No repetir hasta obtener mejora ni heredar el 5 %.

No se escoge ruta todavía. Se preguntó al usuario qué priorizar, restricciones/fecha límite y si conservar 2018–2024 o tratar 2025 como extensión separada. La media global, geografía de colegio y población permanecen intactas; cualquier cambio material se justifica antes de evaluar. Mejorar rigor, interpretación y presentación también cuenta como mejorar, aunque no reduzca el error.

## Objetivo 4: separar validación realizada y escenarios pendientes

La primera parte tiene evidencia concreta: modelo entrenado hasta 2022 evaluado sobre 2023 y 2024 sin usarlos en ese ajuste. Los años ya estaban expuestos en investigaciones anteriores, por lo que no son una prueba inédita. El diagnóstico territorial existente usa hiperparámetros seleccionados previamente con esos territorios; no es validación territorial independiente. Fuente: informe fase6 §§3–5 y protocolo.

La p. 59 añade referencias de promedio territorial y especificación sin IPM/composición, robustez Matemáticas y exclusión 2021; los análisis localizados no acreditan todas esas tareas. Debe conciliarse qué se mantiene con el alcance final del objetivo 3 antes de declarar cumplimiento íntegro.

La parte de escenarios sigue pendiente en las entregas revisadas. Los gráficos y clasificadores antiguos no constituyen una ejecución actual validada. El modelo a emplear debe depender de las variables de pobreza y tener soporte para las entradas hipotéticas; una política que selecciona solo historia no permite atribuir una respuesta a reducir IPM. Se puede obtener un cambio nulo o un modelo predictivo insuficiente: no forzar sensibilidad para producir escenarios atractivos.

Antes de calcular escenarios: decidir modelo y especificación, justificar reducciones plausibles, verificar soporte conjunto y coherencia entre IPM/contribuciones/tasas, documentar qué permanece constante e interpretar solo estimaciones condicionales. La reducción proporcional de tasas no garantiza por sí sola una reducción equivalente del IPM: faltan privaciones conjuntas. Con datos marginales no inventar esa identidad. Si no hay escenarios defendibles, corresponde una decisión académica sobre el objetivo, sin declararlo cumplido.

## Orden recomendado, sin activar ejecución

1. Acordar fecha límite, periodo final y prioridades de mejora del objetivo 3 con el usuario. La pregunta ya está presentada y sigue pendiente.
2. Cerrar correcciones del objetivo 1 y localizar/planificar la estimación del objetivo 2: es la brecha analítica más clara.
3. Conciliar objetivo 3 y metodología con las entregas existentes; ejecutar únicamente mejoras autorizadas y justificadas. Preservar persistencia e historia como referencias y resultados anteriores.
4. Con ese alcance resuelto, completar la correspondencia de validación y decidir escenarios del objetivo 4 en fase separada.
5. Integrar texto, tablas, notebooks existentes y limitaciones en la tesis mediante autorización editorial; no reescribir objetivos silenciosamente.

No se promete una duración de cómputo ni fecha de terminación sin alcance y plazo humanos. No se realizaron nuevos modelos, paneles, microdatos, bases ICFES, escenarios ni contactos externos.
