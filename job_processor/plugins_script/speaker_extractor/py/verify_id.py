'''
Created on Oct 1, 2014

@author: labcontenuti
'''


from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
from voiceid.utils import humanize_time
import fnmatch
import os
import logging

#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/adaltavoce/test/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/radio/TEST/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Paolo_Fadda/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Michele_Giannotta/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/youtube/Giovanni_Ghiselli/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Gianni_Locatelli/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/DataSetVideolinaVoci/Mario_Leoni/'


#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/VidTIMIT-Audio/TestSetWav/fa_dg0/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/VidTIMIT-Audio/TestSetWav/fa_ks0/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/VidTIMIT-Audio/TestSetWav/fc_ft0/'
#DIR_PATH='/Users/labcontenuti/Desktop/voiceid/VidTIMIT-Audio/TestSetWav/fc_mh0/'


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
def verify_speaker(wav_file, best_speaker):
    """ 
    Si presume che il file abbia un formato del tipo
    nome_cognome##altreinfo.wav
    """
    if wav_file.find("##")==-1:
        print "ERROR: MALFORMED WAV FILE ", wav_file
        return False
    ns=wav_file.split("##")[0]
    
    if best_speaker==ns.split("_")[0]+ns.split("_")[1]:
        return True
    else:
        return False

def verify_identity(pid,best_speaker):
    return pid==best_speaker

def verify_goodness(all_wav):
    """Verifica che i nomi dei file siano scritti secondo il formato  nome_cognome##altreinfo.wav"""
    for wav_file in all_wav:
        if wav_file.find("##")==-1:
            print "ERROR: MALFORMED WAV FILE ", wav_file
            return False             
        ns=wav_file.split("##")[0]
        if ns.split("_")==-1:
            print "ERROR: MALFORMED WAV FILE ", wav_file
            return False             
        return True
if __name__ == '__main__':
    
    from optparse import OptionParser
    usage = "usage: %prog [options] model_filename"    
    parser = OptionParser(usage=usage)
    parser.add_option('-p',"--database_voice_path", action="store", dest="DB_PATH",type="string")
    parser.add_option("-i", "--person_id", action="store", dest="PID", type="string")
    parser.add_option("-m", "--model_path", action="store", dest="MODEL", type="string")
    parser.add_option("-f", "--file_path", action="store", dest="FILE_PATH", type="string", default=None)
    parser.add_option("-d", "--dir_path", action="store", dest="DIR_PATH", type="string", default=None)
    
    #parser.print_help()
     
    (options, args) = parser.parse_args()
    print "options " 
    """
    print "args ", args
    if len(args) == 0:
        print "[Error] No model was given."
        exit()
    """    
        
    # This model will be used (or created if the training parameter (-t, --train) exists:
    if options.DB_PATH:
        DB_PATH=options.DB_PATH
    print "Using DB_PATH ", DB_PATH
    
    if options.PID:
        PID=options.DB_PATH
    else:
        print "[Error] No PID was given."
        exit()
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
        
   
    all_wav =[]
    if DIR_PATH:
        for f in os.listdir(DIR_PATH):
            if fnmatch.fnmatch(f, '*.wav') and f.find("##")>-1:
                all_wav.append(DIR_PATH+"/"+f)
    if FILE_PATH:
            if fnmatch.fnmatch(FILE_PATH, '*.wav') and FILE_PATH.find("##")>-1:
                all_wav.append(FILE_PATH)   
        
    
    print "all_wav ", all_wav
    verify_goodness(all_wav)
    print "verifica ok... procediamo"
    db = GMMVoiceDB(DB_PATH)
    for wav in all_wav:
            OK=0
            OK_best5=0
            print "--------------------"+ wav+ "------------------------"
            v = Voiceid(db, wav)
            v.extract_speakers()
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                print "cluster.get_best_speaker ", str(cluster.get_best_five()[0]) , " correct?", verify_speaker(wav, cluster.get_best_speaker())
                if verify_identity(PID, str(cluster.get_best_five()[0])):
                        OK=OK+1
                if verify_speaker(wav, cluster.get_best_five()[0] ):
                    OK_best5=OK_best5+1
            if 2*OK>= len(v.get_clusters()):
                print "------------------VERIFICA RIUSCITA------------------Doveva riuscire? ", 2*OK_best5>= len(v.get_clusters())
            else:
                print "+++++++++++++++++VERIFICA FALLITA+++++++++++++++++++++Doveva riuscire? ", 2*OK_best5>= len(v.get_clusters())
    print "RND"