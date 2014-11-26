
import sys
sys.path.insert(0,'.')
sys.path.insert(0,'..')
import os
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
from voiceid.utils import humanize_time
import Constant4Audio as C4a
import logging
import time

class VoiceModels(object):
    '''
    The persistent data structure containing the voice models used by the 
    voice recognition algorithm and replicated on each worker.
    This class ensures that the voice models are replicated and updated on each worker.
    '''
    def __init__(self, workers=None):
        '''
        Initialize the face models on all workers.

        :type  workers: list of strings
        :param workers: the address (IP and port) of workers.
        '''       
        self._dbpath=C4a.DB_PATH
        self._db_name=os.path.join(self._dbpath).split(os.path.sep)[-1]
        if C4a.VERBOSE:
            logging.basicConfig(filename= time.asctime().replace(' ','_'),level=logging.INFO)
            logging.info("DB_PATH ", C4a.DB_PATH)
            logging.info("_db_name ", self._db_name)
    def add_voices(self, filenames, tag):
        '''
        Add new voices to the voice models and associate them with the given tag.
        No check is done on invalid or duplicated voices (it is resposibility of the caller to provide valid faces).
        This method is asynchronous and is propagated to all workers.
    
        :type  filenames: a list of strings (path of audio file)
        :param filenames: voices to be added to the face models data structure

        :type  tag: string
        :param tag: the tag associated to the voice to be added to the voice models data structure
        '''
        db = GMMVoiceDB(self._dbpath)    
        for wav in filenames:
            db.add_model(wav, tag)
            if C4a.VERBOSE:
                logging.info("...add voices ", tag)

    def remove_tags(self, tags):
        '''
        Remove the given tag or tags (and all associated voices) from the voice models data structure.
        If any of the provided tags is not in the voice models data structure, the tag is ignored.
        This method is asynchronous and is propagated to all workers.

        :type  tags: string or list of strings
        :param tags: the tags associated to the voice to be removed to the voice models data structure
        '''
        if isinstance(tags,str):
            tags=[tags]
        for dirname, dirnames, filenames in os.walk(self.DB_PATH):
            for filename in filenames:
                if filename.endswith(".gmm"):
                    if filename.endswith(".gmm") in tags:
                        os.remove(os.path.join(dirname, filename))
        
    def rename_tag(self, old_tag, new_tag, blocking=True):
        '''
        Rename a tag in the face models data structure.
        Raise an exception if old_tag does not exist in face models data structure.
        Raise an exception if new_tag already exists in face models data structure.
        This method is asynchronous and is propagated to all workers.

        :type  old_tag: string
        :param old_tag: a tag already present in the face models data structure

        :type  new_tag: string
        :param new_tag: a tag not yet present in the face models data structure
        '''
        return self.facemodel.rename_tag(old_tag, new_tag, blocking)

    def sync(self):
        '''
        Wait until all asynchronous methods previously invoked have been executed by all workers.
        This method shall be called in order to ensure that face models data structure on all workers are aligned.
        '''
        pass
        
    def dump(self):
        '''
        Return a file containig the dump of the face models data structure.
        '''
        pass
        
    def load(self, file_name):
        '''
        Update the face models data structure on all workers from a file.
        
        :type  file_name: string
        :param file_name: the name of the file containing the dump of the face models data structure
        '''
        pass


class VoiceExtractor(object):
    '''
    Tool for detecting and recognizing voices in audio and video.
    '''
    def __init__(self, voice_models=None, params=None):
        '''
        Initialize the voice extractor.
        The configuration parameters define and customize the voice extraction algorithm.
        If any of the configuration parameters is not provided a default value is used.

        :type  voice_models: a VoiceModels object
        :param voice_models: the voice models data structure

        :type  params: dictionary 
        :param params: configuration parameters (see table)
        '''
        self._DB_PATH=C4a.DB_PATH
        if voice_models:
            self._DB_PATH=voice_models
    def extractVoicesFromAudio(self, resource_path, save_as="xml"):
        '''
        Launch the voice extractor on one audio resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        handle=time.asctime().replace(' ','_')
        if save_as=="xml":
            result_file=""
            db = GMMVoiceDB(self._DB_PATH)
            v = Voiceid(db, resource_path)            
            v.extract_speakers()
            for c in v.get_clusters():
                cluster = v.get_cluster(c) 
                result_file=result_file+"\n<cluster><speacker>"+str(cluster.get_best_speaker())+"</speacker>"
                list_seg=cluster.get_segments()
                for seg in list_seg:
                    print "start %s stop %s" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                    result_file=result_file+"<start> %s </start><stop> %s </stop>" %  (humanize_time(float(seg.get_start()) / 100),  humanize_time(float(seg.get_end()) / 100))
                result_file=result_file+"</cluster>"
            file = open(handle+".txt", "w")
            file.write(result_file)
            file.close()
        print "extractVoicesFromAudio FINISHED"
        return handle
    def extractVoicesFromVideo(self, resource):
        '''
        Launch the face extractor on one video resource.
        This method is asynchronous and returns a task handle.

        :type  resource_path: string
        :param resource_path: resource file path
        '''
        pass
        
    def wait(self, handle):
        '''
        Wait until the task associated with the given handle has completed.
        If the handle is invalid, this method is ignored.
        TODO: alternatively, a callback mechanism could be provided

        :type  handle: integer ?
        :param handle: the task handle
        '''
        pass

    def getResults(self, handle):
        '''
        Return the results of the voice extraction process.
        This call invalidates the specified handle.
        If the handle was returned by extractFacesFromImage(), a dictionary 
        is returned with the following entries:
          elapsed_cpu_time:  float  (the elapsed cpu time in sec)
          error: a string specyfing an error condition, or None if no errors occurred
          voices: a list of tags with the init and the end in sec
        Example:
            results = {'elapsed_cpu_time':  0.011,
                       'error': None,
		               'voices': ({'tag': 'Barack Obama', ["1:3", "10:50"], ...},
                                 {'tag': 'Betty White',  ["30:45", "120:250", ...]}
                                )
                      }
        For extractVoicesFromVideo() a dictionary is returned with the following entries:
            TBD  
                   
        :type  handle: integer ?
        :param handle: the task handle
        '''
        pass
    
    def getProgress(self, handle):
        '''
        Return an integer between 0 and 100 indicating the the execution progress of the face extraction task.
            0: queued
            100: completed
            any value between 0 and 100: running
        Raise an exception if an error was encountered during the face extraction.

        :type  handle: integer ?
        :param handle: the task handle
        '''
