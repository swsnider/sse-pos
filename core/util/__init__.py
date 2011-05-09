from google.appengine.api import memcache

from security import *
from presentation import *
import models

__all__ = []

def public(f):
  global __all__
  __all__.append(f.__name__)
  return f

def model_to_dict(obj, klass):
  ret = dict(__key__ = str(obj.key()))
  for field in klass.USEFUL_FIELDS:
    ret[field] = getattr(obj, field)
  return ret

@public
def get_lists(*lists):
  ret_list = []
  for model in lists:
    model_klass = getattr(models, model)
    if model_klass is None:
      ret_list.append(tuple())
    else:
      objs = memcache.get('__lists__' + model)
      if objs is not None:
        ret_list.append(objs)
      else:
        objs = model_klass.all().filter('stati =', 'visible')
        for i in model_klass.ORDERING:
          objs = objs.order(i)
        objs = [model_to_dict(i, model_klass) for i in objs]
        ret_list.append(objs)
        memcache.add('__lists__' + model, objs)
  return ret_list

@public
def binary_search(haystack, needle, key=lambda x:x):
  """Returns the index that the value needle can be found at in the sorted haystack."""
  length = len(haystack)
  if length < 5:
    for i in range(len(haystack)):
      if key(haystack[i]) == needle:
        return i
    else:
      return -1
  pivot = length / 2
  pivot_key = key(haystack[pivot])
  if pivot_key == needle:
    return pivot
  elif pivot_key > needle:
    return binary_search(haystack[:pivot], needle, key=key)
  elif pivot_key < needle:
    return binary_search(haystack[pivot+1:], needle, key=key)