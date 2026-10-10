# Prompt aprobado de inicio — ejecutar únicamente fase 1

Continúa en `/home/kelium/Documents/espcarlos/icfes-predict-improved` y ejecuta únicamente la fase 1 de `experimentos_objetivo3_v2`, conforme al plan aprobado.

Lee primero `AGENTS.md` y `CONTINUIDAD_OBJETIVO_3.md`; después la continuidad v2 si existe y únicamente fase 1 del nuevo plan. Si falta la carpeta, créala y guarda el plan completo como `PLAN_INVESTIGACION_V2.md`, este prompt como `PROMPT_INICIO_V2.md` y una continuidad propia.

Comprueba Git, registra el commit real de partida y conserva cambios existentes. El cierre conocido es `fc8dc23de8a85cffcc1c87d47ac740650b27ace5`; documenta diferencias. Crea o reutiliza `codex/objetivo3-v2-piloto` sin sobrescribir trabajo.

Consulta protocolo v1, decisiones y entrega revisada de fase 6 como antecedentes. Verifica huellas históricas en modo lectura. Excluye definitivamente 2020; no lo audites ni utilices en sensibilidades.

Usa el Excel local `Fuente del IPM/anex-PMultidimensional-Departamental-2025.xlsx`, con cobertura declarada 2018–2025 y actualización del 14 de abril de 2026. No busques ni descargues otro anexo.

Considera `panel_departamento_anio_unido_2025.csv` como consolidado candidato: tiene 231 filas y 15 tasas, pero falta la columna IPM. Coteja su contenido y completa IPM únicamente en una reconstrucción separada, con fuentes y celdas verificables.

Audita íntegramente ICFES 20251 y 20252 por bloques. Comprueba identidad Saber 11 frente a Pre Saber, población, filtros, cobertura, faltantes, exclusiones, sumas, denominadores y medias. No conviertas nulos en cero ni imputes puntajes. Realiza los diagnósticos definidos en fase 1.

Conserva exactamente las 198 filas históricas y añade 2025 solo si supera los controles. No sustituyas cifras históricas por revisiones del anexo nuevo. Guarda reconstrucciones, controles y registros en la carpeta v2; registra páginas PDF efectivamente leídas.

Documenta las decisiones del piloto futuro: 100 configuraciones, dos horas acumuladas de entrenamiento y notebook personal únicamente si el procedimiento completo reduce el MAE conjunto al menos 5% frente a la referencia v1 reentrenada. No ejecutes ese piloto ahora.

No entrenes, selecciones, generes predicciones, simules ni avances al objetivo 4. No modifiques originales, entregables históricos, continuidad del objetivo 3 o `.gitignore`. No generes todavía notebooks de modelos.

Cierra con auditoría verificable, decisión sobre 2025, conservación, pendientes y continuidad v2 actualizada. Crea un commit local descriptivo únicamente con los nuevos entregables de esta fase e informa identificador, estado Git y rutas. No hagas push ni ejecutes fase 2 sin autorización expresa.
