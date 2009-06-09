from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

class TransactionExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Transaction',
                                 [('owner', str, None),
                                  ('items', repr, None),
                                  ('created_on', str, None),
                                 ])

class LineItemExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'LineItem',
                                  [('color', str, None),
                                   ('quantity', str, None),
                                   ('category', str, None),
                                  ])

class UserExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'User',
                                [('email', str, None),
                                 ('salt', str, None),
                                 ('first_name', str, None),
                                 ('last_name', str, None),
                                 ('is_admin', str, None),
                                 ('is_developer', str, None),
                                 ('password', str, None),
                                ])

exporters = [TransactionExporter]