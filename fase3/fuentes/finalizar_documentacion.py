"""Actualiza huellas tras documentación; no repite ajustes aprobados."""
import sys
sys.dont_write_bytecode=True
from comun import *
import nbformat,re
from datetime import datetime,timezone
v=read('verificacion.json');assert v['aprobada']
# Tres ajustes en intento de control que falló por nombres Git y tres en control aprobado.
v['ajustes_verificacion_por_invocacion']=v.pop('ajustes_adicionales_verificacion')
v['ajustes_adicionales_verificacion_sesion']=6
v['documentacion_finalizada_utc']=datetime.now(timezone.utc).isoformat()
for source in (ROOT/'fase3/fuentes').glob('*.py'):
    text=source.read_text()
    if re.search(r'^# %%',text,re.M):
        parts=re.split(r'^# %%([^\n]*)\n',text,flags=re.M)
        for flag,body in zip(parts[1::2],parts[2::2]):
            if '[markdown]' not in flag:compile(body,str(source),'exec')
    else:compile(text,str(source),'exec')
for name,h in read('preparacion.json')['entradas_sha256'].items():assert huella(ROOT/name)==h
for name,h in read('congelacion.json')['artefactos_sha256'].items():assert huella(ROOT/name)==h
nbinfo=read('verificacion_notebooks.json')
for entry in nbinfo:
    path=ROOT/entry['notebook'];nbformat.validate(nbformat.read(path,as_version=4));assert huella(path)==entry['notebook_sha256']
# Verificar que solo continuidad cambió entre archivos versionados iniciales.
changed=subprocess.check_output(['git','diff','7e95ffe823c3d08f345620c0f9bc65dc72fae7d5','--name-only'],cwd=ROOT,text=True).splitlines()
assert changed==['CONTINUIDAD_OBJETIVO_3.md'],changed
save('verificacion.json',v)
files=[p for p in (ROOT/'fase3').rglob('*') if p.is_file() and p.name!='manifiesto_cierre.json']+[ROOT/e['notebook'] for e in nbinfo]+[ROOT/'CONTINUIDAD_OBJETIVO_3.md']
save('manifiesto_cierre.json',{str(p.relative_to(ROOT)):huella(p) for p in files})
print('Documentación, fuentes, notebooks y huellas finales comprobados; sin nuevos ajustes.')
