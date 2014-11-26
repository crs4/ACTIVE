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
DIR_PATH='/Users/labcontenuti/Desktop/voiceid/VidTIMIT-Audio/TestSetWav/fc_mh0/'


DB_PATH='/Users/labcontenuti/.voiceid/gmm_db'
find_ok=[]
find_errata=[]
not_find=[]
unknown_ok=[]
unknown_errata=[]

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
    
    parser.print_help()
     
    (options, args) = parser.parse_args()
    print "options ", options
    print "args ", args
    if len(args) == 0:
        print "[Error] No model was given."
        exit()
    # This model will be used (or created if the training parameter (-t, --train) exists:
    model_filename = args[0]
   
    all_wav =[]
    for f in os.listdir(DIR_PATH):
        if fnmatch.fnmatch(f, '*.wav') and f.find("##")>-1:
            all_wav.append(f)   
    print all_wav
    
    verify_goodness(all_wav)
    
    print "verifica ok... procediamo"
    
    logging.basicConfig(filename=DIR_PATH+'/result.log',level=logging.INFO)
    
    db = GMMVoiceDB('/Users/labcontenuti/.voiceid/gmm_db')
    filter_criteria="Fabrizio_Gifuni##02Pasticciaccio.wav"
    for wav in all_wav: 
        #if wav.find(filter_criteria)>-1:
            print "--------------------"+ wav+ "------------------------"
            v = Voiceid(db, DIR_PATH+wav)
            v.extract_speakers()
            
            logging.info("\n\n\n---------------------"+wav+"------------------")
            wav_tostring=str(wav)+";   "
            
            for c in v.get_clusters():
                cluster = v.get_cluster(c)
                for seg in cluster.get_segments():
                    print "\n seg: ", seg
                    print seg.get_start()
                    print seg.get_end()
                    print humanize_time(seg.get_duration())
                
                
                print "cluster.get_duration  ", cluster.get_duration()
                logging.info("duration: "+ str(cluster.get_duration()))      
                wav_tostring=wav_tostring+":  "+"duration:"+ str(cluster.get_duration())
                      
                print "cluster.get_name ", cluster.get_name()        
                print "cluster.get_best_speaker ", cluster.get_best_speaker() , " correct?", verify_speaker(wav, cluster.get_best_speaker())
                logging.info("best_speaker "+str(cluster.get_best_speaker()))
                wav_tostring=wav_tostring+";  "+"best_speaker:"+str(cluster.get_best_speaker())
                
                print "v._get_time() ", v._get_time(), " ", humanize_time(v._get_time())
                logging.info("get_time:  "+str(humanize_time(v._get_time() ) ))
                wav_tostring=wav_tostring+";  "+"get_time:"+str(humanize_time(v._get_time() ) )
                
                #if cluster.get_best_speaker()=="unknown":
                print "cluster.get_best_five ", cluster.get_best_five(), cluster.get_best_five()[0]
                logging.info("best of five: "+ str(cluster.get_best_five()[0]) ) 
                wav_tostring=wav_tostring+";  "+"best of five:"+ str(cluster.get_best_five()[0]) 
                
                
                print "cluster.get_distance() ", str( cluster.get_distance() )
                logging.info("distance best-closest "+ str(cluster.get_distance()) ) 
                wav_tostring=wav_tostring+";  "+"distance best-closest:"+ str(cluster.get_distance())

                    
                print
                if not cluster.get_best_speaker()=="unknown":
                    if verify_speaker(wav, cluster.get_best_speaker()):
                        find_ok.append(wav_tostring)
                    else:
                        find_errata.append(wav_tostring)     
                else: 
                    not_find.append(wav_tostring)
                    if verify_speaker(wav, cluster.get_best_five()[0][0]):
                        unknown_ok.append(wav_tostring)
                    else:
                        unknown_errata.append(wav_tostring  )     

        
            print "Number TEST--"+ str(len(find_ok) +len(find_errata)+len(not_find))
            print "OK---------  "+ str(len(find_ok))
            print "ERRATA-------"+ str(len(find_errata))
            print "UNKNOWN------"+ str(len(not_find))
            print "UNKNOWN ERR--"+ str(len(unknown_errata))
            print "UNKNOWN  OK--"+ str(len(unknown_ok))
        #resutl_file=file(DIR_PATH+"result.txt", "a+")
        
    logging.info("\n\n")    #for wav in unknown_errata:
    logging.info("Number TEST "+ str(len(find_ok) +len(find_errata)+len(not_find)))
    logging.info("ok "+ str(len(find_ok)) )         
    logging.info("ERRATA"+ str(len(find_errata)))
    logging.info("UNKNOWN"+ str(len(not_find)))
    logging.info("UNKNOWN ERR "+ str(len(unknown_errata)))
    logging.info("UNKNOWN  OK "+ str(len(unknown_ok)))
    
    
    logging.info("\n\n\n----UNKNOWN  OK ---")
    for f in unknown_ok: 
        logging.info(f)
    
    logging.info("\n\n\n----UNKNOWN  ERRATA ---")
    for f in unknown_errata: 
        logging.info(f)
    
    logging.info("\n\n\n----ERRATA---")
    for f in find_errata: 
        logging.info(f)
        

    
    

    print "RND"