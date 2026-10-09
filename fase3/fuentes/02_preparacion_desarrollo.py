# %% [markdown]
# Preparación reproducible del panel y separación temporal

## Pregunta y vínculo con el objetivo

¿Puede el procedimiento iniciar modelos sobre la misma población agregada auditada, sin transformar la reserva en información de selección? El objetivo es estimar el promedio global de registros Saber 11 elegibles en un territorio-año dadas sus entradas de pobreza del mismo año. La unidad del análisis es la celda territorial, no un estudiante; el panel tiene 198 filas y 33 territorios, incluida Bogotá, en seis años. Los filtros de estudiante, libertad, disponibilidad de seis puntajes, colegio y grado 11 permanecen en la construcción de fase 1. No se leen ni publican microdatos.

La variable principal es $y_{dt}=\sum_{i\in(dt)}PUNT\_GLOBAL_i/n_{dt}$. Las medias no se redondean y no se reconstruyen desde asignaturas; las diferencias aritméticas documentadas de fuente se conservan. Dentro de una celda cada registro contribuyó igualmente; entre celdas el entrenamiento y las métricas dan igual peso a cada territorio-año. Esto define desempeño promedio agregado y no el desempeño del estudiante nacional típico.

## Datos, fuentes y método de control

La entrada única es auditoria/base_analitica_departamento_anio.csv, con SHA256 fijado en protocolo/fuentes/configuracion.py. Su diccionario y los 2.574 cotejos raw/final de auditoria/evidencia/actualizacion_20261008 respaldan población, sumas y denominadores. El protocolo v1.0 §§1–4 fija tres especificaciones: IPM, 15 tasas y ambas (1/15/16 columnas). Excluye año, códigos, conteos, INSE, puntajes de áreas, percentiles y derivados del resultado de X. IPM refiere personas y las tasas hogares; no inventamos un promedio de dimensiones.

Antes de cualquier ajuste se creó un entorno virtual sin paquetes del sistema, se comprobó su integridad con pip check, se construyeron los 67 estimadores sin entrenarlos y se exportaron sus defaults y todas las versiones a preparacion.json y requirements.lock.txt. La documentación de fase2 mencionaba sklearn 1.9.1 sin afirmar instalación: ahora esa versión sí está instalada. Las diferencias frente al plan anterior constan en fase3/decisiones.md antes de métricas. Las versiones actuales no reconstruyen las históricas.

El control detiene el trabajo si cambian huellas, población, llaves, rangos o particiones. La lectura estructural de 198 filas no calcula errores de reserva. Se separan inmediatamente desarrollo (2018, 2019, 2021, 2022) y reserva (2023, 2024); el buscador solo recibe desarrollo. Ventanas: 2018→2019, 2018+2019→2021 y 2018+2019+2021→2022. El salto sin 2020 se conserva.

## Supuestos y procedimiento

Los controles suponen que los archivos locales auditados son las entradas acordadas; no autentican una descarga oficial. Saber ubica el colegio, IPM ubica hogares residentes: su unión es ecológica. Las notas IPM (auditoria/evidencia/notas_ipm.csv, hojas y celdas citadas en protocolo §8) limitan comparabilidad entre años. Este control no demuestra causalidad ni representatividad de toda la juventud.

La siguiente celda localiza el proyecto desde raíz o notebooks/, verifica huellas del manifiesto previo, importa las funciones comunes y presenta únicamente conteos estructurales. No ejecuta scripts de fase2 que guardarían sobre evidencias anteriores.
# %%
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path.cwd()
if not (root / 'fase3').exists():
    root = root.parent
sys.path.insert(0, str(root / 'fase3/fuentes'))
from comun import panel, read, huella, cfg
prep = read('preparacion.json')
for name, expected in prep['entradas_sha256'].items():
    assert huella(root / name) == expected
assert sys.prefix != sys.base_prefix
assert prep['python'] == __import__('platform').python_version()
import importlib.metadata
for name, version in prep['paquetes'].items():
    assert importlib.metadata.version(name) == version
base = panel()
desarrollo = base[base.anio.isin(cfg.DESARROLLO)].copy()
reserva = base[base.anio.isin(cfg.REEVALUACION)].copy()
assert len(desarrollo) == 132 and len(reserva) == 66
print({'panel':len(base),'desarrollo':len(desarrollo),'reserva':len(reserva),
       'territorios':base.codigo_departamento.nunique(),'semilla':cfg.SEMILLA,
       'python':prep['python'],'sklearn':prep['paquetes']['scikit-learn']})
# %% [markdown]
## Interpretación del control ejecutado

La salida anterior es el resultado actual del control, no una expectativa de desempeño. Las 132 filas de desarrollo permiten tres validaciones de 33 celdas; las 66 de reserva quedan excluidas del ajuste y selección. La presencia de 33 territorios y las huellas verificadas mantiene el estimando acordado. La separación por años completos impide que una fila contemporánea del año validado aparezca en entrenamiento.

Que los controles pasen no significa que el modelo sea preciso. Solo habilita la comparación conforme al protocolo: ningún umbral de éxito predictivo se introduce aquí. La reserva fue examinada en estudios anteriores (prom.pdf pp.13–14,18,22 y nueva ivestigacion .pdf pp.5–7, ubicaciones verificadas en fase1), por lo que su evaluación posterior será reevaluación temporal. El siguiente notebook realiza la búsqueda finita y congela la selección usando solo desarrollo; esta etapa no incluye simulación ni contraste territorial.
