# All Rights Reserved. Use is subject to license terms. 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
    
    file_path='/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/BBBangelina.mp3'
    with open(file_path.split(".")[0]+'.properties', "w") as f:
        with open('/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/config.properties') as fp:
            for line in fp:
                    f.write(line)
    f.write("fileName="+file_path.split(".")[0]+".wav")
    f.write("outputRoot="+file_path.split(".")[0]+"/out/")
    f.flush()
    f.close()
    
    exit()
    
    f=open('/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/AAAangelina.properties', "w")
    with open('/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/angelina.properties') as fp:
        for line in fp:
            print line
            f.write(line)
    f.close()
    print "finitooo"
    exit()
    
    
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
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/Piero_Baldini##mobyDick01_1sec.wav')
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/Piero_Baldini##mobyDick01_3sec.wav')
    #v = Voiceid(db, '/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Giacomo_Mameli/2/Giacomo_Mameli##1-1.wav')
    v = Voiceid(db, '/Users/labcontenuti/Documents/workspace/activevoice/audio_test/2sec.wav')
        
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