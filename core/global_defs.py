import os
import os.path
import sys
_lib_path = os.path.join(os.getcwd(), 'lib')
if sys.path[0] != _lib_path:
  sys.path.insert(0, _lib_path)
del _lib_path
DEBUG = ('SERVER_SOFTWARE' not in os.environ) or (os.environ['SERVER_SOFTWARE'].lower().startswith("development/"))
if DEBUG:
  sys.stderr.write('\n\n#%s#\n\n' % repr(sys.path))
SESSION_OPTS = {
  'session.type': 'ext:google',
  'session.cookie_expires': True,
  # TODO: Change this value to use elsewhere.
  'session.secret': 'spO7sp6Us5I0ql1voe3Leroubrouxlu8riamieSlEciUpri227EHlE2IUb5aYie2',
  'session.auto': True
}
if DEBUG:
  STATIC_PREFIX = 'http://localhost:8081/'
else:
  STATIC_PREFIX = 'http://static.snider-cashregister.appspot.com/'
TAX_RATE = .07
GLOBAL_NAMESPACE = '-global-'
VIEW_DIR='new_views'