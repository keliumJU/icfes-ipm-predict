# Fase4 — auditoría independiente, interpretación y cierre

Fecha: 2026-10-11, America/Bogota. **Recálculos actuales de guardados; cero nuevos fits y cero modelos cargados.** El primario global predefinido mejora 1.7979745286559843%, por debajo de la meta fija del 5%. La auditoría técnica pasó; esta aceptación no acredita autenticidad, disponibilidad temporal ni confirmación científica.

## 1. Entrada, alcance y procedimiento

El primer comando fue `cerrar_fase3.py --verificar`, con PYTHONDONTWRITEBYTECODE=1: aprobado, completa, 1018 huellas, 31245 protegidos y sin diferencias. Su salida se transcribe en REGISTRO_FASE4.json. El auditor independiente `auditor.py` cotejó los manifiestos originales de fase1 (28 huellas), fase2 (234) y fase3 (1018); aceptación, congelaciones y notebooks previos. La continuidad histórica de fase2 se verificó íntegra desde etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md contra el manifiesto original. La continuidad actual de fase3 se preservó antes de actualizarla. No se exige al inventario histórico de fase2 incorporar los artefactos posteriores.

Git HEAD75c3a25182af363f47b0d743820f99084e18fed5, asunto «etapa 2 v5: cerrar piloto36 MAE y auditoria sin mejora», rama codex/objetivo3-v5-mae, ascendencia y ausencia de trabajo posterior versionado comprobados en PREFLIGHT_FASE4.json. V5etapa1 se cotejó en su commit real109797407d75d2097e5b71f8bcef3fc266bc61d2; temporaletapa1 únicamente por texto preservado y huella en su etapa2/resultados/partida.json. No reset, commits ni push.

ENTORNO_FASE4.json acredita Python3.12.14/sklearn1.9.1/54paquetes exactos lock/pipcheck0/PYTHONDONTWRITEBYTECODE=1/semilla20261010 antes de cálculos. Semilla contractual, sin operaciones aleatorias nuevas. Fuentev2 SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5 SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc intactos. Originales conservados. PRUEBAS_AUDITOR.json y AUDITORIA_COMPLEMENTARIA.json guardan ensayos inventados sin fit, positivos y negativos, separados de guardados reales.

`analizar.py:panel/audit`, sin importar selector, constructores ni runners operativos, reconstruyó los 231 niveles/198 cambios, los campos derivados, d/c/r, X/y/llaves/entradas/unidades/contextos, scaler y puntajes de todos los jobs. Los modelos se inspeccionan por parámetros JSON; no se deserializan. Los coeficientes se aplican al scaler guardado, no se estiman. Scaler contrastado aritméticamente con atol1e-12/rtol0 por diferencias de suma; matrices/CSV/contextos/predicciones exigen igualdad exacta. Repetición ajustada: atol1e-10/rtol0. No son relajaciones del cotejo CSV.

Se conserva población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario/media recibida/geografía colegio, 2020excluido, 2018historial, d sin anualizar, 2021externo fijo, 165pares/igualpeso/meta5%. 2019 solo historial, sin respuesta con lag inexistente. El máximo previo de2021 es2019 y el intervalo2 no divide el cambio. La cronología lógica se verifica, pero no autentica fechas de publicación. Cero años completos implica respaldo declarado sin fit; uno permite ajuste. Común1fila/año; territoriales33filas/año. Cuatro candidatos exactos con Pipelines separados y componentes comunes propios; defaults congelados, sin recencia, código como entrada o efecto individual.

## 2. Integridad de cobertura, selección y ejecución histórica

AUDITORIA_INDEPENDIENTE.json:1320internas originales,16registros,825externas,528únicas,1320linajes y5comprobaciones globales. Cada copia interna tiene idénticos valores/contexto y representante de menor externo. Diez internas acumuladas son copias de cuatro años de validación, no diez años independientes. Global reutiliza únicamente candidato y ventana correspondientes. Externa2021 no ajusta ni puntúa ni selecciona; internas2021 sí se puntúan con respaldos. CSV cotejado exactamente contra salidas JSON y copias control_csv, aceptando int/float0 y rechazando1e-11 en pruebas.

Ledger histórico cerrado:41fits=24internos+16externos+1repetición, sin fallos/retries,58.63946153299912segundos de7200 y cota46 sin fallos. AUDITORIA_COMPLEMENTARIA.json coteja95snapshots (0000–0094), arranque durable pending de31jobs ajustados antes success,61jobs totales incluyendo respaldos, ejecución serial, tiempos monotónicos crecientes, identidad acumulada, procesos terminados con retorno0 y cierre final exactamente igual al ledger. La suma de intentos medidos36.574579537005775s no reemplaza el total: este incluye preparación/comunicación/pausas hasta el cierre. No saldo reutilizado ni reapertura. Los registros locales no son autenticación externa de tiempos.

## 3. Resultado primario y contrastes descriptivos

Todas las métricas usan fsum, igual peso y las mismas165llaves/observados (33territorios×5años); RMSE raíz de la media de errores cuadrados. Denominador MAE de persistencia positivo y finito. Tabla completa: tablas/metricas_165.csv.

| Política | MAE (puntos) | RMSE (puntos) | Sesgo predicho−observado (puntos) | Mejora MAE (%) |
|---|---:|---:|---:|---:|
| Persistencia |3.429267191379531|4.314920647368904|−2.0960105973100562|0|
| **Global primario** |**3.3676098407589707**|4.306243910848592|−1.5242014817652496|**1.7979745286559843**|
| Memoria exploratoria |3.004299017227967|4.212665669505837|−0.965693505233788|12.392390281511053|
| Común |3.436546823383837|4.476778255626107|−1.4260966275450535|−0.21227952206830963|
| Común+corrección |3.436546823383837|4.476778255626107|−1.4260966275450535|−0.21227952206830963|

Los resultados declarados por fase3 se cotejaron: discrepancias numéricas ninguna. La política memoria es diagnóstico; su12.392% no sustituye el global para declarar éxito. V3/persistencia, v5/global y recencia/global coinciden exactamente con la misma referencia165pares en tablas/referencias.csv; son una referencia compartida, no tres evidencias independientes.

## 4. Qué aprendió memoria

En los11ajustes guardados de memoria (6internos+4externos+1repetición), coeficiente del rezago exactamente0. Todas las predicciones reconstruidas son **puntaje previo + intercepto constante**. Tabla verificable: tablas/coeficientes_todos_41.csv, filtrando component=memoria; cada fila identifica archivo JSON/pipelines/memoria. Los interceptos externos2022–2025 son −1.2006135943734648,1.6516505643865287,2.341502912644245 y2.8590455777240322puntos.

El intercepto está en el intervalo de medianas empíricas de las respuestas territoriales históricas apiladas; con n par el óptimo de pérdida absoluta puede ser cualquier punto de ese intervalo, por lo que no se exige la mediana promediada. La referencia documental futura de cambio histórico debe fijar esa convención antes de resultados. Impacto: la mejora exploratoria de memoria acredita aquí beneficio de un nivel histórico constante, **no una relación aprendida entre cambios sucesivos**. Alternativa verificable resuelta en esta fase: reconstruir todas las predicciones con coeficiente/intercepto guardados y cotejar el intervalo de mediana, sin fit. Atribuir el cero exclusivamente a alpha1 requeriría un contraste separado que no se ejecutó.

## 5. Común y corrección

Las165predicciones externas de común y común+corrección son exactamente iguales: tablas/correccion_comun.csv y contrastes_pareados_495.csv. Los10ajustes de corrección (6internos+4externos) tienen coeficiente0 e intercepto0; no añaden movimiento territorial bajo esta configuración. Los20componentes comunes separados (10por candidato) se auditaron sin compartir ajuste; sus coeficientes también0 y sus interceptos pertenecen al intervalo de mediana de cambios comunes anuales. Común resume1–4respuestas anuales, frente a33–132territoriales en memoria. Común puede aportar un nivel histórico de movimientos medianos, pero aquí su MAE agregado es ligeramente peor que persistencia. Igualdad y corrección nula no prueban inutilidad en otras configuraciones ni otros periodos.

## 6. Por qué global difiere de memoria

Tabla completa: tablas/decisiones_internas.csv; cada ventana usa únicamente sus internas, MAE≤mínimo+0.1, luego RMSE≤mínimo del pool+0.1, luego entradas0/1/1/2 y orden.

- 2022: las cuatro internas2021 son respaldos iguales (MAE2.6402236932057406/RMSE3.5097490978755155); todos quedan en ambos pools; persistencia gana por0entradas.
- 2023: persistencia MAE3.8660950033867016; memoria4.395729786151121 supera3.9660950033867016. Solo persistencia entra al pool MAE.
- 2024: memoria MAE3.6163992477074265 frente3.6464872456777355 de persistencia; ambas entran al pool MAE. Memoria RMSE4.718798774674416 supera el límite4.543974419419438; el filtro RMSE conserva solo persistencia.
- 2025: memoria MAE3.2707967025508324 frente3.7249352319645874 de persistencia; solo memoria en ambos pools. Global usa memoria2025 y persistencia2021–2024.

La ventaja externa posterior de memoria no estaba disponible para seleccionar antes de evaluar esos años. Usarla retrospectivamente alteraría el procedimiento primario. Un retraso de la selección acumulada frente a cambios del nivel es una hipótesis compatible con este patrón, no una causa demostrada ni una autorización para cambiar ventanas o criterios.

## 7. Distribución del beneficio y deterioro

Tablas completas por año/territorio: por_anio.csv (25filas), por_territorio.csv (165filas), errores_pareados_825.csv y contrastes_pareados_495.csv. Se guardan errores absolutos/firmados, sesgo, cambios observados/predichos y coincidencia de dirección exacta. direccion_cambios.csv conserva signos y medianas anuales. Gráficos con unidades/n: graficos/mae_por_anio.png, beneficio_territorial.png y memoria_nivel_y_rezago.png.

Global coincide con persistencia en132pares2021–2024; toda su mejora agregada procede de2025. En2025 n33, MAEglobal1.9383082759365036puntos, beneficio MAE0.3082867531028031puntos,18territorios mejoran y15empeoran, sin empates. El beneficio agregado sobre165 es0.0616573506205602puntos; sus posibles diferencias de últimos dígitos al operar MAE o beneficios se deben al orden de aritmética binaria. Por territorio en los cinco años también18mejoran y15empeoran porque solo cambia2025. En2025 predice cambio positivo uniforme: coincide con la dirección en27de33; sesgo global+1.364113221808658puntos (sobrepredicción), aunque el sesgo agregado sigue negativo. Acierto de signo no equivale a mejora de magnitud.

No se presentan165pares como observaciones independientes ni copias internas como réplicas científicas. No p-valores ni intervalos de confirmación; pocos años, dependencia territorial/temporal y selección acumulada limitan generalización. Contrastes memoria/persistencia, común/persistencia y corrección/común son descriptivos y exploratorios.

## 8. Hipótesis futuras, límites y cierre

PROPUESTAS_FUTURAS.md especifica preguntas, contrastes, evidencia necesaria y límites. La evidencia justifica estudiar una referencia simple de cambio histórico y separar su aporte del rezago/regularización; no justifica afirmar dinámica predictiva confirmada, elegir hiperparámetros nuevos ni usar estos años como confirmación. No se implementa ningún experimento futuro.

Procedencia local no autenticada. Guainía238vs404/21.012105832431985puntos es antecedente histórico v2/fase1/resultados/diagnostico_medias_disponibles.csv, filas57y90; media recibida intacta. IPMhogares-alumnos, colegio-residencia, ecología sin inferencia individual, dependencia y pocos años permanecen. Todos2021–2025vistos: exploratorio, sin confirmación independiente ni causalidad. Aceptación técnica no resuelve origen oficial, publicación o disponibilidad temporal.

Pendientes indispensables técnicos: ninguno después del cierre verificado. Pendientes científicos: autenticidad/disponibilidad y confirmación independiente, prueba del aporte del rezago/regularización y de referencia simple; requieren protocolo y autorización separados. Sin nuevos fits, búsquedas, regularización cambiada, rediseño, fuentes/instalaciones, commit/push, modelo final, notebook personal, simulación, objetivo4 ni avance automático.
