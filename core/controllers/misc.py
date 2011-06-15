from bottle import route, request, redirect
import util
from util import view, user_namespace
from models import User


@route('/')
@util.secure
@view('index')
@user_namespace
def index():
  return dict()


@route('/login')
@view('login')
def login():
  return dict()


@route('/do_login', method="POST")
@util.provide_session
@util.global_namespace
def do_login():
  _session = request._session
  email = request.forms.get('email', '')
  password = request.forms.get('password', '')
  user = User.get_user(email, password)
  if user is None or 'deleted' in user.stati or 'inactive' in user.stati:
    util.flash('Incorrect email or password!')
    redirect('/login')
  _session['current_user'] = str(user.key())
  redirect('/')


@route('/logout')
@util.secure
@util.provide_session
def logout():
  request._session.delete()
  redirect('/')


@route('/pwchange')
@util.pwchange_secure
@view('pwchange')
def pwchange():
  return dict()


@route('/do_pwchange', method='POST')
@util.pwchange_secure
@util.provide_user
def do_pwchange():
  
  redirect('/')