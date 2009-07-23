from auth_layer import uses_users
from models import Setting
import random

__all__ = ['secure', 'admin_only', 'developer_only']

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