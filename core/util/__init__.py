from bottle import request, redirect
from google.appengine.api import memcache
from google.appengine.api import namespace_manager
from google.appengine.ext import db

from security import *
from presentation import *
import models

__all__ = [
  'group',
  'provide_user',
  'global_namespace',
  'user_namespace',
  'provide_session',
  'get_lists',
  'binary_search'
]

def group(seq, num):
  counter = 0
  appender = []
  idx = 0
  while idx < len(seq):
    while counter < num:
      appender.append(seq[idx])
      idx += 1
      counter += 1
    yield appender
    appender = []
    counter = 0


def global_namespace(f):
  def g(*args, **kwargs):
    old_namespace = namespace_manager.get_namespace()
    namespace_manager.set_namespace('-global-')
    ret_dict = f(*args, **kwargs)
    namespace_manager.set_namespace(old_namespace)
    return ret_dict
  return g

def user_namespace(f):
  @provide_user
  def g(*args, **kwargs):
    _user = request._user
    namespace = _user.organization.namespace
    org_name = _user.organization.name
    request._old_namespace = namespace_manager.get_namespace()
    namespace_manager.set_namespace(namespace)
    ret_dict = f(*args, **kwargs)
    return ret_dict
  return g

def provide_session(f):
  def g(*args, **kwargs):
    request._session = request.environ.get('beaker.session')
    return f(*args, **kwargs)
  return g

def model_to_dict(obj, klass):
  ret = dict(__key__ = str(obj.key()))
  for field in klass.USEFUL_FIELDS:
    ret[field] = getattr(obj, field)
  return ret

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
        objs = model_klass.all().filter('stati =', 'admin_active').filter('stati =', 'active')
        for i in model_klass.ORDERING:
          objs = objs.order(i)
        objs = [model_to_dict(i, model_klass) for i in objs]
        ret_list.append(objs)
        memcache.add('__lists__' + model, objs)
  return ret_list

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