'''
Created on Oct 1, 2014

@author: labcontenuti
'''
import sys
sys.path.insert(0,'.')
sys.path.insert(0,'..')
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
from voiceid.utils import humanize_time
import logging

if __name__ == '__main__':
    db = GMMVoiceDB('/var/spool/active/jobprocessor/audio/db/gmm_db')
    #print "adding"
    #db.add_model('/Users/labcontenuti/Desktop/voiceid/adaltavoce/voci/PinoLoperfidoCap2MobyDick.wav', 'PinoLoperfido')
    #print "added"
    #v = Voiceid(db, '../Test_set_all/GianniVattimoPostmodernit-Lyotard.mp3')
    #v = Voiceid(db, '../Test_set_all/Monica-Bellucci-interview.mp3')
    #v = Voiceid(db, '../Test_set_all/Pasolini1971.mp3')
    #v = Voiceid(db, '/home/felix/Desktop/u/facciamoiconti.mp3')
    #v = Voiceid(db, '/home/felix/Desktop/u/facciamoiconti/S32.wav')
    
    
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/voci/FabrizioGifuni-promessisposi-p1.wav')
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/Piero_Baldini##mobyDick01_1sec.wav')
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/Piero_Baldini##mobyDick01_3sec.wav')
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Giacomo_Mameli/2/Giacomo_Mameli##1-1.wav')
    v = Voiceid(db, '/var/spool/active/jobprocessor/audio/audio_test/2sec.wav')
        
    v.extract_speakers()
    
    for c in v.get_clusters():
        #print "c ", c   
        cluster = v.get_cluster(c) 
        """
        print "cluster.get_name ", cluster.get_name()        
        print "cluster.get_best_speaker ", cluster.get_best_speaker()
        print "cluster.get_duration ", cluster.get_duration()
        print "cluster.to_dict ", cluster.to_dict()
        print "cluster.get_segments ", cluster.get_segments()
        cluster.print_segments()
        #cluster.print_segments()
        """
        print "cluster.wave ", cluster.wave
        print "cluster.get_name ", cluster.get_name()
        print "\n\n\n\n\n\n"
        list_seg=cluster.get_segments()
        for seg in list_seg:
            print "start %s stop %s" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
            print "speaker ", cluster.get_best_speaker()
            print "get_basename ",seg.get_basename()
            print "\n\n"
        print
     
    print "RND"