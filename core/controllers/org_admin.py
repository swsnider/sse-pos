import re

from google.appengine.ext import db

from bottle import route, request, redirect
import util
from util import view, admin_secure
from models import User, Organization

@bottle.route('/org_admin')
@bottle.route('/org_admin/')
@view('org_admin_index')
@util.global_namespace
def org_admin_index():
  return dict(orgs=Organization.all().filter('stati =', 'active'))