from models import User, Visit
from google.appengine.ext import webapp
from auth_layer import uses_users
import hashlib

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
            self.response.out.write(repr(i.modified_on) + "#")
            self.response.out.write(i.session + "#\n")

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