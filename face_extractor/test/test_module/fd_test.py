import cv2
import os
import shutil
import sys

import constants_for_experiments as ce
import utils_for_experiments as utilse

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.face_detection import detect_faces_in_image
import tools.utils as utils


# Save in csv file given list of experiments
def save_experiments_in_CSV_file(file_path, experiments):
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
                 ce.EXPERIMENT_ALGORITHM_KEY + ',' +
                 c.CHECK_EYE_POSITIONS_KEY + ',' +
                 c.EYE_DETECTION_CLASSIFIER_KEY + ',' +
                 c.FLAGS_KEY + ',' +
                 c.MIN_NEIGHBORS_KEY + ',' +
                 c.MIN_SIZE_WIDTH_KEY + ',' +
                 c.MIN_SIZE_HEIGHT_KEY + ',' +
                 c.SCALE_FACTOR_KEY + ',' +
                 c.MAX_EYE_ANGLE_KEY + ',' +
                 c.MIN_EYE_DISTANCE_KEY + ',' +
                 c.NOSE_DETECTION_CLASSIFIER_KEY + ',' +
                 c.USE_NOSE_POS_IN_DETECTION_KEY + ',' +
                 ce.PRECISION_KEY + ',' +
                 ce.RECALL_KEY + ',' +
                 ce.F1_KEY + ',' +
                 ce.MEAN_DETECTION_TIME_KEY + '\n')

    for experiment_dict_extended in experiments:
        print('experiment_dict_extended', experiment_dict_extended)
        experiment_dict = experiment_dict_extended[ce.EXPERIMENT_KEY]
        params_dict = experiment_dict[ce.EXPERIMENT_PARAMS_KEY]
        stream.write(str(experiment_dict[ce.EXPERIMENT_NUMBER_KEY]) + ',' +
                     experiment_dict[ce.EXPERIMENT_ALGORITHM_KEY] + ',' +
                     str(params_dict[c.CHECK_EYE_POSITIONS_KEY]) + ',' +
                     str(params_dict[c.EYE_DETECTION_CLASSIFIER_KEY]) + ',' +
                     params_dict[c.FLAGS_KEY] + ',' +
                     str(params_dict[c.MIN_NEIGHBORS_KEY]) + ',' +
                     str(params_dict[c.MIN_SIZE_WIDTH_KEY]) + ',' +
                     str(params_dict[c.MIN_SIZE_HEIGHT_KEY]) + ',' +
                     str(params_dict[c.SCALE_FACTOR_KEY]) + ',' +
                     str(params_dict[c.MAX_EYE_ANGLE_KEY]) + ',' +
                     str(params_dict[c.MIN_EYE_DISTANCE_KEY]) + ',' +
                     str(params_dict[c.NOSE_DETECTION_CLASSIFIER_KEY]) + ',' +
                     str(params_dict[c.USE_NOSE_POS_IN_DETECTION_KEY]) + ',' +
                     str(experiment_dict[ce.PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.F1_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_DETECTION_TIME_KEY]) + '\n')
    stream.close()


def fd_test(params=None, show_results=False):
    """
    Execute software test on face_detection module

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with detected faces

    :rtype: boolean
    :returns: True if test was successful, False otherwise

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

    image_path = ('..' + os.sep + 'test_files' + os.sep +
                  'face_detection' + os.sep + 'Test.jpg')

    if params and (ce.SOFTWARE_TEST_FILE_PATH_KEY in params):
        image_path = params[ce.SOFTWARE_TEST_FILE_PATH_KEY]

    test_passed = True

    if os.path.isfile(image_path):
        
        try:
    
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image_width = len(image[0, :])
            image_height = len(image[:, 0])
            rect_image = [0, 0, image_width, image_height]
    
            aligned_faces_path = os.path.join(
            ce.ACTIVE_ROOT_DIRECTORY, c.ALIGNED_FACES_DIR)
            
            if (params is not None) and (ce.ALIGNED_FACES_PATH_KEY in params):
                
                aligned_faces_path = params[ce.ALIGNED_FACES_PATH_KEY]
            
            if not(os.path.exists(aligned_faces_path)):
            
                os.makedirs(aligned_faces_path)
    
            detection_results = detect_faces_in_image(
            image_path, aligned_faces_path, params, show_results)
            
            shutil.rmtree(aligned_faces_path)
            
            error = detection_results[c.ERROR_KEY]
    
            if error is None:
    
                faces = detection_results[c.FACES_KEY]
    
                # Check that rectangles are inside the original image
                face_counter = 0
                for face in faces:
                    
                    rect_face = face[c.BBOX_KEY]
                    
                    if not(utils.is_rect_enclosed(rect_face, rect_image)):
                        test_passed = False
                        break
                    face_counter += 1
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


def fd_experiments(params=None, show_results=False):
    """
    Execute face detection experiments

    :type params: dictionary
    :param params: configuration parameters to be used for the experiment (see table)

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with detected faces

    ============================================  ========================================  =============================
    Key                                           Value                                     Default value
    ============================================  ========================================  =============================
    annotations_path                              Path of directory containing the
                                                  manual annotations for the images
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
    face_detection_results_path                   Path of directory where
                                                  test results will be saved
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    max_eye_angle                                 Maximum inclination of the line           0.125
                                                  connecting the eyes
                                                  (in % of pi radians)
    min_eye_distance                              Minimum distance between eyes             0.25
                                                  (in % of the width of the face
                                                  bounding box)
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    test_set_path                                 Path of directory
                                                  containing test set
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    ============================================  ========================================  =============================
    """
    
    # Folder with test files
    frames_path = ce.FACE_DETECTION_TEST_SET_PATH + os.sep
    # Folder with annotation files
    annotations_path = ce.FACE_DETECTION_ANN_PATH + os.sep
    # Folder with results
    results_path = ce.FACE_DETECTION_RESULTS_PATH + os.sep
    
    if params is not None:
        
        # Get path of directories with used files from params
        if ce.TEST_SET_PATH_KEY in params:
            frames_path = params[ce.TEST_SET_PATH_KEY] + os.sep
        if ce.ANNOTATIONS_PATH_KEY in params:
            annotations_path = params[ce.ANNOTATIONS_PATH_KEY] + os.sep
        if ce.FACE_DETECTION_RESULTS_PATH_KEY in params:
            results_path = params[ce.FACE_DETECTION_RESULTS_PATH_KEY] + os.sep
    
    annotated_faces_nr = 0
    true_positives_nr = 0
    false_positives_nr = 0
    mean_detection_time = 0

    # Dictionary containing all results for this experiment
    detection_dict = {}

    images_list_for_YAML = []  # List used for creating YAML file
    
    # Name of used algorithm for face detection
    algorithm_name = c.FACE_DETECTION_ALGORITHM_KEY
    
    if (params is not None) and (c.FACE_DETECTION_ALGORITHM_KEY in params):
        
        algorithm_name = params[c.FACE_DETECTION_ALGORITHM_KEY]

    video_directories = os.listdir(frames_path)

    # Iterate over all directories with test frames
    global_frame_counter = 0
    for video_dir in video_directories:
        video_dir_complete_path = frames_path + video_dir

        # File with annotations
        annotations_file = annotations_path + video_dir + '_annotations.yml'

        # Load annotations for this video
        frames = utilse.load_image_annotations(annotations_file)
        
        if frames:

            # Directory where aligned faces are saved
            aligned_faces_path = os.path.join(
            ce.ACTIVE_ROOT_DIRECTORY, c.ALIGNED_FACES_DIR)
            
            if (params is not None) and (c.ALIGNED_FACES_PATH_KEY in params):
                
                aligned_faces_path = params[c.ALIGNED_FACES_PATH_KEY]
            
            if not(os.path.exists(aligned_faces_path)):
            
                os.makedirs(aligned_faces_path)

            # Iterate over all frames taken from this video
            frame_counter = 0
            for frame_file in os.listdir(video_dir_complete_path):
    
                annotations_dict = (
                    frames[frame_counter][ce.ANNOTATIONS_FRAME_KEY])
    
                frame_name = annotations_dict[ce.ANNOTATIONS_FRAME_NAME_KEY]
    
                # Check that frame name from file with annotations
                # corresponds to file name
                if frame_name != frame_file:
                    print('Check failed')
                    print('Frame file: ' + frame_file)
                    print(
                        'Frame name from file with annotations: ' + frame_name)
                    continue
    
                # Set path of frame
                frame_path = video_dir_complete_path + '\\' + frame_file
    
                # Call function for face detection
                detection_results = detect_faces_in_image(
                frame_path, aligned_faces_path, params, show_results)
    
                # Add detection time to total
                mean_detection_time += detection_results[c.ELAPSED_CPU_TIME_KEY]
    
                detected_faces = detection_results[c.FACES_KEY]
    
                # Save name of image and number
                # of detected faces in image dictionary
                detected_faces_nr_in_im = len(detected_faces)
                image_dict = {}
                image_dict_extended = {}
                image_dict[ce.FRAME_NAME_KEY] = frame_name
                image_dict[ce.DETECTED_FACES_NR_KEY] = detected_faces_nr_in_im
    
                # Save number of annotated faces in image dictionary
                ann_faces_nr_in_im = (
                    annotations_dict[ce.ANNOTATIONS_FRAME_FACES_NR_KEY])
                image_dict[ce.ANNOTATED_FACES_NR_KEY] = ann_faces_nr_in_im
    
                annotated_faces = []
                if ann_faces_nr_in_im > 0:
                    annotated_faces = annotations_dict[ce.ANNOTATIONS_FACES_KEY]
                    annotated_faces_nr = annotated_faces_nr + ann_faces_nr_in_im
    
                # Compare rectangles
                # and update number of true positives and false positives
                true_pos_nr_in_image = 0
    
                # Array used for creating YAML file
                detected_faces_list_for_YAML = []
    
                # Iterate through detected faces
                for detected_face in detected_faces:
                    
                    detected_face_rectangle = detected_face[c.BBOX_KEY]
                    
                    detected_face_width = detected_face_rectangle[2]
                    detected_face_height = detected_face_rectangle[3]
                    # True if detected face is a real face
                    true_positive = False
    
                    # Check if detected face
                    # contains one of the annotated faces.
                    # Width of detected face must not be more
                    # than 4 times width of correctly annotated face.
                    for ann_face_dict_extended in annotated_faces:
                        annotated_face_dict = (
                            ann_face_dict_extended[ce.ANNOTATIONS_FACE_KEY])
                        x = annotated_face_dict[ce.FACE_X_KEY]
                        y = annotated_face_dict[ce.FACE_Y_KEY]
                        width = annotated_face_dict[ce.FACE_WIDTH_KEY]
                        height = annotated_face_dict[ce.FACE_HEIGHT_KEY]
                        # Create annotated face rectangle
                        annotated_face_rectangle = [x, y, width, height]
                        
                        if utils.is_rect_enclosed(
                                annotated_face_rectangle,
                                detected_face_rectangle) \
                                and (detected_face_width <= 4 * width):
                            true_positive = True
                            true_positives_nr += 1
                            true_pos_nr_in_image += 1
    
                            # Each face must be considered once
                            annotated_faces.remove(ann_face_dict_extended)
                            break
    
                    # Save position and size of detected face in face dictionary
                    # and add this to list
                    detected_face_dict_extended = {}
                    detected_face_dict = {
                    ce.FACE_X_KEY: int(detected_face_rectangle[0]),
                    ce.FACE_Y_KEY: int(detected_face_rectangle[1]),
                    ce.FACE_WIDTH_KEY: int(detected_face_width),
                    ce.FACE_HEIGHT_KEY: int(detected_face_height)}

                    # Save check result
                    if true_positive:
                        # Face is a true positive detection
                        detected_face_dict[ce.FACE_CHECK_KEY] = 'TP'
                    else:
                        # Face is a false positive detection
                        detected_face_dict[ce.FACE_CHECK_KEY] = 'FP'
    
                    detected_face_dict_extended[c.FACE_KEY] = detected_face_dict
                    detected_faces_list_for_YAML.append(
                        detected_face_dict_extended)
    
                false_pos_nr_in_image = (
                    detected_faces_nr_in_im - true_pos_nr_in_image)
                image_dict[ce.TRUE_POSITIVES_NR_KEY] = true_pos_nr_in_image
                image_dict[ce.FALSE_POSITIVES_NR_KEY] = false_pos_nr_in_image

                false_positives_nr += false_pos_nr_in_image
    
                if len(detected_faces_list_for_YAML) > 0:
                    image_dict[c.FACES_KEY] = detected_faces_list_for_YAML
    
                image_dict_extended[ce.FRAME_KEY] = image_dict
    
                images_list_for_YAML.append(image_dict_extended)

                frame_counter += 1
                global_frame_counter += 1
            
            shutil.rmtree(aligned_faces_path)
                
    if global_frame_counter > 0:
        
        detection_dict[c.FRAMES_KEY] = images_list_for_YAML
    
        # Save check results
        detection_dict[ce.ANNOTATED_FACES_NR_KEY] = annotated_faces_nr
        detection_dict[ce.TRUE_POSITIVES_NR_KEY] = true_positives_nr
        detection_dict[ce.FALSE_POSITIVES_NR_KEY] = false_positives_nr
    
        precision = 0
        if true_positives_nr != 0:
            precision = (float(true_positives_nr) /
                         (float(true_positives_nr + false_positives_nr)))
    
        recall = 0
        if annotated_faces_nr != 0:
            recall = float(true_positives_nr) / float(annotated_faces_nr)
    
        f1 = 0
        if (precision + recall) != 0:
            f1 = 2 * (precision * recall) / (precision + recall)
    
        detection_dict[ce.PRECISION_KEY] = precision
        detection_dict[ce.RECALL_KEY] = recall
        detection_dict[ce.F1_KEY] = f1

        mean_detection_time /= global_frame_counter
    
        detection_dict[ce.MEAN_DETECTION_TIME_KEY] = mean_detection_time
    
        print("\n ### RESULTS ###\n")
    
        print('Precision: ' + str(precision * 100) + '%')
        print('Recall: ' + str(recall * 100) + '%')
        print('F1: ' + str(f1 * 100) + '%')
        print('Mean detection time: ' + str(mean_detection_time) + ' s\n\n')
    
        # Update YAML file with results related to all the experiments
        number_of_already_done_experiments = 0
    
        new_experiment_dict = {ce.EXPERIMENT_ALGORITHM_KEY: algorithm_name}
        # Save algorithm name

        # Save classification parameters
        exp_params = {
            c.CHECK_EYE_POSITIONS_KEY: c.CHECK_EYE_POSITIONS,
            c.EYE_DETECTION_CLASSIFIER_KEY: c.EYE_DETECTION_CLASSIFIER,
            c.FACE_DETECTION_ALGORITHM_KEY: c.FACE_DETECTION_ALGORITHM,
            c.FLAGS_KEY: c.FACE_DETECTION_FLAGS,
            c.MIN_NEIGHBORS_KEY: c.FACE_DETECTION_MIN_NEIGHBORS,
            c.MIN_SIZE_HEIGHT_KEY: c.FACE_DETECTION_MIN_SIZE_HEIGHT,
            c.MIN_SIZE_WIDTH_KEY: c.FACE_DETECTION_MIN_SIZE_WIDTH,
            c.SCALE_FACTOR_KEY: c.FACE_DETECTION_SCALE_FACTOR,
            c.MAX_EYE_ANGLE_KEY: c.MAX_EYE_ANGLE,
            c.MIN_EYE_DISTANCE_KEY: c.MIN_EYE_DISTANCE,
            c.NOSE_DETECTION_CLASSIFIER_KEY: c.NOSE_DETECTION_CLASSIFIER,
            c.USE_NOSE_POS_IN_DETECTION_KEY: c.USE_NOSE_POS_IN_DETECTION
        }

        if params is not None:
            if c.CHECK_EYE_POSITIONS_KEY in params:
                exp_params[c.CHECK_EYE_POSITIONS_KEY] = (
                    params[c.CHECK_EYE_POSITIONS_KEY])
            if c.EYE_DETECTION_CLASSIFIER_KEY in params:
                exp_params[c.EYE_DETECTION_CLASSIFIER_KEY] = (
                    params[c.EYE_DETECTION_CLASSIFIER_KEY])
            if c.FACE_DETECTION_ALGORITHM_KEY in params:
                exp_params[c.FACE_DETECTION_ALGORITHM_KEY] = (
                    params[c.FACE_DETECTION_ALGORITHM_KEY])
            if c.FLAGS_KEY in params:
                exp_params[c.FLAGS_KEY] = params[c.FLAGS_KEY]
            if c.MIN_NEIGHBORS_KEY in params:
                exp_params[c.MIN_NEIGHBORS_KEY] = params[c.MIN_NEIGHBORS_KEY]
            if c.MIN_SIZE_HEIGHT_KEY in params:
                exp_params[c.MIN_SIZE_HEIGHT_KEY] = (
                    params[c.MIN_SIZE_HEIGHT_KEY])
            if c.MIN_SIZE_WIDTH_KEY in params:
                exp_params[c.MIN_SIZE_WIDTH_KEY] = params[c.MIN_SIZE_WIDTH_KEY]
            if c.SCALE_FACTOR_KEY in params:
                exp_params[c.SCALE_FACTOR_KEY] = params[c.SCALE_FACTOR_KEY]
            if c.MAX_EYE_ANGLE_KEY in params:
                exp_params[c.MAX_EYE_ANGLE_KEY] = params[c.MAX_EYE_ANGLE_KEY]
            if c.MIN_EYE_DISTANCE_KEY in params:
                exp_params[c.MIN_EYE_DISTANCE_KEY] = (
                    params[c.MIN_EYE_DISTANCE_KEY])
            if c.NOSE_DETECTION_CLASSIFIER_KEY in params:
                exp_params[c.NOSE_DETECTION_CLASSIFIER_KEY] = (
                    params[c.NOSE_DETECTION_CLASSIFIER_KEY])
            if c.USE_NOSE_POS_IN_DETECTION_KEY in params:
                exp_params[c.USE_NOSE_POS_IN_DETECTION_KEY] = (
                    params[c.USE_NOSE_POS_IN_DETECTION_KEY])

        new_experiment_dict[ce.EXPERIMENT_PARAMS_KEY] = exp_params
    
        # Save results
        new_experiment_dict[ce.PRECISION_KEY] = precision
        new_experiment_dict[ce.RECALL_KEY] = recall
        new_experiment_dict[ce.F1_KEY] = f1
        new_experiment_dict[ce.MEAN_DETECTION_TIME_KEY] = mean_detection_time
    
        all_results_YAML_file_path = (
            results_path + ce.EXPERIMENT_RESULTS_FILE_NAME + '.yml')
        file_check = os.path.isfile(all_results_YAML_file_path)
    
        experiments = list()
        if file_check:
            experiments = utilse.load_experiment_results(
                all_results_YAML_file_path)
            number_of_already_done_experiments = len(experiments)
            new_experiment_dict[ce.EXPERIMENT_NUMBER_KEY] = (
                number_of_already_done_experiments + 1)
    
        else:
            new_experiment_dict[ce.EXPERIMENT_NUMBER_KEY] = 1
    
        new_experiment_dict_extended = {ce.EXPERIMENT_KEY: new_experiment_dict}
        experiments.append(new_experiment_dict_extended)
        experiments_dict = {ce.EXPERIMENTS_KEY: experiments}
        utils.save_YAML_file(all_results_YAML_file_path, experiments_dict)
    
        # Update csv file with results related to all the experiments
        all_results_CSV_file_path = (
            results_path + ce.EXPERIMENT_RESULTS_FILE_NAME + '.csv')
        save_experiments_in_CSV_file(all_results_CSV_file_path, experiments)
    
        # Save file with results related to this experiment
        results_file_path = results_path + 'FaceDetectionExperiment' + str(
            number_of_already_done_experiments + 1) + 'Results.yml'
        utils.save_YAML_file(results_file_path, detection_dict)
        
    else:
        
        print 'No image was analyzed'

if __name__ == "__main__":
    
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Execute face detection tests")
    parser.add_argument("-config", help="configuration file")
    args = parser.parse_args()

    params = None

    if args.config:
        # Load given configuration file
        try:
            params = utils.load_YAML_file(args.config)
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
            print("Default configuration file will be used")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        
    print("\n ### EXECUTING SOFTWARE TEST ###\n")

    test_passed = fd_test(params, False)

    if test_passed:
        print("\nSOFTWARE TEST PASSED\n")
        print("\n ### EXECUTING EXPERIMENTS ###\n")
        fd_experiments(params, False)
    else:
        print("\nSOFTWARE TEST FAILED\n")
