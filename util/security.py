from auth_layer import uses_users
from models import Setting
import random

__all__ = ['secure', 'admin_only', 'developer_only', 'api_only']

def secure(f):
    @uses_users
    def g(*args, **kwargs):
        if args[0].users.get_current_user() != None:
            return f(*args, **kwargs)
        else:
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

alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def api_only(f):
    def g(*args, **kwargs):
        connection_secret = Setting.filter('name =', 'connection_secret').get()
        if not connection_secret:
            connection_secret = Setting()
            secret = "".join([random.choice(alphas) for i in range(32)])
            connection_secret.name = 'connection_secret'
            connection_secret.set_at = secret
            connection_secret.put()
        connection_secret = connection_secret.set_at
        my_sec = self.request.get('secret', "")
        if my_sec == connection_secret:
            return f(*args, **kwargs)
        else:
            self.response.error(403)
            return