"""Fijar las huellas de entrega después de controles, sin circularidad del manifiesto."""
import json
from integridad import ROOT, OUT, PARTIDA, CIERRE5, sha, guardar, cierre

def main():
    cierre()
    assert json.loads((OUT/'verificacion_final.json').read_text())['aprobado']
    assert json.loads((OUT/'verificacion_numerica.json').read_text())['aprobado']
    paths=[p for p in (ROOT/'fase6').rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json' and '__pycache__' not in p.parts]
    paths.append(ROOT/'CONTINUIDAD_OBJETIVO_3.md')
    guardar('manifiesto_cierre.json',dict(commit_partida=PARTIDA,cierre_anterior=CIERRE5,
        fecha_cliente='2026-10-09',fase='6: revisión y entrega local',
        entregables_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},
        excepcion_historia='informe raíz del usuario conservado; continuidad actualizada documentadamente',
        modelos_ajustados=0,simulaciones=0,push=False,aceptacion_editorial_grupo='pendiente externa'))
    print(f'Manifiesto final: {len(paths)} archivos')

if __name__=='__main__': main()
