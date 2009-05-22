import cgi, os
import hashlib
from google.appengine.api import users
from google.appengine.ext import webapp
from util import render_template, secure, tg_template
from auth_layer import uses_users
from models import User, Visit

class MainPage(webapp.RequestHandler):
    @secure
    @tg_template("main.html")
    def get(self, **kwargs):
        return {}

class LogoutPage(webapp.RequestHandler):
    @sec

class DumpPage(webapp.RequestHandler):
    @uses_users
    def get(self, **kwargs):
        r = User.all().fetch(1000)
        for i in r:
            self.response.out.write(str(i.key().id_or_name()) + "#")
            self.response.out.write(i.email+"#")
            self.response.out.write(i.salt +"#")
            self.response.out.write(i.password + "#")
            self.response.out.write(i.first_name+ "#")
            self.response.out.write(i.last_name+"#\n")
        self.response.out.write("\n\n")
        self.response.out.write(repr(self.session))
        self.response.out.write("\n\n")
        r = Visit.all().fetch(1000)
        for i in r:
            self.response.out.write(str(i.key().id_or_name()) + "#")
            self.response.out.write(repr(i.expired) + "#")
            self.response.out.write(i.session + "#\n")

class LoginPage(webapp.RequestHandler):
    @tg_template("login.html")
    def get(self, **kwargs):
        return {'forward_to':self.request.get('forward_to', '/')}
    @tg_template("login.html")
    @uses_users
    def post(self, **kwargs):
        if self.users.login(self.request.get('email'), self.request.get('password')):
            self.response.out.write(repr(self.session))
        else:
            return {'forward_to': self.request.get('forward_to', '/'), 'error':True}

class InsertPage(webapp.RequestHandler):
    def get(self, **kwargs):
        h = hashlib.sha512()
        h.update("silas")
        h.update("qwe")
        u = User()
        u.email="swsnider@gmail.com"
        u.salt='qwe'
        u.password=h.hexdigest()
        u.first_name="Silas"
        u.last_name="Snider"
        u.put()
        self.redirect('/')