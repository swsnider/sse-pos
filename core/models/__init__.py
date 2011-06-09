from global_defs import *
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import namespace_manager
import util
import hashlib
import random

__all__ = ['Organization', 'User', 'Item', 'Color', 'Sale', 'Setting', 'MODEL_CLASSES']

MODEL_CLASSES = [
  'Organization',
  'User',
  'Item',
  'Color',
  'Sale',
  'Setting'
]

salt_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

class Organization(db.Model):
  name = db.StringProperty()
  namespace = db.StringProperty()
  stati = db.StringListProperty()

class User(db.Model):
  email = db.EmailProperty()
  salt = db.StringProperty()
  password = db.StringProperty()
  first_name = db.StringProperty()
  last_name = db.StringProperty()
  organization = db.ReferenceProperty(Organization)
  stati = db.StringListProperty()
  initial_password = db.StringProperty()
  ORDERING = ('last_name', 'first_name')
  USEFUL_FIELDS = (
      'email',
      'salt',
      'password',
      'first_name',
      'last_name',
      'stati')

  @staticmethod
  def generate_password(plaintext_pwd = None):
    if plaintext_pwd is None:
      pwd = []
      for i in range(16):
        pwd.append(random.choice(salt_chars))
      plaintext_pwd = ''.join(pwd)
      del pwd
    salt = []
    for i in xrange(64):
      salt.append(random.choice(salt_chars))
    salt = ''.join(salt)
    return (salt, hashlib.sha512(salt + plaintext_pwd).hexdigest(), plaintext_pwd)

  @staticmethod
  def get_user(email, password):
    old_namespace = namespace_manager.get_namespace()
    namespace_manager.set_namespace('-global-')
    user = User.all().filter('email =', email).filter('stati =', 'active').get()
    if user is None:
      return None
    salt = user.salt
    candidate_hash = hashlib.sha512(salt + password).hexdigest()
    namespace_manager.set_namespace(old_namespace)
    if user.password == candidate_hash:
      return user
    else:
      return None

class Item(db.Model):
  name = db.StringProperty()
  price = db.IntegerProperty()
  code = db.StringProperty()
  stati = db.StringListProperty()
  ORDERING = ('name', 'price')
  USEFUL_FIELDS = (
      'name',
      'price',
      'code',
      'stati'
  )

class Color(db.Model):
  name = db.StringProperty()
  discount = db.IntegerProperty()
  code = db.StringProperty()
  stati = db.StringListProperty()
  ORDERING = ('name', 'discount')
  USEFUL_FIELDS = (
      'name',
      'discount',
      'code',
      'stati'
  )

class Sale(db.Model):
  owner = db.ReferenceProperty(User)
  # Items is a list of colon delimited strings
  # Format: item:color:quantity:discount:per_item_price:tax
  items = db.StringListProperty()
  created_on = db.DateTimeProperty(auto_now_add=True)
  stati = db.StringListProperty()
  ORDERING = ('-created_on', 'finalized')
  USEFUL_FIELDS = (
      'items',
      'created_on',
      'stati'
  )

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
  ORDERING = ('name',)
  USEFUL_FIELDS = (
      'name',
      'value'
  )