from global_defs import *

import os
import os.path
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

from beaker.middleware import SessionMiddleware
import bottle
if DEBUG:
  from paste.evalexception import EvalException

import controllers


def main():
  app = bottle.app()
  app.catchall = False
  app = SessionMiddleware(app, SESSION_OPTS)
  if DEBUG:
    app = EvalException(app)
  bottle.run(app=app, server='gae')


if __name__ == '__main__':
  main()