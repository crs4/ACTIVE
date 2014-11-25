import cv2
import numpy as np
import sys
sys.path.append("../../..")
from tools.Constants import *
from tools.face_extractor import FaceExtractor
from tools.FaceModelsLBP import FaceModelsLBP
from tools.Utils import load_YAML_file, save_YAML_file

def save_results_in_csv_file(file_path, people_and_images_list):
    '''
    Save results in csv file
    
    :type file_path: string
    :param file_path: path of csv file
    
    :type people_and_images_list: list
    :param people_and_images_list: results for each tested image
    '''
    
    with open(file_path, 'w') as stream:
        
        # Write csv header
        stream.write('Image path,' + 
                     'Annotated tag,' +
                     'Predicted tag,' + 
                     'Confidence' + '\n')
                     
        for person_dict in people_and_images_list:
            
            ann_tag = person_dict[ANN_TAG_KEY]
        
            images_list = person_dict[IMAGES_KEY]
            
            for im_dict in images_list:
                
                im_path = im_dict[IMAGE_PATH_KEY]
                
                ass_tag = im_dict[ASSIGNED_TAG_KEY]
        
                conf = im_dict[CONFIDENCE_KEY]
                
                if(conf != -1):
                    
                    stream.write(im_path + ',' +
                                 ann_tag + ',' +
                                 ass_tag + ',' +
                                 str(conf) + '\n')
                else:
                    
                    stream.write(im_path + ',' +
                                 ann_tag + ',' +
                                 ass_tag + ',,\n')

def test_on_image(im_path, ann_tag, fm):
    '''
    Test on single image
    
    :type im_path: string
    :param im_path: path of image
    
    :type ann_tag: string
    :param ann_tag: annotated person tag in image
    
    :type fm: FaceModelsLBP
    :param fm: fame model
    '''
    
    ass_tag = NO_FACE_STRING
    
    conf = -1
    
    fe = FaceExtractor(fm)
    
    handle = fe.extractFacesFromImage(im_path)
    
    results = fe.getResults(handle)
    
    faces = results[FACES_KEY]
    
    im_dict = {}
    im_dict[IMAGE_PATH_KEY] = im_path
    im_dict[ASSIGNED_TAG_KEY] = NO_FACE_STRING
    im_dict[FACES_KEY] = NO_FACE_STRING
    
    im_dict[ELAPSED_CPU_TIME_KEY] = results[ELAPSED_CPU_TIME_KEY]
    
    if(len(faces) != 0):
        
        face = faces[0]
        
        ass_tag = face[ASSIGNED_TAG_KEY]
        
        conf = face[CONFIDENCE_KEY]
    
        im_dict[ASSIGNED_TAG_KEY] = ass_tag
        
        im_dict[CONFIDENCE_KEY] = conf
        
        im_dict_faces = []
        
        im_dict_face = {}
        
        im_dict_face[ASSIGNED_TAG_KEY] = ass_tag
        
        im_dict_faces.append(im_dict_face)
        
        if(len(faces) > 1):
            
            for counter in range(1, len(faces)):
                
                other_face = faces[counter]
                other_face_ass_tag = other_face[ASSIGNED_TAG_KEY]
                im_dict_face[ASSIGNED_TAG_KEY] = other_face_ass_tag
                im_dict_faces.append(im_dict_face)
                
        im_dict[FACES_KEY] = im_dict_faces   
    
    print 'Assigned person tag:', ass_tag
    
    return im_dict
    
def calculate_stats(tags, rec_im_nr, test_im_nr, tp_dict, fp_dict, 
                    tp_conf_list, fp_conf_list, test_im_nr_dict,
                    tot_rec_time, results_path):
    '''
    Calculate statistics for this experiment
    
    :type tags: list
    :param tags: tags contained in face model
    
    :type rec_im_nr: int
    :param rec_im_nr: number of correctly recognized images
    
    :type test_im_nr: int
    :param test_im_nr: number of total test images
    
    :type tp_dict: dictionary
    :param tp_dict: true positives for each person
    
    :type fp_dict: dictionary
    :param fp_dict: false positives for each person
    
    :type tp_conf_list: list
    :param tp_conf_list: list of confidences for true positives
    
    :type fp_conf_list: list
    :param fp_conf_list: list of confidences for false positives
    
    :type test_im_nr_dict: dictionary
    :param test_im_nr_dict: number of test images for each person
    
    :type tot_rec_time: float
    :param tot_rec_time: total recognition time
    
    :type results_path: string
    :param results_path: path of directory that will contain results    
    '''
    
    # Calculate statistics for each person
    
    prec_list = []
    rec_list = []
    f1_list = []
    
    # List used for creating YAML file with list of people
    people_list = []
    
    print('tp_dict', tp_dict)
    print('fp_dict', fp_dict)
    
    for tag in tags:
        
        tp = tp_dict[tag]
        fp = fp_dict[tag]
        im_nr = test_im_nr_dict[tag]
        
        prec = 0
        if(tp != 0):
            prec = float(tp) / float(tp + fp)
        prec_list.append(prec)
        
        rec = 0
        if(im_nr != 0):
            rec = float(tp) / im_nr
        rec_list.append(rec)
        
        f1 = 0
        if((prec != 0) and (rec != 0)):
            f1 = 2 * (prec * rec) / (prec + rec)
        f1_list.append(f1)
        
        # Populate dictionary with results for this person
        person_dict = {}
        person_dict[ANN_TAG_KEY] = tag
        person_dict[TRUE_POSITIVES_NR_KEY] = tp
        person_dict[FALSE_POSITIVES_NR_KEY] = fp
        person_dict[TEST_IMAGES_NR_KEY] = im_nr
        person_dict[PRECISION_KEY] = prec
        person_dict[RECALL_KEY] = rec
        person_dict[F1_KEY] = f1
        people_list.append(person_dict)
        
    # Complete path of file with people results
    people_results_path = os.path.join(results_path, 'Results.yml')    
        
    save_YAML_file(people_results_path, people_list)
        
    # Calculate global statistics   
        
    rec_rate = float(rec_im_nr) / float(test_im_nr)    
        
    mean_prec = float(np.mean(prec_list))
    std_prec = float(np.std(prec_list))
    
    mean_rec = float(np.mean(rec_list))
    std_rec = float(np.std(rec_list))
    
    mean_f1 = float(np.mean(f1_list))
    std_f1 = float(np.std(f1_list))
    
    if(len(tp_conf_list) > 0):
        mean_tp_conf = float(np.mean(tp_conf_list))
        std_tp_conf = float(np.std(tp_conf_list))
    
    if(len(fp_conf_list) > 0):
        mean_fp_conf = float(np.mean(fp_conf_list))
        std_fp_conf = float(np.std(fp_conf_list))
    
    mean_rec_time = tot_rec_time / test_im_nr
    
    print('Recognition rate: ' + str(rec_rate))
    print('Mean of precision: ' + str(mean_prec))
    print('Standard deviation of precision: ' + str(std_prec))
    print('Mean of recall: ' + str(mean_rec))
    print('Standard deviation of recall: ' + str(std_rec))
    print('Mean of f1: ' + str(mean_f1))
    print('Standard deviation of f1: ' + str(std_f1))
    
    if(len(tp_conf_list) > 0):
        print('Mean of confidence for true positives: ' + str(mean_tp_conf))
        print('Standard deviation of confidence for true positives: ' + 
        str(std_tp_conf))
        
    if(len(fp_conf_list) > 0):
        print('Mean of confidence for false positives: ' + 
        str(mean_fp_conf))
        print('Standard deviation of confidence for false positives: ' + 
        str(std_fp_conf))
    
    print('Mean recognition time: ' + str(mean_rec_time) + ' s\n')
        
        
def fr_VidTIMIT_experiments(params):
    '''
    Execute face recognition experiments for VidTIMIT database

    :type params: dictionary
    :param params: dictionary containing the parameters 
    to be used for the test
    ''' 
    
    rec_im_nr = 0 # Number of correctly recognized images
    test_im_nr = 0 # Number of total test images
    tp_conf_list = []
    fp_conf_list = []
    tot_rec_time = 0 # Mean time for face extraction from an image

    # Initialize dictionaries with people
    tp_dict = {}
    fp_dict = {}
    test_im_nr_dict = {}
    
    # List used for creating csv file with list of people and images
    people_and_images_list = []
    
    fm = FaceModelsLBP()

    people_nr = fm.get_people_nr()  # Number of people in face model
        
    tags = fm.get_tags()
    
    for tag in tags:
        tp_dict[tag] = 0
        fp_dict[tag] = 0
        test_im_nr_dict[tag] = 0
        
    if(params == None):
        # Load configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH)
    
    test_set_path = FACE_RECOGNITION_TEST_SET_PATH
    results_path = FACE_RECOGNITION_RESULTS_PATH
    
    if(params is not None):
        
        # Get path of directories with used files from params   
        fr_test_params = params[FACE_RECOGNITION_KEY]
        test_set_path = fr_test_params[TEST_SET_PATH_KEY]
        results_path = fr_test_params[RESULTS_PATH_KEY]
    
    # Iterate over all directories with videos
    
    tested_tags = []
    for p_dir in os.listdir(test_set_path):
        
        ann_tag = p_dir
        
        tested_tags.append(ann_tag)
        
        # List used for creating YAML file with list of images
        images_list = []
        
        person_dict = {}
        
        print 'Annotated person tag:', ann_tag
        
        # Complete path of person's directory
        p_path = os.path.join(test_set_path, p_dir)
        
        for v_dir in os.listdir(p_path):
            
            # Complete path of video directory
            v_path = os.path.join(p_path, v_dir)
        
            for im in os.listdir(v_path):
                
                # Increment number of test images for this person
                test_im_nr_dict[ann_tag] = test_im_nr_dict[ann_tag] + 1
                
                # Increment total number of test images
                test_im_nr = test_im_nr + 1
                
                # Complete path of image
                im_path = os.path.join(v_path, im)
        
                im_dict = test_on_image(im_path, ann_tag, fm) 
        
                ass_tag = im_dict[ASSIGNED_TAG_KEY]
                
                conf = im_dict[CONFIDENCE_KEY]
                
                rec_time = im_dict[ELAPSED_CPU_TIME_KEY]
                
                tot_rec_time = tot_rec_time + rec_time
        
                if(ass_tag == ann_tag):
                    
                    # Person is correctly recognized
                    im_dict[PERSON_CHECK_KEY] = 'TP'
                    tp_dict[ass_tag] = tp_dict[ass_tag] + 1
                    rec_im_nr = rec_im_nr + 1
                    tp_conf_list.append(conf)
                
                else:
                    
                    # Person is not correctly recognized
                    im_dict[PERSON_CHECK_KEY] = 'FP'
                    if(ass_tag != NO_FACE_STRING):
                        fp_dict[ass_tag] = fp_dict[ass_tag] + 1
                        fp_conf_list.append(conf)
                
                images_list.append(im_dict)
                
        person_dict[ANN_TAG_KEY] = ann_tag
        
        person_dict[IMAGES_KEY] = images_list
        
        person_file = p_dir + '.yml'
        
        person_results_path = os.path.join(results_path, person_file)
                
        save_YAML_file(person_results_path, person_dict)
        
        people_and_images_list.append(person_dict)
    
    calculate_stats(tested_tags, rec_im_nr, test_im_nr, tp_dict, 
                    fp_dict,tp_conf_list, fp_conf_list, 
                    test_im_nr_dict, tot_rec_time, results_path)
          
    csv_file_path = os.path.join(results_path, 'Results.csv')
                    
    save_results_in_csv_file(csv_file_path, people_and_images_list)


fr_VidTIMIT_experiments(None)
