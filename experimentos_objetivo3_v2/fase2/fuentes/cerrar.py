"""Conservación, informe ejecutado y manifiesto. No ejecuta modelos ni fases anteriores."""
import sys
sys.dont_write_bytecode=True
import json,subprocess
import configuracion as cfg
from comun import sha,guardar
from verificar import huellas

def cerrar():
 out=cfg.F2/'resultados'
 initial=json.loads((out/'integridad_inicial.json').read_text())
 continuity='experimentos_objetivo3_v2/CONTINUIDAD_V2.md'
 preserved=[]
 for p,h in initial['snapshot_versionados'].items():
  if p!=continuity:assert sha(cfg.ROOT/p)==h,p;preserved.append(p)
 for p,h in initial['fuentes'].items():assert sha(cfg.ROOT/p)==h,p
 changes=subprocess.check_output(['git','diff','--name-only'],cwd=cfg.ROOT).decode().splitlines()
 assert set(changes)<={continuity},changes
 assert subprocess.check_output(['git','branch','--show-current'],cwd=cfg.ROOT).decode().strip()==initial['rama']
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=cfg.ROOT).decode().strip()==initial['commit_partida']
 freeze=json.loads((out/'congelacion_previa.json').read_text())
 assert sha(cfg.F2/'PROTOCOLO_V2.md')==freeze['protocolo_sha256']
 assert sha(out/'configuraciones_congeladas.json')==freeze['configuraciones_sha256']
 for p,h in freeze['fuentes_sha256'].items():assert sha(cfg.ROOT/p)==h,p
 reports=[json.loads((out/name).read_text()) for name in ('controles.json','controles_notebook.json')]
 assert all(r['aprobado'] and r['controles_aprobados']==9 and r['predicciones_panel']==r['ajustes_candidatos_panel']==0 for r in reports)
 nb=json.loads((out/'verificacion_notebook.json').read_text())
 assert nb['ejecucion_real_kernel'] and nb['nbformat']
 assert nb['notebook_sha256']==sha(cfg.F2/'notebooks/01_protocolo_verificacion.ipynb')
 assert nb['fuente_sha256']==sha(cfg.F2/'fuentes/01_protocolo_verificacion.py')
 assert nb['controles_notebook_sha256']==sha(out/'controles_notebook.json')
 histories=huellas();guardar(out/'huellas_anteriores.json',histories)
 guardar(out/'conservacion_final.json',dict(aprobado=True,commit_partida=initial['commit_partida'],
  diferencia_cierre_conocido=False,archivos_versionados_intactos=len(preserved),fuentes_intactas=len(initial['fuentes']),
  excepcion_autorizada=dict(archivo=continuity,antes=initial['snapshot_versionados'][continuity],despues=sha(cfg.ROOT/continuity)),
  fase1_intacta=True,originales_intactos=True,huellas_manifiestos=histories['cotejos'],pdf_leidos=[],
  ajustes_candidatos_panel=0,predicciones_panel=0,simulaciones=0,notebook_personal_entregado=False,push=False))
 rows=['| Control | Estado | Evidencia |','|---|---|---|']
 for c in reports[0]['controles']:rows.append(f"| {c['control']}. {c['nombre']} | Aprobado | resultados/controles.json, control {c['control']} |")
 report=f'''# Informe de cierre — exclusivamente fase 2 v2

2026-10-10, America/Bogota. Partida real `{initial['commit_partida']}` y cierre conocido idénticos;
Git inicialmente limpio, rama `{initial['rama']}` reutilizada. Sin resultados predictivos reales nuevos.

Protocolo v2.0.2 y exactamente 100 configuraciones congelados antes del piloto.
100 estimadores construidos para exportar defaults completos, **cero candidatos ajustados**.
Referencia v1 identificada históricamente, sin reentrenar. Su semilla histórica queda como antecedente; el futuro reentrenamiento usa 20261010.
Cinco evaluaciones externas futuras 2021–2025, búsqueda interna temporal y 7200 segundos
acumulados para ajustes, referencias, fallos y repeticiones. Condición de notebook personal:
MAE conjunto al menos 5% menor frente a v1 reentrenada, procedimiento completo.
Todavía no se puede comprobar esa condición ni atribuir mejora. No requisito de tres años.

## Comprobaciones ejecutadas

{chr(10).join(rows)}

Los nueve controles se ejecutaron tanto por Python como en kernel real del notebook de
verificación ({nb['celdas_codigo_ejecutadas']} celdas de código), válido con nbformat;
resultados/controles_notebook.json y verificacion_notebook.json. Los controles de panel
confirman 231 filas, 33 territorios por año y las 198 históricas exactas/prefijo literal.
La unión estructural de columnas de ese mismo panel rechaza duplicados, llaves sin
correspondencia y entradas ausentes; no se importa el candidato ni se reconstruye raw.

Escalado y separación temporal usan pipelines con doble Espia sobre datos sintéticos;
el extremo externo 1e100 no altera media/escala. Agregación: media conocida 200,
media anual ponderada por registros 250, nulos rechazados sin cero. Métricas sintéticas
de tres predicciones guardadas: MAE 1, RMSE raíz(5/3), sesgo −1/3, R² −1.5,
recalculadas independientemente con biblioteca estándar. Esas cifras **no describen el panel**.
Presupuesto: doble con reloj controlado, persistencia/repeticiones/interrupción conservadora
y terminación real de proceso lento al agotar 1.5 segundos. Duración observada completa
(incluida latencia de terminación) en presupuesto_sintetico.json; no es tiempo de piloto.
Presupuesto de entrenamiento del panel consumido: 0 segundos.

## Hallazgos, resolución y conservación

El control inicial rechazó 35 cadenas territoriales por 05/5 y 08/8 entre histórico y
2025. Enmienda técnica previa a predicciones: normalizar solo en memoria a dos dígitos,
validar 33 códigos conocidos, sin modificar CSV. Evidencia fallida y congelación inicial
conservadas en resultados/antecedentes/. No discrepancia territorial ni cambio poblacional.

La interpretación inicial de semilla del comparador se corrigió a 20261010 por instrucción
explícita del usuario, antes de cualquier ajuste real; estructura ganadora v1 intacta.
La ejecución inicial del kernel quedó bloqueada por sockets locales del aislamiento;
se interrumpió y repitió fuera del aislamiento con éxito, sin cambiar controles.

El entorno transitorio v1 faltaba. Se recuperaron offline sus paquetes exactos desde
caché local, Python 3.12.14/sklearn 1.9.1. Primer intento falló por etiquetas wheel
abreviadas; se recuperaron todas las etiquetas originales y se instaló sin red. pip check
aprobado, versiones reales y ejecutable en entorno.json; requirements.lock.txt congelado.
No se buscaron versiones según métricas. Registro de problemas distingue estos controles
resueltos de limitaciones y antecedentes archivados.

Se cotejaron {histories['cotejos']} entradas de manifiestos de fase1 v2 y v1 pertinentes;
las excepciones históricas de continuidad/informe se comprobaron en sus commits.
{len(preserved)} archivos versionados previos intactos y siete fuentes intactas; única
actualización previa autorizada: continuidad v2. Evidencia conservación_final.json.
No alteraciones de fase1, originales, continuidad objetivo3 o .gitignore.
**PDF consultados ahora: ninguno, cero páginas.** Sin descargas de datos, nuevo censo raw,
simulaciones, objetivo4, entrenamiento real, notebook personal ni push.

Persisten casos completos/Guainía, procedencia local sin autenticación independiente,
comparabilidad IPM, enlace ecológico y dependencia. No se afirman efectos causales ni
significancia estadística del umbral; 2025 no reserva inédita. Antecedentes históricos
sin impacto nuevo se mantienen archivados (registro_problemas.md).

Pendiente: autorización expresa de fase3 para implementar orquestación y ejecutar piloto
con estas funciones, huellas y reglas; producir informe completo incluso sin mejora.
No hay control indispensable de fase2 pendiente. Commit local se informa fuera del
manifiesto para evitar autorreferencia; no hay autorización de fase3 implícita en el cierre.
'''
 (cfg.F2/'INFORME_CIERRE.md').write_text(report)
 files={str(p.relative_to(cfg.ROOT)):sha(p) for p in sorted(cfg.F2.rglob('*'))
        if p.is_file() and p.name!='manifiesto_cierre.json' and '__pycache__' not in p.parts}
 files[continuity]=sha(cfg.ROOT/continuity)
 guardar(out/'manifiesto_cierre.json',dict(fase='v2/fase2',fecha_cliente='2026-10-10',commit_partida=initial['commit_partida'],
  entregables_sha256=files,controles_aprobados=9,kernel_real=True,ajustes_panel=0,predicciones_panel=0,pdf_leidos=[],push=False))
 print(f'Cierre conservado y manifiesto de {len(files)} archivos.')
if __name__=='__main__':cerrar()
