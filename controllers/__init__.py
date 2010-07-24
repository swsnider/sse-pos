import cgi, os
import hashlib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import render_template, secure, tg_template, jsonify, developer_only
from auth_layer import uses_users
from models import User, Visit, Transaction, Transaction2, ItemCategory
from debugging import DebuggingPages
from transactions import TransactionPage, TransactionAPI
from admin import AdminPages, ColorAPI, CategoryAPI, UserAPI, UserPages
from pos import PosPage

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
        if int(self.request.get('version', 0)) < 6:
            return dict(valid=True, data="<a onclick='destroy_cache();'>Welcome</a> " + u.first_name+" "+u.last_name + ".<a onclick=\"destroy_cache();\"><span class=\"new_feature\"> New features have been added! To enable them, click here.</span></a>")
        else:
            return dict(valid=True, data="<a onclick='destroy_cache();'>Welcome</a> " + u.first_name+" "+u.last_name)
    
    @secure
    def logout(self, **kwargs):
        if 'transaction_key' in self.session:
            try:
                Transaction2.get(Key(encoded=self.session['transaction_key'])).delete()
            except:
                Transaction.get(Key(encoded=self.session['transaction_key'])).delete()
        self.users.logout()
        self.redirect('/')
    
    @developer_only
    def logout_pred(self, **kwargs):
        self.users.logout()
        q = Visit.all()
        for r in q:
            r.delete()
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

    @tg_template("pricelist.html")
    def pricelist(self, **kwargs):
        return {'itemtypes':ItemCategory.all().filter('display =', True).order("description")}
