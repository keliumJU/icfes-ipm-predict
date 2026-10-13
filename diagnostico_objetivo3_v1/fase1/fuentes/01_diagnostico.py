"""Fuente editable del notebook diagnóstico. Ejecutar desde raíz o subcarpeta del repo.
Solo lee panel/CSV/JSON/PNG guardados; no ajusta ni genera nuevas tablas.
Las secciones # %% se convierten a celdas por generar_notebook.py.
"""
# %%
from pathlib import Path
import sys
root = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / 'diagnostico_objetivo3_v1/fase1/fuentes/comun_diagnostico.py').exists())
sys.path.insert(0, str(root / 'diagnostico_objetivo3_v1/fase1/fuentes'))
from comun_diagnostico import environment, read_json, csv, OUT, TABLES, FIGS
env = environment()
audit = read_json(OUT / 'auditoria_diagnostico.json')
preflight = read_json(OUT / 'preflight_actual.json')
assert audit['aprobado'] and env['aprobado'] and preflight['reconstruccion_exacta']
print('DIAGNÓSTICO EXPLORATORIO. Cero fits;solo guardados;sin causalidad ni confirmación independiente.')
print('Python', env['python'], 'sklearn', env['sklearn'], 'paquetes', len(env['paquetes']), env['pip_check'])
print('Panel:', preflight['filas'], 'filas;', preflight['territorios'], 'territorios;', preflight['cambios'], 'cambios')
print('Internas:', audit['internos_originales'], 'originales;', audit['internos_unicos'], 'únicas;4años únicos')
print('Externas:', audit['externas'], '=7×165;seleccionesv5intactas;modeloscargados:', audit['modelos_deserializados'])

# %%
annual = csv(TABLES / 'estabilidad_anual.csv')
print(annual[['periodo', 'n', 'media', 'mediana', 'iqr', 'n_negativos', 'n_ceros', 'n_positivos']].to_string(index=False))
print('Unidades:puntos;2021 respecto2019,intervalo2,sin anualizar;restointervalo1.')
transitions = csv(TABLES / 'transiciones_signo.csv')
print(transitions.groupby(['anio_desde','anio_hasta']).cambia_signo.agg(['sum','size']).to_string())
print('Particionesoriginales completas en contrastes_particiones_originales.csv;no contar10como10años.')

# %%
variation = csv(TABLES / 'variacion_entradas.csv')
assoc = csv(TABLES / 'asociaciones_objetivo.csv')
pairs = csv(TABLES / 'asociaciones_entre_entradas.csv')
exact_pairs = csv(TABLES / 'redundancia_exacta.csv')
print('18entradasexactas:126resúmenes;', int(variation.constante_exacta.sum()), 'constantes;', int(variation.no_finitos.sum()), 'no finitos')
print('252asociacionesobjetivo;', len(pairs), 'entreentradas;', int(exact_pairs.iguales_exactamente.sum()), 'paresidénticos')
shown = assoc[(assoc.metodo == 'spearman') & assoc.entrada.isin(['puntaje_previo','ipm','cambio_ipm'])]
print(shown[['periodo','entrada','n','correlacion','razon']].to_string(index=False))
print('Pearson/Spearman completos en tablas;rangosmedios;sin p-valores/selección;correlación no es capacidadpredictiva.')

# %%
unique_metrics = csv(TABLES / 'metricas_internas_unicas.csv')
total = unique_metrics[unique_metrics.periodo == 'total']
print(total.groupby('familia').agg(configuraciones=('id','size'), n_por_configuracion=('n','first'),
                                 mae_min_descriptivo=('mae','min'), mae_max=('mae','max'),
                                 sesgo_min=('sesgo','min'), sesgo_max=('sesgo','max')).to_string())
print(csv(TABLES / 'conteos_ventaja_interna_por_anio.csv').to_string(index=False))
external_metrics = csv(TABLES / 'metricas_externas.csv')
print(external_metrics[(external_metrics.procedimiento=='global') &
                       (~external_metrics.periodo.str.startswith('territorio'))]
      [['periodo','n','mae','rmse','sesgo','delta_mae_pareado','direccion_acertada']].to_string(index=False))
print('Mínimos internos descriptivos;no nuevosganadores;35ajustados sinexternas,no fabricadas.')
print('Direcciónexacta−/0/+;persistencia0 no acierta cambiosno0 aunque tenga menorMAE.')

# %%
hypotheses = csv(TABLES / 'matriz_hipotesis.csv')
print(hypotheses[['id','hipotesis','estado','n']].to_string(index=False))
alternatives = csv(TABLES / 'alternativas_y_pruebas_futuras.csv')
print(alternatives[['alternativa','conclusion']].to_string(index=False))
print('Matrizcompleta:ubicación/favor/contra/impacto/alternativa/resolución/pendiente. Ningúnpunto departidamejorvalidado.')
print('Nuevoexperimento:requiere protocolo/autorización separados;no grilla/hiperparámetros fijados.')
print('Guainía238vs404/21.012106puntos,evidenciahistórica;procedencia local noautenticada;IPMhogares/alumnos;colegio/residencia;enlaceecológico;dependencia/pocosaños.')

# %%
# En el notebook, IPython muestra las imágenes; el generador captura los PNG reales.
for name in ['01_distribuciones_anuales.png','02_trayectorias_33.png','03_contrastes_particiones.png',
             '04_asociaciones_anuales.png','05_deltas_internos.png']:
    print(name)
    if 'mostrar_png' in globals():
        mostrar_png(FIGS / name)
    else:
        from IPython.display import display, Image
        display(Image(filename=str(FIGS / name)))
