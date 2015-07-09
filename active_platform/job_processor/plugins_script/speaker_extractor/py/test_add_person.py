'''
Created on Oct 1, 2014

@author: labcontenuti
'''


from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
import os, fnmatch 

DIR_PATH='/Users/labcontenuti/Desktop/voiceid/radio/voci/'
DB_PATH='/Users/labcontenuti/.voiceid/gmm_db'
DB_PATH='.'
find_ok=[]
find_errata=[]
not_find=[]
unknown_ok=[]
unknown_errata=[]

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
def get_simbol(wav):
    tmp=wav.split("##")[0]
    ns=tmp.split("_")
    return ns[0]+ns[1]

if __name__ == '__main__':
    all_wav =[]
    for f in os.listdir(DIR_PATH):
        if fnmatch.fnmatch(f, '*.wav') and f.find("##")>-1:
            all_wav.append(f)   
    print all_wav
    #all_wav=["/Users/labcontenuti/Documents/workspace/activevoice/voiceid/Talk_Radio##S10.wav"]
    #all_wav=["/Users/labcontenuti/Music/Renato_Soru0##S0.wav"]
    all_wav=["/Users/labcontenuti/Music/RenatoSoruS0.wav"]
    db = GMMVoiceDB(DB_PATH)

    for wav in all_wav:
        #db.add_model(DIR_PATH+wav, get_simbol(wav))
        db.add_model(wav, "RenatoSoru")
        print "added ", wav

    print "RND"
