import datetime
from google.appengine.ext.db import Property

class ESTTZDateTimeProperty(Property):
  """The base class of all of our date/time properties.

  We handle common operations, like converting between time tuples and
  datetime instances.
  """

  def __init__(self, verbose_name=None, auto_now=False, auto_now_add=False,
               **kwds):
    """Construct a DateTimeProperty

    Args:
      verbose_name: Verbose name is always first parameter.
      auto_now: Date/time property is updated with the current time every time
        it is saved to the datastore.  Useful for properties that want to track
        the modification time of an instance.
      auto_now_add: Date/time is set to the when its instance is created.
        Useful for properties that record the creation time of an entity.
      timezone: Specify the timezone to use.
    """
    super(ESTTZDateTimeProperty, self).__init__(verbose_name, **kwds)
    self.auto_now = auto_now
    self.auto_now_add = auto_now_add

  def validate(self, value):
    """Validate datetime.

    Returns:
      A valid value.

    Raises:
      BadValueError if property is not instance of 'datetime'.
    """
    value = super(ESTTZDateTimeProperty, self).validate(value)
    if value and not isinstance(value, self.data_type):
      raise BadValueError('Property %s must be a %s' %
                          (self.name, self.data_type.__name__))
    return value

  def default_value(self):
    """Default value for datetime.

    Returns:
      value of now() as appropriate to the date-time instance if auto_now
      or auto_now_add is set, else user configured default value implementation.
    """
    if self.auto_now or self.auto_now_add:
      return self.now()
    return Property.default_value(self)

  def get_value_for_datastore(self, model_instance):
    """Get value from property to send to datastore.

    Returns:
      now() as appropriate to the date-time instance in the odd case where
      auto_now is set to True, else the default implementation.
    """
    if self.auto_now:
      return self.now()
    else:
      return super(ESTTZDateTimeProperty,
                   self).get_value_for_datastore(model_instance)

  data_type = datetime.datetime
  offset = datetime.timedelta(hours=5)

  @staticmethod
  def now():
    """Get now as a full datetime value.

    Returns:
      'now' as a whole timestamp, including both time and date.
    """
    return (datetime.datetime.now() - ESTTZDateTimeProperty.offset)