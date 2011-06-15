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
  def generate_salt():
    salt = []
    for i in xrange(64):
      salt.append(random.choice(salt_chars))
    salt = ''.join(salt)
    return salt

  @staticmethod
  def generate_password(plaintext_pwd = None):
    if plaintext_pwd is None:
      pwd = []
      for i in range(16):
        pwd.append(random.choice(salt_chars))
      plaintext_pwd = ''.join(pwd)
      del pwd
    salt = User.generate_salt()
    return (salt, hashlib.sha512(salt + plaintext_pwd).hexdigest(), plaintext_pwd)

  def change_password(self, password):
    salt = User.generate_salt()
    self.salt = salt
    self.password = hashlib.sha512(salt+password).hexdigest()
    if 'pwchange' in self.stati:
      self.stati.remove('pwchange')
    self.put()

  def check_password(self, password):
    cand_pwd = hashlib.sha512(self.salt+password).hexdigest()
    return cand_pwd == self.password

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

  def add_item(self, item, color, quantity):
    discount = 0
    for i in Discount.all().filter('stati =', 'active'):
      discount += i.get_discount_for_item(item)
    tax = 0
    if 'taxable' in item.stati:
      tax = item.price * TAX_RATE
    item_list = [item.name,color.name,str(quantity),str(color.discount),str(item.price - discount),str(tax)]
    self.items.append(':'.join(item_list))
    self.put()

  def get_items(self):
    return [tuple(i.split(':')) for i in self.items]

  def get_subtotal(self):
    running_total = 0
    for i in self.get_items():
      subtotal = int(i[4]) * int(i[2])
      discount = (int(i[3]) / 100.0) * subtotal
      discounted = subtotal - discount
      running_total += discounted + int(i[5]) # add in the tax
    return running_total

  def get_total(self):
    discount = 0
    for i in (Discount.all().filter('stati =', 'active')):
      discount += i.get_discount_for_sale(self)
    return self.get_subtotal() - discount
  

class Discount(db.Model):
  name = db.StringProperty()
  start_date = db.DateTimeProperty()
  end_date = db.DateTimeProperty()
  items = db.StringListPropert()
  # This is an encoded string -- you should use one of the methods below to set
  # it, instead of looking at it directly.
  discount = db.StringProperty()
  #Two possible values: 'cart' or 'item'
  scope = db.StringProperty()
  stati = db.StringListProperty()
  ORDERING = ('name')
  USEFUL_FIELDS = (
    'name',
    'start_date',
    'end_date',
    'items',
    'discount',
    'stati'
  )

  def flat_rate_discount(self, price):
    self.discount = 'flat:%s' % price

  def percentage_discount(self, percentage):
    self.discount = 'percent:%s' % percentage

  def price_set_discount(self, price):
    self.discount = 'set_price:%s' % price

  def get_discount_for_item(self, item):
    '''Returns the amount to discount the given item by.'''
    if 'dated' in self.stati:
      # TODO(swsnider): Calculate whether the current time is in the date range
    if item.key() not in self.items or scope == 'cart':
      return 0
    discount_num = int(self.discount.split(':')[1])
    if self.discount.startswith('flat'):
      return discount_num
    elif self.discount.startswith('percent'):
      return item.price * (discount_num / 100.0)
    elif self.discount.startswith('set_price'):
      return item.price - discount_num

  def get_discount_for_sale(self, sale):
    '''Returns the amount to discount the given cart by.'''
    if 'dated' in self.stati:
      # TODO(swsnider): Calculate whether the current time is in the date range
    if scope != 'cart':
      return 0
    discount_num = int(self.discount.split(':')[1])
    if self.discount.startswith('flat'):
      return discount_num
    elif self.discount.startswith('percent'):
      return sale.get_subtotal() * (discount_num / 100.0)
    elif self.discount.startswith('set_price'):
      return sale.get_subtotal() - discount_num

class Setting(db.Model):
  name = db.StringProperty()
  value = db.StringProperty()
  ORDERING = ('name',)
  USEFUL_FIELDS = (
      'name',
      'value'
  )