import os, csv, simplejson as json, datetime as datetime_module, urllib
from re import compile, subn
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

class eastern(datetime_module.tzinfo):
    """Implementation of the Eastern timezone."""
    def utcoffset(self, dt):
        return datetime_module.timedelta(hours=-5) + self.dst(dt)

    def _FirstSunday(self, dt):
        """First Sunday on or after dt."""
        return dt + datetime_module.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        # 2 am on the second Sunday in March
        dst_start = self._FirstSunday(datetime_module.datetime(dt.year, 3, 8, 2))
        # 1 am on the first Sunday in November
        dst_end = self._FirstSunday(datetime_module.datetime(dt.year, 11, 1, 1))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime_module.timedelta(hours=1)
        else:
            return datetime_module.timedelta(hours=0)

    def tzname(self, dt):
        if self.dst(dt) == datetime_module.timedelta(hours=0):
            return "EST"
        else:
            return "EDT"

def render_fragment(name, template_values):
    template_values['standalone'] = True
    return render_template(name, template_values)

def render_template(name, template_values):
    template_dirs = []
    template_dirs.append(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    env = Environment(loader = FileSystemLoader(template_dirs))
    try:
        template = env.get_template(name)
    except TemplateNotFound:
        raise TemplateNotFound(name)
    if not template_values:
        template_values = {}
        if 'standalone' not in template_values:
            template_values['standalone'] = False
    return template.render(template_values)

def tg_template(name):
    def h(f):
        def g(*args, **kwargs):
            args[0].response.out.write(render_template(name, f(*args, **kwargs)))
        return g
    return h

def jsonify(f):
    def g(*args, **kwargs):
        self = args[0]
        self.response.out.write(json.dumps(f(*args, **kwargs)))
    return g

def csvify(f):
    def g(*args, **kwargs):
        self = args[0]
        result = f(*args, **kwargs)
        self.response.headers['Content-Type'] = "text/csv"
        self.response.headers['Content-Disposition'] = 'attachment;filename="users.csv"'
        ourWriter = csv.DictWriter(self.response.out, result[0].keys())
        for i in result:
            ourWriter.writerow(i)
    return g

def str_to_money(amt):
    if '.' not in amt: amt += "00"
    amt = amt.replace(",", "")
    amt = amt.replace(".", "")
    amt = int(amt)
    return amt

def money_to_str(amt):
    temp = "%.2f" % (amt / 100.0)
    profile = compile(r"(\d)(\d\d\d[.,])")
    while 1:
        temp, count = subn(profile,r"\1,\2",temp)
        if not count: break
    return temp

def report(f):
    def g(*args, **kwargs):
        self = args[0]
        start_date = self.request.get('start_date', '')
        end_date = self.request.get('end_date', '')
        if start_date == '' or end_date == '':
            oneDay = datetime_module.timedelta(days=1)
            now = datetime_module.datetime.now()
            if int(now.hour) < 5:
                start_date = (datetime_module.date.today() - oneDay).strftime('%m/%d/%Y')
                end_date = datetime_module.date.today().strftime('%m/%d/%Y')
            else:
                start_date = datetime_module.date.today().strftime('%m/%d/%Y')
                end_date = (datetime_module.date.today() + oneDay).strftime('%m/%d/%Y')
        e = s = None
        if start_date != '' and end_date != '':
            e = datetime_module.datetime.strptime(end_date, '%m/%d/%Y')
            s = datetime_module.datetime.strptime(start_date, '%m/%d/%Y')
        kwargs['e'] = e
        kwargs['s'] = s
        r = f(*args, **kwargs)
        r['start_date'] = start_date
        r['end_date'] = end_date
        return r
    return g

def pie_chart(f):
    def g(*args, **kwargs):
        self = args[0]
        r = f(*args, **kwargs)
        if 'categorized' in r:
            ###Single case
            categorized = r['categorized']
            cats = sorted(categorized.items(), key=lambda x:x[1], reverse=True)
            categorized_labels = '|'.join([urllib.quote_plus(str(i[0])) for i in cats])
            categorized_data = ','.join([urllib.quote_plus(str(i[1])) for i in cats])
        elif 'categorized_list' in r:
            ###Multiple case
            categorized_list = r['categorized_list']
            cats = {}
            categorized_labels = {}
            categorized_data = {}
            for k in categorized_list.keys():
                categorized = categorized_list[k]
                c = sorted(categorized.items(), key=lambda x:x[1], reverse=True)
                c_l = '|'.join([urllib.quote_plus(str(i[0])) for i in c])
                c_d = ','.join([urllib.quote_plus(str(i[1])) for i in c])
                cats[k] = c
                categorized_labels[k] = c_l
                categorized_data[k] = c_d
        r['cats'] = cats
        r['categorized_labels'] = categorized_labels
        r['categorized_data'] = categorized_data
        return r
    return g