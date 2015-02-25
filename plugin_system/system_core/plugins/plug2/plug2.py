from system_core.plugin_mount_point import ActionProvider

class Insert(ActionProvider):


    def perform(self):
        print(self.configuration)
        
