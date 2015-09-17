import argparse
import constants_for_experiments as ce
import cv2
import unittest
import os
import person_tracking as pt
import sys
from person_tracking_software_test import TestPersonTracking

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
import tools.utils as utils

def person_tracking_image_experiments(params=None):
    """
    Execute person tracking experiments on images

    :type params: dictionary
    :param params: configuration parameters
                   to be used for the experiment (see table)
    ============================================  ========================================  ==============
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============
    clothes_bounding_box_height                   Height of bounding box for clothes
                                                  (in % of the face bounding box height)    1.0
    clothes_bounding_box_width                    Width of bounding box for clothes         2.0
                                                  (in % of the face bounding box width)
    neck_height                                   Height of neck (in % of the               0.0
                                                  face bounding box height)
    nr_of_hsv_channels_nr_in_person_tracking      Number of HSV channels used               2
                                                  in person tracking (1-2)
    use_mask_in_person_tracking                   If True, use a mask for HSV values        False
    annotations_path                              Path of directory containing the
                                                  manual annotations for the images
    dataset_path                                  Path of dataset
    ============================================  ========================================  ==============
    """

    ann_path = ce.PERSON_TRACKING_IMAGE_ANN_PATH
    dataset_path = ce.PERSON_TRACKING_IMAGE_DATASET_PATH
    if params is not None:
        if ce.PERSON_TRACKING_IMAGE_ANN_PATH_KEY in params:
            ann_path = params[ce.PERSON_TRACKING_IMAGE_ANN_PATH_KEY]
        if ce.PERSON_TRACKING_IMAGE_DATASET_PATH_KEY in params:
            dataset_path = params[ce.PERSON_TRACKING_IMAGE_DATASET_PATH_KEY]

    # Load file with annotations
    ann_dict = utils.load_YAML_file(ann_path)

    tot_discrete_score = 0
    tot_cont_score = 0
    tot_tracking_time = 0

    matches_counter = 0
    for subject_dir in os.listdir(dataset_path):
        subject_path = os.path.join(dataset_path, subject_dir)

        # Every image in directory is used as a reference image
        for ref_im_name in os.listdir(subject_path):
            print('ref_im_name', ref_im_name)
            # Full path of reference image
            ref_im_path = os.path.join(subject_path, ref_im_name)
            # Path of image relative to dataset path
            ref_rel_im_path = os.path.join(subject_dir, ref_im_name)
            ref_bbox = ann_dict[ref_rel_im_path][c.BBOX_KEY]

            # Other images in same directory are used as test images
            for test_im_name in os.listdir(subject_path):
                if test_im_name != ref_im_name:
                    # Full path of test image
                    test_im_path = os.path.join(subject_path, test_im_name)
                    # Path of image relative to dataset path
                    test_rel_im_path = os.path.join(subject_dir, ref_im_name)
                    test_true_bbox = ann_dict[test_rel_im_path][c.BBOX_KEY]
                    true_face_width = test_true_bbox[2]
                    true_face_height = test_true_bbox[3]

                    # TODO ADD PARAMS
                    show_results = False
                    # Saving processing time
                    start_time = cv2.getTickCount()
                    test_found_bbox = pt.find_person_by_clothes(
                        test_im_path, ref_im_path, ref_bbox, None, show_results)
                    clocks = cv2.getTickCount() - start_time
                    seconds = clocks / cv2.getTickFrequency()
                    tot_tracking_time += seconds

                    if test_found_bbox:
                        (sim, int_area, int_area_pct) = utils.is_rect_similar(
                            test_true_bbox, test_found_bbox, 0)
                        if sim:
                            tot_discrete_score += 1
                            tot_cont_score += int_area_pct
                    matches_counter += 1

    discrete_score = float(tot_discrete_score) / matches_counter
    cont_score = tot_cont_score / matches_counter
    mean_tracking_time = tot_tracking_time / matches_counter

    print("\n ### RESULTS ###\n")
    print('Mean of discrete score: ' + str(discrete_score * 100) + '%')
    print('Mean of continuous score: ' + str(cont_score * 100) + '%')
    print('Mean tracking time: ' + str(mean_tracking_time) + ' s\n\n')

# params = {}
# params[ce.PERSON_TRACKING_IMAGE_ANN_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-629I-75P\Annotations.yml'
# params[ce.PERSON_TRACKING_IMAGE_DATASET_PATH_KEY] = r'C:\Users\Maurizio\Documents\Dataset\Evolutive\Videolina-629I-75P'
# person_tracking_image_experiments(params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute person tracking tests")
    parser.add_argument("-config", help="configuration_file")
    parser.add_argument("--no_software_test",
                        help="do not execute software test",
                        action="store_true")
    args = parser.parse_args()
    no_software_test = args.no_software_test

    # Set parameters
    params = None

    if args.config:
        # Load given configuration file
        try:
            params = utils.load_YAML_file(args.config)
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
            print("Default configuration file will be used")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    else:
        print("Default configuration file will be used")

    execute_experiments = False

    if not no_software_test:
        print("\n ### EXECUTING SOFTWARE TEST ###\n")

        suite = unittest.TestLoader().loadTestsFromTestCase(
        TestPersonTracking)
        test_result = unittest.TextTestRunner(verbosity=2).run(suite)

        if test_result.wasSuccessful():
            execute_experiments = True

    else:
        execute_experiments = True

    if execute_experiments:
        print("\n ### EXECUTING EXPERIMENTS ###\n")
        person_tracking_image_experiments(params)