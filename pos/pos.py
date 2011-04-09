from global_defs import *
import bottle
import controllers


class StripPathMiddleware(object):
  def __init__(self, app):
    self.app = app
  def __call__(self, e, h):
    e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
    return self.app(e,h)


def main():
  app = bottle.app()
  app = StripPathMiddleware(app)
  bottle.run(app=app, server='gae')


if __name__ == '__main__':
  main()