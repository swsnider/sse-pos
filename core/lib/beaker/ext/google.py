import cPickle
import logging
from datetime import datetime

from beaker.container import OpenResourceNamespaceManager, Container
from beaker.exceptions import InvalidCacheBackendError
from beaker.synchronization import null_synchronizer

log = logging.getLogger(__name__)

db = None
namespace_manager = None

class GoogleNamespaceManager(OpenResourceNamespaceManager):
    tables = {}

    @classmethod
    def _init_dependencies(cls):
        global db
        global namespace_manager
        if db is not None:
            return
        try:
            db = __import__('google.appengine.ext.db').appengine.ext.db
            namespace_manager = __import__('google.appengine.api.namespace_manager').appengine.api.namespace_manager
        except ImportError:
            raise InvalidCacheBackendError("Datastore cache backend requires the "
                                           "'google.appengine.ext' library")
    
    def __init__(self, namespace, table_name='beaker_cache', **params):
        """Creates a datastore namespace manager"""
        OpenResourceNamespaceManager.__init__(self, namespace)
        curr_namespace = namespace_manager.get_namespace()
        namespace_manager.set_namespace('-global-')
        
        def make_cache():
            table_dict = dict(created=db.DateTimeProperty(),
                              accessed=db.DateTimeProperty(),
                              data=db.BlobProperty())
            table = type(table_name, (db.Model,), table_dict)
            return table
        self.table_name = table_name
        self.cache = GoogleNamespaceManager.tables.setdefault(table_name, make_cache())
        self.hash = {}
        self._is_new = False
        self.loaded = False
        self.log_debug = logging.DEBUG >= log.getEffectiveLevel()
        
        # Google wants namespaces to start with letters, change the namespace
        # to start with a letter
        self.namespace = 'p%s' % self.namespace
        namespace_manager.set_namespace(curr_namespace)
    
    def get_access_lock(self):
        return null_synchronizer()

    def get_creation_lock(self, key):
        # this is weird, should probably be present
        return null_synchronizer()

    def do_open(self, flags):
        curr_namespace = namespace_manager.get_namespace()
        namespace_manager.set_namespace('-global-')
        # If we already loaded the data, don't bother loading it again
        if self.loaded:
            self.flags = flags
            return
        
        item = self.cache.get_by_key_name(self.namespace)
        
        if not item:
            self._is_new = True
            self.hash = {}
        else:
            self._is_new = False
            try:
                self.hash = cPickle.loads(str(item.data))
            except (IOError, OSError, EOFError, cPickle.PickleError):
                if self.log_debug:
                    log.debug("Couln't load pickle data, creating new storage")
                self.hash = {}
                self._is_new = True
        self.flags = flags
        self.loaded = True
        namespace_manager.set_namespace(curr_namespace)
    
    def do_close(self):
        curr_namespace = namespace_manager.get_namespace()
        namespace_manager.set_namespace('-global-')
        if self.flags is not None and (self.flags == 'c' or self.flags == 'w'):
            if self._is_new:
                item = self.cache(key_name=self.namespace)
                item.data = cPickle.dumps(self.hash)
                item.created = datetime.now()
                item.accessed = datetime.now()
                item.put()
                self._is_new = False
            else:
                item = self.cache.get_by_key_name(self.namespace)
                item.data = cPickle.dumps(self.hash)
                item.accessed = datetime.now()
                item.put()
        self.flags = None
        namespace_manager.set_namespace(curr_namespace)
    
    def do_remove(self):
        curr_namespace = namespace_manager.get_namespace()
        namespace_manager.set_namespace('-global-')
        item = self.cache.get_by_key_name(self.namespace)
        item.delete()
        self.hash = {}
        
        # We can retain the fact that we did a load attempt, but since the
        # file is gone this will be a new namespace should it be saved.
        self._is_new = True
        namespace_manager.set_namespace(curr_namespace)

    def __getitem__(self, key):
        return self.hash[key]

    def __contains__(self, key): 
        return self.hash.has_key(key)
        
    def __setitem__(self, key, value):
        self.hash[key] = value

    def __delitem__(self, key):
        del self.hash[key]

    def keys(self):
        return self.hash.keys()
        

class GoogleContainer(Container):
    namespace_class = GoogleNamespaceManager
