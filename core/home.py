from global_defs import *

_libs = ['beaker', 'bottle.py', 'jinja2', 'pytz']
import os
import os.path
import sys
# sys.path.extend([os.path.join(os.getcwd(), 'lib', i) for i in _libs])
sys.path.append(os.path.join(os.getcwd(), 'lib'))

sys.stderr.write('[SYSPATH] ' + repr(sys.path) + '\n')

from beaker.middleware import SessionMiddleware
import bottle
import controllers


def main():
  app = bottle.app()
  app = SessionMiddleware(app, SESSION_OPTS)
  bottle.run(app=app, server='gae')


if __name__ == '__main__':
  main()