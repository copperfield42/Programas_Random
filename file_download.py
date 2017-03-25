"""Simple modulo para descargar archivos de internet"""


import os, sys
import urllib.request, urllib.error 

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

_path1 = os.path.expanduser("~/Downloads")
_path2 = os.path.expanduser("~/Descargas")
PATH   = os.path.normpath( next(filter(os.path.exists,(_path1,_path2)),os.getcwd()) )


def estatus_hook(progress_bar):
    """Wraps tqdm instance. Don't forget to close() or __exit__()
       the tqdm instance once you're done with it (easiest using `with` syntax).
    
       Example
       -------
    
       >>> with tqdm(...) as t:
       ...     reporthook = my_hook(t)
       ...     urllib.urlretrieve(..., reporthook=reporthook)  """
    if progress_bar is None:
        return None
    last_b=0
    def inner(b=1,bsize=1,tsize=None):
        """
        b  : int, optional
            Number of blocks just transferred [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        nonlocal last_b
        if tsize is not None:
            progress_bar.total = tsize
        progress =  (b - last_b)*bsize 
        if progress<1:
            progress = 1
        progress_bar.update( progress )
        last_b = b
    return inner

def download(url, nombre=None, carpeta=PATH, desc=None, **tqdm_karg):
    """Descarga un archivo desde la url dada a un archivo del nombre dado en la carpeta path"""
    progress_bar = tqdm_gui if 'idlelib' in sys.modules else tqdm
    if desc is None:
        desc = "descargando %s"%nombre
    with progress_bar(unit="B", unit_scale=True, leave=False, miniters=1, desc=desc, **tqdm_karg) as bar:
        file, header = urllib.request.urlretrieve(
                                   url,
                                   os.path.join(carpeta,nombre) if nombre else None,
                                   reporthook=estatus_hook(bar)
                                   )
    return os.path.abspath(file), header
            


def download_many(archivos:[("url","nombre")], carpeta=PATH, *, ignore_error=True, _gui=False, **tqdm_karg):
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

            
def url_exist(url):
    """Determina si url dada existe"""     
    try:
        with urllib.request.urlopen(url) as conn:
            return conn.reason == "OK" and conn.status == 200
    except urllib.error.URLError as error:
        pass
    return False
    
    
          

def uso():
    manual="""
Script para descargar archivos con urllib.request.urlretrieve 

uso:
$> {script} name_file url [path]
$> {script} -h

name_file      Nombre que se desea para el archivo descargado

url            url o link del archivo a descargar

path           Carpeta donde se desea guardar el archivo 
               por defecto: {path}

-h             muestra esta ayuda               

"""
    print(manual.format(script=os.path.basename(__file__),path=PATH))

    
if __name__=="__main__":        
    datos = sys.argv[1:]
    if datos:
        if any( h in datos for h in ("-h","help","-help","--help","?","/?")):
            uso()
        else:
            if len(datos) in {2,3}:
                download(*datos)                
            else:
                uso()








