import bottle
from auth_layer import uses_users
from models import Setting
import random

def secure(f):
  def g(*args, **kwargs):
    session = bottle.request.environ.get('beaker.session')
    if 'current_user' not in session:
      bottle.redirect('/login')
    return f(*args, **kwargs)