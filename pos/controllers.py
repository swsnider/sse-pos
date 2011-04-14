from models import *
from google.appengine.ext.db import Key
from google.appengine.api import memcache
from bottle import route, jinja2_view as view, request
import util


@route('/')
@view('transaction')
@util.secure()
def main():
  session = request.environ.get('beaker.session')
  sale = None
  if 'sale_key' not in session:
    sale = Sale()
    sale.owner = User.get(Key(encoded=session['current_user']['key']))
    sale.put()
    session['sale_key'] = str(sale.key())
  else:
    sale = Sale.get(Key(encoded=session['sale_key']))
    if sale is None:
      sale = Transaction2()
      sale.owner = User.get(Key(encoded=session['user']))
      sale.put()
      session['sale_key'] = str(sale.key())
  pending_items = sale.get_items()
  grand_total = money.to_str(sale.get_total())
  colors, items = util.get_lists('Color', 'Item')
  return dict(sale=sale, items=items, grand_total=grand_total, colors=colors, itemtypes=items)