from google.appengine.ext import db
from google.appengine.api import urlfetch

#add models here

__all__ = ['User', 'Visit', 'ItemCategory', 'ColorCode', 'LineItem', 'Transaction']

class User(db.Model):
    email = db.EmailProperty()
    salt = db.StringProperty()
    password = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    is_admin = db.BooleanProperty(default=False)

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
    def total(self):
        return self.category.price*int(self.quantity)*((100 - self.color.discount)/100.0)
    def total_str(self):
        return "%#.2f" % self.total()

class Transaction(db.Model):
    owner = db.ReferenceProperty(User)
    items = db.StringListProperty() # List of str(LineItem.key())