from google.appengine.ext import db
from google.appengine.api import urlfetch

#add models here

class User(db.Model):
    email = db.EmailProperty()
    salt = db.StringProperty()
    password = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()

class Visit(db.Model):
    expired = db.BooleanProperty()
    session = db.StringProperty()

class ItemCategory(db.Model):
    price = db.IntegerProperty()
    description = db.TextProperty()
    title = db.StringProperty()