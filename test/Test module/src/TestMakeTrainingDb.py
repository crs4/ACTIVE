'''
Created on Apr 15, 2014

@author: labcontenuti
'''
import unittest
from tools.make_training_db import DBOrder

class Test(unittest.TestCase):


    def test1(self):
        dbo=DBOrder("../data/testimg", "../data/ordered")
        dbo._sep="_I_"
        dbo.sort()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()