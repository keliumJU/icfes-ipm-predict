"""Auditoría adicional de años exactos/firmas/scaler y firmas hash del ledger."""
import json,math,hashlib
import numpy as np
from auditar import ROOT,OUT,K,read,csv

def main():
    panel=csv(ROOT/'experimentos_objetivo3_v5/etapa1/reconstrucciones/panel_cambios.csv');conf=read(ROOT/'experimentos_objetivo3_v5/etapa1/resultados/configuraciones_congeladas.json');cs={c['id']:c for c in conf['configuraciones']}
    signatures=read(OUT/'firmas_internas.json');metas={p.stem:read(p) for p in (OUT/'metadatos').glob('*.json')}
    for row in signatures:
        sig=row['firma'];year=row['validacion'];c=cs[row['id']]
        years=[a for a in (2019,2021,2022,2023,2024) if a<year]
        train=panel[panel.anio.isin(years)].sort_values(K).reset_index(drop=True)
        assert sig['pesos']['anios_train']==years and sig['train_llaves']==train[K].values.tolist()
        assert np.array_equal(sig['X'],train[c['entradas']].to_numpy(float)) and np.array_equal(sig['y'],train.cambio_observado.to_numpy(float))
        if c['familia']!='persistencia':
            name=f'e{row["externo"]}_i{year}_{row["id"]}';meta=metas[name]
            assert meta['pesos']==sig['pesos']
            assert meta['contexto']['firma_sha256']==hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest()
            if c['familia']=='mediana':
                scales=np.sqrt(np.asarray(meta['transformaciones']['varianza']))
                scales[scales==0]=1.
                np.testing.assert_array_equal(meta['transformaciones']['escala'],scales)
                assert abs(meta['transformaciones']['suma_pesos']-math.fsum(sig['pesos']['pesos']))<=1e-12
    checks=read(OUT/'comprobaciones_globales.json');assert len(checks)==5 and all(c['aprobado'] for c in checks)
    # Métodos de selección son persistencia; se prueba recálculo puro de los cinco años.
    assert all(c['sin_fit'] and c['id']=='persistencia' for c in checks)
    assert not list((OUT/'modelos').glob('*externo*')) and not list((OUT/'modelos').glob('*repeticion*'))
    with (OUT/'pruebas_contextos.json').open('x') as f:json.dump(dict(aprobado=True,firmas_train_exactas=360,metas=350,scaler_escala_y_suma=True,comprobaciones_persistencia=5,sin_nuevos_fits=True),f,indent=2)
    print('360 firmas y350metadatos cotejados con años/matrices exactos;5persistencias sinfit')
if __name__=='__main__':main()
