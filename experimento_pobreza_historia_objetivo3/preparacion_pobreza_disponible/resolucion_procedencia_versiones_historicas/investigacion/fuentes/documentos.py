"""Adquisiciones de documentación institucional, nunca bases de evaluados."""
from adquirir import acquire, Links
from iniciar import HERE
from urllib.parse import urljoin
DOCS={
'icfes_paac2022_2.pdf':'https://www.icfes.gov.co/wp-content/uploads/2024/11/Seguimiento-PAAC-2022-2-Cuatrimestre-2022.pdf',
'icfes_paac2022_3.pdf':'https://www.icfes.gov.co/wp-content/uploads/2024/11/Seguimiento-PAAC-2022-3-Cuatrimestre-2022.pdf',
'icfes_acceso_diccionarios.html':'https://www.icfes.gov.co/transparencia-y-acceso-a-la-informacion-publica/datos-abiertos/acceso-a-bases-de-datos-y-diccionarios/',
'icfes_data.html':'https://www.icfes.gov.co/investigaciones/data-icfes/',
'icfes_analisis.html':'https://www.icfes.gov.co/analisis-de-datos/',
'icfes_informes.html':'https://www.icfes.gov.co/transparencia-y-acceso-a-la-informacion-publica/planeacion-presupuesto-e-informes/informes-de-gestion-evaluacion-y-auditoria/',
'icfes_2018.pdf':'https://www.icfes.gov.co/wp-content/uploads/2024/12/Informe-de-gestion-2018.pdf',
'icfes_2019.pdf':'https://www.icfes.gov.co/wp-content/uploads/2024/12/Informe-de-gestion-2019.pdf',
'icfes_2020.pdf':'https://www.icfes.gov.co/wp-content/uploads/2024/12/Informe-de-gestion-2020.pdf',
'icfes_cuatrienio.pdf':'https://www.icfes.gov.co/wp-content/uploads/2025/10/DG-Informe-del-cuatrienio-ICFES-Acces.pdf',
'icfes_2023.pdf':'https://www.icfes.gov.co/wp-content/uploads/2025/10/Informe-Gestio%CC%81n-2023-version-final-30-01-2024.pdf',
'icfes_2024.pdf':'https://www.icfes.gov.co/wp-content/uploads/2025/02/Informe-de-Gestion-2024.pdf',
'icfes_2025.pdf':'https://www.icfes.gov.co/wp-content/uploads/2026/03/f52-24-informe-de-gestion-2025.pdf',
'dane_original_2018.html':'https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-y-desigualdad/pobreza-monetaria-y-multidimensional-en-colombia-2018'
}
if __name__=='__main__':
    for name,url in DOCS.items():
        if not (HERE/'evidencia'/name).exists(): acquire(url,name,'documentación institucional')
        print(name,flush=True)
    p=Links(); p.feed((HERE/'evidencia/dane_original_2018.html').read_text())
    links=[urljoin(DOCS['dane_original_2018.html'],u) for u,t in p.links if 'multidimensional' in u and u.endswith(('.xls','.xlsx')) and 'depart' in t.lower()]
    assert len(set(links))==1, links
    for url in set(links):
        name='dane_original_2018.'+url.rsplit('.',1)[1]
        if not (HERE/'evidencia'/name).exists(): acquire(url,name,'anexo departamental original enlazado hoy')
        print(name,url,flush=True)
