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
from tools.face_extractor import FaceExtractor
import shutil
from tools.Constants import ACTIVE_ROOT_DIRECTORY
from tools.Constants import ACTIVE_ROOT_DIRECTORY

if __name__ == '__main__':
    
            fml=FaceModels()
            #fml.set_dbname("Dataset AT&T")    
            #fml.create()
            for file in os.listdir(ACTIVE_ROOT_DIRECTORY+"data"+os.sep+"testsimple"):
                fe=FaceExtractor(fml)
            
                handle=fe.extract_faces_from_image_sync(ACTIVE_ROOT_DIRECTORY+"data"+os.sep+"testsimple"+os.sep+file)
                print "image ", file, ' result ', fe.getResults(handle)
                print "\n\n"