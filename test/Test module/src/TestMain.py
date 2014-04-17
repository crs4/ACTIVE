'''
Created on Apr 16, 2014

@author: labcontenuti
'''

import cv2
import os
import sys
import numpy as np
import unittest
import sys
from random import shuffle
import shutil
sys.path.append("../../..")
from tools import Constants
from tools.toolsAPI import FaceModels
from tools.toolsAPI import FaceExtractor

import shutil

if __name__ == '__main__':
            fml=FaceModels()
            #fml.set_dbname("Dataset AT&T")    
            fml.create()
            resource_path=""
            fe=FaceExtractor(fml)
            handle=fe.extractFacesFromImage(resource_path)
            progress = 0
            while progress < 100:
                progress = fe.getProgress(handle)
            print fe.getResults(handle)