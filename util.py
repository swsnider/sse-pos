from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import simplejson as json
from auth_layer import uses_users

def render_template(name, template_values):
    template_dirs = []
    template_dirs.append(os.path.join(os.path.dirname(__file__), 'templates'))
    env = Environment(loader = FileSystemLoader(template_dirs))
    try:
        template = env.get_template(name)
    except TemplateNotFound:
        raise TemplateNotFound(name)
    if not template_values:
        template_values = {}
    return template.render(template_values)

def secure(f):
    @uses_users
    def g(*args, **kwargs):
        if args[0].users.get_current_user() != None:
            return f(*args, **kwargs)
        else:
            args[0].redirected = True
            args[0].redirect("/login")
    return g

def admin_only(f):
    @uses_users
    def g(*args, **kwargs):
        current_user = args[0].users.get_current_user()
        if current_user != None and current_user.is_admin:
            return f(*args, **kwargs)
        else:
            args[0].redirect("/denied")
    return g

def developer_only(f):
    @uses_users
    def g(*args, **kwargs):
        current_user = args[0].users.get_current_user()
        if current_user != None and current_user.is_developer:
            return f(*args, **kwargs)
        else:
            args[0].redirect("/denied")
    return g

def tg_template(name):
    def h(f):
        def g(*args, **kwargs):
            retval = f(*args, **kwargs)
            args[0].response.out.write(render_template(name, retval))
        return g
    return h

def jsonify(f):
    def g(*args, **kwargs):
        self = args[0]
        retval = f(*args, **kwargs)
        #if type(retval) == type(dict()):
        #    for i in retval.keys():
        #        if i.startswith('__sse_pos'):
        #            del retval[i]
        self.response.out.write(json.dumps(retval))
    return g