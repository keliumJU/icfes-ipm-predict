# Extensión operativa etapa2 — protocolo4.0.0 intacto

Autorización del usuario en esta sesión: exclusivamente etapa2 v4, fecha cliente
2026-10-10, America/Bogota. El texto «solo etapa1 autorizada» del protocolo congelado
identifica su sesión histórica; la autorización actual permite implementar/probar/
congelar y ejecutar este piloto. No modificar etapa1 ni los criterios congelados.

Decisiones del usuario: panel único y derivado congelado; población y agregación
intactas;2020 excluido/2018historial/2021 previo2019/diferencias sin anualizar;
29 candidatos/defaults/orden/cinco matrices; mediana de todas las filas train con
igual peso; semilla20261010; scaler solo train dentro del Pipeline presupuestado;
modelos aprenden cambios y selección/métricas sobre puntaje reconstruido;
2021 persistencia fija; internas2021–2024 expansivas sin reutilizar entre externos;
bandas MAE/RMSE0.1, entradas ajustadas, familia, JSON; global y cinco grupos antes
externo; deduplicación solo identidad de ID;7200s propios acumulados y cota308
sin fallos/reintentos; cinco comprobaciones atol1e-10/rtol0; meta global exacta≥5%
frente persistencia/v3 en165 llaves/observados íntegros. Sin cambiar estos criterios.

Decisiones de implementación, anteriores al primer fit real: fuentes editables
piloto.py/verificar.py/probar.py/generar_notebook.py/01_resultados_piloto.py/cerrar.py.
Reutilización exclusivamente en lectura de comun_v4/constructor Ridge/métricas/
bandas/Presupuesto. Hijos spawn importan clases v4; prioridad de carpetas propias.
Corrección real estima la mediana en proceso presupuestado. No modelos históricos
cargados. Modelo propio se carga únicamente para reanudación tras validar artefactos.

Runner conserva contexto del panel en memoria/configuraciones/origen/límite/
congelación y un índice de todos sus archivos. Reanudación exige mismo contexto,
huellas/cobertura de archivos/ledger/llaves/observados. Meta del ajuste coteja matrices,
años y llaves train, parámetros/entradas/semilla/entorno/panel/congelación antes de
reutilizar modelo; éxito previo sin artefacto íntegro detiene. Numérico/convergencia
queda inelegible persistente; predicción no finita no se rescata. Infraestructura
permite máximo dos intentos totales, ambos presupuestados; fallo persistente detiene.
Presupuesto agotado no crea un nuevo intento ficticio. Caída pendiente no medida
agota conservadoramente; discrepancia de índice detiene sin aceptar datos alterados.
Sin meta parcial, exclusiones nuevas, rescate de candidatos ni nuevos comparadores.

Presupuesto incluye arranque del proceso, fit del Pipeline/mediana, comunicación,
fallos, reintentos, limpieza/terminación y repeticiones ajustadas. Persistencia mide
su cálculo aparte. Predicción y escritura/lectura de artefactos tienen tiempos
registrados aparte; no se confunden con tiempo de fit. Ledger no se reinicia/amplía.

Fuente/derivado/198 cambios se cotejan íntegramente en preflight. Auditoría recorre
las280 particiones ajustadas requeridas, modelos/transforms/entradas/predicciones,
intentos, selecciones y roles externos; recálculo independiente math.fsum desde CSV
round_trip. Comparadores CSV históricos v1/v2/v3/media/tresOLS se verifican por
huella/selecciones/llaves/observados. Ningún nuevo ajuste o búsqueda comparadora.
Congelación operativa antes de primer fit incluye fuentes, entorno, pruebas y
artefactos reutilizados congelados. No nueva instalación/descarga.

Etapa2 no entrega notebook personal/modelos/simulación ni entrena modelo final.
Notebook útil únicamente lectura de resultados, generado desde fuente editable y
validado con nbformat; celdas ejecutadas con Python exec, no salidas ficticias.
No PDFs leídos ahora (0 páginas). Toda escritura de artefactos dentro v4;
conservación compara el snapshot inicial, salvo continuidad propia actualizada,
cuyo antecedente permanece íntegro. No push. Etapa3 exige autorización distinta.
