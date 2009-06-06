from models import *
from datetime import datetime, date
import traceback, urllib, hashlib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import admin_only, developer_only, secure, tg_template, jsonify

class AdminPages(webapp.RequestHandler):
    @admin_only
    @tg_template('admin.html')
    def index(self, **kwargs):
        return {}
    
    @admin_only
    @tg_template('category_list.html')
    def category(self, **kwargs):
        return dict(categories=ItemCategory.all().fetch(1000))
    @admin_only
    @tg_template('color_list.html')
    def color(self, **kwargs):
        return dict(colors=ColorCode.all().fetch(1000))
    
    @admin_only
    @tg_template('unimplemented.html')
    def reports(self, **kwargs):
        return dict(return_url="/admin")
    
    @admin_only
    @tg_template('user_list.html')
    def user(self, **kwargs):
        return dict(users=User.all().fetch(1000))
    
    @admin_only
    @tg_template('stats.html')
    def stats(self, **kwargs):
        ts = Transaction.all().filter('created_on >=', date.today()).fetch(1000)
        our_total = 0
        our_count = 0
        for i in ts:
            if i.items is None or len(i.items) == 0:
                continue
            our_count += 1
            for k in i.items:
                j = LineItem.get(Key(encoded=k))
                our_total += j.total()
        return dict(sales_today=our_count, sales_today_total=our_total)
    
    @developer_only
    @tg_template('eval.html')
    def eval(self, **kwargs):
        return {}
    
    @developer_only
    @jsonify
    def do_eval(self, **kwargs):
        code = urllib.unquote_plus(self.request.get('code'))
        return {'evalResult': eval(code), 'errors': traceback.format_exc()}

class UserPages(webapp.RequestHandler):
    def index(self, **kwargs):
        self.redirect("/admin/user")

    @admin_only
    @tg_template("add_user.html")
    def add(self, **kwargs):
        return {}
    
    @admin_only
    @tg_template("edit_user.html")
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
    @admin_only
    @jsonify
    def delete(self, **kwargs):
        try:
            c = User.get(Key(encoded=self.request.get('key')))
            c.delete()
            return dict(valid=True)
        except:
            return dict(valid=False, failure=traceback.format_exc())

class ColorAPI(webapp.RequestHandler):
    @admin_only
    @jsonify
    def delete(self, **kwargs):
        try:
            c = ColorCode.get(Key(encoded=self.request.get('key')))
            c.delete()
            return dict(valid=True)
        except:
            return dict(valid=False, failure=traceback.format_exc())
    @admin_only
    @jsonify
    def new_blank(self, **kwargs):
        c = ColorCode()
        c.put()
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)scolor" /></td><td><input type="text" id="%(key)sdiscount" />%%</td><td><input type="text" id="%(key)scode" /></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key())})
    
    @admin_only
    @jsonify
    def update(self, **kwargs):
        try:
            c = ColorCode.get(Key(encoded=self.request.get('key')))
            c.discount = int(urllib.unquote_plus(self.request.get('discount')))
            c.color = urllib.unquote_plus(self.request.get('color'))
            c.code = urllib.unquote_plus(self.request.get('code'))
            c.put()
            return dict(valid=True, html="""<tr id="%(key)s"><td>%(color)s</td><td>%(discount)s%%</td><td>%(code)s</td><td><a onclick="delete_color('%(key)s');" style="color: red;">X</a></td><td><a onclick="edit_row('%(key)s');" style="color: green;">edit</a></td></tr>""" % {'key': str(c.key()), 'discount': str(c.discount), 'color': str(c.color), 'code': str(c.code)})
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    @admin_only
    @jsonify
    def edit(self, **kwargs):
        c = ColorCode.get(Key(encoded=self.request.get('key')))
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)scolor" value="%(color)s"/></td><td><input type="text" id="%(key)sdiscount" value="%(discount)s"/>%%</td><td><input type="text" id="%(key)scode" value="%(code)s"/></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key()), 'discount': str(c.discount), 'color': str(c.color), 'code': str(c.code)})

class CategoryAPI(webapp.RequestHandler):
    @admin_only
    @jsonify
    def delete(self, **kwargs):
        try:
            c = ItemCategory.get(Key(encoded=self.request.get('key')))
            c.delete()
            return dict(valid=True)
        except:
            return dict(valid=False, failure=traceback.format_exc())
    @admin_only
    @jsonify
    def new_blank(self, **kwargs):
        c = ItemCategory()
        c.put()
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)sdescription" /></td><td>$<input type="text" id="%(key)sprice" /></td><td><input type="text" id="%(key)scode" /></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key())})
    
    @admin_only
    @jsonify
    def update(self, **kwargs):
        try:
            c = ItemCategory.get(Key(encoded=self.request.get('key')))
            c.price = int(urllib.unquote_plus(self.request.get('price')))
            c.description = urllib.unquote_plus(self.request.get('description'))
            c.code = urllib.unquote_plus(self.request.get('code'))
            c.put()
            return dict(valid=True, html="""<tr id="%(key)s"><td>%(description)s</td><td>$%(price)s</td><td>%(code)s</td><td><a onclick="delete_category('%(key)s');" style="color: red;">X</a></td><td><a onclick="edit_row('%(key)s');" style="color: green;">edit</a></td></tr>""" % {'key': str(c.key()), 'price': str(c.price), 'description': str(c.description), 'code': str(c.code)})
        except:
            return dict(valid=False, failure=traceback.format_exc())
    
    @admin_only
    @jsonify
    def edit(self, **kwargs):
        c = ItemCategory.get(Key(encoded=self.request.get('key')))
        return dict(valid=True, html="""<tr id="%(key)srow"><td><input type="text" id="%(key)sdescription" value="%(description)s"/></td><td>$<input type="text" id="%(key)sprice" value="%(price)s"/></td><td><input type="text" id="%(key)scode" value="%(code)s"/></td><td><button onclick="commit_row('%(key)s');">Commit</button></td></tr>""" % {"key": str(c.key()), 'price': str(c.price), 'description': str(c.description), 'code': str(c.code)})