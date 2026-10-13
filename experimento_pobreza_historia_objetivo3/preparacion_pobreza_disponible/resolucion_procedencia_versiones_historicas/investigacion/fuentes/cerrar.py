"""Crear controles propios tras acabar documentos; no modificar controles previos."""
from iniciar import HERE,sha
import json,datetime,sys
if __name__=='__main__':
    assert not (HERE/'MANIFIESTO.json').exists(),'Cierre ya existe; no sobrescribir'
    closing=dict(fecha_cliente='2026-10-12 America/Bogota',fecha_cierre_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),estado='CIERRE DOCUMENTAL INCOMPLETO',entrega_documental='COMPLETADA HASTA EVIDENCIA AUTORIZADA',fecha_uso=None,pendientes=['Sellado histórico de contenido/ediciones DANE y revisiones por corte','Identidad de 14 TXT ICFES con publicación/revisiones/diccionario','Uso/corte humano pendiente','Cobertura y protocolo de evaluación futuro por decidir'],fits=0,repeticiones=0,escenarios=0,modelos=0,datasets_analiticos_nuevos=0,objetivo4=False,avance_automatico=False)
    (HERE/'CIERRE.json').write_text(json.dumps(closing,ensure_ascii=False,indent=2)+'\n')
    ex=['MANIFIESTO.json','VERIFICACION.json']
    files={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and p.name not in ex}
    (HERE/'MANIFIESTO.json').write_text(json.dumps(dict(sha256=files,exclusiones=ex,limite='Integridad de la entrega; no sello institucional histórico.'),ensure_ascii=False,indent=2)+'\n')
    sys.path.insert(0,str(HERE))
    from verificar import verify
    # Crear primero salida prevista vacía para inventario cerrado; verificar solo lectura.
    (HERE/'VERIFICACION.json').write_text('{}\n')
    result=verify(True)
    (HERE/'VERIFICACION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
