"""E2-01: solo auditoría, CSV cero entero/flotante. Fuentes congeladas intactas.
Ningún ajuste/selección/umbral modificado; comparación de valores aún más estricta.
"""
import inspect,types,tempfile
import verificar as original
from piloto import *
NEEDLE="pd.testing.assert_frame_equal(q[allframes[label].columns].reset_index(drop=True),allframes[label].reset_index(drop=True))"
REPLACEMENT=NEEDLE[:-1]+",check_dtype=False,check_exact=True)"

def pruebas():
    a=pd.DataFrame(dict(codigo_departamento=['05'],anio=[2021],cambio_predicho=[0]))
    b=a.copy();b['cambio_predicho']=b.cambio_predicho.astype(float)
    pd.testing.assert_frame_equal(a,b,check_dtype=False,check_exact=True)
    for field,value in [('cambio_predicho',1e-11),('codigo_departamento','08'),('anio',2022)]:
        c=b.copy();c[field]=value
        try:pd.testing.assert_frame_equal(a,c,check_dtype=False,check_exact=True)
        except AssertionError:pass
        else:raise AssertionError('no rechazó valores o llaves distintos')
    return dict(aprobado=True,ceros_int_float_iguales=True,rechaza_cambio_1e_11=True,rechaza_llaves_distintas=True,check_exact=True,ajustes_nuevos=0)

def ejecutar():
    verify_freeze()
    assert not (OUT/'meta.json').exists() or read(OUT/'meta.json')['completo']
    source=inspect.getsource(original.verificar)
    assert source.count(NEEDLE)==1,'la extensión solo admite el punto documentado'
    checks=pruebas()
    files=[Path(__file__),E2/'ENMIENDA_AUDITORIA_E2_01.md']
    extension=OUT/'congelacion_extension_auditoria.json'
    content=dict(instante_utc=now(),criterios_modificados=False,ajustes_nuevos=0,
                 congelacion_operativa_sha256=sha(OUT/'congelacion_operativa.json'),
                 verificador_original_sha256=sha(E2/'fuentes/verificar.py'),
                 artefactos_sha256={str(p.relative_to(ROOT)):sha(p) for p in files},pruebas=checks)
    if extension.exists():
        saved=read(extension)
        assert saved['congelacion_operativa_sha256']==content['congelacion_operativa_sha256']
        assert saved['verificador_original_sha256']==content['verificador_original_sha256']
        check_hashes(saved['artefactos_sha256']);assert saved['pruebas']==checks
    else:
        assert not (OUT/'meta.json').exists(),'justificar la extensión antes de calcular la meta'
        guardar(extension,content)
    before=sha(OUT/'piloto/ledger.json')
    # Función independiente recompilada en memoria; archivo congelado no editado.
    scope=dict(original.verificar.__globals__)
    exec(compile(source.replace(NEEDLE,REPLACEMENT),str(Path(__file__)),'exec'),scope)
    scope['verificar']()
    assert sha(OUT/'piloto/ledger.json')==before,'auditoría no puede consumir ni ajustar'
    guardar(OUT/'verificacion_extension_auditoria.json',dict(aprobado=True,pruebas=checks,
            codigo_congelado_intacto=True,ledger_intacto=True,ajustes_nuevos=0,
            extension_congelada_sha256=sha(extension)))
if __name__=='__main__':ejecutar()
