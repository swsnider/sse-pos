from models import *
from google.appengine.ext.db import Key
from google.appengine.api import memcache
from bottle import route, request, redirect
import util
from util import view
from controllers.admin import std_admin_wrapper


@route('/admin/sale')
@std_admin_wrapper('admin/sale.html')
def admin_sale():
  if 'superuser' in request._user.stati:
    return dict(sales=Discount.all().order('name'))
  else:
    return dict(sales=Discount.all().filter('stati =', 'admin_active').order('name'))


@route('/admin/sale/:sale_key/edit')
@std_admin_wrapper('admin/sale_edit.html')
def admin_sale_edit(sale_key):
  return dict(sale=Discount.get(Key(sale_key)))


@route('/admin/sale/create', method='POST')
@std_admin_wrapper()
def admin_sale_create():
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  price = request.forms.get('price', '0')
  sale = Discount()
  sale.name = name
  sale.code = code
  sale.price = util.money.from_str(price)
  sale.stati = ['active', 'admin_active']
  sale.put()
  memcache.delete('__lists__Discount')
  redirect('/admin/sale')


@route('/admin/sale/:sale_key/commit', method='POST')
@std_admin_wrapper()
def admin_sale_commit(sale_key):
  name = request.forms.get('name', '')
  code = request.forms.get('code', '')
  price = request.forms.get('price', '0')
  sale = Discount.get(Key(sale_key))
  sale.name = name
  sale.code = code
  sale.price = util.money.from_str(price)
  sale.put()
  memcache.delete('__lists__Discount')
  redirect('/admin/sale')


def toggle_active(sale):
  l = sale.stati
  if 'inactive' in sale.stati:
    l.remove('inactive')
    l.append('active')
  else:
    l.append('inactive')
    l.remove('active')
  sale.stati = l
  sale.put()


def toggle_admin_active(sale):
  l = sale.stati
  if 'admin_inactive' in sale.stati:
    l.remove('admin_inactive')
    l.append('admin_active')
  elif 'admin_active' not in sale.stati:
    l.append('admin_active')
  else:
    l.append('admin_inactive')
    l.remove('admin_active')
  sale.stati = l
  sale.put()


def delete_sale(sale):
  sale.stati = ['deleted']
  sale.put()


_actions = {
  'toggle_active': toggle_active,
  'toggle_admin_active': toggle_admin_active,
  'delete': delete_sale
}


@route('/admin/sale/multi_edit', method='POST')
@std_admin_wrapper()
def admin_sale_multi_edit():
  sale_keys = request.forms.getall('multi_edit')
  action = _actions.get(request.forms.get('action'), lambda x:None)
  for sale_key in sale_keys:
    sale = Discount.get(Key(sale_key))
    action(sale)
  memcache.delete('__lists__Discount')
  redirect('/admin/sale')