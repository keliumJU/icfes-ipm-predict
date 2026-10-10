"""Reejecutar la auditoría encontrada sin sobrescribirla ni tocar fuentes."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from integridad import ROOT, V2, OUT, sha, save, verificar_conservacion

def main():
    verificar_conservacion()
    previous = {str(p.relative_to(ROOT)): sha(p) for p in V2.rglob('*')
                if p.is_file() and '__pycache__' not in p.parts}
    temp = Path(tempfile.mkdtemp(prefix='icfes-v2-fase1-'))
    for p in ROOT.iterdir():
        if p.name != V2.name:
            (temp / p.name).symlink_to(p, target_is_directory=p.is_dir())
    shutil.copytree(V2, temp / V2.name)
    runs = []
    for relative in ['fuentes/auditar_2025.py', 'fuentes/investigar_identificadores.py',
                     'fuentes/documentar.py', 'pruebas/test_auditoria.py']:
        process = subprocess.run([sys.executable, '-B', str(temp / V2.name / 'fase1' / relative)],
                                 cwd=temp, capture_output=True, text=True)
        runs.append(dict(procedimiento=relative, codigo_salida=process.returncode))
        print(relative, process.returncode, flush=True)
        if process.returncode:
            print(process.stderr[-4000:])
            raise RuntimeError(relative)
    same, different = [], []
    for directory in ['resultados', 'reconstrucciones']:
        for p in sorted((V2 / 'fase1' / directory).rglob('*')):
            if not p.is_file() or p.name in ['reproduccion_actual.json', 'verificacion_reproduccion_actual.json',
                                            'pruebas_reproduccion_actual.json', 'manifiesto_cierre.json',
                                            'conservacion_final.json']:
                continue
            other = temp / p.relative_to(ROOT)
            if other.exists():
                (same if sha(p) == sha(other) else different).append(str(p.relative_to(ROOT)))
    allowed = {str((OUT / n).relative_to(ROOT)) for n in ['verificacion_auditoria.json', 'pruebas_auditoria.json']}
    assert set(different) <= allowed, different
    current = json.loads((temp / V2.name / 'fase1/resultados/verificacion_auditoria.json').read_text())
    old = json.loads((OUT / 'verificacion_auditoria.json').read_text())
    assert {k:v for k,v in current.items() if k not in ['duracion_segundos', 'entorno']} == {
        k:v for k,v in old.items() if k not in ['duracion_segundos', 'entorno']}
    for p, h in previous.items():
        assert sha(ROOT / p) == h, p
    verificar_conservacion()
    save(OUT / 'verificacion_reproduccion_actual.json', current)
    save(OUT / 'pruebas_reproduccion_actual.json', json.loads(
        (temp / V2.name / 'fase1/resultados/pruebas_auditoria.json').read_text()))
    save(OUT / 'reproduccion_actual.json', dict(fecha_cliente='2026-10-10', aprobado=True,
        commit_real=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        copia_temporal=str(temp), procedimientos=runs, archivos_identicos=same,
        diferencias_solo_duracion_o_entorno=different,
        entregables_encontrados_conservados=previous,
        paginas_pdf_leidas_en_esta_ejecucion=[], raw_auditado=['20251', '20252'],
        entrenamiento=False, predicciones=False, simulacion=False))
    print(json.dumps(dict(aprobado=True, identicos=len(same), diferentes=different)), flush=True)

if __name__ == '__main__':
    main()
