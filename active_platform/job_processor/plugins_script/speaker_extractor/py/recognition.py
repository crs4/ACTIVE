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
import pickle
import shelve
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
from voiceid.utils import humanize_time
import logging
DB_PATH='/Users/labcontenuti/.voiceid/gmm_db'
find_ok=[]
find_errata=[]
not_find=[]
unknown_ok=[]
unknown_errata=[]
PID=None
MODEL=None
FILE_PATH=None
DIR_PATH=None
OK=0
import time

if __name__ == '__main__':
    
    from optparse import OptionParser
    usage = "usage: %prog [options] model_filename"    
    parser = OptionParser(usage=usage)
    parser.add_option('-p',"--database_voice_path", action="store", dest="DB_PATH",type="string")
    parser.add_option("-i", "--person_id", action="store", dest="PID", type="string")
    parser.add_option("-m", "--model_path", action="store", dest="MODEL", type="string")
    parser.add_option("-s", "--score", action="store", dest="SCORE", type="float", default=0.5)
    parser.add_option("-f", "--file_path", action="store", dest="FILE_PATH", type="string", default=None)
    parser.add_option("-d", "--dir_path", action="store", dest="DIR_PATH", type="string", default=None)
    parser.add_option("-x", "--shelve_db", action="store", dest="SHELVE_DB", type="string", default=False)
    #parser.print_help()
    (options, args) = parser.parse_args()
    print "options " 
    if options.DB_PATH:
        DB_PATH=options.DB_PATH
    print "Using DB_PATH ", DB_PATH
    
    if options.PID:
        PID=options.DB_PATH
    else:
        print "[Error] No PID was given."
        #exit()
    print "PID ", PID
    
    if options.MODEL:
        MODEL=options.MODEL
        print "MODEL ", MODEL

    
    if options.FILE_PATH:
        FILE_PATH=options.FILE_PATH
        print "FILE_PATH ", FILE_PATH
    
    if options.DIR_PATH:
        DIR_PATH=options.DIR_PATH
        print "DIR_PATH ", DIR_PATH

    if options.SCORE:
        SCORE=float(options.SCORE)
        print "SCORE ", SCORE
    
    if options.SHELVE_DB:
        SHELVE_DB=options.SHELVE_DB
        print "SHELVE_DB ", SHELVE_DB
    
    
    db = GMMVoiceDB(DB_PATH)
    v = Voiceid(db, FILE_PATH)
    #v.extract_speakers()
    try:
        v.extract_speakers_without_diarization()
        print "Only  speacker extraction"
    except:
         print "diarization and  speacker extraction"
         v.extract_speakers()
    output = open(FILE_PATH+'.pkl', 'wb')
    dic_pkl={}
    for c in v.get_clusters():
                cluster = v.get_cluster(c)
                dic_pkl[cluster._label]=cluster
    print "dic_pkl=", dic_pkl 
    pickle.dump(dic_pkl, output,-1)
    output.close()
    save_as=""
    handle=FILE_PATH+str(time.asctime().replace(' ','_'))
            
    if True:
            print "=============SHELVE================"
            sdb= shelve.open(FILE_PATH+"_shelve")
            tmp_sdb={}
            """
            db = GMMVoiceDB(DB_PATH)
            v = Voiceid(db, FILE_PATH)            
            v.extract_speakers()
            """
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                print "", cluster._label, " cluster.get_best_five()[0][0]=", cluster.get_best_five()[0][0], "  cluster.get_distance()=", cluster.get_distance(), " cluster.get_distance()>SCORE", cluster.get_distance()<SCORE
                speaker="Unknown" 
                if cluster.get_distance()>SCORE:
                    speaker=cluster.get_best_five()[0][0]
                sp0=cluster.get_best_five()[0][0]
                sp1=cluster.get_best_five()[0][1]
                if sp0.startswith(sp1[0:-1]) or sp1.startswith(sp0[0:-1]): 
                    speaker=cluster.get_best_five()[0][0] 
                list_seg=cluster.get_segments()
                for seg in list_seg:
                    tmp_sdb[seg.get_start()]=[str(speaker),str( humanize_time( (float(seg.get_end())-float(seg.get_start())) / 100) ),str( humanize_time(float(seg.get_end()) / 100) ), str( humanize_time(float(seg.get_start()) / 100) )]
            tmp_sdb_keys=tmp_sdb.keys()
            tmp_sdb_keys.sort()
            for k in tmp_sdb_keys:
                sdb[str(k)]=tmp_sdb[k]
                sdb.sync()
                print " start = ", str(k), " data=", sdb[str(k)]
            sdb.close()
    print "RND"