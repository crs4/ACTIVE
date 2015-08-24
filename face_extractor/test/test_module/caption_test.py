import argparse
import cv2
import numpy
import os
import sys
import unittest

from caption_software_test import TestCaptionRecognition
import constants_for_experiments as ce

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.caption_recognition import get_tag_from_image
import tools.constants as c
import tools.utils as utils


def caption_experiments(params=None):
    """
    Execute caption recognition experiments

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the experiment (see table)
    ============================================  ========================================  ==============
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============
    test_set_path                                 Path of directory containing test set
    lev_ratio_pct_threshold                       Minimum threshold for considering         0.8
                                                  captions in frame
    min_tag_length                                Minimum length of tags considered         10
                                                  in caption recognition
    tags_file_path                                Path of text file containing
                                                  list of tags
    tesseract_parent_dir_path                     Path of directory containing
                                                  'tesseract' directory
    use_blacklist                                 If True, use blacklist of items           True
                                                  that make the results of the
                                                  caption recognition on a frame
                                                  rejected
    use_levenshtein                               If True, words found in image             True
                                                  by caption recognition and tags
                                                  are compared by using
                                                  the Levenshtein distance
    ============================================  ========================================  ==============
    """
    
    test_set_path = ce.CAPTION_RECOGNITION_TEST_SET_PATH
    
    if params is not None:
        
        if ce.TEST_SET_PATH_KEY in params:
            
            test_set_path = params[ce.TEST_SET_PATH_KEY]
            
    # Iterate over all directories with images
    
    rec_rate_list = []
    
    conf_list = []
    
    time_list = []
    
    for images_dir in os.listdir(test_set_path):
        
        ann_tag = images_dir
        
        images_dir_complete_path = os.path.join(
        test_set_path, images_dir)
        
        true_pos_nr = 0.0
        
        person_test_images_nr = 0.0
        
        for image in os.listdir(images_dir_complete_path):
            
            image_complete_path = os.path.join(
            images_dir_complete_path, image)
            
            start_time = cv2.getTickCount()
        
            result_dict = get_tag_from_image(
            image_complete_path, params)
            
            time_in_clocks = cv2.getTickCount() - start_time
            
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            time_list.append(time_in_seconds)
            
            assigned_tag = result_dict[c.ASSIGNED_TAG_KEY]
            
            conf = result_dict[c.CONFIDENCE_KEY]
            
            if assigned_tag == ann_tag:
                
                true_pos_nr += 1
                
                conf_list.append(conf)

            person_test_images_nr += 1
                
        rec_rate = true_pos_nr / person_test_images_nr
        
        rec_rate_list.append(rec_rate)
        
    mean_rec_rate = float(numpy.mean(rec_rate_list))
    std_rec_rate = float(numpy.std(rec_rate_list))
    mean_conf = float(numpy.mean(conf_list))
    mean_time = float(numpy.mean(time_list))
    
    print("\n ### RESULTS ###\n")
    
    print('Mean of recognition rate: ' + str(mean_rec_rate))
    print('Standard deviation of recognition rate: ' + str(std_rec_rate))
    print('Mean of confidence in true positives: ' + str(mean_conf))
    print('Mean analysis time: ' + str(mean_time) + ' s')
    
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Execute caption recognition tests")
    parser.add_argument("-config", help="configuration file")
    args = parser.parse_args()

    given_params = None

    if args.config:
        # Load given configuration file
        try:
            given_params = utils.load_YAML_file(args.config)
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
            print("Default configuration file will be used")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        
    print("\n ### EXECUTING SOFTWARE TEST ###\n")

    suite = unittest.TestLoader().loadTestsFromTestCase(
    TestCaptionRecognition)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

    if test_result.wasSuccessful():
        
        print("\n ### EXECUTING EXPERIMENTS ###\n")

        caption_experiments(given_params)
