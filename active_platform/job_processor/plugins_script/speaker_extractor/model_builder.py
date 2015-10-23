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
import fnmatch
import os
import shlex
import subprocess
import sys
import shelve
import shutil
from plugins_script.commons.person  import *
from plugins_script.commons.training_set_manager  import *
 
"""Module containing some utilities about subprocess,
threading and file checking."""
import os.path

def split_audio_file(orig,start,duration, dest):
    if dest==None:
        dest=orig.split(".wav")[0]
        dest=dest+"_temp.wav"
    
    command="/usr/bin/ffmpeg -i "+str(orig) + " -ss "+_humanize_time(start)+" -t "+_humanize_time(duration)+" -acodec copy "+dest
    print "split_audio_file ",command
    start_subprocess(command)
    return dest

def concatena(orig,add):
       command="/opt/local/bin/sox "+str(orig) + "  "+str(add)+" " +str(orig)+"_TMP.wav"
       start_subprocess(command)
       start_subprocess("/bin/rm "+str(orig))
       shutil.copy2(str(orig)+"_TMP.wav", str(orig))
       start_subprocess("/bin/rm "+str(orig)+"_TMP.wav")
       start_subprocess("/bin/rm "+str(add))

def concatena_multi(file_paths, dest_file):
    command="/usr/bin/sox"
    for path in file_paths:
        command += " " + path
    command += " " + dest_file
    start_subprocess(command)
    #start_subprocess("/bin/rm "+str(orig))
    #shutil.copy2(str(orig)+"_TMP.wav", str(orig))
    #start_subprocess("/bin/rm "+str(orig)+"_TMP.wav")
    #start_subprocess("/bin/rm "+str(add))

def _de_humanize(tm):
    print "tm ",tm
    tms=tm.split(",")
    msec= float(tms[1])/1000
    hms=tms[0].split(":")
    h=float(hms[0])*60
    m=float(hms[1])*60
    s=float(hms[2])
    return str(int(msec+h+m+s))

def _humanize_time(secs):
    """Convert seconds into time format.
    :type secs: integer
    :param secs: the time in seconds to represent in human readable format
           (hh:mm:ss)"""
    print '_humanize_time', secs
    mins, secs = divmod(int(secs), 60)
    hours, mins = divmod(int(mins), 60)
    return '%02d:%02d:%02d' % (hours, mins, int(secs))

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
    print "MODEL BUILDER -- commandline ",  commandline
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
def get_wave_duration(wave_file):
    import wave
    import contextlib
     
    with contextlib.closing(wave.open(wave_file,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()

        duration = frames / float(rate)
        print(duration)
    return duration
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
    """
    Convert seconds into time format.

    :type secs: integer
    :param secs: the time in seconds to represent in human readable format
           (hh:mm:ss)
    """
    print secs
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d,%s' % (hours, mins, int(secs), 
                                  str(("%0.3f" % secs))[-3:])
    
def convert_with_ffmpeg(file_name):
    print "try conversion..."
    
    print "ffmpeg -i "+file_name+" -acodec pcm_s16le -ac 1 -ar 16000 "+file_name.split(".")[0]+".wav"
    subprocess.call("ffmpeg -i "+file_name+" -acodec pcm_s16le -ac 1 -ar 16000 "+file_name.split(".")[0]+".wav", shell=True)
    
def convert_dir_with_ffmpeg(dir_path, ext=None):
    all_wav=[]
    for f in os.listdir(dir_path):
        if not ext==None:
            if fnmatch.fnmatch(f, '*.'+ext):
                all_wav.append(f)
        else:
            all_wav.append(f)
    for f in all_wav:
        convert_with_ffmpeg(dir_path+"/"+f)
"""
java -Xmx2048m -jar ../../LIUM_SpkDiarization-8.4.1.jar fr.lium.spkDiarization.system.Diarization  --sOutputMask=%s.seg --doCEClustering SandroLombardi##gep_01
"""

def diarization(classpath,file_name,base_name):

    if base_name==None:
        base_name=file_name.split(".wav")[0]
    else:
        tmp=file_name.split(".wav")[0]
        old=tmp.split("/")[-1]
        base_name=tmp.replace(old,base_name)
    command= "java -jar "+classpath+" fr.lium.spkDiarization.system.Diarization  --sOutputMask="+base_name+".seg --fInputMask="+base_name+".wav --doCEClustering " +base_name
    print "diarization command ",command
    start_subprocess(command)
def train_init(classpath, ubm, file_name, base_name):
    if base_name==None:    
        base_name=file_name.split(".wav")[0]
    else:
        tmp=file_name.split(".wav")[0]
        old=base_name.split("/")[-1]
        base_name=tmp.replace(old,base_name)
    command= "java -cp "+classpath+" fr.lium.spkDiarization.programs.MTrainInit --sInputMask="+base_name+".seg --fInputMask="+base_name+".wav " 
    command=command +"--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4 --emInitMethod=copy --tInputMask="+ubm + " --tOutputMask="+base_name+".init.gmm "+base_name 
    start_subprocess(command)

def train_map(classpath,file_name,base_name):
    if base_name==None:
        base_name=file_name.split(".wav")[0]
    else:
        tmp=file_name.split(".wav")[0]
        old=base_name.split("/")[-1]
        base_name=tmp.replace(old,base_name)
    command= "java -cp "+classpath+" fr.lium.spkDiarization.programs.MTrainMAP --sInputMask="+base_name+".seg --fInputMask="+base_name+".wav " 
    command=command +" --fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4  --tInputMask="+base_name + ".init.gmm --emCtrl=1,5,0.01 --varCtrl=0.01,10.0 --tOutputMask="+base_name+".gmm "+base_name 
    start_subprocess(command)
    return base_name+".gmm"

def garbage(file_name):
    base_name=file_name.split(".wav")[0]
    print "garbage ---"+ "/usr/bin/rm "+base_name+".seg"
    start_subprocess("/bin/rm "+base_name+".seg")
    print "garbage ---"+ "/bin/rm "+base_name+".init.gmm"
    start_subprocess("/bin/rm "+base_name+".init.gmm")

def create_new_model(classpath, ubm, file_path, start, duration, gmm_name):
    if duration is None:
        duration = get_wave_duration(file_path)

    print "create_new_model ",classpath, ubm, file_path, start, duration, gmm_name
    diarization(classpath,file_path , gmm_name)
    train_init(classpath, ubm, file_path, gmm_name)
    gmm_path=train_map(classpath,file_path, gmm_name)
    #garbage(file_path)
    return gmm_path
 
def Main(classpath, ubm, orig, start, duration, train_wav_file, gmm_name):
    new_audio=split_audio_file(orig, start, duration, gmm_name)
    if train_wav_file==None:
        train_wav_file=new_audio
    else:
        concatena(train_wav_file,new_audio)
    if not gmm_name==None:
        old=train_wav_file.split("/")[-1]
        new_train_wav_file=train_wav_file.replace(old,gmm_name+".wav")
        print "trying rename %s --%s ", train_wav_file, new_train_wav_file
        shutil.copy2(train_wav_file, new_train_wav_file)
        train_wav_file=new_train_wav_file
    diarization(classpath, train_wav_file, gmm_name)
    train_init(classpath, ubm, train_wav_file, gmm_name)
    gmm_path=train_map(classpath,train_wav_file, gmm_name)
    garbage(train_wav_file)
    return gmm_path

def build_model (entity_id, classpath, ubm, orig, start, duration, train_wav_file, name_surname, token):
    gmm_name=name_surname[0]+name_surname[1]

    gmm_path=Main(classpath, ubm,  orig, start, duration, train_wav_file, gmm_name)
    create_model(entity_id,"audio",gmm_name,gmm_path)
    return gmm_path

if __name__ == '__main__':
    classpath="lium_spkdiarization-8.4.1.jar"
    ubm="/home/active/active/active_platform/data/models/audio/globals/ubm.gmm"
    train_wav_file=None
    name_surname=["Emanuele","Prova"]
    #orig="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/wav/SandroLombardi##gep_01.wav"
    orig="EmanueleDessiTrain.wav"
    start=0
    duration=None
    dest="/home/active/active/active_platform/job_processor/plugins_script/speaker_extractor/var/prova.wav"
    if duration==None:
        duration=get_wave_duration(orig)
    build_model (classpath, ubm, orig, start, duration, train_wav_file, name_surname)
    exit()
    Main(classpath, ubm,  orig, start, duration, train_wav_file, gmm_name)

    exit()
    classpath="/Users/labcontenuti/Documents/workspace/AudioActive/84/lium_spkdiarization-8.4.1.jar"
    ubm="/Users/labcontenuti/Documents/workspace/AudioActive/84/ubm.gmm"
    orig="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/wav/SandroLombardi##gep_01.wav"
   
    
 
    exit()
    #write_in_srt("/Users/labcontenuti/Music/facciamo_i_conti_internet.wav_shelve.db")    
    #write_in_yuml("/Users/labcontenuti/Music/facciamo_i_conti_internet.wav_shelve.db")    
    #seg2srt("/Users/labcontenuti/Documents/workspace/AudioActive/84/littizzetto_salvini/littizzetto_salvini.s.seg")
    orig="/Users/labcontenuti/Music/FacciamoIConti_GiacomoMameli-1minuto-prove.wav"
    start=345
    duration=123
    dest=None
    split_audio_file(orig, start, duration, dest)
    concatena(orig, orig)
