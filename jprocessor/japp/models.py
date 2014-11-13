from django.db import models

class Job(models.Model):
    
    created  = models.DateTimeField(auto_now_add=True)
    
    resource = models.CharField(max_length=256)
    
    data     = models.TextField(default = '')
    
    duration = models.FloatField(default = 0)
    
    class Meta:
        ordering = ('created',)
