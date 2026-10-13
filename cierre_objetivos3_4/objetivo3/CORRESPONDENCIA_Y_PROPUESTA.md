# Objetivo 3 — correspondencia y mejoras focalizadas por acordar

12/10/2026. Lectura documental, no nuevos resultados. Prioridad humana: mejoras focalizadas del modelo y su evaluación. No se ha autorizado una grilla nueva.

## Correspondencia con la p. 58

Fuente de promesas: Tesis Vigente/ACA2.pdf, p. 58 completa, leída en texto y visualmente en esta etapa. Fuente de implementación: fase6/entrega/informe_objetivo_3_revisado.md, §§1–5. Diferencias no equivalen a fallo de software; requieren decidir alcance académico.

| Aspecto | P. 58 | Fase6 existente | Impacto y alternativa |
|---|---|---|---|
| Respuesta/unidad | Media global, departamento-año, 198 observaciones | Coincide; media recibida, colegio, 198 celdas | Conservar, sin repetir auditoría completa |
| Línea base | Efectos de año; proporciones oficial/urbana; número de evaluados | Media constante y OLS; composición, año y conteos excluidos como entradas | Referencias no equivalentes. Verificar composición solo si se decide incorporarla; explicar tratamiento de años futuros |
| Entradas de pobreza | Base+IPM; reemplazo por cinco contribuciones dimensionales y quince tasas; indicador 2021 | IPM, quince tasas, ambas; cinco dimensiones solo como organización documental | No afirmar cumplimiento literal. Decidir cuáles mantener; contribuciones oficiales requieren control propio |
| Familias | Ridge, Lasso, ElasticNet | OLS, Ridge, RF, GBR, media | Ampliación finita si requerida; no añadir familias solo para perseguir error menor |
| Selección | Dejar un año fuera dentro del entrenamiento | Ventanas temporales expansivas hasta 2022 | Son diseños distintos. Fijar diseño consistente con pregunta temporal antes de nuevas métricas |
| Robustez | Proporción de estudiantes en niveles 3 o 4 de Matemáticas | No ejecutada en ese informe | No confundir con media de Matemáticas. Incluir solo si requisito retenido y derivación auditada |
| Anticipación | Puntaje en años no usados en construcción | Estimación contemporánea condicionada a pobreza; 2023–2024 previamente expuestos | Mantener límites; separación del ajuste no prueba anticipación documental ni evaluación inédita |

## Dos ejercicios anteriores, sin mezclar métricas

1. Fase6: 198 celdas 2018, 2019, 2021–2024; desarrollo hasta 2022, reevaluación 2023–2024. Modelo GBR con IPM+tasas, MAE conjunto anterior 6,345582 puntos (tabla 5; no recalculado). Persistencia no evaluada en ese ejercicio (§1).
2. Complemento historia/pobreza: 231 celdas 2018–2025; 165 pares evaluados 2021–2025. La política ampliada escogió historia/persistencia y empató su MAE (tablas 1–2 de experimento_pobreza_historia_objetivo3/TEXTO_OBJETIVO3_TESIS.md). No refuta toda asociación ni demuestra sensibilidad a pobreza. Su umbral anterior del 5 % no se adopta para trabajo nuevo.

## Propuesta inicial, pendiente de alcance

- Prioridad técnica: comparación justa con persistencia e historia, con misma respuesta, llaves, años evaluables y tratamiento del salto 2019→2021, preservando resultados anteriores. Definir antes si comparación de modelos congelados o una nueva selección focal; no comparar directamente los MAE de los dos informes.
- Prioridad académica: conciliar los requisitos de p. 58 con el producto exigido y cambios admitidos. Composición/dimensiones/respuesta alternativa no son precondiciones universales: serán indispensables si se mantiene su promesa en el alcance final.
- Prioridad de entrega: protocolo finito, tabla de evaluación por año/territorio, diferencias y limitaciones; puente al objetivo 4. No prometer mejora, causalidad o escenarios defendibles antes de comprobar soporte.

No estimar efectos fijos para habilitar este objetivo. No rehacer descriptivos ni reabrir versiones históricas. Solo revisar controles necesarios de los insumos elegidos. La tesis completa no queda cerrada al concentrar trabajo en 3/4.

Pendientes antes de propuesta ejecutable: producto a entregar dentro del día; periodo/2025; margen académico del director. Después acordar entradas/candidatos, selección/evaluación, salidas y presupuesto. Aún no existen protocolo nuevo de entrenamiento ni resultados nuevos.
