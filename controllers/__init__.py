import cgi, os
import hashlib
from google.appengine.api import users
from google.appengine.ext import webapp
from util import render_template, secure, tg_template, jsonify
from auth_layer import uses_users
from models import User, Visit
from debugging import DebuggingPages
from transactions import TransactionPage, TransactionAPI
from admin import AdminPages, ColorAPI, CategoryAPI, UserAPI, UserPages

#'Core' controller

class GenericPages(webapp.RequestHandler):
    
    @tg_template("main.html")
    @secure
    def index(self, **kwargs):
        return {'user': self.users.get_current_user()}
    
    @jsonify
    @secure
    def user_name(self, **kwargs):
        u = self.users.get_current_user()
        return dict(valid=True, data="Welcome " + u.first_name+" "+u.last_name)
    
    @uses_users
    def logout(self, **kwargs):
        self.users.logout()
        self.redirect('/')
    
    @tg_template("login.html")
    def login(self, **kwargs):
        return {'forward_to':self.request.get('forward_to', '/')}
    
    @tg_template("login.html")
    @uses_users
    def do_login(self, **kwargs):
        if self.users.login(self.request.get('email'), self.request.get('password')):
            self.redirect('/')
        else:
            return {'forward_to': self.request.get('forward_to', '/'), 'error':True}
    
    @tg_template("denied.html")
    def denied(self, **kwargs):
        return {}