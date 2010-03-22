from models import *
import traceback, urllib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import secure, tg_template, jsonify, str_to_money, money_to_str

class PosPage(webapp.RequestHandler):
    @tg_template("pos.html")
    @secure
    def index(self, **kwargs):
        if 'transaction_key' not in self.session:
            trans = Transaction2()
            trans.owner = self.users.get_current_user()
            trans.put()
            self.session['transaction_key'] = str(trans.key())
        else:
            trans = Transaction2.get(Key(encoded=self.session['transaction_key']))
            if trans is None:
                trans = Transaction2()
                trans.owner = self.users.get_current_user()
                trans.put()
                self.session['transaction_key'] = str(trans.key())
        items = [LineItem2.get(Key(encoded=i)) for i in trans.items]
        grand_total = 0
        for i in items:
            grand_total += i.total_str()
        return dict(transaction=trans, grand_total=grand_total, itemtypes=ItemCategory.all().filter('display =', True).order('description'))