import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader


class TransactionLoader(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Transaction', [('created_on', lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date(), None), ('items', repr, None), ('owner', str, None)])
exporters = [TransactionLoader]

class User(db.Model):
    email = db.EmailProperty()
    salt = db.StringProperty()
    password = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    is_admin = db.BooleanProperty(default=False)
    is_developer = db.BooleanProperty(default=False)

class Transaction(db.Model):
    owner = db.ReferenceProperty(User)
    items = db.StringListProperty() # List of str(LineItem.key())
    created_on = db.DateTimeProperty(auto_now=True)
    finalized = db.BooleanProperty(default=False)
    def total(self):
        total = 0
        for i in self.items:
            it = LineItem2.get(db.Key(encoded=i))
            total += it.total()
        return total
    def total_str(self):
        return "%#.2f" % self.total()
