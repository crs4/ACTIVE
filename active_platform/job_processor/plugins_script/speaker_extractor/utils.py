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
from skeleton.skeletons import Farm, Seq
from skeleton.visitors import Executor
from seg_file_utility import make_name_compact
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
    try:
        token = auth_params['token']
        # remove existing tags (and dynamic tags) for the item
        tags = get_tags_by_item(func_params['id'], token)
        for tag in tags:
            if tag['type'] == 'speaker':
                remove_tag(tag['id'], token)

        print "***** PLUGIN SPEAKER RECOGNITION: DIARIZATION ---> START"
        file_path=os.path.join(settings.MEDIA_ROOT, func_params["file"])
        new_file_path=os.path.join(settings.MEDIA_ROOT,'items',str(func_params["id"]),str(func_params["id"]))
        print "new file path ",new_file_path
        shutil.copy2(file_path,new_file_path)
        file_root=os.path.join(settings.MEDIA_ROOT, 'items', str(func_params["id"])) # e' necessario il casting esplicito degli interi?
        file_path=new_file_path
        #convert_with_ffmpeg(file_path)

        #_mkdir_out(file_root+"/out")
        # delete the path if exists and create a new one
        if os.path.exists(file_root + "/out"):
            shutil.rmtree(file_root + "/out")
        os.mkdir(file_root + "/out")

        with open(file_path.split(".")[0]+'.properties', "w") as f:
            #f.write("fileName="+file_path.split(".")[0]+".wav")
	    f.write("fileName="+file_path.split(".")[0])
            with open(os.path.join(settings.MEDIA_ROOT, 'models/audio/globals/settings.properties')) as fp:
                for line in fp:
                    f.write(line)
                    print line
            #f.writelines("fileName="+file_path.split(".")[0]+".wav")
            f.writelines("outputRoot="+file_root+"/out/")
            #f.writelines("outputRoot="+file_root)
        f.close()
        diarization(file_path.split(".")[0]+'.properties')

        # fare la diarization sul file originale
        # splittare il file di property dei cluster
        # file_list = ['/path/property/file', '...']
        # seq = Seq(diarization)  # incapsula la funzione da calcolare in modo distribuito
        # farm = Farm(seq)        # skeleton necessario per l'esecuzione parallela
        # Executor().eval(farm, file_list) # costrutto che valuta lo skeleton tree

        print "***** PLUGIN SPEAKER RECOGNITION: DIARIZATION ---> STOP"
        print "fp=",file_root+"/out/"+func_params["filename"].split(".")[0]
        post_di_esempio(str(func_params["id"]) , file_root+"/out/"+str(func_params["id"]), token)
    except Exception as e:
        print e

def post_di_esempio(id_item, fp,token):
    print "***** PLUGIN SPEAKER RECOGNITION: POST DI ESEMPIO ---> Start"
    id_persona=None
    #id_item=3601
    #name_p=open(name_file, "r")
    #name_p_list=name_p.readlines()
    result=make_name_compact(fp) #result simile a [[nome,start,stop][nome,start,stop]]
    print "result=",result
    uniform_tag_ids_arr =[]

    for res in result:
	try:
		name=res[0]
		p=re.compile('[A-Z]')
		print "find name ", name
		if name.find("GiacomoMameli")>-1:
		    print "trovato giacomino"
		    id_persona=create_person("Giacomo","Mameli", token)["id"]
                    #createTagKeyword(id_item, 'Giacomo', 'Mameli', token)
		    print "id persona ",id_persona
		else:
		    mai=p.findall(name)
		    if len(mai)==2:
			f_name=name.split(mai[1])[0]
			s_name=mai[1]+name.split(mai[1])[1]
                        
                        # corregge il problema delle identita' duplicate
                        persona = None
                        if f_name == "Unknown":
			    persona=create_person(f_name,s_name+'_'+str(id_item), token)
                        else:
                            persona=create_person(f_name, s_name, token)
                        
                        # create a tag for person name
                        #createTagKeyword(id_item, persona['first_name'], persona['last_name'], token)

			id_persona=persona["id"]
		    else:	
		    	persona=create_person("Il","Manutentore", token)
		    	id_persona=persona["id"]
		print "create_tag id_item,id_persona ", id_item, " ",id_persona
		tag=create_tag(id_item,id_persona, "speaker", token)
		uniform_tag = create_tag(id_item, id_persona, "face+speaker", token)
		uniform_tag_ids_arr.append(uniform_tag['id'])

		print "tag ",tag
		st=int( float(res[1])*1000 )
		print "start ", st
		dur=int (float(res[2])*1000)
		print "dur ",dur
		dtag=create_dtag(tag["id"],st,dur, token=token)
		print "dtag ",dtag
        
    
	except Exception, e:
		print e
    
    set_status(id_item,"SPEAKER_RECOG", token)    
    """
    item_status = get_status(id_item, token) 
    if "FACE_RECOG" in item_status['status']:
        for u_tag_id in uniform_tag_ids_arr:
            create_uniform_dtags(id_item, uniform_tag_id, token)
    """
    create_uniform_dtags(id_item, token)
    print "***** PLUGIN SPEAKER RECOGNITION: POST DI ESEMPIO ---> STOP"
    """

    r_json=create_dtag(id_persona,"0","60000", token)    
    set_status(id_item,"SPEAKER_RECOG", token)
    """




def _mkdir_out(path_dir):
    print "try mkdir "+path_dir
    subprocess.check_output("/bin/mkdir "+path_dir,shell=True)

def _convert_with_ffmpeg(file_name):
    print "try conversion..."
    
    print '/usr/bin/ffmpeg -y -i "' + file_name + '" -acodec pcm_s16le -ac 1 -ar 16000 "' + file_name.split(".")[0] + '.wav"'	
    subprocess.check_output('/usr/bin/ffmpeg -y -i "' + file_name + '" -acodec pcm_s16le -ac 1 -ar 16000 "' + file_name.split(".")[0] + '.wav"', shell=True)
    print "conversion ok"


def diarization(file_properties):
    cd_go="cd " + settings.BASE_DIR + "/plugins_script/speaker_extractor/;"
    java="java -Xmx2048m " #da definire in base alla macchina
    java_classpath=" -classpath " + settings.BASE_DIR + "/plugins_script/speaker_extractor/lium_spkdiarization-8.4.1.jar " 
    commandline=java+java_classpath+" it.crs4.identification.DBScore \""+file_properties + "\"" 
    print "diarization -- command \n"
    print commandline
    start_subprocess(commandline)




def alive_threads(t_dict):
    """
    Check how much threads are running and alive in a thread dictionary

    :type t: dictionary
    :param t: thread dictionary like  { key : thread_obj, ... }
    """
    num = 0
    for thr in t_dict:
        if t_dict[thr].is_alive():
            num += 1
    return num


def start_subprocess(commandline):
    """Start a subprocess using the given commandline and check for correct
    termination.

    :type commandline: string
    :param commandline: the command to run in a subprocess"""
    if sys.platform == 'win32':
        commandline = commandline.replace('\\','\\\\')
        
        args = shlex.split(commandline)
        startupinfo = subprocess.STARTUPINFO()
        #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(args)
    else:
        print "UTILS -- commandline ",  commandline
        args = shlex.split(commandline)
#         print commandline
        proc = subprocess.Popen(args)
    retval = proc.wait()
#    except:
#        print "except 1327"
#        args = commandline.split(' ')
#        proc = subprocess.Popen(args, stdin=output_redirect, 
#                                stdout=output_redirect, 
#                             stderr=output_redirect)
#        retval = proc.wait()        

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

