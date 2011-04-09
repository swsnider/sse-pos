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

def transaction_process(entity):
    new_its = []
    for it in entity.items:
        i = LineItem.get(Key(encoded=it))
        new_i = LineItem2()
        new_i.quantity = i.quantity
        new_i.set_color(i.color)
        new_i.set_category(i.category)
        if i.misc_amount is not None:
            new_i.price = i.misc_amount
        else:
            new_i.price = i.category.price
        yield op.db.Put(entity)
        new_its.append(new_i.key())
    new_trans = Transaction2()
    new_trans.created_on = entity.created_on
    new_trans.owner = entity.owner
    new_trans.items = new_its
    new_trans.finalized = False
    new_trans.total_and_cert()
    new_trans.daily_stats_collected = False
    yield op.db.Put(new_trans)
    new_trans.created_on = entity.created_on
    yield op.db.Put(new_trans)