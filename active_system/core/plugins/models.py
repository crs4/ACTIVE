from django.db import models


class Event(models.Model):
    name = models.CharField(max_length = 100, unique = True)    

    def save(self, *args, **kwargs):
	self.name = self.name.replace(' ', '').upper()
	super(Event, self).save(*args, **kwargs)
        
    def set_views(self,*args):
        self.view_set = [ self.view_set.create(path_abs = a) for a in args] 
    
    def __repr__(self):
        return self.name

    def __unicode__(self):
	return self.name

class View(models.Model):
    path_abs = models.CharField(max_length = 300)
    event = models.ForeignKey(Event)
   
    def __repr__(self):
        return self.path_abs

    def __unicode__(self):
        return self.path_abs

class Plugin(models.Model):
    title = models.CharField(max_length = 100)
    path = models.CharField(max_length = 100, unique=True)
    description = models.CharField(max_length = 400)
    active_version = models.CharField(max_length = 10)
    plugin_version = models.CharField(max_length = 10)
    job_main = models.CharField(max_length = 100)
    url_info = models.CharField(max_length = 300)
    #required_plugins = advanced(Expert required)
    events = models.ManyToManyField(Event)
    authors = models.CharField(max_length = 100)

    def __repr__(self):
        return self.title

    def __unicode__(self):
        return self.title
