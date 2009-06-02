from models import *
import traceback
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import secure, tg_template, jsonify

class TransactionPage(webapp.RequestHandler):
    @secure
    @tg_template("transaction.html")
    def index(self, **kwargs):
        return {}

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
                grand_total += j.category.price*int(j.quantity)*((100 + j.color.discount)/100.0)
            total = category.price*int(quantity)*((100 + color.discount)/100.0)
            html = """<tr><td>%(item_id)s</td><td>%(description)s</td><td>%(price)s</td><td>%(quantity)s</td><td>%(discount)s%%</td><td>%(total)s</td></tr>""" % {'item_id': str(cat_code), 'description': str(category.description), 'price': str(category.price), 'quantity': str(quantity), 'discount':str(color.discount), 'total': total}
            return {'valid':"true", 'html':html, 'total_row':"""<tr id="total_row"><th>Grand Total</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>$%s</td></tr>""" %(str(grand_total)), 'sess':repr(self.session)}
        except:
            return {'valid':"false", 'payload':traceback.format_exc()}