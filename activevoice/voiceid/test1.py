'''
Created on Oct 1, 2014

@author: labcontenuti
'''


from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB


if __name__ == '__main__':
    db = GMMVoiceDB('/Users/labcontenuti/.voiceid/gmm_db')
    #print "adding"
    #db.add_model('/Users/labcontenuti/Desktop/voiceid/adaltavoce/voci/PinoLoperfidoCap2MobyDick.wav', 'PinoLoperfido')
    #print "added"
    #v = Voiceid(db, '../Test_set_all/GianniVattimoPostmodernit-Lyotard.mp3')
    #v = Voiceid(db, '../Test_set_all/Monica-Bellucci-interview.mp3')
    #v = Voiceid(db, '../Test_set_all/Pasolini1971.mp3')
    #v = Voiceid(db, '/home/felix/Desktop/u/facciamoiconti.mp3')
    #v = Voiceid(db, '/home/felix/Desktop/u/facciamoiconti/S32.wav')
    
    
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/voci/FabrizioGifuni-promessisposi-p1.wav')
    v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/Piero_Baldini##mobyDick01_1sec.wav')
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/Piero_Baldini##mobyDick01_3sec.wav')
    
    v.extract_speakers()
    
    for c in v.get_clusters():
        cluster = v.get_cluster(c)
        print "cluster.get_name ", cluster.get_name()        
        print "cluster.get_best_speaker ", cluster.get_best_speaker()
        print "cluster.get_duration ", cluster.get_duration()
        print "cluster.to_dict ", cluster.to_dict()
        
        #cluster.print_segments()
        print
     
    print "RND"