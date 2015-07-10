import argparse
import math
import numpy
import os
import sys
import unittest

import constants_for_experiments as ce
from face_models_test import TestFaceModels
from people_clustering_experiments import PeopleClusterExtractor
from utils_for_experiments import load_experiment_results
from video_face_extractor_test import TestVideoFaceExtractor

path_to_be_appended = ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.utils import load_YAML_file, save_YAML_file
from tools.video_face_extractor import VideoFaceExtractor


def calculate_rec_time_auto_man(auto_segments, man_segments):
    """
    Calculate amount of time in which
    segments automatic annotated and manually annotated  corresponds

    :type auto_segments: list
    :param auto_segments: automatic annotated segments

    :type man_segments: list
    :param man_segments: manually annotated segments

    :rtype: float
    :returns: amount of time (in milliseconds)
    """

    rec = 0.0  # Correctly recognized video (in milliseconds)

    for auto_segment in auto_segments:

        auto_start = auto_segment[c.SEGMENT_START_KEY]

        auto_duration = auto_segment[c.SEGMENT_DURATION_KEY]

        auto_end = auto_start + auto_duration

        # In manual annotation, we consider as start
        # end as end previous second

        auto_start = math.ceil(auto_start / 1000.0) * 1000

        auto_end = math.floor(auto_end / 1000.0) * 1000

        auto_duration = auto_end - auto_start

        if auto_duration < 0:

            auto_tag = auto_segment[c.ANN_TAG_KEY]

            print(auto_start)
            print(auto_end)
            print(auto_segment)
            print(auto_tag)

            print 'Warning! Duration is less than zero'

        # Check if there is a segment in manual annotations
        # that corresponds to this segment

        for man_segment in man_segments:

            man_start = man_segment[c.SEGMENT_START_KEY]

            man_duration = man_segment[c.SEGMENT_DURATION_KEY]

            man_end = man_start + man_duration

            # Real segment is smaller than automatic segment
            if (man_start >= auto_start) and (man_end <= auto_end):

                # Whole real segment is correctly recognized
                rec += man_duration

            # Real segment is bigger than automatic segment
            elif (man_start <= auto_start) and (man_end >= auto_end):

                # Whole automatic segment is correctly recognized
                rec += auto_duration

            # Real segment starts before automatic segment
            elif (man_start <= auto_start) and (man_end >= auto_start):

                # Both automatic and real segments are
                # partially correctly recognized
                rec += man_end - auto_start

            # Real segment starts after automatic segment
            elif (man_start <= auto_end) and (man_end >= auto_end):

                # Both automatic and real segments are
                # partially correctly recognized
                rec += auto_end - man_start

    return rec


def calculate_rec_time_man_auto(man_segments, auto_segments):
    """
    Calculate amount of time in which
    segments manually annotated and automatic annotated corresponds

    :type man_segments: list
    :param man_segments: manually annotated segments

    :type auto_segments: list
    :param auto_segments: automatic annotated segments

    :rtype: float
    :returns: amount of time (in milliseconds)
    """

    rec = 0.0  # Correctly recognized video (in milliseconds)

    for man_segment in man_segments:

        man_start = man_segment[c.SEGMENT_START_KEY]
        man_duration = man_segment[c.SEGMENT_DURATION_KEY]
        man_end = man_start + man_duration

        # Check if there is a segment in automatic annotations
        # that corresponds to this segment

        for auto_segment in auto_segments:

            auto_start = auto_segment[c.SEGMENT_START_KEY]
            auto_duration = auto_segment[c.SEGMENT_DURATION_KEY]
            auto_end = auto_start + auto_duration

            # Real segment is smaller than automatic segment
            if (man_start >= auto_start) and (man_end <= auto_end):

                # Whole real segment is correctly recognized
                rec += man_duration

            # Real segment is bigger than automatic segment
            elif (man_start <= auto_start) and (man_end >= auto_end):

                # Whole automatic segment is correctly recognized
                rec += auto_duration

            # Real segment starts before automatic segment
            elif (man_start <= auto_start) and (man_end >= auto_start):

                # Both automatic and real segments are
                # partially correctly recognized
                rec = rec + (man_end - auto_start)

            # Real segment starts after automatic segment
            elif (man_start <= auto_end) and (man_end >= auto_end):

                # Both automatic and real segments are
                # partially correctly recognized
                rec = rec + (auto_end - man_start)

    return rec




# Save in csv file given list of experiments
def save_video_indexing_experiments_in_CSV_file(file_path, experiments):
    """
    Save experiments in CSV file

    :type file_path: string
    :param file_path: path of CSV file

    :type experiments: list
    :param experiments: list of experiments
    """

    stream = open(file_path, 'w')
    
    # Write csv header
    stream.write(ce.CODE_VERSION_KEY + ',' +
                 ce.EXPERIMENT_NUMBER_KEY + ',' +
                 ce.USE_PEOPLE_CLUSTERING_KEY + ',' +
                 ce.USE_PEOPLE_RECOGNITION_KEY + ',' + 
                 ce.VIDEO_NAME_KEY + ',' + 
                 c.VIDEO_DURATION_KEY + ',' + 
                 c.VIDEO_FPS_KEY + ',' +
                 c.USED_FPS_KEY + ',' +
                 c.USED_FPS_FOR_CAPTIONS_KEY + ',' +

                 c.CHECK_EYE_POSITIONS_KEY + ',' +
                 c.CLASSIFIERS_DIR_PATH_KEY + ',' +
                 c.EYE_DETECTION_CLASSIFIER_KEY + ',' +
                 c.FACE_DETECTION_ALGORITHM_KEY + ',' +
                 c.FLAGS_KEY + ',' +
                 c.MIN_NEIGHBORS_KEY + ',' +
                 c.MIN_SIZE_HEIGHT_KEY + ',' +
                 c.MIN_SIZE_WIDTH_KEY + ',' +
                 c.SCALE_FACTOR_KEY + ',' +
                 c.NOSE_DETECTION_CLASSIFIER_KEY + ',' +

                 ce.EXPERIMENT_ALGORITHM_KEY + ',' +
                 c.LBP_RADIUS_KEY + ',' + 
                 c.LBP_NEIGHBORS_KEY + ',' +
                 c.LBP_GRID_X_KEY + ',' + 
                 c.LBP_GRID_Y_KEY + ',' +
                 c.CROPPED_FACE_HEIGHT_KEY + ',' +
                 c.CROPPED_FACE_WIDTH_KEY + ',' +
                 c.OFFSET_PCT_X_KEY + ',' + 
                 c.OFFSET_PCT_Y_KEY + ',' +
                 c.CONF_THRESHOLD_KEY + ',' + 
                 c.HALF_WINDOW_SIZE_KEY + ',' +
                 c.MIN_DETECTION_PCT_KEY + ',' + 
                 c.MIN_SEGMENT_DURATION_KEY + ',' +
                 c.TRACKING_MIN_INT_AREA_KEY + ',' + 
                 c.STD_MULTIPLIER_FRAME_KEY + ',' +
                 c.STD_MULTIPLIER_FACE_KEY + ',' + 
                 c.MAX_FR_WITH_MISSED_DET_KEY + ',' +
                 c.USE_ALIGNED_FACE_IN_TRACKING_KEY + ',' +
                 c.USE_AGGREGATION_KEY + ',' + 
                 c.USE_NOSE_POS_IN_DETECTION_KEY + ',' +
                 c.USE_NOSE_POS_IN_RECOGNITION_KEY + ',' + 
                 c.MAX_NOSE_DIFF_KEY + ',' +
                 ce.UPDATE_FACE_MODEL_AFTER_MERGING_KEY + ',' + 
                 c.USE_MAJORITY_RULE_KEY + ',' + 
                 c.USE_MEAN_CONFIDENCE_RULE_KEY + ',' + 
                 c.USE_MIN_CONFIDENCE_RULE_KEY + ',' +
                 
                 c.USE_CLOTHING_RECOGNITION_KEY + ',' +
                 c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY + ',' +
                 c.CLOTHES_BBOX_HEIGHT_KEY + ',' +
                 c.CLOTHES_BBOX_WIDTH_KEY + ',' +
                 c.CLOTHES_CHECK_METHOD_KEY + ',' +
                 c.CLOTHING_REC_HSV_CHANNELS_NR_KEY + ',' +
                 c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY + ',' +
                 c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY + ',' +
                 c.CLOTHING_REC_USE_3_BBOXES_KEY + ',' +
                 c.MIN_CLOTH_MODEL_SIZE_KEY + ',' +
                 c.NECK_HEIGHT_KEY + ',' +
                 c.HIST_SMOOTHING_KERNEL_SIZE_KEY + ',' +
                 c.CLOTHES_CONF_THRESH_KEY + ',' +
                 c.VARIABLE_CLOTHING_THRESHOLD_KEY + ',' +
                                  
                 c.USE_CAPTION_RECOGNITION_KEY + ',' +
                 c.USE_FACE_RECOGNITION_KEY + ',' +
                 c.GLOBAL_FACE_REC_THRESHOLD_KEY + ',' +
                 c.LEV_RATIO_PCT_THRESH_KEY + ',' +
                 c.MIN_TAG_LENGTH_KEY + ',' +
                 c.USE_BLACKLIST_KEY + ',' +
                 c.USE_LEVENSHTEIN_KEY + ',' +

                 c.FRAME_EXTRACTION_TIME_KEY + ',' +
                 c.FACE_DETECTION_TIME_KEY + ',' +
                 c.SHOT_CUT_DETECTION_TIME_KEY + ',' + 
                 c.FACE_TRACKING_TIME_KEY + ',' +
                 c.FACE_MODELS_CREATION_TIME_KEY + ',' + 
                 c.CLOTH_MODELS_CREATION_TIME_KEY + ',' +
                 c.PEOPLE_CLUSTERING_TIME_KEY + ',' +
                 c.PEOPLE_RECOGNITION_TIME_KEY + ',' +  
                 c.SEGMENTS_NR_KEY + ',' + 
                 c.PEOPLE_CLUSTERS_NR_KEY + ',' +
                 c.RELEVANT_PEOPLE_NR_KEY + ',' +

                 ce.PRECISION_KEY + ',' + 
                 ce.RECALL_KEY + ',' + 
                 ce.F1_KEY + ',' +
                 ce.MEAN_PRECISION_KEY + ',' + 
                 ce.STD_PRECISION_KEY + ',' +
                 ce.MEAN_RECALL_KEY + ',' + 
                 ce.STD_RECALL_KEY + ',' +
                 ce.MEAN_F1_KEY + ',' + 
                 ce.STD_F1_KEY + ',' +

                 ce.CAPTION_PRECISION_KEY + ',' +
                 ce.CAPTION_RECALL_KEY + ',' +
                 ce.CAPTION_F1_KEY + ',' +
                 ce.CAPTION_MEAN_PRECISION_KEY + ',' +
                 ce.CAPTION_STD_PRECISION_KEY + ',' +
                 ce.CAPTION_MEAN_RECALL_KEY + ',' +
                 ce.CAPTION_STD_RECALL_KEY + ',' +
                 ce.CAPTION_MEAN_F1_KEY + ',' +
                 ce.CAPTION_STD_F1_KEY + ',' +

                 ce.SAVED_FRAMES_NR_KEY + '\n')
                 
    for experiment_dict_extended in experiments:
        
        experiment_dict = experiment_dict_extended[ce.EXPERIMENT_KEY]
        
        stream.write(str(experiment_dict[ce.CODE_VERSION_KEY]) + ',' +
                     str(experiment_dict[ce.EXPERIMENT_NUMBER_KEY]) + ',' +
                     str(experiment_dict[ce.USE_PEOPLE_CLUSTERING_KEY]) + ',' +
                     str(experiment_dict[ce.USE_PEOPLE_RECOGNITION_KEY]) + ',' +                     
                     str(experiment_dict[ce.VIDEO_NAME_KEY]) + ',' +  
                     str(experiment_dict[c.VIDEO_DURATION_KEY]) + ',' + 
                     str(experiment_dict[c.VIDEO_FPS_KEY]) + ',' +
                     str(experiment_dict[c.USED_FPS_KEY]) + ',' +
                     str(experiment_dict[c.USED_FPS_FOR_CAPTIONS_KEY]) + ',' +
                     str(experiment_dict[c.CHECK_EYE_POSITIONS_KEY]) + ',' +
                     str(experiment_dict[c.CLASSIFIERS_DIR_PATH_KEY]) + ',' +
                     str(experiment_dict[c.EYE_DETECTION_CLASSIFIER_KEY]) + ',' +
                     str(experiment_dict[c.FACE_DETECTION_ALGORITHM_KEY]) + ',' +
                     str(experiment_dict[c.FLAGS_KEY]) + ',' +
                     str(experiment_dict[c.MIN_NEIGHBORS_KEY]) + ',' +
                     str(experiment_dict[c.MIN_SIZE_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[c.MIN_SIZE_WIDTH_KEY]) + ',' +
                     str(experiment_dict[c.SCALE_FACTOR_KEY]) + ',' +
                     str(experiment_dict[c.NOSE_DETECTION_CLASSIFIER_KEY]) + ',' +
                     str(experiment_dict[ce.EXPERIMENT_ALGORITHM_KEY]) + ',' +
                     str(experiment_dict[c.LBP_RADIUS_KEY]) + ',' + 
                     str(experiment_dict[c.LBP_NEIGHBORS_KEY]) + ',' +
                     str(experiment_dict[c.LBP_GRID_X_KEY]) + ',' + 
                     str(experiment_dict[c.LBP_GRID_Y_KEY]) + ',' +
                     str(experiment_dict[c.CROPPED_FACE_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[c.CROPPED_FACE_WIDTH_KEY]) + ',' +
                     str(experiment_dict[c.OFFSET_PCT_X_KEY]) + ',' + 
                     str(experiment_dict[c.OFFSET_PCT_Y_KEY]) + ',' +
                     str(experiment_dict[c.CONF_THRESHOLD_KEY]) + ',' + 
                     str(experiment_dict[c.HALF_WINDOW_SIZE_KEY]) + ',' +
                     str(experiment_dict[c.MIN_DETECTION_PCT_KEY]) + ',' + 
                     str(experiment_dict[c.MIN_SEGMENT_DURATION_KEY]) + ',' +
                     str(experiment_dict[c.TRACKING_MIN_INT_AREA_KEY]) + ',' + 
                     str(experiment_dict[c.STD_MULTIPLIER_FRAME_KEY]) + ',' +
                     str(experiment_dict[c.STD_MULTIPLIER_FACE_KEY]) + ',' + 
                     str(experiment_dict[c.MAX_FR_WITH_MISSED_DET_KEY]) + ',' +
                     str(experiment_dict[c.USE_ALIGNED_FACE_IN_TRACKING_KEY]) + ',' +
                     str(experiment_dict[c.USE_AGGREGATION_KEY]) + ',' + 
                     str(experiment_dict[c.USE_NOSE_POS_IN_DETECTION_KEY]) + ',' +
                     str(experiment_dict[c.USE_NOSE_POS_IN_RECOGNITION_KEY]) + ',' + 
                     str(experiment_dict[c.MAX_NOSE_DIFF_KEY]) + ',' +    
                     str(experiment_dict[ce.UPDATE_FACE_MODEL_AFTER_MERGING_KEY]) + ',' +
                     str(experiment_dict[c.USE_MAJORITY_RULE_KEY]) + ',' +
                     str(experiment_dict[c.USE_MEAN_CONFIDENCE_RULE_KEY]) + ',' +
                     str(experiment_dict[c.USE_MIN_CONFIDENCE_RULE_KEY]) + ',' +
                     
                     str(experiment_dict[c.USE_CLOTHING_RECOGNITION_KEY]) + ',' +
                     str(experiment_dict[c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHES_BBOX_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHES_BBOX_WIDTH_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHES_CHECK_METHOD_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHING_REC_USE_3_BBOXES_KEY]) + ',' +
                     str(experiment_dict[c.MIN_CLOTH_MODEL_SIZE_KEY]) + ',' +
                     str(experiment_dict[c.NECK_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[c.HIST_SMOOTHING_KERNEL_SIZE_KEY]) + ',' +
                     str(experiment_dict[c.CLOTHES_CONF_THRESH_KEY]) + ',' +
                     str(experiment_dict[c.VARIABLE_CLOTHING_THRESHOLD_KEY]) + ',' +
                                        
                     str(experiment_dict[c.USE_CAPTION_RECOGNITION_KEY]) + ',' +
                     str(experiment_dict[c.USE_FACE_RECOGNITION_KEY]) + ',' +
                     str(experiment_dict[c.GLOBAL_FACE_REC_THRESHOLD_KEY]) + ',' +
                     str(experiment_dict[c.LEV_RATIO_PCT_THRESH_KEY]) + ',' +
                     str(experiment_dict[c.MIN_TAG_LENGTH_KEY]) + ',' +
                     str(experiment_dict[c.USE_BLACKLIST_KEY]) + ',' +
                     str(experiment_dict[c.USE_LEVENSHTEIN_KEY]) + ',' +

                     str(experiment_dict[c.FRAME_EXTRACTION_TIME_KEY]) + ',' +
                     str(experiment_dict[c.FACE_DETECTION_TIME_KEY]) + ',' +
                     str(experiment_dict[c.SHOT_CUT_DETECTION_TIME_KEY]) + ',' + 
                     str(experiment_dict[c.FACE_TRACKING_TIME_KEY]) + ',' +
                     str(experiment_dict[c.FACE_MODELS_CREATION_TIME_KEY]) + ',' + 
                     str(experiment_dict[c.CLOTH_MODELS_CREATION_TIME_KEY]) + ',' + 
                     str(experiment_dict[c.PEOPLE_CLUSTERING_TIME_KEY]) + ',' + 
                     str(experiment_dict[c.SEGMENTS_NR_KEY]) + ',' + 
                     str(experiment_dict[c.PEOPLE_CLUSTERS_NR_KEY]) + ',' +
                     str(experiment_dict[c.RELEVANT_PEOPLE_NR_KEY]) + ',' +

                     str(experiment_dict[ce.PRECISION_KEY]) + ',' + 
                     str(experiment_dict[ce.RECALL_KEY]) + ',' + 
                     str(experiment_dict[ce.F1_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_PRECISION_KEY]) + ',' + 
                     str(experiment_dict[ce.STD_PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_RECALL_KEY]) + ',' + 
                     str(experiment_dict[ce.STD_RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.MEAN_F1_KEY]) + ',' + 
                     str(experiment_dict[ce.STD_F1_KEY]) + ',' +

                     str(experiment_dict[ce.CAPTION_PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_F1_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_MEAN_PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_STD_PRECISION_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_MEAN_RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_STD_RECALL_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_MEAN_F1_KEY]) + ',' +
                     str(experiment_dict[ce.CAPTION_STD_F1_KEY]) + ',' +

                     str(experiment_dict[ce.SAVED_FRAMES_NR_KEY]) + '\n')
                     
    stream.close()

    
def video_indexing_experiments(resource_path, resource_id, params):
    """
    Execute video indexing experiments

    :type resource_path: string
    :param resource_path: file path of resource

    :type resource_id: string
    :param resource_id: identifier of resource

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test
    """

    man_ann_path = ce.ANNOTATIONS_PATH
    use_people_recognition = ce.USE_PEOPLE_RECOGNITION
    
    if params is not None:
        if ce.ANNOTATIONS_PATH_KEY in params:
            man_ann_path = params[ce.ANNOTATIONS_PATH_KEY]
        if ce.USE_PEOPLE_RECOGNITION_KEY in params:
            use_people_recognition = params[ce.USE_PEOPLE_RECOGNITION_KEY]   
    
    fs = None
    
    if use_people_recognition:
    
        fs = VideoFaceExtractor(resource_path, resource_id, params)
        # Delete results of previous experiment
        fs.delete_recognition_results()
        fs.analyze_video()
        
    else:

        fs = PeopleClusterExtractor(resource_path, resource_id, params)
        fs.analyze_video()
    
    # Directory for this video  
    video_path = fs.video_path
    
    # Directory with simple annotations
    simple_ann_path = os.path.join(video_path, c.FACE_SIMPLE_ANNOTATION_DIR)
    
    # Get tags by analyzing folder with annotation files
    people_precision_dict = {}  # Video
    people_cap_prec_dict = {}  # Captions
    people_recall_dict = {}  # Video
    people_cap_rec_dict = {}  # Captions
    tags = []
    for ann_file in os.listdir(man_ann_path):
        
        tag = os.path.splitext(ann_file)[0]
        tags.append(tag)
        people_precision_dict[tag] = 0
        people_cap_prec_dict[tag] = 0
        people_recall_dict[tag] = 0
        people_cap_rec_dict[tag] = 0
    
    # Calculate recall
    
    video_tot_rec = 0
    video_tot_cap_rec = 0
    video_tot_duration = 0
    video_tot_cap_duration = 0
    
    # Iterate through manual annotations
    for ann_file in os.listdir(man_ann_path):
        
        ann_path = os.path.join(man_ann_path, ann_file)
        man_dict = load_YAML_file(ann_path)
        man_tag = man_dict[c.ANN_TAG_KEY]
        auto_ann_file = os.path.join(simple_ann_path, ann_file)
            
        if not(os.path.exists(auto_ann_file)):
            print(auto_ann_file)
            error_str = ('Warning! Automatic annotation for ' +
                         ann_file + ' does not exist')
            print error_str
            continue
        
        auto_dict = load_YAML_file(auto_ann_file)
        
        if (auto_dict is None) or (c.ANN_TAG_KEY not in auto_dict):
            print 'Warning! Automatic annotation file does not exist!'
            break        
        
        auto_tag = auto_dict[c.ANN_TAG_KEY]
        
        if man_tag != auto_tag:
            print 'Warning! Tags are different!'
            break

        # Calculate recall for correctly recognized video
        tot_duration = man_dict[c.TOT_SEGMENT_DURATION_KEY]
        video_tot_duration = video_tot_duration + tot_duration
        man_segments = man_dict[c.SEGMENTS_KEY]
        auto_segments = auto_dict[c.SEGMENTS_KEY]
        rec = calculate_rec_time_man_auto(man_segments, auto_segments)
        recall = rec / tot_duration
        people_recall_dict[man_tag] = recall
        video_tot_rec += rec

        # Calculate recall for correctly recognized captions
        if c.CAPTION_SEGMENTS_KEY in auto_dict:
            tot_cap_duration = man_dict[c.TOT_CAPTION_SEGMENT_DURATION_KEY]
            video_tot_cap_duration = video_tot_cap_duration + tot_cap_duration
            man_cap_segments = man_dict[c.CAPTION_SEGMENTS_KEY]
            auto_cap_segments = auto_dict[c.CAPTION_SEGMENTS_KEY]
            cap_rec = calculate_rec_time_man_auto(
                man_cap_segments, auto_cap_segments)
            cap_recall = cap_rec / tot_cap_duration
            people_cap_rec_dict[man_tag] = cap_recall
            video_tot_cap_rec += cap_rec
        
    tot_recall = 0
    if video_tot_duration > 0:
        tot_recall = video_tot_rec / video_tot_duration

    tot_cap_recall = 0
    if video_tot_cap_duration > 0:
        tot_cap_recall = video_tot_cap_rec / video_tot_cap_duration
    
    # Calculate precision
    
    video_tot_rec = 0
    video_tot_cap_rec = 0
    video_tot_duration = 0
    video_tot_cap_duration = 0
    
    # Iterate through automatic annotations
    for ann_file in os.listdir(simple_ann_path):
        
        ann_path = os.path.join(simple_ann_path, ann_file)
        auto_dict = load_YAML_file(ann_path)
        auto_tag = auto_dict[c.ANN_TAG_KEY]
        man_ann_file = os.path.join(man_ann_path, ann_file)
        man_dict = load_YAML_file(man_ann_file)
        
        if (man_dict is None) or (c.ANN_TAG_KEY not in man_dict):
            print 'Warning! Manual annotation file does not exist!'
            print man_ann_file
            break
        
        man_tag = man_dict[c.ANN_TAG_KEY]
        
        if man_tag != auto_tag:
            print 'Warning! Tags are different!'
            break
                    
        # Calculate precision for correctly recognized video
        tot_duration = auto_dict[c.TOT_SEGMENT_DURATION_KEY]
        auto_segments = auto_dict[c.SEGMENTS_KEY]
        man_segments = man_dict[c.SEGMENTS_KEY]
        rec = calculate_rec_time_auto_man(auto_segments, man_segments)
        precision = 0

        if tot_duration != 0:
            precision = rec / tot_duration      
                    
        people_precision_dict[auto_tag] = precision
        video_tot_rec += rec
        video_tot_duration = video_tot_duration + tot_duration

        # Calculate precision for correctly recognized captions
        if c.CAPTION_SEGMENTS_KEY in auto_dict:
            tot_cap_duration = auto_dict[c.TOT_CAPTION_SEGMENT_DURATION_KEY]
            auto_cap_segments = auto_dict[c.CAPTION_SEGMENTS_KEY]
            man_cap_segments = man_dict[c.CAPTION_SEGMENTS_KEY]
            cap_rec = calculate_rec_time_auto_man(
                auto_cap_segments, man_cap_segments)
            cap_prec = 0

            if tot_cap_duration != 0:
                cap_prec = cap_rec / tot_cap_duration

            people_cap_prec_dict[auto_tag] = cap_prec
            video_tot_cap_rec += cap_rec
            video_tot_cap_duration = video_tot_cap_duration + tot_cap_duration
        
    tot_precision = 0
    
    if video_tot_duration != 0:
        tot_precision = video_tot_rec / video_tot_duration

    tot_cap_precision = 0
    if video_tot_cap_duration != 0:
        tot_cap_precision = video_tot_cap_rec / video_tot_cap_duration
    
    # Calculate f-measure
    tot_f1 = 0
    if (tot_precision != 0) and (tot_recall != 0):
        tot_f1 = 2 * (tot_precision * tot_recall) / (tot_precision + tot_recall)

    tot_cap_f1 = 0
    if (tot_cap_precision != 0) and (tot_cap_recall != 0):
        tot_cap_f1 = 2 * ((tot_cap_precision * tot_cap_recall) /
                          (tot_cap_precision + tot_cap_recall))
        
    # Calculate statistics for each person
    people_precision_list = []
    people_recall_list = []
    people_f1_list = []
    people_cap_precision_list = []
    people_cap_recall_list = []
    people_cap_f1_list = []
    
    for tag in tags:
        
        # Video
        person_precision = people_precision_dict[tag]
        people_precision_list.append(person_precision)
        
        person_recall = people_recall_dict[tag]
        people_recall_list.append(person_recall)
    
        person_f1 = 0
        if (person_precision != 0) and (person_recall != 0):
            person_f1 = (2 * (person_precision * person_recall) /
                         (person_precision + person_recall))
            
        people_f1_list.append(person_f1)

        # Captions
        person_cap_precision = people_cap_prec_dict[tag]
        people_cap_precision_list.append(person_cap_precision)

        person_cap_recall = people_cap_rec_dict[tag]
        people_cap_recall_list.append(person_cap_recall)

        person_cap_f1 = 0
        if (person_cap_precision != 0) and (person_cap_recall != 0):
            person_cap_f1 = (2 * (person_cap_precision * person_cap_recall) /
                         (person_cap_precision + person_cap_recall))

        people_cap_f1_list.append(person_cap_f1)
        
    # Get mean and standard deviation of precision, recall and f-measure
    mean_precision = float(numpy.mean(people_precision_list))
    std_precision = float(numpy.std(people_precision_list))

    mean_recall = float(numpy.mean(people_recall_list))
    std_recall = float(numpy.std(people_recall_list))

    mean_f1 = float(numpy.mean(people_f1_list))
    std_f1 = float(numpy.std(people_f1_list))

    print("\n ### RESULTS ###\n")

    print('Tot precision: ' + str(tot_precision))
    print('Tot recall: ' + str(tot_recall))
    print('Tot f1: ' + str(tot_f1))

    print('Mean of precision: ' + str(mean_precision))
    print('Standard deviation of precision: ' + str(std_precision))
    print('Mean of recall: ' + str(mean_recall))
    print('Standard deviation of recall: ' + str(std_recall))
    print('Mean of f1: ' + str(mean_f1))
    print('Standard deviation of f1: ' + str(std_f1))

    mean_cap_precision = float(numpy.mean(people_cap_precision_list))
    std_cap_precision = float(numpy.std(people_cap_precision_list))

    mean_cap_recall = float(numpy.mean(people_cap_recall_list))
    std_cap_recall = float(numpy.std(people_cap_recall_list))

    mean_cap_f1 = float(numpy.mean(people_cap_f1_list))
    std_cap_f1 = float(numpy.std(people_cap_f1_list))

    print('\nTot caption precision: ' + str(tot_cap_precision))
    print('Tot caption recall: ' + str(tot_cap_recall))
    print('Tot caption f1: ' + str(tot_cap_f1))

    print('Mean of caption precision: ' + str(mean_cap_precision))
    print('Standard deviation of caption precision: ' + str(std_cap_precision))
    print('Mean of caption recall: ' + str(mean_cap_recall))
    print('Standard deviation of caption recall: ' + str(std_cap_recall))
    print('Mean of caption f1: ' + str(mean_cap_f1))
    print('Standard deviation of caption f1: ' + str(std_cap_f1))
    
    new_experiment_dict = {ce.VIDEO_NAME_KEY: fs.resource_name,
                           ce.USE_PEOPLE_RECOGNITION_KEY: use_people_recognition}

    duration = fs.video_frames / fs.fps
    
    new_experiment_dict[c.VIDEO_DURATION_KEY] = duration
    new_experiment_dict[c.VIDEO_FPS_KEY] = fs.fps

    new_experiment_dict[ce.CODE_VERSION_KEY] = -1
    if ce.CODE_VERSION_KEY in fs.params:
        new_experiment_dict[ce.CODE_VERSION_KEY] = fs.params[ce.CODE_VERSION_KEY]

    new_experiment_dict[ce.USE_PEOPLE_CLUSTERING_KEY] = ce.USE_PEOPLE_CLUSTERING_KEY
    if ce.USE_PEOPLE_CLUSTERING_KEY in fs.params:
        new_experiment_dict[ce.USE_PEOPLE_CLUSTERING_KEY] = fs.params[ce.USE_PEOPLE_CLUSTERING_KEY]

    new_experiment_dict[c.USED_FPS_KEY] = c.USED_FPS
    if c.USED_FPS_KEY in fs.params:
        new_experiment_dict[c.USED_FPS_KEY] = fs.params[c.USED_FPS_KEY]

    new_experiment_dict[c.USED_FPS_FOR_CAPTIONS_KEY] = c.USED_FPS_FOR_CAPTIONS
    if c.USED_FPS_FOR_CAPTIONS_KEY in fs.params:
        new_experiment_dict[c.USED_FPS_FOR_CAPTIONS_KEY] = fs.params[
            c.USED_FPS_FOR_CAPTIONS_KEY]

    new_experiment_dict[c.CHECK_EYE_POSITIONS_KEY] = c.CHECK_EYE_POSITIONS
    if c.CHECK_EYE_POSITIONS_KEY in fs.params:
        new_experiment_dict[c.CHECK_EYE_POSITIONS_KEY] = fs.params[c.CHECK_EYE_POSITIONS_KEY]

    new_experiment_dict[c.CLASSIFIERS_DIR_PATH_KEY] = c.CLASSIFIERS_DIR_PATH
    if c.CLASSIFIERS_DIR_PATH_KEY in fs.params:
        new_experiment_dict[c.CLASSIFIERS_DIR_PATH_KEY] = fs.params[c.CLASSIFIERS_DIR_PATH_KEY]

    new_experiment_dict[c.EYE_DETECTION_CLASSIFIER_KEY] = c.EYE_DETECTION_CLASSIFIER
    if c.EYE_DETECTION_CLASSIFIER_KEY in fs.params:
        new_experiment_dict[c.EYE_DETECTION_CLASSIFIER_KEY] = fs.params[c.EYE_DETECTION_CLASSIFIER_KEY]

    new_experiment_dict[c.FACE_DETECTION_ALGORITHM_KEY] = c.FACE_DETECTION_ALGORITHM
    if c.FACE_DETECTION_ALGORITHM_KEY in fs.params:
        new_experiment_dict[c.FACE_DETECTION_ALGORITHM_KEY] = fs.params[c.FACE_DETECTION_ALGORITHM_KEY]

    new_experiment_dict[c.FLAGS_KEY] = c.FACE_DETECTION_FLAGS
    if c.FLAGS_KEY in fs.params:
        new_experiment_dict[c.FLAGS_KEY] = fs.params[c.FLAGS_KEY]

    new_experiment_dict[c.MIN_NEIGHBORS_KEY] = c.FACE_DETECTION_MIN_NEIGHBORS
    if c.MIN_NEIGHBORS_KEY in fs.params:
        new_experiment_dict[c.MIN_NEIGHBORS_KEY] = fs.params[c.MIN_NEIGHBORS_KEY]

    new_experiment_dict[c.MIN_SIZE_HEIGHT_KEY] = c.FACE_DETECTION_MIN_SIZE_HEIGHT
    if c.MIN_SIZE_HEIGHT_KEY in fs.params:
        new_experiment_dict[c.MIN_SIZE_HEIGHT_KEY] = fs.params[c.MIN_SIZE_HEIGHT_KEY]

    new_experiment_dict[c.MIN_SIZE_WIDTH_KEY] = c.FACE_DETECTION_MIN_SIZE_WIDTH
    if c.MIN_SIZE_WIDTH_KEY in fs.params:
        new_experiment_dict[c.MIN_SIZE_WIDTH_KEY] = fs.params[c.MIN_SIZE_WIDTH_KEY]

    new_experiment_dict[c.SCALE_FACTOR_KEY] = c.FACE_DETECTION_SCALE_FACTOR
    if c.SCALE_FACTOR_KEY in fs.params:
        new_experiment_dict[c.SCALE_FACTOR_KEY] = fs.params[c.SCALE_FACTOR_KEY]

    new_experiment_dict[c.NOSE_DETECTION_CLASSIFIER_KEY] = c.NOSE_DETECTION_CLASSIFIER
    if c.NOSE_DETECTION_CLASSIFIER_KEY in fs.params:
        new_experiment_dict[c.NOSE_DETECTION_CLASSIFIER_KEY] = fs.params[c.NOSE_DETECTION_CLASSIFIER_KEY]
        
    new_experiment_dict[ce.EXPERIMENT_ALGORITHM_KEY] = ce.FACE_MODEL_ALGORITHM
    if ce.FACE_MODEL_ALGORITHM_KEY in fs.params:
        new_experiment_dict[ce.EXPERIMENT_ALGORITHM_KEY] = fs.params[
            ce.FACE_MODEL_ALGORITHM_KEY]
    
    new_experiment_dict[c.LBP_RADIUS_KEY] = c.LBP_RADIUS
    if c.LBP_RADIUS_KEY in fs.params:
        new_experiment_dict[c.LBP_RADIUS_KEY] = fs.params[c.LBP_RADIUS_KEY]
        
    new_experiment_dict[c.LBP_NEIGHBORS_KEY] = c.LBP_NEIGHBORS
    if c.LBP_NEIGHBORS_KEY in fs.params:
        new_experiment_dict[c.LBP_NEIGHBORS_KEY] = fs.params[
            c.LBP_NEIGHBORS_KEY]
        
    new_experiment_dict[c.LBP_GRID_X_KEY] = c.LBP_GRID_X
    if c.LBP_GRID_X_KEY in fs.params:
        new_experiment_dict[c.LBP_GRID_X_KEY] = fs.params[c.LBP_GRID_X_KEY]
        
    new_experiment_dict[c.LBP_GRID_Y_KEY] = c.LBP_GRID_Y
    if c.LBP_GRID_Y_KEY in fs.params:
        new_experiment_dict[c.LBP_GRID_Y_KEY] = fs.params[c.LBP_GRID_Y_KEY]
        
    new_experiment_dict[c.CROPPED_FACE_HEIGHT_KEY] = c.CROPPED_FACE_HEIGHT
    if c.CROPPED_FACE_HEIGHT_KEY in fs.params:
        new_experiment_dict[c.CROPPED_FACE_HEIGHT_KEY] = fs.params[
            c.CROPPED_FACE_HEIGHT_KEY]
        
    new_experiment_dict[c.CROPPED_FACE_WIDTH_KEY] = c.CROPPED_FACE_WIDTH
    if c.CROPPED_FACE_WIDTH_KEY in fs.params:
        new_experiment_dict[c.CROPPED_FACE_WIDTH_KEY] = fs.params[
            c.CROPPED_FACE_WIDTH_KEY]
    
    new_experiment_dict[c.OFFSET_PCT_X_KEY] = c.OFFSET_PCT_X
    if c.OFFSET_PCT_X_KEY in fs.params:
        new_experiment_dict[c.OFFSET_PCT_X_KEY] = fs.params[c.OFFSET_PCT_X_KEY]
    
    new_experiment_dict[c.OFFSET_PCT_Y_KEY] = c.OFFSET_PCT_Y
    if c.OFFSET_PCT_Y_KEY in fs.params:
        new_experiment_dict[c.OFFSET_PCT_Y_KEY] = fs.params[c.OFFSET_PCT_Y_KEY]
    
    new_experiment_dict[c.CONF_THRESHOLD_KEY] = c.CONF_THRESHOLD
    if c.CONF_THRESHOLD_KEY in fs.params:
        new_experiment_dict[c.CONF_THRESHOLD_KEY] = fs.params[
            c.CONF_THRESHOLD_KEY]
        
    new_experiment_dict[c.HALF_WINDOW_SIZE_KEY] = c.HALF_WINDOW_SIZE
    if c.HALF_WINDOW_SIZE_KEY in fs.params:
        new_experiment_dict[c.HALF_WINDOW_SIZE_KEY] = fs.params[
            c.HALF_WINDOW_SIZE_KEY]
    
    new_experiment_dict[c.MIN_DETECTION_PCT_KEY] = c.MIN_DETECTION_PCT
    if c.MIN_DETECTION_PCT_KEY in fs.params:
        new_experiment_dict[c.MIN_DETECTION_PCT_KEY] = fs.params[
            c.MIN_DETECTION_PCT_KEY]
        
    new_experiment_dict[c.MIN_SEGMENT_DURATION_KEY] = c.MIN_SEGMENT_DURATION
    if c.MIN_SEGMENT_DURATION_KEY in fs.params:
        new_experiment_dict[c.MIN_SEGMENT_DURATION_KEY] = fs.params[
            c.MIN_SEGMENT_DURATION_KEY]
    
    new_experiment_dict[c.TRACKING_MIN_INT_AREA_KEY] = c.TRACKING_MIN_INT_AREA
    if c.TRACKING_MIN_INT_AREA_KEY in fs.params:
        new_experiment_dict[c.TRACKING_MIN_INT_AREA_KEY] = fs.params[
            c.TRACKING_MIN_INT_AREA_KEY]
        
    new_experiment_dict[c.STD_MULTIPLIER_FRAME_KEY] = c.STD_MULTIPLIER_FRAME
    if c.STD_MULTIPLIER_FRAME_KEY in fs.params:
        new_experiment_dict[c.STD_MULTIPLIER_FRAME_KEY] = fs.params[
            c.STD_MULTIPLIER_FRAME_KEY]
    
    new_experiment_dict[c.STD_MULTIPLIER_FACE_KEY] = c.STD_MULTIPLIER_FACE
    if c.STD_MULTIPLIER_FACE_KEY in fs.params:
        new_experiment_dict[c.STD_MULTIPLIER_FACE_KEY] = fs.params[
            c.STD_MULTIPLIER_FACE_KEY]
    
    new_experiment_dict[c.MAX_FR_WITH_MISSED_DET_KEY] = c.MAX_FR_WITH_MISSED_DET
    if c.MAX_FR_WITH_MISSED_DET_KEY in fs.params:
        new_experiment_dict[c.MAX_FR_WITH_MISSED_DET_KEY] = fs.params[
            c.MAX_FR_WITH_MISSED_DET_KEY]

    new_experiment_dict[c.USE_ALIGNED_FACE_IN_TRACKING_KEY] = c.USE_ALIGNED_FACE_IN_TRACKING
    if c.USE_ALIGNED_FACE_IN_TRACKING_KEY in fs.params:
        new_experiment_dict[c.USE_ALIGNED_FACE_IN_TRACKING_KEY] = fs.params[
            c.USE_ALIGNED_FACE_IN_TRACKING_KEY]
    
    new_experiment_dict[c.USE_AGGREGATION_KEY] = c.USE_AGGREGATION
    if c.USE_AGGREGATION_KEY in fs.params:
        new_experiment_dict[c.USE_AGGREGATION_KEY] = fs.params[
            c.USE_AGGREGATION_KEY]
    
    new_experiment_dict[c.USE_NOSE_POS_IN_DETECTION_KEY] = c.USE_NOSE_POS_IN_DETECTION
    if c.USE_NOSE_POS_IN_DETECTION_KEY in fs.params:
        new_experiment_dict[c.USE_NOSE_POS_IN_DETECTION_KEY] = fs.params[
            c.USE_NOSE_POS_IN_DETECTION_KEY]
    
    new_experiment_dict[c.USE_NOSE_POS_IN_RECOGNITION_KEY] = c.USE_NOSE_POS_IN_RECOGNITION
    if c.USE_NOSE_POS_IN_RECOGNITION_KEY in fs.params:
        new_experiment_dict[c.USE_NOSE_POS_IN_RECOGNITION_KEY] = fs.params[
            c.USE_NOSE_POS_IN_RECOGNITION_KEY]
    
    new_experiment_dict[c.MAX_NOSE_DIFF_KEY] = c.MAX_NOSE_DIFF
    if c.MAX_NOSE_DIFF_KEY in fs.params:
        new_experiment_dict[c.MAX_NOSE_DIFF_KEY] = fs.params[
            c.MAX_NOSE_DIFF_KEY]
    
    new_experiment_dict[ce.UPDATE_FACE_MODEL_AFTER_MERGING_KEY] = ce.UPDATE_FACE_MODEL_AFTER_MERGING
    if ce.UPDATE_FACE_MODEL_AFTER_MERGING_KEY in fs.params:
        new_experiment_dict[ce.UPDATE_FACE_MODEL_AFTER_MERGING_KEY] = fs.params[
            ce.UPDATE_FACE_MODEL_AFTER_MERGING_KEY]
    
    new_experiment_dict[c.USE_MAJORITY_RULE_KEY] = c.USE_MAJORITY_RULE
    if c.USE_MAJORITY_RULE_KEY in fs.params:
        new_experiment_dict[c.USE_MAJORITY_RULE_KEY] = fs.params[
            c.USE_MAJORITY_RULE_KEY]
    
    new_experiment_dict[c.USE_MEAN_CONFIDENCE_RULE_KEY] = c.USE_MEAN_CONFIDENCE_RULE
    if c.USE_MEAN_CONFIDENCE_RULE_KEY in fs.params:
        new_experiment_dict[c.USE_MEAN_CONFIDENCE_RULE_KEY] = fs.params[
            c.USE_MEAN_CONFIDENCE_RULE_KEY]
    
    new_experiment_dict[c.USE_MIN_CONFIDENCE_RULE_KEY] = c.USE_MIN_CONFIDENCE_RULE
    if c.USE_MIN_CONFIDENCE_RULE_KEY in fs.params:
        new_experiment_dict[c.USE_MIN_CONFIDENCE_RULE_KEY] = fs.params[
            c.USE_MIN_CONFIDENCE_RULE_KEY]
    
    new_experiment_dict[c.USE_CLOTHING_RECOGNITION_KEY] = c.USE_CLOTHING_RECOGNITION
    if c.USE_CLOTHING_RECOGNITION_KEY in fs.params:
        new_experiment_dict[c.USE_CLOTHING_RECOGNITION_KEY] = fs.params[
            c.USE_CLOTHING_RECOGNITION_KEY]

    new_experiment_dict[c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY] = c.ALL_CLOTH_BBOXES_IN_FRAMES
    if c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY in fs.params:
        new_experiment_dict[c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY] = fs.params[
            c.ALL_CLOTH_BBOXES_IN_FRAMES_KEY]
    
    new_experiment_dict[c.CLOTHES_BBOX_HEIGHT_KEY] = c.CLOTHES_BBOX_HEIGHT
    if c.CLOTHES_BBOX_HEIGHT_KEY in fs.params:
        new_experiment_dict[c.CLOTHES_BBOX_HEIGHT_KEY] = fs.params[
            c.CLOTHES_BBOX_HEIGHT_KEY]
    
    new_experiment_dict[c.CLOTHES_BBOX_WIDTH_KEY] = c.CLOTHES_BBOX_WIDTH
    if c.CLOTHES_BBOX_WIDTH_KEY in fs.params:
        new_experiment_dict[c.CLOTHES_BBOX_WIDTH_KEY] = fs.params[
            c.CLOTHES_BBOX_WIDTH_KEY]
    
    new_experiment_dict[c.CLOTHES_CHECK_METHOD_KEY] = c.CLOTHES_CHECK_METHOD
    if c.CLOTHES_CHECK_METHOD_KEY in fs.params:
        new_experiment_dict[c.CLOTHES_CHECK_METHOD_KEY] = fs.params[
            c.CLOTHES_CHECK_METHOD_KEY]

    new_experiment_dict[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY] = c.CLOTHING_REC_HSV_CHANNELS_NR
    if c.CLOTHING_REC_HSV_CHANNELS_NR_KEY in fs.params:
        new_experiment_dict[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY] = fs.params[
            c.CLOTHING_REC_HSV_CHANNELS_NR_KEY]
    
    new_experiment_dict[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = c.CLOTHING_REC_USE_DOMINANT_COLOR
    if c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY in fs.params:
        new_experiment_dict[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = fs.params[
            c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY]
    
    new_experiment_dict[c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY] = c.CLOTHING_REC_USE_MEAN_X_OF_FACES
    if c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY in fs.params:
        new_experiment_dict[c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY] = fs.params[
            c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]
    
    new_experiment_dict[c.CLOTHING_REC_USE_3_BBOXES_KEY] = c.CLOTHING_REC_USE_3_BBOXES
    if c.CLOTHING_REC_USE_3_BBOXES_KEY in fs.params:
        new_experiment_dict[c.CLOTHING_REC_USE_3_BBOXES_KEY] = fs.params[
            c.CLOTHING_REC_USE_3_BBOXES_KEY]
    
    new_experiment_dict[c.MIN_CLOTH_MODEL_SIZE_KEY] = c.MIN_CLOTH_MODEL_SIZE
    if c.MIN_CLOTH_MODEL_SIZE_KEY in fs.params:
        new_experiment_dict[c.MIN_CLOTH_MODEL_SIZE_KEY] = fs.params[
            c.MIN_CLOTH_MODEL_SIZE_KEY]

    new_experiment_dict[c.NECK_HEIGHT_KEY] = c.NECK_HEIGHT
    if c.NECK_HEIGHT_KEY in fs.params:
        new_experiment_dict[c.NECK_HEIGHT_KEY] = fs.params[c.NECK_HEIGHT_KEY] 
    
    new_experiment_dict[c.HIST_SMOOTHING_KERNEL_SIZE_KEY] = c.HIST_SMOOTHING_KERNEL_SIZE
    if c.HIST_SMOOTHING_KERNEL_SIZE_KEY in fs.params:
        new_experiment_dict[c.HIST_SMOOTHING_KERNEL_SIZE_KEY] = fs.params[
            c.HIST_SMOOTHING_KERNEL_SIZE_KEY]
    
    new_experiment_dict[c.CLOTHES_CONF_THRESH_KEY] = c.CLOTHES_CONF_THRESH
    if c.CLOTHES_CONF_THRESH_KEY in fs.params:
        new_experiment_dict[c.CLOTHES_CONF_THRESH_KEY] = fs.params[
            c.CLOTHES_CONF_THRESH_KEY]
        
    new_experiment_dict[c.VARIABLE_CLOTHING_THRESHOLD_KEY] = c.VARIABLE_CLOTHING_THRESHOLD
    if c.VARIABLE_CLOTHING_THRESHOLD_KEY in fs.params:
        new_experiment_dict[c.VARIABLE_CLOTHING_THRESHOLD_KEY] = fs.params[
            c.VARIABLE_CLOTHING_THRESHOLD_KEY]
    
    new_experiment_dict[c.USE_CAPTION_RECOGNITION_KEY] = c.USE_CAPTION_RECOGNITION
    if c.USE_CAPTION_RECOGNITION_KEY in fs.params:
        new_experiment_dict[c.USE_CAPTION_RECOGNITION_KEY] = fs.params[
            c.USE_CAPTION_RECOGNITION_KEY]

    new_experiment_dict[c.USE_FACE_RECOGNITION_KEY] = c.USE_FACE_RECOGNITION
    if c.USE_FACE_RECOGNITION_KEY in fs.params:
        new_experiment_dict[c.USE_FACE_RECOGNITION_KEY] = fs.params[
            c.USE_FACE_RECOGNITION_KEY]

    new_experiment_dict[c.GLOBAL_FACE_REC_THRESHOLD_KEY] = c.GLOBAL_FACE_REC_THRESHOLD
    if c.GLOBAL_FACE_REC_THRESHOLD_KEY in fs.params:
        new_experiment_dict[c.GLOBAL_FACE_REC_THRESHOLD_KEY] = fs.params[
            c.GLOBAL_FACE_REC_THRESHOLD_KEY]

    new_experiment_dict[c.LEV_RATIO_PCT_THRESH_KEY] = c.LEV_RATIO_PCT_THRESH
    if c.LEV_RATIO_PCT_THRESH_KEY in fs.params:
        new_experiment_dict[c.LEV_RATIO_PCT_THRESH_KEY] = fs.params[
            c.LEV_RATIO_PCT_THRESH_KEY]

    new_experiment_dict[c.MIN_TAG_LENGTH_KEY] = c.MIN_TAG_LENGTH
    if c.MIN_TAG_LENGTH_KEY in fs.params:
        new_experiment_dict[c.MIN_TAG_LENGTH_KEY] = fs.params[
            c.MIN_TAG_LENGTH_KEY]

    new_experiment_dict[c.USE_BLACKLIST_KEY] = c.USE_BLACKLIST
    if c.USE_BLACKLIST_KEY in fs.params:
        new_experiment_dict[c.USE_BLACKLIST_KEY] = fs.params[
            c.USE_BLACKLIST_KEY]

    new_experiment_dict[c.USE_LEVENSHTEIN_KEY] = c.USE_LEVENSHTEIN
    if c.USE_LEVENSHTEIN_KEY in fs.params:
        new_experiment_dict[c.USE_LEVENSHTEIN_KEY] = fs.params[
            c.USE_LEVENSHTEIN_KEY]

    # Analysis time
    
    frame_extr_time = 0
    if c.FRAME_EXTRACTION_TIME_KEY in fs.anal_times:
        frame_extr_time = fs.anal_times[c.FRAME_EXTRACTION_TIME_KEY]
    new_experiment_dict[c.FRAME_EXTRACTION_TIME_KEY] = frame_extr_time
        
    face_det_time = 0
    if c.FACE_DETECTION_TIME_KEY in fs.anal_times:
        face_det_time = fs.anal_times[c.FACE_DETECTION_TIME_KEY]
    new_experiment_dict[c.FACE_DETECTION_TIME_KEY] = face_det_time        
        
    shot_cut_det_time = 0
    if c.SHOT_CUT_DETECTION_TIME_KEY in fs.anal_times:
        shot_cut_det_time = fs.anal_times[c.SHOT_CUT_DETECTION_TIME_KEY]
    new_experiment_dict[c.SHOT_CUT_DETECTION_TIME_KEY] = shot_cut_det_time        
    
    face_tracking_time = 0
    if c.FACE_TRACKING_TIME_KEY in fs.anal_times:
        face_tracking_time = fs.anal_times[c.FACE_TRACKING_TIME_KEY]
    new_experiment_dict[c.FACE_TRACKING_TIME_KEY] = face_tracking_time        
        
    face_models_creation_time = 0
    if c.FACE_MODELS_CREATION_TIME_KEY in fs.anal_times:
        face_models_creation_time = fs.anal_times[
            c.FACE_MODELS_CREATION_TIME_KEY]
    new_experiment_dict[c.FACE_MODELS_CREATION_TIME_KEY] = face_models_creation_time    
    
    cloth_models_creation_time = 0
    if c.CLOTH_MODELS_CREATION_TIME_KEY in fs.anal_times:
        cloth_models_creation_time = fs.anal_times[
            c.CLOTH_MODELS_CREATION_TIME_KEY]
    new_experiment_dict[c.CLOTH_MODELS_CREATION_TIME_KEY] = cloth_models_creation_time
    
    people_clustering_time = 0
    if c.PEOPLE_CLUSTERING_TIME_KEY in fs.anal_times:
        people_clustering_time = fs.anal_times[
            c.PEOPLE_CLUSTERING_TIME_KEY]
    new_experiment_dict[c.PEOPLE_CLUSTERING_TIME_KEY] = people_clustering_time
    
    face_rec_time = 0
    if c.FACE_RECOGNITION_TIME_KEY in fs.anal_times:
        face_rec_time = fs.anal_times[c.FACE_RECOGNITION_TIME_KEY]
    new_experiment_dict[c.FACE_RECOGNITION_TIME_KEY] = face_rec_time         
    
    new_experiment_dict[c.SEGMENTS_NR_KEY] = fs.anal_results[c.SEGMENTS_NR_KEY]
    new_experiment_dict[c.PEOPLE_CLUSTERS_NR_KEY] = fs.anal_results[
        c.PEOPLE_CLUSTERS_NR_KEY]
    new_experiment_dict[c.RELEVANT_PEOPLE_NR_KEY] = fs.anal_results[
        c.RELEVANT_PEOPLE_NR_KEY]

    new_experiment_dict[ce.PRECISION_KEY] = tot_precision
    new_experiment_dict[ce.RECALL_KEY] = tot_recall
    new_experiment_dict[ce.F1_KEY] = tot_f1
    new_experiment_dict[ce.MEAN_PRECISION_KEY] = mean_precision
    new_experiment_dict[ce.STD_PRECISION_KEY] = std_precision
    new_experiment_dict[ce.MEAN_RECALL_KEY] = mean_recall
    new_experiment_dict[ce.STD_RECALL_KEY] = std_recall
    new_experiment_dict[ce.MEAN_F1_KEY] = mean_f1
    new_experiment_dict[ce.STD_F1_KEY] = std_f1

    new_experiment_dict[ce.CAPTION_PRECISION_KEY] = tot_cap_precision
    new_experiment_dict[ce.CAPTION_RECALL_KEY] = tot_cap_recall
    new_experiment_dict[ce.CAPTION_F1_KEY] = tot_cap_f1
    new_experiment_dict[ce.CAPTION_MEAN_PRECISION_KEY] = mean_cap_precision
    new_experiment_dict[ce.CAPTION_STD_PRECISION_KEY] = std_cap_precision
    new_experiment_dict[ce.CAPTION_MEAN_RECALL_KEY] = mean_cap_recall
    new_experiment_dict[ce.CAPTION_STD_RECALL_KEY] = std_cap_recall
    new_experiment_dict[ce.CAPTION_MEAN_F1_KEY] = mean_cap_f1
    new_experiment_dict[ce.CAPTION_STD_F1_KEY] = std_cap_f1

    new_experiment_dict[ce.SAVED_FRAMES_NR_KEY] = fs.saved_frames
      
    results_path = ce.VIDEO_INDEXING_RESULTS_PATH
    experiment_results_file_name = ce.VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME
    
    if params is not None:
        
        if ce.VIDEO_INDEXING_RESULTS_PATH_KEY in params:
            results_path = params[ce.VIDEO_INDEXING_RESULTS_PATH_KEY]
            
        if ce.VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME_KEY in params:
            experiment_results_file_name = params[
                ce.VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME_KEY]
    
    yaml_results_file_name = experiment_results_file_name + '.yml'
    
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
    save_YAML_file(all_results_YAML_file_path, experiments_dict)

    # Update csv file with results related to all the experiments
    csv_results_file_name = experiment_results_file_name + '.csv'
    all_results_CSV_file_path = os.path.join(
        results_path, csv_results_file_name)
    save_video_indexing_experiments_in_CSV_file(
        all_results_CSV_file_path, experiments)

    del fs


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Execute video indexing tests")
    parser.add_argument("-resource_path", help="resource path")
    parser.add_argument("-resource_id", help="resource id")
    parser.add_argument("-config", help="configuration file")
    parser.add_argument("--no_software_test",
                        help="do not execute software test",
                        action="store_true")

    args = parser.parse_args()

    no_software_test = args.no_software_test

    # Set resource path
    resource_path = None

    if args.resource_path:
        resource_path = args.resource_path
    else:
        if not no_software_test:
            print("Resource path not provided. "
                  "Only software test will be executed")
        else:
            print("Resource path not provided")
            exit()

    # Set resource id
    resource_id = None

    if args.resource_id:
        resource_id = args.resource_id
    else:
        if resource_path:
            # Use resource name as resource id
            resource_id = os.path.basename(resource_path)
            print("Resource id not provided. "
                  "Resource name will be used as resource id")

    # Set parameters
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
    else:
        print("Default configuration file will be used")

    execute_experiments = False
    if not no_software_test:
        print("\n ### EXECUTING SOFTWARE TEST ###\n")

        suite = unittest.TestLoader().loadTestsFromTestCase(
        TestFaceModels)
        test_result = unittest.TextTestRunner(verbosity=2).run(suite)

        if test_result.wasSuccessful():

            suite = unittest.TestLoader().loadTestsFromTestCase(
            TestVideoFaceExtractor)

            test_result = unittest.TextTestRunner(verbosity=2).run(suite)

            if test_result.wasSuccessful():
                execute_experiments = True
                print("\n ### EXECUTING EXPERIMENTS ###\n")
    else:
        execute_experiments = True

    if execute_experiments and resource_path and resource_id:
        video_indexing_experiments(resource_path, resource_id, params)
