from google.appengine.ext import db
from google.appengine.api import urlfetch
from util import *
import hashlib

#add models here

__all__ = ['User', 'Visit', 'ItemCategory', 'ColorCode', 'LineItem2', 'LineItem', 'Transaction', 'Transaction2', 'Setting']

class Deposits(db.Model):
    amount = db.IntegerProperty()
    explanation = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class InitialCount(db.Model):
    amount = db.IntegerProperty()
    explanation = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class DailyStats(db.Model):
    day = db.DateProperty()
    volume = db.IntegerProperty()
    revenue = db.IntegerProperty()
    donations = db.IntegerProperty()
    giftcerts = db.IntegerProperty()

class User(db.Model):
    email = db.EmailProperty()
    salt = db.StringProperty()
    password = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    is_admin = db.BooleanProperty(default=False)
    is_developer = db.BooleanProperty(default=False)
    def gravatarHash(self):
        return str(hashlib.md5(self.email.strip().lower()).hexdigest())

class Visit(db.Model):
    expired = db.BooleanProperty()
    session = db.StringProperty()
    modified_on = db.DateTimeProperty(auto_now=True)

class ItemCategory(db.Model):
    price = db.IntegerProperty()
    description = db.StringProperty()
    code = db.StringProperty()
    display = db.BooleanProperty(default=True)
    
    def get_price(self):
        import util
        return util.money_to_str(self.price)

class ColorCode(db.Model):
    discount = db.IntegerProperty()
    color = db.StringProperty()
    code = db.StringProperty()
    display = db.BooleanProperty(default=True)

class LineItem(db.Model):
    color = db.ReferenceProperty(ColorCode)
    quantity = db.IntegerProperty()
    category = db.ReferenceProperty(ItemCategory)
    misc_amount = db.IntegerProperty(default=0)
    misc_discount = db.IntegerProperty(default=0)
    def get_discount(self):
        if self.color.discount == 0:
            return self.misc_discount
        else:
            return self.color.discount
    def total(self):
        return (((self.category.price/100.0) + self.misc_amount)*int(self.quantity)*((100 - self.get_discount())/100.0))
    def total_str(self):
        return "%#.2f" % self.total()

class LineItem2(db.Model):
    discount = db.IntegerProperty()
    quantity = db.IntegerProperty()
    price = db.IntegerProperty()
    color = db.StringProperty()
    category = db.StringProperty()
    color_code = db.StringProperty()
    category_code = db.StringProperty()
    def set_color(self, color):
        self.color = color.color
        self.color_code = color.code
        self.discount = color.discount
    def set_category(self, cat):
        self.category = cat.description
        self.price = cat.price
        self.category_code = cat.code
    def get_discount(self):
        return self.discount
    
    def total(self):
        return (self.price * self.quantity * ((100 - self.get_discount())/100.0))/100.0
    
    def get_price(self):
        import util
        return util.money_to_str(self.price)
    
    def total_str(self):
        return "%#.2f" % self.total()

class Transaction(db.Model):
    owner = db.ReferenceProperty(User)
    items = db.StringListProperty() # List of str(LineItem.key())
    created_on = db.DateTimeProperty(auto_now_add=True)
    finalized = db.BooleanProperty(default=False)
    def total(self):
        total = 0
        for i in self.items:
            it = LineItem.get(db.Key(encoded=i))
            total += it.total()
        self.put()
        return total
    def total_str(self):
        return "%#.2f" % self.total()

class Transaction2(db.Model):
    import util.db
    owner = db.ReferenceProperty(User)
    items = db.StringListProperty() # List of str(LineItem2.key())
    created_on = util.db.ESTTZDateTimeProperty(auto_now_add=True)
    finalized = db.BooleanProperty(default=False)
    cached_total = db.IntegerProperty(default=0)
    cached_cert = db.IntegerProperty(default=0)
    daily_stats_collected = db.BooleanProperty(default=False)
    def total(self):
        total = 0
        for i in self.items:
            it = LineItem2.get(db.Key(encoded=i))
            total += it.total()
        self.cached_total = int(total * 100)
        self.put()
        return total
    def total_and_cert(self):
        total = 0
        cert = 0
        for i in self.items:
            it = LineItem2.get(db.Key(encoded=i))
            total += it.total()
            if it.category_code == ":::":
                cert += -it.total()
        self.cached_total = int(total * 100)
        self.cached_cert = int(cert * 100)
        self.put()
        return total, cert
    def total_str(self):
        return "%#.2f" % self.total()

class Setting(db.Model):
    name = db.StringProperty()
    set_at = db.StringProperty()