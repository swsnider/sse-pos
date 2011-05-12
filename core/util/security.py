import bottle

def secure(f):
  def g(*args, **kwargs):
    session = bottle.request.environ.get('beaker.session')
    if 'current_user' not in session:
      bottle.redirect('/login')
    return f(*args, **kwargs)
  return g

def is_authenticated():
  session = bottle.request.environ.get('beaker.session')
  return 'current_user' in session