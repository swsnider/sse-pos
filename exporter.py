from google.appengine.ext import db
from google.appengine.tools import bulkloader
import util
import models
User = models.User

def mysql_safe_repr(data):
    return repr(data).replace(',', ';')

def mysql_bool(data):
    if data:
        return '1'
    else:
        return '0'

class TransactionExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Transaction',
                                 [('__key__', str, 'None'),
                                  ('owner', str, 'None'),
                                  ('items', mysql_safe_repr, []),
                                  ('created_on', str, 'None'),
                                 ])
class Transaction2Exporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Transaction2',
                                  [('__key__', str, 'None'),
                                   ('owner', str, 'None'),
                                   ('items', mysql_safe_repr, []),
                                   ('created_on', str, 'None'),
                                   ('finalized', mysql_bool, False),
                                  ])

class LineItemExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'LineItem',
                                  [('__key__', str, 'None'),
                                   ('color', str, 'None'),
                                   ('quantity', str, 'None'),
                                   ('category', str, 'None'),
                                  ])

class LineItem2Exporter(bulkloader.Exporter):
  def __init__(self):
      bulkloader.Exporter.__init__(self, 'LineItem2',
                                [('__key__', str, 'None'),
                                 ('color', str, 'None'),
                                 ('quantity', str, 'None'),
                                 ('discount', str, 'None'),
                                 ('price', str, 'None'),
                                 ('color_code', str, 'None'),
                                 ('category_code', str, 'None'),
                                 ('category', str, 'None'),
                                ])

class UserExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'User',
                                [('__key__', str, 'None'),
                                 ('email', str, 'None'),
                                 ('salt', str, 'None'),
                                 ('first_name', str, 'None'),
                                 ('last_name', str, 'None'),
                                 ('is_admin', mysql_bool, False),
                                 ('is_developer', mysql_bool, False),
                                 ('password', str, 'None'),
                                ])

class ColorExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'ColorCode',
                                [('__key__', str, 'None'),
                                 ('discount', str, 'None'),
                                 ('color', str, 'None'),
                                 ('code', str, 'None'),
                                 ('display', mysql_bool, False),
                                ])

class CategoryExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'ItemCategory',
                                [('__key__', str, 'None'),
                                 ('price', str, 'None'),
                                 ('description', str, 'None'),
                                 ('code', str, 'None'),
                                 ('display', mysql_bool, False),
                                ])

exporters = [UserExporter, LineItemExporter, TransactionExporter, LineItem2Exporter, Transaction2Exporter, ColorExporter, CategoryExporter]