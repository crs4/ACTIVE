import numpy
import os
import sys

import constants_for_experiments as ce
from face_extractor_for_experiments import FaceExtractor
from face_models_for_experiments import FaceModels

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.utils import load_YAML_file, save_YAML_file


def save_experiment_results_in_CSV_file(
        file_path, experiment_dict_list, sim_tracking):
    """
    Save experiments in CSV file

    :type file_path: string
    :param file_path: path of CSV file

    :type experiment_dict_list: list
    :param experiment_dict_list: list with experiments

    :type sim_tracking: boolean
    :param sim_tracking: True is tracking simulation is used, False otherwise
    """
    stream = open(file_path, 'w')

    # Write csv header
    stream.write('Video number,' + 
                 'Timestamp,' +
                 'Annotated tag,' + 
                 'Predicted tag,' +
                 'Confidence' + '\n')
                     
    for experiment_dict in experiment_dict_list:
        
        video_counter = experiment_dict[ce.VIDEO_COUNTER_KEY]
        
        ann_face_tag = experiment_dict[c.ANN_TAG_KEY]
        
        if sim_tracking:
            
            assigned_tag = experiment_dict[c.ASSIGNED_TAG_KEY]
            
            confidence = experiment_dict[c.CONFIDENCE_KEY]
            
            if confidence != -1:
            
                stream.write(str(video_counter) + ',' +
                             str(ann_face_tag) + ',' + 
                             str(assigned_tag) + ',' +
                             str(confidence) + '\n')
            else:
                
                stream.write(str(video_counter) + ',' +
                             str(ann_face_tag) + ',' + 
                             str(assigned_tag) + ',,\n')            
            
        else:
        
            frames = experiment_dict[c.FRAMES_KEY]
            
            for frame in frames:
                
                time_stamp = frame[c.ELAPSED_VIDEO_TIME_KEY]
                
                assigned_tag = frame[c.ASSIGNED_TAG_KEY]
                
                confidence = frame[c.CONFIDENCE_KEY]
    
                if confidence != -1:
                
                    stream.write(str(video_counter) + ',' +
                                 str(time_stamp) + ',' + 
                                 str(ann_face_tag) + ',' + 
                                 str(assigned_tag) + ',' +
                                 str(confidence) + '\n')
                else:
                    
                    stream.write(str(video_counter) + ',' +
                                 str(time_stamp) + ',' + 
                                 str(ann_face_tag) + ',' + 
                                 str(assigned_tag) + ',,\n')
                     
    stream.close()


def aggregate_frame_results_in_sim_tracking(frames, fm):
    """
    Aggregate frame results when simulating tracking

    :type frames: list
    :param frames: list of frames

    :type fm: FaceModels
    :param fm: face models

    :rtype: tuple
    :return: a (final_tag, final_confidence) tuple,
             where final_tag is the assigned tag
             and final_confidence the assigned confidence
    """

    assigned_frames_nr_dict = {}
    confidence_lists_dict = {}
    people_nr = fm.get_people_nr()
    
    tags = fm.get_tags()
    
    for tag in tags:

        assigned_frames_nr_dict[tag] = 0
        confidence_lists_dict[tag] = []

    for frame in frames:

        faces = frame[c.FACES_KEY]

        if len(faces) != 0:

            face = faces[0]

            assigned_tag = face[c.ASSIGNED_TAG_KEY]

            assigned_frames_nr_dict[assigned_tag] += 1

            confidence = face[c.CONFIDENCE_KEY]

            confidence_lists_dict[assigned_tag].append(confidence)

    # Take final decision on person

    final_tag = 'Undefined'
    final_confidence = -1
    if c.USE_MAJORITY_RULE:
        max_frames_nr = 0
        candidate_tags_list = []
        
        people_found = False
        
        for tag in tags:
            
            assigned_frames_nr = assigned_frames_nr_dict[tag]
            
            if assigned_frames_nr > 0:
                people_found = True

            if assigned_frames_nr > max_frames_nr:

                # There is one tag that has more occurrences that the others
                candidate_tags_list = [tag]
                max_frames_nr = assigned_frames_nr

            elif assigned_frames_nr == max_frames_nr:

                # There are two or more tags
                # that have the same number of occurrences
                candidate_tags_list.append(tag)

        if people_found:
        
            if len(candidate_tags_list) >= 1:
    
                final_tag = candidate_tags_list[0]
    
                if c.USE_MIN_CONFIDENCE_RULE:
                    
                    if len(confidence_lists_dict[final_tag]) > 0:
    
                        final_confidence = float(
                            numpy.min(confidence_lists_dict[final_tag]))
    
                    for i in range(1, len(candidate_tags_list)):
                        
                        if len(confidence_lists_dict[candidate_tags_list[i]]) > 0:
    
                            min_confidence = float(numpy.min(
                                confidence_lists_dict[candidate_tags_list[i]]))
    
                        if min_confidence < final_confidence:
    
                            final_tag = candidate_tags_list[i]
    
                            final_confidence = min_confidence
    
                elif c.USE_MEAN_CONFIDENCE_RULE:
    
                    if len(confidence_lists_dict[final_tag]) > 0:
                        final_confidence = float(numpy.mean(
                            confidence_lists_dict[final_tag]))
    
                    for i in range(1, len(candidate_tags_list)):
                        
                        if len(confidence_lists_dict[candidate_tags_list[i]]) > 0:
    
                            mean_confidence = float(numpy.mean(
                                confidence_lists_dict[candidate_tags_list[i]]))
    
                        if mean_confidence < final_confidence:
    
                            final_tag = candidate_tags_list[i]
    
                            final_confidence = mean_confidence
    
    else:
        if c.USE_MIN_CONFIDENCE_RULE:

            if people_nr > 0:

                final_tag = tags[0]

                if len(confidence_lists_dict[final_tag]) > 0:

                    final_confidence = float(numpy.min(
                        confidence_lists_dict[final_tag]))

                for tag in tags:

                    if len(confidence_lists_dict[tag]) > 0:

                        min_confidence = float(
                            numpy.min(confidence_lists_dict[tag]))

                        if ((final_confidence == -1) or
                                (min_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = min_confidence

        elif c.USE_MEAN_CONFIDENCE_RULE:

            if people_nr > 0:

                final_tag = tags[0]

                if len(confidence_lists_dict[final_tag]) > 0:

                    final_confidence = float(numpy.mean(
                        confidence_lists_dict[final_tag]))

                for tag in tags:

                    if len(confidence_lists_dict[tag]) > 0:

                        mean_confidence = float(numpy.mean(
                            confidence_lists_dict[tag]))

                        if ((final_confidence == -1) or
                                (mean_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = mean_confidence
            
        else:
            print('Warning! Method is not available')
                        
    return final_tag, final_confidence


def fr_video_experiments(params, show_results):
    """
    Execute face recognition experiments on video files

    :type params: dictionary
    :param params: configuration parameters to be used for the experiment

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with detected faces

    ============================================  ========================================  ==============
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============
    annotations_path                              Path of directory containing the
                                                  manual annotations for the images
    check_eye_positions                           If True, check eye positions              True
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    eye_detection_classifier                      Classifier for eye detection              'haarcascade_mcs_lefteye.xml'
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
                                                  'FindBiggestObject', 'DoRoughSearch')
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
                                                  the first candidate object is found.
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    face_detection_results_path                   Path of directory where
                                                  test results will be saved
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    max_eye_angle                                 Maximum inclination of the line           0.125
                                                  connecting the eyes
                                                  (in % of pi radians)
    min_eye_distance                              Minimum distance between eyes             0.25
                                                  (in % of the width of the face
                                                  bounding box)
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    software_test_file                            Path of image to be used for
                                                  software test
    test_set_path                                 path of directory
                                                  containing test set
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    aligned_faces_path                            Default path of directory
                                                  for aligned faces
    cropped_face_height                           Height of aligned faces (in pixels)       400
    cropped_face_width                            Width of aligned faces (in pixels)        200
    dataset_already_divided                       If True, dataset is already divided       False
                                                  between training and test set
    dataset_path                                  Path of whole dataset, used if dataset
                                                  is not already divided between
                                                  training and test set
    db_name                                       Name of single file
                                                  containing face models
    db_models_path                                Path of directory containing face models
    face_model_algorithm                          Algorithm for face recognition            'LBP'
                                                  ('Eigenfaces', 'Fisherfaces' or 'LBP')
    face_recognition_results_path                 Path of directory where
                                                  test results will be saved
    test_set_path                                 Path of directory containing
                                                  test set
    training_set_path                             Path of directory containing
                                                  training set
    LBP_grid_x                                    Number of columns in grid                 4
                                                  used for calculating LBP
    LBP_grid_y                                    Number of columns in grid                 8
                                                  used for calculating LBP
    LBP_neighbors                                 Number of neighbors                       8
                                                  used for calculating LBP
    LBP_radius                                    Radius used                               1
                                                  for calculating LBP (in pixels)
    max_frames_with_missed_detection              Maximum number of frames with             5
                                                  missed detection that
                                                  does not interrupt tracking
    offset_pct_x                                  % of the image to keep next to            0.20
                                                  the eyes in the horizontal direction
    offset_pct_y                                  % of the image to keep next to            0.50
                                                  the eyes in the vertical direction
    sim_tracking                                  If True, results from all frames in       False
                                                  video are aggregated
    sliding_window_size                           Size of sliding window in seconds         5.0
    software_test_file                            Path of image to be used for
                                                  software test
    test_video_path                               Path of test video
    training_images_nr                            Number of images per person used in
                                                  training set
    use_captions                                  If True, training set                     False
                                                  for face recognition is built
                                                  on the base of captions
    use_eye_detection                             If True, use eye detection for detecting  True
                                                  eye position for aligning faces in
                                                  test images
    use_eye_detection_in_training                 If True, use eye detection for detecting  True
                                                  eye position for aligning faces in
                                                  training images
    use_eyes_position                             If True, align faces in test images       True
                                                  by using eye positions
    use_eyes_position_in_training                 If True, align faces in training images   True
                                                  by using eye positions
    use_face_detection_in_training                If True, use face detection               False
                                                  for images in training set
    use_majority_rule                             If True, in aggregating results           True
                                                  from several frames,
                                                  final tag is the tag that was
                                                  assigned to the majority of frames
    use_mean_confidence_rule                      If True, in aggregating results           False
                                                  from several frames,
                                                  final tag is the tag that received
                                                  the minimum value for the mean of
                                                  confidences among frames
    use_min_confidence_rule                       If True, in aggregating results           True
                                                  from several frames,
                                                  final tag is the tag that received
                                                  the minimum confidence value
    use_NBNN                                      If True,                                  False
                                                  use Naive Bayes Nearest Neighbor
    use_one_file_for_face_models                  If True, use one file for face models     True
    use_original_fps                              If True, original frame rate is used      False
    use_original_fps_in_training                  If True, use original frame rate          False
                                                  of video when creating training set
    use_resizing                                  If True, resize images                    True
    use_sliding_window                            If True, use sliding window               False
                                                  in face extraction
    use_tracking                                  If True,                                  False
                                                  use tracking in face extraction
    use_weighted_regions                          If True, use weighted LBP                 False
    used_fps                                      Frame rate at which video                 5.0
                                                  is analyzed (in frames per second)
    used_fps_in_training                          Frame rate at which video is analyzed     1.0
                                                  in training from captions
                                                  (in frames per second)
    ============================================  ========================================  ==============
    """

    # Folder with results
    results_path = ce.FACE_RECOGNITION_RESULTS_PATH
    sim_tracking = ce.SIM_TRACKING
    # Folder with test files
    test_set_path = ce.FACE_RECOGNITION_TEST_SET_PATH
    use_captions = ce.USE_CAPTIONS
    use_tracking = ce.USE_TRACKING
    video_path = ce.TEST_VIDEO_PATH
    if params is not None:
        if ce.RESULTS_PATH_KEY in params:
            results_path = params[ce.RESULTS_PATH_KEY]
        if ce.SIM_TRACKING_KEY in params:
            sim_tracking = params[ce.SIM_TRACKING_KEY]
        if ce.TEST_SET_PATH_KEY in params:
            test_set_path = params[ce.TEST_SET_PATH_KEY]
        if ce.USE_CAPTIONS_KEY in params:
            use_captions = params[ce.USE_CAPTIONS_KEY]
        if use_captions:
            if ce.TEST_VIDEO_PATH_KEY in params:
                video_path = params[ce.TEST_VIDEO_PATH_KEY]
        else:
            video_path = None
        if ce.USE_TRACKING_KEY in params:
            use_tracking = params[ce.USE_TRACKING_KEY]


    tot_rec_frames_nr = 0  # Number of correctly recognized frames
    tot_test_frames_nr = 0  # Number of total test frames
    mean_rec_time = 0  # Mean recognition time for videos

    # List of confidence values for true positives
    true_pos_confidence_list = []
    # List of confidence values for false positives
    false_pos_confidence_list = []
    # List of tags of people that appear in test set
    tested_people_tag_list = []

    fm = FaceModels(params=params, video_path=video_path)
    # Number of people
    people_nr = fm.get_people_nr()

    # Initialize dictionaries with people
    people_true_positives_dict = {}
    people_false_positives_dict = {}
    people_test_frames_nr_dict = {}

    tags = fm.get_tags()
    
    for tag in tags:
        
        people_true_positives_dict[tag] = 0
        people_false_positives_dict[tag] = 0
        people_test_frames_nr_dict[tag] = 0

    # Iterate over all videos
    
    experiment_dict_list = []
    
    number_of_anal_video = 0
    
    for video in os.listdir(test_set_path):
        
        # Dictionary for YAML file with results
        experiment_dict = {}
        experiment_dict_frames = []
        
        assigned_tag = 'Undefined'
        final_confidence = -1

        video_delta_xs = []
        video_delta_ys = []
        video_delta_ws = []

        ann_face_tag, file_ext = os.path.splitext(video)

        print('Annotated face tag: ', ann_face_tag)

        tested_people_tag_list.append(ann_face_tag)

        video_complete_path = test_set_path + video

        print(video_complete_path)

        try:

            fe = FaceExtractor(fm)

            handle = fe.extract_faces_from_video(video_complete_path)

            results = fe.get_results(handle)

            error = results[c.ERROR_KEY]

            if error:

                print('Warning')
                print(error)

            else:

                video_test_frames_nr = results[ce.TOT_FRAMES_NR_KEY]

                tot_test_frames_nr = tot_test_frames_nr + video_test_frames_nr

                people_test_frames_nr_dict[ann_face_tag] = video_test_frames_nr
                
                mean_rec_time = mean_rec_time + results[c.ELAPSED_CPU_TIME_KEY]

                if use_tracking:

                    segments = results[c.SEGMENTS_KEY]

                    tot_segments_frames_nr = 0

                    true_positives_in_segment = 0

                    for segment in segments:

                        segment_frames = segment[c.FRAMES_KEY]

                        frames_nr = segment[c.SEGMENT_TOT_FRAMES_NR_KEY]

                        assigned_tag = segment[c.ASSIGNED_TAG_KEY]

                        print('assigned_tag = ' + assigned_tag)

                        final_confidence = segment[c.CONFIDENCE_KEY]

                        tot_segments_frames_nr = tot_segments_frames_nr + frames_nr

                        if assigned_tag == ann_face_tag:

                            people_true_positives_dict[assigned_tag] += frames_nr
                            true_positives_in_segment = true_positives_in_segment + frames_nr
                            tot_rec_frames_nr = tot_rec_frames_nr + frames_nr
                            true_pos_confidence_list.append(final_confidence)

                        else:

                            if assigned_tag != 'Undefined':

                                people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + frames_nr
                                false_pos_confidence_list.append(final_confidence)


                    # Tot number of frames in segments
                    # cannot be more than number of frames in video
                    if true_positives_in_segment > video_test_frames_nr:
                        print('### WARNING! ###')
                        print 'true_positives_in_segment = ' + str(
                            true_positives_in_segment)
                        print 'video_test_frames_nr = ' + str(
                            video_test_frames_nr)
                        people_false_positives_dict[
                            ann_face_tag] += (tot_segments_frames_nr -
                                              video_test_frames_nr)
                        tot_rec_frames_nr -= (tot_segments_frames_nr -
                                              video_test_frames_nr)

                elif sim_tracking:

                    # Simulate tracking
                    # (every frame of this video contains the same person)

                    frames = results[c.FRAMES_KEY]

                    [assigned_tag, final_confidence] = aggregate_frame_results_in_sim_tracking(frames, fm)

                    print('assigned_tag = ' + assigned_tag)

                    if assigned_tag == ann_face_tag:

                        people_true_positives_dict[assigned_tag] += len(frames)
                        tot_rec_frames_nr += len(frames)
                        true_pos_confidence_list.append(final_confidence)

                    else:

                        if assigned_tag != 'Undefined':

                            people_false_positives_dict[assigned_tag] += len(
                                frames)
                            false_pos_confidence_list.append(final_confidence)

                else:

                    frames = results[c.FRAMES_KEY]

                    frame_counter = 0
                    prev_frame_counter = -1
                    for frame in frames:

                        assigned_tag = 'Undefined'
                        confidence = -1

                        faces = frame[c.FACES_KEY]
                        
                        time_stamp = frame[c.ELAPSED_VIDEO_TIME_KEY]
                        
                        experiment_dict_frame = {
                        c.ELAPSED_VIDEO_TIME_KEY: time_stamp}

                        if len(faces) != 0:

                            face = faces[0]

                            assigned_tag = face[c.ASSIGNED_TAG_KEY]
                            
                            experiment_dict_faces = []
                            
                            experiment_dict_face = {
                            c.ASSIGNED_TAG_KEY: assigned_tag}

                            experiment_dict_faces.append(experiment_dict_face)
                            
                            if len(faces) > 1:
                                
                                for face_counter in range(1, len(faces)):
                                    
                                    other_face = faces[face_counter]
                                    
                                    other_face_assigned_tag = other_face[c.ASSIGNED_TAG_KEY]
                                    
                                    experiment_dict_face = {
                                    c.ASSIGNED_TAG_KEY: other_face_assigned_tag}

                                    experiment_dict_faces.append(experiment_dict_face)

                            confidence = face[c.CONFIDENCE_KEY]

                            bbox = face[c.BBOX_KEY]

                            if((frame_counter > 0) and
                                   (frame_counter <= (prev_frame_counter + c.MAX_FR_WITH_MISSED_DET + 1))):

                                bbox_x = bbox[0]
                                bbox_y = bbox[1]
                                bbox_w = bbox[2]
                                
                                prev_bbox_x = prev_bbox[0]
                                prev_bbox_y = prev_bbox[1]
                                prev_bbox_w = prev_bbox[2]

                                delta_x = (abs(bbox_x - prev_bbox_x) /
                                           float(prev_bbox_w))
                                delta_y = (abs(bbox_x - prev_bbox_x) /
                                           float(prev_bbox_w))
                                delta_w = (abs(bbox_w - prev_bbox_w) /
                                           float(prev_bbox_w))

                                video_delta_xs.append(delta_x)
                                video_delta_ys.append(delta_y)
                                video_delta_ws.append(delta_w)

                                if((delta_x > ce.MAX_DELTA_PCT_X) or
                                           (delta_y > ce.MAX_DELTA_PCT_Y) and
                                           (delta_w > ce.MAX_DELTA_PCT_W)):

                                    print('delta_x: ', delta_x)
                                    print('delta_y: ', delta_y)
                                    print('delta_w: ', delta_w)

                            prev_frame_counter = frame_counter

                            prev_bbox = bbox
                            
                            experiment_dict_frame[c.FACES_KEY] = experiment_dict_faces

                            experiment_dict_frame[c.ASSIGNED_TAG_KEY] = assigned_tag
                            
                        else:
                            
                            experiment_dict_frame[c.FACES_KEY] = "No face detected"

                            experiment_dict_frame[c.ASSIGNED_TAG_KEY] = "No face detected"
                            
                        experiment_dict_frame[c.CONFIDENCE_KEY] = confidence
                            
                        experiment_dict_frames.append(experiment_dict_frame)

                        if assigned_tag == ann_face_tag:

                            people_true_positives_dict[assigned_tag] += 1
                            tot_rec_frames_nr += 1
                            true_pos_confidence_list.append(confidence)

                        else:

                            if assigned_tag != 'Undefined':

                                people_false_positives_dict[assigned_tag] += 1
                                false_pos_confidence_list.append(confidence)

                        frame_counter += 1
                
                experiment_dict[ce.VIDEO_COUNTER_KEY] = number_of_anal_video
        
                experiment_dict[c.ANN_TAG_KEY] = ann_face_tag
                
                if sim_tracking:
                    
                    experiment_dict[c.ASSIGNED_TAG_KEY] = assigned_tag
                    experiment_dict[c.CONFIDENCE_KEY] = final_confidence
                
                else:
                
                    experiment_dict[c.FRAMES_KEY] = experiment_dict_frames
                
                save_YAML_file(
                    results_path + ann_face_tag + ".yml", experiment_dict)
                
                experiment_dict_list.append(experiment_dict)

                number_of_anal_video += 1
                    
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
    if number_of_anal_video > 0:
    
        csv_file_path = results_path + ce.CSV_FILE_NAME
            
        save_experiment_results_in_CSV_file(
            csv_file_path, experiment_dict_list, sim_tracking)
    
        # Calculate statistics for each person
        people_precision_list = []
        people_recall_list = []
        people_f1_list = []

        print('\nTRUE POSITIVES\n')
        print(people_true_positives_dict)
        print('\nFALSE POSITIVES\n')
        print(people_false_positives_dict)
        print('\nTEST FRAMES NR\n')
        print(people_test_frames_nr_dict)    
        
        for tag in tags:
    
            if tag in tested_people_tag_list:
    
                person_true_positives = people_true_positives_dict[tag]
                person_false_positives = people_false_positives_dict[tag]
                person_test_frames_nr = people_test_frames_nr_dict[tag]
    
                person_precision = 0
                if person_true_positives != 0:
                    person_precision = (float(person_true_positives) /
                                        float(person_true_positives +
                                              person_false_positives))
                people_precision_list.append(person_precision)
            
                person_recall = 0
                if person_test_frames_nr != 0:
                    person_recall = (float(person_true_positives) /
                                     person_test_frames_nr)
                people_recall_list.append(person_recall)

                person_f1 = 0
                if (person_precision != 0) and (person_recall != 0):
                    person_f1 = (2 * (person_precision * person_recall) /
                                 (person_precision + person_recall))
                people_f1_list.append(person_f1)

        mean_precision = float(numpy.mean(people_precision_list))
        std_precision = float(numpy.std(people_precision_list))

        mean_recall = float(numpy.mean(people_recall_list))
        std_recall = float(numpy.std(people_recall_list))

        mean_f1 = float(numpy.mean(people_f1_list))
        std_f1 = float(numpy.std(people_f1_list))

        recognition_rate = float(tot_rec_frames_nr) / float(tot_test_frames_nr)

        mean_rec_time /= number_of_anal_video
    
        mean_true_pos_confidence = float(numpy.mean(true_pos_confidence_list))
        std_true_pos_confidence = float(numpy.std(true_pos_confidence_list))

        mean_false_pos_confidence = float(numpy.mean(false_pos_confidence_list))
        std_false_pos_confidence = float(numpy.std(false_pos_confidence_list))

        print("\n ### RESULTS ###\n")

        print('\nRecognition rate: ' + str(recognition_rate * 100) + '%')
        print('Mean of precision: ' + str(mean_precision * 100) + '%')
        print('Standard deviation of precision: ' + str(
            std_precision * 100) + '%')
        print('Mean of recall: ' + str(mean_recall * 100) + '%')
        print('Standard deviation of recall: ' + str(std_recall * 100) + '%')
        print('Mean of f1: ' + str(mean_f1 * 100) + '%')
        print('Standard deviation of f1: ' + str(std_f1 * 100) + '%')
        print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')

        print('Recognition rate: ' + str(recognition_rate))
        print('Mean of precision: ' + str(mean_precision))
        print('Standard deviation of precision: ' + str(std_precision))
        print('Mean of recall: ' + str(mean_recall))
        print('Standard deviation of recall: ' + str(std_recall))
        print('Mean of f1: ' + str(mean_f1))
        print('Standard deviation of f1: ' + str(std_f1))
        print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')

        print('Mean of confidence for true positives: ' + str(
            mean_true_pos_confidence))
        print('Standard deviation of confidence for true positives: ' + str(
            std_true_pos_confidence))
        print('Mean of confidence for false positives: ' + str(
            mean_false_pos_confidence))
        print('Standard deviation of confidence for false positives: ' + str(
            std_false_pos_confidence))

    else:
        
        print 'No video was analyzed'


if __name__ == "__main__":

    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Execute face recognition tests")
    parser.add_argument("-config", help="configuration file")
    args = parser.parse_args()

    params = None

    if args.config:
        # Load given configuration file
        try:
            params = load_YAML_file(args.config)
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
            print("Default configuration file will be used")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    fr_video_experiments(params, False)
