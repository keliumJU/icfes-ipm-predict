"""IO durable, rutas limitadas y reloj absoluto. Sin estimadores."""
from pathlib import Path
import hashlib, json, os, time
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
START = 1791828479.0  # primera acción: 2026-10-12 18:07:59 UTC
SEED = 20261010
def sha(p):
    p=Path(p)
    if p.is_symlink(): return hashlib.sha256(os.readlink(p).encode()).hexdigest()
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def load(p): return json.loads(Path(p).read_text())
def check(v,label):
    if not v: raise AssertionError(label)
def safe(p):
    p=Path(p).absolute()
    check(p.is_relative_to(HERE) and '..' not in p.parts,'ruta fuera/traversal')
    check(all(not q.is_symlink() for q in [p,*p.parents] if q.is_relative_to(HERE)),'symlink')
    return p
def save(p,x):
    p=safe(p);p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+'.tmp')
    with t.open('w') as f:
        f.write(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
        f.flush();os.fsync(f.fileno())
    os.replace(t,p)
    fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
def elapsed(): return time.time()-START
def deadline(fits=False): check(elapsed() < (5400 if fits else 7200),'presupuesto absoluto agotado')
def csv_save(p,df):
    import pandas as pd, numpy as np
    p=safe(p);save(p,df.to_csv(index=False,float_format='%.17g'))
    textcols={c:str for c in df if not pd.api.types.is_numeric_dtype(df[c])}
    r=pd.read_csv(p,float_precision='round_trip',dtype=textcols,keep_default_na=False)
    check(list(r.columns)==list(df.columns) and len(r)==len(df),'CSV forma')
    for c in df:
        if pd.api.types.is_numeric_dtype(df[c]):
            check(np.array_equal(df[c].to_numpy(),r[c].to_numpy(),equal_nan=True),'CSV exacto '+c)
        else: check(df[c].fillna('').astype(str).tolist()==r[c].fillna('').astype(str).tolist(),'CSV texto '+c)
    return sha(p)
