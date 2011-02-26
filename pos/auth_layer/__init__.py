from models import Visit, User
import hashlib
from google.appengine.ext.db import Key
from session import uses_session

def uses_users(f):
    @uses_session
    def g(*args, **kwargs):
        self = args[0]
        self.users = users(self.session)
        retval = f(*args, **kwargs)
        return retval
    return g

class users:
    def __init__(self, session):
        self.session = session
    def logout(self):
        if 'curr_user_key' in self.session:
            self.session.clear()
    def get_current_user(self):
        if 'curr_user_key' in self.session:
            return User.get(Key(encoded=str(self.session['curr_user_key'])))
        return None
    def login(self, email, passwd):
        if 'curr_user_key' in self.session:
            self.logout()
        h = hashlib.sha512()
        h.update(passwd)
        user = User.all().filter('email =', email).get()
        if not user:
            return False
        h.update(user.salt)
        real = h.hexdigest()
        if real == user.password:
            self.session['curr_user_key'] = str(user.key())
            return True
        else:
            return False