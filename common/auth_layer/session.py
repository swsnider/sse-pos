import base64
from models import Visit
from google.appengine.ext.db import Key

def uses_session(f):
    def g(*args, **kwargs):
        self = args[0]
        invalid_cookie = False
        self.request.charset = None
        if 'sse_pos_session_key' not in self.request.cookies:
            curr_session = Visit(expired=False, session='{}')
            curr_session.expired=False
            curr_session.session = '{}'
            curr_session.put()
            invalid_cookie = True
        else:
            curr_session = Visit.get(Key(encoded=str(self.request.cookies['sse_pos_session_key'])))
            if not curr_session or curr_session.expired:
                curr_session = Visit(expired=False, session='{}')
                curr_session.expired=False
                curr_session.session = '{}'
                curr_session.put()
                invalid_cookie=True
        sess = eval(curr_session.session)
        self.session = sess
        self.real_session = curr_session
        ret_val = f(*args, **kwargs)
        curr_session.session = repr(sess)
        curr_session.put()
        if invalid_cookie:
            self.response.headers['Set-Cookie'] = 'sse_pos_session_key=%s; expires=Thu, 22-May-2014 17:36:31 GMT; Path=/; Domain=.sse-pos.appspot.com' % str(curr_session.key())
        return ret_val
    return g