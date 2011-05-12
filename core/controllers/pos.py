from models import *
from google.appengine.ext.db import Key
from bottle import route, request, redirect
import util
from util import view


class NoSaleError(Exception):
  """Raised if there isn't a sale present."""
  pass


def ensure_sale(f):
  def g(*args, **kwargs):
    session = request.environ.get('beaker.session')
    sale = None
    if 'sale_key' not in session:
      sale = Sale()
      sale.owner = User.get(Key(encoded=session['current_user']))
      sale.put()
      session['sale_key'] = str(sale.key())
    else:
      sale = Sale.get(Key(encoded=session['sale_key']))
      if sale is None:
        sale = Sale()
        sale.owner = User.get(Key(encoded=session['current_user']))
        sale.put()
        session['sale_key'] = str(sale.key())
    kwargs['_sale'] = sale
    return f(*args, **kwargs)
  return g


def require_sale(f):
  def g(*args, **kwargs):
    session = request.environ.get('beaker.session')
    if 'sale_key' not in session:
      util.flash('Error #777')
      raise NoSaleError('Error #777')
    sale = Sale.get(Key(encoded=session['sale_key']))
    if sale is None:
      util.flash('Error #778')
      raise NoSaleError('Error #778')
    kwargs['_sale'] = sale
    return f(*args, **kwargs)
  return g


@route('/pos')
@route('/pos/')
@view('pos')
@util.secure
@ensure_sale
def main_page(_sale):
  pending_items = _sale.get_items()
  grand_total = util.money.to_str(_sale.get_total())
  colors, items = util.get_lists('Color', 'Item')
  return dict(sale=_sale, items=items, grand_total=grand_total, colors=colors, itemtypes=items)