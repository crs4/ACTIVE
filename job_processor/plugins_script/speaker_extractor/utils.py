
import os
import shlex
import subprocess
import sys
from django.conf import  settings

"""
Module containing some utilities about subprocess, threading and file checking.
"""
   


def speaker_diarization(func_in, func_out):
	try:
		file_path=os.path.join(settings.MEDIA_ROOT, "items", func_out["file"])	
		file_root=os.path.join(settings.MEDIA_ROOT, "items", str(func_out["id"])) # e' necessario il casting esplicito degli interi?

		_convert_with_ffmpeg(file_path)

		os.mkdir(file_root + "/out")		
	   	with open(file_path.split(".")[0]+'.properties', "w") as f:
                        f.write("fileName="+file_path.split(".")[0]+".wav")
                        #f.write("outputRoot="+file_root+"/")
	    		with open('/var/spool/active/data/models/audio/globals/settings.properties') as fp:
        			for line in fp:
            				f.write(line)
					print line
			#f.writelines("fileName="+file_path.split(".")[0]+".wav")
			f.writelines("outputRoot="+file_root+"/out/")
		#f.flush()
		f.close()
		#fp.close()    		
		diarization(file_path.split(".")[0]+'.properties')
	except Exception as e:
		print e

def _convert_with_ffmpeg(file_name):
    print "try conversion..."
    
    print "/usr/bin/ffmpeg -y -i "+file_name+" -acodec pcm_s16le -ac 1 -ar 16000 "+file_name.split(".")[0]+".wav"	
    subprocess.check_output("/usr/bin/ffmpeg -y -i "+file_name+" -acodec pcm_s16le -ac 1 -ar 16000 "+file_name.split(".")[0]+".wav", shell=True)


def diarization(file_properties):
    cd_go="cd /var/spool/active/job_processor/plugins_script/speaker_extractor/;"
    java="java -Xmx2048m " #da definire in base alla macchina
    java_classpath=" -classpath /var/spool/active/job_processor/plugins_script/speaker_extractor/lium_spkdiarization-8.4.1.jar " 
    commandline=java+java_classpath+" it.crs4.active.diarization.Diarization "+file_properties 
    print "diarization -- command \n"
    print commandline
    start_subprocess(commandline)


def alive_threads(t_dict):
    """Check how much threads are running and alive in a thread dictionary

    :type t: dictionary
    :param t: thread dictionary like  { key : thread_obj, ... }"""
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
    """Check if the wave is in correct format for LIUM.

    :type filename: string
    :param filename: file to check"""
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
    """Convert seconds into time format.

    :type secs: integer
    :param secs: the time in seconds to represent in human readable format
           (hh:mm:ss)"""
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d,%s' % (hours, mins, int(secs), 
                                  str(("%0.3f" % secs))[-3:])
def convert_with_ffmpeg(file_name):
    print "try conversion..."
    
    print "ffmpeg -i "+file_name+" -acodec pcm_s16le -ac 1 -ar 16000 "+file_name.split(".")[0]+".wav"
    subprocess.call("ffmpeg -i "+file_name+" -acodec pcm_s16le -ac 1 -ar 16000 "+file_name.split(".")[0]+".wav")
