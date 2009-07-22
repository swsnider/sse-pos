from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from models import models
from util import api_only
import simplejson as json

class SyncAPI(webapp.RequestHandler):
    @jsonify
    @api_only
    def create(self, **kwargs):
        model = models[str(self.request.get('model'))]
        my_row = model()
        my_row.put()
        return {"__key__":str(my_row.key())}
    
    @jsonify
    @api_only
    def read(self, **kwargs):
        model = models[str(self.request.get('model'))]
        row = str(self.request.get('key'))
        my_row = model.get(Key(encoded=row))
        props = model.properties().keys()
        d = {}
        for i in props:
            d[i] = getattr(my_row, i)
        d['__key__'] = row
        return d
        
    @jsonify
    @api_only
    def update(self, **kwargs):
        model = models[str(self.request.get('model'))]
        row = str(self.request.get('key'))
        my_row = model.get(Key(encoded=row))
        mods = json.loads(self.request.get('mods'))
        for i in mods:
            setattr(my_row, i['prop'], i['value'])
        my_row.put()
        props = model.properties().keys()
        d = {}
        for i in props:
            d[i] = getattr(my_row, i)
        d['__key__'] = row
        return d
        
    #included for completeness only -- should not be used!
    @api_only
    def delete(self, **kwargs):
        model = models[str(self.request.get('model'))]
        row = str(self.request.get('key'))
        my_row = model.get(Key(encoded=row))
        my_row.delete()
        return {}