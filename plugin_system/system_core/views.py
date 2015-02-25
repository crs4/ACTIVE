from django.shortcuts import render
from plugin_mount_point import ActionProvider
from plugins import *

# Create your views here.


from django.http import HttpResponse




def run_plugins(request):
    
    result= []
    actions = ActionProvider.get_plugins()
    

    for a in actions:
        a.perform()
        result.append(a.configuration)
  
  
    
 
    return HttpResponse(result)
    
