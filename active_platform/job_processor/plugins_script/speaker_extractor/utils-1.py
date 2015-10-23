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
"""
Module containing some utilities about subprocess, threading and file checking.
"""

import os
import shlex
import subprocess
import sys
import requests
from django.conf import  settings
from plugins_script.commons.item import set_status, get_status
from plugins_script.commons.keyword import create_keyword
from plugins_script.commons.tags import create_tag, create_dtag, get_tags_by_item, remove_tag, create_uniform_dtags
from plugins_script.commons.person import create_person
from plugins_script.commons.training_set_manager import create_instance, edit_instance, set_instance_feature, get_instance
from plugins_script.commons.training_set_manager import create_model, get_models_by_entity, get_models, edit_instance, set_model_file
from skeleton.skeletons import Farm, Seq
from skeleton.visitors import Executor
from seg_file_utility import make_name_compact , segfile_compact_name2
from model_builder import _humanize_time, build_model, create_new_model, concatena_multi
import re
import shutil



def createTagKeyword(item_id, first_name, last_name, token):
    """
    Funzione temporanea utilizzata per creare una
    keyword contenente il nome della persona e
    associarla all'item in cui compare.
    Necessaria solo per la ricerca nella demo di sinnova!
    """
    k1 = create_keyword(first_name, token)
    k2 = create_keyword(last_name, token)
    
    t1 = create_tag(item_id, k1['id'], 'keyword', token)
    t2 = create_tag(item_id, k2['id'], 'keyword', token)


def speaker_diarization_video(auth_params, func_params):
    try:
        cmd = '/usr/bin/ffmpeg -y -i "' + os.path.join(settings.MEDIA_ROOT, func_params["file"]) + '"'
        cmd += ' -strict -2 -acodec pcm_s16le -ac 1 -ar 16000 '
        cmd += os.path.join(settings.MEDIA_ROOT, 'items', str(func_params['id']), 'audio.wav')
        print cmd
        subprocess.call(cmd, shell=True)
        func_params['file'] = os.path.join('items', str(func_params['id']), 'audio.wav')
        print func_params
        speaker_diarization(auth_params, func_params)
    except:
        print "Error on video speaker extraction"

def speaker_diarization(auth_params, func_params):
    """Bisogna cambiare il nome di questa funzione in speaker identification  """
    try:
        token = auth_params['token']
        # remove existing tags (and dynamic tags) for the item
        tags = get_tags_by_item(func_params['id'], token)
        for tag in tags:
            if tag['type'] == 'speaker':
                remove_tag(tag['id'], token)

        file_path=os.path.join(settings.MEDIA_ROOT, func_params["file"])
        new_file_path=os.path.join(settings.MEDIA_ROOT,'items',str(func_params["id"]),str(func_params["id"]))
        shutil.copy2(file_path,new_file_path)
        file_root=os.path.join(settings.MEDIA_ROOT, 'items', str(func_params["id"]))
        file_path=new_file_path

        if os.path.exists(file_root + "/out"):
            shutil.rmtree(file_root + "/out")
        os.mkdir(file_root + "/out")
        # creazione del file di properties
        with open(file_path.split(".")[0]+'.properties', "w") as f:
	    f.write("fileName="+file_path.split(".")[0])
            with open(os.path.join(settings.MEDIA_ROOT, 'models/audio/globals/settings.properties')) as fp:
                for line in fp:
                    f.write(line)
                    print line
            f.writelines("outputRoot="+file_root+"/out/")
        f.close()
        diarization(file_path.split(".")[0]+'.properties')

        # fare la diarization sul file originale
        # splittare il file di property dei cluster
        # file_list = ['/path/property/file', '...']
        # seq = Seq(diarization)  # incapsula la funzione da calcolare in modo distribuito
        # farm = Farm(seq)        # skeleton necessario per l'esecuzione parallela
        # Executor().eval(farm, file_list) # costrutto che valuta lo skeleton tree

        post_(str(func_params["id"]) , file_root+"/out/"+str(func_params["id"]), token)
    except Exception as e:
        print e

def _build_model(audio_file,train_wav_file,name_surname,duration, token):
    classpath= os.path.join(settings.BASE_DIR, 'plugins_script',"speaker_extractor","lium_spkdiarization-8.4.1.jar" )
    
    ubm= os.path.join(settings.MEDIA_ROOT,"models/audio/globals/ubm.gmm")
    start=0
    audio_file="/tmp/prova.wav"
    gmm_path= build_model (classpath, ubm,audio_file, start, duration, train_wav_file, name_surname, token)
    return gmm_path




def post_(id_item, fp,token):
    classpath= os.path.join(settings.BASE_DIR, 'plugins_script',"speaker_extractor","lium_spkdiarization-8.4.1.jar" )
    ubm= os.path.join(settings.MEDIA_ROOT,"models/audio/globals/ubm.gmm")
    id_persona=None
    result=segfile_compact_name2(fp)
    uniform_tag_ids_arr =[]

    for res in result:
	try:
		name=res[0]
		feature_path = None
		model = None
		p=re.compile('[A-Z]')
		st=int( float(res[1]))#*1000 )
		dur=int (float(res[2]))#*1000)
		feature_path = split4diarization(os.path.join(settings.MEDIA_ROOT, 'items', str(id_item), 'audio.wav'),st,dur,"/tmp/model.wav")
		inst = create_instance('audio', False, token=token) # impostare id modello		
		set_instance_feature(inst['id'], feature_path, token)
		mai=p.findall(name)
		
		f_name="Unknown"
		s_name=name + '_' + str(id_item)
                print "f_name, s_name ", f_name, s_name
                # corregge il problema delle identita' duplicate
                persona = None
		#feature_path = split4diarization(fp,st,dur,"/tmp/model_wav")
                if f_name == "Unknown":
		id_persona=persona["id"]
		tag=create_tag(id_item,id_persona, "speaker", token)
		dtag=create_dtag(tag["id"], st*10, dur*10, token=token)
		uniform_tag = create_tag(id_item, id_persona, "face+speaker", token)
		uniform_tag_ids_arr.append(uniform_tag['id'])

	except Exception, e:
		print e
    
    set_status(id_item,"SPEAKER_RECOG", token)    
    create_uniform_dtags(id_item, token)

def split4diarization(orig,start,duration, dest):
    command="/usr/bin/ffmpeg -y -i "+str(orig) + " -ss " + str(start) + " -t " + str(duration) + " -acodec copy "+dest
    start_subprocess(command)
    return dest

def _mkdir_out(path_dir):
    print "try mkdir "+path_dir
    subprocess.check_output("/bin/mkdir "+path_dir,shell=True)

def _convert_with_ffmpeg(file_name):
    subprocess.check_output('/usr/bin/ffmpeg -y -i "' + file_name + '" -acodec pcm_s16le -ac 1 -ar 16000 "' + file_name.split(".")[0] + '.wav"', shell=True)


def diarization(file_properties):
    cd_go="cd " + settings.BASE_DIR + "/plugins_script/speaker_extractor/;"
    java="java -Xmx2048m " #da definire in base alla macchina
    java_classpath = " -classpath " + settings.BASE_DIR + "/plugins_script/speaker_extractor/lium_spkdiarization-8.4.1.jar " 
    commandline=java+java_classpath+" it.crs4.identification.DBScore \""+file_properties + "\"" 
    start_subprocess(commandline)


def identification(file_properties):
    cd_go="cd " + settings.BASE_DIR + "/plugins_script/speaker_extractor/;"
    java="java -Xmx2048m " #da definire in base alla macchina
    java_classpath = " -classpath " + settings.BASE_DIR + "/plugins_script/speaker_extractor/lium_spkdiarization-8.4.1.jar " 
    commandline=java+java_classpath+" it.crs4.identification.DBScore \""+file_properties + "\" nodiarization"
    print "diarization -- command \n"
    print commandline
    start_subprocess(commandline)
    # restituire la lista di file creati dalla fase di diariation???

"""
def alive_threads(t_dict):
    
    #Check how much threads are running and alive in a thread dictionary

    #:type t: dictionary
    #:param t: thread dictionary like  { key : thread_obj, ... }
    
    num = 0
    for thr in t_dict:
        if t_dict[thr].is_alive():
            num += 1
    return num
"""



def start_subprocess(commandline):
    #Start a subprocess using the given commandline and check for correct
    #termination.

    #:type commandline: string
    #:param commandline: the command to run in a subprocess
    #"""
    if sys.platform == 'win32':
        commandline = commandline.replace('\\','\\\\')
        
        args = shlex.split(commandline)
        startupinfo = subprocess.STARTUPINFO()
        #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(args)
    else:
        print "UTILS -- commandline ",  commandline
        args = shlex.split(commandline)
        proc = subprocess.Popen(args)
    retval = proc.wait()

    if retval != 0:
        err = OSError("Subprocess %s closed unexpectedly [%s]" % (str(proc),
                                                                  commandline))
        err.errno = retval
        raise err


def check_cmd_output(command):
    "Run a shell command and return the result as string"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
    output = process.communicate()
    retcode = process.poll()
    if retcode:
        raise subprocess.CalledProcessError(retcode,
                                            command)
                                            # output=output[0]???
    return output

def ensure_file_exists(filename):
    """Ensure file exists and is not empty, otherwise raise an IOError.

    :type filename: string
    :param filename: file to check"""
    if not os.path.exists(filename):
        raise IOError("File %s doesn't exist or not correctly created" 
                      % filename)
    if not (os.path.getsize(filename) > 0):
        raise IOError("File %s empty" % filename)
    
    (shortname, extension) = os.path.splitext(filename)
    if sys.platform == 'win32' and extension=='.seg':
        import fileinput
        for line in fileinput.FileInput(filename,inplace=0):
            line = line.replace("\\\\","/")

def is_good_wave(filename):
    """
    Check if the wave is in correct format for LIUM.

    :type filename: string
    :param filename: file to check
    """
    import wave
    par = None
    try:
        w_file = wave.open(filename)
        par = w_file.getparams()
        w_file.close()
    except wave.Error, exc:
        print exc
        return False
    if par[:3] == (1, 2, 16000) and par[-1:] == ('not compressed',):
        return True
    else:
        return False


def humanize_time(secs):
    """
    Convert seconds into time format.

    :type secs: integer
    :param secs: the time in seconds to represent in human readable format
   (hh:mm:ss)
   """
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d,%s' % (hours, mins, int(secs), 
                                 str(("%0.3f" % secs))[-3:])

def convert_with_ffmpeg(file_name):
    print "try conversion..."
    
    print 'ffmpeg -i "' + file_name + '" -acodec pcm_s16le -ac 1 -ar 16000 "'+ file_name.split(".")[0] + '.wav"'
    subprocess.call('ffmpeg -i "' + file_name + '" -acodec pcm_s16le -ac 1 -ar 16000 "' + file_name.split(".")[0] + '.wav"')







####### funzione utilizzata per estrarre e salvare le istanze ####
def __generate_instances(auth_params, func_params):
    """
    Funzione utilizzata per estrarre le istanze da un file audio e
    salvarle nel database senza associarle ad alcuna entita'/modello.
    Le istanze sono ottenute applicando prima una conversione sulla traccia
    audio originale e successivamente splittandola sul parlato delle persone.
    Il parametro generato dalle funzioni contiene i dati associati al nuovo
    """
    try:
        # extract all needed parameters
        item_id   = func_params['id']
        item_path = os.path.join(settings.MEDIA_ROOT, func_params['file'])
        temp_root = os.path.join('/tmp', 'speak_recog_' + str(item_id))
        dest_path = os.path.join(temp_root, 'audio.wav')
        properties_path = dest_path.split(".")[-2]+'.properties'
        settings_path   = os.path.join(settings.MEDIA_ROOT, 'models/audio/globals/settings.properties')
        token     = auth_params.get('token', '1234')
        #print 'item_id',   item_id
        #print 'item_path', item_path
        #print 'temp_root', temp_root
        #print 'dest_path', dest_path
        #print 'properties_path', properties_path
        #print 'settings_path',   settings_path

        # create a directory for temporary files for diarization phase
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)
        os.mkdir(temp_root)
        os.chmod(temp_root, 0o777)
        os.mkdir(temp_root + '/out')
        os.chmod(temp_root + '/out', 0o777)

        # extract the item audio and convert it in the wav format
        command  = '/usr/bin/ffmpeg -y -i "' + item_path + '"'
        command += ' -strict -2 -acodec pcm_s16le -ac 1 -ar 16000 '
        command += '"' + dest_path + '"'
        subprocess.call(command, shell=True)
        #print command
        
        # generate the local settings file
        with open(properties_path, "w") as f:
	    f.write("fileName=" + dest_path)
            with open(settings_path) as fp:
                for line in fp:
                    f.write(line)
                    #print line
            f.writelines("outputRoot=" + temp_root + "/out/")

        # applica la fase di diarization e calcola gli spezzoni audio
        diarization(properties_path)            # salva gli spezzoni audio nel file di settings?
        
        # extract the audio portions and save them in a temp directory
        occurrences = segfile_compact_name2(temp_root + '/out/audio')
        for o in occurrences:
            start    = int(o[1])*10
            duration = int(o[2])*10
            # genera lo spezzone a partire dal file audio
            feature_path = temp_root + '/out/segment_' + str(item_id) + '_' + str(o[1]) + '.wav'
            split4diarization(dest_path, start, duration, feature_path)

            # genera il tag e il dtag da associare all'istanza
            persona = create_person('Unknown', o[0] + '_' + str(item_id), token=token)
            tag     = create_tag(item_id, persona['id'], 'speaker', token=token)
            dtag    = create_dtag(tag['id'], start, duration, token=token)

            # crea l'istanza e la carica nel database
            inst = create_instance('audio', False, token=token)
            set_instance_feature(inst['id'], feature_path, token=token)

        # remove all temporary directories and files
        #os.remove(temp_path)
    except Exception as e:
        print e


def __recognize_instance(auth_params, func_params):
    """
    Funzione utilizzata per applicare i modelli esistenti alle nuove istanze di
    tipo audio che vengono salvate nel database.
    Il modello con il punteggio di riconoscimento piu' alto viene assegnato
    all'istanza considerata (l'id della persona associata al modello)
    """
    try:
        # extract all needed parameters
        instance_id   = func_params["id"]
        instance_path = os.path.join(settings.MEDIA_ROOT, func_params["features"])
        models = get_models('audio', token=token)

        # copiare i modelli in una cartella in tmp

        # avviare l'identificazione dell'istanza
        model_id = identification() # ha bisogno del file di settings locale (ricostruirlo?)

        # extract model parameters
        model_id   = model['id']
        model_path = os.path.join(settings.MEDIA_ROOT, model['model_file'])
        entity_id  = model['entity']
        print 'Comparing model ' + model_id + ' with instance ' + instance_id

            
        # update the instance reference if recognized
        if model_id is not None:
            edit_instance(instance_id, model_id=model_id, token=token)
            return 'Instance ' + instance_id + ' associated to model ' + model_id
        return 'Instance ' + instance_id + ' not recognized by any model'

        #TODO modificare i dynamic tag per associare automaticamente la persona

    except Exception as e:
        print e
        return 'Error on instance recognition'
    

####### funzione utilizzata per costruire i modelli audio ########
def __build_model(auth_params, func_params):
    """
    Funzione utilizzata per costruire il modello di riconoscimento audio
    a partire da un insieme di istanze che vengono fornite dall'utente
    attraverso l'apposita GUI.
    In particolar ela funzione consente di :
    - ottenere la lista di istanze specificate dall'utente
    - recuperare il path completo associato a ciascuna istanza
    - unire le istanze in un unico file audio
    - effettuare la costruzione del modello di riconoscimento vocale
    - creare la persona e il modello sul database
    - associare i file creati alla persona e al modello
    - rimuovere tutti i file temporanei creati
    """
    try:
        token    = auth_params.get('token', '1234')
        f_name   = func_params.get('first_name', 'Pinco')
        s_name   = func_params.get('last_name',  'Pallino')
        inst_ids = func_params.get('inst_list', [])
        ubm      = os.path.join(settings.MEDIA_ROOT, 'models', 'audio', 'globals', 'ubm.gmm')
        classpath= os.path.join(settings.BASE_DIR, 'plugins_script', 'speaker_extractor' , 'lium_spkdiarization-8.4.1.jar')

        # crea un modello e una persona con i dati forniti
        person = create_person(f_name, s_name, token=token)
        model  = create_model(person['id'], 'audio', f_name + ' ' + s_name, last_update=None, token=token)
        #print person, model
        
        # recupera gli oggetti corrispondenti alle istanze
        #print inst_ids
        inst_paths = []
        for inst_id in inst_ids:
            inst = get_instance(inst_id, token=token)
            inst_paths.append(os.path.join(settings.MEDIA_ROOT, inst['features']))
        #print inst_paths

        # concat all provided feature files
        temp = '/tmp/model_' + str(model['id']) + '.wav'
        concatena_multi(inst_paths, temp)
        #print temp

        # calcola e imposta il modello generato nel database
        model_path = create_new_model(classpath, ubm, temp, 0, None, None)
        set_model_file(model['id'], model_path, token=token)
        #print model_path

        # remove all created temporary files
        #os.remove(model_path)
        
    except Exception as e:
        print e
        return 'Error during entity model building'
