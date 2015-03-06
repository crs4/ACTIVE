from abc import abstractmethod
import sys
import os
from utils import load_configuration
 
class PluginMount(type):																
    def __init__(cls, name, bases, attrs):	    										
        if not hasattr(cls, 'plugins'):													
            # This branch only executes when processing the mount point itself.			
            # So, since this is a new plugin type, not an implementation, this			
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = {} #[]
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            # cls.plugins.append(cls)
	    print name
	    print bases
	    print attrs
            cls.plugins[attrs['__module__']] = cls

    def get_plugin(cls, id):
	if id in cls.plugins:
		return cls.plugins[id]
	return None

    def get_plugins(cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins.values()]


class ActionProvider:
    __metaclass__ = PluginMount
    
	# each plugin has his own path automatically set when its object is created. 
	#~ Then the path is used to load the config files of the plugin that is stored in a dictionary (self.info)
	#~ es. self.info = {'INFOPlug1': {'author': 'ale', 'title': 'insert'}}
    def __init__(self,*args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.path = os.path.dirname(sys.modules[self.__module__].__file__)
        self.configuration = load_configuration(self.path)
    
        
    @abstractmethod
    def perform(self, args=None):
	pass        
