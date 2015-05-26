import argparse
import cv2
import numpy
import os
import sys
import unittest

from caption_software_test import TestCaptionRecognition

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.caption_recognition import get_tag_from_image
import tools.Constants as c

def caption_experiments(params):
    '''
    Execute face recognition experiments

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the experiments
    '''
    
    test_set_path = c.CAPTION_RECOGNITION_TEST_SET_PATH
    
    if(params is not None):
        
        if(c.TEST_SET_PATH_KEY in params):
            
            test_set_path = params[c.TEST_SET_PATH_KEY]
            
    # Iterate over all directories with images

    total_test_images_nr = 0
    
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
            
            gray_im = cv2.imread(
            image_complete_path, cv2.IMREAD_GRAYSCALE)
        
            result_dict = get_tag_from_image(gray_im, params)
            
            time_in_clocks = cv2.getTickCount() - start_time
            
            time_in_seconds = time_in_clocks / cv2.getTickFrequency()
            
            time_list.append(time_in_seconds)
            
            assigned_tag = result_dict[c.ASSIGNED_TAG_KEY]
            
            conf = result_dict[c.CONFIDENCE_KEY]
            
            if(assigned_tag == ann_tag):
                
                true_pos_nr = true_pos_nr + 1
                
                conf_list.append(conf)
                
            person_test_images_nr = person_test_images_nr + 1
                
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
    
    parser = argparse.ArgumentParser(description = "Execute caption recognition tests")
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

    suite = unittest.TestLoader().loadTestsFromTestCase(
    TestCaptionRecognition)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

    if(test_result.wasSuccessful()):
        
        print("\n ### EXECUTING EXPERIMENTS ###\n")
        
        # Define parameters
        
        #test_set_path = r'Videolina-798I-28P'
        test_set_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-798I-28P'
        
        tags_file_path = '..' + os.sep + '..' + os.sep + 'Test files' + os.sep + 'Caption recognition' + os.sep + 'SoftwareTestingFiles' + os.sep + 'Tags.txt'
        
        params = {}
        
        params[c.TEST_SET_PATH_KEY] = test_set_path
        
        params[c.USE_LEVENSHTEIN_KEY] = True
        
        params[c.LEV_RATIO_PCT_THRESH_KEY] = 0
        
        params[c.MIN_TAG_LENGTH_KEY] = 0
        
        params[c.TAGS_FILE_PATH_KEY] = tags_file_path
        
        caption_experiments(params)
