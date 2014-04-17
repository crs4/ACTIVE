from os import listdir, path
import cv2
import numpy
from sympy import Polygon
import sys
sys.path.append("../../..");
from tools.Constants import *
from tools.face_extractor import FaceExtractor
from tools.FaceModelsLBP import FaceModelsLBP
from tools.Utils import load_experiment_results,load_image_annotations, load_YAML_file, save_YAML_file

# Save in csv file given list of experiments
def save_ext_experiments_in_CSV_file(file_path, experiments):
    stream = open(file_path, 'w');

    # Write csv header
    stream.write(EXPERIMENT_NUMBER_KEY + ',' + 
                 MEAN_PRECISION_KEY + ',' + STD_PRECISION_KEY + ',' +
                 MEAN_RECALL_KEY + ',' + STD_RECALL_KEY + ',' +
                 MEAN_F1_KEY + ',' + STD_F1_KEY + ',' +
                 MEAN_RECOGNITION_TIME_KEY + '\n');

    for experiment_dict_extended in experiments:
        experiment_dict = experiment_dict_extended[EXPERIMENT_KEY];
        stream.write(str(experiment_dict[EXPERIMENT_NUMBER_KEY]) + ',' +
                     str(experiment_dict[MEAN_PRECISION_KEY]) + ',' +
                     str(experiment_dict[STD_PRECISION_KEY]) + ',' +
                     str(experiment_dict[MEAN_RECALL_KEY]) + ',' +
                     str(experiment_dict[STD_RECALL_KEY]) + ',' +
                     str(experiment_dict[MEAN_F1_KEY]) + ',' +
                     str(experiment_dict[STD_F1_KEY]) + ',' +
                     str(experiment_dict[MEAN_RECOGNITION_TIME_KEY]) + '\n');
    stream.close();

def fe_test(params, show_results):
    ''' Execute face extraction test

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with detected and classified faces
    '''

    if(params == None):
        # Load default configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH);

    fe_test_params = params[FACE_EXTRACTION_KEY];
    image_path = fe_test_params[SOFTWARE_TEST_FILE_KEY];

    test_passed = True;

    try:

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE);
        image_width = len(image[0,:]);
        image_height = len(image[:,0]);
        polygon_image = Polygon((0,0), (image_width, 0), (image_width, image_height), (0, image_height));        

        fe = FaceExtractor(None);

        result = fe.extract_faces_from_image_sync(image_path);

        error = result[FACE_EXTRACTION_ERROR_KEY];

        if(len(error) == 0):

            faces = result[FACE_EXTRACTION_FACES_KEY];
            
            for face in faces:
                
                tag = face[FACE_EXTRACTION_TAG_KEY];
                # Check that tag is a not empty string
                if(len(tag) == 0):
                    test_passed = False;
                    break;

                # Check that bounding box rectangle is inside the original image
                face_bbox = face[FACE_EXTRACTION_BBOX_KEY];
                x = face_bbox[0];
                y = face_bbox[1];
                width = face_bbox[2];
                height = face_bbox[3];

                polygon_bbox = Polygon((x,y), (x+width,y), (x+width, y+height), (x, y+height));
                if(not(polygon_image.encloses(polygon_bbox))):
                    test_passed = False;
                    break;
            
        else:
            test_passed = False;
        
    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror);
        test_passed = False;
    except:
        print "Unexpected error:", sys.exc_info()[0];
        test_passed = False;
        raise;
        
    return test_passed;

def fe_experiments(params, show_results):
    '''
    Execute face detection experiments

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with detected faces
    '''
    
    if(params == None):
        # Load configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH);

    mean_ext_time = 0;
    
    fm = FaceModelsLBP();

    # Get path of directories with used files from params
    fe_test_params = params[FACE_EXTRACTION_KEY];
    frames_path = fe_test_params[TEST_FILES_PATH_KEY] + '\\'; # directory with test files
    annotations_path = fe_test_params[ANNOTATIONS_PATH_KEY] + '\\'; # directory with annotation files
    results_path = fe_test_params[RESULTS_PATH_KEY] + '\\'; # directory with results
    people_nr = fe_test_params[PEOPLE_NR_KEY];

    # Total number of images for each person
    person_images_nr = fe_test_params[PERSON_IMAGES_NR_KEY];

    # Number of images for each person to be used for the training
    training_images_nr = fe_test_params[TRAINING_IMAGES_NR_KEY];

    # Number of images for each person to be used for the test
    test_images_nr = person_images_nr - training_images_nr;

    ext_dict = {}; # Dictionary containing all results for this experiment
    images_list_for_YAML = []; # List used for creating YAML file with list of images
    people_list_for_YAML = []; # List used for creating YAML file with list of people

    # Initialize dictionaries with people
    people_true_positives_dict = {};
    people_false_positives_dict = {};
    people_test_images_nr_dict = {};
    for label in range(0, people_nr):
        tag = fm.get_label(label);
        people_true_positives_dict[tag] = 0;
        people_false_positives_dict[tag] = 0;
        people_test_images_nr_dict[tag] = 0;

    video_directories = listdir(frames_path);

    # Iterate over all directories with test frames
    global_frame_counter = 0;
    for video_dir in video_directories:
        video_dir_complete_path = frames_path + video_dir;

        # Load annotations for this video
        annotations_file = annotations_path + video_dir + '_annotations.yml';
    
        frames = load_image_annotations(annotations_file);

        # Iterate over all frames taken from this video
        frame_counter = 0;
        for frame_file in listdir(video_dir_complete_path):

            image_dict = {};

            ext_faces_list = [];

            annotations_dict = frames[frame_counter][ANNOTATIONS_FRAME_KEY];

            frame_name = annotations_dict[ANNOTATIONS_FRAME_NAME_KEY];

            # Check that frame name from file with annotations corresponds to file name
            if(frame_name != frame_file):
                print('Check failed');
                print('Frame file: ' + frame_file);
                print('Frame name from file with annotations: ' + frame_name);
                continue;

            # Set path of frame
            frame_path = video_dir_complete_path + '\\' + frame_file;

            # Extract faces from image
            fe = FaceExtractor(fm);
            ext_results = fe.extract_faces_from_image_sync(frame_path);

            # Add extraction time to total
            mean_ext_time = mean_ext_time + ext_results[FACE_EXTRACTION_ELAPSED_CPU_TIME_KEY];

            annotated_faces_nr_in_image = annotations_dict[ANNOTATIONS_FRAME_FACES_NR_KEY];
            annotated_faces = [];
            if(annotated_faces_nr_in_image > 0):
                annotated_faces = annotations_dict[ANNOTATIONS_FACES_KEY];

                # Update number of test images
                for annotated_face_dict_extended in annotated_faces:
                    annotated_face_dict = annotated_face_dict_extended[ANNOTATIONS_FACE_KEY];
                    ann_face_tag = annotated_face_dict[ANNOTATIONS_PERSON_NAME_KEY];
                    test_images_nr = people_test_images_nr_dict.get(ann_face_tag, 0);
                    people_test_images_nr_dict[ann_face_tag] = test_images_nr + 1;

            ext_faces = ext_results[FACE_EXTRACTION_FACES_KEY];

            # Iterate through detected faces
            for ext_face in ext_faces:

                detection_true_positive = False; #True if detected face is a real face
                recognition_true_positive = False; # True if assigned tag equals annotated tag

                ext_face_dict = {};
                
                ext_face_tag = ext_face[FACE_EXTRACTION_TAG_KEY];

                # Convert opencv rectangle in sympy polygon
                ext_face_rect = ext_face[FACE_EXTRACTION_BBOX_KEY];
                ext_face_rect_x = int(ext_face_rect[0]);
                ext_face_rect_y = int(ext_face_rect[1]);
                ext_face_rect_width = int(ext_face_rect[2]);
                ext_face_rect_height = int(ext_face_rect[3]);
                ext_face_rect_polygon = Polygon((ext_face_rect_x, ext_face_rect_y),
                                                (ext_face_rect_x+ext_face_rect_width, ext_face_rect_y),
                                                (ext_face_rect_x+ext_face_rect_width, ext_face_rect_y+ext_face_rect_height),
                                                (ext_face_rect_x, ext_face_rect_y+ext_face_rect_height));

                ext_face_dict[FACE_X_KEY] = ext_face_rect_x;
                ext_face_dict[FACE_Y_KEY] = ext_face_rect_y;
                ext_face_dict[FACE_WIDTH_KEY] = ext_face_rect_width;
                ext_face_dict[FACE_HEIGHT_KEY] = ext_face_rect_height;
                ext_face_dict[PERSON_ASSIGNED_TAG_KEY] = ext_face_tag;
                
                # Check if detected face contains one of the annotated face.
                # Width of detected face must not be more than 4 times width of correctly annotated face.
                for annotated_face_dict_extended in annotated_faces:
                    annotated_face_dict = annotated_face_dict_extended[ANNOTATIONS_FACE_KEY];

                    # Convert opencv rectangle in sympy polygon
                    ann_face_rect_x = annotated_face_dict[FACE_X_KEY];
                    ann_face_rect_y = annotated_face_dict[FACE_Y_KEY];
                    ann_face_rect_width = annotated_face_dict[FACE_WIDTH_KEY];
                    ann_face_rect_height = annotated_face_dict[FACE_HEIGHT_KEY];
                    ann_face_rect_polygon = Polygon((ann_face_rect_x, ann_face_rect_y),
                                                    (ann_face_rect_x+ann_face_rect_width, ann_face_rect_y),
                                                    (ann_face_rect_x+ann_face_rect_width, ann_face_rect_y+ ann_face_rect_height),
                                                    ((ann_face_rect_x, ann_face_rect_y+ ann_face_rect_height)));

                    if(ext_face_rect_polygon.encloses(ann_face_rect_polygon) and (ext_face_rect_width <= 4 * ann_face_rect_width)):

                        detection_true_positive = True;
                        ext_face_dict[FACE_CHECK_KEY] = 'Face detection - TP';
                        # Check tag
                        ann_face_tag = annotated_face_dict[ANNOTATIONS_PERSON_NAME_KEY];
                        if(ext_face_tag == ann_face_tag):s
                            recognition_true_positive = True;
                            ext_face_dict[PERSON_CHECK_KEY] = 'Face recognition - TP';
                            people_true_positives_dict[ext_face_tag] = people_true_positives_dict[ext_face_tag] + 1;
                        else:
                            ext_face_dict[PERSON_CHECK_KEY] = 'Face recognition - FP';
                            ext_face_dict[PERSON_ANNOTATED_TAG_KEY] = ann_face_tag;

                        # Each face must be considered once
                        annotated_faces.remove(annotated_face_dict_extended);
                        break;

                if(not(detection_true_positive)):
                    ext_face_dict[FACE_CHECK_KEY] = 'Face detection - FP';
                
                if(not(detection_true_positive) or not(recognition_true_positive)):
                    people_false_positives_dict[ext_face_tag] = people_false_positives_dict[ext_face_tag] + 1;

                ext_face_dict_extended = {};
                ext_face_dict_extended[FACE_EXTRACTION_FACE_KEY] = ext_face_dict;
                ext_faces_list.append(ext_face_dict_extended);

            image_dict_extended = {};
            image_dict[FACE_EXTRACTION_FACES_KEY] = ext_faces_list;
            image_dict_extended[FACE_EXTRACTION_IMAGE_KEY] = image_dict;
            images_list_for_YAML.append(image_dict_extended);

            frame_counter = frame_counter + 1;
            global_frame_counter = global_frame_counter + 1;

    # Calculate statistics for each person
    people_precision_list = [];
    people_recall_list = [];
    people_f1_list = [];
    for label in range(0, people_nr - 1):

        tag = fm.get_label(label);
        person_true_positives = people_true_positives_dict[tag];
        person_false_positives = people_false_positives_dict[tag];
        person_test_images_nr = people_test_images_nr_dict[tag];

        person_precision = 0;
        if(person_true_positives != 0):
            person_precision = float(person_true_positives) / float(person_true_positives + person_false_positives);
        people_precision_list.append(person_precision);

        person_recall = 0;
        if(person_test_images_nr != 0):
            person_recall = float(person_true_positives) / person_test_images_nr;
        people_recall_list.append(person_recall);

        person_f1 = 0;
        if((person_precision != 0) and (person_recall != 0)):
            person_f1 = 2 * (person_precision * person_recall) / (person_precision + person_recall);
        people_f1_list.append(person_f1);

        # Populate dictionary with results for this person
        person_dict = {};
        person_dict[PERSON_ANNOTATED_TAG_KEY] = tag;
        person_dict[PERSON_TRUE_POSITIVES_NR_KEY] = person_true_positives;
        person_dict[PERSON_FALSE_POSITIVES_NR_KEY] = person_false_positives;
        person_dict[PERSON_PRECISION_KEY] = person_precision;
        person_dict[PERSON_RECALL_KEY] = person_recall;
        person_dict[PERSON_F1_KEY] = person_f1;
        people_list_for_YAML.append(person_dict);

    mean_precision = float(numpy.mean(people_precision_list));
    std_precision = float(numpy.std(people_precision_list));

    mean_recall = float(numpy.mean(people_recall_list));
    std_recall = float(numpy.std(people_recall_list));

    mean_f1 = float(numpy.mean(people_f1_list));
    std_f1 = float(numpy.std(people_f1_list));

    mean_ext_time = mean_ext_time / global_frame_counter;

    print('Mean of precision: ' + str(mean_precision*100) + '%');
    print('Standard deviation of precision: ' + str(std_precision*100) + '%');
    print('Mean of recall: ' + str(mean_recall*100) + '%');
    print('Standard deviation of recall: ' + str(std_recall*100) + '%');
    print('Mean of f1: ' + str(mean_f1*100) + '%');
    print('Standard deviation of f1: ' + str(std_f1*100) + '%');
    print('Mean recognition time: ' + str(mean_ext_time) + ' s\n');

        # Update YAML file with results related to all the experiments
    number_of_already_done_experiments = 0;

    new_experiment_dict = {};

    new_experiment_dict[MEAN_PRECISION_KEY] = mean_precision;
    new_experiment_dict[STD_PRECISION_KEY] = std_precision;
    new_experiment_dict[MEAN_RECALL_KEY] = mean_recall;
    new_experiment_dict[STD_RECALL_KEY] = std_recall;
    new_experiment_dict[MEAN_F1_KEY] = mean_f1;
    new_experiment_dict[STD_F1_KEY] = std_f1;
    new_experiment_dict[MEAN_RECOGNITION_TIME_KEY] = mean_ext_time;

    ext_dict[GLOBAL_RESULTS_KEY] = new_experiment_dict;    
    ext_dict[IMAGES_KEY] = images_list_for_YAML;
    ext_dict[PEOPLE_KEY] = people_list_for_YAML;

    all_results_YAML_file_path = results_path + FACE_EXTRACTION_EXPERIMENT_RESULTS_FILE_NAME + '.yml';
    file_check = path.isfile(all_results_YAML_file_path);

    experiments = list();
    if(file_check):
        experiments = load_experiment_results(all_results_YAML_file_path);
        number_of_already_done_experiments = len(experiments);
        new_experiment_dict[EXPERIMENT_NUMBER_KEY] = number_of_already_done_experiments + 1;
    else:
        new_experiment_dict[EXPERIMENT_NUMBER_KEY] = 1;

    new_experiment_dict_extended = {};
    new_experiment_dict_extended[EXPERIMENT_KEY] = new_experiment_dict;
    experiments.append(new_experiment_dict_extended);
    experiments_dict = {};
    experiments_dict[EXPERIMENTS_KEY] = experiments;
    save_YAML_file(all_results_YAML_file_path, experiments_dict);

    # Update csv file with results related to all the experiments
    all_results_CSV_file_path = results_path + FACE_EXTRACTION_EXPERIMENT_RESULTS_FILE_NAME + '.csv';
    save_ext_experiments_in_CSV_file(all_results_CSV_file_path, experiments);

    # Save file with results related to this experiment
    results_file_path = results_path + 'FaceExtractionExperiment' + str(number_of_already_done_experiments + 1) + 'Results.yml';
    save_YAML_file(results_file_path, ext_dict);

if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(description = "Execute face extraction tests")
    parser.add_argument("-config", help = "configuration file");
    args = parser.parse_args()

    if(args.config):
        # Load given configuration file
        try:
            params = load_YAML_file(args.config);
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror));
            print("Default configuration file will be used");
        except:
            print("Unexpected error:", sys.exc_info()[0]);
            raise
        
    print("\n ### EXECUTING SOFTWARE TEST ###\n");

    params = None;

    test_passed = True; # TEST ONLY

    #TODO: UNCOMMENT
    test_passed = fe_test(params, False); 

    if(test_passed):
        print("\nSOFTWARE TEST PASSED\n");
        print("\n ### EXECUTING EXPERIMENTS ###\n");
        fe_experiments(params, False);
    else:
        print("\nSOFTWARE TEST FAILED\n");
