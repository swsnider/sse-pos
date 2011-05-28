import re

from google.appengine.ext import db

from bottle import route, request, redirect
import util
from util import view, admin_secure
from models import User, Organization

@route('/org_admin/setup')
@route('/org_admin/setup/')
@view('org_setup')
@admin_secure
def setup_main():
  return dict()

@route('/org_admin/setup/do_setup', method='POST')
@view('setup_fin')
@admin_secure
def finish_setup():
  org_name = request.forms.get('org_name', '')
  email = request.forms.get('email', '')
  first_name = request.forms.get('first_name', '')
  last_name = request.forms.get('last_name', '')
  org = Organization()
  org.name = org_name
  org.stati = ['active']
  org.namespace = re.sub(r'[^-0-9A-Za-z\._]', '-', org_name.replace('-', '_'))
  org.put()
  user = User()
  user.email = email
  user.salt, user.password, password = User.generate_password()
  user.first_name = first_name
  user.last_name = last_name
  user.organization = org
  user.stati = ['admin', 'active', 'pwchange']
  key = user.put()
  user = db.get(key)
  return dict(user=user, password=password)