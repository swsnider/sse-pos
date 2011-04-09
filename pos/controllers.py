from models import *
from google.appengine.ext.db import Key
from bottle import route, jinja2_view as view, request
from util import money


@route('/')
@view('transaction')
def transaction():
  session = request.environ.get('beaker.session')
  if 'transaction_key' not in session:
    trans = Transaction2()