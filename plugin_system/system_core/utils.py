
from ConfigParser import ConfigParser
import os
import glob


def load_configuration(path):
    
    config = {}    
    conf_files = glob.glob(path+"/*.ini")
    for file in conf_files:               	
        parser = ConfigParser()                     
        parser.read(file)
        config = dict(parser._sections)
        for k in config:
            config[k] = dict(parser._defaults, **config[k])
            config[k].pop('__name__', None)
            		
	return config

