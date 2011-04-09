from models import *
import datetime
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

def timezone_process(entity):
    if entity.created_on.year >= 2011 and entity.created_on.month >= 3 and entity.created_on.day >= 13:
        entity.created_on = entity.created_on - datetime.timedelta(hours=1)
        yield op.db.Put(entity)