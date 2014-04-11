# This script creates the configuration file for face extractor

import sys
sys.path.append("..")
from tools.Constants import *
from tools.Utils import save_YAML_file

configuration_file_path = FACE_EXTRACTOR_CONFIGURATION_FILE;

conf_dict  = {};

# Creation of dictionary for face detection
fd_dict = {};

fd_dict[ALGORITHM_KEY] = 'HaarCascadeFrontalFaceAlt2';
fd_dict[CLASSIFIERS_FOLDER_PATH_KEY] = ACTIVE_ROOT_DIRECTORY + r'\test\Test files\Face detection\ClassifierFiles';
fd_dict[SCALE_FACTOR_KEY] = 1.1;
fd_dict[MIN_NEIGHBORS_KEY] = 5;
fd_dict[FLAGS_KEY] = 'DoCannyPruning';
fd_dict[MIN_SIZE_WIDTH_KEY] = 20;
fd_dict[MIN_SIZE_HEIGHT_KEY] = 20;

conf_dict[FACE_DETECTION_KEY] = fd_dict;

# Creation of dictionary for face recognition
fe_dict = {};
fe_dict[ALGORITHM_KEY] = 'LBP';

conf_dict[FACE_RECOGNITION_KEY] = fe_dict;

print(conf_dict);

save_YAML_file(configuration_file_path, conf_dict);


