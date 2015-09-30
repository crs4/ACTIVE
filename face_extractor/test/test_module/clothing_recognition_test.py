import argparse
import os
import pickle
import sys
import constants_for_experiments as ce
import tools.utils as utils
import tools.constants as c
import tools.person_tracking as pt

from utils_for_experiments import load_experiment_results

def clothing_recognition_experiments(dataset_path, params=None):
    """
    Execute clothing recognition experiments

    :type dataset_path: string
    :param dataset_path: path of directory with first frame sequence

    :type params: dictionary
    :param params: configuration parameters (see table)

    ============================================  ========================================  =============================
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  =============================
    clothes_bounding_box_height                   Height of bounding box for clothes
                                                  (in % of the face bounding box height)    1.0
    clothes_bounding_box_width                    Width of bounding box for clothes         2.0
                                                  (in % of the face bounding box width)
    clothing_recognition_K                        Multiplier for intra distances            1
                                                  for calculating local threshold
                                                  in clothing recognition
    neck_height                                   Height of neck (in % of the               0.0
                                                  face bounding box height)
    nr_of_HSV_channels_in_clothing_recognition    Number of HSV channels used
                                                  in clothing recognition (1-3)             3
    use_mask_in_clothing_recognition              If True, use mask for HSV values          True
                                                  in clothing recognition
    use_motion_mask_in_clothing_recognition       If True, calculate histograms only        False
                                                  on regions where motion is detected
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    face_detection_algorithm                      Classifier for face detection             'HaarCascadeFrontalFaceAlt2'
                                                  ('HaarCascadeFrontalFaceAlt',
                                                  'HaarCascadeFrontalFaceAltTree',
                                                  'HaarCascadeFrontalFaceAlt2',
                                                  'HaarCascadeFrontalFaceDefault',
                                                  'HaarCascadeProfileFace',
                                                  'HaarCascadeFrontalAndProfileFaces',
                                                  'HaarCascadeFrontalAndProfileFaces2',
                                                  'LBPCascadeFrontalface',
                                                  'LBPCascadeProfileFace' or
                                                  'LBPCascadeFrontalAndProfileFaces')
    flags                                         Flags used in face detection              'DoCannyPruning'
                                                  ('DoCannyPruning', 'ScaleImage',
                                                  'FindBiggestObject', 'DoRoughSearch').
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    clothing_recognition_results_path             Directory that will contain results
                                                  of clothing recognition experiments
    video_name                                    Name of video to be tested
    ============================================  ========================================  =============================
    """

    # Set parameters
    cloth_models_dir_path = None
    clothing_rec_k = c.CLOTHING_REC_K
    hsv_channels = c.CLOTHING_REC_HSV_CHANNELS_NR
    results_path = ce.CLOTHING_RECOGNITION_RESULTS_PATH
    use_LBP = c.CLOTHING_REC_USE_LBP
    use_mask = c.CLOTHING_REC_USE_MASK
    use_motion_mask = c.CLOTHING_REC_USE_MOTION_MASK
    video_name = ce.TEST_VIDEO_NAME
    if params is not None:
        if ce.CLOTH_MODELS_DIR_PATH_KEY in params:
            cloth_models_dir_path = params[ce.CLOTH_MODELS_DIR_PATH_KEY]
        if c.CLOTHING_REC_K_KEY in params:
            clothing_rec_k = params[c.CLOTHING_REC_K_KEY]
        if c.CLOTHING_REC_HSV_CHANNELS_NR_KEY in params:
            hsv_channels = params[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY]
        if ce.CLOTHING_RECOGNITION_RESULTS_PATH_KEY in params:
            results_path = params[ce.CLOTHING_RECOGNITION_RESULTS_PATH_KEY]
        if c.CLOTHING_REC_USE_LBP_KEY in params:
            use_LBP = params[c.CLOTHING_REC_USE_LBP_KEY]
        if c.CLOTHING_REC_USE_MASK_KEY in params:
            use_mask = params[c.CLOTHING_REC_USE_MASK_KEY]
        if c.CLOTHING_REC_USE_MOTION_MASK_KEY in params:
            use_motion_mask = params[c.CLOTHING_REC_USE_MOTION_MASK_KEY]
        if ce.VIDEO_NAME_KEY in params:
            video_name = params[ce.VIDEO_NAME_KEY]

    # Number of correctly matched pairs of frame sequences
    rec_pairs_nr = 0

    # Number of checked pairs of frame sequences
    total_test_pairs_nr = 0

    # Iterate through videos
    for video in os.listdir(dataset_path):
        video_path = os.path.join(dataset_path, video)
        if video != video_name:
            continue

        # If directory for clothing models is provided and
        # file for this video exists, load models from file
        file_path = None
        loaded = False
        models = None
        if cloth_models_dir_path:
            file_path = os.path.join(cloth_models_dir_path, video_name)
            if os.path.exists(file_path):
                with open(file_path) as f:
                    models = pickle.load(f)
                    loaded = True

        if not loaded:

            # Calculate clothing models
            models = []
            for subj in os.listdir(video_path):
                subj_path = os.path.join(video_path, subj)
                frame_seq = []
                for im in os.listdir(subj_path):
                    im_path = os.path.join(subj_path, im)
                    frame_seq.append(im_path)
                model = pt.get_clothing_model_from_sequence(frame_seq, params)
                models.append(model)

            # If directory for clothing models is provided,
            # save models into a file
            if cloth_models_dir_path:
                with open(file_path, 'w') as f:
                    pickle.dump(models, f)

        # Compare each possible pair of frame sequences in the same video
        counter_1 = 0
        for subj_1 in os.listdir(video_path):

            counter_2 = 0
            for subj_2 in os.listdir(video_path):
                if subj_2 != subj_1:

                    model_1 = models[counter_1]
                    model_2 = models[counter_2]

                    if model_1 and model_2:
                        total_test_pairs_nr += 1

                        # If LBP histograms are used, there is only one channel
                        if use_LBP:
                            if params is None:
                                params = {}
                            params[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY] = 1

                        (sim, dist_ratio) = utils.compare_clothes(
                            model_1, model_2, '', '', 0, None, params,
                            clothing_rec_k)

                        # First part of directory name contains person's tag
                        tag1 = subj_1.split('-')[0]
                        tag2 = subj_2.split('-')[0]

                        # Check correctness of result
                        if ((sim and (tag1 == tag2))
                                or (not sim and (tag1 != tag2))):
                            rec_pairs_nr += 1
                counter_2 += 1
            counter_1 += 1

    recognition_rate = 0
    if total_test_pairs_nr != 0:
        recognition_rate = float(rec_pairs_nr) / float(total_test_pairs_nr)

    print("\n ### RESULTS ###\n")

    print('Number of checked pairs of image sequences: ' + str(total_test_pairs_nr))
    print('Number of correctly matched pairs of image sequences: ' + str(rec_pairs_nr))
    print('Recognition rate: ' + str(recognition_rate * 100) + '%')

    # Update YAML file with the results of all the experiments

    new_experiment_dict = {ce.VIDEO_NAME_KEY: video_name,
                           c.CLOTHING_REC_HSV_CHANNELS_NR_KEY: hsv_channels,
                           c.CLOTHING_REC_K_KEY: clothing_rec_k,
                           c.CLOTHING_REC_USE_LBP_KEY: use_LBP,
                           c.CLOTHING_REC_USE_MASK_KEY: use_mask,
                           c.CLOTHING_REC_USE_MOTION_MASK_KEY: use_motion_mask,
                           ce.TEST_IMAGES_NR_KEY: total_test_pairs_nr,
                           ce.RECOGNITION_RATE_KEY: recognition_rate}

    experiment_results_file_name = ce.EXPERIMENT_RESULTS_FILE_NAME

    yaml_results_file_name = experiment_results_file_name + '.yaml'

    all_results_YAML_file_path = os.path.join(
        results_path, yaml_results_file_name)
    file_check = os.path.isfile(all_results_YAML_file_path)

    experiments = list()
    if file_check:
        experiments = load_experiment_results(all_results_YAML_file_path)
        number_of_already_done_experiments = len(experiments)
        new_experiment_dict[ce.EXPERIMENT_NUMBER_KEY] = (
            number_of_already_done_experiments + 1)
    else:
        new_experiment_dict[ce.EXPERIMENT_NUMBER_KEY] = 1

    new_experiment_dict_extended = {ce.EXPERIMENT_KEY: new_experiment_dict}
    experiments.append(new_experiment_dict_extended)
    experiments_dict = {ce.EXPERIMENTS_KEY: experiments}
    utils.save_YAML_file(all_results_YAML_file_path, experiments_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute clothing recognition tests")
    parser.add_argument(
        "-dataset_path", help="path of dataset")
    parser.add_argument("-config", help="configuration_file")
    args = parser.parse_args()

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

    # Set paths
    dataset_path = None
    if args.dataset_path:
        dataset_path = args.dataset_path
    else:
        print("Path of dataset not provided")
        exit()

    clothing_recognition_experiments(dataset_path, params)
