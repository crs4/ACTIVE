import cv2
import os
import sys
import numpy as np
import shutil

import constants_for_experiments as ce
from train_by_captions import train_by_captions
from utils_for_experiments import save_model_file

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
import tools.face_detection as fd
import tools.utils as utils


class FaceModels:
    """
    The face models used by the
    face recognition and caption recognition algorithms.
    Used for experiments on face recognition and caption recognition

    :type params: dictionary
    :param params: configuration parameters to be used
                   for the face model (see table)

    :type force_db_creation: boolean
    :param force_db_creation: if true, db is always created

    :type video_path: string
    :param video_path: path of video with captions

    ============================================  ========================================  ==============
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============
    check_eye_positions                           If True, check eye positions              True
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    eye_detection_classifier                      Classifier for eye detection              'haarcascade_mcs_lefteye.xml'
    face_detection_algorithm                      Classifier for face detection             'HaarCascadeFrontalFaceAlt2'
                                                  ('HaarCascadeFrontalFaceAlt',
                                                  'HaarCascadeFrontalFaceAltTree',
                                                  'HaarCascadeFrontalFaceAlt2',
                                                  'HaarCascadeFrontalFaceDefault',
                                                  'HaarCascadeProfileFace',
                                                  'HaarCascadeFrontalAndProfileFaces',
                                                  'HaarCascadeFrontalAndProfileFaces2',
                                                  'LBPCascadeFrontalface',
                                                  'LBPCascadeProfileFace' or
                                                  'LBPCascadeFrontalAndProfileFaces')
    flags                                         Flags used in face detection              'DoCannyPruning'
                                                  ('DoCannyPruning', 'ScaleImage',
                                                  'FindBiggestObject', 'DoRoughSearch')
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    max_eye_angle                                 Maximum inclination of the line           0.125
                                                  connecting the eyes
                                                  (in % of pi radians)
    min_eye_distance                              Minimum distance between eyes             0.25
                                                  (in % of the width of the face
                                                  bounding box)
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    aligned_faces_path                            Default path of directory
                                                  for aligned faces
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
    db_name                                       Name of single file
                                                  containing face models
    db_models_path                                Path of directory containing face models
    face_model_algorithm                          Algorithm for face recognition            'LBP'
                                                  ('Eigenfaces', 'Fisherfaces' or 'LBP')
    LBP_grid_x                                    Number of columns in grid                 4
                                                  used for calculating LBP
    LBP_grid_y                                    Number of columns in grid                 8
                                                  used for calculating LBP
    LBP_neighbors                                 Number of neighbors                       8
                                                  used for calculating LBP
    LBP_radius                                    Radius used                               1
                                                  for calculating LBP (in pixels)
    offset_pct_x                                  % of the image to keep next to            0.20
                                                  the eyes in the horizontal direction
    offset_pct_y                                  % of the image to keep next to            0.50
                                                  the eyes in the vertical direction
    use_eye_detection                             If True, use eye detection for detecting  True
                                                  eye position for aligning faces in
                                                  test images
    use_eye_detection_in_training                 If True, use eye detection for detecting  True
                                                  eye position for aligning faces in
                                                  training images
    use_eyes_position                             If True, align faces in test images       True
                                                  by using eye positions
    use_eyes_position_in_training                 If True, align faces in training images   True
                                                  by using eye positions
    use_face_detection_in_training                If True, use face detection               False
                                                  for images in training set
    use_NBNN                                      If True,                                  False
                                                  use Naive Bayes Nearest Neighbor
    use_one_file_for_face_models                  If True, use one file for face models     True
    use_resizing                                  If True, resize images                    True
    use_weighted_regions                          If True, use weighted LBP                 False
    ============================================  ========================================  ==============
    """

    def __init__(
            self, params=None, force_db_creation=False,
            video_path=None):
        """
        Initialize the face models.

        :type params: dictionary
        :param params: configuration parameters to be used
                       for the face model (see table)

        :type force_db_creation: boolean
        :param force_db_creation: if true, db is always created

        :type video_path: string
        :param video_path: path of video with captions
        """
        
        self._params = params
        self._tags = {}
        self.model = None
        self.model_creation_time = 0
        
        self._algorithm = ce.FACE_MODEL_ALGORITHM
        dataset_already_divided = ce.DATASET_ALREADY_DIVIDED
        db_name = ce.DB_NAME
        db_path = ce.FACE_RECOGNITION_DATASET_PATH
        training_set_path = ce.FACE_RECOGNITION_TRAINING_SET_PATH
        use_captions = ce.USE_CAPTIONS
        use_one_file = ce.USE_ONE_FILE_FOR_FACE_MODELS

        if params is not None:
            self._algorithm = params[ce.FACE_MODEL_ALGORITHM_KEY]
            if ce.DATASET_ALREADY_DIVIDED_KEY in params:
                dataset_already_divided = params[ce.DATASET_ALREADY_DIVIDED_KEY]
            if ce.DB_NAME_KEY in params:
                db_name = params[ce.DB_NAME_KEY]
            if ce.DATASET_PATH_KEY in params:
                db_path = params[ce.DATASET_PATH_KEY]
            if ce.USE_CAPTIONS_KEY in params:
                use_captions = params[ce.USE_CAPTIONS_KEY]
            if ce.TRAINING_SET_PATH_KEY in params:
                training_set_path = params[ce.TRAINING_SET_PATH_KEY]
            if ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY in params:
                use_one_file = params[ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY]

        if use_captions:

            if video_path:

                self._dbpath = video_path

                file_name, file_ext = os.path.splitext(video_path)

                self._db_name = file_name + '-DB'

            else:

                print 'No video path was provided'
        else:
            self._dbpath = training_set_path
            self._db_name = db_name

            if not dataset_already_divided:
                self._dbpath = db_path

            self._db_name = db_name

            if dataset_already_divided:
                self._dbpath = training_set_path

            else:
                self._dbpath = db_path

        if force_db_creation:
            self.create(video_path)
        else:
            ok = False
            
            if use_one_file:
                # Try to load db
                ok = self.load(None)

            else:

                ok = self.load_tags(None)

            # If loading was not successful, create it
            if not ok:
                self.create(video_path)

    def get_tag(self, index):
        """
        Get tag string given numeric index

        :type index: int
        :param index: index of tag

        :rtype: string
        :returns: tag or -1 if an exception occurred
        """
        try:
            if self._tags is not None:
                return self._tags[index]
            return -1
        except:
            return -1

    def get_tags(self):
        """
        Get all tags as list of strings

        :rtype: list
        :returns: list of tags or -1 if an exception occurred
        """
        try:
            if self._tags is not None:
                return self._tags.values()
            return - 1
        except:
            return -1

    def get_people_nr(self):
        """
        Get number of people in face model

        :rtype: integer
        :returns: number of people or -1 if an exception occurred
        """
        try:
            if self._tags is not None:
                return len(self._tags)
            return -1
        except:
            return -1

    def remove_tags(self, tags):
        """
        Remove the given tag or tags (and all associated faces)
        from the face models data structure.
        If any of the provided tags is not in the face models data structure,
        the tag is ignored.

        :type  tags: string or list of strings
        :param tags: the tags associated to the face to be removed
                     from the face models data structure

        :rtype: boolean
        :returns: True if tags have been removed
        """

        for tag in tags:
            if os.path.exists(self._dbpath + "/" + tag):
                print "removing ", self._dbpath + "/" + tag
                shutil.rmtree(self._dbpath + "/" + tag)
        self.create()
        return True

    def load(self, db_file_name):
        """
        Update the face models data structure from a file.

        :type  db_file_name: string
        :param db_file_name: the name of the file containing
                             the dump of the face models data structure

        :rtype: boolean
        :returns: True if loading was successful
        """
        if db_file_name is None:
            '''
            Set the name of database.
            Algorithm :
            LBP (Local Binary Pattern)
            '''
            db_file_name = self._db_name + '-' + self._algorithm

        tags_file_name = db_file_name + '-Tags'

        algorithm = ce.FACE_MODEL_ALGORITHM
        
        if self._params is not None:
            
            algorithm = self._params[ce.FACE_MODEL_ALGORITHM_KEY]
        
        model = None
        
        if algorithm == 'Eigenfaces':
            
            model = cv2.createEigenFaceRecognizer()
        
        elif algorithm == 'Fisherfaces':
            
            model = cv2.createFisherFaceRecognizer()
            
        elif algorithm == 'LBP':
            
            model = cv2.createLBPHFaceRecognizer()
        
        ok = False

        if os.path.isfile(db_file_name) and (os.path.isfile(tags_file_name)):

            if(not((ce.USE_TRACKING or ce.SIM_TRACKING or ce.USE_SLIDING_WINDOW)
                   and ce.LOAD_IND_FRAMES_RESULTS)):
                model.load(db_file_name)

            if not(model is None):
                self.model = model
                self._tags = utils.load_YAML_file(tags_file_name)
                ok = True
                print('\n### DB LOADED ###\n')

        return ok

    def load_tags(self, db_file_name):
        """
        Load tags from a file.

        :type  db_file_name: string
        :param db_file_name: the root name of the file containing the tags

        :rtype: boolean
        :returns: True if loading was successful
        """
        if db_file_name is None:
            # Set the name of database.
            # Algorithm : LBP (Local Binary Pattern)
            db_file_name = self._db_name

        tags_file_name = self._db_name + "-LBP-Tags"

        ok = False

        if os.path.isfile(tags_file_name):

            self._tags = utils.load_YAML_file(tags_file_name)
            ok = True
            print('\n### TAGS LOADED ###\n')

        return ok

    def load_model(self, db_file_name):
        """
        Update the face models data structure for a single person from a file.

        :type  db_file_name: string
        :param db_file_name: the name of the file containing
                             the dump of the face models data structure

        :rtype: boolean
        :returns: True if loading was successful
        """

        ok = False

        if db_file_name is None:

            print "No db file was provided"

        else:

            algorithm = ce.FACE_MODEL_ALGORITHM
        
            if self._params is not None:
                
                algorithm = self._params[ce.FACE_MODEL_ALGORITHM_KEY]
            
            model = None
            
            if algorithm == 'Eigenfaces':
                
                model = cv2.createEigenFaceRecognizer()
            
            elif algorithm == 'Fisherfaces':
                
                model = cv2.createFisherFaceRecognizer()
                
            elif algorithm == 'LBP':
                
                model = cv2.createLBPHFaceRecognizer()

            if os.path.isfile(db_file_name):
                model.load(db_file_name)
                if not(model is None):
                    self.model = model
                    ok = True

        return ok

    def create(self, video_path=None, db_file_name=None):
        """
        Create the face models data structure

        :type video_path: String
        :param video_path: path of video used for creating the models

        :type db_file_name: String
        :param db_file_name: the name of the file containing
                             the dump of the face models data structure

        :rtype: FaceRecognizer
        :returns: the face models data structure
        """

        print('\n### CREATING DB ####\n')

        model = None

        use_captions = ce.USE_CAPTIONS
        
        if (self._params is not None) and (ce.USE_CAPTIONS_KEY in self._params):
            
            use_captions = self._params[ce.USE_CAPTIONS_KEY]

        if use_captions:

            db_file_name = self._db_name + "-" + self._algorithm
            [model, tags] = train_by_captions(video_path, db_file_name)
            self.model = model
            self._tags = tags

        else:

            start_time = cv2.getTickCount()

            if db_file_name is None:

                db_file_name = self._db_name + "-" + self._algorithm

            sz = None
            
            use_resizing = ce.USE_RESIZING
        
            if self._params is not None:
            
                use_resizing = self._params[ce.USE_RESIZING_KEY]
            
            if use_resizing:
                
                width = c.CROPPED_FACE_WIDTH
                height = c.CROPPED_FACE_HEIGHT
        
                if self._params is not None:
            
                    width = self._params[c.CROPPED_FACE_WIDTH_KEY]
                    height = self._params[c.CROPPED_FACE_HEIGHT_KEY]
                    
                sz = (width, height)

            [X, y] = self.__read_images(self._dbpath, sz)

            if len(self._tags) > 0:

                use_one_file = ce.USE_ONE_FILE_FOR_FACE_MODELS
        
                if self._params is not None:
                    
                    use_one_file = (
                        self._params[ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY])

                if use_one_file:

                    algorithm = ce.FACE_MODEL_ALGORITHM
                
                    if self._params is not None:
                        
                        algorithm = self._params[ce.FACE_MODEL_ALGORITHM_KEY]
                    
                    model = None
                    
                    if algorithm == 'Eigenfaces':
                        
                        model = cv2.createEigenFaceRecognizer()
                    
                    elif algorithm == 'Fisherfaces':
                        
                        model = cv2.createFisherFaceRecognizer()
                        
                    elif algorithm == 'LBP':
                        
                        radius = c.LBP_RADIUS
                        neighbors = c.LBP_NEIGHBORS
                        grid_x = c.LBP_GRID_X
                        grid_y = c.LBP_GRID_Y
                        
                        if self._params is not None:

                            radius = self._params[c.LBP_RADIUS_KEY]
                            neighbors = self._params[c.LBP_NEIGHBORS_KEY]
                            grid_x = self._params[c.LBP_GRID_X_KEY]
                            grid_y = self._params[c.LBP_GRID_Y_KEY]
                        
                        model = cv2.createLBPHFaceRecognizer(
                        radius,
                        neighbors,
                        grid_x,
                        grid_y)
                        
                    model.train(np.asarray(X), np.asarray(y))
                    model.save(db_file_name)
                    self.model = model

                # Save tags in YAML file
                utils.save_YAML_file(db_file_name + "-Tags", self._tags)

                time_in_clocks = cv2.getTickCount() - start_time
                time_in_seconds = time_in_clocks / cv2.getTickFrequency()
                
                self.model_creation_time = time_in_seconds
                
                print('Creation time: ' + str(time_in_seconds) + ' s\n')

            else:

                print "No model was created"
        
        return model

    def clear(self):
        pass

    def __read_images(self, path, sz=None):

        l = 0
        X, y = [], []
        
        # Set parameters
        align_path = c.ALIGNED_FACES_PATH
        use_eyes_pos_in_training = ce.USE_EYES_POSITION_IN_TRAINING
        use_eye_det_in_training = ce.USE_EYE_DETECTION_IN_TRAINING
        use_face_det_in_training = ce.USE_FACE_DETECTION_IN_TRAINING
        offset_pct_x = c.OFFSET_PCT_X
        offset_pct_y = c.OFFSET_PCT_Y
        
        if self._params is not None:
            
            align_path = self._params[c.ALIGNED_FACES_PATH_KEY]
            use_eyes_pos_in_training = (self._params
                [ce.USE_EYES_POSITION_IN_TRAINING_KEY])
            use_eye_det_in_training = (
                self._params[ce.USE_EYE_DETECTION_IN_TRAINING_KEY])
            use_face_det_in_training = (
                self._params[ce.USE_FACE_DETECTION_IN_TRAINING_KEY])
            offset_pct_x = self._params[c.OFFSET_PCT_X_KEY]
            offset_pct_y = self._params[c.OFFSET_PCT_Y_KEY]
        
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                # print "creating model for", subdirname
                subject_path = os.path.join(dirname, subdirname)
                # print "subject path:", subject_path
                file_counter = 0
                for filename in os.listdir(subject_path):
                    # print "image path", os.path.join(subject_path, filename)
                    try:
                        
                        if use_face_det_in_training:
                            im = fd.get_detected_cropped_face(
                                os.path.join(subject_path, filename),
                                align_path, self._params,
                                return_always_face=False)

                        elif use_eyes_pos_in_training:
                            
                            if use_eye_det_in_training:
                                im = None
                                crop_result = fd.get_cropped_face(
                                    os.path.join(subject_path, filename),
                                    align_path, self._params,
                                    return_always_face=False)
                                if crop_result:
                                    im = crop_result[c.FACE_KEY]

                            else:
                                im = fd.get_cropped_face_using_fixed_eye_pos(
                                    os.path.join(subject_path, filename),
                                    align_path,
                                    offset_pct=(offset_pct_x, offset_pct_y),
                                    dest_size=sz)
                        
                        else:
                            im = cv2.imread(
                                os.path.join(subject_path, filename),
                                cv2.IMREAD_GRAYSCALE)
                            # resize to given size (if given)
                            if (im is not None) and (sz is not None):
                                im = cv2.resize(im, sz)

                        if im is not None:

                            X.append(np.asarray(im, dtype=np.uint8))
                            y.append(l)
                            self._tags[l] = str(subdirname)

                        else:
                            print "Image", os.path.join(subject_path, filename), "not considered"

                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise

                    file_counter += 1
                    
                    already_div = ce.DATASET_ALREADY_DIVIDED
                    training_images_nr = ce.TRAINING_IMAGES_NR
                    
                    if self._params is not None:
                        
                        already_div = (
                            self._params[ce.DATASET_ALREADY_DIVIDED_KEY])
                        training_images_nr = (
                            self._params[ce.TRAINING_IMAGES_NR_KEY])
                    
                    if((not already_div) and
                           (file_counter >= training_images_nr)):
                        # Number of training images has been reached
                        break

                use_one_file = ce.USE_ONE_FILE_FOR_FACE_MODELS
        
                if self._params is not None:
                    
                    use_one_file = (
                        self._params[ce.USE_ONE_FILE_FOR_FACE_MODELS_KEY])
                
                if not use_one_file:
                    save_model_file(X, y)
                    X, y = [], []

                l += 1
        return [X, y]

    def read_images(self, path, sz=None):
        """
        Reads the images in a given folder,
        resizes images on the fly if size is given.

        :type path: String
        :param path: Path to a folder with subfolders
                    representing the subjects (people)

        :type sz: tuple
        :param sz: output image size, given as a (width, height) tuple

        :rtype: list
        :returns: A list [X,y]
                  X: The images, which is a Python list of numpy arrays.
                  y: The corresponding labels
                  (the unique number of the subject/person) in a Python list.
        """

        self.__read_images(path, sz)
