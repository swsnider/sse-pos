import cgi, os
import hashlib
from google.appengine.api import users
from google.appengine.ext import webapp
from util import render_template, secure, tg_template
from auth_layer import uses_users
from models import User, Visit
from debugging import DumpPage, InsertPage
from transactions import TransactionPage

#'Core' controllers

class MainPage(webapp.RequestHandler):
    @secure
    @tg_template("main.html")
    def get(self, **kwargs):
        return {}

class LogoutPage(webapp.RequestHandler):
    @uses_users
    def get(self, **kwargs):
        self.users.logout()
        self.redirect('/')

class LoginPage(webapp.RequestHandler):
    @tg_template("login.html")
    def get(self, **kwargs):
        return {'forward_to':self.request.get('forward_to', '/')}
    @tg_template("login.html")
    @uses_users
    def post(self, **kwargs):
        if self.users.login(self.request.get('email'), self.request.get('password')):
            self.redirect('/')
        else:
            return {'forward_to': self.request.get('forward_to', '/'), 'error':True}