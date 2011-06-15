from google.appengine.api import users
import bottle
from bottle import request, redirect
from presentation import flash
from google.appengine.ext import db


def provide_user(f):
  def g(*args, **kwargs):
    if '_user' not in dir(request):
      user_key = request.environ.get('beaker.session').get('current_user', None)
      if user_key is None:
        redirect('/login')
      request._user = db.get(user_key)
      _user = request._user
      if 'active' not in _user.stati or 'active' not in _user.organization.stati:
        request.environ.get('beaker.session').invalidate()
        flash('Invalid user!')
        redirect('/login')
    return f(*args, **kwargs)
  return g


def secure(f):
  def g(*args, **kwargs):
    session = bottle.request.environ.get('beaker.session')
    if 'current_user' not in session:
      bottle.redirect('/login')
    if 'pwchange' in db.get(db.Key(session['current_user'])).stati:
      redirect('/pwchange')
    return f(*args, **kwargs)
  return g


def pwchange_secure(f):
  def g(*args, **kwargs):
    session = bottle.request.environ.get('beaker.session')
    if 'current_user' not in session:
      bottle.redirect('/login')
    return f(*args, **kwargs)
  return g

def admin_secure(f):
  def g(*args, **kwargs):
    if not users.is_current_user_admin():
      flash('You are not a super-admin!')
      bottle.redirect('/')
    return f(*args, **kwargs)
  return g

def has_stati(*stati):
  def h(f):
    @provide_user
    def g(*args, **kwargs):
      for status in stati:
        if status not in request._user.stati:
          flash('Incorrect credentials')
          bottle.redirect('/')
      return f(*args, **kwargs)
    return g
  return h

def is_authenticated():
  session = bottle.request.environ.get('beaker.session')
  return 'current_user' in session