from models import *
from datetime import datetime
import traceback, urllib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import secure, tg_template, jsonify, str_to_money, money_to_str

class MapReducePage(webapp.RequestHandler):
    def index(self, **kwargs):
        pass