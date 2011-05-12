from bottle import route, request, redirect
import util
from util import view
from models import User

@route('/setup')
@route('/setup/')
@view('setup')
def setup_main():
  return dict()

@route('/setup/do_setup', method='POST')
@view('setup_fin')
@util.provide_session
def finish_setup(_session):
  email = request.forms.get('email', '')
  password = request.forms.get('password', '')
  first_name = request.forms.get('first_name', '')
  last_name = request.forms.get('last_name', '')
  user = User()
  user.email = email
  user.salt, user.password = User.generate_password(password)
  user.first_name = first_name
  user.last_name = last_name
  user.stati = ['admin', 'active']
  key = user.put()
  _session['current_user'] = str(key)
  return dict()