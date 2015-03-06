import fnmatch
import os
import shlex
import subprocess
import sys
import shelve
"""Module containing some utilities about subprocess,
threading and file checking."""
import os.path

def _de_humanize(tm):
    
    print "tm ",tm
    tms=tm.split(",")
    msec= float(tms[1])/1000
    hms=tms[0].split(":")
    h=float(hms[0])*60
    m=float(hms[1])*60
    s=float(hms[2])
    return str(int(msec+h+m+s))

def write_in_srt(file_path):
    if not os.path.exists(file_path):
        print "error in file name"
        exit()
    sdb= shelve.open(file_path)
    f=open(file_path+".srt","w")
    index =1
    srt="\n"
    key=sdb.keys()
    key.sort()
    print key
    order_list=[]
    dict_start={}
    for k in key:
        order_list.append(str(sdb[k][3]))
        dict_start[str(sdb[k][3])]=sdb[k]
    order_list.sort()
    print order_list 
    for k in order_list:
        #print str(index)+"\n"+ sdb[k][3]+" --> "+ sdb[k][2]+"\n"+sdb[k][0]+"\n"
        #srt=srt+str(index)+"\n"+ sdb[k][3]+" --> "+ sdb[k][2]+"\n<i>"+sdb[k][0]+"</i>\n\n"
        srt=srt+str(index)+"\n"+ dict_start[k][3]+" --> "+ dict_start[k][2]+"\n<i>"+dict_start[k][0]+"</i>\n\n"
        print dict_start[k][3]
        index=index+1
    f.write(srt)
    f.close()
    
def write_in_yuml(file_path):
    if not os.path.exists(file_path):
        print "error in file name"
        exit()
    sdb= shelve.open(file_path)
    f=open(file_path+".yaml","w")
    yuml="\n"
    key=sdb.keys()
    key.sort()
    print key
    order_list=[]
    dict_start={}
    for k in key:
        order_list.append(str(sdb[k][3]))
        dict_start[str(sdb[k][3])]=sdb[k]
    order_list.sort()
    print order_list 
    for k in order_list:
        #yuml=yuml+"\n"+ "- ann_tag:"+sdb[k][0]+"\n   segment_duration:"+ sdb[k][1]+"\n   segment_end:"+ sdb[k][2]+"\n   segment_start:"+ sdb[k][3]
        yuml=yuml+"\n"+ "- ann_tag:"+dict_start[k][0]+"\n   segment_duration:"+ dict_start[k][1]+"\n   segment_end:"+ dict_start[k][2]+"\n   segment_start:"+ _de_humanize(dict_start[k][3])
    f.write(yuml)
    f.close()


def alive_threads(t_dict):
    """Check how much threads are running and alive in a thread dictionary

    :type t: dictionary
    :param t: thread dictionary like  { key : thread_obj, ... }"""
    num = 0
    for thr in t_dict:
        if t_dict[thr].is_alive():
            num += 1
    return num

"""
def start_subprocess(commandline):

    if sys.platform == 'win32':
        commandline = commandline.replace('\\','\\\\')
        
        args = shlex.split(commandline)
        startupinfo = subprocess.STARTUPINFO()
        #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(args, stdin=CONFIGURATION.output_redirect,
                             stdout=CONFIGURATION.output_redirect,
                             stderr=CONFIGURATION.output_redirect, startupinfo=startupinfo)
    else:
        print "UTILS -- commandline ",  commandline
        args = shlex.split(commandline)
#         print commandline
        proc = subprocess.Popen(args, stdin=CONFIGURATION.output_redirect,
                             stdout=CONFIGURATION.output_redirect,
                             stderr=CONFIGURATION.output_redirect)
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

"""
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

if __name__ == '__main__':
    write_in_srt("/Users/labcontenuti/Movies/fic.02/fic_02.wav_shelve.db")    
    write_in_yuml("/Users/labcontenuti/Movies/fic.02/fic_02.wav_shelve.db")    
        