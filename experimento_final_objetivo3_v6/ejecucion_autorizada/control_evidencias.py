"""Control exacto de valores/llaves de texto. No cálculos predictivos ni fits."""
from comun import *
import csv,math
import pandas as pd

def validate():
    file=HERE/'EVIDENCIAS_TEXTO.csv';ev=pd.read_csv(file,dtype=str,keep_default_na=False);cache={};checked=0
    for row in ev.itertuples():
        path=HERE/row.file;check(sha(path)==row.sha256,'claim source SHA')
        if path.suffix=='.json':
            d=load(path);actual=d
            for piece in row.key.split('.'):
                if piece.isdigit():actual=actual[int(piece)]
                else:actual=actual[piece]
        else:
            if row.file not in cache:cache[row.file]=pd.read_csv(path,dtype=str,keep_default_na=False)
            df=cache[row.file];index,column=row.key.split(':',1);actual=df.iloc[int(index)][column]
        if row.kind in ['float','int']:
            check(float(actual)==float(row.value) and math.isfinite(float(actual)),'claim exact numeric '+row.claim)
        else:check(str(actual)==row.value,'claim exact label '+row.claim)
        check(int(row.cell) in range(1,8),'claim actual notebook cell');checked+=1
    return dict(aprobado=True,claims=checked,files=len(set(ev.file)),exact_numeric=True)
if __name__=='__main__':print(validate())
