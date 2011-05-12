import bottle
from StringIO import StringIO
import csv
import datetime
import os
import re
import simplejson as json
import sys
import urllib

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

def str_to_money(amt):
  if '.' not in amt: amt += "00"
  amt = amt.replace(",", "")
  amt = amt.replace(".", "")
  amt = int(amt)
  return amt

def money_to_str(amt):
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
    @bottle.view(*view_args, **view_kwargs)
    def h(*args, **kwargs):
      session = bottle.request.environ.get('beaker.session')
      if 'flash' not in session:
        session['flash'] = []
      ret_dict = f(*args, **kwargs)
      ret_dict['__flash__'] = list(session['flash'])
      session['flash'] = []
      return ret_dict
    return h
  return g