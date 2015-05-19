# -*##- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import sys

from matplotlib import rcParams

sys.path.append("..")

import tools.Constants as c
import tools.Utils as utils


def plot_people_clustering_3_bboxes():
    '''
    Plot experiments for people clustering with face recognition
    and clothing recognition with 3 bounding boxes
    '''

    COMPARE_ONLY_BBOX_SIZES = False
    ITALIAN = False # True -> Italian, False -> English
    ORDER_LISTS = False

    yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-324-.yml'
    # File with corrected results for MONITOR072011
    #yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-449-473-corretti-.yml'
    
    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1000-.yml'
    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1200-.yml'
    yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1700-.yml'

    dic1 = utils.load_YAML_file(yaml_path1)

    dic2 = utils.load_YAML_file(yaml_path2)

    experiments_list = dic1[c.EXPERIMENTS_KEY]

    experiments_list.extend(dic2[c.EXPERIMENTS_KEY])

    rel_video_name = 'MONITOR072011.mpg'

    base_video_name = os.path.splitext(rel_video_name)[0]

    x_lists = {}

    prec_lists = {}

    rec_lists = {}

    f_measure_lists = {}

    time_lists = {}

    unv_time = 0
    
    if(rel_video_name == 'fic.02.mpg'):

        unv_time = 1650.53 + 12689.56 + 822.92 + 1176.06 + 1848.82

    elif(rel_video_name == 'MONITOR072011.mpg'):

        unv_time = 3143.2 + 28188.89 + 1518.76 + 2648.58 + 4498.50
    
    method_names = []

    if(COMPARE_ONLY_BBOX_SIZES):
        
        if(ITALIAN):
        
            method_names = ['Solo face recognition', '1 x 2', '1 x 1', '2 x 1', '2 x 2']
        else:
            
            method_names = ['Only face features', 'Face + clothing features (1x2)', 'Face + clothing features (1x1)', 'Face + clothing features (2x1)', 'Face + clothing features (2x2)']
            
    else:
        
        if(ITALIAN):
        
            method_names = ['Solo face recognition', '2 x 1 (1 cella)', '2 x 2 (1 cella)', '2 x 1 (3 celle)', '2 x 2 (3 celle)']
            
        else:
            
            #method_names = ['Only face features', 'Face + clothing features', '', '', '']
            method_names = ['Solo face recognition', 'Face + clothing recognition', '', '', '']

    for i in range(0, len(method_names)):

        x_lists[method_names[i]] = []

        prec_lists[method_names[i]] = []

        rec_lists[method_names[i]] = []

        f_measure_lists[method_names[i]] = []

        time_lists[method_names[i]] = []

    for exp_extended in experiments_list:

        exp = exp_extended[c.EXPERIMENT_KEY]

        video_name = exp[c.VIDEO_NAME_KEY]

        if(video_name == rel_video_name):

            # Number of clusters
            nr_clusters = exp[c.PEOPLE_CLUSTERS_NR_KEY]

            # Precision
            prec = exp[c.MEAN_PRECISION_KEY]

            rec = exp[c.MEAN_RECALL_KEY]

            f_measure = exp[c.MEAN_F1_KEY]

            models_creation_time = exp[c.CLOTH_MODELS_CREATION_TIME_KEY]

            cluster_time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]

            time = unv_time + models_creation_time + cluster_time

            use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]

            clothes_height = exp[c.CLOTHES_BBOX_HEIGHT_KEY]

            clothes_width = exp[c.CLOTHES_BBOX_WIDTH_KEY]

            use_3_bboxes = exp[c.CLOTHING_REC_USE_3_BBOXES_KEY]

            clothes_check_method = exp[c.CLOTHES_CHECK_METHOD_KEY]

            use_aggr = exp[c.USE_AGGREGATION_KEY]

            code_version = exp[c.CODE_VERSION_KEY]
            
            conf_threshold = exp[c.CONF_THRESHOLD_KEY]

            if(not(use_clothing)):

                # Only face features

                if(not(use_aggr)):

                    x_lists[method_names[0]].append(nr_clusters)

                    prec_lists[method_names[0]].append(prec)

                    rec_lists[method_names[0]].append(rec)

                    f_measure_lists[method_names[0]].append(f_measure)

                    time_lists[method_names[0]].append(time)
                    
                    if(conf_threshold < 10):
                        
                        x_lists[method_names[1]].append(nr_clusters)

                        prec_lists[method_names[1]].append(prec)
        
                        rec_lists[method_names[1]].append(rec)
        
                        f_measure_lists[method_names[1]].append(f_measure)
        
                        time_lists[method_names[1]].append(time)

            elif(code_version >= 317):

                # Face + clothing features
                
                if(COMPARE_ONLY_BBOX_SIZES):

                    if(not(use_3_bboxes)):
    
                        if((clothes_width == 1.0) and (clothes_height == 2.0)):
    
                            x_lists[method_names[1]].append(nr_clusters)
    
                            prec_lists[method_names[1]].append(prec)
    
                            rec_lists[method_names[1]].append(rec)
    
                            f_measure_lists[method_names[1]].append(f_measure)
    
                            time_lists[method_names[1]].append(time)
    
                        elif((clothes_width == 1.0) and (clothes_height == 1.0)):
    
                            x_lists[method_names[2]].append(nr_clusters)
    
                            prec_lists[method_names[2]].append(prec)
    
                            rec_lists[method_names[2]].append(rec)
    
                            f_measure_lists[method_names[2]].append(f_measure)
    
                            time_lists[method_names[2]].append(time)
    
                        elif((clothes_width == 2.0) and (clothes_height == 1.0)):
    
                            x_lists[method_names[3]].append(nr_clusters)
    
                            prec_lists[method_names[3]].append(prec)
    
                            rec_lists[method_names[3]].append(rec)
    
                            f_measure_lists[method_names[3]].append(f_measure)
    
                            time_lists[method_names[3]].append(time)
                            
                        elif((clothes_width == 2.0) and (clothes_height == 2.0)):
    
                            x_lists[method_names[4]].append(nr_clusters)
    
                            prec_lists[method_names[4]].append(prec)
    
                            rec_lists[method_names[4]].append(rec)
    
                            f_measure_lists[method_names[4]].append(f_measure)
    
                            time_lists[method_names[4]].append(time)                        
    
                else:
                    if(not(use_3_bboxes)):
    
                        if((clothes_width == 2.0) and (clothes_height == 1.0)):
    
                            x_lists[method_names[1]].append(nr_clusters)
    
                            prec_lists[method_names[1]].append(prec)
    
                            rec_lists[method_names[1]].append(rec)
    
                            f_measure_lists[method_names[1]].append(f_measure)
    
                            time_lists[method_names[1]].append(time)
    
                        elif((clothes_width == 2.0) and (clothes_height == 2.0)):
    
                            x_lists[method_names[2]].append(nr_clusters)
    
                            prec_lists[method_names[2]].append(prec)
    
                            rec_lists[method_names[2]].append(rec)
    
                            f_measure_lists[method_names[2]].append(f_measure)
    
                            time_lists[method_names[2]].append(time)
    
                    else:
                        
                        
                        if((clothes_width == 2.0) and (clothes_height == 1.0)):
    
                            x_lists[method_names[3]].append(nr_clusters)
    
                            prec_lists[method_names[3]].append(prec)
    
                            rec_lists[method_names[3]].append(rec)
    
                            f_measure_lists[method_names[3]].append(f_measure)
    
                            time_lists[method_names[3]].append(time)
                            
                        elif((clothes_width == 2.0) and (clothes_height == 2.0)):
    
                            x_lists[method_names[4]].append(nr_clusters)
    
                            prec_lists[method_names[4]].append(prec)
    
                            rec_lists[method_names[4]].append(rec)
    
                            f_measure_lists[method_names[4]].append(f_measure)
    
                            time_lists[method_names[4]].append(time)

    if(ORDER_LISTS):
        # Order lists
        for i in range(0, len(method_names)):
        
            #print('x_lists[method_names[i]]', x_lists[method_names[i]])
            
            idxs = sorted(range(len(x_lists[method_names[i]])), key=lambda k: x_lists[method_names[i]][k])
    
            #print('x_lists[method_names[i]]', x_lists[method_names[i]])
    
            # Number of clusters
            ord_x_list = []
            for idx in idxs:
                
                ord_x_list.append(x_lists[method_names[i]][idx])
                
            x_lists[method_names[i]] = ord_x_list
            
            # Precision
            ord_prec_list = []
            for idx in idxs:
                
                ord_prec_list.append(prec_lists[method_names[i]][idx])
                
            prec_lists[method_names[i]] = ord_prec_list
    
            # Recall
            ord_rec_list = []
            for idx in idxs:
                
                ord_rec_list.append(rec_lists[method_names[i]][idx])
                
            rec_lists[method_names[i]] = ord_rec_list
            
            # F-measure
            ord_f_measure_list = []
            for idx in idxs:
                
                ord_f_measure_list.append(f_measure_lists[method_names[i]][idx])
                
            f_measure_lists[method_names[i]] = ord_f_measure_list
    
    
            # Times
            ord_time_list = []
            for idx in idxs:
                
                ord_time_list.append(time_lists[method_names[i]][idx])
                
            time_lists[method_names[i]] = ord_time_list
            
            #print('x_lists[method_names[i]]',x_lists[method_names[i]])
            #print('prec_lists[method_names[i]]',prec_lists[method_names[i]])
            
            #raw_input('Aspetta poco poco')
    
    plt.figure(figsize = (8,4))
    #rcParams.update({'figure.autolayout': True})

    #plt.subplot(2,2,1)
    font_dict = {'fontsize':15}
    
    if(ITALIAN):
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
    else:
        plt.plot(
        x_lists[method_names[0]], prec_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], prec_lists[method_names[1]], 'bo--', label = method_names[1])          
     
    #plt.plot(
    #x_lists[method_names[5]], prec_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], prec_lists[method_names[6]], 'k1:', label = method_names[6])

    if(ITALIAN):
        title_str = base_video_name + ' - Precision media al variare del numero di cluster'
        plt.title(title_str)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        plt.xlabel('Number of clusters', font_dict)
    
    if(ITALIAN):
        plt.ylabel('Precision')
    else:
        plt.ylabel('Precision', font_dict)
    #plt.title('Precision')
    plt.ylim([0,1])

    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)
        #plt.tick_params(axis='both', which='major', labelsize=15)
        #plt.legend(bbox_to_anchor=(1, 0.35), fontsize = 15)

    plt.grid(True)

    plt.show()


    plt.figure(figsize = (8,4))
    #plt.subplot(2,2,2)

    if(ITALIAN):
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
    else:
        plt.plot(
        x_lists[method_names[0]], rec_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], rec_lists[method_names[1]], 'bo--', label = method_names[1])  
    #plt.plot(
    #x_lists[method_names[5]], rec_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], rec_lists[method_names[6]], 'k1:', label = method_names[6])

    if(ITALIAN):
        title_str = base_video_name + ' - Recall media al variare del numero di cluster'
        plt.title(title_str)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        plt.xlabel('Number of clusters', font_dict)

    if(ITALIAN):
        plt.ylabel('Recall')
    else:
        plt.ylabel('Recall', font_dict)
    #plt.title('Precision')
    plt.ylim([0,1])

    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)      
        #plt.legend(bbox_to_anchor=(1, 0.35), fontsize = 15)

    plt.grid(True)

    plt.show()

    plt.figure(figsize = (8,4))
    #plt.subplot(2,2,3)

    if(ITALIAN):
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
    else:
        plt.plot(
        x_lists[method_names[0]], f_measure_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], f_measure_lists[method_names[1]], 'bo--', label = method_names[1])  
        
    if(ITALIAN):
        title_str = base_video_name + ' - $F_1$ media al variare del numero di cluster'
        plt.title(title_str)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        #plt.xlabel('Number of clusters', font_dict)
        plt.xlabel('Numero di cluster', font_dict)
    
    if(ITALIAN):
        plt.ylabel('$F_1$')
    else:   
        plt.ylabel('F-measure', font_dict)
    plt.ylim([0,1])

    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        #plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)
        #plt.legend(bbox_to_anchor=(1, 0.35), fontsize = 15)
        plt.legend(bbox_to_anchor = (1,0.15), fontsize = 15)

    plt.grid(True)

    plt.show()


    fig =plt.figure(figsize = (8,4))
    #plt.subplot(2,2,3)
    ax = fig.add_subplot(111)
    
    if(ITALIAN):
        ax.plot(
        x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
        ax.plot(
        x_lists[method_names[1]], time_lists[method_names[1]], 'g+--', label = method_names[1])
        ax.plot(
        x_lists[method_names[2]], time_lists[method_names[2]], 'r*-.', label = method_names[2])
        ax.plot(
        x_lists[method_names[3]], time_lists[method_names[3]], 'cv-', label = method_names[3])
        ax.plot(
        x_lists[method_names[4]], time_lists[method_names[4]], 'bo:', label = method_names[4])
    else:
        plt.plot(
        x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], time_lists[method_names[1]], 'bo--', label = method_names[1])  
    #plt.plottime_lists
    #x_lists[method_names[5]], f_measure_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], f_measure_lists[method_names[6]], 'k1:', label = method_names[6])

    if(ITALIAN):
        title_str = base_video_name + ' - Tempo per il people clustering al variare del numero di cluster'

        # Change font size
        font_dict = {'fontsize':10}
        plt.title(title_str, font_dict)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        #plt.xlabel('Number of clusters', font_dict)
        plt.xlabel('Numero di cluster', font_dict)
    
    plt.ylabel('s', font_dict)
    #plt.title('Precision')

    if(rel_video_name == 'fic.02.mpg'):

        plt.ylim([0,25000])

    elif(rel_video_name == 'MONITOR072011.mpg'):

        plt.ylim([0,70000])

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    ax.get_yaxis().major.formatter._useMathText = True
    
    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        #plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)
        #plt.legend(bbox_to_anchor=(1, 0.35), fontsize = 15)
        plt.legend(bbox_to_anchor = (1,0.15), fontsize = 15)
    
    plt.title('"Monitor" - Tempo totale per l\'analisi')
    
    plt.grid(True)

    plt.show()

def plot_people_clustering_variable_threshold():
    '''
    Plot experiments for people clustering with face recognition
    and clothing recognition with variable/fixed threshold
    '''

    ITALIAN = True # True -> Italian, False -> English
    ORDER_LISTS = False

    yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-324-.yml'

    yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1000-.yml'
    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1200-.yml'
    
    yaml_path3 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-1400-.yml'

    dic1 = utils.load_YAML_file(yaml_path1)

    dic2 = utils.load_YAML_file(yaml_path2)
    
    dic3 = utils.load_YAML_file(yaml_path3)

    experiments_list = dic1[c.EXPERIMENTS_KEY]

    experiments_list.extend(dic2[c.EXPERIMENTS_KEY])
    
    experiments_list.extend(dic3[c.EXPERIMENTS_KEY])

    rel_video_name = 'MONITOR072011.mpg'

    base_video_name = os.path.splitext(rel_video_name)[0]

    x_lists = {}

    prec_lists = {}

    rec_lists = {}

    f_measure_lists = {}

    time_lists = {}

    unv_time = 0
    
    #if(rel_video_name == 'fic.02.mpg'):

        #unv_time = 1650.53 + 12689.56 + 822.92 + 1176.06 + 1848.82

    #elif(rel_video_name == 'MONITOR072011.mpg'):

        #unv_time = 3143.2 + 28188.89 + 1518.76 + 2648.58 + 4498.50
    
    method_names = []
        
    if(ITALIAN):
    
        method_names = ['Solo face recognition', 'k = 1', 'k variabile']
        
    else:
        
        method_names = ['Only face features', 'Face + clothing features', '', '', '']

    for i in range(0, len(method_names)):

        x_lists[method_names[i]] = []

        prec_lists[method_names[i]] = []

        rec_lists[method_names[i]] = []

        f_measure_lists[method_names[i]] = []

        time_lists[method_names[i]] = []

    for exp_extended in experiments_list:

        exp = exp_extended[c.EXPERIMENT_KEY]

        video_name = exp[c.VIDEO_NAME_KEY]

        if(video_name == rel_video_name):

            # Number of clusters
            nr_clusters = exp[c.PEOPLE_CLUSTERS_NR_KEY]

            # Precision
            prec = exp[c.MEAN_PRECISION_KEY]

            rec = exp[c.MEAN_RECALL_KEY]

            f_measure = exp[c.MEAN_F1_KEY]

            models_creation_time = exp[c.CLOTH_MODELS_CREATION_TIME_KEY]

            cluster_time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]

            time = unv_time + models_creation_time + cluster_time

            use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]

            clothes_height = exp[c.CLOTHES_BBOX_HEIGHT_KEY]

            clothes_width = exp[c.CLOTHES_BBOX_WIDTH_KEY]

            use_3_bboxes = exp[c.CLOTHING_REC_USE_3_BBOXES_KEY]

            clothes_check_method = exp[c.CLOTHES_CHECK_METHOD_KEY]

            use_aggr = exp[c.USE_AGGREGATION_KEY]

            code_version = exp[c.CODE_VERSION_KEY]
            
            variable_k = False
            
            if(c.VARIABLE_CLOTHING_THRESHOLD_KEY in exp):
            
                variable_k = exp[c.VARIABLE_CLOTHING_THRESHOLD_KEY]

            if(not(use_clothing)):

                # Only face features

                if(not(use_aggr)):

                    x_lists[method_names[0]].append(nr_clusters)

                    prec_lists[method_names[0]].append(prec)

                    rec_lists[method_names[0]].append(rec)

                    f_measure_lists[method_names[0]].append(f_measure)

                    time_lists[method_names[0]].append(time)

            elif(code_version >= 317):

                # Face + clothing features
                
                if(not(use_3_bboxes)):
    
                    if((clothes_width == 2.0) and (clothes_height == 1.0)):
                        
                        if(variable_k):
                            
                            x_lists[method_names[2]].append(nr_clusters)

                            prec_lists[method_names[2]].append(prec)
        
                            rec_lists[method_names[2]].append(rec)
        
                            f_measure_lists[method_names[2]].append(f_measure)
        
                            time_lists[method_names[2]].append(time)
                            
                        else:   

                            x_lists[method_names[1]].append(nr_clusters)
    
                            prec_lists[method_names[1]].append(prec)
    
                            rec_lists[method_names[1]].append(rec)
    
                            f_measure_lists[method_names[1]].append(f_measure)
    
                            time_lists[method_names[1]].append(time)         

    if(ORDER_LISTS):
        # Order lists
        for i in range(0, len(method_names)):
        
            #print('x_lists[method_names[i]]', x_lists[method_names[i]])
            
            idxs = sorted(range(len(x_lists[method_names[i]])), key=lambda k: x_lists[method_names[i]][k])
    
            #print('x_lists[method_names[i]]', x_lists[method_names[i]])
    
            # Number of clusters
            ord_x_list = []
            for idx in idxs:
                
                ord_x_list.append(x_lists[method_names[i]][idx])
                
            x_lists[method_names[i]] = ord_x_list
            
            # Precision
            ord_prec_list = []
            for idx in idxs:
                
                ord_prec_list.append(prec_lists[method_names[i]][idx])
                
            prec_lists[method_names[i]] = ord_prec_list
    
            # Recall
            ord_rec_list = []
            for idx in idxs:
                
                ord_rec_list.append(rec_lists[method_names[i]][idx])
                
            rec_lists[method_names[i]] = ord_rec_list
            
            # F-measure
            ord_f_measure_list = []
            for idx in idxs:
                
                ord_f_measure_list.append(f_measure_lists[method_names[i]][idx])
                
            f_measure_lists[method_names[i]] = ord_f_measure_list
    
    
            # Times
            ord_time_list = []
            for idx in idxs:
                
                ord_time_list.append(time_lists[method_names[i]][idx])
                
            time_lists[method_names[i]] = ord_time_list
            
            #print('x_lists[method_names[i]]',x_lists[method_names[i]])
            #print('prec_lists[method_names[i]]',prec_lists[method_names[i]])
            
            #raw_input('Aspetta poco poco')
    
    plt.figure()

    #plt.subplot(2,2,1)
    font_dict = {'fontsize':15}
    
    if(ITALIAN):
        plt.plot(
        x_lists[method_names[0]], prec_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], prec_lists[method_names[1]], 'g+--', label = method_names[1])
        plt.plot(
        x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = method_names[2])
    else:
        plt.plot(
        x_lists[method_names[0]], prec_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], prec_lists[method_names[1]], 'bo--', label = method_names[1])          
     
    #plt.plot(
    #x_lists[method_names[5]], prec_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], prec_lists[method_names[6]], 'k1:', label = method_names[6])

    if(ITALIAN):
        title_str = base_video_name + ' - Precision media al variare del numero di cluster'
        plt.title(title_str)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        plt.xlabel('Number of clusters', font_dict)
    
    if(ITALIAN):
        plt.ylabel('Precision')
    else:
        plt.ylabel('Precision', font_dict)
    #plt.title('Precision')
    plt.ylim([0,1])

    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)
        #plt.tick_params(axis='both', which='major', labelsize=15)

    plt.grid(True)

    plt.show()


    plt.figure()
    #plt.subplot(2,2,2)

    if(ITALIAN):
        plt.plot(
        x_lists[method_names[0]], rec_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], rec_lists[method_names[1]], 'g+--', label = method_names[1])
        plt.plot(
        x_lists[method_names[2]], rec_lists[method_names[2]], 'r*-.', label = method_names[2])
    else:
        plt.plot(
        x_lists[method_names[0]], rec_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], rec_lists[method_names[1]], 'bo--', label = method_names[1])  
    #plt.plot(
    #x_lists[method_names[5]], rec_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], rec_lists[method_names[6]], 'k1:', label = method_names[6])

    if(ITALIAN):
        title_str = base_video_name + ' - Recall media al variare del numero di cluster'
        plt.title(title_str)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        plt.xlabel('Number of clusters', font_dict)

    if(ITALIAN):
        plt.ylabel('Recall')
    else:
        plt.ylabel('Recall', font_dict)
    #plt.title('Precision')
    plt.ylim([0,1])

    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)      

    plt.grid(True)

    plt.show()

    plt.figure()
    #plt.subplot(2,2,3)

    if(ITALIAN):
        plt.plot(
        x_lists[method_names[0]], f_measure_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], f_measure_lists[method_names[1]], 'g+--', label = method_names[1])
        plt.plot(
        x_lists[method_names[2]], f_measure_lists[method_names[2]], 'r*-.', label = method_names[2])
    else:
        plt.plot(
        x_lists[method_names[0]], f_measure_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], f_measure_lists[method_names[1]], 'bo--', label = method_names[1])  
        
    if(ITALIAN):
        title_str = base_video_name + ' - $F_1$ media al variare del numero di cluster'
        plt.title(title_str)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        plt.xlabel('Number of clusters', font_dict)
    
    if(ITALIAN):
        plt.ylabel('$F_1$')
    else:   
        plt.ylabel('F-measure', font_dict)
    plt.ylim([0,1])

    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)

    plt.grid(True)

    plt.show()


    fig =plt.figure()
    #plt.subplot(2,2,3)
    ax = fig.add_subplot(111)
    
    if(ITALIAN):
        ax.plot(
        x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
        ax.plot(
        x_lists[method_names[1]], time_lists[method_names[1]], 'g+--', label = method_names[1])
        ax.plot(
        x_lists[method_names[2]], time_lists[method_names[2]], 'r*-.', label = method_names[2])
    else:
        plt.plot(
        x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
        plt.plot(
        x_lists[method_names[1]], time_lists[method_names[1]], 'bo--', label = method_names[1])  
    #plt.plottime_lists
    #x_lists[method_names[5]], f_measure_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], f_measure_lists[method_names[6]], 'k1:', label = method_names[6])

    if(ITALIAN):
        title_str = base_video_name + ' - Tempo per il people clustering al variare del numero di cluster'

        # Change font size
        font_dict = {'fontsize':10}
        plt.title(title_str, font_dict)

    if(ITALIAN):
        plt.xlabel('Numero di cluster')
    else:
        plt.xlabel('Number of clusters', font_dict)
    
    plt.ylabel('s', font_dict)
    #plt.title('Precision')

    if(rel_video_name == 'fic.02.mpg'):

        plt.ylim([0,25000])

    elif(rel_video_name == 'MONITOR072011.mpg'):

        plt.ylim([0,70000])

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    ax.get_yaxis().major.formatter._useMathText = True
    
    if(ITALIAN):
        plt.legend(bbox_to_anchor=(1, 0.34))
    else:
        plt.legend(bbox_to_anchor=(1, 0.23), fontsize = 15)

    plt.grid(True)

    plt.show()


def plot_people_clustering():
    '''
    Plot experiments for people clustering with face recognition
    and clothing recognition
    '''

    #yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\fic.02 - no clothing recognition.yml'

    yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-324-.yml'

    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-650-.yml'

    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-524-.yml'

    dic1 = utils.load_YAML_file(yaml_path1)

    #dic2 = utils.load_YAML_file(yaml_path2)

    #dic3 = utils.load_YAML_file(yaml_path3)

    experiments_list = dic1[c.EXPERIMENTS_KEY]

    #experiments_list.extend(dic2[c.EXPERIMENTS_KEY])

    #experiments_list.extend(dic3[c.EXPERIMENTS_KEY])

    # Video for which plots are to be made
    rel_video_name = 'fic.02.mpg'

    # Total unvariable time

    unv_time = 0

    if(rel_video_name == 'fic.02.mpg'):

        unv_time = 1650.53 + 12689.56 + 822.92 + 1176.06 + 1848.82

    else:

        unv_time = 3143.2 + 28188.89 + 1518.76 + 2648.58 + 4498.50

    x_lists = {}

    prec_lists = {}

    rec_lists = {}

    f_measure_lists = {}

    time_lists = {}

    #method_names = ['Only face features', 'Face + clothing features']
    method_names = ['Only face features', 'Face + clothing features (max)', 'Face + clothing features (min)']

    for i in range(0, len(method_names)):

        x_lists[method_names[i]] = []

        prec_lists[method_names[i]] = []

        rec_lists[method_names[i]] = []

        f_measure_lists[method_names[i]] = []

        time_lists[method_names[i]] = []

    for exp_extended in experiments_list:

        exp = exp_extended[c.EXPERIMENT_KEY]

        video_name = exp[c.VIDEO_NAME_KEY]

        if(video_name == rel_video_name):

            # Number of clusters
            nr_clusters = exp[c.PEOPLE_CLUSTERS_NR_KEY]

            # Precision
            prec = exp[c.MEAN_PRECISION_KEY]

            rec = exp[c.MEAN_RECALL_KEY]

            f_measure = exp[c.MEAN_F1_KEY]

            models_creation_time = exp[c.CLOTH_MODELS_CREATION_TIME_KEY]

            cluster_time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]

            time = unv_time + models_creation_time + cluster_time

            use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]

            clothes_width = exp[c.CLOTHES_BBOX_WIDTH_KEY]

            clothes_check_method = exp[c.CLOTHES_CHECK_METHOD_KEY]

            use_aggr = exp[c.USE_AGGREGATION_KEY]

            code_version = exp[c.CODE_VERSION_KEY]

            #print(clothes_check_method)

            if(not(use_clothing)):

                if(not(use_aggr)):

                    x_lists[method_names[0]].append(nr_clusters)

                    prec_lists[method_names[0]].append(prec)

                    rec_lists[method_names[0]].append(rec)

                    f_measure_lists[method_names[0]].append(f_measure)

                    time_lists[method_names[0]].append(time)

            elif(code_version >= 311):
            #else:
                if((clothes_width == 1.0) and (clothes_check_method == 'max')):

                    x_lists[method_names[1]].append(nr_clusters)

                    prec_lists[method_names[1]].append(prec)

                    rec_lists[method_names[1]].append(rec)

                    f_measure_lists[method_names[1]].append(f_measure)

                    time_lists[method_names[1]].append(time)

                elif((clothes_width == 1.0) and (clothes_check_method == 'min')):

                    x_lists[method_names[2]].append(nr_clusters)

                    prec_lists[method_names[2]].append(prec)

                    rec_lists[method_names[2]].append(rec)

                    f_measure_lists[method_names[2]].append(f_measure)

                    time_lists[method_names[2]].append(time)

    # Plots

    plt.figure()

    plt.plot(
    x_lists[method_names[0]], prec_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], prec_lists[method_names[1]], 'bo:', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], prec_lists[method_names[2]], 'gd--', label = method_names[2])

    plt.xlabel('Number of clusters')
    plt.ylabel('Precision')

    plt.ylim([0,1])

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


    plt.figure()

    plt.plot(
    x_lists[method_names[0]], rec_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], rec_lists[method_names[1]], 'bo:', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], rec_lists[method_names[2]], 'gd--', label = method_names[2])

    plt.xlabel('Number of clusters')
    plt.ylabel('Recall')

    plt.ylim([0,1])

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


    plt.figure()

    plt.plot(
    x_lists[method_names[0]], f_measure_lists[method_names[0]], 'ks-', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], f_measure_lists[method_names[1]], 'bo:', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], f_measure_lists[method_names[2]], 'gd--', label = method_names[2])


    plt.xlabel('Number of clusters')
    plt.ylabel('F-measure')

    plt.ylim([0,1])

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.plot(
    x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
    ax.plot(
    x_lists[method_names[1]], time_lists[method_names[1]], 'bo:', label = method_names[1])
    plt.plot(
    x_lists[method_names[2]], time_lists[method_names[2]], 'gd--', label = method_names[2])

    plt.xlabel('Number of clusters')
    plt.ylabel('s')

    if(rel_video_name == 'fic.02.mpg'):

        plt.ylim([15000,25000])

    else:

        pass #plt.ylim([])

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    ax.get_yaxis().major.formatter._useMathText = True

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


def plot_people_clustering_test():
    '''
    Plot experiments for people clustering with face recognition
    and clothing recognition
    '''

    #yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST 109-119 e 153-163.yml'

    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-109-.yml'

    #yaml_path3 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-172-.yml'

    #yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\fic.02 - no clothing recognition.yml'

    #yaml_path1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-524-.yml'

    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-263-.yml'

    #yaml_path2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-324-.yml'

    yaml_path1 = r'C:\Users\Maurizio\Documents\Face summarization\Test\Results\ID-TEST-574-.yml'
    
    dic1 = utils.load_YAML_file(yaml_path1)

    #dic2 = utils.load_YAML_file(yaml_path2)

    #dic3 = utils.load_YAML_file(yaml_path3)

    experiments_list = dic1[c.EXPERIMENTS_KEY]

    #experiments_list.extend(dic2[c.EXPERIMENTS_KEY])

    #experiments_list.extend(dic3[c.EXPERIMENTS_KEY])

    # Video for which plots are to be made
    rel_video_name = 'fic.02.mpg'

    base_video_name = 'fic.02'

    # Total unvariable time

    unv_time = 0

    #if(rel_video_name == 'fic.02.mpg'):

        #unv_time = 1650.53 + 12689.56 + 822.92 + 1176.06 + 1848.82

    #else:

        #unv_time = 3143.2 + 28188.89 + 1518.76 + 2648.58 + 4498.50

    x_lists = {}

    prec_lists = {}

    rec_lists = {}

    f_measure_lists = {}

    time_lists = {}

    #method_names = ['Only face recognition', 'Dominant color - Fixed x position', 'Dominant color - Variable x position', 'Whole bbox - Fixed x position', 'Whole bbox - Variable x position','Dominant color - 3 bboxes', 'Whole bbox - 3 bboxes']

    #method_names = ['Only face recognition', '2 x 1.5 - dominant color','1 x 1 - dominant color', '2 x 1.5 - whole bbox' , '1 x 1 - whole bbox']

    method_names = ['Solo face recognition', '2 x 1.5 - colore dominante','1 x 1 - colore dominante', '2 x 1.5 - bbox intero' , '1 x 1 - bbox intero']

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

            f_measure = exp[c.MEAN_F1_KEY]

            models_creation_time = exp[c.CLOTH_MODELS_CREATION_TIME_KEY]

            cluster_time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]

            time = unv_time + models_creation_time + cluster_time

            use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]

            use_aggr = exp[c.USE_AGGREGATION_KEY]

            use_dom_color = exp[c.CLOTHING_REC_USE_DOMINANT_COLOR_KEY]

            if(use_dom_color):
                print('use_dom_color', use_dom_color)

            mean_x_of_faces = exp[c.CLOTHING_REC_USE_MEAN_X_OF_FACES_KEY]

            clothes_check_method = exp[c.CLOTHES_CHECK_METHOD_KEY]

            clothes_width = exp[c.CLOTHES_BBOX_WIDTH_KEY]

            big_bbox = False

            if(clothes_width == 2.0):

                big_bbox = True

            use_3_bboxes = False

            if(c.CLOTHING_REC_USE_3_BBOXES_KEY in exp):

                use_3_bboxes = exp[c.CLOTHING_REC_USE_3_BBOXES_KEY]

            if(not(use_clothing)):

                if(not(use_aggr)):

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

                elif((clothes_check_method.lower() == 'max') and not(mean_x_of_faces)):

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
                        print('time', time)

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


    title_str = base_video_name + ' - Precision media al variare del numero di cluster'
    plt.title(title_str)

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    plt.ylabel('Precision')
    #plt.title('Precision')
    plt.ylim([0,1])

    plt.legend(bbox_to_anchor=(1, 0.34))

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

    title_str = base_video_name + ' - Recall media al variare del numero di cluster'
    plt.title(title_str)

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')

    plt.ylabel('Recall')
    #plt.title('Precision')
    plt.ylim([0,1])

    plt.legend(bbox_to_anchor=(0.56, 1))

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

    title_str = base_video_name + ' - $F_1$ media al variare del numero di cluster'
    plt.title(title_str)

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    plt.ylabel('$F_1$')
    #plt.title('Precision')
    plt.ylim([0,1])

    plt.legend(bbox_to_anchor=(0.56, 1))

    plt.grid(True)

    plt.show()


    fig =plt.figure()
    #plt.subplot(2,2,3)
    ax = fig.add_subplot(111)

    ax.plot(
    x_lists[method_names[0]], time_lists[method_names[0]], 'ks-', label = method_names[0])
    ax.plot(
    x_lists[method_names[1]], time_lists[method_names[1]], 'g+--', label = method_names[1])
    ax.plot(
    x_lists[method_names[2]], time_lists[method_names[2]], 'r*-.', label = method_names[2])
    ax.plot(
    x_lists[method_names[3]], time_lists[method_names[3]], 'cv-', label = method_names[3])
    ax.plot(
    x_lists[method_names[4]], time_lists[method_names[4]], 'bo:', label = method_names[4])
    #plt.plottime_lists
    #x_lists[method_names[5]], f_measure_lists[method_names[5]], 'm^-', label = method_names[5])
    #plt.plot(
    #x_lists[method_names[6]], f_measure_lists[method_names[6]], 'k1:', label = method_names[6])

    title_str = base_video_name + ' - Tempo per il people clustering al variare del numero di cluster'

    # Change font size
    font_dict = {'fontsize':10}
    plt.title(title_str, font_dict)

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    plt.ylabel('s')
    #plt.title('Precision')
    #plt.ylim([0,22000])

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    ax.get_yaxis().major.formatter._useMathText = True

    plt.legend(bbox_to_anchor=(0.56, 1))

    plt.grid(True)

    plt.show()


def plot_people_clustering_with_only_face_rec_experiments():
    '''
    Plot experiments for people clustering with only face recognition
    '''

    yaml_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\YAML annotazione semi-automatica\ID-TEST-324-.yml'

    dic = utils.load_YAML_file(yaml_path)

    experiments_list = dic[c.EXPERIMENTS_KEY]

    # Video for which plots are to be made
    rel_video_name = 'MONITOR072011.mpg'

    base_video_name = 'MONITOR072011'

    x_lists = {}

    prec_lists = {}

    rec_lists = {}

    f_measure_lists = {}

    cluster_time_lists = {}

    #method_names = ['Method 5', 'Method 6', 'Method 7', 'Method 8']

    #method_names = ['Majority rule', 'Min distance']

    method_names = ['Metodo 2', 'Metodo 4']

    method_5 = [True, True]

    method_6 = [True, False]

    method_7 = [False, True]

    method_8 = [False, False]

    for i in range(0, len(method_names)):

        x_lists[method_names[i]] = []

        prec_lists[method_names[i]] = []

        rec_lists[method_names[i]] = []

        f_measure_lists[method_names[i]] = []

        cluster_time_lists[method_names[i]] = []

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

            f_measure = exp[c.MEAN_F1_KEY]

            cluster_time = exp[c.PEOPLE_CLUSTERING_TIME_KEY]

            use_majority_rule = exp[c.USE_MAJORITY_RULE_KEY]

            use_nose_pos = exp[c.USE_NOSE_POS_IN_RECOGNITION_KEY]

            use_clothing = exp[c.USE_CLOTHING_RECOGNITION_KEY]

            use_aggregation = exp[c.USE_AGGREGATION_KEY]

            if(not(use_clothing)):

                if(use_aggregation):

                    x_lists[method_names[0]].append(nr_clusters)

                    prec_lists[method_names[0]].append(prec)

                    rec_lists[method_names[0]].append(rec)

                    f_measure_lists[method_names[0]].append(f_measure)

                    cluster_time_lists[method_names[0]].append(cluster_time)

                else:

                    x_lists[method_names[1]].append(nr_clusters)

                    prec_lists[method_names[1]].append(prec)

                    rec_lists[method_names[1]].append(rec)

                    f_measure_lists[method_names[1]].append(f_measure)

                    cluster_time_lists[method_names[1]].append(cluster_time)

            #if(use_majority_rule and use_nose_pos):

                #x_lists[method_names[0]].append(nr_clusters)

                #prec_lists[method_names[0]].append(prec)

            #elif(use_majority_rule and not(use_nose_pos)):

                #x_lists[method_names[1]].append(nr_clusters)

                #prec_lists[method_names[1]].append(prec)

            #elif(not(use_majority_rule) and use_nose_pos):

                #x_lists[method_names[2]].append(nr_clusters)

                #prec_lists[method_names[2]].append(prec)

            #elif(not(use_majority_rule) and not(use_nose_pos)):

                #x_lists[method_names[3]].append(nr_clusters)

                #prec_lists[method_names[3]].append(prec)

            #else:

            #   print('Warning! Method not available')

    #print('x_lists', x_lists)
    #print('prec_lists', prec_lists)

    # Change font size
    font_dict = {'fontsize':12}

    # Precision

    plt.plot(
    x_lists[method_names[0]], prec_lists[method_names[0]], 'r+--', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], prec_lists[method_names[1]], 'go-', label = method_names[1])
    #plt.plot(
    #x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = 'Method 7')
    #plt.plot(
    #x_lists[method_names[3]], prec_lists[method_names[3]], 'ks:', label = 'Method 8')

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    plt.ylabel('Precision')
    #plt.title('Precision')
    plt.ylim([0,1])

    title_str = base_video_name + ' - Precision media al variare del numero di cluster'
    plt.title(title_str, font_dict)

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


    # Recall

    plt.plot(
    x_lists[method_names[0]], rec_lists[method_names[0]], 'r+--', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], rec_lists[method_names[1]], 'go-', label = method_names[1])
    #plt.plot(
    #x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = 'Method 7')
    #plt.plot(
    #x_lists[method_names[3]], prec_lists[method_names[3]], 'ks:', label = 'Method 8')

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    plt.ylabel('Recall')
    #plt.title('Precision')
    plt.ylim([0,1])

    title_str = base_video_name + ' - Recall media al variare del numero di cluster'
    plt.title(title_str, font_dict)

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


    # F-measure

    plt.plot(
    x_lists[method_names[0]], f_measure_lists[method_names[0]], 'r+--', label = method_names[0])
    plt.plot(
    x_lists[method_names[1]], f_measure_lists[method_names[1]], 'go-', label = method_names[1])
    #plt.plot(
    #x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = 'Method 7')
    #plt.plot(
    #x_lists[method_names[3]], prec_lists[method_names[3]], 'ks:', label = 'Method 8')

    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    #plt.ylabel('F-measure')
    plt.ylabel('$F_1$')
    #plt.title('Precision')
    plt.ylim([0,1])

    title_str = base_video_name + ' - $F_1$ media al variare del numero di cluster'
    plt.title(title_str, font_dict)

    plt.legend(bbox_to_anchor=(1, 0.17))

    plt.grid(True)

    plt.show()


    # Time for clustering
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(
    x_lists[method_names[0]], cluster_time_lists[method_names[0]], 'r+--', label = method_names[0])
    ax.plot(
    x_lists[method_names[1]], cluster_time_lists[method_names[1]], 'go-', label = method_names[1])
    #plt.plot(
    #x_lists[method_names[2]], prec_lists[method_names[2]], 'r*-.', label = 'Method 7')
    #plt.plot(
    #x_lists[method_names[3]], prec_lists[method_names[3]], 'ks:', label = 'Method 8')



    #plt.xlabel('Number of clusters')
    plt.xlabel('Numero di cluster')
    plt.ylabel('s')
    #plt.title('Precision')
    #plt.ylim([0,1])

    # Change font size
    font_dict = {'fontsize':9}

    title_str = base_video_name + ' - Tempo per la face recognition al variare del numero di cluster'

    plt.title(title_str, font_dict)

    plt.legend(bbox_to_anchor=(1, 0.17))

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0), font_dict = font_dict)

    ax.get_yaxis().major.formatter._useMathText = True

    plt.grid(True)

    plt.show()


def plot_face_rec_Videolina_1040I_80P():
    '''
    Plot experiments for face recognition on datasets derived by
    dataset Videolina_1040I_80P
    '''
    yaml_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\Face recognition\Videolina-80I-80P-whole_images\FaceRecognitionExperimentsResults.yml'
    #yaml_path = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\Videolina-80I-80P-whole_images\FaceRecognitionExperimentsResults.yml'

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
    x_list, rec_lists[method_names[1]], 'gD--', label = method_names[1])

    plt.plot(
    x_list, rec_lists[method_names[2]], 'cv-', label = method_names[2])

    plt.plot(
    x_list, rec_lists[method_names[3]], 'r*-.', label = method_names[3])

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
    x_list, model_creation_time_lists[method_names[1]], 'gD--', label = method_names[1])

    plt.plot(
    x_list, model_creation_time_lists[method_names[2]], 'cv-', label = method_names[2])

    plt.plot(
    x_list, model_creation_time_lists[method_names[3]], 'r*-.', label = method_names[3])

    plt.plot(
    x_list, model_creation_time_lists[method_names[4]], 'ko-', label = method_names[4])

    plt.xlabel('Number of people')
    plt.ylabel('s')
    #plt.title('Precision')
    plt.ylim([0,1200])

    plt.legend(bbox_to_anchor=(0.77, 1))

    plt.grid(True)

    plt.show()

    # Mean recognition time

    plt.figure()

    plt.plot(
    x_list, mean_rec_time_lists[method_names[0]], 'bs:', label = method_names[0])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[1]], 'gD--', label = method_names[1])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[2]], 'cv-', label = method_names[2])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[3]], 'r*-.', label = method_names[3])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[4]], 'ko-', label = method_names[4])

    plt.xlabel('Number of people')
    plt.ylabel('s')
    #plt.title('Precision')
    plt.ylim([0,1.2])

    plt.legend(bbox_to_anchor=(1, 0.43))

    plt.grid(True)

    plt.show()

def plot_face_rec_Videolina_1040I_80P_new():
    '''
    Plot experiments for face recognition on datasets derived by
    dataset Videolina_1040I_80P
    '''
    yaml_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Test\Face recognition\Videolina-80I-80P-whole_images\FaceRecognitionExperimentsResults.yml'
    #yaml_path = r'C:\Users\Maurizio\Documents\Risultati test\Face recognition\Videolina-80I-80P-whole_images\FaceRecognitionExperimentsResults.yml'

    dic = utils.load_YAML_file(yaml_path)

    experiments_list = dic[c.EXPERIMENTS_KEY]

    method_names = [r'grid 4x4, x offset 20%, y offset 20%',
                    r'grid 4x4, x offset 30%, y offset 30%',
                    r'grid 8x8, x offset 20%, y offset 20%',
                    r'grid 8x8, x offset 30%, y offset 30%',
                    r'grid 4x8, x offset 20%, y offset 50%']

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

    fontsize = 15
    
    font_dict = {'fontsize':fontsize}
    
    # Recognition rate

    plt.figure()

    plt.plot(
    x_list, rec_lists[method_names[0]], 'bs:', label = method_names[0])

    plt.plot(
    x_list, rec_lists[method_names[1]], 'gD--', label = method_names[1])

    plt.plot(
    x_list, rec_lists[method_names[2]], 'cv-', label = method_names[2])

    plt.plot(
    x_list, rec_lists[method_names[3]], 'r*-.', label = method_names[3])

    plt.plot(
    x_list, rec_lists[method_names[4]], 'ko-', label = method_names[4])

    #plt.xlabel('Number of people', font_dict)
    plt.xlabel('Numero di persone', font_dict)
    plt.ylabel('Recognition rate', font_dict)
    #plt.title('Precision')
    plt.ylim([0,1])

    #plt.legend(bbox_to_anchor=(1, 0.43), fontsize = fontsize)
    plt.legend(bbox_to_anchor=(1, 0.36), fontsize = fontsize)

    plt.grid(True)

    plt.show()

    # Model creation time

    plt.figure()

    plt.plot(
    x_list, model_creation_time_lists[method_names[0]], 'bs:', label = method_names[0])

    plt.plot(
    x_list, model_creation_time_lists[method_names[1]], 'gD--', label = method_names[1])

    plt.plot(
    x_list, model_creation_time_lists[method_names[2]], 'cv-', label = method_names[2])

    plt.plot(
    x_list, model_creation_time_lists[method_names[3]], 'r*-.', label = method_names[3])

    plt.plot(
    x_list, model_creation_time_lists[method_names[4]], 'ko-', label = method_names[4])

    #plt.xlabel('Number of people', font_dict)
    plt.xlabel('Numero di persone', font_dict)
    plt.ylabel('s', font_dict)
    plt.title('Tempo creazione db')
    #plt.title('Precision')
    plt.ylim([0,1200])

    plt.legend(bbox_to_anchor=(0.77, 1), fontsize = fontsize)

    plt.grid(True)

    plt.show()

    # Mean recognition time

    plt.figure()

    plt.plot(
    x_list, mean_rec_time_lists[method_names[0]], 'bs:', label = method_names[0])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[1]], 'gD--', label = method_names[1])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[2]], 'cv-', label = method_names[2])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[3]], 'r*-.', label = method_names[3])

    plt.plot(
    x_list, mean_rec_time_lists[method_names[4]], 'ko-', label = method_names[4])

    #plt.xlabel('Number of people', font_dict)
    plt.xlabel('Numero di persone', font_dict)
    plt.ylabel('s', font_dict)
    plt.title('Tempi di riconoscimento medi')
    #plt.title('Precision')
    plt.ylim([0,1.2])

    #plt.legend(bbox_to_anchor=(1, 0.43), fontsize = fontsize)
    plt.legend(bbox_to_anchor=(1, 0.36), fontsize = fontsize)
    plt.grid(True)

    plt.show()


#plot_people_clustering_variable_threshold()
plot_people_clustering_3_bboxes()
#plot_people_clustering_test()
#plot_people_clustering_with_only_face_rec_experiments()
#plot_face_rec_Videolina_1040I_80P_new()
