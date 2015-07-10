# -*- coding: utf-8 -*-

import os
import re
import struct

def wave_duration(wavfile):
    """Extract the duration of a wave file in sec.

    :type wavfile: string
    :param wavfile: the wave input file"""
    import wave
    w_file = wave.open(wavfile)
    par = w_file.getparams()
    w_file.close()
    return par[3] / par[2]


def merge_waves(input_waves, wavename):
    """Take a list of waves and append them to a brend new destination wave.

    :type input_waves: list
    :param input_waves: the wave files list

    :type wavename: string
    :param wavename: the output wave file to be generated"""
    #if os.path.exists(wavename):
            #raise Exception("File gmm %s already exist!" % wavename)
    waves = [w_names.replace(" ", "\ ") for w_names in input_waves]
    w_names = " ".join(waves)
    commandline = "sox " + str(w_names) + " " + str(wavename)
    
    utils.start_subprocess(commandline)


def file2wav(filename):
    """Take any kind of video or audio and convert it to a
    "RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit,
    mono 16000 Hz" wave file using gstreamer. If you call it passing a wave it
    checks if in good format, else it converts the wave in the good format.

    :type filename: string
    :param filename: the input audio/video file to convert"""
    name, ext = os.path.splitext(filename)
    if ext == '.wav' and utils.is_good_wave(filename):
        pass
    else:
        if ext == '.wav':
            name += '_'
        print "gst-launch filesrc location='" + filename + "' ! decodebin ! audioresample ! 'audio/x-raw-int,rate=16000' !"+ " audioconvert !"+ " 'audio/x-raw-int,rate=16000,depth=16,signed=true,channels=1' !"+ "wavenc ! filesink location=" + name + ".wav "
        
        utils.start_subprocess("gst-launch filesrc location='" + filename
           + "' ! decodebin ! audioresample ! 'audio/x-raw-int,rate=16000' !"
           + " audioconvert !"
           + " 'audio/x-raw-int,rate=16000,depth=16,signed=true,channels=1' !"
           + "wavenc ! filesink location=" + name + ".wav ")
    utils.ensure_file_exists(name + '.wav')
    return name + ext



#-------------------------------------
#   seg files and trim functions
#-------------------------------------
def seg2trim(filebasename):
    """Take a wave and splits it in small waves in this directory structure
    <file base name>/<cluster>/<cluster>_<start time>.wav

    :type filebasename: string
    :param filebasename: filebasename of the seg and wav input files"""
    segfile = filebasename + '.seg'
    seg = open(segfile, 'r')
    for line in seg.readlines():
        if not line.startswith(";;"):
            arr = line.split()
            clust = arr[7]
            start = float(arr[2]) / 100
            end = float(arr[3]) / 100
            try:
                mydir = os.path.join(filebasename, clust)
                if sys.platform == 'win32':
                    mydir = filebasename +'/'+ clust
                os.makedirs(mydir)
            except os.error, err:
                if err.errno == 17:
                    pass
                else:
                    raise os.error
            wave_path = os.path.join(filebasename, clust,
                                     "%s_%07d.%07d.wav" % (clust, int(start),
                                                           int(end)))
            
            if sys.platform == 'win32':
                wave_path = filebasename +"/"+ clust +"/"+ "%s_%07d.%07d.wav" % (clust, int(start), int(end))
            
            commandline = "sox %s.wav %s trim  %s %s" % (filebasename,
                                                         wave_path,
                                                         start, end)    
                        
            start_subprocess(commandline)
            #ensure_file_exists(wave_path)
    seg.close()

def humanize_time(secs):
    """Convert seconds into time format.

    :type secs: integer
    :param secs: the time in seconds to represent in human readable format
           (hh:mm:ss)"""
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d,%s' % (hours, mins, int(secs), 
                                  str(("%0.3f" % secs))[-3:])

def seg2srt(segfile):
    """Take a seg file and convert it in a subtitle file (srt).

    :type segfile: string
    :param segfile: the segmentation file to convert"""
    def readtime(aline):
        "Help function for sort, to extract time from line"
        return int(aline[2])

    basename = os.path.splitext(segfile)[0]
    seg = open(segfile, 'r')
    lines = []
    for line in seg.readlines():
        if not line.startswith(";;"):
            arr = line.split()
            lines.append(arr)
    seg.close()
    lines.sort(key=readtime, reverse=False)
    fileoutput = basename + ".srt"
    srtfile = open(fileoutput, "w")
    row = 0
    for line in lines:
        row = row + 1
        start = float(line[2]) / 100
        end = start + float(line[3]) / 100
        srtfile.write(str(row) + "\n")
        srtfile.write(humanize_time(start) + " --> "
                      + humanize_time(end) + "\n")
        srtfile.write(line[7] + "\n")
        srtfile.write("\n")
    srtfile.close()
    #utils.ensure_file_exists(basename + '.srt')
def split_seg_file(segfile):
    """Take a seg file and split it.

    :type segfile: string
    :param segfile: the segmentation file to convert"""
    print "************ segfile ", segfile
    index=0
    basename = os.path.splitext(segfile)[0]
    seg = open(segfile, 'r')
    new_seg=None #open(basename+".seg_part"+str(index), 'w')
    lines = []
    for line in seg.readlines():
        if not line.startswith(";;"):
            new_seg.writelines(line)
        else:
            if not new_seg==None:
                new_seg.close()
            index=index+1 
            new_seg=open(basename+".seg_part"+str(index), 'w')
            new_seg.writelines(line)
    seg.close()
    new_seg.close()
    return index

def seg2srt_rename(segfile, identity):
    """Take a seg file and convert it in a subtitle file (srt).

    :type segfile: string
    :param segfile: the segmentation file to convert"""
    def readtime(aline):
        "Help function for sort, to extract time from line"
        return int(aline[2])
    ##creo un identity per prova
    """
    identity={}
    for i in range(100):
        identity["S"+str(i)]="MICHIAMO"+str(i)
    """
    basename = os.path.splitext(segfile)[0]
    seg = open(segfile, 'r')
    lines = []
    for line in seg.readlines():
        if not line.startswith(";;"):
            arr = line.split()
            lines.append(arr)
    seg.close()
    lines.sort(key=readtime, reverse=False)
    fileoutput = basename + ".srt"
    srtfile = open(fileoutput, "w")
    row = 0
    for line in lines:
        row = row + 1
        start = float(line[2]) / 100
        end = start + float(line[3]) / 100
        srtfile.write( str(row) + "\n")
        srtfile.write(humanize_time(start) + " --> "
                      + humanize_time(end) + "\n")
        val=line[7]
        if identity.has_key(line[7]): val= identity[line[7]] 
        srtfile.write(val + "\n")
        srtfile.write("\n")
    srtfile.close()
    
def cluster_name(clufile):
    identity={}
    cluf=open(clufile, 'r')
    lines = []
    for line in cluf.readlines():
        arr=line.split()
        if len(arr)>1:
                for i in range(len(arr)-1):
                    identity[arr[i+1]]=arr[0]
                    print "[arr[i+1]]=arr[0]", arr[i+1]," ", arr[0] 
    return identity
def seg2tag(segfile, clufile):
    """Take a seg file and convert it in a dinamic tag sequence.

    :type segfile: string
    :param segfile: the segmentation file to convert"""
    def readtime(aline):
        "Help function for sort, to extract time from line"
        return int(aline[2])
    identity=cluster_name(clufile)
    print "identity ", identity
    basename = os.path.splitext(segfile)[0]
    seg = open(segfile, 'r')
    lines = []
    for line in seg.readlines():
        if not line.startswith(";;"):
            arr = line.split()
            lines.append(arr)
    seg.close()
    lines.sort(key=readtime, reverse=False)
    fileoutput = basename + ".tag.txt"
    print "se2tag fileoutput " , fileoutput
    srtfile = open(fileoutput, "w")
    row = 0
    for line in lines:
        row = row + 1
        start = float(line[2]) / 100
        duration = float(line[3]) / 100
        val=line[7]
        if identity.has_key(line[7]): val= identity[line[7]] 
        srtfile.write(val +" "+str(start)+" "+str(duration)+"\n")
        srtfile.write("\n")
    srtfile.close()

def ident_seg(filebasename, identifier):
    """Substitute cluster names with speaker names ang generate a
    "<filebasename>.ident.seg" file."""
    ident_seg_rename(filebasename, identifier, filebasename + '.ident')


def ident_seg_rename(filebasename, identifier, outputname):
    """Take a seg file and substitute the clusters with a given name or
    identifier."""
    seg_f = open(filebasename + '.seg', 'r')
    clusters = []
    lines = seg_f.readlines()
    for line in lines:
        for key in line.split():
            if key.startswith('cluster:'):
                clu = key.split(':')[1]
                clusters.append(clu)
    seg_f.close()
    output = open(outputname + '.seg', 'w')
    clusters.reverse()
    for line in lines:
        for clu in clusters:
            line = line.replace(clu, identifier)
        output.write(line)
    output.close()


def srt2subnames(filebasename, key_value):
    """Substitute cluster names with real names in subtitles."""

    def replace_words(text, word_dic):
        """Take a text and replace words that match a key in a dictionary with
        the associated value, return the changed text"""
        rec = re.compile('|'.join(map(re.escape, word_dic)))

        def translate(match):
            "not documented"
            return word_dic[match.group(0)] + '\n'

        return rec.sub(translate, text)

    file_original_subtitle = open(filebasename + ".srt")
    original_subtitle = file_original_subtitle.read()
    file_original_subtitle.close()
    key_value = dict(map(lambda (key, value): (str(key) + "\n", value),
                         key_value.items()))
    text = replace_words(original_subtitle, key_value)
    out_file = filebasename + ".ident.srt"
    # create a output file
    fout = open(out_file, "w")
    fout.write(text)
    fout.close()
    utils.ensure_file_exists(out_file)


def file2trim(filename):
    """Take a video or audio file and converts it into smaller waves according
    to the diarization process.

    :type filename: string
    :param filename: the input file audio/video"""
    if not CONFIGURATION.QUIET_MODE:
        print "*** converting video to wav ***"
    file2wav(filename)
    file_basename = os.path.splitext(filename)[0]
    if not CONFIGURATION.QUIET_MODE:
        print "*** diarization ***"
    diarization(file_basename)
    if not CONFIGURATION.QUIET_MODE:
        print "*** trim ***"
    seg2trim(file_basename)


#--------------------------------------------
#   diarization and voice matching functions
#--------------------------------------------



def _silence_segmentation(filebasename):
    """Make a basic segmentation file for the wave file,
    cutting off the silence."""
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -cp '
            + CONFIGURATION.LIUM_JAR
            + ' fr.lium.spkDiarization.programs.MSegInit '
            + '--fInputMask=%s.wav '
            + '--fInputDesc=audio2sphinx,1:1:0:0:0:0,13,0:0:0'
            + ' --sInputMask= --sOutputMask=%s.s.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.s.seg')


def _gender_detection(filebasename):
    """Build a segmentation file where for every segment is identified
    the gender of the voice."""
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -cp '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MDecode  '
           + '--fInputMask=%s.wav '
           + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,0:0:0 '
           + '--sInputMask=%s.s.seg --sOutputMask=%s.g.seg '
           + '--dPenality=10,10,50 --tInputMask=' + CONFIGURATION.SMS_GMMS
           + ' ' + filebasename)
    utils.ensure_file_exists(filebasename + '.g.seg')
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -cp '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MScore --help  --sGender '
           + '--sByCluster '
           + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:0:0 '
           + '--fInputMask=%s.wav --sInputMask=%s.g.seg --sOutputMask=%s.seg '
           + '--tInputMask=' + CONFIGURATION.GENDER_GMMS + ' ' + filebasename)
    utils.ensure_file_exists(filebasename + '.seg')


def diarization_standard(filebasename):
    """Take a wave file in the correct format and build a segmentation file.
    The seg file shows how much speakers are in the audio and when they talk.

    :type filebasename: string
    :param filebasename: the basename of the wav file to process"""
    print JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -jar '+ CONFIGURATION.LIUM_JAR+ ' fr.lium.spkDiarization.system.Diarization '+ '--fInputMask=%s.wav --sOutputMask=%s.seg --doCEClustering '+ filebasename
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -jar '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.system.Diarization '
           + '--fInputMask=%s.wav --sOutputMask=%s.seg --doCEClustering '
           + filebasename)
    utils.ensure_file_exists(filebasename + '.seg')


def diarization(filebasename, h_par='3', c_par='1.5'):
    """Take a wav and wave file in the correct format and build a
    segmentation file.
    The seg file shows how much speakers are in the audio and when they talk.

    :type filebasename: string
    :param filebasename: the basename of the wav file to process"""
#    par=' --help --trace '
    par = ''
    #generate_uem_seg(filebasename)
    st_fdesc = "audio2sphinx,1:1:0:0:0:0,13,0:0:0"
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MSegInit  '
           + par + ' --fInputMask=%s.wav --fInputDesc='
           + st_fdesc + ' '
           + ' --sOutputMask=%s.i.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.i.seg')

    #Speech/Music/Silence segmentation
    md_fdesk = 'audio2sphinx,1:3:2:0:0:0,13,0:0:0'
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MDecode  '
           + par + '  --fInputMask=%s.wav  --fInputDesc='
           + md_fdesk + ' --sInputMask=%s.i.seg     --tInputMask='
           + CONFIGURATION.SMS_GMMS
           + ' --dPenality=10,10,50  --sOutputMask=%s.pms.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.pms.seg')

    #GLR based segmentation, make small segments
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR + ' fr.lium.spkDiarization.programs.MSeg  '
           + par + ' --fInputMask=%s.wav --fInputDesc=' + st_fdesc
           + '    --sInputMask=%s.i.seg  '
           + ' --kind=FULL --sMethod=GLR --sOutputMask=%s.s.seg '
           + filebasename)
    utils.ensure_file_exists(filebasename + '.s.seg')

    # linear clustering
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MClust ' + par
           + ' --fInputMask=%s.wav --fInputSpeechThr=0.1 --fInputDesc=' + st_fdesc
           + ' --sInputMask=%s.s.seg --cMethod=l --cThr=2 '
           + '--sOutputMask=%s.l.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.l.seg')

    # hierarchical clustering
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MClust ' + par
           + ' --fInputMask=%s.wav --fInputDesc=' + st_fdesc
           + ' --sInputMask=%s.l.seg --cMethod=h --cThr=' + h_par
           + '  --sOutputMask=%s.h.' + h_par + '.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.h.' + h_par + '.seg')

    # initialize GMM
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MTrainInit '
           + par + ' --fInputMask=%s.wav --fInputDesc='
           + st_fdesc + '    --sInputMask=%s.h.' + h_par
           + '.seg --nbComp=8 --kind=DIAG    --tOutputMask=%s.init.gmms '
           + filebasename)
    utils.ensure_file_exists(filebasename + '.init.gmms')

    # EM computation
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MTrainEM ' + par
           + ' --fInputMask=%s.wav --fInputDesc=' + st_fdesc
           + ' --sInputMask=%s.h.' + h_par
           + '.seg --tInputMask=%s.init.gmms --nbComp=8 '
           + '--kind=DIAG --tOutputMask=%s.gmms ' + filebasename)
    utils.ensure_file_exists(filebasename + '.gmms')

    #Viterbi decoding
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MDecode '
           + par + ' --fInputMask=%s.wav  --fInputDesc='
           + st_fdesc + ' --sInputMask=%s.h.' + h_par
           + '.seg  --tInputMask=%s.gmms --dPenality=250'
           + '  --sOutputMask=%s.d.' + h_par + '.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.d.' + h_par + '.seg')

    #Adjust segment boundaries
    s_desc = 'audio2sphinx,1:1:0:0:0:0,13,0:0:0'
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR + ' fr.lium.spkDiarization.tools.SAdjSeg '
           + par + '  --fInputMask=%s.wav  --fInputDesc=' + s_desc
           + '    --sInputMask=%s.d.' + h_par + '.seg   --sOutputMask=%s.adj.'
           + h_par + '.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.adj.' + h_par + '.seg')

    #filter spk segmentation according pms segmentation
    fl_desc = 'audio2sphinx,1:3:2:0:0:0,13,0:0:0'
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR + ' fr.lium.spkDiarization.tools.SFilter '
           + par + '  --fInputMask=%s.wav  --fInputDesc=' + fl_desc
           + '   --sInputMask=%s.adj.' + h_par
           + '.seg  --fltSegMinLenSpeech=150 --fltSegMinLenSil=25 '
           + '--sFilterClusterName=j --fltSegPadding=25 '
           + '--sFilterMask=%s.pms.seg --sOutputMask=%s.flt.'
           + h_par + '.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.flt.' + h_par + '.seg')

    #Split segment longer than 20s
    ss_desc = 'audio2sphinx,1:3:2:0:0:0,13,0:0:0'
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR + ' fr.lium.spkDiarization.tools.SSplitSeg '
           + par + '  --fInputMask=%s.wav  --fInputDesc=' + ss_desc
           + ' --sInputMask=%s.flt.' + h_par + '.seg  --tInputMask='
           + CONFIGURATION.S_GMMS + ' --sFilterMask=%s.pms.seg '
           + '--sFilterClusterName=iS,iT,j  --sOutputMask=%s.spl.' + h_par
           + '.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.spl.' + h_par + '.seg')

    #Set gender and bandwith
    f_desc_clr = "audio2sphinx,1:3:2:0:0:0,13,1:1:300:4"
    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR + ' fr.lium.spkDiarization.programs.MScore '
           + par + ' --fInputMask=%s.wav --fInputDesc=' + f_desc_clr
           + ' --sInputMask=%s.spl.' + h_par + '.seg --tInputMask='
           + CONFIGURATION.GENDER_GMMS
           + ' --sGender --sByCluster --sOutputMask=%s.g.'
           + h_par + '.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.g.' + h_par + '.seg')

    utils.start_subprocess(JAVA_EXE +' -Xmx' + JAVA_MEM + 'm -classpath '
           + CONFIGURATION.LIUM_JAR
           + ' fr.lium.spkDiarization.programs.MClust ' + par
           + ' --fInputMask=%s.wav --fInputDesc=' + f_desc_clr
           + ' --sInputMask=%s.g.' + h_par + '.seg   –fInputSpeechThr=1 --tInputMask='
           + CONFIGURATION.UBM_PATH + ' --cMethod=ce --cThr=' + c_par
           + ' --emCtrl=1,5,0.01 --sTop=5,'
           + CONFIGURATION.UBM_PATH
           + ' --tOutputMask=%s.c.gmm --sOutputMask=%s.seg ' + filebasename)
    utils.ensure_file_exists(filebasename + '.seg')

    if not CONFIGURATION.KEEP_INTERMEDIATE_FILES:
        f_list = ['.i.seg', '.pms.seg', '.s.seg', '.l.seg',
                  '.h.' + h_par + '.seg', '.init.gmms', '.gmms',
                  '.d.' + h_par + '.seg', '.adj.' + h_par + '.seg',
                  '.flt.' + h_par + '.seg', '.spl.' + h_par + '.seg',
                  '.g.' + h_par + '.seg']
        for ext in f_list:
            os.remove(filebasename + ext)


def _train_init(filebasename):
    """Train the initial speaker gmm model."""
    utils.start_subprocess(JAVA_EXE +' -Xmx256m -cp ' + CONFIGURATION.LIUM_JAR
        + ' fr.lium.spkDiarization.programs.MTrainInit '
        + '--sInputMask=%s.ident.seg --fInputMask=%s.wav '
        + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4 '
        + '--emInitMethod=copy --tInputMask=' + CONFIGURATION.UBM_PATH
        + ' --tOutputMask=%s.init.gmm ' + filebasename)
    utils.ensure_file_exists(filebasename + '.init.gmm')


def _train_map(filebasename):
    """Train the speaker model using a MAP adaptation method."""
    utils.start_subprocess(JAVA_EXE +' -Xmx256m -cp ' + CONFIGURATION.LIUM_JAR
        + ' fr.lium.spkDiarization.programs.MTrainMAP --sInputMask=%s.ident.seg'
        + ' --fInputMask=%s.wav '
        + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4 '
        + '--tInputMask=%s.init.gmm --emCtrl=1,5,0.01 --varCtrl=0.01,10.0 '
        + '--tOutputMask=%s.gmm ' + filebasename)
    
    utils.ensure_file_exists(filebasename + '.gmm')


def wav_vs_gmm(filebasename, gmm_file, gender, custom_db_dir=None):
    """Match a wav file and a given gmm model file and produce a segmentation
    file containing the score obtained.

    :type filebasename: string
    :param filebasename: the basename of the wav file to process

    :type gmm_file: string
    :param gmm_file: the path of the gmm file containing the voice model

    :type gender: char
    :param gender: F, M or U, the gender of the voice model

    :type custom_db_dir: None or string
    :param custom_db_dir: the voice models database to use"""
    database = CONFIGURATION.DB_DIR
    
    if custom_db_dir != None:
        database = custom_db_dir
    gmm_name = os.path.split(gmm_file)[1]
    if sys.platform == 'win32':
        utils.start_subprocess(JAVA_EXE +' -Xmx256M -cp ' + CONFIGURATION.LIUM_JAR
        + ' fr.lium.spkDiarization.programs.MScore --sInputMask=%s.seg '
        + '--fInputMask=%s.wav --sOutputMask=%s.ident.' + gender + '.'
        + gmm_name + '.seg --sOutputFormat=seg,UTF8 '
        + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:0:300:4 '
        + '--tInputMask=' + database + '\\' + gender + '\\' + gmm_file
        + ' --sTop=8,' + CONFIGURATION.UBM_PATH
        + '  --sSetLabel=add --sByCluster ' + filebasename)
    else:
        utils.start_subprocess(JAVA_EXE +' -Xmx256M -cp ' + CONFIGURATION.LIUM_JAR
        + ' fr.lium.spkDiarization.programs.MScore --sInputMask=%s.seg '
        + '--fInputMask=%s.wav --sOutputMask=%s.ident.' + gender + '.'
        + gmm_name + '.seg --sOutputFormat=seg,UTF8 '
        + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:0:300:4 '
        + '--tInputMask=' + database + '/' + gender + '/' + gmm_file
        + ' --sTop=8,' + CONFIGURATION.UBM_PATH
        + '  --sSetLabel=add --sByCluster ' + filebasename)
    utils.ensure_file_exists(filebasename + '.ident.'
                             + gender + '.' + gmm_name + '.seg')
    
#     f = open(filebasename + '.ident.'
#                              + gender + '.' + gmm_name + '.seg', "r")
#     print "SEG CREATED "+filebasename + '.ident.' + gender + '.' + gmm_name + '.seg'
#     print f.readlines()
#     f.close() 
#     print "END SEG"



def threshold_tuning():
    """ Get a score to tune up the 
    threshold to define when a speaker is unknown"""
    filebasename = os.path.join(test_path,'mr_arkadin')
    gmm_file = "mrarkadin.gmm"
    gender = 'M'
    utils.ensure_file_exists(filebasename+'.wav')
    utils.ensure_file_exists( os.path.join(test_path,gender,gmm_file ) )
    file2trim(filebasename+'.wav')
    extract_mfcc(filebasename)
    wav_vs_gmm(filebasename, gmm_file, gender,custom_db_dir=test_path)
    clusters = {}
    extract_clusters(filebasename+'.seg',clusters)
    manage_ident(filebasename,gender+'.'+gmm,clusters)
    return clusters['S0'].speakers['mrarkadin']


def segfile_compact_name(file_path):
    result=[]
    res_file=open(file_path+".tag.res.txt", "w")
    with open(file_path+".g.3.tag.txt", "r") as f:
         name=None
         start=None
         dur=None
         
         for line in f:
             print "line ", line
             line_s=line.split()
             if len(line_s)>2:
                 if  name==None:
                     name=line_s[0]
                     start=line_s[1]
                     dur=line_s[2]
                 else:
                     #print "float(start)+float(dur)=", float(start)+float(dur)," float(line_s[1])=",float(line_s[1]), "uguali? ", float(start)+float(dur)==float(line_s[1])
                     if str(float(start)+float(dur))==str(float(line_s[1])) and name==line_s[0]:
                         dur=float(dur)+float(line_s[2])
                         print "**dur ", dur
                     else:
                         #print "name=", name, " start=", start, " dur=", dur
                         res_file.write(name+ "  "+ str(start)+ " "+ str(dur) )
                         result.append([name, start, dur])
                         name=line_s[0]
                         start=line_s[1]
                         dur=line_s[2]
    res_file.write(name+ "  "+ str(start)+ " "+ str(dur) )
    result.append([name, start, dur])
    res_file.close()    
    return result
def make_name_compact(fp):
    cluf=fp+".nomi.txt"
    seg2tag(fp+".g.3.seg",cluf)
    res=segfile_compact_name(fp)
    print "res ", res
    return res
import shutil
def make_propertirs_part(file_properties,basename,num_part):
    file_list=[]
    print "***** basename ", basename, " item ", basename.split("/")[-1]
    imsr="s_inputMaskRoot="+basename+"/out/"+basename.split("/")[-1]+ ".spl.3.seg_part"
    somr="s_outputMaskRoot="+basename+"/out/"+basename.split("/")[-1]+".g.3.seg_part"
    print "**** file_properties ", file_properties
    new_file_properties=file_properties.split(".")[0]
    print "new_file_properties ", new_file_properties
    for i in range(num_part):
        shutil.copy2(file_properties, new_file_properties+"_part"+str(i+1)+".properties")
        f=open(new_file_properties+"_part"+str(i+1)+".properties","a")
        file_list.append(new_file_properties+"_part"+str(i+1)+".properties")
        f.write("\n")
        f.write(imsr+str(i+1))
        f.write("\n")
        f.write(somr+str(i+1))
        f.close()
    print "lista di nuovi file properties ", file_list
    return file_list    
if __name__ == '__main__':
    file_properties="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/FacciamoIConti_GiacomoMameli-1minuto.properties"
    basename="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/FacciamoIConti_GiacomoMameli-1minuto/FacciamoIConti_GiacomoMameli-1minuto"
    fs="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/FacciamoIConti_GiacomoMameli-1minuto/FacciamoIConti_GiacomoMameli-1minuto.spl.3.seg"
    num_part=split_seg_file(fs)
    print num_part
    make_propertirs_part(file_properties, basename, num_part)
    exit()
    """ """
    #fp="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/FacciamoIConti_GiacomoMameli-1minuto/FacciamoIConti_GiacomoMameli-1minuto"
    #fp="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/SandroLombardi##gep_01/SandroLombardi##gep_01"
    #fp="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/SandroLombardi##gep_01-part1/SandroLombardi##gep_01-part1"
    fp="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/Mameli-Lombardi-2minuti/Mameli-Lombardi-2minuti"
    
    make_name_compact(fp)
    print "END"
    exit()
    
    cluf="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/FacciamoIConti_GiacomoMameli-1minuto/FacciamoIConti_GiacomoMameli-1minuto.nomi.txt"
    seg2tag("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/FacciamoIConti_GiacomoMameli-1minuto/FacciamoIConti_GiacomoMameli-1minuto.g.3.seg",cluf)
