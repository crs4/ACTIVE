'''
Created on Nov 4, 2014

@author: labcontenuti
'''
import sys
sys.path.insert(0,'.')
sys.path.insert(0,'..')
import unittest
from audioToolsAPI import VoiceExtractor

class Test(unittest.TestCase):


    def test_AudioToolApi_extractVoicesFromAudio(self):
        vc=VoiceExtractor()
        vc.extractVoicesFromAudio('/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Giacomo_Mameli/Giacomo_Mameli##1-1.wav')

    def test_AudioToolApi_extractVoicesFromAudio_gmm(self):
        vc=VoiceExtractor("/Users/labcontenuti/.voiceid/gmm_db/M/GiacomoMameli.gmm")
        vc.extractVoicesFromAudio('/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Giacomo_Mameli/Giacomo_Mameli##1-1.wav')


if __name__ == "__main__":
    #import sys;sys.argv = ['','Test.AudioToolApi_extractVoicesFromAudio_gmm', 'Test.AudioToolApi_extractVoicesFromAudio']
    unittest.main()
