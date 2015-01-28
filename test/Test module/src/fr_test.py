import cv2
import numpy
import sys
sys.path.append("../../..")
from os import listdir, path
from tools.Constants import *
from tools.face_detection import get_cropped_face, get_cropped_face_using_eyes_pos
from tools.face_extractor import FaceExtractor
from tools.face_recognition import recognize_face
from tools.FaceModelsLBP import FaceModelsLBP
from tools.Utils import load_experiment_results,load_image_annotations, load_YAML_file, save_YAML_file

USE_FACEEXTRACTOR = False # True if recognition is carried out by using FaceExtractor class

# Save in csv file given list of experiments
def save_rec_experiments_in_CSV_file(file_path, experiments):
    stream = open(file_path, 'w')

    # Write csv header
    stream.write(EXPERIMENT_NUMBER_KEY + ',' + EXPERIMENT_ALGORITHM_KEY + ',' +
                 RECOGNITION_RATE_KEY + ',' +
                 MEAN_PRECISION_KEY + ',' + STD_PRECISION_KEY + ',' +
                 MEAN_RECALL_KEY + ',' + STD_RECALL_KEY + ',' +
                 MEAN_F1_KEY + ',' + STD_F1_KEY + ',' +
                 MEAN_RECOGNITION_TIME_KEY + '\n')

    for experiment_dict_extended in experiments:
        experiment_dict = experiment_dict_extended[EXPERIMENT_KEY]
        stream.write(str(experiment_dict[EXPERIMENT_NUMBER_KEY]) + ',' +
                     experiment_dict[EXPERIMENT_ALGORITHM_KEY] + ',' +
                     str(experiment_dict[RECOGNITION_RATE_KEY]) + ',' +
                     str(experiment_dict[MEAN_PRECISION_KEY]) + ',' +
                     str(experiment_dict[STD_PRECISION_KEY]) + ',' +
                     str(experiment_dict[MEAN_RECALL_KEY]) + ',' +
                     str(experiment_dict[STD_RECALL_KEY]) + ',' +
                     str(experiment_dict[MEAN_F1_KEY]) + ',' +
                     str(experiment_dict[STD_F1_KEY]) + ',' +
                     str(experiment_dict[MEAN_RECOGNITION_TIME_KEY]) + '\n')
    stream.close()

def fr_test(params, show_results):
    ''' Execute face recognition test

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with assigned tag
    '''
    
    image_path = SOFTWARE_TEST_FILE_PATH
    
    if params is not None:

        image_path = params[SOFTWARE_TEST_FILE_KEY]
    
    test_passed = True
    
    if os.path.isfile(image_path):

        try:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
            # Load face recognition parameters
    
            recognition_results = recognize_face(image, None, params, show_results)
    
            error = recognition_results[ERROR_KEY]
    
            if(len(error) == 0):
    
                tag = recognition_results[ASSIGNED_TAG_KEY]
    
                confidence = recognition_results[CONFIDENCE_KEY]
    
				if(len(tag) == 0):
					
					test_passed = False
    
                if(confidence < 0):
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
    '''
    Execute face recognition experiments

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) images with detected faces
    '''

    rec_images_nr = 0 # Number of correctly recognized images
    test_images_nr = 0 # Number of total test images
    mean_rec_time = 0

    true_pos_confidence_list = [] # List of confidence values for true positives
    false_pos_confidence_list = [] # List of confidence values for false positives

    fm = FaceModelsLBP()

    # Total number of images for each person
    person_images_nr = params[PERSON_IMAGES_NR_KEY]

    # Number of images for each person to be used for the training
    training_images_nr = params[TRAINING_IMAGES_NR_KEY]
    
    # Number of images for each person to be used for the test
    test_images_nr = person_images_nr - training_images_nr

    # Number of people
    people_nr = fm.get_people_nr()

    rec_dict = {} # Dictionary containing all results for this experiment
    images_list_for_YAML = [] # List used for creating YAML file with list of images
    people_list_for_YAML = [] # List used for creating YAML file with list of people

    # Initialize dictionaries with people
    people_true_positives_dict = {}
    people_false_positives_dict = {}
    people_test_images_nr_dict = {}
    
    tags = fm.get_tags()
    
    for tag in tags:
		
        people_true_positives_dict[tag] = 0
        people_false_positives_dict[tag] = 0

    # Get path of directories with used files from params
    test_set_path = None # directory with test set

    dataset_already_divided = params[DATASET_ALREADY_DIVIDED_KEY]
    
    if(dataset_already_divided):
        training_set_path = params[TRAINING_SET_PATH_KEY] + '\\'
        test_set_path = params[TEST_SET_PATH_KEY] + '\\'
    else:
        test_set_path = params[DATASET_PATH_KEY] + '\\'
    
    results_path = params[RESULTS_PATH_KEY] + '\\' # directory with results

    # Iterate over all directories with images
    images_dirs = listdir(test_set_path)

    total_test_images_nr = 0
    for images_dir in images_dirs:

        ann_face_tag = images_dir

        print('ann_face_tag: ', ann_face_tag)
        
        images_dir_complete_path = test_set_path + images_dir

        # Iterate over all images in this directory
        image_counter = 0
        for image in listdir(images_dir_complete_path):

            # If dataset is not already divided, first training_images_nr images are used for training, the remaining for test
            if((dataset_already_divided) or (image_counter >= training_images_nr)):

                total_test_images_nr = total_test_images_nr + 1
                
                # Complete path of image
                image_complete_path = images_dir_complete_path + '\\' + image

                try:

                    assigned_tag = 'Undefined'
                    confidence = -1

                    if(USE_FACEEXTRACTOR):

                        fe = FaceExtractor(fm)

                        handle = fe.extractFacesFromImage(image_complete_path)

                        results = fe.getResults(handle)

                        faces = results[FACES_KEY]

                        if(len(faces) != 0):
                            face = faces[0]

                            mean_rec_time = mean_rec_time + results[ELAPSED_CPU_TIME_KEY]
                            
                            assigned_tag = face[ASSIGNED_TAG_KEY]

                            confidence = face[CONFIDENCE_KEY]
                    else:
                        #print 'test image:', image_complete_path
                        face = cv2.imread(image_complete_path, cv2.IMREAD_GRAYSCALE)

                        sz = None
                        if(USE_RESIZING):
                            sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)

                        if(USE_EYES_POSITION):
                            if(USE_EYE_DETECTION):
                                face = get_cropped_face(image_complete_path, offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y), dest_size = sz, return_always_face = False)
                            else:
                                face = get_cropped_face_using_eyes_pos(image_complete_path, offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y), dest_size = sz)
                        else:
                            if (sz is not None):
                                face = cv2.resize(face, sz)
                    
                        rec_results = recognize_face(face, fm, params, show_results)

                        # Add recognition time to total
                        mean_rec_time = mean_rec_time + rec_results[ELAPSED_CPU_TIME_KEY]
                    
                        assigned_tag = rec_results[ASSIGNED_TAG_KEY]
                        confidence = rec_results[CONFIDENCE_KEY]

                    image_dict = {}

                    image_dict[IMAGE_KEY] = image
                    image_dict[ANN_TAG_KEY] = images_dir
                    image_dict[ASSIGNED_TAG_KEY] = assigned_tag
                    image_dict[CONFIDENCE_KEY] = confidence

                    print('assigned_tag = ', assigned_tag)
                    
                    if(assigned_tag == ann_face_tag):
                        image_dict[PERSON_CHECK_KEY] = 'TP'
                        people_true_positives_dict[assigned_tag] = people_true_positives_dict[assigned_tag] + 1
                        rec_images_nr = rec_images_nr + 1
                        true_pos_confidence_list.append(confidence)
                    else:
                        image_dict[PERSON_CHECK_KEY] = 'FP'
                        if(assigned_tag != 'Undefined'):
                            people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + 1
							false_pos_confidence_list.append(confidence)

                    image_dict_extended = {}
                    image_dict_extended[IMAGE_KEY] = image_dict

                    images_list_for_YAML.append(image_dict_extended)

                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                
            image_counter = image_counter + 1
            
        # Check number of images
        if((image_counter < person_images_nr) or (image_counter > person_images_nr)):
            warning_message = images_dir + ' directory contains ' + str(image_counter) + ' images'
            #print(warning_message)

    # Calculate statistics for each person
    people_precision_list = []
    people_recall_list = []
    people_f1_list = []

    #print(people_true_positives_dict)
    #print(people_false_positives_dict)
    
    for tag in tags:

        person_true_positives = people_true_positives_dict[tag]
        person_false_positives = people_false_positives_dict[tag]

        person_precision = 0
        if(person_true_positives != 0):
            person_precision = float(person_true_positives) / float(person_true_positives + person_false_positives)
        people_precision_list.append(person_precision)
    
        person_recall = 0
        if(test_images_nr != 0):
            person_recall = float(person_true_positives) / test_images_nr
        people_recall_list.append(person_recall)

        person_f1 = 0
        if((person_precision != 0) and (person_recall != 0)):
            person_f1 = 2 * (person_precision * person_recall) / (person_precision + person_recall)
        people_f1_list.append(person_f1)

        # Populate dictionary with results for this person
        person_dict = {}
        person_dict[ANN_TAG_KEY] = tag
        person_dict[TRUE_POSITIVES_NR_KEY] = person_true_positives
        person_dict[FALSE_POSITIVES_NR_KEY] = person_false_positives
        person_dict[PRECISION_KEY] = person_precision
        person_dict[RECALL_KEY] = person_recall
        person_dict[F1_KEY] = person_f1
        people_list_for_YAML.append(person_dict)

    mean_precision = float(numpy.mean(people_precision_list))
    std_precision = float(numpy.std(people_precision_list))

    mean_recall = float(numpy.mean(people_recall_list))
    std_recall = float(numpy.std(people_recall_list))

    mean_f1 = float(numpy.mean(people_f1_list))
    std_f1 = float(numpy.std(people_f1_list))

    recognition_rate = float(rec_images_nr) / float(total_test_images_nr)

    mean_rec_time = mean_rec_time / total_test_images_nr

    mean_true_pos_confidence = float(numpy.mean(true_pos_confidence_list))
    std_true_pos_confidence = float(numpy.std(true_pos_confidence_list))

    mean_false_pos_confidence = float(numpy.mean(false_pos_confidence_list))
    std_false_pos_confidence = float(numpy.std(false_pos_confidence_list))

    print("\n ### RESULTS ###\n")

    print('Recognition rate: ' + str(recognition_rate*100) + '%')
    print('Mean of precision: ' + str(mean_precision*100) + '%')
    print('Standard deviation of precision: ' + str(std_precision*100) + '%')
    print('Mean of recall: ' + str(mean_recall*100) + '%')
    print('Standard deviation of recall: ' + str(std_recall*100) + '%')
    print('Mean of f1: ' + str(mean_f1*100) + '%')
    print('Standard deviation of f1: ' + str(std_f1*100) + '%')
    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')

    print('Recognition rate: ' + str(recognition_rate))
    print('Mean of precision: ' + str(mean_precision))
    print('Standard deviation of precision: ' + str(std_precision))
    print('Mean of recall: ' + str(mean_recall))
    print('Standard deviation of recall: ' + str(std_recall))
    print('Mean of f1: ' + str(mean_f1))
    print('Standard deviation of f1: ' + str(std_f1))
    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')
    
    print('Mean of confidence for true positives: ' + str(mean_true_pos_confidence))
    print('Standard deviation of confidence for true positives: ' + str(std_true_pos_confidence))
    print('Mean of confidence for false positives: ' + str(mean_false_pos_confidence))
    print('Standard deviation of confidence for false positives: ' + str(std_false_pos_confidence))
    

    # Update YAML file with results related to all the experiments
    number_of_already_done_experiments = 0

    new_experiment_dict = {}
    algorithm_name = face_rec_params[ALGORITHM_KEY]
    new_experiment_dict[EXPERIMENT_ALGORITHM_KEY] = algorithm_name

    new_experiment_dict[RECOGNITION_RATE_KEY] = recognition_rate
    new_experiment_dict[MEAN_PRECISION_KEY] = mean_precision
    new_experiment_dict[STD_PRECISION_KEY] = std_precision
    new_experiment_dict[MEAN_RECALL_KEY] = mean_recall
    new_experiment_dict[STD_RECALL_KEY] = std_recall
    new_experiment_dict[MEAN_F1_KEY] = mean_f1
    new_experiment_dict[STD_F1_KEY] = std_f1
    new_experiment_dict[MEAN_RECOGNITION_TIME_KEY] = mean_rec_time

    rec_dict[FACE_RECOGNITION_GLOBAL_RESULTS] = new_experiment_dict
    rec_dict[FACE_RECOGNITION_IMAGES_KEY] = images_list_for_YAML
    rec_dict[FACE_RECOGNITION_PEOPLE_KEY] = people_list_for_YAML

    all_results_YAML_file_path = results_path + FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME + '.yml'
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
    all_results_CSV_file_path = results_path + FACE_RECOGNITION_EXPERIMENT_RESULTS_FILE_NAME + '.csv'
    save_rec_experiments_in_CSV_file(all_results_CSV_file_path, experiments)

    # Save file with results related to this experiment
    results_file_path = results_path + 'FaceRecognitionExperiment' + str(number_of_already_done_experiments + 1) + 'Results.yml'
    save_YAML_file(results_file_path, rec_dict)

if __name__ == "__main__":
    
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description = "Execute face recognition tests")
    parser.add_argument("-config", help = "configuration file")
    args = parser.parse_args()

    params = None

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

    test_passed = fr_test(params, False)

    if(test_passed):
        print("\nSOFTWARE TEST PASSED\n")
        print("\n ### EXECUTING EXPERIMENTS ###\n")
        fr_experiments(params, False)
    else:
        print("\nSOFTWARE TEST FAILED\n")
