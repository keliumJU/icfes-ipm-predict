"""Funciones compartidas de resultados sin sklearn ni nuevos fits.

El notebook llama a estas funciones para todas las cifras/tablas/figuras del texto.
"""
from infra import *
import math, numpy as np, pandas as pd
def read_csv(name):return pd.read_csv(HERE/name,float_precision='round_trip',dtype={'codigo_departamento':str})
def measure(d):
    e=d.error.to_numpy();n=len(e);check(n>0,'analysis nonempty')
    return dict(n=n,MAE=math.fsum(abs(float(x)) for x in e)/n,RMSE=math.sqrt(math.fsum(float(x)*float(x) for x in e)/n),sesgo=math.fsum(float(x) for x in e)/n)
def tables():
    deadline();audit=load(HERE/'AUDITORIA.json');check(audit['aprobado'],'audit prerequisite')
    policy=read_csv('piloto/POLITICAS.csv');pred=read_csv('piloto/PREDICCIONES.csv');panel=read_csv('preflight/PANEL.csv');spec=load(HERE/'ESPECIFICACION.json')
    tab=HERE/'resultados/tablas'
    globalrows=[dict(policy=p,**measure(d)) for p,d in policy.groupby('policy',sort=False)]
    globaldf=pd.DataFrame(globalrows);csv_save(tab/'metricas_globales.csv',globaldf)
    annual=pd.DataFrame([dict(policy=p,anio=int(y),**measure(d)) for (p,y),d in policy.groupby(['policy','anio'],sort=False)]);csv_save(tab/'metricas_anuales.csv',annual)
    territory=pd.DataFrame([dict(policy=p,codigo_departamento=c,departamento=panel[panel.codigo_departamento==c].departamento.iloc[0],**measure(d)) for (p,c),d in policy.groupby(['policy','codigo_departamento'],sort=False)]);csv_save(tab/'metricas_territoriales.csv',territory)
    external=pred[pred.context.str.startswith('e')];candidates=pd.DataFrame([dict(id=id,**measure(d)) for id,d in external.groupby('id',sort=False)]);csv_save(tab/'candidatos_global.csv',candidates)
    ca=pd.DataFrame([dict(id=id,anio=int(y),**measure(d)) for (id,y),d in external.groupby(['id','anio'],sort=False)]);csv_save(tab/'candidatos_anual.csv',ca)
    sel=load(HERE/'piloto/SELECCIONES.json');selection=[];inner=[]
    for year in range(2021,2026):
        chosen={p:'persistencia' for p in spec['policies']} if year==2021 else sel[str(year)]['chosen']
        for p,id in chosen.items():selection.append(dict(anio=year,policy=p,id=id,grupo=next(c['group'] for c in spec['candidates'] if c['id']==id),usa_pobreza=int(id.startswith('Ridge_HI_') or id.startswith('Ridge_HD_'))))
        if year>2021:
            for id,v in sel[str(year)]['scores'].items():inner.append(dict(externo=year,id=id,**v))
    selection=pd.DataFrame(selection);csv_save(tab/'selecciones.csv',selection);csv_save(tab/'metricas_internas.csv',pd.DataFrame(inner))
    pairs=[]
    for family in ['Ridge','Arbol']:
        for alpha in ([.1,1.,10.] if family=='Ridge' else [None]):
            hid=f'Ridge_H_{alpha:g}' if family=='Ridge' else 'Arbol_H';hm=candidates[candidates.id==hid].iloc[0]
            for g in ['HI','HD']:
                id=f'Ridge_{g}_{alpha:g}' if family=='Ridge' else f'Arbol_{g}';m=candidates[candidates.id==id].iloc[0]
                pairs.append(dict(familia=family,alpha='no aplica' if alpha is None else str(alpha),referencia=hid,id=id,n=int(m.n),MAE_H=float(hm.MAE),MAE_combinado=float(m.MAE),mejora_percent=100*(hm.MAE-m.MAE)/hm.MAE,RMSE_H=float(hm.RMSE),RMSE_combinado=float(m.RMSE)))
    csv_save(tab/'comparaciones_mismo_alpha.csv',pd.DataFrame(pairs))
    errors=policy.merge(panel[['codigo_departamento','anio','departamento','puntaje_previo','ipm','cambio_observado']],on=['codigo_departamento','anio'],validate='many_to_one')
    errors['error_absoluto']=errors.error.abs();errors['cambio_estimado']=errors.prediccion-errors.puntaje_previo
    errors['direccion_correcta']=(np.sign(errors.cambio_estimado)==np.sign(errors.cambio_observado)).astype(int)
    csv_save(tab/'errores_completos.csv',errors)
    direction=pd.DataFrame([dict(policy=p,anio=int(y),n=len(d),aciertos=int(d.direccion_correcta.sum()),porcentaje=100*int(d.direccion_correcta.sum())/len(d)) for (p,y),d in errors.groupby(['policy','anio'],sort=False)]);csv_save(tab/'direccion_anual.csv',direction)
    # grupos exclusivamente descriptivos: tercios de rangos de IPM2018, sin usar error
    from preflight import BASE
    b=pd.read_csv(ROOT/BASE,float_precision='round_trip',dtype={'codigo_departamento':str})
    b['codigo_departamento']=b.codigo_departamento.str.zfill(2)
    initial=b[b.anio==2018].sort_values(['ipm','codigo_departamento']);lookup={c:['bajo','medio','alto'][i//11] for i,c in enumerate(initial.codigo_departamento)}
    errors['grupo_ipm2018']=errors.codigo_departamento.map(lookup)
    groups=pd.DataFrame([dict(policy=p,grupo_ipm2018=g,**measure(d)) for (p,g),d in errors.groupby(['policy','grupo_ipm2018'],sort=False)]);csv_save(tab/'grupos_descriptivos.csv',groups)
    csv_save(tab/'grupos_definicion.csv',pd.DataFrame([dict(codigo_departamento=c,grupo_ipm2018=g,criterio='orden IPM2018, 11 territorios; desempate código') for c,g in lookup.items()]))
    ranges=pd.DataFrame([dict(variable=v,unidad='puntos' if v in ['puntaje_previo','cambio_previo','prom_punt_global'] else ('% personas' if v=='ipm' else '% hogares'),n=len(panel),minimo=float(panel[v].min()),maximo=float(panel[v].max())) for v in ['prom_punt_global','puntaje_previo','cambio_previo','ipm',*spec['groups']['D']]]);csv_save(tab/'rangos.csv',ranges)
    coef=[];intercepts=[];tree=[]
    led=load(HERE/'piloto/ledger.json')
    for identity in led['originals']:
        rec=load(HERE/f'piloto/records/{identity}.json')
        if rec['family']=='Ridge':
            w=np.asarray(rec['coef'])/rec['scaler']['scale'];inter=rec['intercept']-math.fsum(float(a)*float(b) for a,b in zip(w,rec['scaler']['mean']))
            intercepts.append(dict(context=identity.split('__')[0],id=rec['id'],intercept_estandarizado=rec['intercept'],intercept_original=inter))
            for v,c,orig in zip(rec['inputs'],rec['coef'],w):coef.append(dict(context=identity.split('__')[0],id=rec['id'],variable=v,coef_estandarizado=c,coef_original=float(orig),unidad='puntos por punto de historia' if v in ['puntaje_previo','cambio_previo'] else 'puntos por punto porcentual',interpretacion='asociación condicional; no causal'))
        else:
            for node in range(rec['tree']['node_count']):tree.append(dict(context=identity.split('__')[0],id=rec['id'],nodo=node,**{k:rec['tree'][k][node] for k in ['children_left','children_right','feature','threshold','value','impurity','n_node_samples','weighted_n_node_samples']}))
    csv_save(tab/'coeficientes.csv',pd.DataFrame(coef));csv_save(tab/'interceptos.csv',pd.DataFrame(intercepts));csv_save(tab/'arboles.csv',pd.DataFrame(tree))
    hist=float(globaldf[globaldf.policy=='historico'].MAE.iloc[0]);amp=float(globaldf[globaldf.policy=='ampliado'].MAE.iloc[0]);poverty=float(globaldf[globaldf.policy=='con_pobreza'].MAE.iloc[0])
    check(math.isfinite(hist) and hist>0,'denominator positive')
    primary=100*(hist-amp)/hist;check(primary==audit['primary_percent'],'audit primary exact')
    result=dict(MAE_historico=hist,MAE_ampliado=amp,MAE_con_pobreza=poverty,mejora_primaria_percent=primary,meta_percent=5,meta_cumplida=primary>=5,mejora_secundaria_percent=100*(hist-poverty)/hist,n=165,territorios=33,respuestas_anios=5,pares_fuente=231,anios_fuente=7,usa_pobreza_ampliado_anios=selection[(selection.policy=='ampliado')&(selection.usa_pobreza==1)].anio.tolist(),ultimo_anio_local=int(panel.anio.max()),confirmacion_independiente=False)
    save(HERE/'resultados/PRIMARIO.json',result)
    save(HERE/'resultados/TRAZA_CELDAS.json',dict(tablas='celda2:analisis.tables',figuras='celda3:analisis.figures',texto='celda4:analisis.academic_text',control='celda5:analisis.text_control'))
    return result
def figures():
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    deadline();annual=read_csv('resultados/tablas/metricas_anuales.csv');g=read_csv('resultados/tablas/metricas_globales.csv')
    colors={'historico':'#234F70','ampliado':'#D17427','con_pobreza':'#388268'};labels={'historico':'Historia','ampliado':'Historia con opción de pobreza','con_pobreza':'Historia + pobreza obligatoria'}
    out=HERE/'resultados/figuras';out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'figure.dpi':150})
    fig,ax=plt.subplots(figsize=(8,4.6))
    for policy in colors:
        d=annual[annual.policy==policy];ax.plot(d.anio,d.MAE,'o-',label=labels[policy],color=colors[policy],linewidth=2)
    ax.set(xlabel='Año evaluado',ylabel='MAE (puntos del puntaje global)',title='Error anual de las políticas de selección');ax.set_xticks(range(2021,2026));ax.grid(alpha=.2);ax.legend(fontsize=9)
    fig.text(.1,.02,'n = 33 territorios por año; igual peso. 2021: persistencia fija para todas.',fontsize=9);fig.tight_layout(rect=(0,.06,1,1));fig.savefig(out/'01_error_anual.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.6));x=np.arange(len(g))
    ax.barh(x,g.MAE,color=[colors[p] for p in g.policy]);ax.set_yticks(x,[labels[p] for p in g.policy]);ax.set(xlabel='MAE (puntos del puntaje global)',title='Contraste agregado en los mismos pares territoriales');ax.grid(axis='x',alpha=.2)
    for i,row in g.iterrows():ax.text(row.MAE+.02,i,f'{row.MAE:.3f}',va='center')
    ax.set_xlim(0,g.MAE.max()*1.2);fig.text(.15,.025,'n = 165 pares territorio-año, 2021-2025; análisis exploratorio.',fontsize=9);fig.tight_layout(rect=(0,.07,1,1));fig.savefig(out/'02_error_global.png');plt.close(fig)
    territories=read_csv('resultados/tablas/metricas_territoriales.csv');wide=territories.pivot(index='departamento',columns='policy',values='MAE');delta=(wide.historico-wide.ampliado).sort_values()
    fig,ax=plt.subplots(figsize=(9,10));ax.barh(delta.index,delta.values,color=['#D17427' if v>=0 else '#234F70' for v in delta]);ax.axvline(0,color='black',lw=.8);ax.set(xlabel='MAE historia - MAE ampliado (puntos; positivo = menor error)',title='Diferencias territoriales de error');ax.grid(axis='x',alpha=.2)
    fig.text(.12,.015,'n = 5 años por territorio; 33 territorios. Descriptivo, sin interpretación causal.',fontsize=9);fig.tight_layout(rect=(0,.035,1,1));fig.savefig(out/'03_diferencias_territoriales.png');plt.close(fig)
    hashes={p.name:sha(p) for p in sorted(out.glob('*.png'))};save(HERE/'resultados/FIGURAS.json',dict(files=hashes,cell=3,function='analisis.figures'))
    return hashes
def academic_text():
    # Se genera únicamente después de revisión visual documentada.
    visual=load(HERE/'resultados/REVISION_VISUAL.json');check(visual['aprobado'],'visual review prerequisite')
    for name,h in visual['files'].items():check(sha(HERE/'resultados/figuras'/name)==h,'visual same figure')
    r=load(HERE/'resultados/PRIMARIO.json');g=read_csv('resultados/tablas/metricas_globales.csv');a=read_csv('resultados/tablas/metricas_anuales.csv');sel=read_csv('resultados/tablas/selecciones.csv');pairs=read_csv('resultados/tablas/comparaciones_mismo_alpha.csv');territory=read_csv('resultados/tablas/metricas_territoriales.csv')
    fmt=lambda x:f'{float(x):.3f}'.replace('.',',')
    evidence=[]
    def ev(ident,claim,file,table,key,n,unit,value,cell=2,function='analisis.tables'):
        evidence.append(dict(afirmacion_id=ident,afirmacion=claim,celda=cell,funcion=function,archivo=file,tabla=table,llave=key,n=n,unidad=unit,valor=str(value),sha256=sha(HERE/file)))
    for ident,key,unit in [('N','n','pares territorio-año'),('T','territorios','territorios'),('F','pares_fuente','pares territorio-año'),('Y','anios_fuente','años'),('H','MAE_historico','puntos'),('A','MAE_ampliado','puntos'),('P','MAE_con_pobreza','puntos'),('R','mejora_primaria_percent','%'),('S','mejora_secundaria_percent','%'),('M','meta_percent','%'),('ULT','ultimo_anio_local','año')]:ev(ident,key,'resultados/PRIMARIO.json','PRIMARIO',key,r['n'],unit,r[key])
    policy_names={'historico':'Historia','ampliado':'Ampliado','con_pobreza':'Con pobreza'}
    table1='| Política | MAE (puntos) | RMSE (puntos) | Sesgo (puntos) |\n|---|---:|---:|---:|\n'
    for _,row in g.iterrows():
        table1+=f'| {policy_names[row.policy]} | {fmt(row.MAE)} | {fmt(row.RMSE)} | {fmt(row.sesgo)} |\n'
        for col in ['MAE','RMSE','sesgo']:ev('G_'+row.policy+'_'+col,'tabla1 '+col,'resultados/tablas/metricas_globales.csv','metricas_globales','policy='+row.policy+';col='+col,int(row.n),'puntos',row[col])
    table2='| Año | Histórico | Ampliado | Con pobreza |\n|---|---|---|---|\n'
    for year in sorted(sel.anio.unique()):
        values=[sel[(sel.anio==year)&(sel.policy==p)].id.iloc[0] for p in policy_names]
        # etiquetas académicas; mismos IDs documentados en tablas completas
        def pretty(id):return 'Persistencia' if id=='persistencia' else id.replace('Ridge_','Ridge ').replace('_','; α = ')
        table2+=f'| {year} | '+ ' | '.join(pretty(id) for id in values)+' |\n'
        for p,id in zip(policy_names,values):ev(f'SEL_{year}_{p}','tabla2 selección','resultados/tablas/selecciones.csv','selecciones',f'anio={year};policy={p}',33,'candidato',id)
    table3='| Año | Historia | Ampliado | Con pobreza |\n|---|---:|---:|---:|\n'
    for year in sorted(a.anio.unique()):
        values=[a[(a.anio==year)&(a.policy==p)].MAE.iloc[0] for p in policy_names];table3+=f'| {year} | '+' | '.join(fmt(x) for x in values)+' |\n'
        for p,x in zip(policy_names,values):ev(f'AN_{year}_{p}','tabla3 MAE','resultados/tablas/metricas_anuales.csv','metricas_anuales',f'anio={year};policy={p};col=MAE',33,'puntos',x)
    selected_years=r['usa_pobreza_ampliado_anios'];usage='La política ampliada incorporó pobreza en '+', '.join(str(y) for y in selected_years)+'.' if selected_years else 'La política ampliada seleccionó exclusivamente historia o persistencia; por ello, su desempeño no constituye evidencia de uso de las variables de pobreza.'
    ev('USO','años ampliado utiliza pobreza','resultados/PRIMARIO.json','PRIMARIO','usa_pobreza_ampliado_anios',165,'años',json.dumps(selected_years))
    interpretation=(f'La reducción del MAE alcanzó el umbral exploratorio previamente establecido de {fmt(r["meta_percent"])} %. Este resultado respalda estudiar posteriormente la utilidad de la información de pobreza como condición de estimación territorial, sujeto a las limitaciones de procedencia, disponibilidad y dependencia descritas.' if r['meta_cumplida'] else f'La reducción del MAE no alcanzó el umbral exploratorio previamente establecido de {fmt(r["meta_percent"])} %. El resultado se limita a estos datos, entradas, modelos y reglas de selección; no demuestra ausencia de relación entre pobreza y educación.')
    text=f'''# Aporte de la pobreza multidimensional frente a la historia del desempeño académico

Como complemento al diseño predictivo departamental, se examinó si la incidencia de la pobreza multidimensional o sus tasas de privación aportan información adicional a la historia del puntaje global de Saber 11. El propósito es comparar estimaciones condicionales territoriales, sin atribuir cambios del desempeño a intervenciones sobre la pobreza. La unidad de análisis es el par territorio-año y se conserva el promedio del puntaje global recibido, vinculado al departamento del establecimiento educativo. Cada par tiene igual peso; los conteos de evaluados no se emplean como predictores.

La base local contiene {r['pares_fuente']} observaciones, correspondientes a {r['territorios']} territorios y {r['anios_fuente']} años: 2018, 2019 y 2021-2025. La evaluación comprende {r['n']} pares de 2021-2025. Los puntajes de 2018 y 2019 se utilizan exclusivamente para construir historia; 2020 queda excluido. Para 2021, el puntaje anterior es el de 2019 y el cambio histórico se calcula frente a 2018, sin anualizar el intervalo.

La historia (H) incluye el puntaje del año disponible anterior y el cambio registrado entre los dos años disponibles anteriores. La incidencia (I) se expresa como porcentaje de personas; los quince indicadores (D), como porcentajes de hogares. Se comparan H, I, D, H+I (HI) y H+D (HD), sin reunir simultáneamente el índice y las tasas. La pobreza del año evaluado funciona como condición contemporánea de estimación. Su disponibilidad anticipada no ha sido demostrada, por lo que el ejercicio no acredita una predicción prospectiva factible.

Se emplean la persistencia del puntaje previo, regresión ridge con penalizaciones 0,1, 1 y 10 y árboles de profundidad máxima dos, con al menos once observaciones por hoja. Las transformaciones de escala se calculan únicamente sobre el entrenamiento correspondiente. Las respuestas de ajuste comienzan en 2021 y siempre preceden al año evaluado. En la evaluación de 2021 se aplica persistencia fija a todos los candidatos. En los años posteriores, la selección utiliza las ventanas internas acumuladas, incluidas las predicciones de respaldo de 2021, sin consultar los errores externos del año que se va a evaluar.

El selector conserva los candidatos con MAE hasta 0,1 puntos por encima del mínimo; dentro de ese conjunto conserva aquellos con RMSE hasta 0,1 puntos por encima del mínimo correspondiente. Después prioriza el menor número de entradas y el orden fijado. La política histórica elige entre persistencia y ridge H. La ampliada añade ridge HI y HD. La política con pobreza exige ridge HI o HD, salvo el respaldo fijo de 2021. Los árboles y las especificaciones I y D se utilizan únicamente como diagnósticos descriptivos.

La comparación primaria es la reducción porcentual del MAE de la política ampliada frente a la histórica, calculada sobre los mismos pares observados. El denominador es el MAE histórico, positivo y finito. La meta se estableció antes de los ajustes y no se utiliza el desempeño externo para escoger retrospectivamente una política ganadora.

**Tabla 1. Error agregado de las políticas de selección.**

{table1}
Fuente: cálculo sobre las predicciones externas; n = {r['n']} pares con igual peso. El sesgo es predicción menos observado.

El MAE histórico fue {fmt(r['MAE_historico'])} puntos y el ampliado {fmt(r['MAE_ampliado'])} puntos. La mejora primaria fue {fmt(r['mejora_primaria_percent'])} %. {interpretation} {usage}

**Tabla 2. Candidatos seleccionados mediante información interna.**

{table2}
H representa historia; HI combina historia e incidencia; HD combina historia y tasas. Las elecciones preceden a la evaluación externa respectiva.

**Tabla 3. MAE por año evaluado, en puntos del puntaje global.**

{table3}
Fuente: predicciones externas, n = {r['territorios']} territorios por año. El primer año emplea el respaldo fijo.

La política que obliga a incorporar pobreza obtuvo un MAE de {fmt(r['MAE_con_pobreza'])} puntos, equivalente a una mejora secundaria de {fmt(r['mejora_secundaria_percent'])} % frente a la política histórica. Esta comparación no sustituye el criterio primario. Las tablas completas documentan las comparaciones de H con HI y HD a la misma penalización, los árboles equivalentes, el error firmado y absoluto por territorio y año, el sesgo, la dirección del cambio, los rangos observados y los coeficientes. Los coeficientes describen asociaciones condicionales dentro de la especificación estimada y no efectos de política.

![MAE anual](resultados/figuras/01_error_anual.png)

**Figura 1. Error anual de las políticas**, en puntos del puntaje global, con n = {r['territorios']} por año. Las series usan el mismo conjunto de llaves.

![MAE agregado](resultados/figuras/02_error_global.png)

**Figura 2. Error agregado de las políticas**, en puntos del puntaje global, con n = {r['n']} pares territorio-año.

![Diferencia territorial](resultados/figuras/03_diferencias_territoriales.png)

**Figura 3. Diferencias territoriales del MAE histórico menos el ampliado**. Los valores positivos indican menor error ampliado; cada territorio aporta cinco años. Se trata de una descripción, sin inferencia causal.

Todos los años evaluados ya habían sido examinados en el proceso de investigación. En consecuencia, este contraste es exploratorio y dependiente de evidencia previa, sin confirmación independiente. La aceptación técnica comprueba coherencia local, integridad y reproducción de los cálculos, pero no autentica las fuentes ni verifica su disponibilidad temporal. El vínculo entre hogares residentes y estudiantes evaluados, y entre residencia y ubicación del colegio, es ecológico. Los pocos años disponibles y la dependencia entre observaciones territoriales limitan la generalización.

El último año utilizable en la evidencia local es {r['ultimo_anio_local']}. Las notas locales del anexo de pobreza registran actualización el 14 de abril de 2026, fecha que corresponde a publicación o actualización y no al año observado. Un año posterior solo podría evaluarse si se dispone de información comparable, autenticada y temporalmente documentada; aquí no se proyectan resultados. Antes de estudiar estimaciones condicionales posteriores se requieren esas comprobaciones y una evaluación prospectiva independiente. El contraste no ejecuta escenarios de reducción del IPM ni demuestra reducciones reales de pobreza o efectos causales sobre el puntaje. Tampoco equivale a ejecutar íntegramente las especificaciones y validaciones adicionales del diseño original de la tesis.
'''
    # Evidencia de decisiones/constantes y cifras de especificación usadas en el cuerpo.
    for key,value in [('alpha',[.1,1,10]),('max_depth',2),('min_samples_leaf',11),('indicadores',15),('tolerancias',.1),('anios_historia',[2018,2019]),('anios_eval',[2021,2022,2023,2024,2025]),('pares_por_territorio',5),('primer_externo',2021),('exclusion',2020)]:ev('SPEC_'+key,key,'ESPECIFICACION.json','reglas congeladas','documentary_constants.'+key,165,'regla',json.dumps(value),4,'analisis.academic_text')
    for i,name in enumerate(sorted(visual['files']),1):ev('FIG_'+str(i),'figura/unidades/n','resultados/figuras/'+name,'figura',name,33 if i==1 else 165,'puntos',visual['files'][name],3,'analisis.figures')
    datefile='resultados/FECHA_LOCAL.json';ev('FECHA','fecha actualización anexo local',datefile,'nota documental','fecha_local',0,'fecha','2026-04-14',4,'analisis.academic_text')
    save(HERE/'TEXTO_OBJETIVO3_TESIS.md',text)
    csv_save(HERE/'EVIDENCIAS_TEXTO.csv',pd.DataFrame(evidence))
    return dict(text_sha256=sha(HERE/'TEXTO_OBJETIVO3_TESIS.md'),evidence_rows=len(evidence),cell=4)
def text_control():
    text=(HERE/'TEXTO_OBJETIVO3_TESIS.md').read_text();ev=read_csv('EVIDENCIAS_TEXTO.csv')
    for _,r in ev.iterrows():check(sha(HERE/r.archivo)==r.sha256,'text evidence hash')
    check(not any(s in text.lower() for s in ['v6','v5','v2','ledger','runner','versión']),'academic language')
    r=load(HERE/'resultados/PRIMARIO.json')
    for key in ['MAE_historico','MAE_ampliado','MAE_con_pobreza','mejora_primaria_percent','mejora_secundaria_percent']:check(f'{r[key]:.3f}'.replace('.',',') in text,'text number '+key)
    result=dict(aprobado=True,text_sha256=sha(HERE/'TEXTO_OBJETIVO3_TESIS.md'),evidence_sha256=sha(HERE/'EVIDENCIAS_TEXTO.csv'),evidence_rows=len(ev),numeric_source='notebook executed calls shared functions',citations_invented=False)
    save(HERE/'CONTROL_TEXTO.json',result);return result
