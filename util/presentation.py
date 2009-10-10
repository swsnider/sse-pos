import os, csv, simplejson as json, datetime as datetime_module
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