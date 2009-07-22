from google.appengine.ext.db import Key
from google.appengine.api import urlfetch
from models import *
import simplejson as json

class SyncProxy(object):
    def __init__(self, host, secret):
        self.host = host
        self.secret = secret
    
    def sync(self):
        

    def create(self, model):
        payload = {'secret': self.secret,
                    'model': model}
        result = urlfetch.fetch(url=self.host+"/sync/create", payload=payload, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if result.status_code == 200:
            return json.loads(result.content)

    def read(self, model, key):
        payload = {'secret': self.secret,
                    'model': model,
                    'key': key}
        result = urlfetch.fetch(url=self.host+"/sync/read", payload=payload, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if result.status_code == 200:
            return json.loads(result.content)

    def update(self, model, key, mods):
        payload = {'secret': self.secret,
                    'model': model,
                    'key': key,
                    'mods': json.dumps(mods)}
        result = urlfetch.fetch(url=self.host+"/sync/create", payload=payload, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if result.status_code == 200:
            return json.loads(result.content)

    #included for completeness only -- should not be used!
    def delete(self, model, key):
        payload = {'secret': self.secret,
                    'model': model,
                    'key': key}
        result = urlfetch.fetch(url=self.host+"/sync/delete", payload=payload, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if result.status_code == 200:
            return json.loads(result.content)