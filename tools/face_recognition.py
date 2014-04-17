import os
import cv2
import numpy as np
from Constants import *
from FaceModelsLBP import FaceModelsLBP

def recognize_face(face, face_models, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''

    fm = face_models;
    if(face_models == None):
        fm = FaceModelsLBP();

    start_time = cv2.getTickCount();
    
    [label, confidence] = fm.model.predict(np.asarray(face, dtype=np.uint8));

    # TODO: Get name of person
    tag = fm.get_label(label);
    
    #print "Predicted tag = %s (confidence=%.2f)" % (tag, confidence) # TEST ONLY

    rec_time_in_clocks = cv2.getTickCount() - start_time;
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency();

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {}; 
    result[FACE_RECOGNITION_ELAPSED_CPU_TIME_KEY] = rec_time_in_seconds;
    result[FACE_RECOGNITION_ERROR_KEY] = '';
    result[PERSON_ASSIGNED_LABEL_KEY] = label;
    result[PERSON_ASSIGNED_TAG_KEY] = tag;
    result[PERSON_CONFIDENCE_KEY] = confidence;

    if(show_results):
        cv2.imshow(str(label), face);
        cv2.waitKey(0); 

    return result;
