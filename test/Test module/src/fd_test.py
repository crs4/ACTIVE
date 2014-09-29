from os import listdir, path
import cv2
import sys
from sympy import Polygon
sys.path.append("../../..")
from tools.Constants import *
from tools.face_detection import detect_faces_in_image
from tools.Utils import load_experiment_results,load_image_annotations, load_YAML_file, save_YAML_file

# Save in csv file given list of experiments
def save_experiments_in_CSV_file(file_path, experiments):
    stream = open(file_path, 'w')

    # Write csv header
    stream.write(EXPERIMENT_NUMBER_KEY + ',' + EXPERIMENT_ALGORITHM_KEY + ',' +
                 SCALE_FACTOR_KEY + ',' + MIN_NEIGHBORS_KEY + ',' + FLAGS_KEY + ',' +
                 MIN_SIZE_WIDTH_KEY + ',' + MIN_SIZE_HEIGHT_KEY + ',' +
                 PRECISION_KEY + ',' + RECALL_KEY + ',' + F1_KEY + ',' +
                 MEAN_DETECTION_TIME_KEY + '\n')

    for experiment_dict_extended in experiments:
        experiment_dict = experiment_dict_extended[EXPERIMENT_KEY]
        params_dict = experiment_dict[EXPERIMENT_PARAMS_KEY]
        stream.write(str(experiment_dict[EXPERIMENT_NUMBER_KEY]) + ',' +
                     experiment_dict[EXPERIMENT_ALGORITHM_KEY] + ',' +
                     str(params_dict[SCALE_FACTOR_KEY]) + ',' +
                     str(params_dict[MIN_NEIGHBORS_KEY]) + ',' +
                     params_dict[FLAGS_KEY] + ',' +
                     str(params_dict[MIN_SIZE_WIDTH_KEY]) + ',' +
                     str(params_dict[MIN_SIZE_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[PRECISION_KEY]) + ',' +
                     str(experiment_dict[RECALL_KEY]) + ',' +
                     str(experiment_dict[F1_KEY]) + ',' +
                     str(experiment_dict[MEAN_DETECTION_TIME_KEY]) + '\n')
    stream.close()

def fd_test(params, show_results):
    ''' Execute face detection test

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with detected faces
    '''

    if(params == None):
        # Load default configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH)
        
    image_path = SOFTWARE_TEST_FILE_PATH
    if params is not None:
        fd_test_params = params[FACE_DETECTION_KEY]
        image_path = fd_test_params[SOFTWARE_TEST_FILE_KEY]

    test_passed = True

    if os.path.isfile(image_path):
        
        try:
    
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image_width = len(image[0,:])
            image_height = len(image[:,0])
            polygon_image = Polygon((0,0), (image_width, 0), (image_width, image_height), (0, image_height))
            
            # Load face detection parameters
            face_extractor_params = load_YAML_file(FACE_EXTRACTOR_CONFIGURATION_FILE_PATH)
            
            face_detection_params = None
            if face_extractor_params is not None:
                face_detection_params = face_extractor_params[FACE_DETECTION_KEY]
    
            detection_results = detect_faces_in_image(image_path, face_detection_params, show_results)
            
            error = detection_results[ERROR_KEY]
    
            if error is None:
                
                face_rectangles = detection_results[FACES_KEY]
                face_images = detection_results[FACE_IMAGES_KEY]
    
                # Check that rectangles are inside the original image
                face_counter = 0
                for (x, y, width, height) in face_rectangles:
                    polygon_face = Polygon((x,y), (x+width, y), (x+width,y+height), (x, y+height))
                    if(not(polygon_image.encloses(polygon_face))):
                        test_passed = False
                        break
                    face_counter = face_counter + 1
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

def fd_experiments(params, show_results):
    '''
    Execute face detection experiments

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with detected faces
    '''

    if(params == None):
        # Load configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH)
    
    # Folder with test files
    frames_path = FACE_DETECTION_TEST_SET_PATH + os.sep
    # Folder with annotation files
    annotations_path = ANN_PATH + os.sep
    #Folder with results
    results_path = FACE_DETECTION_RESULTS_PATH
    
    if params is not None:
        
        # Get path of directories with used files from params
        fd_test_params = params[FACE_DETECTION_KEY]
        frames_path = fd_test_params[TEST_FILES_PATH_KEY] + os.sep 
        annotations_path = fd_test_params[ANNOTATIONS_PATH_KEY] + os.sep
        results_path = fd_test_params[RESULTS_PATH_KEY] + os.sep
    
    annotated_faces_nr = 0
    true_positives_nr = 0
    false_positives_nr = 0
    mean_detection_time = 0

    detection_dict = {} # Dictionary containing all results for this experiment
    images_list_for_YAML = [] # List used for creating YAML file
    
    # Load face detection parameters
    face_extractor_params = load_YAML_file(FACE_EXTRACTOR_CONFIGURATION_FILE_PATH)
    
    face_detection_params = None
    if face_extractor_params is not None:
        face_detection_params = face_extractor_params[FACE_DETECTION_KEY]

    video_directories = listdir(frames_path)

    # Iterate over all directories with test frames
    global_frame_counter = 0
    for video_dir in video_directories:
        video_dir_complete_path = frames_path + video_dir

        # File with annotations
        annotations_file = annotations_path + video_dir + '_annotations.yml'

        # Load annotations for this video
        frames = load_image_annotations(annotations_file)
        
        if(frames):

	        # Iterate over all frames taken from this video
	        frame_counter = 0
	        for frame_file in listdir(video_dir_complete_path):
	
	            annotations_dict = frames[frame_counter][ANNOTATIONS_FRAME_KEY]
	
	            frame_name = annotations_dict[ANNOTATIONS_FRAME_NAME_KEY]
	
	            # Check that frame name from file with annotations corresponds to file name
	            if(frame_name != frame_file):
	                print('Check failed')
	                print('Frame file: ' + frame_file)
	                print('Frame name from file with annotations: ' + frame_name)
	                continue
	
	            # Set path of frame
	            frame_path = video_dir_complete_path + '\\' + frame_file
	
	            # Call function for face detection
	            detection_results = detect_faces_in_image(frame_path, face_detection_params, show_results)
	
	            # Add detection time to total
	            mean_detection_time = mean_detection_time + detection_results[ELAPSED_CPU_TIME_KEY]
	
	            # Convert opencv rectangles in sympy polygons
	            opencv_detected_faces = detection_results[FACES_KEY]
	            detected_faces = []
	            for (x, y, width, height) in opencv_detected_faces:
	                polygon_face = Polygon((x,y), (x+width, y), (x+width,y+height), (x, y+height))
	                detected_faces.append(polygon_face)
	
	            # Save name of image and number of detected faces in image dictionary
	            detected_faces_nr_in_image = len(detected_faces)
	            image_dict = {}
	            image_dict_extended = {}
	            image_dict[FRAME_NAME_KEY] = frame_name
	            image_dict[DETECTED_FACES_NR_KEY] = detected_faces_nr_in_image
	
	            # Save number of annotated faces in image dictionary
	            annotated_faces_nr_in_image = annotations_dict[ANNOTATIONS_FRAME_FACES_NR_KEY]
	            image_dict[ANNOTATED_FACES_NR_KEY] = annotated_faces_nr_in_image
	
	            annotated_faces = []
	            if(annotated_faces_nr_in_image > 0):
	                annotated_faces = annotations_dict[ANNOTATIONS_FACES_KEY]
	                annotated_faces_nr = annotated_faces_nr + annotated_faces_nr_in_image
	
	            # Compare rectangles and update number of true positives and false positives
	            true_positives_nr_in_image = 0
	
	            detected_faces_list_for_YAML = [] # Array used for creating YAML file
	
	            # Iterate through detected faces
	            for detected_face_rectangle in detected_faces:
	                
	                detected_face_width = int(detected_face_rectangle.vertices[1].x - detected_face_rectangle.vertices[0].x)
	                detected_face_height = int(detected_face_rectangle.vertices[3].y - detected_face_rectangle.vertices[0].y)
	                true_positive = False #True if detected face is a real face
	
	                # Check if detected face contains one of the annotated faces.
	                # Width of detected face must not be more than 4 times width of correctly annotated face.
	                for annotated_face_dict_extended in annotated_faces:
	                    annotated_face_dict = annotated_face_dict_extended[ANNOTATIONS_FACE_KEY]
	                    x = annotated_face_dict[FACE_X_KEY]
	                    y = annotated_face_dict[FACE_Y_KEY]
	                    width = annotated_face_dict[FACE_WIDTH_KEY]
	                    height = annotated_face_dict[FACE_HEIGHT_KEY]
	                    annotated_face_rectangle = Polygon((x,y), (x+width,y), (x+width,y+height), (x, y+height)) # Create sympy rectangle
	
	                    if(detected_face_rectangle.encloses(annotated_face_rectangle) and (detected_face_width <= 4 * width)):
	                        true_positive = True
	                        true_positives_nr = true_positives_nr + 1
	                        true_positives_nr_in_image = true_positives_nr_in_image + 1
	
	                        # Each face must be considered once
	                        annotated_faces.remove(annotated_face_dict_extended)
	                        break
	
	                # Save position and size of detected face in face dictionary and add this to list
	                detected_face_dict_extended = {}
	                detected_face_dict = {}
	                detected_face_dict[FACE_X_KEY] = int(detected_face_rectangle.vertices[0].x)
	                detected_face_dict[FACE_Y_KEY] = int(detected_face_rectangle.vertices[0].y)
	                detected_face_dict[FACE_WIDTH_KEY] = detected_face_width
	                detected_face_dict[FACE_HEIGHT_KEY] = detected_face_height
	
	                # Save check result
	                if(true_positive):
	                    detected_face_dict[FACE_CHECK_KEY] = 'TP' # Face is a true positive detection
	                else:
	                    detected_face_dict[FACE_CHECK_KEY] = 'FP' # Face is a false positive detection
	
	                detected_face_dict_extended[FACE_DETECTIONS_FACE_KEY] = detected_face_dict
	                detected_faces_list_for_YAML.append(detected_face_dict_extended)
	
	            false_positives_nr_in_image = detected_faces_nr_in_image - true_positives_nr_in_image
	            image_dict[TRUE_POSITIVES_NR_KEY] = true_positives_nr_in_image
	            image_dict[FALSE_POSITIVES_NR_KEY] = false_positives_nr_in_image
	
	            false_positives_nr = false_positives_nr + false_positives_nr_in_image
	
	            if(len(detected_faces_list_for_YAML) > 0):
	                image_dict[FACE_DETECTIONS_FACES_KEY] = detected_faces_list_for_YAML
	
	            image_dict_extended[FACE_DETECTIONS_FRAME_KEY] = image_dict
	
	            images_list_for_YAML.append(image_dict_extended)
	
	            frame_counter = frame_counter + 1
	            global_frame_counter = global_frame_counter + 1
	            
	if(global_frame_counter > 0):
		
	    detection_dict[FRAMES_KEY] = images_list_for_YAML
	
	    # Save check results
	    detection_dict[ANNOTATED_FACES_NR_KEY] = annotated_faces_nr
	    detection_dict[TRUE_POSITIVES_NR_KEY] = true_positives_nr
	    detection_dict[FALSE_POSITIVES_NR_KEY] = false_positives_nr
	
	    precision = 0
	    if(true_positives_nr != 0):
	        precision = float(true_positives_nr) / (float(true_positives_nr + false_positives_nr))
	
	    recall = 0
	    if(annotated_faces_nr != 0):
	        recall = float(true_positives_nr) / float(annotated_faces_nr)
	
	    f1 = 0
	    if((precision + recall) != 0):
	        f1 = 2 * (precision * recall) / (precision + recall)
	
	    detection_dict[PRECISION_KEY] = precision
	    detection_dict[RECALL_KEY] = recall
	    detection_dict[F1_KEY] = f1
	
	    mean_detection_time = mean_detection_time / global_frame_counter
	
	    detection_dict[MEAN_DETECTION_TIME_KEY] = mean_detection_time
	
	    print("\n ### RESULTS ###\n")
	
	    print('Precision: ' + str(precision*100) + '%')
	    print('Recall: ' + str(recall*100) + '%')
	    print('F1: ' + str(f1*100) + '%')
	    print('Mean detection time: ' + str(mean_detection_time) + ' s\n\n')
	
	    # Update YAML file with results related to all the experiments
	    number_of_already_done_experiments = 0
	
	    new_experiment_dict = {}
	    # Save algorithm name
	    algorithm_name = face_detection_params[ALGORITHM_KEY]
	    new_experiment_dict[EXPERIMENT_ALGORITHM_KEY] = algorithm_name
	
	    # Save classification parameters
	    new_experiment_dict[EXPERIMENT_PARAMS_KEY] = face_detection_params
	
	    # Save results
	    new_experiment_dict[PRECISION_KEY] = precision
	    new_experiment_dict[RECALL_KEY] = recall
	    new_experiment_dict[F1_KEY] = f1
	    new_experiment_dict[MEAN_DETECTION_TIME_KEY] = mean_detection_time
	
	    all_results_YAML_file_path = results_path + EXPERIMENT_RESULTS_FILE_NAME + '.yml'
	    file_check = path.isfile(all_results_YAML_file_path)
	
	    experiments = list()
	    if(file_check):
	        experiments = load_experiment_results(all_results_YAML_file_path)
	        number_of_already_done_experiments = len(experiments)
	        new_experiment_dict[EXPERIMENT_NUMBER_KEY] = number_of_already_done_experiments + 1
	
	    else:
	        new_experiment_dict[EXPERIMENT_NUMBER_KEY] = 1
	
	    new_experiment_dict_extended = {}
	    new_experiment_dict_extended[EXPERIMENT_KEY] = new_experiment_dict
	    experiments.append(new_experiment_dict_extended)
	    experiments_dict = {}
	    experiments_dict[EXPERIMENTS_KEY] = experiments
	    save_YAML_file(all_results_YAML_file_path, experiments_dict)
	
	    # Update csv file with results related to all the experiments
	    all_results_CSV_file_path = results_path + EXPERIMENT_RESULTS_FILE_NAME + '.csv'
	    save_experiments_in_CSV_file(all_results_CSV_file_path, experiments)
	
	    # Save file with results related to this experiment
	    results_file_path = results_path + 'FaceDetectionExperiment' + str(number_of_already_done_experiments + 1) + 'Results.yml'
	    result = save_YAML_file(results_file_path, detection_dict)
	    
	else:
		
		print 'No image was analyzed'

if __name__ == "__main__":
    
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description = "Execute face detection tests")
    parser.add_argument("-config", help = "configuration file")
    args = parser.parse_args()

    if(args.config):
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

    params = None

    test_passed = fd_test(params, False)

    if(test_passed):
        print("\nSOFTWARE TEST PASSED\n")
        print("\n ### EXECUTING EXPERIMENTS ###\n")
        fd_experiments(params, True)
    else:
        print("\nSOFTWARE TEST FAILED\n")

