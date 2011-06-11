import global_defs
import bottle
from StringIO import StringIO
import csv
import datetime
import os
import re
import simplejson as json
import sys
import urllib
from google.appengine.api import namespace_manager


import util
import models

class _modules(object):
  util = util
  models = models
  global_defs = global_defs
  bottle = bottle


def jsonify(f):
  def g(*args, **kwargs):
    return json.dumps(f(*args, **kwargs))
  return g

def csvify(f):
  def g(*args, **kwargs):
    result = f(*args, **kwargs)
    bottle.response.headers['Content-Type'] = "text/csv"
    bottle.response.headers['Content-Disposition'] = 'attachment;filename="users.csv"'
    output = StringIO()
    ourWriter = csv.DictWriter(output, result[0].keys())
    for i in result:
      ourWriter.writerow(i)
    return output.getvalue()
  return g

class money(object):
  @staticmethod
  def from_str(amt):
    if '.' not in amt: amt += "00"
    amt = amt.replace(",", "")
    amt = amt.replace(".", "")
    amt = int(amt)
    return amt

  @staticmethod
  def to_str(amt):
    temp = "%.2f" % (amt / 100.0)
    profile = re.compile(r"(\d)(\d\d\d[.,])")
    while 1:
      temp, count = re.subn(profile,r"\1,\2",temp)
      if not count: break
    return temp

def flash(flash_str):
  session = bottle.request.environ.get('beaker.session')
  if 'flash' not in session:
    session['flash'] = []
  session['flash'].append(flash_str)
  session.save()

def view(*view_args, **view_kwargs):
  def g(f):
    @bottle.jinja2_view(*view_args, **view_kwargs)
    def h(*args, **kwargs):
      session = bottle.request.environ.get('beaker.session')
      if 'flash' not in session:
        session['flash'] = []
      ret_dict = f(*args, **kwargs)
      if ret_dict is None:
        ret_dict = {}
      if 'flash' not in session:
        session['flash'] = []
      ret_dict['_flash'] = session['flash']
      ret_dict['_namespace'] = namespace_manager.get_namespace()
      ret_dict['_m_'] = _modules
      if '_user' in dir(bottle.request):
        ret_dict['_user'] = bottle.request._user
      session['flash'] = []
      return ret_dict
    return h
  return g