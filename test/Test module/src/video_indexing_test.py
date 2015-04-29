import numpy
import os
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.face_extractor import FaceExtractor
from tools.Utils import * 

# Save in csv file given list of experiments
def save_video_indexing_experiments_in_CSV_file(file_path, experiments):
    
    stream = open(file_path, 'w')
    
    # Write csv header
    stream.write(CODE_VERSION_KEY + ',' +
                 EXPERIMENT_NUMBER_KEY + ',' + 
                 VIDEO_NAME_KEY + ',' + 
                 VIDEO_DURATION_KEY + ',' + 
                 VIDEO_FPS_KEY + ',' +
                 USED_FPS_KEY + ',' + 
                 EXPERIMENT_ALGORITHM_KEY + ',' +
                 LBP_RADIUS_KEY + ',' + 
                 LBP_NEIGHBORS_KEY + ',' +
                 LBP_GRID_X_KEY + ',' + 
                 LBP_GRID_Y_KEY + ',' +
                 CROPPED_FACE_HEIGHT_KEY + ',' +
                 CROPPED_FACE_WIDTH_KEY + ',' +
                 OFFSET_PCT_X_KEY + ',' + 
                 OFFSET_PCT_Y_KEY + ',' +
                 CONF_THRESHOLD_KEY + ',' + 
                 HALF_WINDOW_SIZE_KEY + ',' +
                 MIN_DETECTION_PCT_KEY + ',' + 
                 MIN_SEGMENT_DURATION_KEY + ',' +
                 TRACKING_MIN_INT_AREA_KEY + ',' + 
                 STD_MULTIPLIER_FRAME_KEY + ',' +
                 STD_MULTIPLIER_FACE_KEY + ',' + 
                 MAX_FR_WITH_MISSED_DET_KEY + ',' +
                 USE_AGGREGATION_KEY + ',' + 
                 USE_NOSE_POS_IN_DETECTION_KEY + ',' +
                 USE_NOSE_POS_IN_RECOGNITION_KEY + ',' + 
                 MAX_NOSE_DIFF_KEY + ',' +
                 UPDATE_FACE_MODEL_AFTER_MERGING_KEY + ',' + 
                 USE_MAJORITY_RULE_KEY + ',' + 
                 USE_MEAN_CONFIDENCE_RULE_KEY + ',' + 
                 USE_MIN_CONFIDENCE_RULE_KEY + ',' +
                 
                 USE_CLOTHING_RECOGNITION_KEY + ',' +
                 CLOTHES_BBOX_HEIGHT_KEY + ',' +
                 CLOTHES_BBOX_WIDTH_KEY + ',' +
                 CLOTHES_CHECK_METHOD_KEY + ',' +
                 CLOTHING_REC_USE_DOMINANT_COLOR_KEY + ',' +
                 CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY + ',' +
                 CLOTHING_REC_USE_3_BBOXES_KEY + ',' +
                 NECK_HEIGHT_KEY + ',' +
                 HIST_SMOOTHING_KERNEL_SIZE_KEY + ',' +
                 CLOTHES_CONF_THRESH_KEY + ',' +
                 VARIABLE_CLOTHING_THRESHOLD_KEY + ',' +
                                  
                 FRAME_EXTRACTION_TIME_KEY + ',' + 
                 FACE_DETECTION_TIME_KEY + ',' +
                 SHOT_CUT_DETECTION_TIME_KEY + ',' + 
                 FACE_TRACKING_TIME_KEY + ',' +
                 FACE_MODELS_CREATION_TIME_KEY + ',' + 
                 CLOTH_MODELS_CREATION_TIME_KEY + ',' +
                 PEOPLE_CLUSTERING_TIME_KEY + ',' +  
                 SEGMENTS_NR_KEY + ',' + 
                 PEOPLE_CLUSTERS_NR_KEY + ',' +
                 RELEVANT_PEOPLE_NR_KEY + ',' + 
                 PRECISION_KEY + ',' + 
                 RECALL_KEY + ',' + 
                 F1_KEY + ',' +
                 MEAN_PRECISION_KEY + ',' + 
                 STD_PRECISION_KEY + ',' +
                 MEAN_RECALL_KEY + ',' + 
                 STD_RECALL_KEY + ',' +
                 MEAN_F1_KEY + ',' + 
                 STD_F1_KEY + ',' +
                 SAVED_FRAMES_NR_KEY + '\n')
                 
    for experiment_dict_extended in experiments:
        
        experiment_dict = experiment_dict_extended[EXPERIMENT_KEY]
        
        stream.write(str(experiment_dict[CODE_VERSION_KEY]) + ',' +
                     str(experiment_dict[EXPERIMENT_NUMBER_KEY]) + ',' +
                     str(experiment_dict[VIDEO_NAME_KEY]) + ',' +  
                     str(experiment_dict[VIDEO_DURATION_KEY]) + ',' + 
                     str(experiment_dict[VIDEO_FPS_KEY]) + ',' +
                     str(experiment_dict[USED_FPS_KEY]) + ',' + 
                     str(experiment_dict[EXPERIMENT_ALGORITHM_KEY]) + ',' +
                     str(experiment_dict[LBP_RADIUS_KEY]) + ',' + 
                     str(experiment_dict[LBP_NEIGHBORS_KEY]) + ',' +
                     str(experiment_dict[LBP_GRID_X_KEY]) + ',' + 
                     str(experiment_dict[LBP_GRID_Y_KEY]) + ',' +
                     str(experiment_dict[CROPPED_FACE_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[CROPPED_FACE_WIDTH_KEY]) + ',' +
                     str(experiment_dict[OFFSET_PCT_X_KEY]) + ',' + 
                     str(experiment_dict[OFFSET_PCT_Y_KEY]) + ',' +
                     str(experiment_dict[CONF_THRESHOLD_KEY]) + ',' + 
                     str(experiment_dict[HALF_WINDOW_SIZE_KEY]) + ',' +
                     str(experiment_dict[MIN_DETECTION_PCT_KEY]) + ',' + 
                     str(experiment_dict[MIN_SEGMENT_DURATION_KEY]) + ',' +
                     str(experiment_dict[TRACKING_MIN_INT_AREA_KEY]) + ',' + 
                     str(experiment_dict[STD_MULTIPLIER_FRAME_KEY]) + ',' +
                     str(experiment_dict[STD_MULTIPLIER_FACE_KEY]) + ',' + 
                     str(experiment_dict[MAX_FR_WITH_MISSED_DET_KEY]) + ',' +
                     str(experiment_dict[USE_AGGREGATION_KEY]) + ',' + 
                     str(experiment_dict[USE_NOSE_POS_IN_DETECTION_KEY]) + ',' +
                     str(experiment_dict[USE_NOSE_POS_IN_RECOGNITION_KEY]) + ',' + 
                     str(experiment_dict[MAX_NOSE_DIFF_KEY]) + ',' +    
                     str(experiment_dict[UPDATE_FACE_MODEL_AFTER_MERGING_KEY]) + ',' +
                     str(experiment_dict[USE_MAJORITY_RULE_KEY]) + ',' +
                     str(experiment_dict[USE_MEAN_CONFIDENCE_RULE_KEY]) + ',' +
                     str(experiment_dict[USE_MIN_CONFIDENCE_RULE_KEY]) + ',' +
                     
                     str(experiment_dict[USE_CLOTHING_RECOGNITION_KEY]) + ',' +
                     str(experiment_dict[CLOTHES_BBOX_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[CLOTHES_BBOX_WIDTH_KEY]) + ',' +
                     str(experiment_dict[CLOTHES_CHECK_METHOD_KEY]) + ',' +
                     str(experiment_dict[CLOTHING_REC_USE_DOMINANT_COLOR_KEY]) + ',' +
                     str(experiment_dict[CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]) + ',' +
                     str(experiment_dict[CLOTHING_REC_USE_3_BBOXES_KEY]) + ',' +
                     str(experiment_dict[NECK_HEIGHT_KEY]) + ',' +
                     str(experiment_dict[HIST_SMOOTHING_KERNEL_SIZE_KEY]) + ',' +
                     str(experiment_dict[CLOTHES_CONF_THRESH_KEY]) + ',' +
                     str(experiment_dict[VARIABLE_CLOTHING_THRESHOLD_KEY]) + ',' +
                                        
                     str(experiment_dict[FRAME_EXTRACTION_TIME_KEY]) + ',' + 
                     str(experiment_dict[FACE_DETECTION_TIME_KEY]) + ',' +
                     str(experiment_dict[SHOT_CUT_DETECTION_TIME_KEY]) + ',' + 
                     str(experiment_dict[FACE_TRACKING_TIME_KEY]) + ',' +
                     str(experiment_dict[FACE_MODELS_CREATION_TIME_KEY]) + ',' + 
                     str(experiment_dict[CLOTH_MODELS_CREATION_TIME_KEY]) + ',' + 
                     str(experiment_dict[PEOPLE_CLUSTERING_TIME_KEY]) + ',' + 
                     str(experiment_dict[SEGMENTS_NR_KEY]) + ',' + 
                     str(experiment_dict[PEOPLE_CLUSTERS_NR_KEY]) + ',' +
                     str(experiment_dict[RELEVANT_PEOPLE_NR_KEY]) + ',' + 
                     str(experiment_dict[PRECISION_KEY]) + ',' + 
                     str(experiment_dict[RECALL_KEY]) + ',' + 
                     str(experiment_dict[F1_KEY]) + ',' +
                     str(experiment_dict[MEAN_PRECISION_KEY]) + ',' + 
                     str(experiment_dict[STD_PRECISION_KEY]) + ',' +
                     str(experiment_dict[MEAN_RECALL_KEY]) + ',' + 
                     str(experiment_dict[STD_RECALL_KEY]) + ',' +
                     str(experiment_dict[MEAN_F1_KEY]) + ',' + 
                     str(experiment_dict[STD_F1_KEY]) + ',' +
                     str(experiment_dict[SAVED_FRAMES_NR_KEY]) + '\n')
                     
    stream.close()

    
def video_indexing_experiments(resource_path, params):
    '''
    Execute video indexing experiments

    :type resource: string
    :param resource: file path of resource

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test 
    '''

    man_ann_path = ANNOTATIONS_PATH
    
    if(params is not None):
        
        man_ann_path = params[ANNOTATIONS_PATH_KEY]
    
    fs = FaceExtractor(params)
        
    fs.analizeVideo(resource_path)
    
    ## Get name of resource
    res_name = os.path.basename(resource_path) 
    
    ## Directory for this video  
    video_indexing_path = VIDEO_INDEXING_PATH
    
    if(params is not None):   
        
        video_indexing_path = params[VIDEO_INDEXING_PATH_KEY]
        
    video_path = os.path.join(video_indexing_path, res_name)
    
    ## Directory with simple annotations
    simple_ann_path = os.path.join(video_path, FACE_SIMPLE_ANNOTATION_DIR)
    
    # Get tags by analyzing folder with annotation files
    
    people_precision_dict = {}
    people_recall_dict = {}
    tags = []
    for ann_file in os.listdir(man_ann_path):
        
        tag = os.path.splitext(ann_file) [0]
        tags.append(tag)
        
        people_precision_dict[tag] = 0
        people_recall_dict[tag] = 0   
    
    
    ### Calculate recall ###
    
    video_tot_rec = 0
    video_tot_duration = 0
    
    # Iterate through manual annotations
    for ann_file in os.listdir(man_ann_path):
        
        ann_path = os.path.join(man_ann_path, ann_file)
        
        man_dict = load_YAML_file(ann_path)
        
        tot_duration = man_dict[TOT_SEGMENT_DURATION_KEY]
        
        video_tot_duration = video_tot_duration + tot_duration
        
        man_tag = man_dict[ANN_TAG_KEY]
        
        man_segments = man_dict[SEGMENTS_KEY]
        
        rec = 0.0 # Correctly recognized video (in milliseconds)
        
        auto_ann_file = os.path.join(simple_ann_path, ann_file)
            
        if(not(os.path.exists(auto_ann_file))):
            
            print(auto_ann_file)
            error_str = ('Warning! Automatic annotation for ' + 
            ann_file + ' does not exist')
             
            print error_str
            continue
        
        auto_dict = load_YAML_file(auto_ann_file)
        
        if((auto_dict is None) or (ANN_TAG_KEY not in auto_dict)):
            
            print 'Warning! Automatic annotation file does not exist!'
            
            break        
        
        auto_tag = auto_dict[ANN_TAG_KEY]
        
        if(man_tag != auto_tag):
            
            print 'Warning! Tags are different!'
            
            break
        
        for man_segment in man_segments:
            
            man_start = man_segment[SEGMENT_START_KEY]
            
            man_duration = man_segment[SEGMENT_DURATION_KEY]
            
            man_end = man_start + man_duration
            
            # Check if there is a segment in automatic annotations 
            # that corresponds to this segment 
                
            auto_segments = auto_dict[SEGMENTS_KEY]
            
            for auto_segment in auto_segments:
                
                auto_start = auto_segment[SEGMENT_START_KEY]
                
                auto_duration = auto_segment[SEGMENT_DURATION_KEY]
                
                auto_end = auto_start + auto_duration
                
                # Real segment is smaller than automatic segment
                if((man_start >= auto_start) and (man_end <= auto_end)):
                    
                    # Whole real segment is correctly recognized
                    rec = rec + man_duration
                
                # Real segment is bigger than automatic segment
                elif((man_start <= auto_start) and (man_end >= auto_end)):
                
                    # Whole automatic segment is correctly recognized
                    rec = rec + auto_duration
                
                # Real segment starts before automatic segment
                elif((man_start <= auto_start) and (man_end >= auto_start)):
                    
                    # Both automatic and real segments are 
                    # partially correctly recognized
                    rec = rec + (man_end - auto_start)
                
                # Real segment starts after automatic segment
                elif((man_start <= auto_end) and (man_end >= auto_end)):
                    
                    # Both automatic and real segments are 
                    # partially correctly recognized
                    rec = rec + (auto_end - man_start)   
        
        recall = rec / tot_duration     
                    
        people_recall_dict[man_tag] = rec / tot_duration
        
        video_tot_rec = video_tot_rec + rec
        
    tot_recall = video_tot_rec / video_tot_duration    
    
    ### Calculate precision ###
    
    video_tot_rec = 0
    video_tot_duration = 0
    
    # Iterate through automatic annotations
    for ann_file in os.listdir(simple_ann_path):
        
        ann_path = os.path.join(simple_ann_path, ann_file)
        
        auto_dict = load_YAML_file(ann_path)
        
        auto_tag = auto_dict[ANN_TAG_KEY]
        
        auto_segments = auto_dict[SEGMENTS_KEY]
        
        rec = 0.0 # Correctly recognized video (in milliseconds)
        
        man_ann_file = os.path.join(man_ann_path, ann_file)
            
        man_dict = load_YAML_file(man_ann_file)
        
        if((man_dict is None) or (ANN_TAG_KEY not in man_dict)):
            
            print 'Warning! Manual annotation file does not exist!'
            
            break
        
        man_tag = man_dict[ANN_TAG_KEY]
        
        if(man_tag != auto_tag):
            
            print 'Warning! Tags are different!'
            
            break
        
        for auto_segment in auto_segments:
            
            auto_start = auto_segment[SEGMENT_START_KEY]
            
            auto_duration = auto_segment[SEGMENT_DURATION_KEY]
            
            auto_end = auto_start + auto_duration
            
            # In manual annotation, we consider as start 
            # end as end previous second
            
            auto_start = math.ceil(auto_start / 1000.0) * 1000
            
            auto_end = math.floor(auto_end / 1000.0) * 1000
            
            auto_duration = auto_end - auto_start
            
            if(auto_duration < 0):
                
                print(auto_start)
                print(auto_end)
                print(auto_segment)
                print(auto_tag)
                
                print 'Warning! Duration is less than zero'
            
            # Check if there is a segment in manual annotations 
            # that corresponds to this segment 
                
            man_segments = man_dict[SEGMENTS_KEY]
            
            for man_segment in man_segments:
                
                man_start = man_segment[SEGMENT_START_KEY]
                
                man_duration = man_segment[SEGMENT_DURATION_KEY]
                
                man_end = man_start + man_duration  
                
                # Real segment is smaller than automatic segment
                if((man_start >= auto_start) and (man_end <= auto_end)):
                    
                    # Whole real segment is correctly recognized
                    rec = rec + man_duration
                
                # Real segment is bigger than automatic segment
                elif((man_start <= auto_start) and (man_end >= auto_end)):
                
                    # Whole automatic segment is correctly recognized
                    rec = rec + auto_duration
                
                # Real segment starts before automatic segment
                elif((man_start <= auto_start) and (man_end >= auto_start)):
                    
                    # Both automatic and real segments are 
                    # partially correctly recognized
                    rec = rec + (man_end - auto_start)
                
                # Real segment starts after automatic segment
                elif((man_start <= auto_end) and (man_end >= auto_end)):
                    
                    # Both automatic and real segments are 
                    # partially correctly recognized
                    rec = rec + (auto_end - man_start)
                    
        tot_duration = auto_dict[TOT_SEGMENT_DURATION_KEY]
        
        precision = 0
        
        if(tot_duration != 0):
        
            precision = rec / tot_duration      
                    
        people_precision_dict[auto_tag] = precision
        
        video_tot_rec = video_tot_rec + rec
        
        video_tot_duration = video_tot_duration + tot_duration
        
    tot_precision = 0
    
    if(video_tot_duration != 0):    
        
        tot_precision = video_tot_rec / video_tot_duration 
    
    tot_f1 = 0
    if((tot_precision != 0) and (tot_recall != 0)):
        tot_f1 = 2 * (tot_precision * tot_recall) / (tot_precision + tot_recall)
        
    # Calculate statistics for each person
    people_precision_list = []
    people_recall_list = []
    people_f1_list = []
    
    for tag in tags:
        
        person_precision = people_precision_dict[tag]
        people_precision_list.append(person_precision)
        
        person_recall = people_recall_dict[tag]
        people_recall_list.append(person_recall)
        
        #print('tag', tag)
        #print('precision', person_precision)
        #print('recall', person_recall)
    
        person_f1 = 0;
        if((person_precision != 0) and (person_recall != 0)):
            person_f1 = 2 * (person_precision * person_recall) / (person_precision + person_recall)
            
        people_f1_list.append(person_f1)   
        
    
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
    
    new_experiment_dict = {}

    new_experiment_dict[CODE_VERSION_KEY] = params[CODE_VERSION_KEY]
    
    new_experiment_dict[VIDEO_NAME_KEY] =  fs.resource_name
    
    duration = fs.video_frames / fs.fps
    
    new_experiment_dict[VIDEO_DURATION_KEY] = duration
    new_experiment_dict[VIDEO_FPS_KEY] = fs.fps
    new_experiment_dict[USED_FPS_KEY] = fs.params[USED_FPS_KEY]
    new_experiment_dict[EXPERIMENT_ALGORITHM_KEY] = fs.params[FACE_MODEL_ALGORITHM_KEY]
    new_experiment_dict[LBP_RADIUS_KEY] = fs.params[LBP_RADIUS_KEY]
    new_experiment_dict[LBP_NEIGHBORS_KEY] = fs.params[LBP_NEIGHBORS_KEY]
    new_experiment_dict[LBP_GRID_X_KEY] = fs.params[LBP_GRID_X_KEY] 
    new_experiment_dict[LBP_GRID_Y_KEY] = fs.params[LBP_GRID_Y_KEY]
    new_experiment_dict[CROPPED_FACE_HEIGHT_KEY] = fs.params[CROPPED_FACE_HEIGHT_KEY]
    new_experiment_dict[CROPPED_FACE_WIDTH_KEY] = fs.params[CROPPED_FACE_WIDTH_KEY]
    new_experiment_dict[OFFSET_PCT_X_KEY] = fs.params[OFFSET_PCT_X_KEY]
    new_experiment_dict[OFFSET_PCT_Y_KEY] = fs.params[OFFSET_PCT_Y_KEY]
    new_experiment_dict[CONF_THRESHOLD_KEY] = fs.params[CONF_THRESHOLD_KEY]
    new_experiment_dict[HALF_WINDOW_SIZE_KEY] = fs.params[HALF_WINDOW_SIZE_KEY]
    new_experiment_dict[MIN_DETECTION_PCT_KEY] = fs.params[MIN_DETECTION_PCT_KEY]
    new_experiment_dict[MIN_SEGMENT_DURATION_KEY] = fs.params[MIN_SEGMENT_DURATION_KEY]
    new_experiment_dict[TRACKING_MIN_INT_AREA_KEY] = fs.params[TRACKING_MIN_INT_AREA_KEY]
    new_experiment_dict[STD_MULTIPLIER_FRAME_KEY] = fs.params[STD_MULTIPLIER_FRAME_KEY]
    new_experiment_dict[STD_MULTIPLIER_FACE_KEY] = fs.params[STD_MULTIPLIER_FACE_KEY]
    new_experiment_dict[MAX_FR_WITH_MISSED_DET_KEY] = fs.params[MAX_FR_WITH_MISSED_DET_KEY]
    new_experiment_dict[USE_AGGREGATION_KEY] = fs.params[USE_AGGREGATION_KEY]
    new_experiment_dict[USE_NOSE_POS_IN_DETECTION_KEY] = fs.params[USE_NOSE_POS_IN_DETECTION_KEY]
    new_experiment_dict[USE_NOSE_POS_IN_RECOGNITION_KEY] = fs.params[USE_NOSE_POS_IN_RECOGNITION_KEY]
    new_experiment_dict[MAX_NOSE_DIFF_KEY] = fs.params[MAX_NOSE_DIFF_KEY]
    new_experiment_dict[UPDATE_FACE_MODEL_AFTER_MERGING_KEY] = fs.params[UPDATE_FACE_MODEL_AFTER_MERGING_KEY]
    new_experiment_dict[USE_MAJORITY_RULE_KEY] = fs.params[USE_MAJORITY_RULE_KEY]
    new_experiment_dict[USE_MEAN_CONFIDENCE_RULE_KEY] = fs.params[USE_MEAN_CONFIDENCE_RULE_KEY]
    new_experiment_dict[USE_MIN_CONFIDENCE_RULE_KEY] = fs.params[USE_MIN_CONFIDENCE_RULE_KEY] 
    
    new_experiment_dict[USE_CLOTHING_RECOGNITION_KEY] = fs.params[USE_CLOTHING_RECOGNITION_KEY]
    
    new_experiment_dict[CLOTHES_BBOX_HEIGHT_KEY] = CLOTHES_BBOX_HEIGHT
    if(CLOTHES_BBOX_HEIGHT_KEY in fs.params):
        new_experiment_dict[CLOTHES_BBOX_HEIGHT_KEY] = fs.params[CLOTHES_BBOX_HEIGHT_KEY]
    
    new_experiment_dict[CLOTHES_BBOX_WIDTH_KEY] = CLOTHES_BBOX_WIDTH
    if(CLOTHES_BBOX_WIDTH_KEY in fs.params):
        new_experiment_dict[CLOTHES_BBOX_WIDTH_KEY] = fs.params[CLOTHES_BBOX_WIDTH_KEY] 
    
    new_experiment_dict[CLOTHES_CHECK_METHOD_KEY] = CLOTHES_CHECK_METHOD
    if(CLOTHES_CHECK_METHOD_KEY in fs.params):
        new_experiment_dict[CLOTHES_CHECK_METHOD_KEY] = fs.params[CLOTHES_CHECK_METHOD_KEY] 
    
    new_experiment_dict[CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = CLOTHING_REC_USE_DOMINANT_COLOR
    if(CLOTHING_REC_USE_DOMINANT_COLOR_KEY in fs.params):
        new_experiment_dict[CLOTHING_REC_USE_DOMINANT_COLOR_KEY] = fs.params[CLOTHING_REC_USE_DOMINANT_COLOR_KEY] 
    
    new_experiment_dict[CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY] = CLOTHING_REC_USE_MEAN_X_OF_FACES
    if(CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY in fs.params):
        new_experiment_dict[CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY] = fs.params[CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY] 
    
    new_experiment_dict[CLOTHING_REC_USE_3_BBOXES_KEY] = CLOTHING_REC_USE_3_BBOXES
    if(CLOTHING_REC_USE_3_BBOXES_KEY in fs.params):
        new_experiment_dict[CLOTHING_REC_USE_3_BBOXES_KEY] = fs.params[CLOTHING_REC_USE_3_BBOXES_KEY]
    
    new_experiment_dict[NECK_HEIGHT_KEY] = NECK_HEIGHT
    if(NECK_HEIGHT_KEY in fs.params):
        new_experiment_dict[NECK_HEIGHT_KEY] = fs.params[NECK_HEIGHT_KEY] 
    
    new_experiment_dict[HIST_SMOOTHING_KERNEL_SIZE_KEY] = HIST_SMOOTHING_KERNEL_SIZE
    if(HIST_SMOOTHING_KERNEL_SIZE_KEY in fs.params):
        new_experiment_dict[HIST_SMOOTHING_KERNEL_SIZE_KEY] = fs.params[HIST_SMOOTHING_KERNEL_SIZE_KEY]    
    
    new_experiment_dict[CLOTHES_CONF_THRESH_KEY] = CLOTHES_CONF_THRESH
    if(CLOTHES_CONF_THRESH_KEY in fs.params):
        new_experiment_dict[CLOTHES_CONF_THRESH_KEY] = fs.params[CLOTHES_CONF_THRESH_KEY]
        
    new_experiment_dict[VARIABLE_CLOTHING_THRESHOLD_KEY] = False
    if(VARIABLE_CLOTHING_THRESHOLD_KEY in fs.params):
        new_experiment_dict[VARIABLE_CLOTHING_THRESHOLD_KEY] = fs.params[VARIABLE_CLOTHING_THRESHOLD_KEY]
    
    # Analysis time
    
    frame_extr_time = 0
    if(FRAME_EXTRACTION_TIME_KEY in fs.anal_times):
        frame_extr_time = fs.anal_times[FRAME_EXTRACTION_TIME_KEY]
    new_experiment_dict[FRAME_EXTRACTION_TIME_KEY] = frame_extr_time
        
    face_det_time = 0
    if(FACE_DETECTION_TIME_KEY in fs.anal_times):
        face_det_time = fs.anal_times[FACE_DETECTION_TIME_KEY]
    new_experiment_dict[FACE_DETECTION_TIME_KEY] = face_det_time        
        
    shot_cut_det_time = 0
    if(SHOT_CUT_DETECTION_TIME_KEY in fs.anal_times):
        shot_cut_det_time = fs.anal_times[SHOT_CUT_DETECTION_TIME_KEY]
    new_experiment_dict[SHOT_CUT_DETECTION_TIME_KEY] = shot_cut_det_time        
    
    face_tracking_time = 0
    if(FACE_TRACKING_TIME_KEY in fs.anal_times):
        face_tracking_time = fs.anal_times[FACE_TRACKING_TIME_KEY]
    new_experiment_dict[FACE_TRACKING_TIME_KEY] = face_tracking_time        
        
    face_models_creation_time = 0
    if(FACE_MODELS_CREATION_TIME_KEY in fs.anal_times):
        face_models_creation_time = fs.anal_times[FACE_MODELS_CREATION_TIME_KEY]
    new_experiment_dict[FACE_MODELS_CREATION_TIME_KEY] = face_models_creation_time    
    
    # TO BE DELETED
    #face_rec_time = 0
    #if(FACE_RECOGNITION_TIME_KEY in fs.anal_times):
        #face_rec_time = fs.anal_times[FACE_RECOGNITION_TIME_KEY]
    #new_experiment_dict[FACE_RECOGNITION_TIME_KEY] = face_rec_time 
    
    cloth_models_creation_time = 0
    if(CLOTH_MODELS_CREATION_TIME_KEY in fs.anal_times):
        cloth_models_creation_time = fs.anal_times[CLOTH_MODELS_CREATION_TIME_KEY]
    new_experiment_dict[CLOTH_MODELS_CREATION_TIME_KEY] = cloth_models_creation_time
    
    people_clustering_time = 0
    if(PEOPLE_CLUSTERING_TIME_KEY in fs.anal_times):
        people_clustering_time = fs.anal_times[PEOPLE_CLUSTERING_TIME_KEY]
    new_experiment_dict[PEOPLE_CLUSTERING_TIME_KEY] = people_clustering_time    
    
    new_experiment_dict[SEGMENTS_NR_KEY] = fs.anal_results[SEGMENTS_NR_KEY]
    new_experiment_dict[PEOPLE_CLUSTERS_NR_KEY] = fs.anal_results[PEOPLE_CLUSTERS_NR_KEY]
    new_experiment_dict[RELEVANT_PEOPLE_NR_KEY] = fs.anal_results[RELEVANT_PEOPLE_NR_KEY]
    new_experiment_dict[PRECISION_KEY] = tot_precision
    new_experiment_dict[RECALL_KEY] = tot_recall
    new_experiment_dict[F1_KEY] = tot_f1
    new_experiment_dict[MEAN_PRECISION_KEY] = mean_precision
    new_experiment_dict[STD_PRECISION_KEY] = std_precision
    new_experiment_dict[MEAN_RECALL_KEY] = mean_recall
    new_experiment_dict[STD_RECALL_KEY] = std_recall
    new_experiment_dict[MEAN_F1_KEY] = mean_f1
    new_experiment_dict[STD_F1_KEY] = std_f1
    new_experiment_dict[SAVED_FRAMES_NR_KEY] = fs.saved_frames
      
    results_path = VIDEO_INDEXING_RESULTS_PATH
    
    if(params is not None):
        
        results_path = params[VIDEO_INDEXING_RESULTS_PATH_KEY]
    
    yaml_results_file_name = VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME + '.yml'
    
    all_results_YAML_file_path = os.path.join(results_path, yaml_results_file_name)
    file_check = os.path.isfile(all_results_YAML_file_path)

    experiments = list()
    if(file_check):
        experiments = load_experiment_results(all_results_YAML_file_path)
        number_of_already_done_experiments = len(experiments)
        new_experiment_dict[EXPERIMENT_NUMBER_KEY] = number_of_already_done_experiments + 1
    else:
        new_experiment_dict[EXPERIMENT_NUMBER_KEY] = 1

    new_experiment_dict_extended = {}
    new_experiment_dict_extended[EXPERIMENT_KEY] = new_experiment_dict
    experiments.append(new_experiment_dict_extended)
    experiments_dict = {}
    experiments_dict[EXPERIMENTS_KEY] = experiments
    save_YAML_file(all_results_YAML_file_path, experiments_dict)

    # Update csv file with results related to all the experiments
    csv_results_file_name = VIDEO_INDEXING_EXPERIMENT_RESULTS_FILE_NAME + '.csv'
    all_results_CSV_file_path = os.path.join(results_path, csv_results_file_name) 
    save_video_indexing_experiments_in_CSV_file(all_results_CSV_file_path, experiments)
