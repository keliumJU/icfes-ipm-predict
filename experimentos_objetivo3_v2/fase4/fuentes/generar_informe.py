from revision import *

def table(frame):
 cols=list(frame.columns);rows=['| '+' | '.join(cols)+' |','|'+'|'.join(['---']*len(cols))+'|']
 for row in frame.itertuples(index=False,name=None):rows.append('| '+' | '.join(f'{x:.9f}' if isinstance(x,float) else str(x) for x in row)+' |')
 return '\n'.join(rows)

def generar():
 out=F4/'resultados';m=csv(out/'metricas.csv');c=csv(out/'comparaciones_v1.csv');pairs=csv(out/'diferencias_emparejadas.csv');v=read(out/'verificacion.json');nb=read(out/'verificacion_notebook.json')
 q=m[(m.periodo=='2021-2025')&(m.ambito=='conjunto')]
 partial=m[(m.ambito=='conjunto')&m.procedimiento.isin(['procedimiento_v2','referencia_v1'])]
 annual=m[(m.periodo=='2021-2025')&(m.ambito=='anual')&m.procedimiento.isin(['procedimiento_v2','referencia_v1'])]
 deterioration=c[(c.periodo=='2021-2025')&(c.procedimiento=='procedimiento_v2')&(c.ambito=='territorial')&c.deteriora_mae]
 improvements=[]
 for period in ('2021-2024','2025'):
  z=partial[partial.periodo==period].set_index('procedimiento');a=z.loc['procedimiento_v2','mae'];b=z.loc['referencia_v1','mae'];improvements.append(f'{period}: {100*(b-a)/b:.9f}%')
 text=f'''# Revisión del piloto y notebook personal — fase 4

Fecha cliente: 2026-10-10, America/Bogota. Fase 4 cerrada localmente.
Partida real `b37a2f338f0708958a412f5a0efa09f33861322b`, igual al cierre conocido fase3;
rama `codex/objetivo3-v2-piloto`, Git inicialmente limpio. No diferencias ni cambios
previos que conservar. Únicamente fase4 y continuidad v2 se actualizan.
Plan consultado: exclusivamente fase4, líneas116–134 (encabezado y requisitos hasta
el cierre de fase; el encabezado siguiente se usó solo como delimitador).
PDF efectivamente leídos: ninguno, cero páginas. No nuevas consultas externas.

## Condición exacta y resultado

Se confirma desde CSV: MAE v2 **{v['mae_v2']}**, MAE v1 fija reentrenada
**{v['mae_v1']}**. Mejora exacta **{v['condicion']['mejora']}%**, con denominador
positivo y las mismas165 llaves de33 territorios ×5 años. Supera el umbral práctico≥5%
sin redondeo adicional, sin exigir tres-de-cinco-años ni sustituir el procedimiento
global por otro ganador elegido desde errores externos. **Notebook personal entregado.**
Fuente: resultados/verificacion.json; cálculo reutilizado `condicion_personal` de fase2.

## Métricas conjuntas de todos los procedimientos

Fuente: resultados/metricas.csv, periodo2021-2025, ámbito conjunto.
MAE/RMSE/sesgo en puntos; R² adimensional. Sesgo=predicción−observado.

{table(q[['procedimiento','n','mae','rmse','sesgo','r2']])}

Comparaciones v2−media, tres OLS y v1 en resultados/comparaciones_referencias.csv,
conjuntas/anuales/territoriales y para los tres periodos. Delta negativo de MAE/RMSE
favorece v2; delta de sesgo indica dirección y requiere comparar su magnitud para
hablar de reducción. Especificaciones comparadas descriptivamente; no se cambia la principal.

## Separación 2021–2024 y 2025

{table(partial[['periodo','procedimiento','n','mae','rmse','sesgo','r2']])}

Mejoras descriptivas separadas: {'; '.join(improvements)}. No sustituyen el umbral
principal fijado para2021–2025. Fuente: resultados/metricas.csv, ámbito conjunto.
Cada periodo concatena errores; RMSE no promedia raíces. La aportación de2025 al
MAE conjunto es exactamente una quinta parte por sus33 de165 filas, sin peso por
conteos estudiantiles. El MAE conjunto combina4/5 del MAE2021–2024 y1/5 del MAE2025.
2025 continúa exploratorio, sin reserva inédita; publicación del IPM posterior al año
observado impide presentar este análisis retrospectivo como pronóstico disponible entonces.

## Comparación anual y deterioros territoriales

{table(annual[['grupo','procedimiento','n','mae','rmse','sesgo','r2']])}

Cero años deterioran el MAE y ocho territorios lo deterioran frente a v1:

{table(deterioration[['grupo','delta_mae','delta_rmse']])}

Códigos corresponden a geografía del colegio, según panel/fase2. Fuente exacta:
resultados/deterioros_v2.csv (incluye también filas sin deterioro). En código13 el MAE
empeora y RMSE mejora; los criterios resumen pérdidas diferentes, sin contradicción.
Todos los33 territorios y nueve procedimientos se conservan en metricas.csv. R²
territorial se calcula contra la media de cinco observados del territorio: baja variación
puede producir R² negativo. Para2025 territorial n=1, R² es no definido/celda vacía,
no cero. No inferir significancia a partir de pocos años o del umbral práctico.

## 165 diferencias emparejadas

Archivo completo: resultados/diferencias_emparejadas.csv, llaves código−año; conserva
IDs/ajustes/selección_sha256/y/predicciones y errores de ambos procedimientos.
- `delta_error_firmado` = e_v2−e_v1, puntos: describe dirección, no ordena exactitud.
- `delta_error_absoluto` = |e_v2|−|e_v1|, puntos: positivo indica peor error absoluto.
- `delta_error_cuadratico` = e_v2²−e_v1², puntos²: positivo indica peor pérdida cuadrática.

Deterioran{int((pairs.delta_error_absoluto>0).sum())} pares; mejora agregada no implica
mejora uniforme. Promediar delta absoluto equivale a diferencia de MAE; promedio delta
cuadrático equivale a diferencia de MSE, no de RMSE. No pruebas nuevas de significancia.
Gráficos: resultados/mae_anual.png, delta_mae_territorial.png y diferencias_emparejadas.png.
Fuentes: revisión.py `independent` importado de fase3, `presentar` y CSV completos.

## Auditoría, referencias y trazabilidad

Manifiestos fase2/fase3 y congelaciones cotejados sin regenerarlos; siete fuentes
originales cotejadas por SHA256, sin censo raw. La continuidad incluida en cada manifiesto
se verifica en su commit de cierre, porque su actualización posterior está autorizada;
no se usa esa excepción para otros archivos. Evidencia: integridad_consulta.json,
partida.json y conservacion_final.json. Registro de conservación fase3 leído y contrastado
con su snapshot de versionados y fuentes. Parámetros/defaults100, referencia v1 fija,
lock íntegro, Python3.12.14 y pip check comprobados; semilla20261010.

Auditoría actual de1552 registros y51216 predicciones de artefactos: huellas de modelos
(sin cargarlos ni ajustarlos), CSV y configuración/entorno;33 filas/validación, llaves
únicas, observados contra panel, anterioridad y años exactos; medias/varianzas/escalas
solo entrenamiento;500 puntuaciones internas recálculo y selección global/por especificación
según bandas congeladas. Verifica orden del ledger, roles y vínculo selección−externo
por SHA256. Fecha registrada y código congelado apoyan secuencia, pero la huella sola
no certifica una cronología física externa. Diez repeticiones históricas cotejadas
nuevamente desde CSV: diferencia máxima0. No nuevas repeticiones de entrenamiento.

1500 internos+42 externos+10 repeticiones, cero fallos;49.500 internas, nueve procedimientos
con165 externas cada uno. Consumo histórico verificado{v['segundos_piloto']} de7200s;
esta fase añade0 ajustes y no consume saldo. Enmiendas E3-01(regex temporal completa)
y E3-02(cota descriptiva1555) conservadas; no cambios a100 candidatos ni presupuesto.
Evidencia de recálculo actual: resultados/verificacion.json, distinta de ejecución fase3.

## Notebook entregado y reproducción voluntaria

notebooks/01_notebook_personal.ipynb desde fuentes/01_notebook_personal.py y generador
Python/nbformat. **{nb['celdas_codigo_ejecutadas']} celdas de código ejecutadas realmente en modo verificar
mediante Python exec**, con3 gráficos incrustados; sin kernel Jupyter ni entrenamiento.
Fuente/huellas y modo documentados en resultados/verificacion_notebook.json. Recalcula
controles/tablas/gráficos en resultados/notebook_verificacion, separado de fase3.

El modo opcional lanza fuentes/reejecutar.py en un subproceso y reutiliza Runner/presupuesto/
construcción/selección compartidos, configuración congelada y semilla fija. Guarda piloto
nuevo en fase4/reproducciones/ con nombre único y ledger propio, máximo7200s para todo
el piloto nuevo. Estimación observada~25.7min, sin garantía en otro equipo. No reutiliza
modelos ni reinicia el ledger original; los resultados nuevos se verifican por separado.
Esta capacidad se inspeccionó/compiló; **no se ejecutó un reentrenamiento completo**.
Ante fallo/interrupción conservar estado/ledger; no afirmar éxito ni reanudar borrándolos.
No se ajusta modelo final con todos los años ni se genera simulación.

## Impacto, alternativas y límites

La mejora conjunta habilita entrega; alternativa resuelta: conservar global predefinido
sin seleccionar ambas retrospectivamente. Ocho territorios y61 pares con deterioro
impiden afirmar beneficio uniforme; alternativa resuelta: tablas completas y gráficos,
sin modificar población, ponderación, variables, criterio ni exclusiones.

Persisten casos completos/Guainía(238 frente404, diferencia descriptiva21.012106 puntos:
fase1/resultados/diagnostico_medias_disponibles.csv), procedencia local sin autenticación
independiente, comparabilidad IPM(protocolo congelado§8), población hogares versus alumnos,
residencia versus colegio/enlace ecológico, dependencia temporal/territorial y pocos años.
Son advertencias activas; no efectos causales ni sesgos causalmente cuantificados.
Antecedentes59/esquema82, causa antigua20212 y fórmula global desconocida siguen archivados
con evidencia/motivo heredados, sin nueva evidencia de impacto ni reapertura.

No quedan controles indispensables pendientes de fase4. Reejecución voluntaria no realizada
es una opción del notebook, no prueba pendiente para cerrar esta revisión. Nueva fase,
simulación/objetivo4, ajuste final, descargas o push requieren autorización posterior.
Cierre: resultados/manifiesto_cierre.json y conservación; commit local descriptivo
identificado fuera del manifiesto para evitar autorreferencia.
'''
 (F4/'INFORME_REVISION.md').write_text(text)
if __name__=='__main__':generar()
