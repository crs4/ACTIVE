import os
import sys
import unittest

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.caption_recognition import get_tag_from_image, get_tags_from_file
import tools.constants as c


class TestCaptionRecognition(unittest.TestCase):

    def test_get_tag_from_image(self):
        
        image_path = ('..' + os.sep + 'test_files' + os.sep +
                      'caption_recognition' + os.sep + 'Test.jpg')

        tags_file_path = ('..' + os.sep + 'test_files' + os.sep +
                          'caption_recognition' + os.sep + 'Tags.txt')

        tags = get_tags_from_file(tags_file_path)
        
        params = {c.USE_LEVENSHTEIN_KEY: True, c.LEV_RATIO_PCT_THRESH_KEY: 0,
                  c.MIN_TAG_LENGTH_KEY: 0, c.USE_BLACKLIST_KEY: False,
                  c.TAGS_FILE_PATH_KEY: tags_file_path}

        result_dict = get_tag_from_image(image_path, params)
        
        assigned_tag = result_dict[c.ASSIGNED_TAG_KEY]
        
        # Threshold and blacklist are not used,
        # so assigned tag must be in tags file
        
        self.assertIn(assigned_tag, tags)
        
        eq_letters_nr = result_dict[c.EQ_LETTERS_NR_KEY]
        
        tot_letters_nr = result_dict[c.TOT_LETTERS_NR_KEY]
        
        self.assertTrue(eq_letters_nr <= tot_letters_nr)
        

    def test_get_tag_from_image_with_threshold(self):
        
        image_path = ('..' + os.sep + 'test_files' + os.sep +
                      'caption_recognition' + os.sep + 'Test.jpg')
        
        tags_file_path = ('..' + os.sep + 'test_files' + os.sep +
                          'caption_recognition' + os.sep + 'Tags.txt')
        
        params = {c.USE_LEVENSHTEIN_KEY: True, c.LEV_RATIO_PCT_THRESH_KEY: 0.99,
                  c.MIN_TAG_LENGTH_KEY: 0, c.USE_BLACKLIST_KEY: False,
                   c.TAGS_FILE_PATH_KEY: tags_file_path}

        result_dict = get_tag_from_image(image_path, params)
        
        assigned_tag = result_dict[c.ASSIGNED_TAG_KEY]
        
        # Assigned tag for this image must be undefined
        
        self.assertEquals(assigned_tag, c.UNDEFINED_TAG)
        
        eq_letters_nr = result_dict[c.EQ_LETTERS_NR_KEY]
        
        tot_letters_nr = result_dict[c.TOT_LETTERS_NR_KEY]
        
        self.assertTrue(eq_letters_nr <= tot_letters_nr)
        
        
if __name__ == '__main__':
    
    unittest.main()
