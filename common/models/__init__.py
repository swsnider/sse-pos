from google.appengine.ext import db
from google.appengine.api import urlfetch
from global_defs import *
import util
import hashlib

#add models here

__all__ = ['User', 'Visit', 'ItemCategory', 'ColorCode', 'LineItem2', 'LineItem', 'Transaction', 'Transaction2', 'Setting']

class User(db.Model):
  email = db.EmailProperty()
  salt = db.StringProperty()
  password = db.StringProperty()
  first_name = db.StringProperty()
  last_name = db.StringProperty()
  stati = db.StringListProperty()

class Item(db.Model):
  name = db.StringProperty()
  price = db.IntegerProperty()
  code = db.StringProperty()
  stati = db.StringListProperty()

class Color(db.Model):
  name = db.StringProperty()
  discount = db.IntegerProperty()
  code = db.StringProperty()
  stati = db.StringListProperty()

class Sale(db.Model):
  owner = db.ReferenceProperty(User)
  # Items is a list of colon delimited strings
  # Format: item:color:quantity:discount:per_item_price:tax
  items = db.StringListProperty()
  created_on = util.db.ESTTZDateTimeProperty(auto_now_add=True)
  finalized = db.BooleanProperty()
  stati = db.StringListProperty()

  def get_items(self):
    return [tuple(i.split(':')) for i in self.items]

  def get_total(self):
    running_total = 0
    for i in self.get_items():
      subtotal = int(i[4]) * int(i[2])
      discount = (int(i[3]) / 100.0) * subtotal
      discounted = subtotal - discount
      running_total += discounted + int(i[5]) # add in the tax
    return running_total
  

class Setting(db.Model):
  name = db.StringProperty()
  value = db.StringProperty()