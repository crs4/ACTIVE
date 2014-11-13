#from face_extractor import FaceModels as FM
import cv2
import os
import sys
import numpy as np
import shutil
from Constants import *
from face_detection import get_cropped_face, get_cropped_face_using_fixed_eye_pos, get_detected_cropped_face
from train_by_captions import train_by_captions
from Utils import load_YAML_file, save_model_file, save_YAML_file

class FaceModelsLBP():
    '''
    The persistent data structure containing the face models used by the 
    face recognition algorithm and replicated on each worker.
    This class ensures that the face models are replicated and updated on each worker.
    '''
    def __init__(self, force_db_creation = False, video_path = None, workers=None):
        '''
        Initialize the face models on all workers.

        :type force_db_creation: boolean
        :param force_db_creation: if true, db is always created
        
        :type  workers: list of strings
        :param workers: the address (IP and port) of workers.
        '''
        self._tags={}
        self.model=None

        if(USE_CAPTIONS):
            
            if(video_path):
                
                self._dbpath = video_path
                
                file_name, file_ext = os.path.splitext(video_path)
                
                self._db_name = file_name + '-DB'
                
            else:
                
                print 'No video path was provided'
        else:       
            self._dbpath=DB_PATH
            self._db_name=DB_NAME

        if(force_db_creation):
            self.create(video_path)
        else:
            ok = False
            if(USE_ONE_FILE_FOR_FACE_MODELS):
                # Try to load db
                ok = self.load(None)
   
            else: 
                
                ok = self.load_tags(None)
                  
            # If loading was not successful, create it
            if(not(ok)):
                self.create(video_path) 
            
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
        
    def get_tag(self, index):
        '''
        Get tag string given numeric index

        :type index: int
        :param index: index of tag
        '''
        try:
            if not self._tags==None:
                return self._tags[index]
            return -1
        except:
            return -1
            
    def get_tags(self):
        '''
        Get all tags as list of strings
        '''
        try:
            if not self._tags == None:
                return self._tags.values()
            return - 1
        except:
            return -1

    def get_people_nr(self):
        '''
        Get number of people in face model
        '''
        try:
            if not self._tags==None:
                return len(self._tags)
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
        
    def load(self, db_file_name):
        '''
        Update the face models data structure on all workers from a file.
        
        :type  file_name: string
        :param file_name: the name of the file containing the dump of the face models data structure
        '''
        if db_file_name==None:
            '''
            Set the name of database.
            Algorithm : 
            LBP (Local Binary Pattern)
            '''  
            db_file_name=self._db_name+"-LBP"

        tags_file_name = db_file_name + "-Tags"
        
        model=cv2.createLBPHFaceRecognizer()
        ok = False;
        
        if(os.path.isfile(db_file_name) and (os.path.isfile(tags_file_name))):
            
            if(not((USE_TRACKING or SIM_TRACKING or USE_SLIDING_WINDOW)
            and LOAD_IND_FRAMES_RESULTS)):          
            
                model.load(db_file_name)
                
            if(not(model == None)):
                self.model=model
                self._tags = load_YAML_file(tags_file_name)
                ok = True
                print('\n### DB LOADED ###\n')

        return ok;
        
    def load_tags(self, db_file_name):
        '''
        Load tags from a file.
        
        :type  file_name: string
        :param file_name: the root name of the file containing the tags
        '''
        if db_file_name==None:
            '''
            Set the name of database.
            Algorithm : 
            LBP (Local Binary Pattern)
            '''  
            db_file_name = self._db_name

        tags_file_name = self._db_name+"-LBP-Tags"
        
        ok = False;
        
        if(os.path.isfile(tags_file_name)):

            self._tags = load_YAML_file(tags_file_name)
            ok = True
            print('\n### TAGS LOADED ###\n')
    
        return ok;  
        
    def load_model(self, db_file_name):
        '''
        Update the face models data structure for a single person on all workers from a file.
        
        :type  file_name: string
        :param file_name: the name of the file containing the dump of the face models data structure
        '''
        
        ok = False
        
        if db_file_name==None:
            
            print "No db file was provided"
        
        else:
        
            model=cv2.createLBPHFaceRecognizer()
                    
            if(os.path.isfile(db_file_name)):
                model.load(db_file_name)
                if(not(model == None)):
                    self.model=model
                    ok = True

        return ok;    
    
    def create(self, video_path = None, db_file_name = None):
        print('\n### CREATING DB ####\n')
        #print "CREATE self._dbpath", self._dbpath

        model = None

        if(USE_CAPTIONS):
            
            db_file_name=self._db_name+"-LBP"
            [model, tags] = train_by_captions(video_path, db_file_name)
            self.model = model
            self._tags = tags
            
        else:

            start_time = cv2.getTickCount();
            
            if(db_file_name == None):
                
                db_file_name=self._db_name+"-LBP"
                
            sz = None;
            if(USE_RESIZING):
                sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)
                
            [X,y] = self.__read_images(self._dbpath, sz)
            
            if(len(self._tags) > 0):
                
                if(USE_ONE_FILE_FOR_FACE_MODELS):
                
                    model=cv2.createLBPHFaceRecognizer(
                    LBP_RADIUS, 
                    LBP_NEIGHBORS, 
                    LBP_GRID_X, 
                    LBP_GRID_Y)
                    model.train(np.asarray(X), np.asarray(y))
                    model.save(db_file_name)
                    self.model=model
                        
                # Save tags in YAML file
                save_YAML_file(db_file_name + "-Tags",self._tags) 
        
                time_in_clocks = cv2.getTickCount() - start_time;
                time_in_seconds = time_in_clocks / cv2.getTickFrequency();
        
                print('Creation time: ' + str(time_in_seconds) + ' s\n');
             
            else:
                
                print "No model was created"
        
        return model
    
    def clear(self): 
        pass
    
    def __read_images(self, path, sz=None):
        """Reads the images in a given folder, resizes images on the fly if size is given.

        Args:
            path: Path to a folder with subfolders representing the subjects (persons).
            sz: A tuple with the size Resizes

        Returns:
            A list [X,y]

                X: The images, which is a Python list of numpy arrays.
                y: The corresponding labels (the unique number of the subject, person) in a Python list.
        """
        c = 0
        X,y = [], []
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                print "creating model for", subdirname
                subject_path = os.path.join(dirname, subdirname)
                #print "subject path:", subject_path
                for filename in os.listdir(subject_path):
                    #print "image path", os.path.join(subject_path, filename)
                    try:
                        if(USE_EYES_POSITION):
                            if(USE_EYE_DETECTION):
                                im = None
                                crop_result = get_cropped_face(os.path.join(subject_path, filename), offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y), dest_size = sz, return_always_face = False)
                                if(crop_result):
                                    im = crop_result[FACE_KEY]
                                
                            else:
                                im = get_cropped_face_using_fixed_eye_pos(os.path.join(subject_path, filename), offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y), dest_size = sz)
                
                        else:
                            if(USE_FACE_DETECTION_IN_TRAINING):
                                im = get_detected_cropped_face(os.path.join(subject_path, filename), return_always_face = False)
##                                if(not(im == None)):
##                                    cv2.namedWindow('Training image', cv2.WINDOW_AUTOSIZE);
##                                    cv2.imshow('Training image', im);
##                                    cv2.waitKey(0);
                            else:   
                                im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                                #resize to given size (if given)
                                if ((im is not None) and (sz is not None)):
                                    im = cv2.resize(im, sz)
##                                if(not(im == None)):
##                                    cv2.namedWindow('Training image', cv2.WINDOW_AUTOSIZE);
##                                    cv2.imshow('Training image', im);
##                                    cv2.waitKey(0);
                        if(im):
                            
                            if(USE_BLACK_PELS):
                                
                                im_width = im.size_column;
                                im_height = im_size_row;
                                # Divide image by using a 4 x 4 grid
                                for im_x in range(0, im_width - 1):
                                    for im_y in range(0, im_height - 1):
                                        if(((im_x < 50) and (im_y >= 50) and (im_y < 150)) or ((im_x >= 150) and (im_y >= 50) and (im_y < 150))):
                                            im[im_x,im_y] = 0
                                            
                                #cv2.imshow(im, "face")
                                #cv2.waitKey(0)
                                                            
                            X.append(np.asarray(im, dtype=np.uint8))
                            y.append(c)
                            self._tags[c]=str(subdirname)
                            
                            if(USE_MIRRORED_FACES_IN_TRAINING):
                                c = c + 1
                                # Add mirrored image
                                mirrored_im = cv2.flip(im,1);
                                X.appen(np.asarry(flipped_im, dtype=np.uint8))
                                y.append(c)
                                self._tags[c] = str(subdirname)
                                
                        else:
                            print "Image", os.path.join(subject_path, filename), "not considered" 
                            
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                
                if(not(USE_ONE_FILE_FOR_FACE_MODELS)):
                    
                    save_model_file(X,y)
                    X,y = [], []
                
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
