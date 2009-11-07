import traceback, urllib, hashlib, time
from models import *
from util import *
from datetime import datetime, date, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.db import Key

class AdminPages(webapp.RequestHandler):
    @tg_template('admin.html')
    @admin_only
    def index(self, **kwargs):
        return {}

    @admin_only
    @csvify
    def export_users(self, **kwargs):
        keys = User.properties().keys()
        instances = User.all()
        result = []
        headers = {}
        for i in keys:
            headers[i] = i
        result.append(headers)
        for i in instances:
            curr = {}
            result.append(curr)
            for j in keys:
                curr[j] = str(getattr(i, j))
        return result

    @tg_template('category_list.html')
    @admin_only
    def category(self, **kwargs):
        return dict(categories=ItemCategory.all(), conv=money_to_str)
    
    @tg_template('color_list.html')
    @admin_only
    def color(self, **kwargs):
        return dict(colors=ColorCode.all())
    
    
    @tg_template('unimplemented.html')
    @admin_only
    def reports(self, **kwargs):
        return dict(return_url="/admin")
    
    
    @tg_template('user_list.html')
    @admin_only
    def user(self, **kwargs):
        return dict(users=User.all())
    
    
    @tg_template('new_stats.html')
    @admin_only
    def stats(self, **kwargs):
        date_requested = self.request.get('date_data', False)
        oneDay = timedelta(days=1)
        if not date_requested:
            now = datetime.now()
            if int(now.hour) < 5:
                date_requested = (date.today() - oneDay).strftime('%Y-%m-%d')
            else:
                date_requested = date.today().strftime('%Y-%m-%d')
        ts = Transaction2.gql("WHERE created_on >= :1 AND finalized = True", datetime.strptime(date_requested, '%Y-%m-%d'))
        our_total = 0
        our_count = 0
        cert_today = 0
        for i in ts:
            our_count += 1
            if i.cached_total not in [None, 0] and i.cached_cert not in [None,0]:
                our_total += i.cached_total / 100.0
                cert_today += i.cached_cert / 100.0
            else:
                total, cert = i.total_and_cert()
                our_total += total
                cert_today += cert
        return dict(sales_today=our_count, sales_today_total=our_total, date_requested=date_requested, cert_today=cert_today)
        
        
    @tg_template('stats.html')
    @admin_only
    def old_stats(self, **kwargs):
        date_requested = self.request.get('date_data', False)
        oneDay = timedelta(days=1)
        if not date_requested:
            now = datetime.now()
            if int(now.hour) < 5:
                date_requested = (date.today() - oneDay).strftime('%Y-%m-%d')
            else:
                date_requested = date.today().strftime('%Y-%m-%d')
        ts = Transaction.gql("WHERE created_on >= :1 AND finalized = True", datetime.strptime(date_requested, '%Y-%m-%d'))
        our_total = 0
        our_count = 0
        for i in ts:
            if i.items is None or len(i.items) == 0:
                            continue
            our_count += 1
            for k in i.items:
                j = LineItem.get(Key(encoded=k))
                our_total += j.total()
        return dict(sales_today=our_count, sales_today_total=our_total, date_requested=date_requested)

class UserPages(webapp.RequestHandler):
    def index(self, **kwargs):
        self.redirect("/admin/user")

    
    @tg_template("add_user.html")
    @admin_only
    def add(self, **kwargs):
        return {}
    
    
    @tg_template("edit_user.html")
    @admin_only
    def edit(self, **kwargs):
        try:
            u = User.get(Key(encoded=self.request.get('key')))
            return dict(user=u)
        except:
            self.redirect("/admin/user")
    
    
    @admin_only
    def do_edit(self, **kwargs):
        try:
            u = User.get(Key(encoded=self.request.get('key')))
            email = urllib.unquote_plus(self.request.get('email'))
            first_name = urllib.unquote_plus(self.request.get('first_name'))
            last_name = urllib.unquote_plus(self.request.get('last_name'))
            password = urllib.unquote_plus(self.request.get('password'))
            is_admin = urllib.unquote_plus(self.request.get('is_admin'))
            is_developer = urllib.unquote_plus(self.request.get('is_developer'))
            u.email = email
            u.first_name = first_name
            u.last_name = last_name
            if is_admin == "True":
                u.is_admin = True
            else:
                u.is_admin = False
            if is_developer == "True":
                u.is_developer = True
            else:
                u.is_developer = False
            if password != "****":
                h = hashlib.sha512()
                u.salt = email
                h.update(password)
                h.update(email)
                u.password=h.hexdigest()
            u.put()
        except:
            pass
        self.redirect("/admin/user")        
    @admin_only
    def do_add(self, **kwargs):
        email = urllib.unquote_plus(self.request.get('email'))
        first_name = urllib.unquote_plus(self.request.get('first_name'))
        last_name = urllib.unquote_plus(self.request.get('last_name'))
        password = urllib.unquote_plus(self.request.get('password'))
        is_admin = urllib.unquote_plus(self.request.get('is_admin'))
        is_developer = urllib.unquote_plus(self.request.get('is_developer'))
        u = User()
        u.salt = email
        u.email = email
        u.first_name = first_name
        u.last_name = last_name
        if is_admin == "True":
            u.is_admin = True
        else:
            u.is_admin = False
        if is_developer == "True":
            u.is_developer = True
        else:
            u.is_developer = False
        h = hashlib.sha512()
        h.update(password)
        h.update(email)
        u.password=h.hexdigest()
        u.put()
        self.redirect("/admin/user")

class UserAPI(webapp.RequestHandler):
    
    @jsonify
    @admin_only
    def delete(self, **kwargs):
        try:
            #c = User.get(Key(encoded=self.request.get('key')))
            #c.delete()
            #return dict(valid=True)
            raise "UnsupportedFeature"
        except:
            return dict(valid=False, failure=traceback.format_exc())

class ColorAPI(webapp.RequestHandler):
    
    @jsonify
    @admin_only
    def delete(self, **kwargs):
        try:
            c = ColorCode.get(Key(encoded=self.request.get('key')))
            c.delete()
            return dict(valid=True)
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    @jsonify
    @admin_only
    def new_blank(self, **kwargs):
        c = ColorCode()
        c.put()
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)scolor" /></td><td><input type="text" id="%(key)sdiscount" />%%</td><td><input type="text" id="%(key)scode" /></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key())})
    
    @jsonify
    @admin_only
    def toggle_display(self, **kwargs):
        try:
            c = ColorCode.get(Key(encoded=self.request.get('key')))
            c.display = not c.display
            c.put()
            return dict(valid=True, html="""<tr id="%(key)s"><td>%(color)s</td><td>%(discount)s%%</td><td>%(code)s</td><td>%(display)s</td><td><a onclick="delete_color('%(key)s');" class="delete_button">X</a></td><td><a onclick="edit_row('%(key)s');" class="edit_button">edit</a></td><td><a onclick="toggle_display('%(key)s');" class="edit_button">Toggle Displayed</a></td></tr>""" % {'key': str(c.key()), 'discount': str(c.discount), 'color': str(c.color), 'code': str(c.code), 'display': str(c.display)})
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    @jsonify
    @admin_only
    def update(self, **kwargs):
        try:
            c = ColorCode.get(Key(encoded=self.request.get('key')))
            c.discount = int(urllib.unquote_plus(self.request.get('discount')))
            c.color = urllib.unquote_plus(self.request.get('color'))
            c.code = urllib.unquote_plus(self.request.get('code'))
            c.put()
            return dict(valid=True, html="""<tr id="%(key)s"><td>%(color)s</td><td>%(discount)s%%</td><td>%(code)s</td><td>%(display)s</td><td><a onclick="delete_color('%(key)s');" class="delete_button">X</a></td><td><a onclick="edit_row('%(key)s');" class="edit_button">edit</a></td><td><a onclick="toggle_display('%(key)s');" class="edit_button">Toggle Displayed</a></td></tr>""" % {'key': str(c.key()), 'discount': str(c.discount), 'color': str(c.color), 'code': str(c.code)})
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    
    @jsonify
    @admin_only
    def edit(self, **kwargs):
        c = ColorCode.get(Key(encoded=self.request.get('key')))
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)scolor" value="%(color)s"/></td><td><input type="text" id="%(key)sdiscount" value="%(discount)s"/>%%</td><td><input type="text" id="%(key)scode" value="%(code)s"/></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key()), 'discount': str(c.discount), 'color': str(c.color), 'code': str(c.code)})

class CategoryAPI(webapp.RequestHandler):
    
    @jsonify
    @admin_only
    def delete(self, **kwargs):
        try:
            c = ItemCategory.get(Key(encoded=self.request.get('key')))
            c.delete()
            return dict(valid=True)
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    @jsonify
    @admin_only
    def new_blank(self, **kwargs):
        c = ItemCategory()
        c.put()
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)sdescription" /></td><td>$<input type="text" id="%(key)sprice" /></td><td><input type="text" id="%(key)scode" /></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key())})
    
    
    @jsonify
    @admin_only
    def toggle_display(self, **kwargs):
        try:
            c = ItemCategory.get(Key(encoded=self.request.get('key')))
            c.display = not c.display
            c.put()
            return dict(valid=True, html="""<tr id="%(key)s"><td>%(description)s</td><td>$%(price)s</td><td>%(code)s</td><td>%(display)s</td><td><a onclick="delete_category('%(key)s');" class="delete_button">X</a></td><td><a onclick="edit_row('%(key)s');" class="edit_button">edit</a></td><td><a onclick="toggle_display('%(key)s');" class="edit_button">Toggle Displayed</a></td></tr>""" % {'key': str(c.key()), 'price': str(c.price), 'description': str(c.description), 'code': str(c.code), 'display': str(c.display)})
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    @jsonify
    @admin_only
    def update(self, **kwargs):
        try:
            c = ItemCategory.get(Key(encoded=self.request.get('key')))
            c.price = str_to_money(urllib.unquote_plus(self.request.get('price')))
            c.description = urllib.unquote_plus(self.request.get('description'))
            c.code = urllib.unquote_plus(self.request.get('code'))
            c.put()
            return dict(valid=True, html="""<tr id="%(key)s"><td>%(description)s</td><td>$%(price)s</td><td>%(code)s</td><td>%(display)s</td><td><a onclick="delete_category('%(key)s');" class="delete_button">X</a></td><td><a onclick="edit_row('%(key)s');" class="edit_button">edit</a></td><td><a onclick="toggle_display('%(key)s');" class="edit_button">Toggle Displayed</a></td></tr>""" % {'key': str(c.key()), 'price': str(c.price), 'description': str(c.description), 'code': str(c.code)})
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    
    @jsonify
    @admin_only
    def edit(self, **kwargs):
        c = ItemCategory.get(Key(encoded=self.request.get('key')))
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)sdescription" value="%(description)s"/></td><td>$<input type="text" id="%(key)sprice" value="%(price)s"/></td><td><input type="text" id="%(key)scode" value="%(code)s"/></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key()), 'price': str(money_to_str(c.price)), 'description': str(c.description), 'code': str(c.code)})