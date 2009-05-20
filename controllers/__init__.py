import cgi, os
from google.appengine.api import users
from google.appengine.ext import webapp
from util import render_template, secure, tg_template


class MainPage(webapp.RequestHandler):
    @tg_template("main.html")
    def get(self, **kwargs):
        return {}