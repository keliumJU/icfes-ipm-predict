"""Control final y huellas de entregables de fase5; sin modificar fases previas."""
from verificar_informe import main
from verificar_integridad import ROOT,sha,guardar

def finalizar():
    main()
    rutas=[ROOT/'informe_objetivo_3.md',ROOT/'CONTINUIDAD_OBJETIVO_3.md']
    rutas += [p for p in (ROOT/'fase5').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifiesto_cierre.json']
    guardar('manifiesto_cierre.json',{'fecha_cliente':'2026-10-09','commit_partida':'da48e1a4f85d206e8753fbad85b78ba2e3858b1a','alcance':'fase5 documental','entregables_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(rutas)},'modelos_ajustados':0,'simulaciones':0,'push':False})
    print('Manifiesto de fase5 generado')
if __name__=='__main__':finalizar()
