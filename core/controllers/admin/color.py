from models import *
from google.appengine.ext.db import Key
from google.appengine.api import memcache
from bottle import route, request, redirect
import util
from util import view
from controllers.admin import std_admin_wrapper


@route('/admin/color')
@std_admin_wrapper('admin/color.html')
def admin_color():
  if 'superuser' in request._user.stati:
    return dict(colors=Color.all().order('name'))
  else:
    return dict(colors=Color.all().filter('stati =', 'admin_active').order('name'))


@route('/admin/color/:color_key/edit')
@std_admin_wrapper('admin/color_edit.html')
def admin_color_edit(color_key):
  return dict(color=Color.get(Key(color_key)))


@route('/admin/color/create', method='POST')
@std_admin_wrapper()
def admin_color_create():
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  discount = request.forms.get('discount', '0')
  color = Color()
  color.name = name
  color.code = code
  color.discount = int(discount)
  color.stati = ['active', 'admin_active']
  color.put()
  memcache.delete('__lists__Color')
  redirect('/admin/color')


@route('/admin/color/:color_key/commit', method='POST')
@std_admin_wrapper()
def admin_color_commit(color_key):
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  discount = request.forms.get('discount', '0')
  color = Color.get(Key(color_key))
  color.name = name
  color.code = code
  color.discount = int(discount)
  color.put()
  memcache.delete('__lists__Color')
  redirect('/admin/color')


def toggle_active(color):
  l = color.stati
  if 'inactive' in color.stati:
    l.remove('inactive')
    l.append('active')
  else:
    l.append('inactive')
    l.remove('active')
  color.stati = l
  color.put()


def toggle_admin_active(color):
  l = color.stati
  if 'admin_inactive' in color.stati:
    l.remove('admin_inactive')
    l.append('admin_active')
  elif 'admin_active' not in color.stati:
    l.append('admin_active')
  else:
    l.append('admin_inactive')
    l.remove('admin_active')
  color.stati = l
  color.put()


def delete_color(color):
  color.stati = ['deleted']
  color.put()


_actions = {
  'toggle_active': toggle_active,
  'toggle_admin_active': toggle_admin_active,
  'delete': delete_color
}


@route('/admin/color/multi_edit', method='POST')
@std_admin_wrapper()
def admin_color_multi_edit():
  color_keys = request.forms.getall('multi_edit')
  action = _actions.get(request.forms.get('action'), lambda x:None)
  for color_key in color_keys:
    color = Color.get(Key(color_key))
    action(color)
  memcache.delete('__lists__Color')
  redirect('/admin/color')