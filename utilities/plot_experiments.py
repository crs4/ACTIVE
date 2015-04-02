import matplotlib.pyplot as plt
import os
import sys

sys.path.append("..")

import tools.Constants as c
import tools.Utils as utils 


def plot_people_clustering():
    '''
    Plot experiments for people clustering with face recognition
    and clothing recognition
    '''

    #yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST 109-119 e 153-163.yml'
    
    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-109-.yml'
    
    #yaml_path3 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-172-.yml'
    
    yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\fic.02 - no clothing recognition.yml'
    
    yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-263-.yml'
    
    dic1 = utils.load_YAML_file(yaml_path1)
    
    dic2 = utils.load_YAML_file(yaml_path2)
    
    #dic3 = utils.load_YAML_file(yaml_path3)
    
    experiments_list = dic1[c.EXPERIMENTS_KEY]
    
    experiments_list.extend(dic2[c.EXPERIMENTS_KEY])
    
    #experiments_list.extend(dic3[c.EXPERIMENTS_KEY])
    
    # Video for which plots are to be made
    rel_video_name = 'fic.02.mpg'
    
    x_lists = {}
    
    prec_lists = {}
    
    rec_lists = {}
    
    f_measure_lists = {}
    
    time_lists = {}
    
    #method_names = ['Only face recognition', 'Dominant color - Fixed x position', 'Dominant color - Variable x position', 'Whole bbox - Fixed x position', 'Whole bbox - Variable x position','Dominant color - 3 bboxes', 'Whole bbox - 3 bboxes']
     
    method_names = ['Only face recognition', '2 x 1.5 - dominant color','1 x 1 - dominant color', '2 x 1.5 - whole bbox' , '1 x 1 - whole bbox'] 
     
    method_2 = [True, True]
    
    method_3 = [True, False]
    
    method_4 = [False, True]
    
    method_5 = [False, False]
    
    for i in range(0, len(method_names)):
        
        x_lists[method_names[i]] = []
        
        prec_lists[method_names[i]] = []
        
        rec_lists[method_names[i]] = []
        
        f_measure_lists[method_names[i]] = []
        
        time_lists[method_names[i]] = []
    
    for exp_extended in experiments_list:
        
        exp = exp_extended[c.EXPERIMENT_KEY]
        
        #print('exp', exp)
        
        video_name = exp[c.VIDEO_NAME_KEY]
        
        if(video_name == rel_video_name):
            
            # Number of clusters
            nr_clusters = exp[c.PEOPLE_CLUSTERS_NR_KEY]
            
            # Precision
            prec = exp[c.MEAN_PRECISION_KEY]
            
            rec = exp[c.MEAN_RECALL_KEY]
            
            f_measure = exp[c.F1_KEY]
            
            time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]
            
            use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]
            
            use_dom_color = exp[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY]
            
            mean_x_of_faces = exp[c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]
            
            clothes_width = exp[c.CLOTHES_BBOX_WIDTH_KEY]
            
            big_bbox = False
            
            if(clothes_width == 2.0):
                
                big_bbox = True
            
            use_3_bboxes = False
            
            if(c.CLOTHING_REC_USE_3_BBOXES_KEY in exp):
            
                use_3_bboxes = exp[c.CLOTHING_REC_USE_3_BBOXES_KEY]
            
            if(not(use_clothing)):
                
                x_lists[method_names[0]].append(nr_clusters)

                prec_lists[method_names[0]].append(prec)
                
                rec_lists[method_names[0]].append(rec)  
                
                f_measure_lists[method_names[0]].append(f_measure)
                
                time_lists[method_names[0]].append(time)
                
            else:  
                
                if(use_3_bboxes):
                    
                    if(use_dom_color):
                        
                        x_lists[method_names[5]].append(nr_clusters)
                        
                        prec_lists[method_names[5]].append(prec)
                        
                        rec_lists[method_names[5]].append(rec)
                        
                        f_measure_lists[method_names[5]].append(f_measure)
                        
                    else:
                        
                        x_lists[method_names[6]].append(nr_clusters)
                        
                        prec_lists[method_names[6]].append(prec)
                        
                        rec_lists[method_names[6]].append(rec)
                        
                        f_measure_lists[method_names[6]].append(f_measure)
                        
                else:
            
                    if(use_dom_color and big_bbox):
                        
                        x_lists[method_names[1]].append(nr_clusters)
                    
                        prec_lists[method_names[1]].append(prec)
                        
                        rec_lists[method_names[1]].append(rec)
                        
                        f_measure_lists[method_names[1]].append(f_measure)
                        
                        time_lists[method_names[1]].append(time)
                        
                    elif(use_dom_color and not(big_bbox)):
                        
                        x_lists[method_names[2]].append(nr_clusters)
                        
                        prec_lists[method_names[2]].append(prec)
                        
                        rec_lists[method_names[2]].append(rec)
                        
                        f_measure_lists[method_names[2]].append(f_measure)
                        
                        time_lists[method_names[2]].append(time)
                        
                    elif(not(use_dom_color) and big_bbox):
                        
                        x_lists[method_names[3]].append(nr_clusters)
                    
                        prec_lists[method_names[3]].append(prec)
                        
                        rec_lists[method_names[3]].append(rec)
                        
                        f_measure_lists[method_names[3]].append(f_measure)
                        
                        time_lists[method_names[3]].append(time)
                        
                    elif(not(use_dom_color) and not(big_bbox)):
                        
                        x_lists[method_names[4]].append(nr_clusters)
                        
                        prec_lists[method_names[4]].append(prec)
                        
                        rec_lists[method_names[4]].append(rec)
                        
                        f_measure_lists[method_names[4]].append(f_measure)
                        
                        time_lists[method_names[4]].append(time)
                    
                    else:
                    
                        print('Warning! Method not available')
    
    plt.figure()
    
    #plt.subplot(2,2,1)
    
    plt.plot(
    x_lists[method_names[0]], prec_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], prec_lists[method_names[1]], 'g+--', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = method_names[2])
    plt.plot(
    x_lists[method_names[3]], prec_lists[method_names[3]], 'cv-', label = method_names[3])
    plt.plot(
    x_lists[method_names[4]], prec_lists[method_names[4]], 'bo:', label = method_names[4])
    #plt.plot(
    #x_lists[method_names[5]], prec_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], prec_lists[method_names[6]], 'k1:', label = method_names[6])    
    
    
    plt.xlabel('Number of clustes')
    plt.ylabel('Precision')
    #plt.title('Precision')
    plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.3))
    
    plt.grid(True)
            
    plt.show()
    
    
    plt.figure()
    #plt.subplot(2,2,2)
    
    plt.plot(
    x_lists[method_names[0]], rec_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], rec_lists[method_names[1]], 'g+--', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], rec_lists[method_names[2]], 'r*-.', label = method_names[2])
    plt.plot(
    x_lists[method_names[3]], rec_lists[method_names[3]], 'cv-', label = method_names[3])
    plt.plot(
    x_lists[method_names[4]], rec_lists[method_names[4]], 'bo:', label = method_names[4])   
    #plt.plot(
    #x_lists[method_names[5]], rec_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], rec_lists[method_names[6]], 'k1:', label = method_names[6])        
    
    plt.xlabel('Number of clustes')
    plt.ylabel('Recall')
    #plt.title('Precision')
    plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.3))
    
    plt.grid(True)
            
    plt.show()    

    plt.figure()
    #plt.subplot(2,2,3)

    plt.plot(
    x_lists[method_names[0]], f_measure_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], f_measure_lists[method_names[1]], 'g+--', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], f_measure_lists[method_names[2]], 'r*-.', label = method_names[2])
    plt.plot(
    x_lists[method_names[3]], f_measure_lists[method_names[3]], 'cv-', label = method_names[3])
    plt.plot(
    x_lists[method_names[4]], f_measure_lists[method_names[4]], 'bo:', label = method_names[4])   
    #plt.plot(
    #x_lists[method_names[5]], f_measure_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], f_measure_lists[method_names[6]], 'k1:', label = method_names[6])        
    
    plt.xlabel('Number of clustes')
    plt.ylabel('F-measure')
    #plt.title('Precision')
    plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.3))
    
    plt.grid(True)
            
    plt.show()  
    

    plt.figure()
    #plt.subplot(2,2,3)

    plt.plot(
    x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], time_lists[method_names[1]], 'g+--', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], time_lists[method_names[2]], 'r*-.', label = method_names[2])
    plt.plot(
    x_lists[method_names[3]], time_lists[method_names[3]], 'cv-', label = method_names[3])
    plt.plot(
    x_lists[method_names[4]], f_measure_lists[method_names[4]], 'bo:', label = method_names[4])   
    #plt.plottime_lists
    #x_lists[method_names[5]], f_measure_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], f_measure_lists[method_names[6]], 'k1:', label = method_names[6])        
    
    plt.xlabel('Number of clustes')
    plt.ylabel('s')
    #plt.title('Precision')
    #plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.3))
    
    plt.grid(True)
            
    plt.show()         


def plot_people_clustering_with_only_face_rec_experiments():
    '''
    Plot experiments for people clustering with only face recognition
    '''

    yaml_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-73-108.yml'
    
    dic = utils.load_YAML_file(yaml_path)
    
    experiments_list = dic[c.EXPERIMENTS_KEY]
    
    # Video for which plots are to be made
    rel_video_name = 'MONITOR072011.mpg'
    
    x_lists = {}
    
    prec_lists = {}
    
    method_names = ['Method 5', 'Method 6', 'Method 7', 'Method 8']
    
    method_5 = [True, True]
    
    method_6 = [True, False]
    
    method_7 = [False, True]
    
    method_8 = [False, False]
    
    for i in range(0, len(method_names)):
        
        x_lists[method_names[i]] = []
        
        prec_lists[method_names[i]] = []
    
    for exp_extended in experiments_list:
        
        exp = exp_extended[c.EXPERIMENT_KEY]
        
        #print('exp', exp)
        
        video_name = exp[c.VIDEO_NAME_KEY]
        
        if(video_name == rel_video_name):
            
            # Number of clusters
            nr_clusters = exp[c.PEOPLE_CLUSTERS_NR_KEY]
            
            # Precision
            prec = exp[c.MEAN_PRECISION_KEY]
            
            use_majority_rule = exp[c.USE_MAJORITY_RULE_KEY]
            
            use_nose_pos = exp[c.USE_NOSE_POS_IN_RECOGNITION_KEY]
            
            if(use_majority_rule and use_nose_pos):
                
                x_lists[method_names[0]].append(nr_clusters)
            
                prec_lists[method_names[0]].append(prec)
                
            elif(use_majority_rule and not(use_nose_pos)):
                
                x_lists[method_names[1]].append(nr_clusters)
                
                prec_lists[method_names[1]].append(prec)
                
            elif(not(use_majority_rule) and use_nose_pos):
                
                x_lists[method_names[2]].append(nr_clusters)
            
                prec_lists[method_names[2]].append(prec)
                
            elif(not(use_majority_rule) and not(use_nose_pos)):
                
                x_lists[method_names[3]].append(nr_clusters)
                
                prec_lists[method_names[3]].append(prec)
                
            else:
                
                print('Warning! Method not available')
            
    print('x_lists', x_lists)
    print('prec_lists', prec_lists)
    
    plt.plot(
    x_lists[method_names[0]], prec_lists[method_names[0]], 'bo-', label = 'Method 5')
    plt.plot(
    x_lists[method_names[1]], prec_lists[method_names[1]], 'g+--', label = 'Method 6')
    plt.plot(
    x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = 'Method 7')
    plt.plot(
    x_lists[method_names[3]], prec_lists[method_names[3]], 'ks:', label = 'Method 8')
    
    plt.xlabel('Number of clustes')
    plt.ylabel('Precision')
    #plt.title('Precision')
    plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.3))
    
    plt.grid(True)
            
    plt.show()
    
    
def plot_face_rec_Videolina_1040I_80P():
    '''    
    Plot experiments for face recognition on datasets derived by 
    dataset Videolina_1040I_80P
    '''
    yaml_path = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\Videolina-80I-80P-whole_images\FaceRecognitionExperimentsResults.yml'
    
    dic = utils.load_YAML_file(yaml_path)
    
    experiments_list = dic[c.EXPERIMENTS_KEY]
    
    method_names = [r'$LBP_{1,8},\ grid\ 4x4,\ x\ offset\ 20\%,\ y\ offset\ 20\%$', 
                    r'$LBP_{1,8},\ grid\ 4x4,\ x\ offset\ 30\%,\ y\ offset\ 30\%$',
                    r'$LBP_{1,8},\ grid\ 8x8,\ x\ offset\ 20\%,\ y\ offset\ 20\%$',
                    r'$LBP_{1,8},\ grid\ 8x8,\ x\ offset\ 30\%,\ y\ offset\ 30\%$',
                    r'$LBP_{1,8},\ grid\ 4x8,\ x\ offset\ 20\%,\ y\ offset\ 50\%$']
   
    x_list = [5,10,20,40,80]
    
    rec_lists = {}
    
    model_creation_time_lists = {}
    
    mean_rec_time_lists = {}
    
    for i in range(0, len(method_names)):
        
        rec_lists[method_names[i]] = []
        
        model_creation_time_lists[method_names[i]] = []
        
        mean_rec_time_lists[method_names[i]] = [] 
        
    for exp_extended in experiments_list:
        
        exp = exp_extended[c.EXPERIMENT_KEY]
        
        rec = exp[c.RECOGNITION_RATE_KEY]
        
        model_creation_time = exp[c.MODEL_CREATION_TIME_KEY]
        
        mean_rec_time = exp[c.MEAN_RECOGNITION_TIME_KEY]
        
        grid_y = exp[c.LBP_GRID_Y_KEY]
        
        grid_offset_pct_y = exp[c.OFFSET_PCT_Y_KEY]
        
        if((grid_y == 4) and (grid_offset_pct_y == 0.20)):
            
            rec_lists[method_names[0]].append(rec)
            
            model_creation_time_lists[method_names[0]].append(model_creation_time)
            
            mean_rec_time_lists[method_names[0]].append(mean_rec_time)
            
        elif((grid_y == 4) and (grid_offset_pct_y == 0.30)):
            
            rec_lists[method_names[1]].append(rec)
            
            model_creation_time_lists[method_names[1]].append(model_creation_time)
            
            mean_rec_time_lists[method_names[1]].append(mean_rec_time)            

        elif((grid_y == 8) and (grid_offset_pct_y == 0.20)):
            
            rec_lists[method_names[2]].append(rec)
            
            model_creation_time_lists[method_names[2]].append(model_creation_time)
            
            mean_rec_time_lists[method_names[2]].append(mean_rec_time)            
            
        elif((grid_y == 8) and (grid_offset_pct_y == 0.30)):
            
            rec_lists[method_names[3]].append(rec)
            
            model_creation_time_lists[method_names[3]].append(model_creation_time)
            
            mean_rec_time_lists[method_names[3]].append(mean_rec_time)              
            
        elif((grid_y == 8) and (grid_offset_pct_y == 0.50)):
            
            rec_lists[method_names[4]].append(rec)
            
            model_creation_time_lists[method_names[4]].append(model_creation_time)
            
            mean_rec_time_lists[method_names[4]].append(mean_rec_time)                     

        else:
                
            print('Warning! Method not available')          
            
    # Recognition rate
    
    plt.figure()
    
    plt.plot(
    x_list, rec_lists[method_names[0]], 'bs:', label = method_names[0])
    
    plt.plot(
    x_list, rec_lists[method_names[1]], 'g+--', label = method_names[1])
    
    plt.plot(
    x_list, rec_lists[method_names[2]], 'r*-.', label = method_names[2])
    
    plt.plot(
    x_list, rec_lists[method_names[3]], 'cv-', label = method_names[3])
    
    plt.plot(
    x_list, rec_lists[method_names[4]], 'ko-', label = method_names[4])
    
    plt.xlabel('Number of people')
    plt.ylabel('Recognition rate')
    #plt.title('Precision')
    plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.43))
    
    plt.grid(True)
            
    plt.show()
    
    # Model creation time
    
    plt.figure()
    
    plt.plot(
    x_list, model_creation_time_lists[method_names[0]], 'bs:', label = method_names[0])
    
    plt.plot(
    x_list, model_creation_time_lists[method_names[1]], 'g+--', label = method_names[1])
    
    plt.plot(
    x_list, model_creation_time_lists[method_names[2]], 'r*-.', label = method_names[2])
    
    plt.plot(
    x_list, model_creation_time_lists[method_names[3]], 'cv-', label = method_names[3])
    
    plt.plot(
    x_list, model_creation_time_lists[method_names[4]], 'ko-', label = method_names[4])
    
    plt.xlabel('Number of people')
    plt.ylabel('s')
    #plt.title('Precision')
    #plt.ylim([0,1])
    
    plt.legend(bbox_to_anchor=(1, 0.43))
    
    plt.grid(True)
            
    plt.show()  
    
    # Mean recognition time
    
    plt.figure()
    
    plt.plot(
    x_list, mean_rec_time_lists[method_names[0]], 'bs:', label = method_names[0])
    
    plt.plot(
    x_list, mean_rec_time_lists[method_names[1]], 'g+--', label = method_names[1])
    
    plt.plot(
    x_list, mean_rec_time_lists[method_names[2]], 'r*-.', label = method_names[2])
    
    plt.plot(
    x_list, mean_rec_time_lists[method_names[3]], 'cv-', label = method_names[3])
    
    plt.plot(
    x_list, mean_rec_time_lists[method_names[4]], 'ko-', label = method_names[4])
    
    plt.xlabel('Number of people')
    plt.ylabel('s')
    #plt.title('Precision')
    plt.ylim([0,1.2])
    
    plt.legend(bbox_to_anchor=(1, 0.43))
    
    plt.grid(True)
            
    plt.show()        
    
   
plot_people_clustering()
#plot_face_rec_Videolina_1040I_80P()
