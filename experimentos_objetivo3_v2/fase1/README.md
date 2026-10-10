# Fase1 v2: auditoría local y ampliación2025

Solo fase1 autorizada. El resultado es el panel separado en
`reconstrucciones/base_analitica_departamento_anio_v2.csv`,231 filas con198
históricas intactas y33 nuevas. Consultar INFORME_AUDITORIA.md para cifras,
registro_problemas.md para decisiones y ../CONTINUIDAD_V2.md para estado vigente.

Se recuperó trabajo sin commit y se reprodujo en copia, preservándolo. La ejecución
de esta sesión consta en resultados/reproduccion_actual.json,
verificacion_reproduccion_actual.json y pruebas_reproduccion_actual.json.
Los controles encontrados no se sobrescribieron ni se presentan como recién generados.

## Entradas, salidas y reproducción

Desde raíz del proyecto, usar Python del runtime de dependencias de Codex con pandas,
numpy y openpyxl; versiones efectivas en verificacion_reproduccion_actual.json.
Los scripts deterministas no necesitan semilla. No contienen entrenamiento.

1. `fuentes/reproducir_en_copia.py`: verifica conservación, crea copia temporal de
   v2 con fuentes enlazadas en lectura y ejecuta auditar_2025.py,
   investigar_identificadores.py, documentar.py y pruebas/test_auditoria.py.
   Censa ambos TXT completos por bloques100.000 y segunda lectura completa;
   coteja resultados con los encontrados y exporta evidencia nueva de reproducción.
2. `fuentes/completar_controles.py`: concentración de exclusiones por etapa y
   territorio/periodo, diagnóstico global disponible, comparación de conteos2024/2025
   y reconciliaciones de filas, denominadores y medias. Sin censo histórico adicional.
3. `fuentes/integridad.py` sin argumentos: verifica311 archivos previos/7 fuentes,
   produce conservación y manifiesto SHA256 de entregables v2. Ejecutar después de
   toda documentación. **No usar --inicio**: el snapshot encontrado fija la partida.

Las entradas son la basev1, raw20251/20252, candidato, anexo local2025 y evidencia
histórica de filtros/agregación; las otras fuentes del snapshot solo se conservan.
Todo derivado nuevo se escribe en v2 o copia temporal. No ejecutar generadores
históricos ni el auditor directamente sobre resultados encontrados: usar copia.
Para reproducir tras el commit, mantener el snapshot original y no inventar nueva
partida. El cierre se identifica por asunto en Git; manifiesto no contiene su hash.

`cifras_xlsx.csv` contiene archivo/hoja/celda por llave/variable. `cotejo_candidato.csv`
contiene fila del candidato y diferencia. `agregados_periodo_2025.csv` y anual
contienen sumas/denominadores/medias; el panel no incluye datos personales.
No notebook de modelo ni métricas de piloto. PDF nuevos: cero páginas.

## Condición de avance

2025 aprobado bajo alcance de coherencia local, con límites de procedencia y
selección por pruebas completas. Fase2 requiere autorización expresa. Piloto futuro:
100 configuraciones, dos horas acumuladas, notebook personal condicionado a mejora
MAE conjunto≥5% frente a v1 reentrenada en las mismas ventanas y procedimiento
completo. Sin cambio de población o criterios basado en métricas. Sin push.
