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


@route('/admin/item')
@std_admin_wrapper('admin/item.html')
def admin_item():
  if 'superuser' in request._user.stati:
    return dict(items=Item.all().order('name'))
  else:
    return dict(items=Item.all().filter('stati =', 'admin_active').order('name'))


@route('/admin/item/:item_key/edit')
@std_admin_wrapper('admin/item_edit.html')
def admin_item_edit(item_key):
  return dict(item=Item.get(Key(item_key)))


@route('/admin/item/create', method='POST')
@std_admin_wrapper()
def admin_item_create():
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  price = request.forms.get('price', '0')
  item = Item()
  item.name = name
  item.code = code
  item.price = util.money.from_str(price)
  item.stati = ['active', 'admin_active']
  item.put()
  memcache.delete('__lists__Item')
  redirect('/admin/item')


@route('/admin/item/:item_key/commit', method='POST')
@std_admin_wrapper()
def admin_item_commit(item_key):
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  price = request.forms.get('price', '0')
  item = Item.get(Key(item_key))
  item.name = name
  item.code = code
  item.price = util.money.from_str(price)
  item.put()
  memcache.delete('__lists__Item')
  redirect('/admin/item')


def toggle_active(item):
  l = item.stati
  if 'inactive' in item.stati:
    l.remove('inactive')
    l.append('active')
  else:
    l.append('inactive')
    l.remove('active')
  item.stati = l
  item.put()


def toggle_admin_active(item):
  l = item.stati
  if 'admin_inactive' in item.stati:
    l.remove('admin_inactive')
    l.append('admin_active')
  elif 'admin_active' not in item.stati:
    l.append('admin_active')
  else:
    l.append('admin_inactive')
    l.remove('admin_active')
  item.stati = l
  item.put()


def delete_item(item):
  item.stati = ['deleted']
  item.put()


_actions = {
  'toggle_active': toggle_active,
  'toggle_admin_active': toggle_admin_active,
  'delete': delete_item
}


@route('/admin/item/multi_edit', method='POST')
@std_admin_wrapper()
def admin_item_multi_edit():
  item_keys = request.forms.getall('multi_edit')
  action = _actions.get(request.forms.get('action'), lambda x:None)
  for item_key in item_keys:
    item = Item.get(Key(item_key))
    action(item)
  memcache.delete('__lists__Item')
  redirect('/admin/item')