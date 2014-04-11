import os
import cv2
import numpy as np
from Constants import *

def recognize_face(face, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

        :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''
    
    # TEST ONLY
    path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Dataset AT&T';
    [X,y] = read_images(path, None)
    model=cv2.createLBPHFaceRecognizer()
    model.train(np.asarray(X), np.asarray(y))
    #

    start_time = cv2.getTickCount();
    
    [label, confidence] = model.predict(np.asarray(face, dtype=np.uint8));
    
    print "Predicted label = %d (confidence=%.2f)" % (label, confidence) # TEST ONLY

    rec_time_in_clocks = cv2.getTickCount() - start_time;
    rec_time_in_seconds = rec_time_in_clocks / cv2.getTickFrequency();

    # Populate dictionary with label, confidence and elapsed CPU time
    result = {}; 
    result[FACE_RECOGNITION_ELAPSED_CPU_TIME_KEY] = rec_time_in_seconds;
    result[FACE_RECOGNITION_ERROR_KEY] = '';
    result[PERSON_ASSIGNED_LABEL_KEY] = label;
    result[PERSON_CONFIDENCE_KEY] = confidence;

    if(show_results):
        cv2.imshow(str(label), face);
        cv2.waitKey(0); 

    return result;

# TEST ONLY
def read_images(path, sz=None):
    c = 0
    X,y = [], []

    # Number of images for each person to be used for the training
    training_images_nr = 6;
    
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:

            subject_path = os.path.join(dirname, subdirname)

            image_counter = 0;
            for filename in os.listdir(subject_path):
                # First training_images_nr images are used for training, the remaining for test
                if(image_counter < training_images_nr):
                    try:
                        im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                        # resize to given size (if given)
                        if (sz is not None):
                            im = cv2.resize(im, sz)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                image_counter = image_counter + 1;
            c = c+1
    return [X,y]
#
