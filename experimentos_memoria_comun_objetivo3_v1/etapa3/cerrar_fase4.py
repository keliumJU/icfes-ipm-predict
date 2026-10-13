"""Cierre propio fase4; --verificar solo lectura, sin imports operativos/fits."""
from auditor import *
import nbformat

def environment_readonly():
 e=load(HERE/'ENTORNO_FASE4.json')
 actual={d.metadata['Name'].lower().replace('_','-'):d.version for d in md.distributions()}
 check(platform.python_version()=='3.12.14' and {k:v for k,v in actual.items() if k!='pip'}==e['lock'] and len(e['lock'])==54,'entorno cierre')
 check(os.environ.get('PYTHONDONTWRITEBYTECODE')=='1' and subprocess.run([sys.executable,'-m','pip','check'],capture_output=True).returncode==0,'pipcheck/bytecode cierre')
 return True

def conservation():
 snap=load(HERE/'PARTIDA_FASE4.json'); continuity=str((BASE/'CONTINUIDAD_EXPERIMENTAL.md').relative_to(ROOT)); bad=[]
 for s,h in snap['protegidos'].items():
  p=HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md' if s==continuity else ROOT/s
  try:
   if sha(p)!=h: bad.append(s)
  except OSError: bad.append(s)
 check(not bad,'conservación '+str(bad))
 current=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
 prefix=str(HERE.relative_to(ROOT))+'/'
 foreign=[s for s in current if s and s not in snap['protegidos'] and not s.startswith(prefix)]
 check(not foreign,'ajenos nuevos '+str(foreign))
 check(command('git','rev-parse','HEAD')==load(HERE/'PREFLIGHT_FASE4.json')['head'] and command('git','branch','--show-current')==load(HERE/'PREFLIGHT_FASE4.json')['rama'] and not command('git','diff','--name-only','HEAD'),'Git conservación')
 # Manifiesto fase3 original compara su continuidad con la copia histórica íntegra.
 m=load(E2/'MANIFIESTO_FASE3.json')
 check(sha(HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md')==m['continuidad_actual_sha256'],'continuidad fase3 original')
 for s,h in m['entregables_sha256'].items(): check(sha(E2/s)==h,'fase3 final intacta '+s)
 return {'aprobado':True,'protegidos':len(snap['protegidos']),'diferencias':bad,'ajenos_nuevos':foreign,'raw':'ignorado; sin lectura/censo/escritura','continuidad_fase3_preservada_sha256':sha(HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md'),'ledger_original_sha256':sha(E2/'resultados/piloto/ledger.json'),'nota':'verificación propia fase4 valida manifiesto fase3 y continuidad preservada; el verificador histórico exige continuidad/inventario de su cierre y no se reescribe'}

def notebook_readonly():
 n=load(HERE/'ACEPTACION_NOTEBOOK.json'); p=HERE/'01_auditoria_resultados.ipynb'
 check(n['aprobado'] and n['notebook_sha256']==sha(p) and n['fuente_sha256']==sha(HERE/'notebook_resultados.py') and n['generador_sha256']==sha(HERE/'generar_notebook.py'),'huellas notebook')
 nb=nbformat.read(p,as_version=4); nbformat.validate(nb); code=[c for c in nb.cells if c.cell_type=='code']
 check([c.execution_count for c in code]==list(range(1,7)) and all(c.outputs and all(o.output_type!='error' for o in c.outputs) for c in code),'ejecución6celdas')
 return True

def verify():
 m=load(HERE/'MANIFIESTO_FASE4.json')
 for s,h in m['entregables_sha256'].items(): check(sha(HERE/s)==h,'manifiesto fase4 '+s)
 actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
 check(actual-set(m['exclusiones_autorreferencia'])==set(m['entregables_sha256']),'inventario etapa3 exacto')
 check(sha(BASE/'CONTINUIDAD_EXPERIMENTAL.md')==m['continuidad_actual_sha256'],'continuidad fase4')
 environment_readonly(); notebook_readonly(); cons=conservation(); acceptance=load(HERE/'ACEPTACION_FASE4.json')
 check(acceptance['completa'] and all(acceptance['controles'].values()) and not acceptance['pendientes_indispensables'],'aceptación fase4')
 result={'aprobado':True,'completa':True,'huellas':len(m['entregables_sha256']),'conservacion':cons,'fits_nuevos':0,'meta_5_satisfecha':False,'modo':'solo lectura; no fits/cargas/escrituras'}
 print(json.dumps(result,ensure_ascii=False)); return result

def main():
 check(not (HERE/'MANIFIESTO_FASE4.json').exists(),'cierre existente; usar --verificar')
 environment_readonly(); notebook_readonly(); cons=conservation()
 for s in ['PREFLIGHT_FASE4.json','PRUEBAS_AUDITOR.json','AUDITORIA_INDEPENDIENTE.json','AUDITORIA_COMPLEMENTARIA.json']: check(load(HERE/s)['aprobado'],s)
 # Registra ubicaciones y alcance; no relee otras secciones del plan.
 reading={}
 for s in ['AGENTS.md','experimentos_memoria_comun_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md','experimentos_memoria_comun_objetivo3_v1/etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md','diseno_memoria_comun_objetivo3_v1/PROTOCOLO_FASE1.md','diseno_memoria_comun_objetivo3_v1/ESPECIFICACION_DOCUMENTAL.json','experimentos_memoria_comun_objetivo3_v1/etapa1/PROTOCOLO_IMPLEMENTACION.md','experimentos_memoria_comun_objetivo3_v1/etapa2/PROTOCOLO_ETAPA2.md','diseno_memoria_comun_objetivo3_v1/CONTINUIDAD_DISENO.md','experimentos_temporales_objetivo3_v1/CONTINUIDAD_EXPERIMENTAL.md']:
  p=ROOT/s; text=p.read_text(); reading[s]={'revisado':'completo','lineas':len(text.splitlines()),'sha256':sha(p)}
 reading['diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md']={'revisado':'vigente líneas1–106; histórico incompleto posterior archivado, no estado actual','sha256':sha(ROOT/'diagnostico_objetivo3_v1/CONTINUIDAD_DIAGNOSTICO.md')}
 reading['experimentos_objetivo3_v5/CONTINUIDAD_V5.md']={'revisado':'vigente hasta separación de antecedente; históricoetapa1 cotejado en commit real','sha256':sha(ROOT/'experimentos_objetivo3_v5/CONTINUIDAD_V5.md')}
 plan=ROOT/'diseno_memoria_comun_objetivo3_v1/PLAN_FASES.md'; lines=plan.read_text().splitlines(); start=next(i for i,l in enumerate(lines) if l.startswith('### Fase4')); end=next(i for i in range(start+1,len(lines)) if lines[i].startswith('## '))
 reading[str(plan.relative_to(ROOT))]={'revisado_autorizado':'decisiones comunes líneas1–15 y fase4 líneas'+str(start+1)+'–'+str(end),'texto_fase4':'\n'.join(lines[start:end]),'incidencia':'apertura inicial accidental completa; documentada, no autoriza otras fases','sha256':sha(plan)}
 save('LECTURAS_FASE4.json',{'lecturas':reading,'PDF':{'paginas_revisadas':0,'pendiente':'No lectura nueva de PDFs requerida en esta fase; afirmaciones históricas atribuidas a archivos originales, no PDFs releídos'},'fuentes_nuevas':0,'web':0,'operativos':'solo lectura textual de formato de contexto, panel y cierres/generador; no importación en cotejos','continuidades_historicas':'v5 commit109797407d75d2097e5b71f8bcef3fc266bc61d2;temporal texto/huella partida;fase2 copia íntegra y manifiesto original;fase3 copia previa propia','pendiente_cientifico':'autenticidad, temporalidad, confirmación y experimentos futuros'})
 save('REVISION_GRAFICOS.json',{'aprobado':True,'metodo':'inspección visual de3PNG en view_image tras generación; ejes/leyendas/unidades/n legibles sin recortes','archivos':{p.name:sha(p) for p in (HERE/'graficos').glob('*.png')}})
 save('CONSERVACION_FASE4.json',cons)
 save('PENDIENTES_FASE4.json',{'indispensables_tecnicos':[],'cientificos':['autenticidad local no resuelta','fechas de publicación/disponibilidad no autenticadas','confirmación temporal independiente','aporte del rezago frente a nivel histórico','causa del coeficiente0 y regularización'],'autorizacion_futura':'protocolo y envío separados; ninguna implementación ni avance automático','meta_5_satisfecha':False})
 (HERE/'README.md').write_text('''# Fase4 — completa técnicamente; meta5% no satisfecha

2026-10-11 America/Bogota. Alcance exclusivo auditoría independiente/interpretación exploratoria/cierre de guardados. Cero fits/cargas/instalaciones/commit/push. Informe principal: INFORME_FASE4.md. Tablas completas: tablas/ (10CSV). Gráficos: graficos/ (3PNG revisados). Notebook:01_auditoria_resultados.ipynb,6celdas realmente ejecutadas/nbformat, desde notebook_resultados.py y generar_notebook.py.

Orden realizado con /tmp/icfes-v2-fase2-venv/bin/python y PYTHONDONTWRITEBYTECODE=1: verificadorfase3 en lectura → auditor.py --preflight → auditor.py --pruebas → analizar.py → complementar.py → documentar.py → generar_notebook.py → cerrar_fase4.py → cerrar_fase4.py --verificar. Incidencias propias resueltas/preservadas en antecedentes y REGISTRO_HALLAZGOS.md. No repetir generadores sobre artefactos existentes; el cierre se verifica solo con --verificar. Notebook solo lectura y cálculo de guardados, sin escritura.

Entradas: fuentev2/derivadov5, diseño y etapa1 congelados, etapa2 guardada, continuidades históricas reales/preservadas. Versiones/semilla: ENTORNO_FASE4.json; Python3.12.14/sklearn1.9.1/54lock/pipcheck/semilla20261010. Salidas: informe/tablas/gráficos/auditorías/pruebas/propuestas/lecturas/conservación/aceptación/manifiesto/continuidad. Manifestación de fase3 original queda intacta y se coteja con su continuidad preservada; el verificador histórico presupone su inventario/continuidad original.

GlobalMAE3.3676098407589707 frente persistencia3.429267191379531,mejora1.7979745286559843%;meta5%NO. Memoria mejora12.392390281511053%descriptivo, coeficiente rezago0 en11ajustes; no rescate del primario ni dinámica confirmada. Correccióncoef/intercept0 en10ajustes. Global mejora solo2025,18territorios mejoran/15empeoran.

Todos2021–2025vistos,exploratorio sin confirmación independiente/causalidad. Procedencia local,Guainía,IPMhogares-alumnos,colegio-residencia,ecología,dependencia/pocos años preservados. Pendientes científicos y propuestas futuras requieren protocolo/autorización separados. Ninguna siguiente fase automática.
''')
 acceptance={'completa':True,'aceptacion':'técnica de auditoría; no confirmación científica','controles':{'entrada_fases1_2_3':True,'entorno_exacto':True,'auditor_independiente':True,'pruebas_inventadas':True,'matrices_fechas_scales_coeficientes':True,'cobertura_seleccion_linaje_global':True,'CSV_exactos':True,'ledger_cerrado_historia':True,'referencias165':True,'metricas_fsum_primario_fijo':True,'graficos_revisados':True,'notebook6celdas_validado':True,'conservacion':True},'pendientes_indispensables':[],'fits_nuevos':0,'modelos_cargados':0,'meta_5_satisfecha':False,'experimento_futuro_autorizado':False}
 save('ACEPTACION_FASE4.json',acceptance)
 continuity='''# Continuidad experimental memoria/común — fase4 COMPLETA TÉCNICAMENTE

2026-10-11 America/Bogota. Usuario envió exclusivamente fase4, luego «continua» sin ampliar alcance. Auditoría independiente/interpretación/cierre sobre guardados;0fits nuevos/0cargas/0instalaciones/0commit/push; no modelo final/notebook personal/simulación/objetivo4/nuevo experimento/avance automático.

Continuidad fase3 anterior íntegra preservada en etapa3/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md, SHA'''+sha(HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md')+''', coincide MANIFIESTO_FASE3 original. Fase2 histórica íntegra en etapa2/antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE2.md contra manifiesto original; no exigir al inventario histórico representar fase3/4. Diseño fase1 aprobado por envío fase2 y piloto completo revalidados. Primer comando cerrar_fase3.py --verificar aprobado1018huellas/31245protegidos. Etapa1/etapa2/diseño/originales/ledgers intactos; etapa3 propia y esta continuidad únicos cambios.

GitHEAD75c3a25182af363f47b0d743820f99084e18fed5/asunto etapa2v5cerrarpiloto36MAEyauditoriasinmejora/rama codex/objetivo3-v5-mae/ascendencia/sin posteriores versionados. Continuidadv5etapa1 en commitreal109797407d75d2097e5b71f8bcef3fc266bc61d2;temporal únicamente texto/huella partidaetapa2. CONSERVACION_FASE4 y PARTIDA_FASE4 protegen todo listado Git sin raw. Verificador propio final coteja etapa2/manifiesto original con continuidadfase3 preservada; el verificador histórico presupone su continuidad/inventario, no modificarlo para fase4.

Python3.12.14/sklearn1.9.1/54lock/pipcheck0/PYTHONDONTWRITEBYTECODE=1/semilla20261010 exactos antes cálculos y cierre; sin aleatoriedad nueva. Fuentev2SHA6cd37c9784f7953de09ba3dec40d0898e0902b907a5448dbf3e850593d8ddfb3 y derivadov5SHAaa761437a94beb1504068d2c5fb9ace0eb03ea84d4d2f182d58832ea21cbe0dc intactos. Falta/diferencia futura exige documentar/consultar sin sustituir/instalar.

Decisiones usuario/documentales conservadas: población ESTUDIANTE/no libertadS/grado11/seis puntajes presentes positivos/sin calendario/media recibida/geografía colegio/2020excluido/2018historial/d sin anualizar/2021externa fija/165pares/igualpeso/meta5%.2019historial sin respuesta supervisada conlag inexistente. Cuatro candidatos0/1/1/2entradas, componentes propios/separados, defaults congelados/sin recencia/efectos por código; común1fila/año, territoriales33, ceroaños respalda sinfit/uno permite. Selección solo internas MAE≤mínimo+0.1→RMSE dentro pool≤mínimo+0.1→entradas→orden. Primario global fijo sin rescate por memoria. Ningún cambio material de criterios.

Recálculos ACTUALES de guardados: MAEpersistencia3.429267191379531/RMSE4.314920647368904;MAEglobal3.3676098407589707/RMSE4.306243910848592/mejora1.7979745286559843%,meta5%NO. MAEmemoria3.004299017227967/mejora12.392390281511053%solo exploratorio. Sin discrepancias con antecedentes fase3. Global persistencia2021–2024/memoria2025;empate2022/rechazoMAE2023/filtroRMSE2024 reconstruidos. Referenciasv3persistencia/v5global/recenciaglobal mismas165llaves/observados/predicciones;una referencia, no evidencias independientes.

Auditoría propia sin importar selector/constructores/runners ni deserializar:231niveles/198cambios, d/c/r/X/y/llaves/fechas/inputs/unidades/defaults/semilla/contextos/scaler/predicciones.1320internas/16registros/825externas/528únicas/1320linajes y menor externo/5global checks exactos. CSVexactos/intfloat0/rechazo1e-11;repeticiónatol1e-10/rtol0;scaler aritméticoatol1e-12/rtol0. Ledger HISTÓRICO41fits=24internos+16externos+1repetición;0fallos/retries;58.63946153299912s/7200/cota46.95snapshots0000–0094,arranque durable pending/serial/terminación/cierre;sin reapertura/saldo reutilizado.

Hallazgos actuales:11ajustes memoria6internos+4externos+1repetición coefrezago0;predicciones constante histórica+previo,intercepto en intervalo de medianas y no siempre mediana promediada. Beneficio de nivel no prueba relación predictiva entre cambios; causa exclusivaalpha1 no probada.10correcciones coef/intercept0;común y común+corrección165externas exactamente iguales bajo configuración, no inutilidad universal. Global mejora íntegramente2025:18territorios mejoran/15empeoran;132pares previos idénticos persistencia. Dirección27/33en2025,sesgo+1.364113221808658puntos;no confundir signo/magnitud. Hipótesis selección acumulada tardía y referencia simple/rezago/regularización solo documentales;PROPUESTAS_FUTURAS requiere protocolo y autorización separados,ninguno implementado.

Entregables etapa3:INFORME_FASE4/tablas10CSV completos/3PNG unidades-n revisados/notebook01_auditoria_resultados6celdas realmente ejecutadasexecPython/nbformat desde fuentes editables+generador/auditorías/pruebas/registro-hallazgos/propuestas/lecturas/aceptación/conservación/manifiesto/verificación/pendientes. Incidencias propias archivadas y resueltas en REGISTRO_HALLAZGOS:lectura inicial plan completo accidental/salidas truncadas;auditor orden-normalización-etiqueta;complemento pending y conteo0000. No originales o criterios alterados ni controles indispensables irresueltos.

Aceptación técnica completa;pendientes indispensables[]. Pendientes científicos autenticidad/disponibilidad/confirmación independiente/aporte del rezago-causa regularización, fuera fase autorizada. Todos2021–2025vistos:exploratorio,sin causalidad/confirmación ni pronóstico anticipado demostrado. Procedencia local no autenticada;Guainía238vs404/21.012105832431985puntos HISTÓRICO v2 diagnóstico_medias_disponibles filas57y90;IPMhogares-alumnos/colegio-residencia/ecología/dependencia/pocos años. La aceptación técnica no resuelve estas advertencias;archivados históricos no reabiertos sin evidencia nueva.

Verificar en lectura:PYTHONDONTWRITEBYTECODE=1 /tmp/icfes-v2-fase2-venv/bin/python experimentos_memoria_comun_objetivo3_v1/etapa3/cerrar_fase4.py --verificar. No regenerar ni ejecutar futuras propuestas automáticamente.
'''
 (BASE/'CONTINUIDAD_EXPERIMENTAL.md').write_text(continuity)
 excluded=['MANIFIESTO_FASE4.json','VERIFICACION_MANIFIESTO_FASE4.json']
 mapping={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and p.relative_to(HERE).as_posix() not in excluded}
 save('MANIFIESTO_FASE4.json',{'completa':True,'entregables_sha256':mapping,'exclusiones_autorreferencia':excluded,'continuidad_actual_sha256':sha(BASE/'CONTINUIDAD_EXPERIMENTAL.md'),'continuidad_fase3_preservada_sha256':sha(HERE/'antecedentes/CONTINUIDAD_EXPERIMENTAL_FASE3.md'),'fits_nuevos':0,'meta_5_satisfecha':False})
 result=verify(); save('VERIFICACION_MANIFIESTO_FASE4.json',result)

if __name__=='__main__':
 if sys.argv[1:]==['--verificar']: verify()
 elif not sys.argv[1:]: main()
 else: raise ValueError('Solo --verificar o cierre nuevo')
