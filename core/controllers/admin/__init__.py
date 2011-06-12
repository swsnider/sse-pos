import util
from util import view


def std_admin_wrapper(*view_args, **view_kwargs):
  def h(wrapped):
    @util.secure
    @util.has_stati('admin')
    @util.user_namespace
    def g(*args, **kwargs):
      if (len(view_args) + len(view_kwargs)) > 0:
        f = view(*view_args, **view_kwargs)(wrapped)
      else:
        f = wrapped
      return f(*args, **kwargs)
    return g
  return h


import item
import color
import user
