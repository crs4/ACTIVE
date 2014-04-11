# This script creates the configuration file for the experiments

import sys
sys.path.append("..")
from tools.Constants import *
from tools.Utils import save_YAML_file

configuration_file_path = TEST_CONFIGURATION_FILE_PATH;

conf_dict  = {};

# Creation of dictionary for face detection experiments
fd_dict = {};
fd_dict[TEST_FILES_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\TestSet'
fd_dict[ANNOTATIONS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\Annotations'
fd_dict[RESULTS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\TestResultsDummy'
fd_dict[SOFTWARE_TEST_FILE_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\SoftwareTestingFiles\Test.jpg'

conf_dict[FACE_DETECTION_KEY] = fd_dict;

# Creation of dictionary for face recognition experiments
fr_dict = {};
fr_dict[DATASET_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\data\Dataset AT&T'
fr_dict[RESULTS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face recognition\TestResults\Dataset AT&T'
fr_dict[SOFTWARE_TEST_FILE_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face recognition\SoftwareTestingFiles\Test.pgm';
fr_dict[PERSON_IMAGES_NR_KEY] = 10;
fr_dict[TRAINING_IMAGES_NR_KEY] = 6;
fr_dict[PEOPLE_NR_KEY] = 40;

conf_dict[FACE_RECOGNITION_KEY] = fr_dict;

# Creation of dictionary for face extraction experiments
fe_dict = {};
fe_dict[TEST_FILES_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face extraction\TestSet'
fe_dict[ANNOTATIONS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face extraction\Annotations'
fe_dict[RESULTS_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face extraction\TestResultsDummy'
fe_dict[SOFTWARE_TEST_FILE_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face extraction\SoftwareTestingFiles\Test.jpg'

conf_dict[FACE_EXTRACTION_KEY] = fe_dict;

save_YAML_file(configuration_file_path, conf_dict);

