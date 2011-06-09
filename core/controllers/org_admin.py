import StringIO
import sys
import re

from google.appengine.ext import db

from bottle import route, request, redirect, abort, jinja2_template as template
import util
from util import view, admin_secure
from models import Organization, User


@route('/org_admin')
@route('/org_admin/')
@util.global_namespace
@view('org_admin_index')
@admin_secure
def org_admin_index():
  return dict(orgs=Organization.all().filter('stati =', 'active'))


@route('/org_admin/:organization')
@util.global_namespace
@view('org_admin_details')
@admin_secure
def org_admin_details(organization):
  org = Organization.get(db.Key(organization))
  return dict(organization=org)


@route('/org_admin/:user/reset_pwd')
@util.global_namespace
@admin_secure
def org_admin_user_pwd_reset(user):
  user = User.get(db.Key(user))
  user.salt, user.password, user.initial_password = User.generate_password()
  if 'pwchange' not in user.stati:
    user.stati = user.stati + ['pwchange']
  user.put()
  redirect('/org_admin/%s' % user.organization.key())


@route('/org_admin/create', method='POST')
@util.global_namespace
@admin_secure
def org_admin_create():
  org = Organization()
  org.name = request.forms.get('org_name', '')
  org.stati = ['active']
  org.namespace = re.sub(r'[^-0-9A-Za-z\._]', '-', org.name.replace('-', '_'))
  key = org.put()
  redirect('/org_admin/%s' % (str(key)))


@route('/org_admin/:organization/new_admin', method='POST')
@util.global_namespace
@admin_secure
def org_admin_new_admin_commit(organization):
  org = Organization.get(db.Key(organization))
  email = request.forms.get('email', '')
  first_name = request.forms.get('first_name', '')
  last_name = request.forms.get('last_name', '')
  user = User()
  user.email = email
  user.salt, user.password, user.initial_password = User.generate_password()
  user.first_name = first_name
  user.last_name = last_name
  user.organization = org
  user.stati = ['admin', 'active', 'pwchange']
  key = user.put()
  redirect('/org_admin/%s' % org.key())