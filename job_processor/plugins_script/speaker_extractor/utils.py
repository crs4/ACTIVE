"""
Module containing some utilities about subprocess, threading and file checking.
"""

import os
import shlex
import subprocess
import sys
import requests
from django.conf import  settings
from plugins_script.commons.item import set_status
from plugins_script.commons.tags import create_tag, create_dtag, get_tags_by_item, remove_tag
from plugins_script.commons.person import create_person
from skeleton.skeletons import Farm, Seq
from skeleton.visitors import Executor
from seg_file_utility import make_name_compact
import re
import shutil

def speaker_diarization(func_in, func_out):
    try:
        # remove existing tags (and dynamic tags) for the item
        tags = get_tags_by_item(func_out['id'])
        for tag in tags:
            remove_tag(tag['id'])

        print "***** PLUGIN SPEAKER RECOGNITION: DIARIZATION ---> START"
        file_path=os.path.join(settings.MEDIA_ROOT, func_out["file"])
        new_file_path=os.path.join(settings.MEDIA_ROOT,'items',str(func_out["id"]),str(func_out["id"]))
        print "new file path ",new_file_path
        shutil.copy2(file_path,new_file_path)
        file_root=os.path.join(settings.MEDIA_ROOT, 'items', str(func_out["id"])) # e' necessario il casting esplicito degli interi?
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
        print "fp=",file_root+"/out/"+func_out["filename"].split(".")[0]
        post_di_esempio(id_item=str(func_out["id"]) , fp=file_root+"/out/"+str(func_out["id"]))
    except Exception as e:
        print e

def post_di_esempio(id_item,fp):
    print "***** PLUGIN SPEAKER RECOGNITION: POST DI ESEMPIO ---> Start"
    id_persona=None
    #id_item=3601
    #name_p=open(name_file, "r")
    #name_p_list=name_p.readlines()
    result=make_name_compact(fp) #result simile a [[nome,start,stop][nome,start,stop]]
    print "result=",result
    for res in result:
	try:
		name=res[0]
		p=re.compile('[A-Z]')
		print "find name ", name
		if name.find("GiacomoMameli")>-1:
		    print "trovato giacomino"
		    id_persona=create_person("Giacomo","Mameli")["id"]
		    print "id persona ",id_persona
		else:
		    mai=p.findall(name)
		    if len(mai)==2:
			f_name=name.split(mai[1])[0]
			s_name=mai[1]+name.split(mai[1])[1]
			persona=create_person(f_name,s_name)
			id_persona=persona["id"]
		    else:	
		    	persona=create_person("Il","Manutentore")
		    	id_persona=persona["id"]
		print "create_tag id_item,id_persona ", id_item, " ",id_persona
		tag=create_tag(id_item,id_persona, "speaker")
		print "tag ",tag
		st=int( float(res[1])*1000 )
		print "start ", st
		dur=int (float(res[2])*1000)
		print "dur ",dur
		dtag=create_dtag(tag["id"],st,dur)
		print "dtag ",dtag
	except Exception, e:
		print e
    print "***** PLUGIN SPEAKER RECOGNITION: POST DI ESEMPIO ---> STOP"
    """

    r_json=create_dtag(id_persona,"0","60000")    
    set_status(id_item,"SPEAKER_RECOG")
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
    cd_go="cd /var/spool/active/job_processor/plugins_script/speaker_extractor/;"
    java="java -Xmx2048m " #da definire in base alla macchina
    java_classpath=" -classpath /var/spool/active/job_processor/plugins_script/speaker_extractor/lium_spkdiarization-8.4.1.jar " 
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

