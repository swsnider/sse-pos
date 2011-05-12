import os
DEBUG = ('SERVER_SOFTWARE' not in os.environ) or (os.environ['SERVER_SOFTWARE'].lower().startswith("development/"))
if DEBUG:
  cookie_domain = 'sse-pos.com'
else:
  cookie_domain = '.sse-pos.appspot.com'
SESSION_OPTS = {
  'session.type': 'ext:google',
  'session.cookie_expires': True,
  'session.cookie_domain': cookie_domain,
  # TODO: Change this value to use elsewhere.
  'session.secret': 'spO7sp6Us5I0ql1voe3Leroubrouxlu8riamieSlEciUpri227EHlE2IUb5aYie2',
  'session.auto': True
}
TAX_RATE = .07
del cookie_domain