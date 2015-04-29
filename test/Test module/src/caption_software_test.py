import cv2
import os
import sys
import unittest

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.caption_recognition import get_tag_from_image, get_tags_from_file
import tools.Constants as c

class TestCaptionRecognition(unittest.TestCase):

    def test_get_tag_from_image(self):
        
        image_path = r'..\..\Test files\Caption recognition\SoftwareTestingFiles\Test.jpg'
        
        gray_im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        tags_file_path = r'..\..\Test files\Caption recognition\SoftwareTestingFiles\Tags.txt'
        
        tags = get_tags_from_file(tags_file_path)
        
        params = {}
        
        params[c.USE_LEVENSHTEIN_KEY] = True
        
        params[c.LEV_RATIO_PCT_THRESH_KEY] = 0
        
        params[c.MIN_TAG_LENGTH_KEY] = 0
        
        params[c.TAGS_FILE_PATH_KEY] = tags_file_path
       
        result_dict = get_tag_from_image(gray_im, params)
        
        assigned_tag = result_dict[c.ASSIGNED_TAG_KEY]
        
        # No threshold is used, so assigned tag must be in tags file
        
        self.assertIn(assigned_tag, tags)
        
        eq_letters_nr = result_dict[c.EQ_LETTERS_NR_KEY]
        
        tot_letters_nr = result_dict[c.TOT_LETTERS_NR_KEY]
        
        self.assertTrue(eq_letters_nr <= tot_letters_nr)
        

    def test_get_tag_from_image_with_threshold(self):
        
        image_path = r'..\..\Test files\Caption recognition\SoftwareTestingFiles\Test.jpg'
        
        gray_im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        tags_file_path = r'..\..\Test files\Caption recognition\SoftwareTestingFiles\Tags.txt'
        
        tags = get_tags_from_file(tags_file_path)
        
        tags.append(-1)
        
        params = {}
        
        params[c.USE_LEVENSHTEIN_KEY] = True
        
        params[c.LEV_RATIO_PCT_THRESH_KEY] = 0.99
        
        params[c.MIN_TAG_LENGTH_KEY] = 0
        
        params[c.TAGS_FILE_PATH_KEY] = tags_file_path
       
        result_dict = get_tag_from_image(gray_im, params)
        
        assigned_tag = result_dict[c.ASSIGNED_TAG_KEY]
        
        # Assigned tag must be in tags file or equals to -1
        
        self.assertIn(assigned_tag, tags)
        
        eq_letters_nr = result_dict[c.EQ_LETTERS_NR_KEY]
        
        tot_letters_nr = result_dict[c.TOT_LETTERS_NR_KEY]
        
        self.assertTrue(eq_letters_nr <= tot_letters_nr)
        
        
if __name__ == '__main__':
    
    unittest.main()
