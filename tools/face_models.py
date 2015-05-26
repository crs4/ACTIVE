import Constants as c
import cv2
import cv2.cv as cv
import face_detection as fd
import Utils as utils
import numpy as np
import os
import shutil
import sys
import uuid

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
        self._algorithm = c.FACE_MODEL_ALGORITHM
        self._data_dir_path = c.GLOBAL_FACE_REC_DATA_DIR_PATH
        self._models = None

        # Association between tags 
        
        if(params is not None):
            
            if(c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY in params):
                self._data_dir_path = params[c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY]
            
            
    def add_face(self, tag, im_path, aligned_face = None, eye_pos = None, bbox = None):
        '''
        Add face to face models
        
        :type tag: string
        :param tag: tag of person whom face belong to
        
        :type im_path: string
        :param im_path: path of image containing the face
        
        :type aligned_face: OpenCV image
        :param aligned_face: aligned face
        
        :type eye_pos: tuple
        :param eye_pos: tuple containing eye positions 
        (left_eye_x, left_eye_y, right_eye_x, right_eye_y)
        
        :type bbox: tuple
        :param bbox: tuple containing position and size of 
        face bounding box in whole image (x, y, width, height)
        
        :rtype: boolean
        :returns: true if face has been added
        '''
        
        ok = False
        
        try:
        
            # Check if face models are loaded
            if(not(self._models)):
                
                self.load_models()

            # Create unique file name
            im_name = str(uuid.uuid4()) + '.png'
            
            rel_im_path = os.path.join(tag, im_name)
            
            training_set_path = os.path.join(
            self._data_dir_path, c.TRAINING_SET_DIR)  
                
            whole_images_path = os.path.join(
            training_set_path, c.WHOLE_IMAGES_DIR)
            
            whole_images_subject_path = os.path.join(whole_images_path, tag)
            
            whole_im_path = os.path.join(whole_images_path, rel_im_path)
            
            # Save aligned face
            aligned_faces_path = os.path.join(
            training_set_path, c.ALIGNED_FACES_DIR)
            
            aligned_faces_subject_path = os.path.join(aligned_faces_path, tag)
            
            if(not(os.path.exists(aligned_faces_subject_path))):
                
                # Create directory
                os.makedirs(aligned_faces_subject_path)    
    
            aligned_im_path = os.path.join(aligned_faces_subject_path, im_name)
            
            good_image = False
            
            print('im_path', im_path)
            print('eye_pos', eye_pos)
            print('bbox', bbox)
            
            cv2.imshow('aligned_face',aligned_face)
            cv2.waitKey(0)
            
            if((aligned_face is not None) and 
            (eye_pos is not None) and 
            (bbox is not None)):
    
                good_image = True    
            
            else:
                
                print('detecting face in whole image')
                
                # Detect face in whole_image
                align_path = c.ALIGNED_FACES_PATH
                if(self._params and (c.ALIGNED_FACES_PATH_KEY in self._params)):
                    
                    align_path = self._params[c.ALIGNED_FACES_PATH_KEY]
                       
                det_results = fd.detect_faces_in_image(
                im_path, align_path, self._params, False)
                
                if(det_results and (c.FACES_KEY in det_results)):
                    
                    faces = det_results[c.FACES_KEY]
        
                    if((len(faces) == 1) and (c.FACE_KEY in faces[0]) and 
                    (c.BBOX_KEY in faces[0]) and 
                    (c.LEFT_EYE_POS_KEY in faces[0]) and 
                    (c.RIGHT_EYE_POS_KEY in faces[0])):
                        
                        aligned_face = faces[0][c.FACE_KEY]
                        
                        # Equalize face
                        if(c.USE_HIST_EQ_IN_CROPPED_FACES):
                           aligned_face = cv2.equalizeHist(aligned_face) 
                           
                        if(c.USE_NORM_IN_CROPPED_FACES):
                           aligned_face = cv2.normalize(aligned_face, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8UC1)
                
                        if(c.USE_CANNY_IN_CROPPED_FACES):
                           aligned_face = cv2.Canny(aligned_face, 0.1,100)
                           
                        if(c.USE_TAN_AND_TRIGG_NORM):
                           aligned_face = normalize_illumination(aligned_face)
                           
                        # Insert oval mask in image
                        if(c.USE_OVAL_MASK):
                            aligned_face = add_oval_mask(aligned_face)                                                
                        
                        bbox = faces[0][c.BBOX_KEY]
                        
                        eye_left = faces[0][c.LEFT_EYE_POS_KEY]
                        
                        eye_right = faces[0][c.RIGHT_EYE_POS_KEY]
                        
                        eye_pos = (
                        eye_left[0], eye_left[1], eye_right[0], eye_right[1])
                        
                        good_image = True
                
            if(good_image): 
                    
                # Save whole image
                if(not(os.path.exists(whole_images_subject_path))):
                    
                    # Create directory
                    os.makedirs(whole_images_subject_path)                    

                cv2.imwrite(aligned_im_path, aligned_face, [cv2.IMWRITE_PNG_COMPRESSION, 0])            

                new_label = 0
                
                # Check if tag is already in face models
                tags = self.get_tags()
                
                if(tag not in tags):
                    
                    # Load file with tag-label associations
                    tag_label_associations_file = os.path.join(
                    self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
                    tag_label_associations = utils.load_YAML_file(
                    tag_label_associations_file)
                    
                    if(tag_label_associations):
                        
                        # Add new tag with related label
                        
                        labels = tag_label_associations.keys()
                        
                        max_label = max(labels)
                        
                        new_label = max_label + 1
                        
                        tag_label_associations[new_label] = tag
                        
                    else:
                        
                        # Create dictionary with tag-label associations
                        tag_label_associations = {new_label: tag}
                        
                    # Save new dictionary in YAML file
                    utils.save_YAML_file(
                    tag_label_associations_file, tag_label_associations)
                    
                whole_image = cv2.imread(im_path, cv2.IMREAD_COLOR)    
                cv2.imwrite(whole_im_path, whole_image, [cv.CV_IMWRITE_PNG_COMPRESSION, 0])
                
                # TEST ONLY Save whole image with face bbox 
                bbox_images_path = os.path.join(
                training_set_path, c.BBOX_IMAGES_DIR)
                
                bbox_images_subject_path = os.path.join(
                bbox_images_path, tag)
                
                if(not(os.path.exists(bbox_images_subject_path))):
                    
                    # Create directory
                    os.makedirs(bbox_images_subject_path)            
                
                bbox_im_path = os.path.join(bbox_images_path, rel_im_path)
                
                x0 = bbox[0]
                x1 = x0 + bbox[2]
                y0 = bbox[1]
                y1 = y0 + bbox[3]
                
                cv2.rectangle(whole_image, (x0,y0), (x1, y1), (0,0,255), 3, 8, 0)
                cv2.imwrite(bbox_im_path, whole_image, [cv.CV_IMWRITE_PNG_COMPRESSION, 0])
                
                face_in_models = False
                
                if(self._models):
                    
                    print('self._models', self._models)
                    
                    # Update models
                    
                    min_diff = c.GLOBAL_FACE_MODELS_MIN_DIFF
                    
                    if(self._params and 
                    (c.GLOBAL_FACE_MODELS_MIN_DIFF in self._params)):
                    
                        min_diff = self._params[c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY]
                    
                    if(min_diff > 0):
                        # Check if face is sufficiently different
                        # from other faces in models
                        (label, conf) = self._models.predict(
                        np.asarray(aligned_face, dtype = np.uint8)) 
                        
                        if(conf >= min_diff):
                            
                            self._models.update(
                            np.asarray([np.asarray(aligned_face, dtype=np.uint8)]), 
                            np.asarray(new_label))
                            
                            face_in_models = True  
                            
                    else:
                        
                        self._models.update(
                        np.asarray([np.asarray(aligned_face, dtype=np.uint8)]), 
                        np.asarray(new_label))  
                        
                        face_in_models = True                  
                    
                else:

                    # Create models
                    
                    # Create face recognizer
                    radius = c.LBP_RADIUS
                    neighbors = c.LBP_NEIGHBORS
                    grid_x = c.LBP_GRID_X
                    grid_y = c.LBP_GRID_Y
                    min_diff = c.GLOBAL_FACE_MODELS_MIN_DIFF
                    
                    if(self._params is not None):
            
                        if(c.LBP_RADIUS_KEY in self._params):
                            radius = self._params[c.LBP_RADIUS_KEY]
                        
                        if(c.LBP_NEIGHBORS_KEY in self._params):
                            neighbors = self._params[c.LBP_NEIGHBORS_KEY]
                            
                        if(c.LBP_GRID_X_KEY in self._params):
                            grid_x = self._params[c.LBP_GRID_X_KEY]
                            
                        if(c.LBP_GRID_Y_KEY in self._params):
                            grid_y = self._params[c.LBP_GRID_Y_KEY]
                               
                    model=cv2.createLBPHFaceRecognizer(
                    radius,
                    neighbors,
                    grid_x,
                    grid_y) 
                 
                    model.train(
                    np.asarray([np.asarray(aligned_face, dtype=np.uint8)]), 
                    np.asarray(new_label))
                    
                    face_in_models = True  
                  
                    # Save file with face models   
                    db_file_name = os.path.join(
                    self._data_dir_path, c.FACE_MODELS_FILE)  
                        
                    model.save(db_file_name)
                    
                    self._models = model
                    
                # Load file with faces
                faces_file = os.path.join(
                self._data_dir_path, c.FACES_FILE)
                faces_dict = utils.load_YAML_file(faces_file)
                if(faces_dict is None):
                    
                    # Create dictionary with association between 
                    # image and related bbox and eye positions
                    faces_dict = {rel_im_path: {}}
                    
                # Save face bbox and eye positions    
                    
                faces_dict[rel_im_path] = {}
                
                faces_dict[rel_im_path][c.BBOX_KEY] = bbox
                
                eye_left = (eye_pos[0], eye_pos[1])
    
                eye_right = (eye_pos[2], eye_pos[3])
                
                faces_dict[rel_im_path][c.LEFT_EYE_POS_KEY] = eye_left
                
                faces_dict[rel_im_path][c.LEFT_EYE_POS_KEY] = eye_right
                
                faces_dict[rel_im_path][c.FACE_IN_MODELS_KEY] = face_in_models                
                
                # Save new dictionary in YAML file
                utils.save_YAML_file(faces_file, faces_dict)        
                                
                ok = True
                
        except IOError, (errno, strerror):
            
            print "I/O error({0}): {1}".format(errno, strerror)
            
        except:
            
            print "Unexpected error:", sys.exc_info()[0]
            
            raise
                            
        return ok
                    
    
    def get_tag(self, label):
        '''
        Get tag corresponding to given label
        
        :type label: integer
        :param label: label for which corresponing tag is wanted
        
        :rtype: string
        :returns: tag correspoding to given label
        '''
        
        tag = c.UNDEFINED_TAG
        
        # Load file with tag-label associations
        tag_label_associations_file = os.path.join(
        self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        tag_label_associations = utils.load_YAML_file(
        tag_label_associations_file)
        
        if(tag_label_associations and 
        (label in tag_label_associations)):
            
            tag = tag_label_associations[label]
            
        return tag
            
    
    def get_tags(self):
        '''
        Get all tags
        
        :rtype: set
        :returns: a set containing all tags
        '''
        
        tags = []
        
        # Load file with tag-label associations
        tag_label_associations_file = os.path.join(
        self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        tag_label_associations = utils.load_YAML_file(
        tag_label_associations_file,)
        
        if(tag_label_associations):
            
            tags = tag_label_associations.values() 
            
        return set(tags)
        

    def get_images_nr_for_tag(self, tag):
        '''
        Get number of images for given tag
        
        :type tag: string
        :param tag: tag for whom number of images is queried        
        
        :rtype: integer
        :returns: number of images for given tag
        '''
        
        training_set_path = os.path.join(
        self._data_dir_path, c.TRAINING_SET_DIR)   
        
        aligned_faces_path = os.path.join(
        training_set_path, c.ALIGNED_FACES_DIR)
        
        aligned_faces_subject_path = os.path.join(aligned_faces_path, tag)
        
        images_nr = 0
        
        for image in os.listdir(aligned_faces_subject_path):
            
            images_nr = images_nr + 1
            
        return images_nr    
    
    
    def get_people_nr(self):
        '''
        Get number of people in face model
        
        :rtype: integer
        :returns: number of people in face model
        '''
        
        tags = self.get_tags()
        
        people_nr = len(tags)
            
        return people_nr
      
    
    def create_models(self):
        '''
        Read images in folder with aligned faces and create face models
        Folder with aligned faces contains one subfolder for each person
        '''
        
        training_set_path = os.path.join(
        self._data_dir_path, c.TRAINING_SET_DIR)   
        
        aligned_faces_path = os.path.join(
        training_set_path, c.ALIGNED_FACES_DIR)
        
        # Create face recognizer
        radius = c.LBP_RADIUS
        neighbors = c.LBP_NEIGHBORS
        grid_x = c.LBP_GRID_X
        grid_y = c.LBP_GRID_Y
        min_diff = c.GLOBAL_FACE_MODELS_MIN_DIFF
        
        if(self._params is not None):

            if(c.LBP_RADIUS_KEY in self._params):
                radius = self._params[c.LBP_RADIUS_KEY]
            
            if(c.LBP_NEIGHBORS_KEY in self._params):
                neighbors = self._params[c.LBP_NEIGHBORS_KEY]
                
            if(c.LBP_GRID_X_KEY in self._params):
                grid_x = self._params[c.LBP_GRID_X_KEY]
                
            if(c.LBP_GRID_Y_KEY in self._params):
                grid_y = self._params[c.LBP_GRID_Y_KEY]
                
            if(c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY in self._params):
                min_diff = self._params[c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY]
        
        model=cv2.createLBPHFaceRecognizer(
        radius,
        neighbors,
        grid_x,
        grid_y)
        
        tag_label_associations = {} 
        
        # Load file with faces
        faces_file = os.path.join(
        self._data_dir_path, c.FACES_FILE)
        faces_dict = utils.load_YAML_file(faces_file)
        if(faces_dict is None):
            
            # Create dictionary with face data
            faces_dict = {}
        
        im_counter = 0
        subject_counter = 0    
        
        for sub_dir_name in os.listdir(aligned_faces_path):
            
            tag_label_associations[subject_counter] = sub_dir_name
            
            subject_path = os.path.join(
            aligned_faces_path, sub_dir_name)  
            
            for im_name in os.listdir(subject_path):
                
                im_path = os.path.join(subject_path, im_name)
                
                rel_im_path = os.path.join(sub_dir_name, im_name)
                
                if(rel_im_path not in faces_dict):
                
                    faces_dict[rel_im_path] = {} 
                
                face_in_models = False
            
                try:
                
                    face = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
                    
                    # If this is the first image train model, 
                    # otherwise update it
                    
                    if(im_counter == 0):
                        
                        model.train(
                        np.asarray([np.asarray(face, dtype=np.uint8)]), 
                        np.asarray(subject_counter))
                        
                        face_in_models = True
                        
                    else:
                        
                        if(min_diff > 0):
                            # Check if face is sufficiently different
                            # from other faces in models
                            (label, conf) = model.predict(
                            np.asarray(face, dtype = np.uint8)) 
                            
                            if(conf >= min_diff):
                                
                                model.update(
                                np.asarray([np.asarray(face, dtype=np.uint8)]), 
                                np.asarray(subject_counter)) 
                                
                                face_in_models = True
                                
                        else:
                            
                            model.update(
                            np.asarray([np.asarray(face, dtype=np.uint8)]), 
                            np.asarray(subject_counter)) 
                            
                            face_in_models = True   
                            
                    faces_dict[rel_im_path][c.FACE_IN_MODELS_KEY] = face_in_models                                             
                    
                    im_counter = im_counter + 1
    
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                    
            subject_counter = subject_counter + 1        
                 
        
        # Save file with face models    
        db_file_name = os.path.join(
        self._data_dir_path, c.FACE_MODELS_FILE)  
                    
        model.save(db_file_name) 
        
        self._models = model
        
        # Save file with tag-label associations
        tag_label_associations_file = os.path.join(
        self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        utils.save_YAML_file(
        tag_label_associations_file, tag_label_associations)
        
        # Save new dictionary in YAML file
        utils.save_YAML_file(faces_file, faces_dict)            
        

    def load_models(self):
        '''
        Load face models
        
        :rtype: boolean
        :returns: True if models were successfully loaded, 
        False otherwise
        '''
        
        ok = False
        
        db_file_path = os.path.join(
        self._data_dir_path, c.FACE_MODELS_FILE)
        
        # Load face recognizer
        
        if(os.path.exists(db_file_path)):
        
            self._models=cv2.createLBPHFaceRecognizer()
        
            self._models.load(db_file_path)
            
            ok = True
            
        return ok
            
        
    def recognize_face(self, face):
        '''
        Recognize given face using 
        the stored face recognition models
        
        :type face: OpenCV image
        :param face: face to be recognized      
                
        :rtype: tuple
        :returns: a tuple containing predicted tag 
        and relative confidence
        '''
        
        tag = c.UNDEFINED_TAG
        conf = sys.maxint
        
        if(self._models):
        
            (label, conf) = self._models.predict(
            np.asarray(face, dtype = np.uint8))
            print('label', label)
            print('conf', conf)
            
            # Consider tag only if distance is below threshold
            if(conf < c.GLOBAL_FACE_REC_THRESHOLD):
            
                tag = self.get_tag(label)
        
        return (tag, conf)
        
        
    def remove_face(self, tag, im_name):
        '''
        Remove face from face models
        
        :type tag: string
        :param tag: tag of person whom face belong to
        
        :type im_name: string
        :param im_path: name of image file containing the face
        
        :rtype: boolean
        :returns: true if face has been removed
        '''
        
        ok = False
        
        rel_im_path = os.path.join(tag, im_name)
        
        training_set_path = os.path.join(
        self._data_dir_path, c.TRAINING_SET_DIR)         
        
        aligned_faces_path = os.path.join(
        training_set_path, c.ALIGNED_FACES_DIR)  
        
        aligned_face_path = os.path.join(
        aligned_faces_path, rel_im_path)
        
        print('aligned_face_path', aligned_face_path)
        
        if(os.path.exists(aligned_face_path)):
        
            images_nr = self.get_images_nr_for_tag(tag)
    
            if(images_nr == 1):
                
                # Remove tag
                
                ok = self.remove_tag(tag)
            
            else:
                
                try:
                    
                    # Remove whole image
                    whole_images_path = os.path.join(
                    training_set_path, c.WHOLE_IMAGES_DIR)
                    
                    whole_image_path = os.path.join(
                    whole_images_path, rel_im_path)
                    print('whole_image_path', whole_image_path)
                    
                    if(os.path.exists(whole_image_path)):
                
                        os.remove(whole_image_path)
                        
                    # TEST ONLY remove bbox image
                    bbox_images_path = os.path.join(
                    training_set_path, c.BBOX_IMAGES_DIR)
                    
                    bbox_image_path = os.path.join(
                    bbox_images_path, rel_im_path)
                    
                    if(os.path.exists(bbox_image_path)):
                
                        os.remove(bbox_image_path)
                        
                    # Remove aligned face
                
                    os.remove(aligned_face_path)
                        
                    # Load file with faces
                    faces_file = os.path.join(
                    self._data_dir_path, c.FACES_FILE)
                    faces_dict = utils.load_YAML_file(faces_file)
                    
                    if(faces_dict):
                        for key in faces_dict.keys():
                            if(key == rel_im_path):
                                
                                del faces_dict[key]     
                                
                        # Save new dictionary in YAML file
                        utils.save_YAML_file(faces_file, faces_dict)
                    
                    # Re-build the models
                    self.create_models() 
                    
                    ok = True                                                                           
                    
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise 
            
        return ok
            
    
    def remove_tag(self, tag):
        '''
        Remove tag from face models
        
        :type tag: string
        :param tag: tag to be removed
        
        :rtype: boolean
        :returns: true if tag has been removed
        '''
        
        ok = False
        
        training_set_path = os.path.join(
        self._data_dir_path, c.TRAINING_SET_DIR)  
        
        # Remove directory with aligned faces related to tag
        
        aligned_faces_path = os.path.join(
        training_set_path, c.ALIGNED_FACES_DIR)
        
        aligned_faces_subject_path = os.path.join(aligned_faces_path, tag)           
         
        if(os.path.exists(aligned_faces_subject_path)):
        
            try:
                
                # Remove directory with whole images related to tag                    
                whole_images_path = os.path.join(
                training_set_path, c.WHOLE_IMAGES_DIR)
                
                whole_images_subject_path = os.path.join(whole_images_path, tag)             
                 
                if(os.path.exists(whole_images_subject_path)):
                
                    shutil.rmtree(whole_images_subject_path)
                    
                # TEST ONLY remove directory with bbox images related to tag
                    
                bbox_images_path = os.path.join(
                training_set_path, c.BBOX_IMAGES_DIR)
                
                bbox_images_subject_path = os.path.join(bbox_images_path, tag)           
                 
                if(os.path.exists(bbox_images_subject_path)):
                
                    shutil.rmtree(bbox_images_subject_path)
    
                shutil.rmtree(aligned_faces_subject_path)
                    
                # Load file with tag-label associations
                tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
                tag_label_associations = utils.load_YAML_file(
                tag_label_associations_file) 
                
                if(tag_label_associations):
                
                    # Remove tag with related label
                    tag_label_associations = {key: value for key, value in tag_label_associations.items() if value != tag}
                    
                    # Save new dictionary in YAML file
                    utils.save_YAML_file(
                    tag_label_associations_file, tag_label_associations)
                
                # Load file with faces
                faces_file = os.path.join(
                self._data_dir_path, c.FACES_FILE)
                faces_dict = utils.load_YAML_file(faces_file)
                
                if(faces_dict):
                
                    for key in faces_dict.keys():
                        key_tag = os.path.split(key)[0]
                        if(key_tag == tag):
                            
                            del faces_dict[key]     
                            
                    # Save new dictionary in YAML file
                    utils.save_YAML_file(faces_file, faces_dict)
                
                # Re-build the models
                self.create_models() 
                
                ok = True                                                                           
                
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise 
            
        return ok          
                            
