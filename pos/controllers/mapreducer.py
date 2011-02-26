from models import *
from datetime import datetime
import traceback, urllib
from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from util import secure, tg_template, jsonify, str_to_money, money_to_str
from mapreduce import operation as op

def is_superuser_process(entity):
    if entity.email in ('swsnider@gmail.com', 'esmukisa@yahoo.com', 'emily.m.faith@gmail.com'):
      entity.is_superuser = True
    else:
      entity.is_superuser = False
    yield op.db.Put(entity)

def disabled_process(entity):
    entity.disabled = not entity.display
    yield op.db.Put(entity)