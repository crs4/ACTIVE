import numpy
import os
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.Constants import *
from tools.face_extractor import FaceExtractor
from tools.FaceModelsLBP import FaceModelsLBP
from tools.Utils import load_YAML_file, save_YAML_file

SIM_TRACKING = False

def aggregate_frame_results_in_sim_tracking(frames, fm):

    assigned_frames_nr_dict = {}
    confidence_lists_dict = {}
    people_nr = fm.get_people_nr();

    for label in range(0, people_nr):
        tag = fm.get_label(label);
        assigned_frames_nr_dict[tag] = 0
        confidence_lists_dict[tag] = []

    #print(frames)

    for frame in frames:

        faces = frame[FACE_EXTRACTION_FACES_KEY]

        if(len(faces) != 0):

            face = faces[0]

            assigned_tag = face[FACE_EXTRACTION_TAG_KEY]

            assigned_frames_nr_dict[assigned_tag] = assigned_frames_nr_dict[assigned_tag] + 1

            confidence = face[FACE_EXTRACTION_CONFIDENCE_KEY]

            confidence_lists_dict[assigned_tag].append(confidence)

    # Take final decision on person

    final_tag = 'Undefined'
    final_confidence = -1
    if(USE_MAJORITY_RULE):
        max_frames_nr = 0
        candidate_tags_list = []
        
        for label in range(0, people_nr):
            
            tag = fm.get_label(label);
            assigned_frames_nr = assigned_frames_nr_dict[tag]

            if(assigned_frames_nr > max_frames_nr):

                # There is one tag that has more occurrences that the others
                candidate_tags_list = []
                candidate_tags_list.append(tag)
                max_frames_nr = assigned_frames_nr

            elif(assigned_frames_nr == max_frames_nr):

                # There are two or more tags that have the same number of occurrences
                candidate_tags_list.append(tag)

        if (len(candidate_tags_list) >= 1):

            final_tag = candidate_tags_list[0]

            if(USE_MIN_CONFIDENCE_RULE):

                final_confidence = float(numpy.min(confidence_lists_dict[final_tag]));

                for i in range(1, len(candidate_tags_list)):

                    min_confidence = float(numpy.min(confidence_lists_dict[candidate_tags_list[i]]));

                    if (min_confidence < final_confidence):

                        final_tag = candidate_tags_list[i]

                        final_confidence = min_confidence

            elif(USE_MEAN_CONFIDENCE_RULE):

                #print('\nCONFIDENCE LIST\n')
                #print(confidence_lists_dict[final_tag])

                final_confidence = float(numpy.mean(confidence_lists_dict[final_tag]));
                #print(candidate_tags_list)

                for i in range(1, len(candidate_tags_list)):

                    mean_confidence = float(numpy.mean(confidence_lists_dict[candidate_tags_list[i]]));

                    if (mean_confidence < final_confidence):

                        final_tag = candidate_tags_list[i]

                        final_confidence = mean_confidence

    else:
        if(USE_MIN_CONFIDENCE_RULE):

            if(people_nr > 0):

                final_tag = fm.get_label(0)

                if(len(confidence_lists_dict[final_tag]) > 0):

                    final_confidence = float(numpy.min(confidence_lists_dict[final_tag]));

                for label in range(1, people_nr):
                
                    tag = fm.get_label(label);

                    if(len(confidence_lists_dict[tag]) > 0):

                        min_confidence = float(numpy.min(confidence_lists_dict[tag]));

                        if ((final_confidence == -1) or (min_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = min_confidence

        elif(USE_MEAN_CONFIDENCE_RULE):

            if(people_nr > 0):

                final_tag = fm.get_label(0)

                if(len(confidence_lists_dict[final_tag]) > 0):

                    final_confidence = float(numpy.mean(confidence_lists_dict[final_tag]));

                for label in range(1, people_nr):
                
                    tag = fm.get_label(label);

                    if(len(confidence_lists_dict[tag]) > 0):

                        mean_confidence = float(numpy.mean(confidence_lists_dict[tag]));

                        if ((final_confidence == -1) or (mean_confidence < final_confidence)):

                            final_tag = tag

                            final_confidence = mean_confidence
            
        else:
            print('Warning! Method is not available')
                        
    return [final_tag, final_confidence]

def fr_video_experiments(params, show_results):
    '''
    Execute face recognition experiments on video files

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with detected faces
    '''  
      
    if(params == None):
        # Load configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH);
    
    tot_rec_frames_nr = 0; # Number of correctly recognized frames
    tot_test_frames_nr = 0; # Number of total test frames
    mean_rec_time = 0; # Mean recognition time for videos

    true_pos_confidence_list = []; # List of confidence values for true positives
    false_pos_confidence_list = []; # List of confidence values for false positives
    tested_people_tag_list = []; # List of tags of people that appear in test set

    fm = FaceModelsLBP();

    fr_test_params = params[FACE_RECOGNITION_KEY];
    
    results_path = fr_test_params[RESULTS_PATH_KEY] + '\\'; # directory with results

    # Number of people
    people_nr = fm.get_people_nr();

    # Initialize dictionaries with people
    people_true_positives_dict = {};
    people_false_positives_dict = {};
    people_test_frames_nr_dict = {};
    
    for label in range(0, people_nr):
        tag = fm.get_label(label);
        people_true_positives_dict[tag] = 0;
        people_false_positives_dict[tag] = 0;
        people_test_frames_nr_dict[tag] = 0;

    test_set_path = fr_test_params[TEST_SET_PATH_KEY] + '\\';

    # Iterate over all videos
    video_counter = 0

    delta_x_maxs = []
    delta_y_maxs = []
    delta_w_maxs = []
    
    for video in os.listdir(test_set_path):
        
        # Dictionary for YAML file with results
        experiment_dict = {}
        experiment_dict_frames = []

        video_delta_xs = []
        video_delta_ys = []
        video_delta_ws = []

        ann_face_tag, file_ext = os.path.splitext(video);

        print('Annotated face tag: ', ann_face_tag)

        tested_people_tag_list.append(ann_face_tag)

        video_complete_path = test_set_path + video

        print(video_complete_path)

        try:

            fe = FaceExtractor(fm);

            handle = fe.extractFacesFromVideo(video_complete_path)

            results = fe.getResults(handle)

            error = results[FACE_EXTRACTION_ERROR_KEY]

            if(error):

                print('Warning')
                print(error)

            else:

                video_test_frames_nr = results[FACE_EXTRACTION_TOT_FRAMES_NR]

                tot_test_frames_nr = tot_test_frames_nr + video_test_frames_nr

                people_test_frames_nr_dict[ann_face_tag] = video_test_frames_nr
                
                mean_rec_time = mean_rec_time + results[FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY]

                if(USE_TRACKING):

                    segments = results[FACE_EXTRACTION_SEGMENTS_KEY]

                    #print(results)

                    tot_segments_frames_nr = 0

                    true_positives_in_segment = 0

                    for segment in segments:

                        segment_frames = segment[FACE_EXTRACTION_FRAMES_KEY]

                        frames_nr = segment[FACE_EXTRACTION_SEGMENT_TOT_FRAMES_NR_KEY]

                        assigned_tag = segment[FACE_EXTRACTION_TAG_KEY]

                        print('assigned_tag = ' + assigned_tag)

                        final_confidence = segment[FACE_EXTRACTION_CONFIDENCE_KEY]

                        tot_segments_frames_nr = tot_segments_frames_nr + frames_nr

                        if(assigned_tag == ann_face_tag):

                            people_true_positives_dict[assigned_tag] = people_true_positives_dict[assigned_tag] + frames_nr
                            true_positives_in_segment = true_positives_in_segment + frames_nr
                            tot_rec_frames_nr = tot_rec_frames_nr + frames_nr
                            true_pos_confidence_list.append(final_confidence)

                        else:

                            if(assigned_tag != 'Undefined'):

                                people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + frames_nr
                                false_pos_confidence_list.append(final_confidence)

                            else:

                                if(assigned_tag != 'Undefined'):

                                    people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + 1
                                    false_pos_confidence_list.appende(confidence)

                    # Tot number of frames in segments cannot be more than number of frames in video
                    if(true_positives_in_segment > video_test_frames_nr):
                        print('### WARNING! ###')
                        print 'true_positives_in_segment = ' + str(true_positives_in_segment)
                        print 'video_test_frames_nr = ' +  str(video_test_frames_nr)
                        people_false_positives_dict[ann_face_tag] = people_false_positives_dict[ann_face_tag] + (tot_segments_frames_nr - video_test_frames_nr)
                        tot_rec_frames_nr = tot_rec_frames_nr - (tot_segments_frames_nr - video_test_frames_nr)

                elif(SIM_TRACKING):

                    # Simulate tracking (every frame of this video contains the same person)

                    frames = results[FACE_EXTRACTION_FRAMES_KEY]

                    [assigned_tag, final_confidence] = aggregate_frame_results_in_sim_tracking(frames, fm)

                    print('assigned_tag = ' + assigned_tag)

                    if(assigned_tag == ann_face_tag):

                        people_true_positives_dict[assigned_tag] = people_true_positives_dict[assigned_tag] + len(frames)
                        tot_rec_frames_nr = tot_rec_frames_nr + len(frames)
                        true_pos_confidence_list.append(final_confidence)

                    else:

                        if(assigned_tag != 'Undefined'):

                            people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + len(frames)
                            false_pos_confidence_list.append(final_confidence)

                        else:

                            if(assigned_tag != 'Undefined'):

                                people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + 1
                                false_pos_confidence_list.appende(confidence)

                else:

                    frames = results[FACE_EXTRACTION_FRAMES_KEY]

                    frame_counter = 0
                    prev_frame_counter = -1
                    for frame in frames:

                        assigned_tag = 'Undefined';
                        confidence = -1;

                        faces = frame[FACE_EXTRACTION_FACES_KEY]
                        
                        time_stamp = frame[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY]
                        
                        experiment_dict_frame = {}
                        
                        experiment_dict_frame[FACE_EXTRACTION_ELAPSED_VIDEO_TIME_KEY] = time_stamp

                        if(len(faces) != 0):

                            face = faces[0]

                            assigned_tag = face[FACE_EXTRACTION_TAG_KEY]
                            
                            experiment_dict_faces = []
                            
                            experiment_dict_face = {}
                            
                            experiment_dict_face[FACE_EXTRACTION_TAG_KEY] = assigned_tag
                            
                            experiment_dict_faces.append(experiment_dict_face)
                            
                            if(len(faces) > 1):
                                
                                for face_counter in range(1, len(faces)):
                                    
                                    other_face = faces [face_counter]
                                    
                                    other_face_assigned_tag = other_face[FACE_EXTRACTION_TAG_KEY]
                                    
                                    experiment_dict_face = {}
                                    
                                    experiment_dict_face[FACE_EXTRACTION_TAG_KEY] = other_face_assigned_tag
                                    
                                    experiment_dict_faces.append(experiment_dict_face)

                            confidence = face[FACE_EXTRACTION_CONFIDENCE_KEY]

                            bbox = face[FACE_EXTRACTION_BBOX_KEY]

                            if((frame_counter > 0) and (frame_counter <= (prev_frame_counter + MAX_FRAMES_WITH_MISSED_DETECTION + 1))):

                                bbox_x = bbox[0]
                                bbox_y = bbox[1]
                                bbox_w = bbox[2]
                                
                                prev_bbox_x = prev_bbox[0]
                                prev_bbox_y = prev_bbox[1]
                                prev_bbox_w = prev_bbox[2]

                                delta_x = abs(bbox_x - prev_bbox_x)/float(prev_bbox_w)
                                delta_y = abs(bbox_x - prev_bbox_x)/float(prev_bbox_w)
                                delta_w = abs(bbox_w - prev_bbox_w)/float(prev_bbox_w)

                                video_delta_xs.append(delta_x)
                                video_delta_ys.append(delta_y)
                                video_delta_ws.append(delta_w)

                                if((delta_x > MAX_DELTA_PCT_X) or (delta_y > MAX_DELTA_PCT_Y) and (delta_w > MAX_DELTA_PCT_W)):

                                    print('delta_x: ', delta_x)
                                    print('delta_y: ', delta_y)
                                    print('delta_w: ', delta_w)

                            prev_frame_counter = frame_counter

                            prev_bbox = bbox
                            
                            experiment_dict_frame[FACE_EXTRACTION_FACES_KEY] = experiment_dict_faces
                            
                        else:
                            
                            experiment_dict_frame[FACE_EXTRACTION_FACES_KEY] = "No face detected"
                            
                        experiment_dict_frames.append(experiment_dict_frame)

                        if(assigned_tag == ann_face_tag):

                            people_true_positives_dict[assigned_tag] = people_true_positives_dict[assigned_tag] + 1
                            tot_rec_frames_nr = tot_rec_frames_nr + 1
                            true_pos_confidence_list.append(confidence)

                        else:

                            if(assigned_tag != 'Undefined'):

                                people_false_positives_dict[assigned_tag] = people_false_positives_dict[assigned_tag] + 1
                                false_pos_confidence_list.append(confidence)

                        frame_counter = frame_counter + 1
                    
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        if(not(USE_TRACKING) and not(SIM_TRACKING)):

            video_max_x = max(video_delta_xs)
            video_max_y = max(video_delta_ys)
            video_max_w = max(video_delta_ws)

            delta_x_maxs.append(video_max_x)
            delta_y_maxs.append(video_max_y)
            delta_w_maxs.append(video_max_w)

        video_counter = video_counter + 1
        
        experiment_dict[FACE_EXTRACTION_FRAMES_KEY] = experiment_dict_frames
        
        save_YAML_file(results_path + ann_face_tag + ".yml", experiment_dict)

    # Calculate statistics for each person
    people_precision_list = [];
    people_recall_list = [];
    people_f1_list = [];

    print('\nTRUE POSITIVES\n')
    print(people_true_positives_dict)
    print('\nFALSE POSITIVES\n')
    print(people_false_positives_dict)
    print('\nTEST FRAMES NR\n')
    print(people_test_frames_nr_dict)    
    
    for label in range(0, people_nr):

        tag = fm.get_label(label);

        if tag in tested_people_tag_list:

            person_true_positives = people_true_positives_dict[tag]
            person_false_positives = people_false_positives_dict[tag]
            person_test_frames_nr = people_test_frames_nr_dict[tag]

            person_precision = 0;
            if(person_true_positives != 0):
                person_precision = float(person_true_positives) / float(person_true_positives + person_false_positives);
            people_precision_list.append(person_precision);
        
            person_recall = 0;
            if(person_test_frames_nr != 0):
                person_recall = float(person_true_positives) / person_test_frames_nr;
            people_recall_list.append(person_recall);

            person_f1 = 0;
            if((person_precision != 0) and (person_recall != 0)):
                person_f1 = 2 * (person_precision * person_recall) / (person_precision + person_recall);
            people_f1_list.append(person_f1);

    mean_precision = float(numpy.mean(people_precision_list));
    std_precision = float(numpy.std(people_precision_list));

    mean_recall = float(numpy.mean(people_recall_list));
    std_recall = float(numpy.std(people_recall_list));

    mean_f1 = float(numpy.mean(people_f1_list));
    std_f1 = float(numpy.std(people_f1_list));

    recognition_rate = float(tot_rec_frames_nr) / float(tot_test_frames_nr);

    mean_rec_time = mean_rec_time / video_counter;

    mean_true_pos_confidence = float(numpy.mean(true_pos_confidence_list));
    std_true_pos_confidence = float(numpy.std(true_pos_confidence_list));

    mean_false_pos_confidence = float(numpy.mean(false_pos_confidence_list));
    std_false_pos_confidence = float(numpy.std(false_pos_confidence_list));

    print("\n ### RESULTS ###\n");

    print("USE_MAJORITY_RULE = " + str(USE_MAJORITY_RULE))
    print("USE_MIN_CONFIDENCE_RULE = " + str(USE_MIN_CONFIDENCE_RULE))
    print("USE_MEAN_CONFIDENCE_RULE = " + str(USE_MEAN_CONFIDENCE_RULE))

##    print('\nRecognition rate: ' + str(recognition_rate*100) + '%');
##    print('Mean of precision: ' + str(mean_precision*100) + '%');
##    print('Standard deviation of precision: ' + str(std_precision*100) + '%');
##    print('Mean of recall: ' + str(mean_recall*100) + '%');
##    print('Standard deviation of recall: ' + str(std_recall*100) + '%');
##    print('Mean of f1: ' + str(mean_f1*100) + '%');
##    print('Standard deviation of f1: ' + str(std_f1*100) + '%');
##    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n');

    print('Recognition rate: ' + str(recognition_rate));
    print('Mean of precision: ' + str(mean_precision));
    print('Standard deviation of precision: ' + str(std_precision));
    print('Mean of recall: ' + str(mean_recall));
    print('Standard deviation of recall: ' + str(std_recall));
    print('Mean of f1: ' + str(mean_f1));
    print('Standard deviation of f1: ' + str(std_f1));
    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n');
    
    print('Mean of confidence for true positives: ' + str(mean_true_pos_confidence));
    print('Standard deviation of confidence for true positives: ' + str(std_true_pos_confidence));
    print('Mean of confidence for false positives: ' + str(mean_false_pos_confidence));
    print('Standard deviation of confidence for false positives: ' + str(std_false_pos_confidence));

    if(not(USE_TRACKING) and not(SIM_TRACKING)):
        print('Maximums for delta x: ')
        print(delta_x_maxs)
        print('Maximums for delta y: ')
        print(delta_y_maxs)
        print('Maximums for delta w: ')
        print(delta_w_maxs)
    
if __name__ == "__main__":

    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description = "Execute face recognition tests")
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

    fr_video_experiments(params, False)

