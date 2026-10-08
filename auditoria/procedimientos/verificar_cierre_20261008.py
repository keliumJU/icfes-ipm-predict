"""Conservación de insumos y revisión de la entrega vigente, sin modelos."""
from pathlib import Path
import csv, hashlib, json, sys, importlib.metadata as metadata
from collections import Counter
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];AUD=ROOT/'auditoria';NEW=AUD/'evidencia/actualizacion_20261008'

def main():
    inventory=pd.read_csv(AUD/'inventario_trazabilidad.csv',keep_default_na=False)
    assert len(inventory)==51 and inventory.archivo.is_unique
    files=0
    for r in inventory.to_dict('records'):
        path=ROOT/r['archivo']
        if r['tipo']=='directorio vacío':
            assert path.is_dir() and not any(path.iterdir());continue
        digest=hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda:stream.read(8*1024*1024),b''):digest.update(block)
        assert path.stat().st_size==int(r['bytes']),r['archivo']
        assert digest.hexdigest()==r['sha256'],r['archivo']
        files+=1
    validation=json.loads((NEW/'validacion_reconstruccion.json').read_text())
    assert validation['reconstruccion_validada'] and all(validation['condiciones'].values())
    assert validation['cotejos_agregacion_independiente']==2574
    ledger=pd.read_csv(NEW/'cotejo_agregacion_raw_final.csv')
    assert len(ledger)==2574 and ledger.delta_raw_menos_final.eq(0).all()
    base=pd.read_csv(AUD/'base_analitica_departamento_anio.csv',dtype={'codigo_departamento':str})
    assert len(base)==198 and not base.isna().any().any()
    assert not base.duplicated(['codigo_departamento','anio']).any()
    assert base.codigo_departamento.str.fullmatch(r'\d{2}').all()
    assert base.groupby('anio').size().eq(33).all() and base.n_estudiantes_saber.sum()==2984199
    dictionary=pd.read_csv(AUD/'diccionario_base_analitica.csv')
    assert list(dictionary.variable)==list(base.columns)
    claims=pd.read_csv(AUD/'auditoria_afirmaciones.csv',keep_default_na=False)
    assert len(claims)==59 and claims.id.is_unique
    assert all(claims.ubicacion) and all(claims.evidencia_verificable)
    assert 'dictamen_20261007' in claims
    required=['diagnostico_calidad.md','mapa_tesis.md','propuesta_correccion_tesis.md',
              'respuestas_pendientes_20261008.md','procedimientos/README.md']
    assert all((AUD/p).exists() for p in required)
    versions={p:metadata.version(p) for p in ['pandas','numpy','openpyxl']}
    result={'fecha_cliente':'2026-10-08','archivos_insumo_tamano_sha256_verificados':files,
            'directorios_vacios':2,'datasets_ignorados':int(inventory.estado_git.eq('ignorado').sum()),
            'base_filas':198,'registros_base':2984199,'cotejos_agregacion_raw_final':2574,
            'dictamenes_actuales':dict(Counter(claims.dictamen)),
            'python_actual':sys.version,'paquetes_actuales_no_historicos':versions,
            'modelos_entrenados':0,'fase2_ejecutada':False,
            'fase1_cerrada_alcance_local':True,
            'salvedades':'Autenticación de descarga, criterio histórico59, causa antigua20212 y métricas históricas no verificadas; explicación aritmética de puntajes desconocida. Ver diagnóstico.',
            'gitignore':'Cambio del usuario previo a sesión, conservado y excluido del commit de auditoría'}
    (NEW/'verificacion_cierre.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
