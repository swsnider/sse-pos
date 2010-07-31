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
    def volume(self, **kwargs):
        start_date = self.request.get('start_date', '')
        end_date = self.request.get('end_date', '')
        if start_date == '' or end_date == '':
            oneDay = timedelta(days=1)
            now = datetime.now()
            if int(now.hour) < 5:
                start_date = (date.today() - oneDay).strftime('%m/%d/%Y')
                end_date = date.today().strftime('%m/%d/%Y')
            else:
                start_date = date.today().strftime('%m/%d/%Y')
                end_date = (date.today() + oneDay).strftime('%m/%d/%Y')
        volume = []
        volumeDict = {}
        if start_date != '' and end_date != '':
            e = datetime.strptime(end_date, '%m/%d/%Y')
            s = datetime.strptime(start_date, '%m/%d/%Y')
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
        return dict(volume=volume, start_date=start_date, end_date=end_date)

    @tg_template('tax.html')
    @admin_only
    def tax(self, **kwargs):
        start_date = self.request.get('start_date', '')
        end_date = self.request.get('end_date', '')
        if start_date == '' or end_date == '':
            oneDay = timedelta(days=1)
            now = datetime.now()
            if int(now.hour) < 5:
                start_date = (date.today() - oneDay).strftime('%m/%d/%Y')
                end_date = date.today().strftime('%m/%d/%Y')
            else:
                start_date = date.today().strftime('%m/%d/%Y')
                end_date = (date.today() + oneDay).strftime('%m/%d/%Y')
        owed = 0
        taxable = 0
        total = 0
        calculated_items = []
        categorized = {}
        if start_date != '' and end_date != '':
            e = datetime.strptime(end_date, '%m/%d/%Y')
            s = datetime.strptime(start_date, '%m/%d/%Y')
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
            cats = sorted(categorized.items(), key=lambda x:x[1], reverse=True)
            categorized_labels = '|'.join([urllib.quote_plus(str(i[0])) for i in cats])
            categorized_data = ','.join([urllib.quote_plus(str(i[1])) for i in cats])
        return dict(cats=cats,categorized_labels=categorized_labels, categorized_data=categorized_data, start_date=start_date, end_date=end_date, owed_amount=owed, items=calculated_items, conv=money_to_str, total=total, taxable=taxable, categorized=categorized)
