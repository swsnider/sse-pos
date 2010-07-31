import traceback, urllib, hashlib, time
import gviz_api
from models import *
from util import *
import code
import urllib
from datetime import datetime, date, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.db import Key

class DataPage(webapp.RequestHandler):
    @admin_only
    def default(self, **kwargs):
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
        tq = urllib.unquote_plus(self.request.get('tq', ''))
        tqx = urllib.unquote_plus(self.request.get('tqx', ''))
        columns = {
            "date": ("date", "Date"),
            "volume": ("number", "Number Sold")
        }
        e = datetime.strptime(end_date, '%m/%d/%Y')
        s = datetime.strptime(start_date, '%m/%d/%Y')
        ts = Transaction2.gql("WHERE created_on >= :1 AND created_on <= :2", s, e)
        tdata = {}
        for t in ts:
            if t.created_on.hour < 5 and t.created_on.day == s.day and t.created_on.month == s.month and t.created_on.year == s.year: continue
            if t.created_on.hour < 5:
                d = t.created_on - oneDay
            else:
                d = t.created_on
            d = d.replace(hour=0,second=0,microsecond=0,minute=0)
            if d not in tdata:
                tdata[d] = 0
            tdata[d] += len(t.items)
        data = [{'date': i[0], 'volume': i[1]} for i in tdata.items()]
        data_table = gviz_api.DataTable(columns)
        data_table.LoadData(data)
        self.response.out.write(data_table.ToResponse(columns_order=['date','volume'], tqx=tqx))
        return