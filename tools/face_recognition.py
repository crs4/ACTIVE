import os
import cv2
import numpy as np

def recognize_face(face, params, show_results):
    '''Recognize given face using the face recognition model

    :type face:image
    :param face: face to be recognized

        :type params: dictionary
    :param params: dictionary containing the parameters to be used for the face recognition
    '''
    
    #TEST ONLY
    path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Dataset AT&T';
    [X,y] = read_images(path, None)
    model=cv2.createLBPHFaceRecognizer()
    model.train(np.asarray(X), np.asarray(y))

    [label, confidence] = model.predict(np.asarray(face, dtype=np.uint8));
    
    print "Predicted label = %d (confidence=%.2f)" % (label, confidence)

    if(show_results):
        cv2.imshow(str(label), face);
        cv2.waitKey(0); 

    return [label, confidence];

    
# TEST ONLY
def read_images(path, sz=None):
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
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,y]
