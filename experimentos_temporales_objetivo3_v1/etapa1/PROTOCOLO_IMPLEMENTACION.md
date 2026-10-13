# Implementación 1.0.0 — criterios aprobados antes de evaluación nueva

Procedencia: el usuario envió expresamente el prompt de fase1, aprobando protocolo
temporal 1.0.0, incluida semivida fija 2. El diseño documental conserva su texto
histórico de propuesta sin ejecutar; no se modifica para reflejar esta autorización.

Población heredada: ESTUDIANTE/no libertad S/grado11/seis puntajes positivos
presentes/sin filtro calendario/media global recibida/geografía colegio. Conteos
solo trazabilidad. Fuente única v2 y derivado v5 con los SHA del diseño. 2018 solo
historial, 2020 excluido; previo máximo anterior por territorio, 2021 previo2019,
intervalo2 sin anualizar. 231 filas/33 territorios/198 cambios reconstruidos exactos.
Esta comprobación no autentica procedencia local ni prueba disponibilidad operativa.

Se heredan exactamente 36 IDs, cinco grupos y unión de 18 entradas, orden, defaults,
semilla20261010 y bandas0.1. Persistencia cuenta cero entradas ajustadas; los demás,
todas las de su grupo. Año/código/intervalo/conteos no entran en X. Sin búsquedas,
nueva familia/variable, simplificación, umbral o fuente. La configuración propia
congelada distingue aprobación actual de estados históricos documentales.

`comun.pesos` recibe SOLO llaves train ordenadas por código/año, valida unicidad y
año entero. Ancla=max(train); bruto=2**(-(ancla-año)/2); normaliza=n*bruto/fsum(bruto).
Todos positivos, igual dentro de año, media1, toda historia recibida retenida;
no usa validación/externo/observados. Vector exactamente1 en uniforme y train de un
solo año. Sin peso explícito en ruta uniforme. No se calculan pesos del panel real
en etapa1. Metadata de pesos inventados en los reportes de cada sesión de pruebas.

`comun.ajustar_inventado` valida origen inventado, construye con defaults heredados,
fija semilla y desactiva routing automático solo dentro del contexto de fit.
Mediana envía escalado__sample_weight/modelo__sample_weight; boosting sample_weight.
Registra ancla/trainaños/llaves/normalización/vector/entradas/parámetros/semilla/
versiones/warnings y, en mediana, mean_/var_/scale_/n_samples_seen_. Audita media y
varianza por fsum independiente, atol1e−12/rtol0. No escala y. Convergencia/runtime
warning invalida ajuste; warnings restantes registrados. Pruebas reales de librería
son exclusivamente sobre inventados; modelos solo memoria/transporte entre procesos.

Métricas y selección siguen igual peso territorio-año; fsum de errores, sin pesos
de recencia. Selector admite solo seis campos internos y los 36 IDs en orden.
Filtra elegibilidad/ventanas completas, MAE banda0.1, RMSE banda0.1, menos entradas,
familia y orden JSON. 2021 persistencia fija sin puntuar candidatos. Global independiente
de cada grupo; deduplicar ajuste externo por ID. Se guarda decisión inventada antes
de ajustar externas inventadas y su SHA acompaña el contexto. Cinco controles
globales: persistencia exacta sin fit o repetición medida (atol1e−10/rtol0 solo
predicción de ajuste repetido, nunca CSV, observados o linaje).

Worker/motor propios usan spawn, presupuesto serial que incluye arranque, Pipeline,
comunicación y terminación. Timeout inclusivo mata/une al hijo; ninguna supervivencia.
Numérico/convergencia inelegible sin retry; infraestructura máximo un retry, segundo
detiene. Reanudar exige contexto/limite idénticos y SHA de artefactos; ajuste completo
no se repite a ciegas. Pendiente sin medición agota conservadoramente el límite.
Estado corrupto se rechaza; no ampliar/reiniciar. Ledger etapa1 SOLO inventado.
Persistencia sin estimador/fit; no se hereda presupuesto v5. Contrato futuro:
350 internos+≤24 externos+≤4 repeticiones=378, nuevo total7200s, no disponible ahora.

CSV round_trip exacto: campos/orden/índices/llaves/valores; int/float0 equivalente,
1e−11 rechazado. Ausencias históricas de fila2018 coinciden por máscaras, sin eliminar
datos; los campos de cambios/evaluación deben ser finitos. Cobertura de dobles
11880 internas/4752 únicas condicionadas/1155 externas, siete procedimientos×165;
no son resultados de recencia. Colapsar copias solo tras igualdad exacta de valores
y firma train/pesos/entradas/defaults/semilla; representante menor externo y linaje
completo, nunca promediar discrepancias. Referencias reales guardadas v5global/v3
cotejadas con previo independiente,165 pares exactos; idénticas entre sí y ajenas
al nuevo fit. No duplican evidencia independiente ni fabrican externas históricas.

Primario futuro fijo recencia_h2/global. Meta contractual global≥5% frente
persistencia en165 pares; ninguna evaluación de cumplimiento se realiza en fase1.
Grupos secundarios, sin rescate/metaparcial. 2021–2025 vistos y exploratorios;
confirmación independiente/fechas de disponibilidad/causalidad siguen sin demostrar.

Destinos lexicográficos y resueltos propios, rechazan .. y symlinks en cualquier
componente incluido base, antes de crear directorios. Escritura exclusiva en etapa1
o continuidad propia. Los symlinks-fixture se conservan por su texto de enlace,
sin tratar sus destinos como outputs propios. Ningún import de runners históricos.
Conservación verifica SHA de todos los antecedentes inventariados y lista Git;
única lectura histórica de continuidad v5 etapa1 usa su commit real109797407d75d2097e5b71f8bcef3fc266bc61d2,
sin excepción para otra ruta. Raw sin lectura/censo; sin nuevas fuentes.

Aceptación: preflight/entorno/reconstrucción/referencias/defaults,17 grupos finales,
notebook6 celdas inventadas,congelación y conservación aprobados. Si falla cualquier
control indispensable, cierre INCOMPLETO. Fase2, su ámbito real y ledger nuevo requieren
prompt separado; ninguna activación automática. Advertencias completas en README.
