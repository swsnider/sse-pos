import traceback, urllib, hashlib, time
from models import *
from util import *
import code
import urllib
from datetime import datetime, date, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.db import Key

TAXABLE_CATEGORIES = ['jw', 'pu', 'ac', 'sa', 'prom', 'LB']
TAX_RATE = 0.07

class ReportPages(webapp.RequestHandler):
    @tg_template('report.html')
    @admin_only
    def index(self, **kwargs):
        return dict()

    @tg_template('volume.html')
    @admin_only
    @report
    def volume(self, **kwargs):
        e = kwargs['e']
        s = kwargs['s']
        volume = []
        volumeDict = {}
        if e != None and s != None:
            ts = Transaction2.gql("WHERE created_on >= :1 AND created_on <= :2", s, e)
            for t in ts:
                if t.created_on.hour < 5:
                    d = (t.created_on - oneDay)
                    d = "new Date(%s, %s, %s)" % (d.year, d.month-1, d.day)
                else:
                    d = t.created_on
                    d = "new Date(%s, %s, %s)" % (d.year, d.month-1, d.day)
                if d not in volumeDict:
                    volumeDict[d] = 0
                volumeDict[d] += len(t.items)
        volume = [(i[0], i[1]) for i in volumeDict.items()]
        return dict(volume=volume)

    @tg_template('tax.html')
    @admin_only
    @pie_chart
    @report
    def tax(self, **kwargs):
        e = kwargs['e']
        s = kwargs['s']
        owed = 0
        taxable = 0
        total = 0
        calculated_items = []
        categorized = {}
        if e != None and s != None:
            ts = Transaction2.gql("WHERE created_on >= :1 AND created_on <= :2", s, e)
            calculated_items = []
            for transaction in ts:
                if transaction.items is None or len(transaction.items) == 0:
                    continue
                for i in transaction.items:
                    it = LineItem2.get(Key(encoded=i))
                    this_total = it.total()
                    total += this_total
                    if it.category_code in TAXABLE_CATEGORIES:
                        taxable += this_total
                        calculated_items.append(it)
                    categorized[it.category] = categorized.get(it.category, 0) + 1
            owed = taxable * 0.07
        return dict(owed_amount=owed, items=calculated_items, conv=money_to_str, total=total, taxable=taxable, categorized=categorized)
    

    @tg_template('report_tag_colors.html')
    @admin_only
    @pie_chart
    @report
    def tag_color(self, **kwargs):
        e = kwargs['e']
        s = kwargs['s']
        if e != None:
            ts = Transaction2.gql("WHERE created_on >= :1 AND created_on <= :2", s, e)
            categorized = {}
            ocategorized = {}
            colorDict = {}
            discountDict = {}
            for t in ts:
                if t.items is None: continue
                volumeDict[d] += len(t.items)
                d_d = {}
                c_d = {}
                for i in t.items:
                    it = LineItem2.get(Key(encoded=i))
                    categorized[str(it.discount) + "%"] = categorized.get(str(it.discount) + "%", 0) + 1
                    ocategorized[str(it.color)] = ocategorized.get(str(it.color), 0) + 1
                    if t.created_on.hour < 5:
                        d = (t.created_on - oneDay)
                        d = "new Date(%s, %s, %s)" % (d.year, d.month-1, d.day)
                    else:
                        d = t.created_on
                        d = "new Date(%s, %s, %s)" % (d.year, d.month-1, d.day)
                    if d not in colorDict:
                        colorDict[d] = {}
                    if d not in discountDict:
                        discountDict[d] = {}
                    d_d[str(it.discount) + "%"] = d_d.get(str(it.discount) + "%", 0) + 1
                    c_d[str(it.color)] = c_d.get(str(it.color), 0) + 1
                
        return dict(conv=money_to_str, categorized_list = dict(categorized=categorized, ocategorized=ocategorized), colorDict=colorDict, discountDict=discountDict)