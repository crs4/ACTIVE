from django.db import models

class Event(models.Model):
    """
    This class is used to provide an object representation to
    Event objects providing all necessary data. An event is used
    as an entity which is triggered when something happens.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400, default='N/A')

    def save(self, *args, **kwargs):
	"""
	Override the save method in order to create uniform names.
	"""
	self.name = self.name.replace(' ', '').upper()
	super(Event, self).save(*args, **kwargs)
        
    def set_views(self,*args):
        self.view_set = [ self.view_set.create(path_abs = a) for a in args] 
    
    def __repr__(self):
        return self.name

    def __unicode__(self):
	return self.name


class Action(models.Model):
    """
    This class is used to provide an object representation to
    Views objects providing all necessary data. A Action object
    is the entity which trigger one or more Event objects.
    In this case it is a function that is called and executed correctely.
    Moreover a Action could trigger ONLY one Event.
    """
    path_abs = models.CharField(max_length=300)
    event = models.ForeignKey(Event)
   
    def __repr__(self):
        return self.path_abs

    def __unicode__(self):
        return self.path_abs



class Plugin(models.Model):
    """
    This class is used to provide an object representation to
    Plugin objects providing all necessary data. A Plugin is
    defined as a set of scripts objects and it embed their common information.
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    active_version = models.CharField(max_length=10)
    plugin_version = models.CharField(max_length=10)
    url_info = models.CharField(max_length = 300)
    #required_plugins = advanced(Expert required)
    authors = models.CharField(max_length = 100)

    def __repr__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Script(models.Model):
    """
    This class is used to provide an object representation to
    Script objects providing all necessary data. A Script is 
    a reference to a function saved inside a module, this reference
    will be used to invoke that function when needed.
    """
    details = models.CharField(max_length=300) 
    path = models.CharField(max_length=100, unique=True)
    job_name = models.CharField(max_length=100)
    plugin = models.ForeignKey(Plugin)
    events = models.ManyToManyField(Event)
    item_type = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return self.details

    def __repr__(self):
        return self.title
