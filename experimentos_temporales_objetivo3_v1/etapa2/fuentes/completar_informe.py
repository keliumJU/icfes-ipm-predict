"""Resultados concretos y comparación interna; solo tablas auditadas."""
from auditar import E2,OUT,csv

def main():
    r=csv(OUT/'tablas/registros_144.csv');s=csv(OUT/'tablas/selecciones.csv');m=csv(OUT/'tablas/metricas_externas.csv')
    assert s.id.eq('persistencia').all() and len(s)==35
    q=m[(m.corte=='global')&(m.procedimiento=='global')].iloc[0]
    text='''\n## Resultado concreto de la selección

Global y los cinco grupos seleccionaron persistencia en2022–2025;2021 fue fijo.
Por eso las siete salidas externas coinciden, todas las diferencias por año y
territorio frente a referencia son0 y el cambio predicho es0 en los165 pares.
Esto muestra que recencia no cambió la política seleccionada en este piloto;
no demuestra que los ajustes ponderados sean idénticos a los uniformes ni que
recencia nunca pueda aportar señal. Ubicación: tablas/selecciones.csv,35filas;
seleccion_2021.json–seleccion_2025.json y predicciones_externas.csv.

|Ventana externa|MAE interno persistencia|Candidato ajustado con menor MAE interno|MAE interno ajustado|Diferencia ajustado−persistencia (puntos)|
|---|---:|---|---:|---:|
'''
    for ext,part in r.groupby('externo'):
        p=part[part.id=='persistencia'].iloc[0];best=part[part.id!='persistencia'].sort_values('mae').iloc[0]
        text+=f'|{int(ext)}|{p.mae!r}|{best.id}|{best.mae!r}|{float(best.mae-p.mae)!r}|\n'
    text+=f'''
Estas diferencias internas son descriptivas: se conserva el selector contractual
MAE/RMSE/bandas0.1/entradas/familia/orden; la tabla no redefine ganadores ni emplea
externas. Todos35 ajustados quedan por encima de persistencia en cada selección
acumulada. Ubicación: tablas/registros_144.csv,36registros porventana, sin nuevas
puntuaciones de2021. Reproducción actual con pesos, distinto de resultados históricos.

RMSE externo global {q.rmse!r} puntos; sesgo(predicho−observado) {q.sesgo!r} puntos.
Dirección exacta correcta {int(q.direccion_aciertos)}/165 ({q.direccion_porcentaje!r}%)
bajo signo−/0/+; magnitud media observada {q.magnitud_observada_media!r} puntos y
predicha {q.magnitud_predicha_media!r} puntos. No se interpreta la dirección como
criterio alternativo de éxito. Ubicación: tablas/metricas_externas.csv,corte=global,
procedimiento=global; tablas/predicciones_errores_pareados.csv,165filas global.

Control adicional independiente:360firmas de train y350metadatos cotejados contra
los años exactos anteriores a validación, matrices/objetivos y pesos; escala/suma
ponderada del scaler; cinco persistencias recalculadas sinfit. Resultado aprobado
pruebas_contextos.json,procedimiento fuentes/comprobar_contextos.py. Los3gráficos
se revisaron visualmente completos: ejes/títulos/unidades/n legibles; delta0 territorial
es resultado exacto, no ausencia de cobertura.
'''
    with (E2/'INFORME.md').open('a') as f:f.write(text)
if __name__=='__main__':main()
