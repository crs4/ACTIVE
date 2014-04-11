# This script creates the configuration file for the experiments

from Utils import save_YAML_file
from Constants import *

configuration_file_path = TEST_CONFIGURATION_FILE;

conf_dict  = {};

# Creation of dictionary for face detection experiments
fd_dict = {};
fd_dict[TEST_FILES_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\TestSet'
fd_dict[ANNOTATIONS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\Annotations'
fd_dict[RESULTS_PATH_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\TestResultsDummy'
fd_dict[SOFTWARE_TEST_FILE_KEY] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\SoftwareTestingFiles\Test.jpg'
fd_dict[DB_PATH] = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\SoftwareTestingFiles\Test.jpg'

conf_dict[FACE_DETECTION_KEY] = fd_dict;

save_YAML_file(configuration_file_path, conf_dict);
