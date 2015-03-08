import cv2
import os
from Utils import save_model_file

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
        
        if(params is not None):
            
            if(FACE_MODEL_ALGORITHM_KEY in params):
                self._algorithm = params[FACE_MODEL_ALGORITHM_KEY]
            
            if(GLOBAL_FACE_REC_DATA_DIR_PATH_KEY in params):
                self._data_dir_path = params[GLOBAL_FACE_REC_DATA_DIR_PATH_KEY]
                
        # Try to load tags
        ok = self.load_tags()
        
        # If loading was not successful, create models?
        if(not(ok)):
            pass
            
            
    def addFace(self, image_path, ):
		'''
		Add face into face model.
		If there are too much images in the face model,
		check which are the two most similar images 
		and delete the image among the two that is less simmetric
		
		:type image_path: string
		:param image_path: path of image to be added
		'''
    
    def createModel(self, subject_path, model_id):
        '''
        Create single face model
        
        :type subject_path: string
        :param subject_path: path of directory with face images 
        for this person
        
        :type model_id: integer
        :param model_id: identifier of face model
        '''
            
        file_counter = 0
        X, y = [], []
        
        max_faces_in_model = 
        
        for filename in os.listdir(subject_path):
            
            try:
            
                file_path = os.path.join(subject_path, filename)
            
                im = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                
                if(im is not None):
                    
                    if(file_counter >= max_faces_in_model):
						
						# Train face model and add new images one by one
                    
                    X.append(np.asarray(im, dtype = np.uint8))
                    y.append(file_counter)
                    
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
                    
            file_counter = file_counter + 1
            
    
    def createModels(self):
        '''
        Read images in training set folder and create model files
        Training set folder contains one subfolder for each person
        '''
        
        training_set_dir_path = os.path.join(
        self._data_dir_path, GLOBAL_FACE_REC_TRAINING_SET_DIR)
        
        model_id = 0
        for sub_dir_name in os.listdir(training_set_dir_path):
            
            subject_path = os.path.join(
            training_set_dir_path, sub_dir_name)
            
            self.createModel(subject_path, model_id)
            
            model_id = model_id + 1
