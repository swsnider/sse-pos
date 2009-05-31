from models import *
from google.appengine.ext import webapp
from util import secure, tg_template

class TransactionPage(webapp.RequestHandler):
    @secure
    @tg_template("transaction.html")
    def get(self, **kwargs):
        return {}