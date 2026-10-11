# Etapa1 v5 — diseño MAE y controles, sin piloto

Protocolo5.0.0. Fecha cliente2026-10-10, America/Bogota; semilla20261010.
Únicamente etapa1 autorizada y cerrada. Cero fits del panel real; presupuesto real
no iniciado; meta v5 no evaluada. No runner/ledger operativo, modelos reales ni
predicciones nuevas. Rama codex/objetivo3-v5-mae; commit exclusivamentev5,sin push.

Entradas: único panelv2 SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3;
derivadov4 SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc
solo cotejo. Grupos/funciones previas en lectura; CSV históricos/selecciones/hashes
v1/v2/v3/v4/media/tresOLS. Sin raw/fuentes adicionales ni modelos comparadores cargados.

Entorno: /tmp/icfes-v2-fase2-venv/bin/python, Python3.12.14,54paquetes exactos de
requirements.lock.txt,sklearn1.9.1,pip check. Comprobarlos antes de usar; falta/diferencia
exige documentar y consultar,sin instalación. Usar PYTHONDONTWRITEBYTECODE=1.

Orden realizado desde raíz:

1. Verificación exacta del entorno y cierre v4/etapa2/fuentes/cerrar.py --verificar
   en lectura. No llamar guardia histórica etapa1v4 ni cierres antiguos que escriban.
2. fuentes/preparar.py: una vez; partida/snapshot,entorno,registro documental,
   manifiestos,grilla36/defaults,reconstrucción propia tras cotejo íntegro en memoria,
   trazabilidad198cambios y referencias guardadas. Rechaza sobrescribir partida.
3. fuentes/controles.py: ocho grupos inventados/dobles,procesos hijos reales con
   inventados. Cada ejecución conserva directorio único dentro resultados/sinteticos.
4. fuentes/generar_notebook.py: notebook01_controles.ipynb desde fuente01_controles.py,
   nbformat valida y ejecuta realmente tres celdas con Python exec, no kernel.
   Una primera suite/notebook y otra tras reforzar orden JSON/particiones se conservan;
   evidencia final corresponde a mismos SHA de fuentes. No resultados ficticios.
5. fuentes/cerrar.py: conservación,congelación,manifiesto etapa1; no recongelar un
   cierre existente. fuentes/cerrar.py --verificar comprueba todo en lectura,sin
   generar outputs/ejecutar controles/fits. Cierre incluye antecedente íntegro v5.

Salidas: PROTOCOLO_V5.md; fuentes editables comunes/preflight/controles/notebook/
generador/cierre; requirements.lock.txt; reconstrucciones/panel_cambios.csv;
resultados/partida,entorno,integridad_antecedentes,estructura_real,trazabilidad198,
referencias_guardadas,configuraciones_congeladas,controles,verificacion_notebook,
sinteticos,lecturas,congelacion_previa,conservacion_final,manifiesto_cierre;
README/INFORME_CIERRE/registro_problemas; continuidad y prompt exclusivo etapa2.

Notebook muestra contratos/grupos/ventanas,historial inventado y suite sintética;
abrirlo es lectura,reejecutarlo crea pruebas separadas y exige cierre nuevo explícito.
No notebook de modelos/personal/simulación. Las interfaces etapa1 no son orquestación:
etapa2,con otra autorización,implementará/probará/congelará motor propio antes del
primer fit real. PROMPT_ETAPA2_NUEVA_SESION.md guardado,NO ejecutado.
Etapa3/revisión detallada y notebook personal únicamente si meta global satisfecha
con otra autorización. No avanzar; nunca simulación,objetivo4,ajuste final,descargas,
instalaciones o push en este alcance. Límites y fuentes en protocolo e informe.
