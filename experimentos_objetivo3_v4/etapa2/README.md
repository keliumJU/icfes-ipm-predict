# Etapa2 v4 — orquestación y piloto29

Autorización exclusiva etapa2, protocolo4.0.0 y extensión PROTOCOLO_OPERATIVO.md.
Fecha cliente2026-10-10, America/Bogota. Semilla20261010. Toda salida v4.
Entorno existente Python3.12.14/sklearn1.9.1/54 paquetes exactos de
etapa1/requirements.lock.txt, comprobados con pip check; no instalar/descargar.

Ejecutar desde la raíz del repositorio con PYTHONDONTWRITEBYTECODE=1 y
/tmp/icfes-v2-fase2-venv/bin/python, previa comprobación del entorno. Orden:

1. Antes de crear etapa2 se ejecutó etapa1/fuentes/cerrar.py --verificar en lectura.
   Su guardia histórica prohíbe la presencia de etapa2; después se usa
   piloto.verificar_etapa1, que comprueba las mismas huellas y la continuidad histórica
   en Git7f25ad0, sin cambiar ni ejecutar cierres antiguos.
2. fuentes/piloto.py --preflight: conserva snapshot/Git/entorno,231 filas/198 cambios,
   fuente/derivado/trazabilidad/grilla29/defaults y referencias. No repetir este paso
   después de iniciar ledger real: rechaza sobrescribir partida/entorno.
3. fuentes/probar.py: sintéticos/dobles, nuevos directorios por ejecución dentro de
   resultados/sinteticos. Prueba completa, procesos hijos reales, reanudación, fallos,
   rutas/huellas/cobertura, agotamiento y terminación. No usa datos reales para ajustar.
4. fuentes/piloto.py --freeze: verifica fuentes de los controles y congela fuentes,
   entradas/entorno/lock/código reutilizado/grilla/pruebas/protocolo operativo. Solo
   antes de ledger real; no recongelar ni editar código congelado tras el primer fit.
5. fuentes/piloto.py: piloto serial con ledger propio7200s. La misma invocación reanuda
   únicamente si coincide contexto/huellas/artefactos/intentos; no reinicia saldo.
6. fuentes/verificar_extension.py: ejecuta auditoría original verificar.py con
   enmienda explícita E2-01 (tipos inferidos CSV, igualdad exacta), fuentes congeladas
   y ledger intactos; audita íntegramente CSV/modelos propios por huella, sin cargar
   modelos ni ajustar; verifica particiones/entradas/scalers/medianas/defaults/selecciones/
   ledger/orden/repeticiones/165 externas por procedimiento y comparadores históricos.
   Calcula métricas independientes y meta solo si la cobertura está completa.
7. fuentes/generar_notebook.py: fuente editable01_resultados_piloto.py; genera/valida
   notebook01_resultados_piloto.ipynb y ejecuta sus tres celdas de lectura con Python exec,
   sin kernel Jupyter ni ajustes adicionales; guarda evidencia/salidas realmente obtenidas.
8. fuentes/cerrar.py: comprueba conservación y crea manifiesto únicamente etapa2.
   --verificar es lectura. Commit local solo v4, sin push.

Entradas: único panel v2/fase1/reconstrucciones/base_analitica_departamento_anio_v2.csv
SHA2566cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;
derivado congelado v4/etapa1/reconstrucciones/panel_cambios.csv
SHA256aa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc;
configuraciones/defaults/ventanas/huellas/lock etapa1; código previo solo en lectura;
CSV históricos v3/etapa2 y v2/fase3, sus selecciones y huellas. No raw adicional,
modelos históricos cargados, ajustes ni búsquedas comparadoras.

Salidas: resultados/piloto/contexto.json/indice_integridad.json/ledger.json;
seleccion_AAAA.json antes externo; ajustes/ETIQUETA (modelo.joblib,ajuste.json,
entradas_entrenamiento.csv,entradas_prediccion.csv,predicciones.csv,huellas,transformación,
mediana cuando aplica,parametrización completa,advertencias,tiempos,semilla y referencias
al entorno congelado); persistencia/ETIQUETA con cálculo aparte, cero fit;
externas_AAAA.csv/reproducibilidad.json/estado.json; tablas agregadas
predicciones_internas/externas,metricas_internas/metricas,ganadores;
meta/fallos_advertencias/verificacion; partida/entorno/pruebas_sinteticas/congelacion_operativa;
notebook y verificacion_notebook; informe/registro/conservacion/manifiesto.

Persistencia recalculada sin fit; corrección común sí ajustada y presupuestada.
Numérico/convergencia conserva inelegibilidad; infraestructura un reintento máximo;
caída no medida agota conservadoramente; fallos persistentes/integridad/cobertura/
límite detienen con evidencia incompleta y sin meta parcial. No alterar resultados
ni borrar intentos. No reutilizar internos entre externos ni saldos anteriores.

Resultados y límites en INFORME_PILOTO.md. Notebook útil de resultados, no personal,
modelos ni simulación. No etapa3, objetivo4, entrenamiento final ni push.
PROMPT_ETAPA3_NUEVA_SESION.md se guarda para otra autorización y no se ejecuta.

Resultado verificado: MAE global3.6091786595605684 frente persistencia/v3
3.429267191379531; mejora exacta−5.246353175200156%, meta no satisfecha.
282 ajustes/282 intentos,0 fallos/advertencias,259.8488030679364s/7200.
Siete procedimientos×165 externas completas; cinco comprobaciones diferencia0.
Notebook útil de resultados validado/ejecutado; no notebook personal.

E2-01: precisión temporal en FE_DE_ERRATAS_E2_01.md; diferencia de tipos
corresponde a persistencia en externo2022. Enmienda congelada conservada.
