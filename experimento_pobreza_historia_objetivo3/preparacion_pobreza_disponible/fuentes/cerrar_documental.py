"""Sella únicamente entrega documental preparada, sin ejecución posterior.

Entradas: archivos documentales y snapshot inicial. Salidas: manifiesto propio,
dictamen y cierre. Python estándar; sin presupuesto, semillas ni estimadores.
"""
from pathlib import Path
import hashlib,json,datetime,platform,subprocess,sys

HERE=Path(__file__).resolve().parents[1]

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def main():
    closure=dict(fecha_consulta='2026-10-12',cierre_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        estado='incompleto_documental_procedencia_disponibilidad',python=platform.python_version(),
        poppler=subprocess.check_output(['pdftotext','-v'],stderr=subprocess.STDOUT,text=True).splitlines()[0],
        fuentes_editables=['fuentes/documental.py','fuentes/leer_paginas.py','fuentes/generar_calendario.py','fuentes/registrar_lecturas.py','fuentes/cerrar_documental.py','verificar_documental.py'],
        procedimiento='lecturas/huellas previas -> documentación oficial por secciones -> calendario -> protocolo propuesto -> conservación/verificador',
        ajustes=0,nuevos_datasets_analiticos=0,escenarios=0,objetivo4_ejecutado=False,presupuesto_heredado=False,
        notebook_generado=False,motivo_sin_notebook='No añade valor a la preparación documental; fuentes .py y CSV documentales suficientes.',
        fechas_uso_aprobadas=False,procedencia_valores_locales_resuelta=False,disponibilidad_indispensable_resuelta=False,
        originales_preservados='Todas las huellas previas de archivos regulares sin symlinks salvo continuidad propia, preservada íntegra; inventario excluye Git/runtime/cache. Destinos de enlaces sin baseline inicial: no certificación retrospectiva.',
        consultas_externas='Solo documentación oficial DANE/ICFES; se archivaron ocho documentos/imágenes, no bases ni anexos de datos.',
        pendientes=['autenticar vintages y disponibilidad de valores','fechas y revisiones de ambas bases Saber por año','fecha de uso/corte','cobertura y protocolo antes de resultados','criterios, candidatos y presupuesto nuevos si se autoriza'],
        avance_automatico=False)
    (HERE/'CIERRE_DOCUMENTAL_DISPONIBILIDAD.json').write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n')
    exclude=['MANIFIESTO_DOCUMENTAL.json','VERIFICACION_DOCUMENTAL.json']
    files={p.relative_to(HERE).as_posix():sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.relative_to(HERE).as_posix() not in exclude}
    manifest=dict(version='1.0',sha256=files,exclusiones=exclude,alcance='inventario ampliado propio; no modifica manifiestos anteriores')
    (HERE/'MANIFIESTO_DOCUMENTAL.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    # Placeholder makes the full closed inventory present before read-only verification.
    report=HERE/'VERIFICACION_DOCUMENTAL.json'
    report.write_text('{}\n')
    p=subprocess.run([sys.executable,'-B',str(HERE/'verificar_documental.py')],capture_output=True,text=True)
    if p.returncode:
        report.write_text(json.dumps(dict(aprobado_integridad_documental=False,error=p.stderr),ensure_ascii=False,indent=2)+'\n')
        raise RuntimeError(p.stderr)
    result=json.loads(p.stdout)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
