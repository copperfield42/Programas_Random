"""http://stackoverflow.com/questions/17248383/pretty-print-by-default-in-python-repl"""
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import pprint
import sys

__all__ = "pprint_on pprint_off set_printers del_printers".split()

orig_displayhook = sys.displayhook

def myhook(value):
    if value is not None:
        builtins._ = value
        pprint.pprint(value)


pprint_on  = lambda: setattr(sys, 'displayhook', myhook)
pprint_off = lambda: setattr(sys, 'displayhook', orig_displayhook)

def set_printers():
    builtins.pprint_on  = pprint_on
    builtins.pprint_off = pprint_off


def del_printers():
    del builtins.pprint_on  
    del builtins.pprint_off 

