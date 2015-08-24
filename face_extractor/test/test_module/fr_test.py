import cv2
import numpy
import os
import sys

import constants_for_experiments as ce
from face_extractor_for_experiments import FaceExtractor
from face_models_for_experiments import FaceModels
from face_recognition import recognize_face
from utils_for_experiments import load_experiment_results

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
import tools.face_detection as fd
from tools.utils import load_YAML_file, save_YAML_file

# True if recognition is carried out by using FaceExtractor class
USE_FACEEXTRACTOR = False


# Save in csv file given list of experiments
def save_rec_experiments_in_CSV_file(file_path, experiments):
    """
    Save experiments in CSV file

    :type file_path: string
    :param file_path: path of CSV file

    :type experiments: dictionary
    :param experiments: dictionary with experiments
    """

    stream = open(file_path, 'w')

    # Write csv header
    stream.write(ce.EXPERIMENT_NUMBER_KEY + ',' +
                 ce.TEST_SET_PATH_KEY + ',' +
                 ce.EXPERIMENT_ALGORITHM_KEY + ',' +
                 c.LBP_RADIUS_KEY + ',' + c.LBP_NEIGHBORS_KEY + ',' +
                 c.LBP_GRID_X_KEY + ',' + c.LBP_GRID_Y_KEY + ',' +
                 ce.TRAINING_IMAGES_NR_KEY + ',' +
                 c.OFFSET_PCT_X_KEY + ',' + c.OFFSET_PCT_Y_KEY + ',' +
                 c.CROPPED_FACE_HEIGHT_KEY + ',' + 
                 c.CROPPED_FACE_WIDTH_KEY + ',' +
                 ce.USE_NBNN_KEY + ',' +
                 ce.USE_WEIGHTED_REGIONS_KEY + ',' +
                 ce.RECOGNITION_RATE_KEY + ',' +
                 ce.MEAN_PRECISION_KEY + ',' + ce.STD_PRECISION_KEY + ',' +
                 ce.MEAN_RECALL_KEY + ',' + ce.STD_RECALL_KEY + ',' +
                 ce.MEAN_F1_KEY + ',' + ce.STD_F1_KEY + ',' +
                 ce.MEAN_RECOGNITION_TIME_KEY + ',' +
                 ce.MODEL_CREATION_TIME_KEY + '\n')

    for experiment_dict_extended in experiments:
        
        experiment_dict = experiment_dict_extended[ce.EXPERIMENT_KEY]
        
        stream.write(str(experiment_dict[ce.EXPERIMENT_NUMBER_KEY]) + ',' +
                     experiment_dict[ce.TEST_SET_PATH_KEY] + ',' +
                     experiment_dict[ce.EXPERIMENT_ALGORITHM_KEY] + ',' +
                     str(experiment_dict[c.LBP_RADIUS_KEY]) + ',' +
                     str(experiment_dict[c.LBP_NEIGHBORS_KEY]) + ',' +
                     str(experiment_dict[c.LBP_GRID_X_KEY]) + ',' +
                     str(experiment_dict[c.LBP_GRID_Y_KEY]) + ',' +
                     str(experiment_dict[ce.TRAINING_IMAGES_NR_KEY]) + ',' +
                     str(experiment_dict[c.OFFSET_PCT_X_KEY]) + ',' +
                     str(experiment_dict[c.OFFSET_PCT_Y_KEY]) + ',' +
                     str(experiment_dict[c.CROPPED_FACE_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[c.CROPPED_FACE_WIDTH_KEY]) + ',' +
                     str(experiment_dict[ce.USE_NBNN_KEY]) + ',' +
                     str(experiment_dict[ce.USE_WEIGHTED_REGIONS_KEY]) + ',' +
                     str(experiment_dict[ce.RECOGNITION_RATE_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.STD_PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.STD_RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_F1_KEY]) + ',' +
                     str(experiment_dict[ce.STD_F1_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_RECOGNITION_TIME_KEY]) + ',' +
                     str(experiment_dict[ce.MODEL_CREATION_TIME_KEY]) + '\n')
    stream.close()


def fr_test(params, show_results):
    """
    Execute software test on face_recognition module

    :type params: dictionary
    :param params: configuration parameters to be used
                   for the test

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with assigned tag

    :rtype: boolean
    :returns: True if test was successful, False otherwise
    """
    
    image_path = ('..' + os.sep + 'test_files' + os.sep +
                  'face_recognition' + os.sep + 'Test.pgm')
    
    if params is not None and ce.SOFTWARE_TEST_FILE_PATH_KEY in params:

        image_path = params[ce.SOFTWARE_TEST_FILE_PATH_KEY]
    
    test_passed = True
    
    if os.path.isfile(image_path):

        try:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
            recognition_results = recognize_face(
                image, None, params, show_results)
    
            if recognition_results is not None:
                
                error = recognition_results[c.ERROR_KEY]
        
                if not error:
        
                    tag = recognition_results[c.ASSIGNED_TAG_KEY]
        
                    confidence = recognition_results[c.CONFIDENCE_KEY]
        
                    if len(tag) == 0:
                        
                        test_passed = False
        
                    if confidence < 0:
                        test_passed = False
                else:
        
                    test_passed = False
                    
            else:
                
                test_passed = False
    
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
            test_passed = False
        except:
            print "Unexpected error:", sys.exc_info()[0]
            test_passed = False
            raise
            
    else:
        
        print "Software test file does not exist"
        test_passed = False         
        
    return test_passed


def fr_experiments(params, show_results):
    """
    Execute face recognition experiments

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the experiment (see table)

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         images with detected faces

    ============================================  ========================================  ==============================
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============================
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
    test_set_path                                 path of directory
                                                  containing test set
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    aligned_faces_path                            Default path of directory
                                                  for aligned faces
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
    dataset_already_divided                       If True, dataset is already divided       False
                                                  between training and test set
    dataset_path                                  Path of whole dataset, used if dataset
                                                  is not already divided between
                                                  training and test set
    db_name                                       Name of single file
                                                  containing face models
    db_models_path                                Path of directory containing face models
    face_model_algorithm                          Algorithm for face recognition            'LBP'
                                                  ('Eigenfaces', 'Fisherfaces' or 'LBP')
    face_recognition_results_path                 Path of directory where
                                                  test results will be saved
    test_set_path                                 Path of directory containing
                                                  test set
    training_set_path                             Path of directory containing
                                                  training set
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
    software_test_file                            Path of image to be used for
                                                  software test
    training_images_nr                            Number of images per person used in
                                                  training set
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
    ============================================  ========================================  ==============================
    """

    rec_images_nr = 0  # Number of correctly recognized images
    test_images_nr = 0  # Number of total test images
    mean_rec_time = 0

    # List of confidence values for true positives
    true_pos_confidence_list = []
    # List of confidence values for false positives
    false_pos_confidence_list = []

    fm = FaceModels(params)

    training_images_nr = ce.TRAINING_IMAGES_NR

    if params is not None:
        # Number of images for each person to be used for the training
        training_images_nr = params[ce.TRAINING_IMAGES_NR_KEY]

    # Number of people
    people_nr = fm.get_people_nr()

    rec_dict = {}  # Dictionary containing all results for this experiment
    # List used for creating YAML file with list of images
    images_list_for_YAML = []
    # List used for creating YAML file with list of people
    people_list_for_YAML = []

    # List containing recognition rates
    rec_rate_list = []

    # Initialize dictionaries with people
    people_true_positives_dict = {}
    people_false_positives_dict = {}
    people_test_images_nr_dict = {}
    
    tags = fm.get_tags()
    
    for tag in tags:
        
        people_true_positives_dict[tag] = 0
        people_false_positives_dict[tag] = 0
        people_test_images_nr_dict[tag] = 0

    dataset_already_divided = ce.DATASET_ALREADY_DIVIDED

    # directory with test set
    test_set_path = ce.FACE_RECOGNITION_TEST_SET_PATH
    
    if not dataset_already_divided:
        test_set_path = ce.FACE_RECOGNITION_DATASET_PATH
   
    results_path = ce.FACE_RECOGNITION_RESULTS_PATH

    if params is not None:
        # Get path of directories with used files from params
        if ce.DATASET_ALREADY_DIVIDED_KEY in params:
            dataset_already_divided = params[ce.DATASET_ALREADY_DIVIDED_KEY]
        
        if dataset_already_divided:
            if ce.TEST_SET_PATH_KEY in params:
                test_set_path = params[ce.TEST_SET_PATH_KEY]
        else:
            if ce.DATASET_PATH_KEY in params:
                test_set_path = params[ce.DATASET_PATH_KEY]
        
        # directory with results
        if ce.FACE_RECOGNITION_RESULTS_PATH_KEY in params:
            results_path = params[ce.FACE_RECOGNITION_RESULTS_PATH_KEY]

    # Iterate over all directories with images
    images_dirs = os.listdir(test_set_path)

    total_test_images_nr = 0
    for images_dir in images_dirs:

        ann_face_tag = images_dir
        
        images_dir_complete_path = os.path.join(test_set_path, images_dir)

        # Iterate over all images in this directory
        image_counter = 0
        person_test_images = 0
        person_rec_images = 0
        
        for image in os.listdir(images_dir_complete_path):

            # If dataset is not already divided,
            # first training_images_nr images are used for training,
            # the remaining for test
            if(dataset_already_divided
               or (image_counter >= training_images_nr)):

                total_test_images_nr += 1
                person_test_images += 1
                
                # Complete path of image
                image_complete_path = os.path.join(
                    images_dir_complete_path, image)

                try:

                    assigned_tag = 'Undefined'
                    confidence = -1

                    if USE_FACEEXTRACTOR:

                        fe = FaceExtractor(fm, params)

                        handle = fe.extract_faces_from_image(
                            image_complete_path)

                        results = fe.get_results(handle)

                        faces = results[c.FACES_KEY]

                        if len(faces) != 0:
                            face = faces[0]

                            mean_rec_time = (
                                mean_rec_time +
                                results[c.ELAPSED_CPU_TIME_KEY])
                            
                            assigned_tag = face[c.ASSIGNED_TAG_KEY]

                            confidence = face[c.CONFIDENCE_KEY]
                    else:
                        face = cv2.imread(
                            image_complete_path, cv2.IMREAD_GRAYSCALE)

                        sz = None
                        
                        use_resizing = ce.USE_RESIZING
                        use_eyes_position = c.USE_EYES_POSITION
                        use_eye_detection = ce.USE_EYE_DETECTION
                        offset_pct_x = c.OFFSET_PCT_X
                        offset_pct_y = c.OFFSET_PCT_Y
                    
                        if params is not None:
                            if ce.USE_RESIZING_KEY in params:
                                use_resizing = params[ce.USE_RESIZING_KEY]
                            if c.USE_EYES_POSITION_KEY in params:
                                use_eyes_position = (
                                    params[c.USE_EYES_POSITION_KEY])
                            if ce.USE_EYE_DETECTION_KEY in params:
                                use_eye_detection = (
                                    params[ce.USE_EYE_DETECTION_KEY])
                            if c.OFFSET_PCT_X_KEY in params:
                                offset_pct_x = params[c.OFFSET_PCT_X_KEY]
                            if c.OFFSET_PCT_Y_KEY in params:
                                offset_pct_y = params[c.OFFSET_PCT_Y_KEY]  
                        
                        if use_resizing:
                            
                            width = c.CROPPED_FACE_WIDTH
                            height = c.CROPPED_FACE_HEIGHT
                    
                            if params is not None:
                                
                                if c.CROPPED_FACE_WIDTH_KEY in params:
                                    width = params[c.CROPPED_FACE_WIDTH_KEY]
                                
                                if c.CROPPED_FACE_HEIGHT_KEY in params:
                                    height = params[c.CROPPED_FACE_HEIGHT_KEY]
                                
                            sz = (width, height)

                        if use_eyes_position:
                            
                            align_path = c.ALIGNED_FACES_PATH
                            
                            if params is not None:
                                
                                align_path = params[c.ALIGNED_FACES_PATH_KEY]
                            
                            if use_eye_detection:
                                face = fd.get_cropped_face(
                                    image_complete_path, align_path, params,
                                    return_always_face=False)
                            else:
                                face = fd.get_cropped_face_using_fixed_eye_pos(
                                    image_complete_path, align_path, 
                                    offset_pct=(offset_pct_x, offset_pct_y), 
                                    dest_size=sz)

                            if face is not None:
                                face = face[c.FACE_KEY]
                        else:
                            if sz is not None:
                                face = cv2.resize(face, sz)
                        
                        if face is not None:
                        
                            rec_results = recognize_face(
                                face, fm, params, show_results)

                            assigned_tag = rec_results[c.ASSIGNED_TAG_KEY]
                            confidence = rec_results[c.CONFIDENCE_KEY]
                        
                            # Add recognition time to total
                            mean_rec_time = (
                                mean_rec_time +
                                rec_results[c.ELAPSED_CPU_TIME_KEY])

                    image_dict = {ce.IMAGE_KEY: image,
                                  c.ANN_TAG_KEY: images_dir,
                                  c.ASSIGNED_TAG_KEY: assigned_tag,
                                  c.CONFIDENCE_KEY: confidence}
                    
                    if assigned_tag == ann_face_tag:
                        image_dict[ce.PERSON_CHECK_KEY] = 'TP'
                        people_true_positives_dict[assigned_tag] += 1
                        rec_images_nr += 1
                        true_pos_confidence_list.append(confidence)
                        person_rec_images += 1
                    else:
                        image_dict[ce.PERSON_CHECK_KEY] = 'FP'
                        if assigned_tag != 'Undefined':
                            people_false_positives_dict[assigned_tag] += 1
                            false_pos_confidence_list.append(confidence)

                    image_dict_extended = {ce.IMAGE_KEY: image_dict}

                    images_list_for_YAML.append(image_dict_extended)

                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise

            image_counter += 1
            
        people_test_images_nr_dict[ann_face_tag] = person_test_images
        
        person_rec_rate = float(person_rec_images) / person_test_images
        
        rec_rate_list.append(person_rec_rate)

    # Calculate statistics for each person
    people_precision_list = []
    people_recall_list = []
    people_f1_list = []
    
    for tag in tags:

        test_images_nr = people_test_images_nr_dict[tag]
        
        person_true_positives = people_true_positives_dict[tag]
        person_false_positives = people_false_positives_dict[tag]
        
        person_precision = 0
        if person_true_positives != 0:
            person_precision = (
                float(person_true_positives) /
                float(person_true_positives + person_false_positives))
        people_precision_list.append(person_precision)
    
        person_recall = 0
        if test_images_nr != 0:
            person_recall = float(person_true_positives) / test_images_nr
        people_recall_list.append(person_recall)

        person_f1 = 0
        if (person_precision != 0) and (person_recall != 0):
            person_f1 = (2 * (person_precision * person_recall) /
                         (person_precision + person_recall))
        people_f1_list.append(person_f1)

        # Populate dictionary with results for this person
        person_dict = {c.ANN_TAG_KEY: tag,
                       ce.TRUE_POSITIVES_NR_KEY: person_true_positives,
                       ce.FALSE_POSITIVES_NR_KEY: person_false_positives,
                       ce.PRECISION_KEY: person_precision,
                       ce.RECALL_KEY: person_recall, ce.F1_KEY: person_f1}
        people_list_for_YAML.append(person_dict)
    
    mean_rec_rate = float(numpy.mean(rec_rate_list))
    
    mean_precision = float(numpy.mean(people_precision_list))
    std_precision = float(numpy.std(people_precision_list))

    mean_recall = float(numpy.mean(people_recall_list))
    std_recall = float(numpy.std(people_recall_list))

    mean_f1 = float(numpy.mean(people_f1_list))
    std_f1 = float(numpy.std(people_f1_list))

    recognition_rate = float(rec_images_nr) / float(total_test_images_nr)

    mean_rec_time /= total_test_images_nr

    print("\n ### RESULTS ###\n")

    print('Recognition rate: ' + str(recognition_rate * 100) + '%')
    print('Mean of recognition rate: ' + str(mean_rec_rate * 100) + '%')
    print('Mean of precision: ' + str(mean_precision * 100) + '%')
    print('Standard deviation of precision: ' + str(std_precision * 100) + '%')
    print('Mean of recall: ' + str(mean_recall * 100) + '%')
    print('Standard deviation of recall: ' + str(std_recall * 100) + '%')
    print('Mean of f1: ' + str(mean_f1 * 100) + '%')
    print('Standard deviation of f1: ' + str(std_f1 * 100) + '%')
    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')

    print('Recognition rate: ' + str(recognition_rate))
    print('Mean of recognition rate: ' + str(mean_rec_rate))
    print('Mean of precision: ' + str(mean_precision))
    print('Standard deviation of precision: ' + str(std_precision))
    print('Mean of recall: ' + str(mean_recall))
    print('Standard deviation of recall: ' + str(std_recall))
    print('Mean of f1: ' + str(mean_f1))
    print('Standard deviation of f1: ' + str(std_f1))
    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')
    
    if len(true_pos_confidence_list) > 0:
        mean_true_pos_confidence = float(numpy.mean(true_pos_confidence_list))
        std_true_pos_confidence = float(numpy.std(true_pos_confidence_list))
        print('Mean of confidence for true positives: ' +
              str(mean_true_pos_confidence))
        print('Standard deviation of confidence for true positives: ' +
              str(std_true_pos_confidence))
    
    if len(false_pos_confidence_list) > 0:
        mean_false_pos_confidence = float(numpy.mean(false_pos_confidence_list))
        std_false_pos_confidence = float(numpy.std(false_pos_confidence_list))  
        print('Mean of confidence for false positives: ' +
              str(mean_false_pos_confidence))
        print('Standard deviation of confidence for false positives: ' +
              str(std_false_pos_confidence))
    
    # Update YAML file with results related to all the experiments
    number_of_already_done_experiments = 0

    new_experiment_dict = {}
    
    algorithm_name = ce.FACE_MODEL_ALGORITHM
    
    radius = c.LBP_RADIUS
    neighbors = c.LBP_NEIGHBORS
    grid_x = c.LBP_GRID_X
    grid_y = c.LBP_GRID_Y
    training_images_nr = ce.TRAINING_IMAGES_NR
    offset_pct_x = c.OFFSET_PCT_X
    offset_pct_y = c.OFFSET_PCT_Y
    cropped_face_height = c.CROPPED_FACE_HEIGHT
    cropped_face_width = c.CROPPED_FACE_WIDTH
    test_set_path = ce.FACE_RECOGNITION_TEST_SET_PATH
    use_NBNN = ce.USE_NBNN
    use_weighted_regions = ce.USE_WEIGHTED_REGIONS

    if params is not None:
        if ce.FACE_MODEL_ALGORITHM_KEY in params:
            algorithm_name = params[ce.FACE_MODEL_ALGORITHM_KEY]
        if c.LBP_RADIUS_KEY in params:
            radius = params[c.LBP_RADIUS_KEY]
        if c.LBP_NEIGHBORS_KEY in params:
            neighbors = params[c.LBP_NEIGHBORS_KEY]
        if c.LBP_GRID_X_KEY in params:
            grid_x = params[c.LBP_GRID_X_KEY]
        if c.LBP_GRID_Y_KEY in params:
            grid_y = params[c.LBP_GRID_Y_KEY]
        if ce.TRAINING_IMAGES_NR_KEY in params:
            training_images_nr = params[ce.TRAINING_IMAGES_NR_KEY]
        if c.OFFSET_PCT_X_KEY in params:
            offset_pct_x = params[c.OFFSET_PCT_X_KEY]
        if c.OFFSET_PCT_Y_KEY in params:
            offset_pct_y = params[c.OFFSET_PCT_Y_KEY]
        if c.CROPPED_FACE_HEIGHT_KEY in params:
            cropped_face_height = params[c.CROPPED_FACE_HEIGHT_KEY]
        if c.CROPPED_FACE_WIDTH_KEY in params:
            cropped_face_width = params[c.CROPPED_FACE_WIDTH_KEY]
        if ce.TEST_SET_PATH_KEY in params:
            test_set_path = params[ce.TEST_SET_PATH_KEY]
        if ce.USE_NBNN_KEY in params:
            use_NBNN = params[ce.USE_NBNN_KEY]
        if ce.USE_WEIGHTED_REGIONS_KEY in params:
            use_weighted_regions = params[ce.USE_WEIGHTED_REGIONS_KEY]
    
    new_experiment_dict[ce.EXPERIMENT_ALGORITHM_KEY] = algorithm_name
    
    new_experiment_dict[c.LBP_RADIUS_KEY] = radius
    new_experiment_dict[c.LBP_NEIGHBORS_KEY] = neighbors  
    new_experiment_dict[c.LBP_GRID_X_KEY] = grid_x
    new_experiment_dict[c.LBP_GRID_Y_KEY] = grid_y
    new_experiment_dict[ce.TRAINING_IMAGES_NR_KEY] = training_images_nr        
    
    new_experiment_dict[c.OFFSET_PCT_X_KEY] = offset_pct_x
    new_experiment_dict[c.OFFSET_PCT_Y_KEY] = offset_pct_y
    new_experiment_dict[c.CROPPED_FACE_HEIGHT_KEY] = cropped_face_height
    new_experiment_dict[c.CROPPED_FACE_WIDTH_KEY] = cropped_face_width

    new_experiment_dict[ce.USE_NBNN_KEY] = use_NBNN
    new_experiment_dict[ce.USE_WEIGHTED_REGIONS_KEY] = use_weighted_regions

    new_experiment_dict[ce.RECOGNITION_RATE_KEY] = recognition_rate
    new_experiment_dict[ce.MEAN_PRECISION_KEY] = mean_precision
    new_experiment_dict[ce.STD_PRECISION_KEY] = std_precision
    new_experiment_dict[ce.MEAN_RECALL_KEY] = mean_recall
    new_experiment_dict[ce.STD_RECALL_KEY] = std_recall
    new_experiment_dict[ce.MEAN_F1_KEY] = mean_f1
    new_experiment_dict[ce.STD_F1_KEY] = std_f1
    new_experiment_dict[ce.MEAN_RECOGNITION_TIME_KEY] = mean_rec_time
    new_experiment_dict[ce.MODEL_CREATION_TIME_KEY] = fm.model_creation_time
    new_experiment_dict[ce.TEST_SET_PATH_KEY] = test_set_path
    rec_dict[ce.GLOBAL_RESULTS_KEY] = new_experiment_dict
    rec_dict[ce.IMAGES_KEY] = images_list_for_YAML
    rec_dict[ce.PEOPLE_KEY] = people_list_for_YAML

    all_results_YAML_file_path = os.path.join(results_path,
        ce.FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME + '.yml')
    file_check = os.path.isfile(all_results_YAML_file_path)

    experiments = list()
    if file_check:
        experiments = load_experiment_results(all_results_YAML_file_path)
        number_of_already_done_experiments = len(experiments)
        new_experiment_dict[ce.EXPERIMENT_NUMBER_KEY] = (
            number_of_already_done_experiments + 1)
    else:
        new_experiment_dict[ce.EXPERIMENT_NUMBER_KEY] = 1

    new_experiment_dict_extended = {ce.EXPERIMENT_KEY: new_experiment_dict}
    experiments.append(new_experiment_dict_extended)
    experiments_dict = {ce.EXPERIMENTS_KEY: experiments}
    save_YAML_file(all_results_YAML_file_path, experiments_dict)

    # Update csv file with results related to all the experiments
    all_results_CSV_file_path = os.path.join(results_path,
        ce.FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME + '.csv')
    save_rec_experiments_in_CSV_file(all_results_CSV_file_path, experiments)

    # Save file with results related to this experiment
    file_name = 'FaceRecognitionExperiment' + str(
        number_of_already_done_experiments + 1) + 'Results.yml'
    results_file_path = os.path.join(results_path, file_name)
    save_YAML_file(results_file_path, rec_dict)

if __name__ == "__main__":
    
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Execute face recognition tests")
    parser.add_argument("-config", help="configuration file")
    args = parser.parse_args()

    params = None

    if args.config:
        # Load given configuration file
        try:
            params = load_YAML_file(args.config)
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
            print("Default configuration file will be used")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        
    print("\n ### EXECUTING SOFTWARE TEST ###\n")

    test_passed = fr_test(params, False)

    if test_passed:
        print("\nSOFTWARE TEST PASSED\n")
        print("\n ### EXECUTING EXPERIMENTS ###\n")
        fr_experiments(params, False)
    else:
        print("\nSOFTWARE TEST FAILED\n")
