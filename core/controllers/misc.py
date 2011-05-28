from bottle import route, request, redirect
import util
from util import view, user_namespace
from models import User


@route('/')
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
  if user is None:
    util.flash('Incorrect email or password!')
    redirect('/login')
  _session['current_user'] = str(user.key())
  redirect('/')


@route('/logout')
@util.secure
@util.provide_session
@view('logout')
def logout():
  request._session.delete()