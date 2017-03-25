"""Simple modulo para descargar archivos de internet"""
try:
    from tqdm import tqdm, tqdm_gui
except ImportError:
    from contextlib import contextmanager 
    
    @contextmanager
    def tqdm(iterable=None,*argv,**karg):
        print( '    ' if karg.get('nested',False) else '', karg.get('desc',''))
        yield iterable
        
    tqdm_gui = tqdm
    
    print("tqdm no esta disponible, este modulo usa esa libreria como su barra de progreso.",
          "Por favor instalarlo, Se puede hacer mediante: pip install tqdm",
          sep="\n", file=sys.stderr)

__all__=['download','download_many','url_exist']

import os, sys, json
from contextlib import closing
import requests
import gevent

_path1 = os.path.expanduser("~/Downloads")
_path2 = os.path.expanduser("~/Descargas")
PATH   = os.path.normpath( next(filter(os.path.exists,(_path1,_path2)),os.getcwd()) )
PARTIALEXT = '.partialfile'


def url_exist(url:str) -> bool:
    """Determina si la url dada existe"""
    with closing(requests.head(url, allow_redirects=True)) as r:
        return r.ok

def download(url:str, nombre:str=None, carpeta:str=PATH, desc:str=None,*,chunk_size=2**16, timeout=5, **tqdm_karg):
    """Descarga un archivo desde la url dada a un archivo del nombre dado en la carpeta espesificada"""
    config = dict(allow_redirects=True)
    tqdm_bar = tqdm_gui if 'idlelib' in sys.modules else tqdm
    resume_header = None
    current = 0
    with closing( requests.head(url, **config) ) as con:
        if not nombre:
            nombre = con.url.split("/")[-1]
        if desc is None:
            desc = f"descargando {nombre!r}"
        result = os.path.join(carpeta,nombre)
        data = os.path.join(carpeta,nombre+PARTIALEXT)  
        total = con.headers.get('content-length')
        try:
            total = int(total)
        except ValueError:
            pass
        if con.headers.get('Accept-Ranges',"").lower() == 'bytes':
            if os.path.exists(data):
                current = os.stat(data).st_size
                if total is not None:
                    assert current <= total, "inconsistent file size"
                resume_header = {'Range': f'bytes={current}-' }              
    tqdm_karg.update( unit="B", unit_scale=True, leave=False, miniters=1, desc=desc, total=total, initial=current)
    config.update( stream=True, timeout=timeout, headers=resume_header )
    with open(data, "ab" if current else "wb") as file, closing( requests.get(url,**config ) ) as con:
        with tqdm_bar(**tqdm_karg) as progress_bar:
            for chunk in con.iter_content(chunk_size):
                file.write(chunk)
                progress_bar.update(len(chunk))
    os.rename(data,result)
    



def _download_many(archivos:[("url","nombre")], carpeta:str=PATH, *, ignore_error:bool=True, _gui:bool=False, **tqdm_karg):
    """Descarga los archivos espesificados en la carpeta dada"""
    if _gui:
        progress_bar = tqdm_gui
    else:
        progress_bar = tqdm_gui if 'idlelib' in sys.modules else tqdm
    if not os.path.exists(carpeta):
        print("creando carpeta:",carpeta)
        os.mkdir(carpeta)
        print("listo",flush=True)          
    esta_pendiente   = lambda x: not os.path.exists( os.path.join(carpeta,x[1]) )
    total_archivos   = list( archivos ) 
    total            = len(total_archivos)
    pendiente        = list( filter(esta_pendiente,total_archivos) )
    listo            = total - len(pendiente)
    with progress_bar(pendiente, total=total, initial=listo, **tqdm_karg) as progreso:
        for url,name in progreso:
            try:
                download(url, name, carpeta=carpeta, desc=name,  nested=True )
            except urllib.error.URLError as error:
                print("\n\nError al descargar:",url,"\n",error, flush=True)
                if not ignore_error:
                    raise

def download_many(archivos:[("url","nombre")], carpeta:str=PATH, *, ignore_error:bool=True, _gui:bool=False, **tqdm_karg):
    """Descarga los archivos espesificados en la carpeta dada"""     


def _yugi():
    url="https://redirector.googlevideo.com/videoplayback?id=9cc97f77a6b5b8fb&itag=22&source=webdrive&requiressl=yes&ttl=transient&mm=30&mn=sn-ab5l6nsk&ms=nxu&mv=m&pl=48&ei=n4bSWPn1KdL2qgXy5pugDA&mime=video/mp4&lmt=1490128739552530&mt=1490191947&ip=2604:a880:800:a1::796:9001&ipbits=0&expire=1490206431&sparams=ip,ipbits,expire,id,itag,source,requiressl,ttl,mm,mn,ms,mv,pl,ei,mime,lmt&signature=70F8A913694908444AEEAC78D3370D2F40B380B0.1801D1D8ADA715336631253B265EF15D14C51987&key=ck2&app=explorer&jparams=MTkwLjIwMy4xNjAuMTY4&upx=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQ7IHJ2OjUyLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvNTIuMA&tr=1"
    download(url, "YGO Movie the Dark Side of Dimension.mp4")    

