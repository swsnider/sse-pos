from security import *
from presentation import *

__all__ = []

def public(f):
  global __all__
  __all__.append(f.__name__)
  return f

@public
def get_lists(*lists):
  ret_list = []
  for i in lists:
    pass # TODO(swsnider): do the list thing