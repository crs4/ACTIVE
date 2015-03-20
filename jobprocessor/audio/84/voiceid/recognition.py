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
        SCORE=options.SCORE
        print "SCORE ", SCORE
    
    if options.SHELVE_DB:
        SHELVE_DB=options.SHELVE_DB
        print "SHELVE_DB ", SHELVE_DB
    
    
    db = GMMVoiceDB(DB_PATH)
    v = Voiceid(db, FILE_PATH)
    v.extract_speakers()
    
    output = open(FILE_PATH+'.pkl', 'wb')
    for c in v.get_clusters():
                cluster = v.get_cluster(c)
                pickle.dump(v.get_cluster(c), output,-1)
    output.close()
    save_as="yuml,srt"
    handle=FILE_PATH+str(time.asctime().replace(' ','_'))
    if save_as.find("xml")>-1:
            result_file=""
            """
            db = GMMVoiceDB(DB_PATH)
            v = Voiceid(db, FILE_PATH)            
            v.extract_speakers()
            """
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                speaker="Unknown" 
                if cluster.get_distance()<SCORE:
                    speaker=cluster.get_best_five()[0][0]
                result_file=result_file+"\n<cluster><speacker>"+str(speaker)+"</speacker>"
                print "cluster.get_best_five()=",cluster.get_best_five()
                print "cluster.get_distance()=",cluster.get_distance()
                list_seg=cluster.get_segments()
                for seg in list_seg:
                    print "start %s stop %s" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    result_file=result_file+"<start> %s </start><stop> %s </stop>" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                result_file=result_file+"</cluster>"
            file = open(handle+".txt", "w")
            file.write(result_file)
            file.close()
            
    if save_as.find("srt")>-1:
            index=1
            result_file="\n"
            """
            db = GMMVoiceDB(DB_PATH)
            v = Voiceid(db, FILE_PATH)            
            v.extract_speakers()
            """
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                speaker="Unknown" 
                if cluster.get_distance()<SCORE:
                    speaker=cluster.get_best_five()[0][0]
                list_seg=cluster.get_segments()
                for seg in list_seg:
                    result_file=result_file+str(index)+"\n"
                    index=index+1
                    print "%s --> %s\n" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    result_file=result_file+"%s --> %s" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    result_file=result_file+"\n<i>"+str(speaker)+"</i>\n"
                
            file = open(handle+".srt", "w")
            file.write(result_file)
            file.close()
    if save_as.find("yuml")>-1:
            index=1
            result_file="\n"
            """
            db = GMMVoiceDB(DB_PATH)
            v = Voiceid(db, FILE_PATH)            
            v.extract_speakers()
            """
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                speaker="Unknown" 
                if cluster.get_distance()<SCORE:
                    speaker=cluster.get_best_five()[0][0]
                list_seg=cluster.get_segments()
                for seg in list_seg:
                    #result_file=result_file+str(index)+"\n"
                    #index=index+1
                    result_file=result_file+ " - ann_tag: "+str(speaker) +"\n"
                    result_file=result_file+ "   segment_duration: "+str( humanize_time( (float(seg.get_end())-float(seg.get_start())) / 100) ) +"\n"
                    result_file=result_file+ "   segment_end: "+str( humanize_time(float(seg.get_end()) / 100) ) +"\n"
                    result_file=result_file+ "   segment_start: "+str( humanize_time(float(seg.get_start()) / 100) ) +"\n"
                    print result_file
                    
                    #print "%s --> %s\n" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    #result_file=result_file+"%s --> %s" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    #result_file=result_file+"\n<i>"+str(speaker)+"</i>\n"
    if save_as=="po":
            index=1
            result_file="\n"
            """
            db = GMMVoiceDB(DB_PATH)
            v = Voiceid(db, FILE_PATH)            
            v.extract_speakers()
            """
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                speaker="Unknown" 
                if cluster.get_distance()<SCORE:
                    speaker=cluster.get_best_five()[0][0]
                list_seg=cluster.get_segments()
                for seg in list_seg:
                    #result_file=result_file+str(index)+"\n"
                    #index=index+1
                    result_file=result_file+ " - ann_tag: "+str(speaker) +"\n"
                    result_file=result_file+ "   segment_duration: "+str( humanize_time( (float(seg.get_end())-float(seg.get_start())) / 100) ) +"\n"
                    result_file=result_file+ "   segment_end: "+str( humanize_time(float(seg.get_end()) / 100) ) +"\n"
                    result_file=result_file+ "   segment_start: "+str( humanize_time(float(seg.get_start()) / 100) ) +"\n"
                    print result_file
                    
                    #print "%s --> %s\n" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    #result_file=result_file+"%s --> %s" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    #result_file=result_file+"\n<i>"+str(speaker)+"</i>\n"                
            file = open(handle+".yuml", "w")
            file.write(result_file)
            file.close()
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
                speaker="Unknown" 
                if cluster.get_distance()<SCORE:
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