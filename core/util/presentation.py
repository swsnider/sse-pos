import bottle
from StringIO import StringIO
import csv
import datetime
import os
import re
import simplejson as json
import urllib

def jsonify(f):
    def g(*args, **kwargs):
        return json.dumps(f(*args, **kwargs))
    return g

def csvify(f):
    def g(*args, **kwargs):
        result = f(*args, **kwargs)
        bottle.response.headers['Content-Type'] = "text/csv"
        bottle.response.headers['Content-Disposition'] = 'attachment;filename="users.csv"'
        output = StringIO()
        ourWriter = csv.DictWriter(output, result[0].keys())
        for i in result:
            ourWriter.writerow(i)
        return output.getvalue()
    return g

def str_to_money(amt):
    if '.' not in amt: amt += "00"
    amt = amt.replace(",", "")
    amt = amt.replace(".", "")
    amt = int(amt)
    return amt

def money_to_str(amt):
    temp = "%.2f" % (amt / 100.0)
    profile = re.compile(r"(\d)(\d\d\d[.,])")
    while 1:
        temp, count = re.subn(profile,r"\1,\2",temp)
        if not count: break
    return temp

# def report(f):
#     def g(*args, **kwargs):
#         self = args[0]
#         start_date = self.request.get('start_date', '')
#         end_date = self.request.get('end_date', '')
#         if start_date == '' or end_date == '':
#             oneDay = datetime.timedelta(days=1)
#             now = datetime.datetime.now()
#             if int(now.hour) < 5:
#                 start_date = (datetime.date.today() - oneDay).strftime('%m/%d/%Y')
#                 end_date = datetime.date.today().strftime('%m/%d/%Y')
#             else:
#                 start_date = datetime.date.today().strftime('%m/%d/%Y')
#                 end_date = (datetime.date.today() + oneDay).strftime('%m/%d/%Y')
#         e = s = None
#         if start_date != '' and end_date != '':
#             e = datetime.datetime.strptime(end_date, '%m/%d/%Y')
#             s = datetime.datetime.strptime(start_date, '%m/%d/%Y')
#         kwargs['e'] = e
#         kwargs['s'] = s
#         r = f(*args, **kwargs)
#         r['start_date'] = start_date
#         r['end_date'] = end_date
#         return r
#     return g
# 
# def pie_chart(f):
#     def g(*args, **kwargs):
#         self = args[0]
#         r = f(*args, **kwargs)
#         if 'categorized' in r:
#             ###Single case
#             categorized = r['categorized']
#             cats = sorted(categorized.items(), key=lambda x:x[1], reverse=True)
#             categorized_labels = '|'.join([urllib.quote_plus(str(i[0])) for i in cats])
#             categorized_data = ','.join([urllib.quote_plus(str(i[1])) for i in cats])
#         elif 'categorized_list' in r:
#             ###Multiple case
#             categorized_list = r['categorized_list']
#             cats = {}
#             categorized_labels = {}
#             categorized_data = {}
#             for k in categorized_list.keys():
#                 categorized = categorized_list[k]
#                 c = sorted(categorized.items(), key=lambda x:x[1], reverse=True)
#                 c_l = '|'.join([urllib.quote_plus(str(i[0])) for i in c])
#                 c_d = ','.join([urllib.quote_plus(str(i[1])) for i in c])
#                 cats[k] = c
#                 categorized_labels[k] = c_l
#                 categorized_data[k] = c_d
#         r['cats'] = cats
#         r['categorized_labels'] = categorized_labels
#         r['categorized_data'] = categorized_data
#         return r
#     return g