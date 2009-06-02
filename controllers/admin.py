from models import *
import traceback, urllib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import admin_only, secure, tg_template, jsonify

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