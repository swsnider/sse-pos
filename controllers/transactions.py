from models import *
import traceback, urllib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import secure, tg_template, jsonify

class TransactionPage(webapp.RequestHandler):
    @secure
    @tg_template("transaction.html")
    def index(self, **kwargs):
        if 'transaction_key' not in self.session:
            trans = Transaction()
            trans.owner = self.users.get_current_user()
            trans.put()
            self.session['transaction_key'] = str(trans.key())
        else:
            trans = Transaction.get(Key(encoded=self.session['transaction_key']))
        items = [LineItem.get(Key(encoded=i)) for i in trans.items]
        grand_total = 0
        for i in items:
            grand_total += i.total()
        return dict(transaction=trans, items=items, grand_total="%#.2f" % grand_total, colors=ColorCode.all().fetch(1000), itemtypes=ItemCategory.all().fetch(1000))

class TransactionAPI(webapp.RequestHandler):
    @secure
    @jsonify
    def add_item(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                trans = Transaction()
                trans.owner = self.users.get_current_user()
                trans.put()
                self.session['transaction_key'] = str(trans.key())
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))    
            t = self.request.get('data')
            item = LineItem()
            l = t.split()
            if len(l) == 2:
                quantity, cat_code, color = 1, l[0], l[1]
            else:
                quantity, cat_code, color = l[0], l[1], l[2]
            item.quantity = int(quantity)
            color = ColorCode.all().filter('code =', color).fetch(1)[0]
            category = ItemCategory.all().filter('code =', cat_code).fetch(1)[0]
            item.color = color
            item.category = category
            item.put()
            trans.items.append(str(item.key()))
            trans.put()
            grand_total = 0
            for i in trans.items:
                j = LineItem.get(Key(encoded=i))
                grand_total += j.total()
            total = category.price*int(quantity)*((100 - color.discount)/100.0)
            html = """<tr><td>%(item_id)s</td><td>%(description)s</td><td>%(price)s</td><td>%(quantity)s</td><td>%(discount)s%%</td><td>$%(total)#.2f</td></tr>""" % {'item_id': str(cat_code), 'description': str(category.description), 'price': str(category.price), 'quantity': str(quantity), 'discount':str(color.discount), 'total': total}
            return {'valid':True, 'html':html, 'total_row':"""<tr id="total_row"><th>Grand Total</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>$%s</td></tr>""" %(str(grand_total)), 'sess':repr(self.session)}
        except:
            return {'valid':False, 'payload':traceback.format_exc()}
    
    @secure
    @jsonify
    def finalize_step_1(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                return {'valid': False, 'is_error': False, 'payload': 'Unable to find the current transaction!'}
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))    
            grand_total = 0
            for i in trans.items:
                j = LineItem.get(Key(encoded=i))
                grand_total += j.total()
            return {'valid': True, 'is_error':False, 'total': grand_total}
        except:
            return {'valid': False, 'is_error':True, 'payload':traceback.format_exc()}
    
    @secure
    @jsonify
    def finalize_step_2(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                return {'valid': False, 'is_error': False, 'payload': 'Unable to find the current transaction!'}
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))    
            customer_total = float(urllib.unquote_plus(self.request.get('customer_total')))
            grand_total = 0
            for i in trans.items:
                j = LineItem.get(Key(encoded=i))
                grand_total += j.total()
            if customer_total < grand_total:
                return {'valid': False, 'is_error': False, 'payload':"The amount received from the customer is not enough to pay the outstanding balance."}
            else:
                del self.session['transaction_key']
                return {'valid': True, 'is_error': False}
        except:
            return {'valid': False, 'is_error': True, 'payload':traceback.format_exc()}
    
    @secure
    @jsonify
    def cancel(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                return {'valid': False, 'is_error': False, 'payload': 'Unable to find the current transaction!'}
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))
            trans.delete()
            del self.session['transaction_key']
            return {'valid':True, 'is_error': False}
        except:
            return {'valid': False, 'is_error': True, 'payload':traceback.format_exc()}