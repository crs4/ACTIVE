#from face_extractor import FaceModels as FM
import cv2
import os
import sys
import numpy as np
from Constants import *
import shutil
class FaceModelsLBP():
    '''
    The persistent data structure containing the face models used by the 
    face recognition algorithm and replicated on each worker.
    This class ensures that the face models are replicated and updated on each worker.
    '''
    def __init__(self, workers=None):
        '''
        Initialize the face models on all workers.

        :type  workers: list of strings
        :param workers: the address (IP and port) of workers.
        '''
        self._labels={}
        
        self._dbpath=DB_PATH
        self._db_name=os.path.join(self._dbpath).split(os.path.sep)[-1]
    '''
    Set the name of database.
    Algorithm : 
    LBP (Local Binary Pattern)
    '''    
            
    def add_faces(self, filenames_or_images, tag):
        '''
        Add new faces to the face models and associate them with the given tag.
        No check is done on invalid or duplicated faces (it is resposibility of the caller to provide valid faces).
        This method is asynchronous and is propagated to all workers.

        :type  filenames_or_images: an Image object, or a string, or a list of Image objects, or a list of strings
        :param filenames_or_images: faces to be added to the face models data structure

        :type  tag: string
        :param tag: the tag associated to the face to be added to the face models data structure
        '''
        if not filenames_or_images==None:
            if not os.path.exists(self._dbpath+"/"+tag):
                os.makedirs(self._dbpath+"/"+tag)
        if type(filenames_or_images) is str:
            print "string"
        
    def  get_label(self, index):
        try:
            if not self._labels==None:
                return self._labels[index]
            return -1
        except:
            return -1
        
    def remove_tags(self, tags):
        '''
        Remove the given tag or tags (and all associated faces) from the face models data structure.
        If any of the provided tags is not in the face models data structure, the tag is ignored.
        This method is asynchronous and is propagated to all workers.

        :type  tags: string or list of strings
        :param tags: the tags associated to the face to be added to the face models data structure
        '''
        print "tags ",  tags 
        for tag in tags: 
            if os.path.exists(self._dbpath+"/"+tag): 
                print "removing ",  self._dbpath+"/"+tag
                shutil.rmtree(self._dbpath+"/"+tag)
        self.create()
        return True
        
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
        pass

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
        if file_name==None:
            file_name=self._db_name+"-LBP"
        model=cv2.createLBPHFaceRecognizer()
        model.load(file_name)
        return model
    
    def create(self):
        
        [X,y] = self.__read_images(self._dbpath, None)
        model=cv2.createLBPHFaceRecognizer()
        model.train(np.asarray(X), np.asarray(y))
        model.save(self._db_name+"-LBP")
        return model
    
    def clear(self): 
        pass
    
    def __read_images(self, path, sz=None):
        c = 0
        X,y = [], []
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    try:
                        im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                        # resize to given size (if given)
                        if (sz is not None):
                            im = cv2.resize(im, sz)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                        self._labels[c]=str( subdirname)
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                c = c+1
        return [X,y]

    def read_images(self, path, sz=None):
        self.__read_images(path, sz)
if __name__ == '__main__':
    """
    fml=FaceModelsLBP()
    #shutil.copytree(fml._dbpath+"/s1", fml._dbpath+"/s1bis")   
    fml.remove_tags(["s1bis"])
    print "fml._dbpath ",fml._dbpath
    """
    pass
