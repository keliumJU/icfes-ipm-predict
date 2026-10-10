"""Revisar IDs repetidos sin serializar IDs ni atributos personales."""
import csv
import hashlib
from collections import defaultdict
from integridad import ROOT, OUT, save

def main():
    seen = set()
    repeated = set()
    for per in ['20251', '20252']:
        with (ROOT / f'raw_data/Examen_Saber_11_{per}.txt').open(encoding='utf-8-sig', newline='') as f:
            r = csv.DictReader(f, delimiter=';')
            for row in r:
                value = row['estu_consecutivo']
                h = hashlib.sha256(value.encode()).digest()
                if h in seen:
                    repeated.add(h)
                seen.add(h)
    occurrences = defaultdict(list)
    for per in ['20251', '20252']:
        with (ROOT / f'raw_data/Examen_Saber_11_{per}.txt').open(encoding='utf-8-sig', newline='') as f:
            r = csv.DictReader(f, delimiter=';')
            for line, row in enumerate(r, 2):
                h = hashlib.sha256(row['estu_consecutivo'].encode()).digest()
                if h not in repeated:
                    continue
                full = hashlib.sha256('\x1f'.join(row.values()).encode()).digest()
                scores = ['punt_global', 'punt_matematicas', 'punt_lectura_critica', 'punt_c_naturales', 'punt_sociales_ciudadanas', 'punt_ingles']
                positive = all(row[c].replace('.', '', 1).isdigit() and float(row[c]) > 0 for c in scores)
                eligible = row['estu_estudiante'].strip().upper() == 'ESTUDIANTE' and row['estu_privado_libertad'].strip().upper() != 'S' and row['estu_grado'] == '11' and bool(row['cole_cod_depto_ubicacion']) and positive
                occurrences[h].append(dict(periodo=per, linea_csv=line, grado=row['estu_grado'],
                    elegible=eligible, _full=full))
    result = []
    for ix, obs in enumerate(sorted(occurrences.values(), key=lambda x: (x[0]['periodo'], x[0]['linea_csv'])), 1):
        distinct = len({r['_full'] for r in obs})
        result.append(dict(grupo=ix, ocurrencias=len(obs), filas_completas_distintas=distinct,
            elegibles=sum(r['elegible'] for r in obs), ubicaciones=[{k:v for k,v in r.items() if k != '_full'} for r in obs]))
    save(OUT / 'identificadores_repetidos_revision.json', dict(grupos=result,
        ids_serializados=False, firmas_serializadas=False,
        repeticiones_misma_fila=sum(len(obs)-len({r['_full'] for r in obs}) for obs in occurrences.values())))
    print(result)

if __name__ == '__main__':
    main()
