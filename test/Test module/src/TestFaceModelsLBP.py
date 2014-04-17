
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
from tools.FaceModelsLBP import FaceModelsLBP
import shutil


class TestFaceModelsLBP(unittest.TestCase):
    
    def test_init(self):
        fml=FaceModelsLBP()
        self.assertEqual(Constants.DB_PATH, fml._dbpath, "OK PATH DB")
        

    def test_create(self):
            
            fml=FaceModelsLBP()
            #fml.set_dbname("Dataset AT&T")    
            fml.create()
            self.assertTrue( os.path.isfile(fml._db_name+"-LBP"))
    
    def test_removetag(self):
             fml=FaceModelsLBP()
             shutil.copytree(fml._dbpath+"/s1", fml._dbpath+"/s1bis")   
             fml.remove_tags(["s1bis"])
             self.assertFalse(os.path.isfile(fml._dbpath+"/s1bis"))
    def test_addfaces(self):
             fml=FaceModelsLBP()
             fml.add_faces("", "tagdiprova")
             self.assertTrue(os.path.exists(fml._dbpath+"/tagdiprova"))
    
    def test_readimages2(self):
            fml=FaceModelsLBP()
            fml.read_images("../data/DATASET AT&T", None)
            self.assertTrue(len(fml._labels.keys()) )
if __name__ == '__main__':
    unittest.main()
    
    
    