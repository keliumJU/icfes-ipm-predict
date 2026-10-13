"""Rutas sin symlinks, CSV exactos y firmas de contexto."""
import csv
import hashlib
import json
import math
from pathlib import Path
from motor import IntegrityError

def safe_path(root, relative):
    root=Path(root).absolute()
    # Rechazar enlaces incluso internos y en cualquier padre.
    for p in (root,*root.parents):
        if p.is_symlink(): raise IntegrityError('Raíz/padre symlink')
    rel=Path(relative)
    if rel.is_absolute() or not rel.parts or any(p in ('..','.') for p in rel.parts):
        raise IntegrityError('Ruta absoluta/traversal')
    target=root/rel
    for p in (target,*target.parents):
        if p.is_symlink(): raise IntegrityError('Symlink prohibido')
        if p==root: break
    if not target.is_relative_to(root): raise IntegrityError('Fuera raíz')
    return target

def digest(path):
    p=Path(path)
    if p.is_symlink(): raise IntegrityError('No seguir symlink')
    return hashlib.sha256(p.read_bytes()).hexdigest()

def context_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def read_csv(path):
    with Path(path).open(newline='') as f:
        reader=csv.reader(f); header=next(reader)
        if len(header)!=len(set(header)): raise IntegrityError('Columnas duplicadas')
        rows=list(reader)
    if any(len(row)!=len(header) for row in rows): raise IntegrityError('CSV mal formado')
    return header,rows

def exact_csv(left,right,numeric=(),keys=()):
    h,a=read_csv(left); h2,b=read_csv(right)
    if h!=h2 or len(a)!=len(b): raise IntegrityError('CSV columnas/orden/cobertura')
    if not set(numeric).issubset(h) or not set(keys).issubset(h): raise IntegrityError('Esquema CSV')
    if keys:
        indexes=[h.index(k) for k in keys]
        for rows in (a,b):
            kk=[tuple(r[i] for i in indexes) for r in rows]
            if len(kk)!=len(set(kk)): raise IntegrityError('CSV llaves duplicadas')
    for ra,rb in zip(a,b):
        for col,x,y in zip(h,ra,rb):
            if col in numeric:
                try: fx,fy=float(x),float(y)
                except ValueError as exc: raise IntegrityError('CSV numérico inválido') from exc
                if not math.isfinite(fx) or not math.isfinite(fy) or fx!=fy:
                    raise IntegrityError('CSV numérico no exacto')
            elif x!=y: raise IntegrityError('CSV texto/llaves/orden')
    return True
