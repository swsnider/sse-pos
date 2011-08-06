from global_defs import *
import os.path

from beaker.middleware import SessionMiddleware
import bottle
if DEBUG:
  from paste.evalexception import EvalException

import controllers


def main():
  bottle.TEMPLATE_PATH.insert(0, os.path.join(os.path.abspath(
      os.path.dirname(__file__)), VIEW_DIR))
  app = bottle.app()
  app.catchall = False
  app = SessionMiddleware(app, SESSION_OPTS)
  if DEBUG:
    app = EvalException(app)
  bottle.run(app=app, server='gae')


if __name__ == '__main__':
  main()