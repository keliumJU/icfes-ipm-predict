"""Redacción desde salidas de notebook; se invoca solamente después de revisión visual."""
from comun import *
from resultados import OUT,TABLES,readcsv,label_candidate
import pandas as pd,numpy as np
class Evidencias:
    def __init__(self):self.rows=[]
    def record(self,claim,value,file,key,n,unit,cell,function):
        kind='int' if isinstance(value,(int,np.integer)) and not isinstance(value,bool) else 'float' if isinstance(value,(float,np.floating)) else 'label'
        self.rows.append(dict(claim=claim,value=str(value),kind=kind,cell=cell,function=function,file=str(file.relative_to(HERE)),table=file.stem,key=key,n=n,unit=unit,sha256=sha(file)))
        return value
    def j(self,claim,key,file,cell,function,unit='conteo',n=165):
        v=load(file)
        for part in key.split('.'):v=v[int(part)] if part.isdigit() else v[part]
        return self.record(claim,v,file,key,n,unit,cell,function)
    def scalar(self,claim,file,index,column,cell,function,unit='puntos',n=165):
        df=readcsv(file);v=df.iloc[index][column];return self.record(claim,v,file,str(index)+':'+column,n,unit,cell,function)
    def table(self,file,df,columns,cell,function,headers=None):
        # Índices originales mantienen la ubicación en el CSV íntegro.
        lines=['| '+' | '.join(headers or columns)+' |','| '+' | '.join(['---']*len(columns))+' |']
        for idx,row in df.iterrows():
            rendered=[]
            for col in columns:
                v=row[col];unit='puntos' if 'MAE' in col or 'RMSE' in col or col=='bias' else 'porcentaje' if 'improvement' in col else 'conteo' if col in ['n','direction_matches','b_improves','b_worsens','ties'] else 'año' if col=='year' else 'identificador/descripción'
                self.record(file.stem+':'+str(idx)+':'+col,v,file,str(idx)+':'+col,row.get('n',165),unit,cell,function)
                rendered.append(f'{v:.4f}'.replace('.',',') if isinstance(v,(float,np.floating)) and unit in ['puntos','porcentaje'] else str(int(v)) if col in ['year','n','direction_matches','b_improves','b_worsens','ties'] else str(v))
            lines.append('| '+' | '.join(rendered)+' |')
        return '\n'.join(lines)
    def finish(self):
        pd.DataFrame(self.rows).to_csv(HERE/'EVIDENCIAS_TEXTO.csv',index=False)
        from control_evidencias import validate
        control=validate();control.update(text_sha=sha(HERE/'TEXTO_OBJETIVO3_TESIS.md'),evidence_sha=sha(HERE/'EVIDENCIAS_TEXTO.csv'),cell=7,function='redaccion.thesis',method='interpolación de salidas notebook; valor/llave exactos y SHA cotejados')
        save(OUT/'CONTROL_TEXTO.json',control);return control

def thesis():
    check(load(OUT/'AUDITORIA.json')['aprobado'] and load(OUT/'REVISION_VISUAL.json')['aprobado'],'texto al final de auditoría y QA')
    e=Evidencias();p=load(OUT/'PRIMARIO.json');design=load(OUT/'DISENO_RECALCULADO.json');hist=readcsv(TABLES/'antecedentes_recalculados.csv');availability=load(OUT/'DISPONIBILIDAD.json')
    def primary(key,precision=6):
        value=e.j(key,key,OUT/'PRIMARIO.json',4,'resultados.analyse','porcentaje' if 'percent' in key else 'puntos' if 'MAE' in key or 'RMSE' in key or 'bias' in key else 'conteo')
        return f'{value:.{precision}f}'.replace('.',',') if isinstance(value,(float,int)) and precision else str(int(value))
    def d(key):return e.j('diseño '+key,key,OUT/'DISENO_RECALCULADO.json',6,'resultados.complementary_tables','año' if key in ['historical_level','historical_change','excluded_year','first_supervised','previous2021'] else 'puntos' if key=='selection_band' else 'identificador' if key=='seed' else 'conteo',design['level_rows'])
    for key in ['years','external_years','seed','internal_windows','selection_band']:d(key)
    def historical(label,column,precision=6):
        idx=hist.index[hist.label==label][0];v=e.scalar(label+' '+column,TABLES/'antecedentes_recalculados.csv',int(idx),column,3,'resultados.antecedents','puntos' if column=='MAE' else 'porcentaje')
        return f'{v:.{precision}f}'.replace('.',',')
    annualfile=TABLES/'tabla_academica_anual.csv';annual=readcsv(annualfile)
    annualtable=e.table(annualfile,annual,['procedimiento','year','n','MAE','RMSE','bias','direction_matches'],4,'resultados.analyse',headers=['Procedimiento','Año','n','MAE','RMSE','Sesgo','Dirección coincidente'])
    decfile=TABLES/'tabla_academica_selecciones.csv';dec=readcsv(decfile);dectable=e.table(decfile,dec,['year','procedimiento'],6,'resultados.complementary_tables',headers=['Año evaluado','Procedimiento elegido con años anteriores'])
    cf=TABLES/'tabla_academica_contrastes.csv';contr=readcsv(cf);ct=e.table(cf,contr,['comparacion','MAE_a','MAE_b','MAE_difference_b_minus_a','b_improves','b_worsens','ties'],6,'resultados.complementary_tables',headers=['Comparación A → B','MAE A','MAE B','Diferencia B − A','B mejora','B empeora','Empates'])
    diagfile=OUT/'DIAGNOSTICO_SELECCION.json'
    def diag(key):return e.j('diagnóstico '+key,key,diagfile,6,'resultados.complementary_tables','conteo' if key!='selected_constant' else 'puntos')
    zero=diag('coef_zero_fits');nf=diag('coef_audited_fits');different=diag('different_midpoint');check(diag('all_median_interval'),'afirmación intervalo mediana');year=diag('year');constant=diag('selected_constant');nh=diag('n_historical');diag('eligible_years')
    gu=TABLES/'guainia_historico.csv';ngu=e.scalar('Guainía completos',gu,0,'n_complete',3,'resultados.antecedents','registros');nglobal=e.scalar('Guainía global disponible',gu,0,'n_global',3,'resultados.antecedents','registros');gdiff=e.scalar('Guainía diferencia',gu,0,'difference',3,'resultados.antecedents','puntos')
    last=e.j('último año local','last_usable_year',OUT/'DISPONIBILIDAD.json',3,'resultados.antecedents','año',design['level_rows']);nextyear=e.j('siguiente año condicional','next_year_conditional',OUT/'DISPONIBILIDAD.json',3,'resultados.antecedents','año',design['level_rows'])
    result='se alcanzó' if p['target_met'] else 'no se alcanzó'
    text=f'''# Objetivo 3. Diseño y evaluación exploratoria de la predicción departamental

### Unidad de análisis y alcance de la evaluación

Se evaluó la capacidad de distintos procedimientos para estimar el puntaje global promedio de Saber 11 a nivel departamental. La unidad de observación fue el par territorio-año, considerando los departamentos y Bogotá D. C. según la ubicación del establecimiento educativo. Se conservaron los registros de estudiantes de grado once, sin privación de libertad reportada y con puntajes presentes y positivos en las pruebas y en el global, sin restringir el calendario. La variable de resultado fue la media del puntaje global recibido. Cada territorio-año recibió el mismo peso; por tanto, las métricas no representan un promedio nacional ponderado por el número de estudiantes.

El objetivo planteado en la investigación considera la predicción a partir del IPM y sus indicadores. Para examinar su desempeño, se recalcularon las métricas de las predicciones departamentales ya obtenidas con indicadores de pobreza y se contrastaron con una referencia temporal. Como evaluación complementaria, se examinó si el nivel histórico y el rezago de los cambios del puntaje ofrecían una mejora adicional. Este contraste complementario incorpora exclusivamente información histórica del resultado; su eventual mejora no constituye evidencia de aprendizaje del IPM.

El panel local reunió {d('level_rows')} observaciones de nivel para {d('territories')} territorios. Se conservaron niveles desde {d('historical_level')} y se excluyó {d('excluded_year')}. La evaluación reunió {primary('n',0)} pares entre {design['external_years'][0]} y {last}. La inclusión de la última anualidad amplió de manera exploratoria el periodo originalmente formulado en la investigación. Los datos se analizaron como agregados locales conservados; su coherencia y sus huellas no demuestran por sí solas autenticidad oficial ni disponibilidad en la fecha en que se habría emitido una predicción.

### Diseño temporal y procedimientos examinados

La persistencia se definió como la predicción del puntaje del año anterior disponible para el mismo territorio. El cambio observado correspondió a la diferencia entre el puntaje actual y ese antecedente. En {d('first_supervised')}, el año previo fue {d('previous2021')}; ese cambio no se anualizó. El cambio de {d('historical_change')} se conservó como historial, sin utilizarlo como respuesta supervisada, dado que no se dispone de un cambio anterior que permita construir su rezago.

Las respuestas de entrenamiento precedieron estrictamente al año evaluado. Las variantes de historia reciente tomaron las últimas respuestas anuales elegibles después de comprobar sus rezagos, conservando los niveles necesarios para construirlas. Cuando no hubo respuestas elegibles, se utilizó persistencia; con una respuesta anual completa se permitió estimar el procedimiento. El primer año de evaluación mantuvo persistencia fija, sin ajuste ni selección. Para las anualidades posteriores se emplearon validaciones internas acumuladas de años anteriores, y la decisión se guardó antes de generar la predicción externa.

Se examinaron {d('candidates')} candidatos previamente definidos: persistencia; media y mediana de cambios históricos; regresiones de mediana con rezago y distintas penalizaciones; Ridge; árboles de profundidad limitada; estimaciones del cambio común; y combinaciones de cambio común con corrección territorial. El cambio común fue la mediana de los cambios territoriales de cada año, mientras que la corrección fue la diferencia entre el cambio territorial y ese componente. El componente común empleó una observación por año; los componentes territoriales conservaron las observaciones de cada territorio. Estas unidades de entrenamiento no equivalen a estudiantes independientes.

Cada estimación utilizó exclusivamente los años autorizados para su ventana. La estandarización se calculó con el entrenamiento correspondiente, y los componentes se ajustaron de forma independiente. El puntaje previsto se reconstruyó sumando el cambio estimado al puntaje previo, sin recortarlo ni calibrarlo con el año evaluado. Las medias y medianas históricas se trataron como estimaciones, aunque no necesitaran un algoritmo de ajuste iterativo.

La selección se basó en el MAE interno: se conservaron los candidatos situados hasta 0,1 puntos por encima del mínimo. Dentro de ese grupo se aplicó la misma banda al RMSE, y se prefirieron menos entradas predictoras y el orden previamente establecido. Las estadísticas constantes contaron como procedimientos sin entradas predictoras y la persistencia tuvo prioridad en el desempate. La evaluación principal correspondió al procedimiento completo de selección, sin sustituirlo por un candidato elegido por sus resultados externos.

### Resultado principal

El procedimiento con indicadores de pobreza presentó un MAE de {historical('v2_global','MAE')} puntos. Sobre las mismas observaciones, la persistencia obtuvo {historical('v3_persistencia','MAE')} puntos, una reducción descriptiva del {historical('v3_persistencia','improvement_vs_reference')} % respecto al primero. Estas cifras corresponden a recálculos de predicciones ya guardadas. La comparación no demuestra que el IPM carezca de utilidad en general; muestra que el procedimiento examinado no superó esta referencia temporal bajo las condiciones evaluadas.

En el contraste complementario, el procedimiento seleccionado alcanzó un MAE de **{primary('global_MAE')} puntos** y un RMSE de **{primary('global_RMSE')} puntos**, frente al MAE de persistencia de **{primary('reference_MAE')} puntos**. La reducción relativa del MAE fue **{primary('improvement_percent')} %**. En consecuencia, **{result} la meta previamente establecida de {primary('target_percent',0)} % de mejora adicional**. El sesgo promedio fue de {primary('global_bias')} puntos; su signo negativo indica subestimación media del puntaje.

Tabla A. Selecciones realizadas con validaciones de años anteriores. La primera anualidad mantuvo persistencia fija.

{dectable}

La selección conservó persistencia hasta la penúltima anualidad y eligió la mediana histórica del cambio territorial en {year}. Para ese año, el cambio constante estimado fue de {format(constant,'.6f').replace('.',',')} puntos, a partir de {nh} cambios territoriales históricos. La mejora agregada del procedimiento provino de esa última anualidad; no debe interpretarse como un avance uniforme durante todo el periodo.

En la comparación pareada, el procedimiento redujo el error absoluto en {primary('improves',0)} observaciones, lo aumentó en {primary('worsens',0)} y empató en {primary('ties',0)}. La dirección prevista del cambio coincidió con la observada en {primary('direction_matches',0)} pares. La persistencia prevé cambio nulo, por lo que este indicador exige igualdad de signo, incluido el cero; no equivale a acertar la magnitud del cambio ni reemplaza al MAE.

### Errores por año y territorio

La tabla B presenta el error absoluto, el error cuadrático, el sesgo y la coincidencia de dirección. Las métricas se expresan en puntos del puntaje global; un sesgo positivo indica sobreestimación. Las variaciones anuales muestran que la mejora agregada convive con diferencias de magnitud y signo que deben conservarse en la interpretación.

{annualtable}

Figura A. Error absoluto medio y sesgo por año. Ambas series coinciden cuando se seleccionó persistencia; cada anualidad conserva el mismo peso territorial.

![Error y sesgo por año](fase3/figuras/01_error_y_sesgo_anual.png)

Figura B. Puntajes observados y previstos del procedimiento seleccionado. La línea de identidad permite examinar la magnitud y dirección de las desviaciones, sin atribuirles una interpretación causal.

![Puntajes observados y previstos](fase3/figuras/02_observado_previsto.png)

Figura C. Diferencia del MAE territorial respecto a persistencia. Los valores negativos indican reducción del error; los positivos muestran deterioro. Las comparaciones abarcan el periodo completo y no excluyen territorios desfavorables.

![Diferencias territoriales del error](fase3/figuras/03_diferencias_territoriales.png)

### Nivel histórico, rezago y complejidad del procedimiento

La tabla C reúne contrastes descriptivos sobre las mismas observaciones. Los candidatos individuales se presentan como diagnósticos del diseño y no sustituyen el resultado del procedimiento seleccionado, aunque alguno tenga menor error externo. La diferencia corresponde al MAE del segundo procedimiento menos el del primero. Las comparaciones por pérdida y por árbol modifican más de un aspecto del estimador, por lo que no permiten atribuir sus diferencias exclusivamente a la pérdida o a la no linealidad. Las tablas completas conservan todos los candidatos y contrastes examinados.

{ct}

La incorporación del rezago sin penalización presentó un error superior al de la mediana histórica. La penalización más elevada examinada redujo el error de esa regresión; sin embargo, su coeficiente de rezago fue nulo en {zero} de {nf} ajustes auditados con historia completa. En esas estimaciones, el procedimiento operó como un nivel constante del cambio. Por ello, la mejora no demuestra que se hubiera aprendido una dependencia temporal activa. Para distinguir un nivel histórico aprendido de un aporte activo del rezago, se examinaron los coeficientes y se compararon las predicciones con las estimaciones históricas sobre las mismas respuestas elegibles.

La regresión de mediana puede admitir un intervalo de soluciones cuando el conjunto de respuestas tiene tamaño par. En {different} ajustes auditados, el intercepto difirió del promedio de los dos valores centrales, aunque permaneció en el intervalo de medianas. Esta diferencia ayuda a interpretar por qué una regresión con coeficiente nulo no necesariamente reproduce exactamente la mediana estadística utilizada como referencia. No se reemplazó ninguna de las dos convenciones para favorecer sus métricas.

La reducción de la historia produjo cambios descriptivos pequeños en el contraste presentado, con mejoras y deterioros en distintos pares. Los árboles limitados redujeron el error frente a la regresión sin penalización del contraste, sin que ello los convierta en el resultado principal. La corrección territorial tampoco aportó una ventaja uniforme: sin penalización aumentó ligeramente el MAE del componente común, mientras que con la penalización elevada ambos procedimientos coincidieron. Estos resultados se refieren a los parámetros, muestras y ventanas examinados; no establecen superioridad universal de una familia ni autorizan una selección retrospectiva por el mejor error externo.

### Limitaciones e interpretación del objetivo

Todos los años de evaluación habían sido observados durante el desarrollo del análisis. Las separaciones temporales evitan incorporar el año evaluado al ajuste y a la selección de su ventana, pero no constituyen una confirmación independiente del diseño. Los pares comparten territorios y años, y las copias de validaciones internas no son nuevas observaciones. Ante el reducido número de anualidades, los resultados se presentan como descriptivos y exploratorios, sin pruebas confirmatorias de significación ni intervalos de incertidumbre no estimados.

La población utilizada también delimita la interpretación. El diagnóstico histórico de Guainía registró {int(ngu)} observaciones con puntajes completos frente a {int(nglobal)} con global disponible, con una diferencia de {format(gdiff,'.6f').replace('.',',')} puntos entre sus medias. Se conservó la población y la media previamente definidas; esta diferencia se reporta como antecedente de sensibilidad de la agregación, sin modificar el análisis para mejorar sus resultados. El IPM caracteriza hogares, mientras que Saber 11 corresponde a estudiantes evaluados; además, el departamento del colegio no equivale necesariamente al de residencia. Estas diferencias impiden trasladar directamente los resultados agregados a relaciones individuales.

La revisión técnica verificó conservación, fechas de entrenamiento, matrices, selección y correspondencia de las predicciones guardadas. Esta aceptación no autentica la fuente local, no establece su disponibilidad histórica y no demuestra pronóstico anticipado. Asimismo, el contraste dinámico complementa la evaluación con indicadores de pobreza, pero no valida íntegramente las especificaciones, pruebas de robustez y reservas originalmente propuestas, ni permite atribuir cambios del puntaje a modificaciones del IPM.

Los resultados permiten documentar el diseño y desempeño de los procedimientos examinados y reconocer la persistencia como una referencia exigente. La mejora adicional del procedimiento seleccionado fue limitada y no cumplió el umbral establecido. El alcance del objetivo queda delimitado por esta evaluación exploratoria: no se demuestra utilidad incremental del IPM ni capacidad de anticipación independiente. El último año utilizable comprobado en el panel local fue {last}; la siguiente anualidad sería {nextyear}, de manera condicional a información comparable y disponibilidad verificable. No se estimaron puntajes de esa anualidad ni escenarios de modificación de la pobreza.
'''
    save(HERE/'TEXTO_OBJETIVO3_TESIS.md',text)
    control=e.finish();print({'texto_guardado':True,'control':control,'fits_redaccion':0});return control
