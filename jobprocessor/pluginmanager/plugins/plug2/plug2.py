from pluginmanager.plugin_mount_point import ActionProvider

class Insert(ActionProvider):


    def perform(self, args=None):
        print(self.configuration)
        
