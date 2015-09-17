import constants as c
import cv2
import os
import sys
import utils
import uuid
from PIL import Image
from crop_face import CropFace

# Face detectors
HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER = 'haarcascade_frontalface_alt.xml'
HAARCASCADE_FRONTALFACE_ALT_TREE_CLASSIFIER = 'haarcascade_frontalface_alt_tree.xml'
HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER = 'haarcascade_frontalface_alt2.xml'
HAARCASCADE_FRONTALFACE_DEFAULT_CLASSIFIER = 'haarcascade_frontalface_default.xml'
HAARCASCADE_PROFILEFACE_CLASSIFIER = 'haarcascade_profileface.xml'
LBPCASCADE_FRONTALFACE_CLASSIFIER = 'lbpcascade_frontalface.xml'
LBPCASCADE_PROFILEFACE_CLASSIFIER = 'lbpcascade_profileface.xml'


def _detect_faces_in_image(params):
    """
    Detect faces in image.
    Parameters are passed as a list.

    :type params: list
    :param params: list of parameters

    :rtype: dictionary
    :returns: dictionary with results
    """
    return detect_faces_in_image(*params)


def detect_faces_in_image(resource_path, align_path, params, show_results=False,
                          delete_files=False, return_always_faces=False):
    """
    Detect faces in image

    :type resource_path: string
    :param resource_path: path of image to be analyzed

    :type align_path: string
    :param align_path: path of directory where aligned faces are saved

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the face detection (see table)

    :type delete_files: boolean
    :param delete_files: delete (True) or do not delete (False)
                         saved image files

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with detected faces

    :type return_always_faces: boolean
    :param return_always_faces: if True,
                                return face even if no eyes are detected

    :rtype: dictionary
    :returns: dictionary with results (see table)

    ============================================  ========================================  =============================
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  =============================
    check_eye_positions                           If True, check eye positions              True
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
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
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    offset_pct_x                                  % of the image to keep next to            0.20
                                                  the eyes in the horizontal direction
    offset_pct_y                                  % of the image to keep next to            0.50
                                                  the eyes in the vertical direction
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    max_eye_angle                                 Maximum inclination of the line           0.125
                                                  connecting the eyes
                                                  (in % of pi radians)
    min_eye_distance                              Minimum distance between eyes             0.25
                                                  (in % of the width of the face
                                                  bounding box)
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    software_test_file                            Path of image to be used for
                                                  software test
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    use_eyes_position                             If True, align faces                      True
                                                  by using eye positions
    ============================================  ========================================  =============================

    =====================================  =============================================================================
    Key (results)                          Value
    =====================================  =============================================================================
    elapsed_CPU_time                       The elapsed CPU time in seconds
    error                                  A string specifying an error condition,
                                           or None if no errors occurred
    faces                                  List of detected faces.
                                           Each face is represented by a dictionary containing: the name of the file
                                           with the aligned face, the face bounding box as (x, y, width, height) tuple,
                                           the eye positions as two (x, y) tuples (with x and y being the absolute
                                           positions of the eye centers in pixels in the face bounding box),
                                           the nose position as a (x, y) tuple
                                           (with x and y being the relative position of the nose center in
                                           the aligned face).
                                            Example:
                                           'faces': [{'aligned_face_file_name': '5fe061c3-184d-40f3-9a41-c91d520f29dc',
                                                      'bbox': (110, 220, 50, 50)},
                                                      'left_eye_position': (120, 230),
                                                      'right_eye_position': (150, 230),
                                                      'nose_position': (0.4, 0.5)},
                                                     {'aligned_face_file_name': '2e46f53a-02db-4f04-90a6-9abc3adf8621',
                                                      'bbox': (40, 270, 40, 40),
                                                      'left_eye_position': (45, 275),
                                                      'right_eye_position': (265, 275),
                                                      'nose_position': (0.55, 0.6)}
                                                      ]                                                                                                       }
    =====================================  =============================================================================
    """

    # Saving processing time for face detection
    start_time = cv2.getTickCount()

    result = {}

    # Open image
    file_check = os.path.isfile(resource_path)
    if not file_check:
        print('Image file does not exist')
        result[c.ERROR_KEY] = 'Image file does not exist'
        return result
    try:
        image = cv2.imread(resource_path, cv2.IMREAD_GRAYSCALE)

        PADDING_BORDER = 0

        # Pad image with zeros
        if PADDING_BORDER != 0:
            image = cv2.copyMakeBorder(
                image, PADDING_BORDER, PADDING_BORDER, PADDING_BORDER,
                PADDING_BORDER, cv2.BORDER_CONSTANT, 0)

        # Load classifier files
        classifier_file = ''
        classifier_file_2 = ''
        use_one_classifier_file = True

        # Algorithm to be used for the face detection
        algorithm = c.FACE_DETECTION_ALGORITHM

        # Path of directory containing classifier files
        classifiers_folder_path = c.CLASSIFIERS_DIR_PATH + os.sep

        # Cascade classifier for eye detection
        eye_detection_classifier = c.EYE_DETECTION_CLASSIFIER

        # Cascade classifiers for nose detection
        nose_detection_classifier = c.NOSE_DETECTION_CLASSIFIER

        use_eyes_position = c.USE_EYES_POSITION

        if params is not None:
            if c.FACE_DETECTION_ALGORITHM_KEY in params:
                algorithm = params[c.FACE_DETECTION_ALGORITHM_KEY]
            if c.CLASSIFIERS_DIR_PATH_KEY in params:
                classifiers_folder_path = params[c.CLASSIFIERS_DIR_PATH_KEY] + os.sep
            if c.EYE_DETECTION_CLASSIFIER_KEY in params:
                eye_detection_classifier = params[c.EYE_DETECTION_CLASSIFIER_KEY]
            if c.NOSE_DETECTION_CLASSIFIER_KEY in params:
                nose_detection_classifier = params[c.NOSE_DETECTION_CLASSIFIER_KEY]
            if c.USE_EYES_POSITION_KEY in params:
                use_eyes_position = params[c.USE_EYES_POSITION_KEY]

        if algorithm == 'HaarCascadeFrontalFaceAlt':
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER
        elif algorithm == 'HaarCascadeFrontalFaceAltTree':
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT_TREE_CLASSIFIER
        elif algorithm == 'HaarCascadeFrontalFaceAlt2':
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER
        elif algorithm == 'HaarCascadeFrontalFaceDefault':
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_DEFAULT_CLASSIFIER
        elif algorithm == 'HaarCascadeProfileFace':
            classifier_file = classifiers_folder_path + HAARCASCADE_PROFILEFACE_CLASSIFIER
        elif algorithm == 'HaarCascadeFrontalAndProfileFaces':
            use_one_classifier_file = False
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT_CLASSIFIER
            classifier_file_2 = classifiers_folder_path + HAARCASCADE_PROFILEFACE_CLASSIFIER
        elif algorithm == 'LBPCascadeFrontalface':
            classifier_file = classifiers_folder_path + LBPCASCADE_FRONTALFACE_CLASSIFIER
        elif algorithm == 'LBPCascadeProfileFace':
            classifier_file = classifiers_folder_path + LBPCASCADE_PROFILEFACE_CLASSIFIER
        elif algorithm == 'LBPCascadeFrontalAndProfileFaces':
            use_one_classifier_file = False
            classifier_file = classifiers_folder_path + LBPCASCADE_FRONTALFACE_CLASSIFIER
            classifier_file_2 = classifiers_folder_path + LBPCASCADE_PROFILEFACE_CLASSIFIER
        elif algorithm == 'HaarCascadeFrontalAndProfileFaces2':
            use_one_classifier_file = False
            classifier_file = classifiers_folder_path + HAARCASCADE_FRONTALFACE_ALT2_CLASSIFIER
            classifier_file_2 = classifiers_folder_path + HAARCASCADE_PROFILEFACE_CLASSIFIER
        else:
            print '\nAlgorithm %s is not available' % algorithm
            result[c.ERROR_KEY] = 'Detection algorithm is not available'
            return result

        faces = []

        if use_one_classifier_file:
            face_cascade_classifier = cv2.CascadeClassifier(classifier_file)

            if face_cascade_classifier.empty():
                print('Error loading face cascade classifier file')
                result[c.ERROR_KEY] = 'Error loading face cascade classifier file'
                return result
            else:
                if algorithm == 'LBPCascadeProfileFace':
                    # lbpcascade_profileface classifier
                    # only detects faces rotated to the right,
                    # so it must be used on the original
                    # and on the flipped image
                    faces_from_orig_image = detect_faces_in_image_with_single_classifier(
                        image, face_cascade_classifier, params)

                    # Flip image around y-axis
                    flipped_image = cv2.flip(image, 1)

                    faces_from_flipped_image = detect_faces_in_image_with_single_classifier(
                        flipped_image, face_cascade_classifier, params)

                    # Transform coordinates of faces from flipped image
                    image_width = len(image[0, :])

                    for i in range(len(faces_from_flipped_image)):
                        faces_from_flipped_image[i][0] = image_width + 1 - faces_from_flipped_image[i][0] - faces_from_flipped_image[i][2]

                    # Merge results
                    faces = merge_classifier_results(
                        faces_from_orig_image, faces_from_flipped_image)

                else:
                    # Use classifier on original image only
                    faces = detect_faces_in_image_with_single_classifier(
                        image, face_cascade_classifier, params)

        else:
            face_cascade_classifier_1 = cv2.CascadeClassifier(classifier_file)
            face_cascade_classifier_2 = cv2.CascadeClassifier(classifier_file_2)
            if face_cascade_classifier_1.empty() | face_cascade_classifier_2.empty():
                print('Error loading face cascade classifier file')
                result[c.ERROR_KEY] = 'Error loading face cascade classifier file'
                return
            else:
                # Detect faces in image using first classifier
                faces_from_classifier_1 = detect_faces_in_image_with_single_classifier(
                    image, face_cascade_classifier_1, params)

                # Detect faces in image using second classifier
                faces_from_classifier_2 = detect_faces_in_image_with_single_classifier(
                    image, face_cascade_classifier_2, params)

                # Merge results
                faces = merge_classifier_results(
                    faces_from_classifier_1, faces_from_classifier_2)

        detection_time_in_clocks = cv2.getTickCount() - start_time
        detection_time_in_seconds = detection_time_in_clocks / cv2.getTickFrequency()

        # Cascade classifier for eye detection
        eye_classifier_file = classifiers_folder_path + eye_detection_classifier
        eye_cascade_classifier = cv2.CascadeClassifier(eye_classifier_file)

        # Cascade classifiers for nose detection
        nose_classifier_file = classifiers_folder_path + nose_detection_classifier
        nose_cascade_classifier = cv2.CascadeClassifier(nose_classifier_file)

        if eye_cascade_classifier.empty():
            print('Error loading eye cascade classifier file')
            result[c.ERROR_KEY] = 'Error loading eye cascade classifier file'
            return result

        if nose_cascade_classifier.empty():
            print('Error loading nose cascade classifier file')
            result[c.ERROR_KEY] = 'Error loading nose cascade classifier file'
            return result

        # Populate dictionary with detected faces and elapsed CPU time
        result[c.ELAPSED_CPU_TIME_KEY] = detection_time_in_seconds
        result[c.ERROR_KEY] = None

        # Create face images from original image
        faces_final = []

        for (x, y, width, height) in faces:

            face_image = image[y: y + height, x: x + width]

            face_dict = {}

            face_list = (int(x), int(y), int(width), int(height))

            face_dict[c.BBOX_KEY] = face_list

            if use_eyes_position:
                crop_result = get_cropped_face_from_image(
                    face_image, resource_path, align_path, params,
                    eye_cascade_classifier, nose_cascade_classifier,
                    (x, y, width, height), delete_files, return_always_faces,
                    show_results
                )

                if crop_result:
                    face_dict[c.LEFT_EYE_POS_KEY] = crop_result[c.LEFT_EYE_POS_KEY]
                    face_dict[c.RIGHT_EYE_POS_KEY] = crop_result[c.RIGHT_EYE_POS_KEY]
                    face_dict[c.NOSE_POSITION_KEY] = crop_result[c.NOSE_POSITION_KEY]

                    if not delete_files:
                        face_dict[c.ALIGNED_FACE_FILE_NAME_KEY] = (
                            crop_result[c.ALIGNED_FACE_FILE_NAME_KEY])

                    faces_final.append(face_dict)

            else:

                faces_final.append(face_dict)

        result[c.FACES_KEY] = faces_final

        if show_results and (not use_eyes_position):

            image = cv2.imread(resource_path, cv2.IMREAD_COLOR)
            for face_dict in faces_final:

                (x, y, w, h) = face_dict[c.BBOX_KEY]

                face = image[y: y + h, x: x + w]

                cv2.rectangle(
                    image, (x, y), (x + w, y + h), (0, 0, 255), 3, 8, 0)

                # TODO DELETE
                # eye_rects = utils.detect_eyes_in_image(
                #     face, eye_cascade_classifier)
                # for(x_eye, y_eye, w_eye, h_eye) in eye_rects:
                #     cv2.rectangle(
                #         face, (x_eye, y_eye), (x_eye + w_eye, y_eye + h_eye),
                #         (0, 0, 255), 3, 8, 0)
                #
                # noses = utils.detect_nose_in_image(
                #     face, nose_cascade_classifier)
                # for(x_ear, y_ear, w_ear, h_ear) in noses:
                #     cv2.rectangle(
                #         face, (x_ear, y_ear), (x_ear + w_ear, y_ear + h_ear),
                #         (0, 0, 255), 3, 8, 0)

            cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Result', image)
            cv2.waitKey(0)

    except IOError as e:
        error_str = "I/O error({0}): {1}".format(e.errno, e.strerror)
        print error_str
        result[c.ERROR_KEY] = error_str
        return result

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    return result


def detect_faces_in_image_with_single_classifier(
        image, face_cascade_classifier, params=None):
    """
    Detect faces in image using a single classifier

    :type image: openCV image
    :param image: image to be analyzed

    :type face_cascade_classifier: face cascade classifier
    :param face_cascade_classifier: classifier to be used for the face detection

    :type params: dictionary
    :param params: configuration parameters to be used for the face detection (see table)

    :rtype: list
    :returns: a list of faces, represented as
              (x, y, width, height) tuples

    ============================================  ========================================  =============================
    Key                                           Value                                     Default value
    ============================================  ========================================  =============================
    flags                                         Flags used in face detection              'DoCannyPruning'
                                                  ('DoCannyPruning', 'ScaleImage',
                                                  'FindBiggestObject', 'DoRoughSearch')
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    ============================================  ========================================  =============================
    """

    haar_scale = c.FACE_DETECTION_SCALE_FACTOR
    min_neighbors = c.FACE_DETECTION_MIN_NEIGHBORS
    haar_flags_str = c.FACE_DETECTION_FLAGS
    min_size = (c.FACE_DETECTION_MIN_SIZE_WIDTH, c.FACE_DETECTION_MIN_SIZE_HEIGHT)

    if params is not None:
        if c.SCALE_FACTOR_KEY in params:
            haar_scale = params[c.SCALE_FACTOR_KEY]
        if c.MIN_NEIGHBORS_KEY in params:
            min_neighbors = params[c.MIN_NEIGHBORS_KEY]
        if c.FLAGS_KEY in params:
            haar_flags_str = params[c.FLAGS_KEY]
        if ((c.MIN_SIZE_WIDTH_KEY in params)
                and (c.MIN_SIZE_HEIGHT_KEY in params)):
            min_size = (params[c.MIN_SIZE_WIDTH_KEY], params[c.MIN_SIZE_HEIGHT_KEY])

    haar_flags = cv2.CASCADE_DO_CANNY_PRUNING
    if haar_flags_str == 'DoRoughSearch':
        haar_flags = cv2.CASCADE_DO_ROUGH_SEARCH
    elif haar_flags_str == 'FindBiggestObject':
        haar_flags = cv2.CASCADE_FIND_BIGGEST_OBJECT
    elif haar_flags_str == 'ScaleImage':
        haar_flags = cv2.CASCADE_SCALE_IMAGE

    faces = face_cascade_classifier.detectMultiScale(
    image, haar_scale, min_neighbors, haar_flags, min_size)
    return faces


def get_cropped_face(image_path, align_path, params=None, return_always_face=False):
    """
    Get face cropped and aligned to eyes from image file.
    Position of eyes is automatically detected

    :type image_path: string
    :param image_path: path of image to be cropped

    :type align_path: string
    :param align_path: path of directory where aligned faces are saved

    :type params: dictionary
    :param params: dictionary containing the parameters
                   to be used for the face detection (see table)

    :type return_always_face: boolean
    :type return_always_face: if true,
                              return face even if no eyes are detected

    :rtype: dictionary
    :returns: dictionary with results (see table)

    ============================================  ========================================  =============================
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  =============================
    check_eye_positions                           If True, check eye positions              True
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
    eye_detection_classifier                      Classifier for eye detection              'haarcascade_mcs_lefteye.xml'
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    offset_pct_x                                  % of the image to keep next to            0.20
                                                  the eyes in the horizontal direction
    offset_pct_y                                  % of the image to keep next to            0.50
                                                  the eyes in the vertical direction
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    use_nose_pos_in_recognition                   If True, compare in face recognition      False
                                                  only faces with similar
                                                  nose positions
    ============================================  ========================================  =============================

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    face                                   Aligned face as an OpenCV image
    left_eye_position                      Left eye position as a (x, y) tuple
                                           (with x and y being the absolute
                                           position of the eye center in
                                           pixels in the face bounding box)
    right_eye_position                     Right eye position as a (x, y) tuple
                                           (with x and y being the absolute
                                           position of the eye center in
                                           pixels in the face bounding box)
    =====================================  =====================================
    """

    # Open image
    file_check = os.path.isfile(image_path)

    if not file_check:
        print('File does not exist')
        return
    try:

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Path of directory containing classifier files
        classifiers_folder_path = c.CLASSIFIERS_DIR_PATH + os.sep

        # Cascade classifier for eye detection
        eye_detection_classifier = c.EYE_DETECTION_CLASSIFIER

        # Cascade classifier for nose detection
        nose_detection_classifier = c.NOSE_DETECTION_CLASSIFIER

        if params is not None:
            if c.CLASSIFIERS_DIR_PATH_KEY in params:
                classifiers_folder_path = params[c.CLASSIFIERS_DIR_PATH_KEY] + os.sep
            if c.EYE_DETECTION_CLASSIFIER_KEY in params:
                eye_detection_classifier = params[c.EYE_DETECTION_CLASSIFIER_KEY]
            if c.NOSE_DETECTION_CLASSIFIER_KEY in params:
                nose_detection_classifier = params[c.NOSE_DETECTION_CLASSIFIER_KEY]

        eye_classifier_file = classifiers_folder_path + eye_detection_classifier
        eye_cascade_classifier = cv2.CascadeClassifier(eye_classifier_file)

        if eye_cascade_classifier.empty():
            print('Error loading eye cascade classifier file')
            return None


        nose_classifier_file = classifiers_folder_path + nose_detection_classifier
        nose_cascade_classifier = cv2.CascadeClassifier(nose_classifier_file)

        if nose_cascade_classifier.empty():
            print('Error loading nose cascade classifier file')
            return None

        crop_result = get_cropped_face_from_image(
            image, image_path, align_path, params, eye_cascade_classifier,
            nose_cascade_classifier, (0, 0), False, return_always_face)

        result = None

        if crop_result:

            result = {}

            cropped_image = crop_result[c.FACE_KEY]

            result[c.FACE_KEY] = cropped_image
            result[c.LEFT_EYE_POS_KEY] = crop_result[c.LEFT_EYE_POS_KEY]
            result[c.RIGHT_EYE_POS_KEY] = crop_result[c.RIGHT_EYE_POS_KEY]

        return result

    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def get_cropped_face_from_image(
        image, image_path, align_path, params, eye_cascade_classifier,
        nose_cascade_classifier, face_bbox, delete_files, return_always_face,
        show_results=False):
    """
    Get face cropped and aligned to eyes from image

    :type image: openCV image
    :param image: image to be cropped

    :type image_path: string
    :param image_path: path of image to be analyzed

    :type align_path: string
    :param align_path: path of directory where aligned faces are saved

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the face detection (see table)

    :type eye_cascade_classifier: CascadeClassifier
    :param eye_cascade_classifier: classifier for detecting eyes

    :type nose_cascade_classifier: CascadeClassifier
    :param nose_cascade_classifier: classifier for detecting nose

    :type face_bbox: tuple
    :type face_bbox: bbox of face in original image,
                     represented as a (x, y, width, height) tuple

    :type delete_files: boolean
    :param delete_files: delete (True) or do not delete (False)
                         saved image files

    :type return_always_face: boolean
    :param return_always_face: if True,
                              return face even if no eyes are detected

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with detected faces

    :rtype: dictionary or None
    :returns: dictionary with results (see table)

    ============================================  ========================================  =============================
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  =============================
    check_eye_positions                           If True, check eye positions              True
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
    offset_pct_x                                  % of the image to keep next to            0.20
                                                  the eyes in the horizontal direction
    offset_pct_y                                  % of the image to keep next to            0.50
                                                  the eyes in the vertical direction
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    use_nose_pos_in_recognition                   If True, compare in face recognition      False
                                                  only faces with similar
                                                  nose positions
    ============================================  ========================================  =============================

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    face                                   Aligned face as an OpenCV image
    left_eye_position                      Left eye position as a (x, y) tuple
                                           (with x and y being the absolute
                                           position of the eye center in
                                           pixels in the face bounding box)
    right_eye_position                     Right eye position as a (x, y) tuple
                                           (with x and y being the absolute
                                           position of the eye center in
                                           pixels in the face bounding box)
    nose_position                          Nose position as a (x, y) tuple
                                           (with x and y being the absolute
                                           position of the nose center in
                                           pixels in the face bounding box)
    =====================================  =====================================
    """

    result = {}

    # Offset given as percentage of eye-to-eye distance
    offset_pct_x = c.OFFSET_PCT_X
    offset_pct_y = c.OFFSET_PCT_Y

    # Final size of cropped face
    cropped_face_width = c.CROPPED_FACE_WIDTH
    cropped_face_height = c.CROPPED_FACE_HEIGHT

    # If True, check eye positions
    check_eye_positions = c.CHECK_EYE_POSITIONS

    if params is not None:
        if c.CROPPED_FACE_WIDTH_KEY in params:
            cropped_face_width = params[c.CROPPED_FACE_WIDTH_KEY]
        if c.CROPPED_FACE_HEIGHT_KEY in params:
            cropped_face_height = params[c.CROPPED_FACE_HEIGHT_KEY]
        if c.OFFSET_PCT_X_KEY in params:
            offset_pct_x = params[c.OFFSET_PCT_X_KEY]
        if c.OFFSET_PCT_Y_KEY in params:
            offset_pct_y = params[c.OFFSET_PCT_Y_KEY]
        if c.CHECK_EYE_POSITIONS_KEY in params:
            check_eye_positions = params[c.CHECK_EYE_POSITIONS_KEY]

    offset_pct = (offset_pct_x, offset_pct_y)

    dest_size = (cropped_face_width, cropped_face_height)

    # Detect eyes in face
    eye_rects = utils.detect_eyes_in_image(image, eye_cascade_classifier)

    eye_left = None

    eye_right = None

    eye_check_ok = False

    opencv_img = None
    if show_results:
        opencv_img = cv2.imread(image_path)

    if len(eye_rects) == 2:

        x_first_eye = eye_rects[0][0]
        y_first_eye = eye_rects[0][1]
        w_first_eye = eye_rects[0][2]
        h_first_eye = eye_rects[0][3]

        x_second_eye = eye_rects[1][0]
        y_second_eye = eye_rects[1][1]
        w_second_eye = eye_rects[1][2]
        h_second_eye = eye_rects[1][3]

        x_left_eye_center = 0
        y_left_eye_center = 0
        x_right_eye_center = 0
        y_right_eye_center = 0
        if x_first_eye < x_second_eye:
            x_left_eye_center = x_first_eye + w_first_eye / 2
            y_left_eye_center = y_first_eye + h_first_eye / 2

            x_right_eye_center = x_second_eye + w_second_eye / 2
            y_right_eye_center = y_second_eye + h_second_eye / 2
        else:
            x_right_eye_center = x_first_eye + w_first_eye / 2
            y_right_eye_center = y_first_eye + h_first_eye / 2

            x_left_eye_center = x_second_eye + w_second_eye / 2
            y_left_eye_center = y_second_eye + h_second_eye / 2

        eye_left = (int(x_left_eye_center + face_bbox[0]),
                    int(y_left_eye_center + face_bbox[1]))
        eye_right = (int(x_right_eye_center + face_bbox[0]),
                     int(y_right_eye_center + face_bbox[1]))

        if check_eye_positions:
            eye_check_ok = utils.check_eye_pos(
                eye_left, eye_right, face_bbox, params)
        else:
            eye_check_ok = True

        if show_results and eye_check_ok:

            (x, y, w, h) = face_bbox

            cv2.rectangle(
                opencv_img, (x, y), (x + w, y + h), (0, 0, 255), 3, 8, 0)

            # First eye
            x_first_eye = x_first_eye + face_bbox[0]
            y_first_eye = y_first_eye + face_bbox[1]
            cv2.rectangle(opencv_img,
                          (x_first_eye, y_first_eye),
                          (x_first_eye + w_first_eye,
                           y_first_eye + h_first_eye),
                          (0, 0, 255), 3, 8, 0)
            # Second eye
            x_second_eye = x_second_eye + face_bbox[0]
            y_second_eye = y_second_eye + face_bbox[1]
            cv2.rectangle(opencv_img,
                          (x_second_eye, y_second_eye),
                          (x_second_eye + w_second_eye,
                           y_second_eye + h_second_eye),
                          (0, 0, 255), 3, 8, 0)

    if eye_check_ok:

        # Open whole image as PIL Image
        img = Image.open(image_path)

        # Store eye positions related to whole image
        result[c.LEFT_EYE_POS_KEY] = eye_left
        result[c.RIGHT_EYE_POS_KEY] = eye_right

        result[c.NOSE_POSITION_KEY] = None

        # Align face image

        # Create directory that will contain aligned faces if it does not exist
        if not os.path.exists(align_path):
            os.makedirs(align_path)

        # Create unique file path
        tmp_file_name = str(uuid.uuid4())
        tmp_file_name_complete = tmp_file_name + '.png'
        tmp_file_path = os.path.join(align_path, tmp_file_name_complete)

        CropFace(
            img, eye_left, eye_right, offset_pct, dest_size).save(tmp_file_path)

        face_image = cv2.imread(tmp_file_path, cv2.IMREAD_GRAYSCALE)

        if delete_files:
            os.remove(tmp_file_path)
        else:
            result[c.ALIGNED_FACE_FILE_NAME_KEY] = tmp_file_name

        # Check nose position
        nose_check_ok = True

        use_nose_pos_in_detection = c.USE_NOSE_POS_IN_DETECTION
        use_nose_pos_in_recognition = c.USE_NOSE_POS_IN_RECOGNITION

        if params is not None:
            if c.USE_NOSE_POS_IN_DETECTION_KEY in params:
                use_nose_pos_in_detection = params[c.USE_NOSE_POS_IN_DETECTION_KEY]
            if c.USE_NOSE_POS_IN_RECOGNITION_KEY in params:
                use_nose_pos_in_recognition = params[c.USE_NOSE_POS_IN_RECOGNITION_KEY]

        if use_nose_pos_in_detection or use_nose_pos_in_recognition:

            noses = utils.detect_nose_in_image(
                face_image, nose_cascade_classifier)

            x_right_eye = offset_pct[0] * dest_size[0]
            x_left_eye = dest_size[0] - x_right_eye
            y_eyes = offset_pct[1] * dest_size[1]

            good_noses = 0

            for(x_nose, y_nose, w_nose, h_nose) in noses:

                # Coordinates of bounding box center in face image
                x_center = float(x_nose + w_nose / 2)
                y_center = float(y_nose + h_nose / 2)

                # Store nose position relative to face image
                nose_x_pct = x_center / cropped_face_width
                nose_y_pct = y_center / cropped_face_height
                nose = (nose_x_pct, nose_y_pct)
                result[c.NOSE_POSITION_KEY] = nose

                # Nose must be between eyes in horizontal direction
                # and below eyes in vertical direction
                if((x_center > x_right_eye) and(x_center < x_left_eye)
                        and (y_center > y_eyes)):
                    good_noses += 1

            if good_noses != 1:

                nose_check_ok = False
                result[c.NOSE_POSITION_KEY] = None

            else:
                if show_results:
                    for(x_ear, y_ear, w_ear, h_ear) in noses:
                        cv2.rectangle(
                            opencv_img, (x_ear, y_ear),
                            (x_ear + w_ear, y_ear + h_ear),
                            (0, 0, 255), 3, 8, 0)

        if show_results:
            cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Result', opencv_img)
            cv2.waitKey(0)

            # TODO DELETE TEST ONLY
            path = os.path.splitext(image_path)[0] + '_detection.png'
            cv2.imwrite(path, opencv_img)

        if nose_check_ok or not use_nose_pos_in_detection:
            if c.USE_HIST_EQ_IN_CROPPED_FACES:
                face_image = cv2.equalizeHist(face_image)
            if c.USE_NORM_IN_CROPPED_FACES:
                face_image = cv2.normalize(
                    face_image, alpha=0, beta=255,
                    norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            if c.USE_CANNY_IN_CROPPED_FACES:
                face_image = cv2.Canny(face_image, 0.1, 100)
            if c.USE_TAN_AND_TRIGG_NORM:
                face_image = utils.normalize_illumination(face_image)
            # Insert oval mask in image
            if c.USE_OVAL_MASK:
                face_image = utils.add_oval_mask(face_image)

            if not delete_files:
                tmp_file_name_gray = (
                    tmp_file_name + c.ALIGNED_FACE_GRAY_SUFFIX + '.png')
                tmp_file_gray_path = os.path.join(
                    align_path, tmp_file_name_gray)

                cv2.imwrite(tmp_file_gray_path, face_image)

            return result

        else:

            result[c.FACE_KEY] = None

            return result

    else:

        if return_always_face:
            result[c.LEFT_EYE_POS_KEY] = None
            result[c.RIGHT_EYE_POS_KEY] = None
            return result

        else:

            return None


def get_cropped_face_using_eye_pos(
        image_path, align_path, eye_pos, offset_pct, dest_size):
    """
    Get face cropped and aligned to eyes from image file.
    Eye positions are known and given as a
    (left_eye_x, left_eye_y, right_eye_x, right_eye_y) list

    :type image_path: string
    :param image_path: path of image to be cropped

    :type align_path: string
    :param align_path: path of directory where aligned faces are saved

    :type eye_pos: list
    :param eye_pos: list containing eye positions

    :type offset_pct: 2-element tuple
    :param offset_pct: offset given as percentage of eye-to-eye distance

    :type dest_size: 2-element tuple
    :param dest_size: size of result

    :rtype: OpenCV image or None
    :returns: face
    """

    cropped_image = None
    # Open image
    file_check = os.path.isfile(image_path)

    if not file_check:
        print('File does not exist')
        return None
    try:
        # Open whole image as PIL Image
        img = Image.open(image_path)

        # Align face image
        (width, height) = img.size

        eye_left = (eye_pos[0], eye_pos[1])

        eye_right = (eye_pos[2], eye_pos[3])

        # Create directory that will contain aligned faces if it does not exist
        if not os.path.exists(align_path):
            os.makedirs(align_path)

        # Create unique file path
        tmp_file_name = str(uuid.uuid4()) + '.png'
        tmp_file_path = os.path.join(align_path, tmp_file_name)

        CropFace(
            img, eye_left, eye_right, offset_pct, dest_size).save(tmp_file_path)

        face_image = cv2.imread(tmp_file_path, cv2.IMREAD_GRAYSCALE)

        if c.USE_HIST_EQ_IN_CROPPED_FACES:
            face_image = cv2.equalizeHist(face_image)

        if c.USE_NORM_IN_CROPPED_FACES:
            face_image = cv2.normalize(
                face_image, alpha=0, beta=255,
                norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        if c.USE_CANNY_IN_CROPPED_FACES:
            face_image = cv2.Canny(face_image, 0.1, 100)

        if c.USE_TAN_AND_TRIGG_NORM:
            face_image = utils.normalize_illumination(face_image)

        # Insert oval mask in image
        if c.USE_OVAL_MASK:
            face_image = utils.add_oval_mask(face_image)

        return face_image

    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def get_cropped_face_using_fixed_eye_pos(
        image_path, align_path, offset_pct, dest_size):
    """
    Get face cropped and aligned to eyes from image file.
    Eye positions are known and corresponds to intersection in grid

    :type image_path: string
    :param image_path: path of image to be cropped

    :type align_path: string
    :param align_path: path of directory where aligned faces are saved

    :type offset_pct: 2-element tuple
    :param offset_pct: offset given as percentage of eye-to-eye distance

    :type dest_size: 2-element tuple
    :param dest_size: size of result

    :rtype: OpenCV image or None
    :returns: face
    """

    cropped_image = None
    # Open image
    file_check = os.path.isfile(image_path)

    if not file_check:
        print('File does not exist')
        return
    try:
        # Open whole image as PIL Image
        img = Image.open(image_path)

        # Align face image
        (width, height) = img.size

        eye_left = (width / c.GRID_CELLS_X, height / c.GRID_CELLS_Y)

        eye_right = (2 * width / c.GRID_CELLS_Y, height / c.GRID_CELLS_Y)

        # Create directory that will contain aligned faces if it does not exist
        if not os.path.exists(align_path):
            os.makedirs(align_path)

        # Create unique file path
        tmp_file_name = str(uuid.uuid4()) + '.png'
        tmp_file_path = os.path.join(align_path, tmp_file_name)

        CropFace(
            img, eye_left, eye_right, offset_pct, dest_size).save(tmp_file_path)

        face_image = cv2.imread(tmp_file_path, cv2.IMREAD_GRAYSCALE)

        if c.USE_HIST_EQ_IN_CROPPED_FACES:
            face_image = cv2.equalizeHist(face_image)

        if c.USE_NORM_IN_CROPPED_FACES:
            face_image = cv2.normalize(
                face_image, alpha=0, beta=255,
                norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        if c.USE_CANNY_IN_CROPPED_FACES:
            face_image = cv2.Canny(face_image, 0.1, 100)

        if c.USE_TAN_AND_TRIGG_NORM:
            face_image = utils.normalize_illumination(face_image)

        # Insert oval mask in image
        if c.USE_OVAL_MASK:
            face_image = utils.add_oval_mask(face_image)

        return face_image

    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def get_detected_cropped_face(
        image_path, align_path, params=None, return_always_face=False):
    """
    Detect face in image and return it cropped and aligned to eyes

    :type image_path: string
    :param image_path: path of image to be cropped

    :type align_path: string
    :param align_path: path of directory where aligned faces are saved

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the face detection (see table)

    :type return_always_face: boolean
    :param return_always_face: if true, face is always returned

    :rtype: OpenCV image or None
    :returns: face

    ============================================  ========================================  =============================
    Key                                           Value                                     Default value
    ============================================  ========================================  =============================
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
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found.
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
    software_test_file                            Path of image to be used for
                                                  software test
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    ============================================  ========================================  =============================
    """

    detection_result = detect_faces_in_image(
        image_path, align_path, params, False, return_always_face)

    if detection_result and (c.FACES_KEY in detection_result):

        faces = detection_result[c.FACES_KEY]

        if (len(faces) == 1) and (c.ALIGNED_FACE_FILE_NAME_KEY in faces[0]):

            face_dict = faces[0][c.FACE_KEY]
            file_name = face_dict[c.ALIGNED_FACE_FILE_NAME_KEY]
            complete_file_name = (
                file_name + c.ALIGNED_FACE_GRAY_SUFFIX + '.png')
            aligned_file_path = os.path.join(align_path, complete_file_name)
            face_image = cv2.imread(aligned_file_path, cv2.IMREAD_GRAYSCALE)

            return face_image
        else:
            return None

    else:
        return None


def merge_classifier_results(faces_from_classifier_1, faces_from_classifier_2):
    """
    Merge results from two classifiers in a single list

    :type faces_from_classifier_1: list
    :param faces_from_classifier_1: list of faces detected
                                    using first classifier, represented as
                                    (x, y, width, height) tuples

    :type faces_from_classifier_2: list
    :param faces_from_classifier_2: list of faces detected
                                    using second classifier, represented as
                                    (x, y, width, height) tuples

    :rtype: list
    :returns: a list of faces, represented as
             (x, y, width, height) tuples
    """

    faces = []

    # Add faces from second classifier only if they are not already present
    # in list of faces from first classifier
    for face2 in faces_from_classifier_2:
        face_must_be_considered = True
        for face1 in faces_from_classifier_1:

            (similar, int_area, int_area_pct) = utils.is_rect_similar(
                face1, face2, c.DET_MIN_INT_AREA)

            if similar:
                face_must_be_considered = False
                break

        if face_must_be_considered:
            faces.append(face2)

    faces.extend(faces_from_classifier_1)

    return faces
