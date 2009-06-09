import os, csv, simplejson as json
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

__all__ = ['render_template', 'tg_template', 'jsonify', 'csvify']

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
