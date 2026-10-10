# Anexo técnico independiente del objetivo 3

Revisión fase 6, 2026-10-09 (America/Bogota). Partida 10ebe23eb2fd1518956391213301439ef718b844; cierre de fase5 9becbc3239a540dfa8f31f45c281ac3a61361d19. El informe raíz del usuario y las entregas previas permanecen conservados. Este anexo conserva las cifras exactas, IDs y ubicaciones empíricas del informe de fase5 y documenta su revisión. Las notas operativas de fase5 que siguen pertenecen a esa ejecución histórica del proyecto; no describen un entrenamiento nuevo en fase6.

## A. Alcance y decisiones congeladas

Estimando: media del puntaje global recibido de registros elegibles de grado11 por departamento del colegio-año; 198 celdas, 33 territorios, seis años2018/2019/2021/2022/2023/2024 y 2.984.199 registros. Sin certificación de personas únicas, filtro nuevo, cambio de calendario o imputación. IPM mismo año, 1/15/16 entradas, peso igual por celda. Protocolo v1.0 §§1–7 define población, X, selección, métricas y diseños. Las declaraciones del usuario sobre promedio/mediana siguen separadas de decisiones nuevas y controles. No efectos causales ni anticipación con entradas desconocidas.

Selección: 67 candidatos, tres ventanas de años completos, 99 predicciones por candidato. Reevaluación: siete modelos congelados en132 filas hasta2022, 66 predicciones por modelo en2023–2024; años previamente expuestos, no prueba inédita. Diagnóstico territorial: tres ganadores preseleccionados, 33 grupos con cuatro años, entrenamiento128/evaluación4; selección previa y años coetáneos, no validación independiente. Ganador global gradient_boosting_ambas_07 intacto. Persistencia no evaluada.

## B. Correcciones y alcance de las comprobaciones

Registro de cada problema/evidencia/impacto/alternativa/decisión: ../registro_problemas.md F06-01–F06-06. Se corrige «tas as» solamente en copias nuevas. Cruzar0 en percentiles no demuestra heterogeneidad territorial de ventajas: indica dispersión condicional de diferencia agregada. La heterogeneidad de errores se acredita separadamente con metricas_territorio.csv. La condición procede de SVD de X centrada/escalada en desarrollo, sin intercepto, sin umbral universal; no identifica causalidad ni importancia GBR.

Matriz exhaustiva de párrafos/tablas del informe fuente: ../resultados/matriz_trazabilidad.csv, con sección/línea y fuentes. Controles numéricos: ../resultados/verificacion_numerica.json. Verificación final: ../resultados/verificacion_final.json. Conservación inicial/final y manifiesto: ../resultados/. No se cargan estimadores, ajustan modelos, recalculan predicciones ni se generan réplicas nuevas. La revisión aritmética no equivale a repetir entrenamiento. Semilla20261008 pertenece a ejecuciones previas; esta fase es determinista. Entorno histórico no reconstruido; versiones exactas de ejecución previa en ../../fase3/requirements.lock.txt.

## C. Referencias, páginas y límites

Lecturas PDF nuevas en fase6: ninguna. Exposición previa heredada: prom.pdf páginas físicas13–14,18,22; nueva ivestigacion .pdf páginas5–7, comprobadas en fase1 según protocolo§7/continuidad. No se reproduce su clasificación ni se atribuyen autores no documentados. Referencias primarias reconsultadas en fase6: ../referencias_verificadas.md. DANE descripción HTML §§3,4.1–4.5, sin lectura del PDF; documentación scikit-learn rotulada1.9.1, sin confundir stable móvil con versiones locales.

Procedencia local, fórmula global desconocida, medición IPM y poblaciones Saber/IPM distintas, pocos años/dependencia, optimismo de selección y exposición previa permanecen. Remuestreo previo:33 grupos completos, errores/modelos/años fijos, 2.000 réplicas por comparación, siete comparaciones. Sus percentiles no incluyen selección, ajuste, precisión IPM, dependencia espacial ni años futuros; no son intervalos causales o de escenarios.

## D. Presentación y condición de avance

Informe limpio: informe_objetivo_3_revisado.md; HTML semántico: informe_para_copiar.html. Tablas compactas conservan seis decimales; los IDs y columnas completas permanecen abajo y en CSV congelados. Figuras PNG/SVG separadas en figuras/, copias byte a byte de fase5. Prueba local de estructura/renderizado no acredita un pegado real en Google Docs, cuyo documento no fue enlazado ni modificado. La entrega local está separada de revisión/adopción por el grupo, pendiente externa. No escenarios ni objetivo4. Avance: aceptación editorial corresponde al grupo y cualquier cálculo posterior requiere autorización expresa y diseño prospectivo con límites de soporte.

## E. Detalle completo con ubicaciones verificables

La copia documental siguiente mantiene las ocho secciones, diez tablas exactas y cuatro pies de figuras. Su encabezado identifica fase5; las correcciones explícitas F06-01/F06-02 pertenecen a fase6. La matriz fija las líneas del original conservado para cotejo.
