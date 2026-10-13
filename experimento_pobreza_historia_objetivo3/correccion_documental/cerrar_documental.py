"""Completa documentos y verifica entrega; nunca importa ni llama ejecutores de modelos."""
from infra_correccion import *
from verificar_entrega_corregida import preserved,verify,evidence_check
from preflight import environment,conservation
import auditor
def run():
    deadline();check(not (MAIN/'MANIFIESTO_FINAL.json').exists(),'entrega final ya cerrada')
    environment();n=preserved();cons=conservation();audit=auditor.run(write=False)
    evidence_check();check(load(MAIN/'CONTROL_TEXTO.json')['aprobado'],'texto')
    result=load(MAIN/'resultados/PRIMARIO.json');l=load(HERE/'LEDGER_DOCUMENTAL.json')
    check([a['mode'] for a in l['attempts'] if a['status']=='complete']==['inventado','preview','final'],'orden documental')
    l.update(status='cerrado_completo',end_epoch=time.time(),saldo_reutilizable=False,new_fits=0);l['elapsed_seconds']=l['end_epoch']-START;save(HERE/'LEDGER_DOCUMENTAL.json',l)
    save(HERE/'CONSERVACION_FINAL.json',dict(aprobado=True,previous_files_preserved=n,foreign_conservation=cons,original_freeze_sha256=sha(MAIN/'CONGELACION.json'),pilot_ledger_sha256=sha(MAIN/'piloto/ledger.json'),no_new_fits=True))
    save(MAIN/'ACEPTACION_FINAL.json',dict(completa=True,operativa=True,tecnica=True,new_fits=0,fits_auditor=0,pilot_reopened=False,pilot_audited=True,notebook_executed=True,visual_review=True,text_verified=True,scientific_criteria_changed=False,original_closed_incomplete_preserved=True,authenticity_resolved=False,temporal_availability_resolved=False,independent_confirmation=False,epoch=time.time(),documental_start_epoch=START))
    save(HERE/'PENDIENTES.md','''# Pendientes científicos de la entrega completa

- Autenticar la fuente local y documentar la disponibilidad temporal antes de una evaluación prospectiva. Aprobación técnica no resuelve procedencia ni disponibilidad anticipada.
- Todos los años ya vistos: contraste exploratorio y dependiente, sin confirmación independiente. Pocos años y dependencia territorial.
- Hogares/personas frente a estudiantes; establecimiento frente a residencia; enlace ecológico, sin efectos causales.
- Último año local2025; nota de actualización14abril2026. Siguiente año solamente condicional a información comparable, autenticada y disponible; no proyectado.
- El contraste no ejecuta íntegramente las especificaciones/validaciones adicionales de la tesis páginas58-59: composición/año/contribuciones dimensionales/lasso/elasticnet/nivelesMatemáticas/validaciónterritorial/robustezexclusión2021.
- No objetivo4, escenarios, simulaciones, modelo final, nuevas fuentes/raw/red/commit/push ni avance automático. Piloto y corrección documental cerrados sin saldo reutilizable.

El bloqueo del kernel está resuelto mediante gestor asíncrono y comunicación local autorizada, probado con inventados y con las celdas reales. El antecedente se archiva con evidencia; no es un fallo activo de resultados.
''')
    save(HERE/'REGISTRO_HALLAZGOS.json',[
        dict(hallazgo='Arranque bloqueado con gestor síncrono',impacto='impedía notebook y entrega académica verificable',alternativa='gestor asíncrono compatible, prueba inventada y celdas reales',resolucion='resuelto; NOTEBOOK_INVENTADO.ipynb/RESULTADOS.ipynb realmente ejecutados; original congelado intacto',estado='antecedente archivado',evidencia='correccion_documental/PRUEBA_NOTEBOOK_INVENTADO.json'),
        dict(hallazgo='Aislamiento rechaza canales locales del kernel',impacto='prueba inicial no puede abrir sockets locales',alternativa='permiso explícito para comunicación local del kernel, sin red externa',resolucion='permiso concedido; un intento sandbox fallido y ejecución aprobada; sin descargas ni fits',estado='resuelto',evidencia='correccion_documental/ERROR_NOTEBOOK_0.txt y LEDGER_DOCUMENTAL.json'),
        dict(hallazgo='Políticas histórica y ampliada coinciden',impacto='no mejora primaria ni uso de pobreza por ampliado',alternativa='respetar selector/meta/denominador; reportar secundario y diagnósticos separados',resolucion='primario0%;meta5%no alcanzada; no afirmar uso pobreza por ampliado',estado='resultado exploratorio',evidencia='resultados/PRIMARIO.json;resultados/tablas/selecciones.csv'),
        dict(hallazgo='Fuente y fechas locales no autenticadas',impacto='aceptación técnica no acredita previsión factible ni causalidad',alternativa='lenguaje condicional y pendientes prospectivos',resolucion='limitación científica explícita; no nuevas fuentes/proyecciones',estado='pendiente científico',evidencia='resultados/FECHA_LOCAL.json;correccion_documental/PENDIENTES.md'),
        dict(hallazgo='Representación de códigos05/08 versus5/8',impacto='historia requería identidad geográfica estable',alternativa='normalización previa y cotejo de nombres',resolucion='ya resuelto antes del piloto, preservado; sin nuevo criterio',estado='antecedente archivado',evidencia='preflight/NORMALIZACION_CODIGOS.csv')])
    save(HERE/'INFORME_TECNICO.md',f'''# Informe técnico de entrega completada

La corrección documental autorizada completó la entrega usando exclusivamente el piloto cerrado y auditado. Cero nuevos ajustes, repeticiones de modelos o cambios científicos. El cierre incompleto y todos sus archivos originales están preservados según PARTIDA_CORRECCION.json; continuidad anterior copiada en antecedentes/CONTINUIDAD_INCOMPLETA.md. El informe anterior de carpeta superior corresponde al antecedente incompleto y no se sobrescribe.

Preflight actual: entorno exacto Python3.12.14/sklearn1.9.1/pip25.0.1,54distribuciones del lock,pipcheck,semilla20261010 y un hilo. Revalidación propia de{cons['protegidos']}originales/Git/commit histórico/ascendencia/manifiestos/mappings/cierres de memoria y continuidades preservadas, separada del verificador histórico aprobado antes de crear carpeta nueva. Nuevos controles preservan{n}archivos del cierre incompleto, incluyendo su manifiesto, diagnóstico y código congelado. Ledger original y congelación científica intactos.

Reparación aislada en correccion_documental/: AsyncKernelManager sustituye el arranque síncrono incompatible; configuración de entorno antes de imports y reloj separado con7200s desde2026-10-12 18:37:59UTC. No cambia START del piloto ni operaciones aritméticas de analisis.py. Las cinco celdas conservan literalmente los fragmentos científicos originales; celdas1/5 añaden únicamente reloj y comprobación de guardia contra fits. El notebook fuente y generador original se conservan; fuentes de corrección independientes con huellas. Prueba inventada de3celdas exitosa antes de resultados. Primer intento con aislamiento falló por socket local no permitido, sin celdas/modelos; ejecución posterior autorizada para comunicación local del kernel, sin red externa, descargas o instalación. Intentos/tiempos/celdas en LEDGER_DOCUMENTAL.json. La corrección y fuentes científicas se congelaron antes del preview.

El piloto original sigue cerrado:200ajustes/cuatrorepeticiones, sin reabrirlo. El auditor independiente intacto revalidó todas las matrices/llaves/historia/fechas/defaults/scaler/params/predicciones reconstruidas/selector propio/CSV/cobertura/copias/linaje/budget/terminación,0fits/importsoperativos/deserialización. 21candidatos,315matrices/315records/10.395predicciones/165pares externos. Población/media recibida/geografía colegio/igualpeso; conteosnoX;2019solo historia/2020excluido/previo2021=2019sinanualizar. Quince tasas orden declaradosin agregados nuevos. Parámetros/población/criterios originales permanecen en ESPECIFICACION.json y PROTOCOLO.md, sin modificaciones; representación geográfica normalizada antes del piloto está trazada porfila.

Notebook RESULTADOS.ipynb validado nbformat,5celdas realmente ejecutadas con kernel exacto, ninguna salida manual; preview de3celdas para revisiónvisual antes del texto. Todas las cifras/tablas/JSON/PNG/texto/evidencias llaman funciones congeladas compartidas. Revisiónvisual con huellas de tresfiguras; nueva ejecución final conserva esas mismas huellas. Texto generado porcelda4 trasrevisión y control porcelda5. Tabla completa de evidencias porafirmación/celda/función/archivo/tabla/llave/n/unidad/huella; verificación devaloresdesdeJSON/CSV. Texto de complementariedad a tesis, sin etiquetas de versiones/historia de iteraciones en cuerpo y sin citas inventadas. Lecturas porpáginas25/58-60/113-114 ypendientesotraspáginas en LECTURAS.json.

Resultado actual exploratorio:MAE histórico={result['MAE_historico']:.17g}puntos;ampliado={result['MAE_ampliado']:.17g};conpobreza={result['MAE_con_pobreza']:.17g}. Primario=100*(MAEhistórico-MAEampliado)/MAEhistórico={result['mejora_primaria_percent']:.17g}%;meta≥5%noalcanzada. Ampliado no eligió variables de pobreza; no afirmar aporte incremental por esa política. Conpobreza secundario ypares a mismoalpha/árboles diagnósticos sin rescateprimario. Cifras exactas en resultados/PRIMARIO.json y tablas/celdas, no comparación directa con porcentajes históricos que tenían otrodenominador. No observaciones independientes añadidas ni ganador elegido por externas.

Tablas completas: métricas globales/anuales/territoriales;21candidatos global/anual;selecciones e internas;comparacionesHvsHI/HD al mismoalpha/árboles;erroresfirmados/absolutos/bias/dirección;gruposdescriptivos definidos antes del piloto por tercilesIPM2018 de11territorios cadauno/desempatecódigo;rangos/coefs/interceptos/árboles. No pvalores confirmatorios. Árboles ycoeficientes describen asociaciones/estimación condicional, no efectos causales.

La aceptación técnica no autentica fuente local ni disponibilidad temporal. Hogares/personas/estudiantes/colegio/residencia, ecología, pocos años, dependencia y todos añosvistos permanecen como límites. Último año local2025 y nota local14abril2026; siguiente año solo condicional, sin proyección. No se ejecutó todo diseño original tesis ni objetivo4/escenarios/modelofinal. No .git/originales/experimentosajenos/redexterna/commit/push; sin avance automático. Pendientes científicos separados del bloqueo de notebook ya resuelto y archivado.

Entrega vigente: TEXTO_OBJETIVO3_TESIS.md, RESULTADOS.ipynb, resultados/tablas y figuras, EVIDENCIAS_TEXTO.csv, ACEPTACION_FINAL.json, MANIFIESTO_FINAL.json y correccion_documental/verificar_entrega_corregida.py. Verificar sólo lectura desde entorno exacto. No ejecutar generadores/piloto automáticamente.
''')
    save(HERE/'README.md','''# Orden y uso de la entrega

1. Leer CONTINUIDAD.md de carpeta superior y el informe de esta carpeta.
2. Fuente científica congelada: analisis.py y notebook_resultados.py de carpeta superior. Las correcciones de infraestructura están exclusivamente aquí.
3. Generador corregido: --inventado (tres celdas sin modelos), --preview (tablas/figuras), revisiónvisual y ejecución final (cinco celdas; texto último). Es el orden ya ejecutado; no repetir automáticamente.
4. Entradas: piloto/ y preflight/PANEL.csv; outputs: RESULTADOS.ipynb, resultados/, TEXTO_OBJETIVO3_TESIS.md y EVIDENCIAS_TEXTO.csv. Versiones/semilla en PREFLIGHT.json; Python exacto de /tmp.
5. Verificador de lectura: verificar_entrega_corregida.py, no el verificador original que corresponde a otra infraestructura/cierre. Los originales se preservan sin modificarlos.
6. El piloto no se reabre; cero nuevosfits. Toda estimación es exploratoria/condicional y no causal.
''')
    save(MAIN/'CONTINUIDAD.md','''# Continuidad propia: entrega completa después de corrección documental autorizada

El usuario autorizó expresamente completar la entrega documental con7200s nuevos desde2026-10-12 18:37:59UTC, cero nuevos ajustes/repeticiones/cambios científicos. El piloto original permanece cerrado:200fits originales/cuatrorepeticiones, sinpending/saldo. Cierre incompleto original preservado por PARTIDA_CORRECCION.json; continuidad incompleta exacta en correccion_documental/antecedentes/CONTINUIDAD_INCOMPLETA.md; preparación anterior preservada en antecedentes/CONTINUIDAD_PREPARACION.md. No heredar/reabrir presupuesto anterior.

Revalidaciones: entorno exacto54lock+pip25.0.1/Python3.12.14/sklearn1.9.1/pipcheck/semilla20261010/unhilo;37744originales/manifiestos/mappings/cierres/Git/commit109797407d75d2097e5b71f8bcef3fc266bc61d2/ascendencia/trabajo posterior/temporal etapa1 texto-huella. Auditor independiente intacto,0fits/importsoperativos/deserialización. Código/reglas/defaults/candidatos/fuentes/matrices/selecciones/predicciones y ledger congelados intactos. Conservación actual propia, distinta de aprobación histórica de verificador previo a carpeta nueva.

Reparación documentada por separado: gestor asíncrono compatible, entorno previo aimports, reloj nuevo y guardia cero fits. Prueba inventada ejecutada antes de resultados; permiso de comunicación local del kernel tras fallo del aislamiento, sin redexterna/descargas. Notebook de5celdas reales validado, tablas/figuras/texto/evidencias desde funciones científicas compartidas sin cambios. Preview/revisiónvisual ytextoúltimo. Bloqueo anterior archivado como antecedente resuelto, no problema activo. Fuentes y orden en correccion_documental/README.md; ledger/congelación propios de infraestructura.

Decisiones científicas conservadas: población/media recibida/geografía colegio/igualpeso;conteosnoX;2018nivel/2019solo historia/2020excluido/previo2021=2019sinanualizar;respuestas2021+;165pares2021-2025. Códigosstrings normalizados dosdígitos antes del piloto, nombrescotejados ytablaoriginal→canónico, sincambio población/bytes. Hdosvariableshistoria,IIPM%personas,Dquince%hogaresordenDIMENSIONES/TASAS,HI/HD;sinagregadosinventados ni otrasentradas. IPM contemporáneo condicionante,sindisponibilidadanticipadademostrada.21candidatos/selectorMAE-RMSE0.1/menosentradas/orden;selecciones antes externas;2021fijopersistencia. Histórico/ampliado/conpobreza yprimario con denominadorMAEhistórico/meta5% sin rescate por diagnósticos/externas. Valores exactos en resultados/PRIMARIO.json y celdas; mejora primaria0%, meta no alcanzada. Ampliado no seleccionó pobreza. Resultado exploratorio limitado a estos datos/modelos, no inexistencia de relación pobrezaeducación.

Entrega vigente: TEXTO_OBJETIVO3_TESIS.md, RESULTADOS.ipynb, resultados/tablas/figuras, EVIDENCIAS_TEXTO.csv, CONTROL_TEXTO.json, ACEPTACION_FINAL.json, MANIFIESTO_FINAL.json, VERIFICACION_FINAL.json y correccion_documental/INFORME_TECNICO.md/REGISTRO_HALLAZGOS.json/PENDIENTES.md/CONSERVACION_FINAL.json/CIERRE_DOCUMENTAL.json. Verificador lectura vigente: correccion_documental/verificar_entrega_corregida.py. INFORME_TECNICO.md/PENDIENTES.md y verificador_cierre_incompleto.py de carpeta superior corresponden al antecedente preservado; no confundirlos con entrega completa.

Pendientes científicos: autenticar fuente local/disponibilidadtemporal/ecología/hogarespersonasestudiantes/colegioresidencia/pocosaños/dependencia/todosañosvistos/sinconfirmaciónindependiente. Último año local2025; fecha local14abril2026; siguienteaño solo condicional. No ejecución íntegra diseños/validaciones adicionales de tesis58-59. No causalidad/objetivo4/escenarios/proyecciones/simulaciones/modelofinal/nuevasfuentes/raw/redexterna/.git/commit/push ni avance automático. Piloto y corrección cerrados sin saldo reutilizable.
''')
    end=time.time();save(HERE/'CIERRE_DOCUMENTAL.json',dict(estado='completo',start_epoch=START,end_epoch=end,elapsed_seconds=end-START,max_seconds=7200,new_fits=0,pilot_reopened=False,saldo_reutilizable=False,no_auto_advance=True))
    preliminary=verify(manifest=False);save(HERE/'VERIFICACION_PREMANIFIESTO.json',preliminary)
    excluded=['MANIFIESTO_FINAL.json','VERIFICACION_FINAL.json']
    mapping={p.relative_to(MAIN).as_posix():sha(p) for p in MAIN.rglob('*') if (p.is_file() or p.is_symlink()) and p.relative_to(MAIN).as_posix() not in excluded}
    save(MAIN/'MANIFIESTO_FINAL.json',dict(sha256=mapping,exclusions=excluded,completa=True,new_fits=0,previous_incomplete_preserved=True,scope=MAIN.name))
    final=verify();save(MAIN/'VERIFICACION_FINAL.json',final)
    end=time.time();cl=load(HERE/'CIERRE_DOCUMENTAL.json');cl.update(end_epoch=end,elapsed_seconds=end-START);check(cl['elapsed_seconds']<=7200,'budget final');save(HERE/'CIERRE_DOCUMENTAL.json',cl)
    m=load(MAIN/'MANIFIESTO_FINAL.json');m['sha256']['correccion_documental/CIERRE_DOCUMENTAL.json']=sha(HERE/'CIERRE_DOCUMENTAL.json');save(MAIN/'MANIFIESTO_FINAL.json',m)
    print(json.dumps(dict(aprobado=final['aprobado'],files=len(mapping),elapsed_seconds=cl['elapsed_seconds'],new_fits=0,entrega_completa=True)))
if __name__=='__main__':run()
