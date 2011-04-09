from models import *
from google.appengine.ext.db import Key
from bottle import route, jinja2_view as view, request
from util import money, secure


@route('/')
@view('transaction')
@secure()
def transaction():
  session = request.environ.get('beaker.session')
  trans = None
  if 'transaction_key' not in session:
    trans = Transaction2()
    trans.owner = User.get(Key(encoded=session['user']))
    trans.put()
    session['transaction_key'] = str(trans.key())
  else:
    trans = Transaction2.get(Key(encoded=session['transaction_key']))
    if trans is None:
      trans = Transaction2()
      trans.owner = User.get(Key(encoded=session['user']))
      trans.put()
      session['transaction_key'] = str(trans.key())
  items = [LineItem2.get(Key(encoded=i)) for i in trans.items]
  grand_total = 0
  for i in items:
    grand_total += i.total()
  return dict(transaction=trans, items=items, grand_total="%#.2f" % grand_total, colors=ColorCode.all().filter('display =', True).order('color'), itemtypes=ItemCategory.all().filter('display =', True).order('description'))