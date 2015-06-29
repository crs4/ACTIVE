import cv2
import os
import unittest
import sys

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.face_models import FaceModels


class TestFaceModels(unittest.TestCase):

    def test_init(self):
        
        data_dir_path = 'Data dir path'
        
        params = {c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY: data_dir_path}

        fm = FaceModels(params)
        
        self.assertEquals(fm._data_dir_path, data_dir_path)

    def test_add_blacklist_item(self):

        item = 'Al_telefono'

        fm = FaceModels()

        fm.add_blacklist_item(item)

        blacklist = fm.get_blacklist()

        self.assertIn(item, blacklist)

    def test_add_face(self):
        
        base_path = os.path.join('..', 'test_files', 'face_models')
        
        fm = FaceModels()

        fm.delete_models()

        label = 3812
        tag = 'Mameli_Giacomo'

        image_path = os.path.join(base_path, '0000000.png')
        
        aligned_image_path = os.path.join(base_path, '0000000_aligned.png')
        
        aligned_face = cv2.imread(aligned_image_path, cv2.IMREAD_GRAYSCALE)
        
        eye_pos = (303, 131, 352, 134)
        
        bbox = (260, 76, 137, 137)
        
        fm.add_face(label, tag, image_path, aligned_face, eye_pos, bbox)

        label = 3813
        tag = 'Fadda_Paolo'

        image_path = os.path.join(base_path, '0000001.png')
        
        aligned_image_path = os.path.join(base_path, '0000001_aligned.png')
        
        aligned_face = cv2.imread(aligned_image_path, cv2.IMREAD_GRAYSCALE)
        
        eye_pos = (323, 150, 376, 145)
        
        bbox = (267, 87, 166, 166)
        
        fm.add_face(label, tag, image_path, aligned_face, eye_pos, bbox)

        label = 3815
        tag = 'Giannotta_Michele'
        
        image_path = os.path.join(base_path, '0000002.png')
        
        aligned_image_path = os.path.join(base_path, '0000002_aligned.png')
        
        aligned_face = cv2.imread(aligned_image_path, cv2.IMREAD_GRAYSCALE)
        
        eye_pos = (337, 190, 393, 183)
        
        bbox = (282, 121, 161, 161)
        
        fm.add_face(label, tag, image_path, aligned_face, eye_pos, bbox)
        
        label = 3814
        tag = 'Leoni_Mario'
        
        image_path = os.path.join(base_path, '0000003.png')
        
        aligned_image_path = os.path.join(base_path, '0000003_aligned.png')
        
        aligned_face = cv2.imread(aligned_image_path, cv2.IMREAD_GRAYSCALE)
        
        eye_pos = (355, 148, 407, 152)
        
        bbox = (300, 89, 156, 156)
        
        fm.add_face(label, tag, image_path, aligned_face, eye_pos, bbox)

        label = 3814
        tag = 'Leoni_Mario'

        image_path = os.path.join(base_path, '0000004.png')
        
        aligned_image_path = os.path.join(base_path, '0000004_aligned.png')
        
        aligned_face = cv2.imread(aligned_image_path, cv2.IMREAD_GRAYSCALE)
        
        eye_pos = (138, 150, 158, 151)
        
        bbox = (119, 128, 60, 60)
        
        fm.add_face(label, tag, image_path, aligned_face, eye_pos, bbox)
        
        label = 3812
        tag = 'Mameli_Giacomo'
        
        image_path = os.path.join(base_path, '0000005.png')
        
        aligned_image_path = os.path.join(base_path, '0000005_aligned.png')
        
        aligned_face = cv2.imread(aligned_image_path, cv2.IMREAD_GRAYSCALE)
        
        eye_pos = (318, 128, 361, 126)
        
        bbox = (272, 86, 126, 126)
        
        fm.add_face(label, tag, image_path, aligned_face, eye_pos, bbox)

    def test_create_models_from_aligned_faces(self):

        self.test_create_models_from_whole_images()

        fm = FaceModels()

        labels = [2000, 2001, 2002, 2003]

        fm.create_models_from_aligned_faces(labels)

        # Check that directory with aligned faces exists
        # and that sub directories have the right name

        aligned_faces_path = os.path.join(
            fm._data_dir_path, c.TRAINING_SET_DIR, c.ALIGNED_FACES_DIR)

        sub_dir_counter = 0
        if os.path.exists(aligned_faces_path):
            for sub_dir in os.listdir(aligned_faces_path):
                self.assertEqual(sub_dir, str(labels[sub_dir_counter]))
                sub_dir_counter += 1

    def test_create_models_from_whole_images(self):

        orig_images_dir_path = os.path.join(
            '..', 'test_files', 'face_models', 'Whole images')

        fm = FaceModels()

        fm.delete_models()

        fm.create_models_from_whole_images(orig_images_dir_path)

        # Check that all files exist

        db_file_name = os.path.join(fm._data_dir_path, c.FACE_MODELS_FILE)
        self.assertTrue(os.path.exists(db_file_name))

        tag_label_associations_file = os.path.join(
            fm._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        self.assertTrue(os.path.exists(tag_label_associations_file))

        faces_file = os.path.join(fm._data_dir_path, c.FACES_FILE)
        self.assertTrue(os.path.exists(faces_file))

        # Check that directory with aligned faces exists
        # and has the right number of sub directories

        aligned_faces_path = os.path.join(
            fm._data_dir_path, c.TRAINING_SET_DIR, c.ALIGNED_FACES_DIR)

        sub_dir_counter = 0
        if os.path.exists(aligned_faces_path):
            for sub_dir in os.listdir(aligned_faces_path):
                sub_dir_counter += 1
        self.assertEqual(sub_dir_counter, 4)

    def test_create_models_from_whole_images_and_labels(self):

        orig_images_dir_path = os.path.join(
            '..', 'test_files', 'face_models', 'Whole images')

        fm = FaceModels()

        fm.delete_models()

        labels = [1000, 1001, 1002, 1003]

        fm.create_models_from_whole_images(orig_images_dir_path, labels)

        # Check that all files exist

        db_file_name = os.path.join(fm._data_dir_path, c.FACE_MODELS_FILE)
        self.assertTrue(os.path.exists(db_file_name))

        tag_label_associations_file = os.path.join(
            fm._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        self.assertTrue(os.path.exists(tag_label_associations_file))

        faces_file = os.path.join(fm._data_dir_path, c.FACES_FILE)
        self.assertTrue(os.path.exists(faces_file))

        aligned_faces_path = os.path.join(
            fm._data_dir_path, c.TRAINING_SET_DIR, c.ALIGNED_FACES_DIR)

        # Check that directory with aligned faces exists
        # and has the right number of sub directories
        # and that each sub directory has the right name

        sub_dir_counter = 0
        if os.path.exists(aligned_faces_path):
            for sub_dir in os.listdir(aligned_faces_path):
                self.assertEqual(sub_dir, str(labels[sub_dir_counter]))
                sub_dir_counter += 1

        self.assertEqual(sub_dir_counter, 4)


    def test_get_tag(self):

        self.test_add_face()

        fm = FaceModels()

        fm.load_models()

        tag = fm.get_tag(3812)

        self.assertEqual(tag, 'Mameli_Giacomo')

    def test_get_tags(self):

        fm = FaceModels()

        fm.delete_models()

        self.test_add_face()
        
        fm.load_models()
        
        tags = fm.get_tags()
        
        self.assertEquals(len(tags), 4)

    def test_prediction(self):

        base_path = '..' + os.sep + 'test_files' + os.sep + 'face_models'

        fm = FaceModels()

        self.test_add_face()

        fm.load_models()

        im_path = os.path.join(base_path, '0000000_aligned.png')

        face = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

        (label, conf) = fm.recognize_face(face)

        print 'Predicted label = %s (confidence=%.2f)' % (label, conf)

        self.assertEquals(label, 3812)

        im_path = os.path.join(base_path, '0000002_aligned.png')

        face = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

        (tag, conf) = fm.recognize_face(face)

        print 'Predicted tag = %s (confidence=%.2f)' % (tag, conf)

        self.assertEquals(tag, 3815)

    def test_remove_face_not_removed(self):
        
        fm = FaceModels()

        fm.delete_models()

        self.test_add_face()
        
        label = 1812
        
        im_name = 'Dummy image'
        
        ok = fm.remove_face(label, im_name)
        
        self.assertFalse(ok)
        

    def test_remove_face_label_removed(self):
        
        fm = FaceModels()

        fm.delete_models()

        self.test_add_face()
        
        training_set_path = os.path.join(
        fm._data_dir_path, c.TRAINING_SET_DIR)   
        
        aligned_faces_path = os.path.join(
        training_set_path, c.ALIGNED_FACES_DIR)
        
        label = 3813
        
        subject_path = os.path.join(aligned_faces_path, str(label))
        
        im_name = ''
        
        for im in os.listdir(subject_path):
            
            im_name = im
        
        ok = fm.remove_face(label, im_name)
        
        labels = fm.get_labels()

        self.assertTrue(ok)
        
        self.assertNotIn(label, labels)
        
        
    def test_remove_face(self):
        
        fm = FaceModels()

        fm.delete_models()

        self.test_add_face()
        
        training_set_path = os.path.join(
        fm._data_dir_path, c.TRAINING_SET_DIR)   
        
        aligned_faces_path = os.path.join(
        training_set_path, c.ALIGNED_FACES_DIR)
        
        label = 3812
        
        subject_path = os.path.join(aligned_faces_path, str(label))
        
        im_name = ''
        
        for im in os.listdir(subject_path):
            
            im_name = im
        
        ok = fm.remove_face(label, im_name)
        
        self.assertTrue(ok)    
        
    
    def test_remove_label_not_removed(self):
        
        fm = FaceModels()

        fm.delete_models()

        self.test_add_face()
        
        label = -1
        
        ok = fm.remove_label(label)
        
        self.assertFalse(ok)
        
    
    def test_remove_label(self):
        
        fm = FaceModels()

        fm.delete_models()

        self.test_add_face()
        
        label = 3815
        
        fm.remove_label(label)
        
        labels = fm.get_labels()
        
        self.assertNotIn(label, labels)
        

if __name__ == '__main__':
    
    unittest.main()
