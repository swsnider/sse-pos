from models import *
from datetime import datetime
from google.appengine.ext import webapp
from auth_layer import uses_users
import hashlib
from util import jsonify, secure

class DebuggingPages(webapp.RequestHandler):
    def fix_items(self, **kwargs):
        its = ItemCategory.all()
        for i in its:
            i.display = True
            i.put()
        cos = ColorCode.all()
        for c in cos:
            c.display = True
            c.put()
        return    
    
    def add_dates(self, **kwargs):
        trans = Transaction.all().fetch(1000)
        for t in trans:
            t.created_on = datetime.now()
            t.put()
    @uses_users
    def dump(self, **kwargs):
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
            self.response.out.write(repr(i.modified_on) + "#")
            self.response.out.write(i.session + "#\n")
    @jsonify
    def insert_item(self, **kwargs):
        i = ItemCategory()
        i.price=7
        i.code="j"
        i.description = 'A small, plain, red-colored, letter J'
        i.put()
        c = ColorCode()
        c.code = 'r'
        c.color = 'Red'
        c.discount = 7
        c.put()
        return {}
    def new(self, **kwargs):
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
    
    @jsonify
    @secure
    def make_admin(self, **kwargs):
        u = self.users.get_current_user()
        u.is_admin = True
        u.put()
        return {}