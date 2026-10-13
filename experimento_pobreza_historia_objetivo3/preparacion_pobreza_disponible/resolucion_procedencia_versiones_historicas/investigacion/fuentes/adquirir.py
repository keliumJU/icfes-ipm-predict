"""Solo páginas oficiales y anexos departamentales agregados DANE enlazados.
No accede a microdatos ni bases ICFES. Reintentos no sobrescriben adquisiciones.
"""
from iniciar import HERE, sha
from urllib.request import urlopen, Request
from urllib.parse import urljoin, urlparse
import json, datetime, re, sys
from html.parser import HTMLParser
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.current=None
    def handle_starttag(self,t,a):
        if t=='a': self.current=[dict(a).get('href',''),dict(a).get('title','')]
    def handle_data(self,d):
        if self.current is not None: self.current[1]+=d
    def handle_endtag(self,t):
        if t=='a' and self.current is not None: self.links.append(self.current); self.current=None
def acquire(url,name,kind):
    assert urlparse(url).hostname in ['www.dane.gov.co','www.icfes.gov.co']
    p=HERE/'evidencia'/name
    assert not p.exists(), name
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:
        data=r.read(); final=r.url; headers=dict(r.headers)
    p.parent.mkdir(exist_ok=True); p.write_bytes(data)
    row=dict(archivo=str(p.relative_to(HERE)),url_solicitada=url,url_final=final,adquisicion_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=sha(p),bytes=len(data),tipo=kind,headers=headers,advertencia='Adquisición actual; Last-Modified no certifica primera publicación histórica.')
    with (HERE/'ADQUISICIONES.jsonl').open('a') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return data
BASE='https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-multidimensional'
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='dane':
        # 2020 solo como edición soporte de 2018/2019; sus valores no se exportan ni incorporan.
        for year in [2019,2020,2021,2022,2023,2024,2025]:
            url=BASE+(f'/pobreza-multidimensional-{year}' if year!=2025 else '')
            saved=HERE/'evidencia'/f'dane_{year}.html'
            data=saved.read_bytes() if saved.exists() else acquire(url,f'dane_{year}.html','página producto')
            parser=Links();parser.feed(data.decode('utf-8',errors='replace'))
            links=[urljoin(url,u) for u,t in parser.links if re.search(r'(anex|anexo).*depart',u+' '+t,re.I) and re.search(r'\.xlsx?$',u,re.I) and 'PDET' not in u.upper()]
            links=list(dict.fromkeys(links));assert len(links)==1,(year,links)
            link=links[0];ext=PathSuffix=link.rsplit('.',1)[1]
            if not (HERE/'evidencia'/f'dane_{year}.{ext}').exists(): acquire(link,f'dane_{year}.{ext}','anexo departamental agregado; edición enlazada hoy')
            print(year,link,flush=True)
    elif mode=='pagina':
        acquire(sys.argv[2],sys.argv[3],'documentación oficial')
