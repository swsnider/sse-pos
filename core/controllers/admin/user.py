from models import *
from google.appengine.ext.db import Key
from google.appengine.api import memcache
from bottle import route, request, redirect
import util
from util import view
from controllers.admin import std_admin_wrapper


@route('/admin/')
@route('/admin')
@std_admin_wrapper('admin/index.html')
def admin_index():
  return dict()


@route('/admin/user')
@std_admin_wrapper('admin/user.html')
def admin_user():
  if 'superuser' in request._user.stati:
    return dict(users=User.all().order('name'))
  else:
    return dict(users=User.all().filter('stati =', 'admin_active').order('name'))


@route('/admin/user/:user_key/edit')
@std_admin_wrapper('admin/user_edit.html')
def admin_user_edit(user_key):
  return dict(user=User.get(Key(user_key)))


@route('/admin/user/create', method='POST')
@std_admin_wrapper()
def admin_user_create():
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  price = request.forms.get('price', '0')
  user = User()
  user.name = name
  user.code = code
  user.price = util.money.from_str(price)
  user.stati = ['active', 'admin_active']
  user.put()
  memcache.delete('__lists__User')
  redirect('/admin/user')


@route('/admin/user/:user_key/commit', method='POST')
@std_admin_wrapper()
def admin_user_commit(user_key):
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  price = request.forms.get('price', '0')
  user = User.get(Key(user_key))
  user.name = name
  user.code = code
  user.price = util.money.from_str(price)
  user.put()
  memcache.delete('__lists__User')
  redirect('/admin/user')


def toggle_active(user):
  l = user.stati
  if 'inactive' in user.stati:
    l.remove('inactive')
    l.append('active')
  else:
    l.append('inactive')
    l.remove('active')
  user.stati = l
  user.put()


def toggle_admin_active(user):
  l = user.stati
  if 'admin_inactive' in user.stati:
    l.remove('admin_inactive')
    l.append('admin_active')
  elif 'admin_active' not in user.stati:
    l.append('admin_active')
  else:
    l.append('admin_inactive')
    l.remove('admin_active')
  user.stati = l
  user.put()


def delete_user(user):
  user.stati = ['deleted']
  user.put()


_actions = {
  'toggle_active': toggle_active,
  'toggle_admin_active': toggle_admin_active,
  'delete': delete_user
}


@route('/admin/user/multi_edit', method='POST')
@std_admin_wrapper()
def admin_user_multi_edit():
  user_keys = request.forms.getall('multi_edit')
  action = _actions.get(request.forms.get('action'), lambda x:None)
  for user_key in user_keys:
    user = User.get(Key(user_key))
    action(user)
  memcache.delete('__lists__User')
  redirect('/admin/user')