from models import *
from google.appengine.ext.db import Key
from google.appengine.api import memcache
from bottle import route, request, redirect
import util
from util import view


def global_admin_wrapper(*view_args, **view_kwargs):
  def h(wrapped):
    @util.secure
    @util.has_stati('superuser', 'admin')
    @util.global_namespace
    def g(*args, **kwargs):
      if (len(view_args) + len(view_kwargs)) > 0:
        f = view(*view_args, **view_kwargs)(wrapped)
      else:
        f = wrapped
      return f(*args, **kwargs)
    return g
  return h


@route('/admin/user')
@global_admin_wrapper('admin/user.html')
def admin_user():
  return dict(users=User.all().order('email'))


@route('/admin/user/:user_key/edit')
@global_admin_wrapper('admin/user_edit.html')
def admin_user_edit(user_key):
  return dict(user=User.get(Key(user_key)))


@route('/admin/user/create', method='POST')
@global_admin_wrapper()
def admin_user_create():
  first_name = request.forms.get('first_name', '')
  last_name = request.forms.get('last_name', '')
  username = request.forms.get('email', '')
  user = User()
  user.email = username
  user.first_name = first_name
  user.last_name = last_name
  stati = ['active']
  user.stati = stati
  user.put()
  memcache.delete('__lists__User')
  redirect('/admin/user')


@route('/admin/user/:user_key/commit', method='POST')
@global_admin_wrapper()
def admin_user_commit(user_key):
  email = request.forms.get('email', '')
  first_name = request.forms.get('first_name', '')
  last_name = request.forms.get('last_name', '')
  admin = request.forms.get('admin', False)
  active = request.forms.get('active', False)
  superuser = request.forms.get('superuser', False)
  user = User.get(Key(user_key))
  user.email = email
  user.last_name = last_name
  user.first_name = first_name
  stati = user.stati
  if admin:
    if 'admin' not in stati:
      stati.append('admin')
  else:
    if 'admin' in stati:
      stati.remove('admin')
  if superuser:
    if 'superuser' not in stati:
      stati.append('superuser')
  else:
    if 'superuser' in stati:
      stati.remove('superuser')
  if active:
    if 'active' not in active:
      stati.append('active')
      try:
        stati.remove('inactive')
      except ValueError: pass
  else:
    if 'active' in stati:
      try:
        stati.remove('active')
      except ValueError: pass
      stati.append('inactive')
  user.stati = stati
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


def toggle_superuser(user):
  l = user.stati
  if 'superuser' in user.stati:
    l.remove('superuser')
  else:
    l.append('superuser')
  user.stati = l
  user.put()


def toggle_admin(user):
  l = user.stati
  if 'admin' in user.stati:
    l.remove('admin')
  else:
    l.append('admin')
  user.stati = l
  user.put()


def delete_user(user):
  user.stati = ['deleted']
  user.put()


_actions = {
  'toggle_active': toggle_active,
  'toggle_superuser': toggle_superuser,
  'toggle_admin': toggle_admin,
  'delete': delete_user
}


@route('/admin/user/multi_edit', method='POST')
@global_admin_wrapper()
def admin_user_multi_edit():
  user_keys = request.forms.getall('multi_edit')
  action = _actions.get(request.forms.get('action'), lambda x:None)
  for user_key in user_keys:
    user = User.get(Key(user_key))
    action(user)
  memcache.delete('__lists__User')
  redirect('/admin/user')