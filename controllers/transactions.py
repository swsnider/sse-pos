from models import *
import traceback, urllib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import secure, tg_template, jsonify, str_to_money, money_to_str

class TransactionPage(webapp.RequestHandler):
    
    @tg_template("transaction.html")
    @secure
    def index(self, **kwargs):
        if 'transaction_key' not in self.session:
            trans = Transaction()
            trans.owner = self.users.get_current_user()
            trans.put()
            self.session['transaction_key'] = str(trans.key())
        else:
            trans = Transaction.get(Key(encoded=self.session['transaction_key']))
            if trans is None:
                trans = Transaction()
                trans.owner = self.users.get_current_user()
                trans.put()
                self.session['transaction_key'] = str(trans.key())
        items = [LineItem2.get(Key(encoded=i)) for i in trans.items]
        grand_total = 0
        for i in items:
            grand_total += i.total()
        return dict(transaction=trans, items=items, grand_total="%#.2f" % grand_total, colors=ColorCode.all().filter('display =', True).order('color'), itemtypes=ItemCategory.all().filter('display =', True).order('description'))
    
    @jsonify
    @secure
    def donate(self, **kwargs):
        try:
            amt = str_to_money(self.request.get('amt', False))
        except:
            return dict(valid=False, payload=traceback.format_exc())
        trans = Transaction()
        trans.owner = self.users.get_current_user()
        trans.put()
        item = LineItem2()
        item.category = "DONATION"
        item.category_code = "+++"
        item.quantity = 1
        item.price = amt
        item.color = "DONATION"
        item.color_code = "+++"
        item.discount = 0
        item.put()
        trans.items.append(str(item.key()))
        trans.finalized = True
        trans.put()
        return dict(valid=True)
        

class TransactionAPI(webapp.RequestHandler):
    
    @jsonify
    @secure
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
            if t.startswith('$'):
                #misc processing
                l = t.split()
                price, color_inp = l[0], l[1]
                #if '.' in price:
                #    z = price.split('.')
                #    dollars, cents = z[0], z[1]
                #    price = int(dollars) + int(cents)*100
                price = str_to_money(price[1:])
                item = LineItem2()
                item.category = "MISC"
                item.category_code = "$$$"
                item.price = price
                item.quantity = 1
                color = ColorCode.all().filter('code =', color_inp).get()
                if color == None:
                    raise "Bad color"
                item.color = color.color
                item.color_code = color.code
                item.discount = color.discount
                item.put()
                trans.items.append(str(item.key()))
                if len(trans.items) % 2 == 0:
                    class_val = 'even'
                else:
                    class_val = 'odd'
                html = """<tr class="%(class)s" id="%(key)s"><td>%(item_id)s</td><td>%(description)s</td><td>$%(price)s</td><td>%(quantity)s</td><td>%(discount)s%%</td><td>$%(total)s</td><td><a class="delete_button" onclick="void_item('%(key)s')">void</a></td></tr>""" % {'key': str(item.key()), 'item_id': str(item.category_code), 'description': str(item.category), 'price': money_to_str(price), 'quantity': str(1), 'discount':str(item.get_discount()), 'total': item.total_str(), "class":class_val}
            else:
                item = LineItem2()
                l = t.split()
                if len(l) == 2:
                    quantity, cat_code, color = 1, l[0], l[1]
                else:
                    quantity, cat_code, color = l[0], l[1], l[2]
                item.quantity = int(quantity)
                if color.startswith('%'):
                    #custom precentage handler
                    item.discount = int(color[1:])
                    item.color = 'CUSTOM'
                    item.color_code = '%%%'
                else:                
                    color = ColorCode.all().filter('code =', color).fetch(1)[0]
                category = ItemCategory.all().filter('code =', cat_code).fetch(1)[0]
                item.set_color(color)
                item.set_category(category)
                item.put()
                trans.items.append(str(item.key()))
                if len(trans.items) % 2 == 0:
                    class_val = 'even'
                else:
                    class_val = 'odd'
                total = item.total()
                html = """<tr class="%(class)s" id="%(key)s"><td>%(item_id)s</td><td>%(description)s</td><td>%(price)s</td><td>%(quantity)s</td><td>%(discount)s%%</td><td>$%(total)#.2f</td><td><a class="delete_button" onclick="void_item('%(key)s')">void</a></td></tr>""" % {'key': str(item.key()), 'item_id': str(cat_code), 'description': str(category.description), 'price': money_to_str(category.price), 'quantity': str(quantity), 'discount':str(item.get_discount()), 'total': total, "class":class_val}
            trans.put()
            grand_total = 0
            for i in trans.items:
                j = LineItem2.get(Key(encoded=i))
                grand_total += j.total()
            return {'valid':True, 'html':html, 'total_row':"""<tr id="total_row"><th>Grand Total</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>$%s</td></tr>""" %(str(grand_total)), 'sess':repr(self.session)}
        except:
            return {'valid':False, 'payload':traceback.format_exc()}
    
    
    @jsonify
    @secure
    def finalize_step_1(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                return {'valid': False, 'is_error': False, 'payload': 'Unable to find the current transaction!'}
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))    
            grand_total = 0
            for i in trans.items:
                j = LineItem2.get(Key(encoded=i))
                grand_total += j.total()
            return {'valid': True, 'is_error':False, 'total': (grand_total)}
        except:
            return {'valid': False, 'is_error':True, 'payload':traceback.format_exc()}
    
    
    @jsonify
    @secure
    def finalize_step_2(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                return {'valid': False, 'is_error': False, 'payload': 'Unable to find the current transaction!'}
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))    
            customer_total = str_to_money(urllib.unquote_plus(self.request.get('customer_total')))
            grand_total = 0
            for i in trans.items:
                j = LineItem2.get(Key(encoded=i))
                grand_total += j.total()
            if customer_total < grand_total:
                return {'valid': False, 'is_error': False, 'payload':"The amount received from the customer is not enough to pay the outstanding balance."}
            else:
                trans.finalized = True
                trans.put()
                del self.session['transaction_key']
                return {'valid': True, 'is_error': False}
        except:
            return {'valid': False, 'is_error': True, 'payload':traceback.format_exc()}
    
    
    @jsonify
    @secure
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
    
    @jsonify
    @secure
    def void_item(self, **kwargs):
        try:
            if 'transaction_key' not in self.session:
                return {'valid': False, 'is_error': False, 'payload': 'Unable to find the current transaction!'}
            else:
                trans = Transaction.get(Key(encoded=self.session['transaction_key']))
            trans.items.remove(self.request.get('data'))
            trans.put()
            return {'valid':True, 'is_error': False, 'total_row': """<tr id="total_row"><th>Grand Total</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>$%s</td></tr>""" % trans.total_str()}
        except:
            return {'valid': False, 'is_error': True, 'payload':traceback.format_exc()}