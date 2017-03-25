"""Script para cythonize todos los .pyx"""
import sys, os, shutil, contextlib#, argparse 
from Cython.Build import Cythonize, cythonize

#TO DO: incluir command line options

@contextlib.contextmanager
def redirect_sys_argv(*argv):
    """contextmanager para cambiar sys.argv al argv dado"""
    original = list(sys.argv)
    sys.argv[:] = argv
    try:
        yield
    finally:
        sys.argv[:] = original

def get_pyx_files(path, abspath=True):
    """Regresa una lista con los archivos .pyx del path dado
       Si abspath es true, la lista de archivos es el path absoluto
       de lo contrario es solo el nombre de los mismos"""
    path = os.path.normpath(os.path.abspath(path))
    to_compile = []
    for name in os.listdir(path):
        if name.endswith(".pyx"):
            pyx = os.path.join(path,name)
            if os.path.isfile(pyx):
                to_compile.append(pyx if abspath else name)
    return to_compile

def compile_dir(path):
    """Funcion para cythonize todos los .pyx del path dado in-place"""
    to_compile = get_pyx_files(path)
    print("De:",path)
    if to_compile:
        print("Se compilaran:", list(map(os.path.basename,to_compile)))
        Cythonize.main( ['-a', '-i'] + to_compile )
    else:
        print("Nada para compilar")


def compile_dir_with_numpy(path, cleanup=True):
    """Funcion para cythonize todos los .pyx del path dado in-place
       incluyendo numpy"""
    from distutils.core import setup
    import numpy
    path = os.path.normpath(os.path.abspath(path))
    temp = os.path.join(path,".temp_build")
    with redirect_sys_argv(os.path.join(path,"make_virtual_script.py"), "build_ext", "--inplace", "-t", temp):
        setup(
            ext_modules = cythonize("./*.pyx", annotate=True),
            include_dirs=[numpy.get_include()]
            )
    if cleanup and os.path.exists(temp):
        shutil.rmtree(temp)
        
if __name__ == "__main__":
    if "with_numpy" in sys.argv[1:]:
        compile_dir_with_numpy(os.getcwd())
    else:        
        compile_dir(os.getcwd())
