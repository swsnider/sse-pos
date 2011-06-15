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
@util.provide_user
@view('pwchange')
def pwchange():
  return dict(user=request._user)


@route('/do_pwchange', method='POST')
@util.global_namespace
@util.pwchange_secure
@util.provide_user
def do_pwchange():
  old_passwd = request.forms.get('old_password', '')
  new_passwd = request.forms.get('new_password', '')
  con_passwd = request.forms.get('con_password', '')
  if new_passwd != con_passwd:
    util.flash('New and confirmation password do not match')
    redirect('/')
  if 'pwchange' not in request._user.stati:
    if not request._user.check_password(old_passwd):
      util.flash('Unable to change the password')
      redirect('/pwchange')
  request._user.change_password(new_passwd)
  redirect('/logout')