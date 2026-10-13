"""Congela infraestructura documental probada, sin modificar congelación científica."""
from infra_correccion import *
from verificar_entrega_corregida import preserved
def run():
    deadline();preserved();check(load(HERE/'PRUEBA_NOTEBOOK_INVENTADO.json')['aprobado'],'prueba inventada')
    check(not (HERE/'CONGELACION_DOCUMENTAL.json').exists(),'no congelación previa de corrección')
    files=['infra_correccion.py','preflight_documental.py','notebook_corregido.py','generar_notebook_corregido.py','verificar_entrega_corregida.py','congelar_documental.py','cerrar_documental.py']
    mapping={'correccion_documental/'+p:sha(HERE/p) for p in files}
    mapping.update({p:sha(MAIN/p) for p in ['analisis.py','notebook_resultados.py','auditor.py','ESPECIFICACION.json','CANDIDATOS.csv','CONGELACION.json','piloto/ledger.json','piloto/PREDICCIONES.csv','piloto/POLITICAS.csv','piloto/SELECCIONES.json']})
    save(HERE/'CONGELACION_DOCUMENTAL.json',dict(aprobado=True,epoch=time.time(),sha256=mapping,new_fits=0,scientific_changes=False,original_freeze_modified=False,modifications='gestor kernel asíncrono, entorno antes imports, reloj documental y guardia cero fits; funciones científicas sin cambios'))
    print(json.dumps(dict(aprobado=True,files=len(mapping),new_fits=0)))
if __name__=='__main__':run()
