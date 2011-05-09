import sys
import unittest2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed
import models
import util

class TestModel(db.Model):
  a_field = db.StringProperty()
  number = db.IntegerProperty()
  USEFUL_FIELDS = ('a_field', 'number')

class CommonTestCase(unittest2.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def testModelToDict(self):
    instance = TestModel()
    instance.a_field = 'some string'
    instance.number = 42
    instance.put()
    result = util.model_to_dict(instance, TestModel)
    self.assertEqual(len(result.keys()), 3)
    self.assertEqual(result['a_field'], 'some string')
    self.assertEqual(result['number'], 42)

  def testGetLists(self):
    item = models.Item()
    item.name = 'test1'
    item.price = 1
    item.code = 't1'
    item.stati = ['visible']
    item.put()
    item = models.Item()
    item.name = 'test2'
    item.price = 2
    item.code = 't2'
    item.stati = ['visible']
    item.put()
    color = models.Color()
    color.name = 'test3'
    color.discount = 0
    color.code = 't3'
    color.stati = ['visible']
    color.put()
    color = models.Color()
    color.name = 'test4'
    color.discount = 0
    color.code = 't4'
    color.stati = []
    color.put()
    result = util.get_lists('Item', 'Color')
    self.assertEqual(len(result), 2)
    self.assertEqual(len(result[0]), 2)
    self.assertEqual(len(result[1]), 1)