from bottle import route, request, redirect
import util
from util import view
from models import User


@route('/')
@view('index')
def index():
  if User.all().count(1) > 0:
    return dict()
  else:
    redirect('/setup')


@route('/login')
@view('login')
def login():
  return dict()


@route('/do_login', method="POST")
@util.provide_session
def do_login(_session):
  email = request.forms.get('email', '')
  password = request.forms.get('password', '')
  user = User.get_user(email, password)
  if user is None:
    util.flash('Incorrect email or password!')
    redirect('/login')
  _session['current_user'] = str(user.key())


@route('/logout')
@util.secure
@util.provide_session
@view('logout')
def logout(_session):
  session.delete()