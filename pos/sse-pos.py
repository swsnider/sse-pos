from routes.mapper import Mapper
from google.appengine.ext.webapp.util import run_wsgi_app
from wsgi import WSGIApplication
from controllers import *
import os


myMap = Mapper(explicit=True)
from routing import add_routes
add_routes(myMap)
debug = os.environ['SERVER_SOFTWARE'].lower().startswith("development/")
app = WSGIApplication(myMap, debug=debug)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()