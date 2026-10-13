# Plan por fases: memoria temporal y componente común

## Propósito y decisiones acordadas

Preparar un experimento nuevo sobre el panel actual que compare persistencia con modelos que aprendan de los cambios anteriores del puntaje y de los movimientos compartidos entre territorios.

Decisiones confirmadas:

- Usar primero el panel actual; nuevas fuentes quedan fuera.
- Incluir modelos estadísticos ajustados.
- Permitir ajustes desde **un año completo de pares de cambios**, documentando su fragilidad.
- Conservar población, objetivo original, evaluación de 165 pares y meta global del 5%.

**Nota de procedencia:** el plan anterior decía «En este turno no se crean archivos porque está activo el modo Plan». Esa frase correspondía al turno de planificación. El usuario autorizó ahora crear el paquete inicial. La ejecución comienza creando el paquete documental; no inicia ajustes ni activa automáticamente fase1.

## Preparación: archivos para retomar el trabajo

Crear una carpeta separada, `diseno_memoria_comun_objetivo3_v1/`, sin modificar los experimentos anteriores.

El paquete inicial contendrá:

- `README.md`: propósito, orden de trabajo y límites.
- `PLAN_FASES.md`: este plan completo.
- `CONTINUIDAD_DISENO.md`: preparación documental realizada y fases pendientes; sin atribuir ejecuciones inexistentes.
- `REGISTRO_PREPARACION.json`: autorización, Git, inventario protegido, huellas y conservación.
- `PROMPT_FASE1_DISENO.md`: prompt reproducido al final de este plan.

Guardar protocolos, especificaciones y resultados nuevos por separado. No crear notebooks ni un ledger operativo durante esta preparación.

## Fases y condiciones de avance

### Fase1 — Diseño científico documental

Leer continuidad vigente y únicamente la sección correspondiente a esta fase. Verificar antecedentes, fuente v2, derivado v5, referencias y restricciones de conservación.

Crear un protocolo nuevo y una especificación ejecutable documental con **cuatro candidatos**, sin búsqueda de parámetros:

| Candidato | Cambio que predecirá |
|---|---|
| Persistencia | Cero |
| Memoria temporal | Cambio territorial a partir de su cambio anterior |
| Componente común | Movimiento compartido a partir del movimiento común anterior |
| Común con corrección territorial | Predicción común más una desviación territorial aprendida |

Definiciones fijas:

- \(d_{j,t}\): cambio observado original del territorio \(j\), sin anualizar.
- \(c_t\): mediana de los 33 cambios territoriales del año; es una estadística auxiliar, no una nueva media nacional ni un reemplazo del objetivo.
- \(r_{j,t}=d_{j,t}-c_t\): desviación respecto al movimiento común.
- Memoria: aprender \(d_{j,t}\) a partir de \(d_{j,\mathrm{previo}(t)}\).
- Común: aprender \(c_t\) a partir de \(c_{\mathrm{previo}(t)}\).
- Corrección territorial: aprender \(r_{j,t}\) a partir de \(r_{j,\mathrm{previo}(t)}\), compartiendo parámetros entre territorios. No introducir efectos individuales por código.

Usar `StandardScaler` y `QuantileRegressor`, cuantíl 0.5, `alpha=1.0`, `fit_intercept=True`, `solver="highs"`, sin pesos de recencia. Registrar los defaults completos del entorno contratado. Esta regularización es una propuesta fija, no un valor optimizado.

Cada componente común se entrenará con una observación por año; memoria y corrección, con una por territorio-año. La disponibilidad de un solo año implica que el componente común aprenderá principalmente un nivel: advertirlo expresamente.

**Historia incompleta:** 2019 permanece como historial y proporciona el cambio anterior de 2021, pero no puede aportar una respuesta supervisada con rezago porque falta su cambio anterior. No imputarlo. Con cero años completos de pares, aplicar persistencia como respaldo declarado; con uno, ajustar. Mantener 2021 externo fijo en persistencia.

Usar siempre el máximo año anterior disponible; conservar el salto 2019–2021 sin anualizar ni inventar 2020. No utilizar objetivos del año evaluado para calcular sus entradas o su componente común.

Entregables: protocolo, especificación JSON, decisiones, trazabilidad temporal, lecturas, conservación y manifiesto documental. Preparar prompts separados para fases2–4. **No entrenar ni convertir el diseño en congelación operativa.**

### Fase2 — Implementación, controles y congelación

Solo mediante su prompt enviado expresamente y diseño aprobado.

Crear implementación propia en `experimentos_memoria_comun_objetivo3_v1/etapa1/`, con continuidad experimental separada. Reutilizar funciones entre componentes; no importar runners históricos.

Controles sobre datos inventados:

- Rezagos estrictamente anteriores, años completos y respaldo por ausencia de pares.
- El año de validación no modifica matrices ni estadísticas de entrenamiento.
- Mediana común calculada sobre los 33 territorios correctos.
- Componentes comunes y territoriales entrenados con sus unidades respectivas.
- Un año de pares permitido; cero años sin fit.
- Reconstrucción del puntaje mediante previo más cambio predicho.
- Selección, cobertura, CSV exactos, linaje, rutas y symlinks.
- Terminación, fallos, presupuesto, reanudación y conservación.

Crear notebook de controles desde fuente Python y generador Python, con `nbformat` y celdas realmente ejecutadas. Congelar código, candidatos, reglas, defaults, entorno y pruebas **antes de ajustes reales**.

Aceptación: controles indispensables aprobados, entorno exacto y conservación íntegra. Si falla, cerrar incompleto; no iniciar fase3 automáticamente.

### Fase3 — Piloto exploratorio

Solo mediante prompt separado y fase2 completa y congelada.

Conservar las ventanas anteriores y las bandas MAE/RMSE de 0.1. Seleccionar globalmente entre los cuatro candidatos usando exclusivamente internas; desempatar por número de entradas derivadas —0, 1, 1 y 2— y orden de la tabla.

El primario será **el procedimiento de selección global**, definido antes de externas. Las salidas individuales serán diagnósticas y no podrán sustituirlo para declarar éxito.

Guardar:

- **1320 predicciones internas originales:** cuatro candidatos × diez internas × 33 territorios.
- **16 registros de selección:** cuatro candidatos × cuatro selecciones.
- **825 externas:** cuatro candidatos y procedimiento global × 165 pares.
- **528 internas únicas**, únicamente si copias y contexto coinciden exactamente, con linaje y representante menor externo.

Ajustar las cuatro políticas externas predefinidas para disponer de un contraste completo; no elegir retrospectivamente entre sus resultados. Reutilizar para el global solo la salida del mismo candidato y ventana. No reutilizar ajustes entre ventanas ni compartir ajustes de componentes entre candidatos distintos.

Presupuesto nuevo propuesto: **7200 segundos**, sin heredar saldos. Cota sin fallos: **46 ajustes de componentes** —24 internos, 16 externos y hasta 6 repeticiones globales—. Cada scaler/regresor completo cuenta como un ajuste; persistencia y respaldos no tienen fit.

Mantener ledger persistente, runner serial terminable, un retry máximo de infraestructura y fallo numérico inelegible. Caída sin tiempo medido agota conservadoramente el saldo. Toda repetición consume presupuesto.

### Fase4 — Auditoría, interpretación y cierre

Auditoría independiente de matrices, fechas, componentes, referencias, selección, presupuesto, cobertura y copias. CSV exactos, equivalencia int/float cero y rechazo de cambios de \(10^{-11}\). Repeticiones ajustadas: atol \(10^{-10}\), rtol cero.

Evaluar la meta original:

\[
100\frac{MAE_{\mathrm{persistencia}}-MAE_{\mathrm{global}}}
{MAE_{\mathrm{persistencia}}}\geq5
\]

Recalcular la referencia sobre las mismas 165 llaves y observados. Los controles históricos v5/global, v3/persistencia y recencia/global coinciden; no contarlos como evidencias independientes ni cargar sus modelos.

Entregar informe incluso sin mejora, tablas completas, gráficos con unidades y n, notebook de resultados ejecutado desde fuentes editables, registro, manifiesto, conservación y continuidad.

Interpretar por separado:

- Si la memoria ayuda.
- Si el componente común ayuda.
- Si la corrección territorial aporta respecto al común.
- Si el procedimiento global satisface la meta.

Estas comparaciones serán descriptivas y exploratorias. Un piloto incompleto permite documentar lo ocurrido, pero impide síntesis dependientes de controles irresueltos. Ningún resultado habilita automáticamente fuentes nuevas, entrenamiento final, simulación u otra fase.

## Prompt para iniciar una nueva sesión

Contenido de `PROMPT_FASE1_DISENO.md`:

# Nueva sesión — fase1 documental de memoria temporal y componente común

Trabajar en `/home/kelium/Documents/espcarlos/icfes-predict-improved`.

Este prompt autoriza exclusivamente fase1 de diseño documental. No autoriza fits reales o inventados, piloto, notebook de modelos, congelación operativa, instalaciones, fuentes adicionales, commit o push. Su existencia o lectura no autoriza ejecución; únicamente su envío expreso por el usuario autoriza esta fase.

Leer AGENTS.md, continuidad propia del diseño y continuidades vigentes del diagnóstico y experimento temporal cerrado. De PLAN_FASES.md leer únicamente fase1 y las decisiones comunes necesarias. Si falta continuidad propia, comenzar con inventario; no inventar fases anteriores.

Verificar Git HEAD/asunto/rama/ascendencia/trabajo posterior y conservación de antecedentes, sin reset ni sobrescribir ajenos. Validar las continuidades históricas versionadas en su commit real. Para la continuidad anterior del experimento temporal, usar la versión preservada y su huella en etapa2/resultados/partida.json, según su cierre; no modificar su etapa1.

Revalidar fuente v2 SHA256 `6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3` y derivado v5 SHA256 `aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc`. Antes de cálculos, comprobar Python3.12.14/sklearn1.9.1/54paquetes del lock/pipcheck, PYTHONDONTWRITEBYTECODE=1 y semilla20261010. Ausencia o diferencia: documentar y consultar, sin sustituciones o instalaciones.

Formalizar los cuatro candidatos y todas las reglas de fase1: persistencia, memoria, componente común y común con corrección territorial; QuantileRegressor0.5/alpha1/StandardScaler, sin búsquedas. Un año completo de pares permite ajuste futuro; cero obliga al respaldo explícito.2019 permanece como historial, sin imputar un rezago inexistente. Conservar objetivo sin anualizar, 2021fijo, particiones,165pares/meta5% y evaluación igual peso territorio-año.

Escribir exclusivamente en diseno_memoria_comun_objetivo3_v1/. Crear protocolo, especificación documental, decisiones, trazabilidad, lecturas, registro, aceptación, conservación, manifiesto y actualización de continuidad. Preparar prompts independientes de implementación/controles, piloto y auditoría, cada uno condicionado a la fase anterior válida.

Distinguir decisiones propuestas de aprobaciones, resultados históricos de hipótesis y diseño documental de congelación operativa. Preservar las advertencias de procedencia local, Guainía, IPMhogares-alumnos, colegio-residencia, ecología, dependencia y pocos años. Todos2021–2025 ya vistos: exploratorio, sin confirmación independiente ni causalidad.

Cerrar con entregables verificables y pendientes. No avanzar automáticamente a fase2.
