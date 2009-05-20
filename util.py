from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
from google.appengine.api import users
import gdata.calendar, gdata.calendar.service

def render_template(name, template_values):
    template_dirs = []
    template_dirs.append(os.path.join(os.path.dirname(__file__), 'templates'))
    env = Environment(loader = FileSystemLoader(template_dirs))
    try:
        template = env.get_template(name)
    except TemplateNotFound:
        raise TemplateNotFound(name)
    return template.render(template_values)

def secure(f):
    def g(*args, **kwargs):
        if users.get_current_user():
            return f(*args, **kwargs)
        else:
            args[0].redirect("/login")
    return g

def tg_template(name):
    def h(f):
        def g(*args, **kwargs):
            args[0].response.out.write(render_template(name, f(*args, **kwargs)))
        return g
    return h