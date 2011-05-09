from global_defs import *
from beaker.middleware import SessionMiddleware
import bottle
import controllers


def main():
  app = bottle.app()
  app = SessionMiddleware(app, SESSION_OPTS)
  bottle.run(app=app, server='gae')


if __name__ == '__main__':
  main()