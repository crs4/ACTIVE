from pluginmanager.plugin_mount_point import ActionProvider

class Delete(ActionProvider):


    def perform(self, args=None):
        print(self.configuration)	

                        
