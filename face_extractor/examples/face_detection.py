import cv2
import os
import sys

sys.path.append('..')
import tools.constants as c
from tools.face_detection import detect_faces_in_image

# Set path of image to be analyzed
image_path = 'images' + os.sep + 'test.jpg'

# Set path of directory where aligned faces will be saved
align_path = 'aligned_faces'

# Set configuration parameters
params = {
    c.CHECK_EYE_POSITIONS_KEY: True,
    c.CLASSIFIERS_DIR_PATH_KEY: 'C:\OpenCV\opencv\sources\data\haarcascades',
    c.CROPPED_FACE_HEIGHT_KEY: 250,
    c.CROPPED_FACE_WIDTH_KEY: 200,
    c.EYE_DETECTION_CLASSIFIER_KEY: 'haarcascade_mcs_lefteye.xml',
    c.FACE_DETECTION_ALGORITHM_KEY: 'HaarCascadeFrontalFaceAlt2',
    c.FLAGS_KEY: 'DoCannyPruning',
    c.MIN_NEIGHBORS_KEY: 5,
    c.MIN_SIZE_HEIGHT_KEY: 20,
    c.MIN_SIZE_WIDTH_KEY: 20,
    c.OFFSET_PCT_X_KEY: 0.30,
    c.OFFSET_PCT_Y_KEY: 0.42,
    c.SCALE_FACTOR_KEY: 1.1,
    c.MAX_EYE_ANGLE_KEY: 0.125,
    c.MIN_EYE_DISTANCE_KEY: 0.25,
    c.USE_EYES_POSITION_KEY: True,
    c.USE_NOSE_POS_IN_DETECTION_KEY: False
}

result = detect_faces_in_image(
    image_path, align_path, params, show_results=True)

# Show aligned faces
if result and c.FACES_KEY in result:
    faces = result[c.FACES_KEY]
    for face in faces:

        # Show RGB image
        file_name = face[c.ALIGNED_FACE_FILE_NAME_KEY] + '.png'
        file_path = os.path.join(align_path, file_name)
        img = cv2.imread(file_path)
        cv2.imshow('RGB aligned face', img)
        cv2.waitKey(0)

        # Show gray-level image
        file_name = face[c.ALIGNED_FACE_FILE_NAME_KEY] + '_gray.png'
        file_path = os.path.join(align_path, file_name)
        img = cv2.imread(file_path)
        cv2.imshow('Gray-level aligned face', img)
        cv2.waitKey(0)