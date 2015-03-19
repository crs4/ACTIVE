import cv2
import cv2.cv as cv
import numpy as np
import os
import shutil
import uuid
from Constants import *
from Utils import get_image_score, load_YAML_file, save_model_file, save_YAML_file

class FaceModels():
    '''
    The persistent data structure containing the global face models 
    used by the face recognition algorithm
    '''
    
    def __init__(self, params = None):
        '''
        Initialize the face models
        
        :type params: dictionary
        :param params: configuration parameters 
        '''
        
        self._params = params   
        self._algorithm = FACE_MODEL_ALGORITHM
        self._data_dir_path = GLOBAL_FACE_REC_DATA_DIR_PATH

        # Differences between images
        self._all_diffs = {}
        
        # Minimum difference between images
        self._all_min_diffs = {}

        # Association between tags 
        # Differences between images of current subject
        self._current_diffs = {}
        # Array with good images of current subject 
        self._current_X = []
        
        # Images already inserted in model for current subject
        self._current_images = []
        
        if(params is not None):
            
            if(FACE_MODEL_ALGORITHM_KEY in params):
                self._algorithm = params[FACE_MODEL_ALGORITHM_KEY]
            
            if(GLOBAL_FACE_REC_DATA_DIR_PATH_KEY in params):
                self._data_dir_path = params[GLOBAL_FACE_REC_DATA_DIR_PATH_KEY]
                
        # Try to load tags
        #ok = self.load_tags()
        
        # If loading was not successful, create models?
        #if(not(ok)):
        #    pass
            
            
    def getTags(self):
        '''
        Get all tags as list of strings
        '''
        pass
        

    def getPeopleNr(self):
        '''
        Get number of people in face model
        '''
        pass
      
    
    def insertFace(self, im_path, tag):
        '''
        Add face to model.
        Check that face is sufficiently different
        from other faces already in model.
        
        :type im_path: string
        :param im_path: path of image to be added
        
        :type tag: string
        :param tag: tag of subject for whom image is being added
        
        :return: True if face is good
        :rtype: boolean
        '''
        
        print('im_path', im_path)
        
        # True if face is considered for model
        ok = False
        
        min_diff = GLOBAL_FACE_MODELS_MIN_DIFF
        
        # Directory with discarded image
        disc_dir_path = os.path.join(
        self._data_dir_path, GLOBAL_FACE_REC_DISC_IMAGES_DIR)
        
        subject_disc_dir_path = os.path.join(disc_dir_path, tag)
        
        if((self._params is not None) and 
        (GLOBAL_FACE_MODELS_MIN_DIFF_KEY in self._params)):
                
            min_diff = self._params[GLOBAL_FACE_MODELS_MIN_DIFF_KEY]
        
        im_score = 0
        
        X, y = [], []

        try:
        
            im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
            
            im_score = get_image_score(im)
            
            # Get name of image file
            file_name = os.path.basename(im_path)
            
            # Get extension of image file
            ext = os.path.splitext(im_path)[1]
            
            #X.append(np.asarray(im, dtype = np.uint8))
            X.append(np.asarray(im, dtype=np.uint8))
            y.append(0)
            
            radius = LBP_RADIUS
            neighbors = LBP_NEIGHBORS
            grid_x = LBP_GRID_X
            grid_y = LBP_GRID_Y
            
            if(self._params is not None):

                if(LBP_RADIUS_KEY in self._params):
                    
                    radius = self._params[LBP_RADIUS_KEY]
                    
                if(LBP_NEIGHBORS_KEY in self._params):
                    
                    neighbors = self._params[LBP_NEIGHBORS_KEY]
                    
                if(LBP_GRID_X_KEY in self._params):
                
                    grid_x = self._params[LBP_GRID_X_KEY]
                    
                if(LBP_GRID_Y_KEY in self._params):
                
                    grid_y = self._params[LBP_GRID_Y_KEY]
            
            model=cv2.createLBPHFaceRecognizer(
            radius,
            neighbors,
            grid_x,
            grid_y)         
            
            model.train(np.asarray(X), np.asarray(y))
 
            hists = model.getMatVector("histograms")
            
            hist = hists[0][0]
            
            image_dict = {}
            
            # Check if face is too similar 
            # to other face already in model
            
            good_face = True
            new_minimum = False
            
            diffs_dict = {}
            
            # Minimum difference between pair of images
            # in current model
            min_pair_diff = sys.maxint
            
            if((tag in self._all_min_diffs) and
            (DIFF_KEY in self._all_min_diffs[tag])):
                
                #print('all_min_diffs', self._all_min_diffs)
            
                min_pair_diff = self._all_min_diffs[tag][DIFF_KEY]
            
            min_diff_dict = {}
            
            for subj_image in self._current_images:
                
                subj_hist = subj_image[HIST_KEY]    
                subj_file_name = subj_image[IMAGE_NAME_KEY]
                
                diff = cv2.compareHist(
                hist, subj_hist, cv.CV_COMP_CHISQR)
                
                diffs_dict[subj_file_name] = diff
                
                if(diff < min_diff):
                    # Move image file 
                    # to directory with discarded images
                    
                    # Create unique file path
                    new_im_name = str(uuid.uuid4()) + '.' + ext
        
                    new_im_path = os.path.join(
                    subject_disc_dir_path, new_im_name) 
                    
                    #print('diff', diff)
                    #print('new_im_path', new_im_path)
                        
                    if(not(os.path.exists(subject_disc_dir_path))):
                
                        # Create directory of discarded images 
                        # for this subject
                        os.makedirs(subject_disc_dir_path) 
                        
                    shutil.move(im_path, new_im_path)
                    
                    raw_input('Aspetta poco poco ...')
                    
                    good_face = False
                    
                    break
                    
                else:
                    
                    if(diff < min_pair_diff):

                        min_diff_dict[IMAGE_1_KEY] = file_name
                        min_diff_dict[IMAGE_2_KEY] = subj_file_name
                        min_diff_dict[DIFF_KEY] = diff  
                        
                        new_minimum = True        
                        
            if((len(self._current_images) == 0) or
            ((len(self._current_images) > 0) and (good_face))):
                        
                image_dict[HIST_KEY] = hist
                image_dict[IMAGE_NAME_KEY] = file_name
                image_dict[IMAGE_PATH_KEY] = im_path
                image_dict[IMAGE_SCORE_KEY] = im_score
                
                self._current_diffs[file_name] = diffs_dict
                
                if(new_minimum):
                    # Update minimum difference
                    self._all_min_diffs[tag] = min_diff_dict
                
                self._current_images.append(image_dict)
                self._current_X.append(np.asarray(im, dtype=np.uint8))
                
                #print('image_dict', image_dict)
                
                ok = True
                        
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
        return ok
        

    def clearDiscImages(self):
        '''
        Delete directory with discarded images
        '''
        # Directory with discarded image
        disc_dir_path = os.path.join(
        self._data_dir_path, GLOBAL_FACE_REC_DISC_IMAGES_DIR)
        if(os.path.exists(disc_dir_path)):
                
            shutil.rmtree(disc_dir_path)


    def createModel(self, subject_path, tag):
        '''
        Create single face model
        
        :type subject_path: string
        :param subject_path: path of directory with face images 
                             for this person
        
        :type tag: string
        :param tag: identifier of face model
        '''
            
        file_counter = 0
        
        max_faces_in_model = MAX_FACES_IN_MODEL
        
        self._current_images = []
        self._current_diffs = {}
        #self._current_X = []
        
        if(self._params is not None):
            
            if(MAX_FACES_IN_MODEL_KEY in self._params):  
                
                max_faces_in_model = self._params[MAX_FACES_IN_MODEL_KEY]
            
        # Add new images one by one
        # If there are too much images in the face model,
        # check which are the two most similar images 
        # and delete the image among the two that is less simmetric.
        for filename in os.listdir(subject_path):
            
            try:
            
                file_path = os.path.join(subject_path, filename)
    
                if(file_counter >= max_faces_in_model):
                    
                    # Add new image or 
                    # replace one image already in the training set
                    ok = self.insertFace(file_path, tag)
                    
                    if(ok):
                        
                        self.deleteWorstFace(tag)
                    
                else:
                    
                    # Add new image
                    ok = self.insertFace(file_path, tag)  
                    
                    if(ok):
                        
                        file_counter = file_counter + 1                      
                    
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
                    
        #print('current diffs', self._current_diffs)
            
    
    def createModels(self):
        '''
        Read images in training set folder and create model files
        Training set folder contains one subfolder for each person
        '''
        
        training_set_dir_path = os.path.join(
        self._data_dir_path, GLOBAL_FACE_REC_TRAINING_SET_DIR)
        
        model_dir_path = os.path.join(
        self._data_dir_path, GLOBAL_FACE_REC_MODELS_DIR)
        
        # Delete and re-create directory
        if(os.path.exists(model_dir_path)):
            
            shutil.rmtree(model_dir_path)
            
        os.makedirs(model_dir_path)
        
        self._all_diffs = {}
        self._all_min_diffs = {}
        
        model_counter = 0
        for sub_dir_name in os.listdir(training_set_dir_path):
            
            subject_path = os.path.join(
            training_set_dir_path, sub_dir_name)
            
            self.createModel(subject_path, sub_dir_name)
            
            self._all_diffs[sub_dir_name] = self._current_diffs
            
            # Train model with good images
            
            radius = LBP_RADIUS
            neighbors = LBP_NEIGHBORS
            grid_x = LBP_GRID_X
            grid_y = LBP_GRID_Y
            
            if(self._params is not None):

                if(LBP_RADIUS_KEY in self._params):
                    radius = params[LBP_RADIUS_KEY]
                
                if(LBP_NEIGHBORS_KEY in self._params):
                    neighbors = params[LBP_NEIGHBORS_KEY]
                    
                if(LBP_GRID_X_KEY in self._params):
                    grid_x = params[LBP_GRID_X_KEY]
                    
                if(LBP_GRID_Y_KEY in self._params):
                    grid_y = params[LBP_GRID_Y_KEY]
            
            model=cv2.createLBPHFaceRecognizer(
            radius,
            neighbors,
            grid_x,
            grid_y)
        
            y = [0] * len(self._current_X)
        
            model.train(np.asarray(self._current_X), np.asarray(y))
            
            # Save model file 
            
            model_path = os.path.join(model_dir_path, sub_dir_name)
            
            model.save(model_path)
            
            model_counter = model_counter + 1
            
        #diffs_file_path = os.path.join(
        #self._data_dir_path, GLOBAL_FACE_REC_DIFFS_FILE)
        
        #save_YAML_file(diffs_file_path, self._all_diffs)
        
        # Save minimum differences between images
        min_diffs_file_path = os.path.join(
        self._data_dir_path, GLOBAL_FACE_REC_MIN_DIFFS_FILE)
        
        save_YAML_file(min_diffs_file_path, self._all_min_diffs)
        
    
    def deleteWorstFace(self, tag):
        '''
        Check which are the two most similar images in the face model
        and delete the image among the two that is less simmetric.
        
        :type tag: string
        :param tag: tag of subject for whom image is being deleted        
        '''
        
        if((tag in self._all_min_diffs) and
        (IMAGE_1_KEY in self._all_min_diffs[tag]) and
        (IMAGE_2_KEY in self._all_min_diffs[tag])):
            
            image_1_name = self._all_min_diffs[tag][IMAGE_1_KEY]
            
            image_2_name = self._all_min_diffs[tag][IMAGE_2_KEY]
            
            image_1_score = 0
            image_1_idx = 0
            image_1_path = ''
            image_2_score = 0
            image_2_idx = 0
            image_2_path = ''
            
            image_counter = 0
            rem_images = 2
            for image_dict in self._current_images:
            
                image_name = image_dict[IMAGE_NAME_KEY]
                
                if(image_name == image_1_name):
                    
                    image_1_score = image_dict[IMAGE_SCORE_KEY]
                    image_1_idx = image_counter
                    image_2_path = image_dict[IMAGE_PATH_KEY]
                    rem_images = rem_images - 1
                    
                elif(image_name == image_2_name):
                    
                    image_2_score = image_dict[IMAGE_SCORE_KEY]
                    image_2_idx = image_counter
                    image_2_path = image_dict[IMAGE_PATH_KEY]
                    rem_images = rem_images - 1                 
                    
                if(rem_images == 0):
                    
                    break
                    
                image_counter = image_counter + 1
               
            im_idx = 0
            im_name = ''
            im_path = '' 
               
            if(image_2_score >= image_1_score):
                # Remove image 2
                im_idx = image_2_idx
                im_name = image_2_name
                im_path = image_2_path
            
            else:
                # Remove image 1
                im_idx = image_1_idx
                im_name = image_2_name
                im_path = image_1_path
            
            print('current diffs', self._current_diffs.keys())
            
            # Delete image from lists and dictionaries
            del self._current_images[im_idx]
            del self._current_X[im_idx]
            del self._current_diffs[im_name]

            current_diffs_keys = self._current_diffs.keys()
            
            for key in current_diffs_keys:
                
                if(im_name in self._current_diffs[key]):
                    
                    del self._current_diffs[key][im_name]
                    
            # Update minimum difference
            self.__update_min_diff(tag)
            
            # Move image file 
            # to directory with discarded images
            
            # Directory with discarded image
            disc_dir_path = os.path.join(
            self._data_dir_path, GLOBAL_FACE_REC_DISC_IMAGES_DIR)
            subject_disc_dir_path = os.path.join(disc_dir_path, tag)
            
            # Get extension of image file
            ext = os.path.splitext(im_path)[1]      
                        
            # Create unique file path
            new_im_name = str(uuid.uuid4()) + '.' + ext

            new_im_path = os.path.join(
            subject_disc_dir_path, new_im_name) 
            
            #print('diff', diff)
            #print('new_im_path', new_im_path)
                
            if(not(os.path.exists(subject_disc_dir_path))):
        
                # Create directory of discarded images 
                # for this subject
                os.makedirs(subject_disc_dir_path) 
                
            shutil.move(im_path, new_im_path)   
            
            
    def __update_min_diff(self, tag):
		'''
		Update minimum difference between pair of images for given tag
		
		:type tag: string
        :param tag: tag of subject for whom difference is being updated
        '''
        
        pass
                
