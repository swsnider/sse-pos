import os
DEBUG = ('SERVER_SOFTWARE' not in os.environ) or (os.environ['SERVER_SOFTWARE'].lower().startswith("development/"))
APPS = None
if DEBUG:
  APPS = dict(
    pos = 'http://localhost:8080',
    static = 'http://localhost:8081',
    donations = 'http://localhost:8082',
    inventory = 'http://localhost:8083',
    mapreducer = 'http://localhost:8084',
    admin = 'http://localhost:8085',
  )
else:
  APPS = dict(
    pos = 'http://pos.sse-pos.appspot.com',
    static = 'http://static.sse-pos.appspot.com',
    donations = 'http://donations.sse-pos.appspot.com',
    inventory = 'http://inventory.sse-pos.appspot.com',
    mapreducer = 'http://mapreducer.sse-pos.appspot.com',
    admin = 'http://admin.sse-pos.appspot.com',
  )
SESSION_OPTS = {
  'session.type': 'ext:google',
  'session.cookie_expires': True,
  'session.cookie_domain': '.sse-pos.appspot.com',
  # TODO: Change this value to use elsewhere.
  'session.secret': 'spO7sp6Us5I0ql1voe3Leroubrouxlu8riamieSlEciUpri227EHlE2IUb5aYie2',
  'session.auto': True
}
TAX_RATE = .07