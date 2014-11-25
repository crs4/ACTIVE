# This script creates the configuration file for the experiments

import sys
sys.path.append('..')
from tools.Constants import *
from tools.Utils import save_YAML_file

configuration_file_path = TEST_CONFIGURATION_FILE_PATH;

conf_dict  = {};

# Creation of dictionary for face detection experiments
fd_dict = {};
fd_dict[TEST_FILES_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\Dataset Videolina 2 - Good faces with detected eyes\Images'
fd_dict[ANNOTATIONS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\Dataset Videolina 2 - Good faces with detected eyes\Annotations'
fd_dict[RESULTS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\TestResultsDummy' #TEST ONLY
fd_dict[SOFTWARE_TEST_FILE_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\SoftwareTestingFiles\Test.jpg'

conf_dict[FACE_DETECTION_KEY] = fd_dict;

# Creation of dictionary for face recognition experiments
fr_dict = {};
fr_dict[DATASET_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\Dataset AT&T'
fr_dict[TRAINING_SET_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\datatest\Dataset AT&T TRAINING'
fr_dict[TEST_SET_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\datatest\Dataset AT&T TEST'
fr_dict[RESULTS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face recognition\TestResults\Dataset AT&T'
fr_dict[SOFTWARE_TEST_FILE_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face recognition\SoftwareTestingFiles\Test.pgm';
fr_dict[PERSON_IMAGES_NR_KEY] = 10;
fr_dict[TRAINING_IMAGES_NR_KEY] = 9;
fr_dict[PEOPLE_NR_KEY] = 40;
fr_dict[DATASET_ALREADY_DIVIDED_KEY] = True;

conf_dict[FACE_RECOGNITION_KEY] = fr_dict;

# Creation of dictionary for face extraction experiments
fe_dict = {};
fe_dict[TEST_FILES_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\Dataset Videolina 2 - Good faces\Images'
fe_dict[ANNOTATIONS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\Dataset Videolina 2 - Good faces\Annotations'
fe_dict[RESULTS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face extraction\TestResults'
fe_dict[SOFTWARE_TEST_FILE_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face extraction\SoftwareTestingFiles\Test.jpg'
fe_dict[PERSON_IMAGES_NR_KEY] = 10;
fe_dict[TRAINING_IMAGES_NR_KEY] = 9;
fe_dict[PEOPLE_NR_KEY] = 5;

conf_dict[FACE_EXTRACTION_KEY] = fe_dict;

save_YAML_file(configuration_file_path, conf_dict);

