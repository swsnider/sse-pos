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
    modified_on = db.DateTimeProperty(auto_now=True)

class ItemCategory(db.Model):
    price = db.IntegerProperty()
    description = db.StringProperty()
    code = db.StringProperty()

class ColorCode(db.Model):
    discount = db.IntegerProperty()
    color = db.StringProperty()
    code = db.StringProperty()

class LineItem(db.Model):
    color = db.ReferenceProperty(ColorCode)
    quantity = db.IntegerProperty()
    category = db.ReferenceProperty(ItemCategory)

class Transaction(db.Model):
    owner = db.ReferenceProperty(User)