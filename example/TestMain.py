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
    '''
            fml=FaceModels()
            #fml.set_dbname("Dataset AT&T")    
            #fml.create()
            
            resource_path=ACTIVE_ROOT_DIRECTORY+"data"+os.sep+"test_image.pgm"
            fe=FaceExtractor(fml)
            
            handle=fe.extract_faces_from_image_sync(resource_path)
            print handle

            print fe.getResults(handle)
    '''
    fml=FaceModels()
    image_test_dir=Constants.ACTIVE_ROOT_DIRECTORY +'data'+os.sep+'datatest'+os.sep+'Dataset AT&T TEST'
    fe=FaceExtractor(fml)
    numero_test=0
    test_ok=0
    test_falliti=0
    print fml._labels
    
    for dirname, dirnames, filenames in os.walk(image_test_dir):
        print '\n\n\n...'
        #print dirname, dirnames, filenames
        for fl in filenames: 
            handle=fe.extract_faces_from_image_sync(dirname+os.sep+fl)
            #print "risultato atteso ", dirname.split(os.sep)[-1], "risultato ottenuto ", fe.getResults(handle)['faces'][0]['tag']
            print dirname
            print fe.getResults(handle)
            numero_test=numero_test+1
            try:
                if dirname.split(os.sep)[-1]==fe.getResults(handle)['faces'][0]['tag']:
                    test_ok=test_ok+1
                else:
                    test_falliti=test_falliti+1
            except: 
                    test_falliti=test_falliti+1
    print "RISULTATO FINALE : test_ok ", test_ok, '  test falliti ', test_falliti